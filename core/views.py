from django.conf import settings
from django.shortcuts import render, redirect, get_object_or_404
from django.http import Http404, HttpResponse, HttpResponseNotAllowed, HttpResponseRedirect
from django.urls import reverse
from django.utils import timezone
from django.utils.http import url_has_allowed_host_and_scheme
from django.contrib.auth import login
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.db.models import Sum, Count
from django.db.models.functions import TruncDate
from django.views.decorators.csrf import csrf_exempt
from django.views.decorators.http import require_POST
from datetime import timedelta
import csv
import stripe
from .models import PumpingSession, DailyLog, Supplement, SupplementLog, SupplementSuggestion, UserProfile
from .forms import PumpingSessionForm, SupplementForm, DailyLogForm, SignupForm
from .middleware import SKIN_COOKIE, SKIN_CHOICES, is_valid_skin


MOOD_PRESETS = ['great', 'good', 'okay', 'tired', 'frustrated']
MOOD_EMOJI = {
    'great': '😊',
    'good': '🙂',
    'okay': '😐',
    'tired': '😴',
    'frustrated': '😤',
}
BREAST_PRESETS = ['normal', 'full', 'sore', 'engorged', 'leaking']


def _combine_words(presets, custom_text):
    """Merge a list of preset values with any custom comma-separated words."""
    parts = list(presets)
    for word in custom_text.split(','):
        word = word.strip()
        if word and word not in parts:
            parts.append(word)
    return ', '.join(parts)


def _split_presets(stored, preset_list):
    """Split a stored comma-string into (matched_presets, leftover_custom_text)."""
    if not stored:
        return [], ''
    parts = [p.strip() for p in stored.split(',') if p.strip()]
    matched = [p for p in parts if p in preset_list]
    leftover = ', '.join(p for p in parts if p not in preset_list)
    return matched, leftover


def _format_h_m(minutes):
    """Render an integer minutes value as 'Xh Ym' or 'Ym'."""
    if minutes is None:
        return None
    h, m = divmod(int(minutes), 60)
    if h == 0:
        return f"{m} min"
    return f"{h} h {m} min"


@login_required
def home(request):
    today = timezone.localdate()
    user = request.user

    today_sessions_qs = PumpingSession.objects.filter(user=user, date__date=today)
    today_minutes = today_sessions_qs.aggregate(total=Sum('duration_minutes'))['total'] or 0
    today_sessions = today_sessions_qs.count()
    today_ml = today_sessions_qs.aggregate(total=Sum('total_ml'))['total'] or 0

    today_supps_taken = SupplementLog.objects.filter(user=user, date=today, taken=True).count()
    total_supps = Supplement.objects.filter(user=user).count()
    adherence_pct = (
        round(100 * today_supps_taken / total_supps) if total_supps else None
    )

    lifetime_minutes = PumpingSession.objects.filter(user=user).aggregate(
        total=Sum('duration_minutes')
    )['total'] or 0

    recent_sessions = PumpingSession.objects.filter(user=user)[:5]

    proto = _galactra_protocol_context(user)

    taken_today_ids = set(
        SupplementLog.objects
        .filter(user=user, date=today, taken=True)
        .values_list('supplement_id', flat=True)
    )
    regimen_inline = [
        {
            'name': s.name,
            'dosage': s.dosage,
            'frequency': s.frequency,
            'taken_today': s.id in taken_today_ids,
        }
        for s in Supplement.objects.filter(user=user).order_by('name')[:8]
    ]

    today_log = DailyLog.objects.filter(user=user, date=today).first()

    return render(request, 'home.html', {
        # Shared context (used by all skins)
        'today_minutes': today_minutes,
        'today_sessions': today_sessions,
        'today_supps_taken': today_supps_taken,
        'total_supps': total_supps,
        'lifetime_minutes': lifetime_minutes,
        'recent_sessions': recent_sessions,

        # Galactra-specific context
        'today_ml': today_ml,
        'adherence_pct': adherence_pct,
        'regimen_inline': regimen_inline,
        'today_log': today_log,
        **proto,
    })


def _galactra_protocol_context(user):
    """Protocol metrics reused by home() and pump_timer() for the Galactra
    overlay templates. Cheap (~3 indexed lookups). Other skins' templates
    ignore the extra context keys."""
    today = timezone.localdate()
    now = timezone.now()

    sessions = PumpingSession.objects.filter(user=user)
    first_session = sessions.order_by('date').first()
    protocol_day = (today - first_session.date.date()).days + 1 if first_session else 0

    last_session = sessions.order_by('-date').first()
    if last_session:
        minutes_since_last = int((now - last_session.date).total_seconds() // 60)
        if minutes_since_last < 60:
            session_status = 'recent'
        elif minutes_since_last < 180:
            session_status = 'due'
        else:
            session_status = 'overdue'
    else:
        minutes_since_last = None
        session_status = 'not_started'

    return {
        'protocol_day': protocol_day,
        'minutes_since_last': minutes_since_last,
        'time_since_last': _format_h_m(minutes_since_last),
        'session_status': session_status,
    }


@login_required
def pump_timer(request):
    user = request.user
    if request.method == 'POST':
        form = PumpingSessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.user = user
            session.total_ml = (session.left_ml or 0) + (session.right_ml or 0)
            session.source_skin = request.skin
            session.save()
            return redirect(f"{request.path}?just_pumped=1")
    else:
        form = PumpingSessionForm()

    today = timezone.localdate()
    today_sessions_qs = PumpingSession.objects.filter(user=user, date__date=today)
    today_minutes = today_sessions_qs.aggregate(total=Sum('duration_minutes'))['total'] or 0
    today_sessions = today_sessions_qs.count()
    today_ml = today_sessions_qs.aggregate(total=Sum('total_ml'))['total'] or 0

    ctx = {
        'form': form,
        'today_minutes': today_minutes,
        'today_sessions': today_sessions,
        'today_ml': today_ml,
    }
    ctx.update(_galactra_protocol_context(user))
    return render(request, 'pump_timer.html', ctx)


@login_required
def daily_log(request):
    today = timezone.localdate()
    user = request.user
    existing = DailyLog.objects.filter(user=user, date=today).first()

    if request.method == 'POST':
        form = DailyLogForm(request.POST, instance=existing)
        if form.is_valid():
            log = form.save(commit=False)
            log.date = today
            log.user = user
            log.mood = _combine_words(
                request.POST.getlist('mood_presets'),
                request.POST.get('mood_custom', ''),
            )
            log.breast_feeling = _combine_words(
                request.POST.getlist('breast_presets'),
                request.POST.get('breast_custom', ''),
            )
            # Preserve original source_skin on edits; only set on first save.
            if not existing:
                log.source_skin = request.skin
            log.save()
            return redirect('daily_log')
    else:
        form = DailyLogForm(instance=existing)

    stored_mood = existing.mood if existing else ''
    stored_breast = existing.breast_feeling if existing else ''
    current_mood_presets, current_mood_custom = _split_presets(stored_mood, MOOD_PRESETS)
    current_breast_presets, current_breast_custom = _split_presets(stored_breast, BREAST_PRESETS)

    mood_presets_display = [
        (value, f"{MOOD_EMOJI.get(value, '')} {value.title()}".strip())
        for value in MOOD_PRESETS
    ]
    breast_presets_display = [(value, value.title()) for value in BREAST_PRESETS]

    recent_logs = DailyLog.objects.filter(user=user).exclude(date=today)[:14]

    return render(request, 'daily_log.html', {
        'form': form,
        'today': today,
        'has_today_log': existing is not None,
        'mood_presets_display': mood_presets_display,
        'breast_presets_display': breast_presets_display,
        'current_mood_presets': current_mood_presets,
        'current_mood_custom': current_mood_custom,
        'current_breast_presets': current_breast_presets,
        'current_breast_custom': current_breast_custom,
        'recent_logs': recent_logs,
        # Field journal scale choices
        'energy_choices': DailyLog.ENERGY_CHOICES,
        'sleep_choices': DailyLog.SLEEP_CHOICES,
        'hydration_choices': DailyLog.HYDRATION_CHOICES,
        'stress_choices': DailyLog.STRESS_CHOICES,
        'existing_energy': existing.energy if existing else None,
        'existing_sleep': existing.sleep_quality if existing else None,
        'existing_hydration': existing.hydration if existing else None,
        'existing_stress': existing.stress if existing else None,
    })


@login_required
def supplements(request):
    user = request.user
    if request.method == 'POST':
        form = SupplementForm(request.POST)
        if form.is_valid():
            supp = form.save(commit=False)
            supp.user = user
            supp.source_skin = request.skin
            supp.save()
            return redirect('supplements')
    else:
        form = SupplementForm()

    today = timezone.localdate()
    taken_today_ids = set(
        SupplementLog.objects
        .filter(user=user, date=today, taken=True)
        .values_list('supplement_id', flat=True)
    )

    supplement_list = []
    for supp in Supplement.objects.filter(user=user).order_by('name'):
        supplement_list.append({
            'obj': supp,
            'taken_today': supp.id in taken_today_ids,
        })

    quick_add_names = list(
        SupplementSuggestion.objects
        .filter(is_active=True)
        .values_list('name', flat=True)
    )

    return render(request, 'supplements.html', {
        'form': form,
        'supplement_list': supplement_list,
        'quick_add_names': quick_add_names,
    })


def supplement_guide(request):
    return render(request, 'supplement_guide.html')


@login_required
def supplement_toggle(request, pk):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    supp = get_object_or_404(Supplement, pk=pk, user=request.user)
    today = timezone.localdate()
    log, created = SupplementLog.objects.get_or_create(
        supplement=supp, date=today,
        defaults={'taken': True, 'user': request.user, 'source_skin': request.skin},
    )
    if not created:
        log.delete()
    return redirect('supplements')


@login_required
def supplement_delete(request, pk):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    get_object_or_404(Supplement, pk=pk, user=request.user).delete()
    return redirect('supplements')


def privacy(request):
    return render(request, 'privacy.html')


def signup(request):
    if request.user.is_authenticated:
        return redirect('home')

    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            consent = form.cleaned_data.get('data_pooling_consent', False)
            UserProfile.objects.create(
                user=user,
                data_pooling_consent=consent,
                data_pooling_consent_at=timezone.now() if consent else None,
            )
            login(request, user)
            return redirect('home')
    else:
        form = SignupForm()

    return render(request, 'registration/signup.html', {'form': form})


def set_skin(request, skin):
    if not is_valid_skin(skin):
        raise Http404(f"Unknown skin: {skin}")

    next_url = request.GET.get('next') or request.META.get('HTTP_REFERER') or '/'
    if not url_has_allowed_host_and_scheme(
        next_url, allowed_hosts={request.get_host()}, require_https=request.is_secure()
    ):
        next_url = '/'

    response = HttpResponseRedirect(next_url)
    response.set_cookie(
        SKIN_COOKIE,
        skin,
        max_age=60 * 60 * 24 * 365,
        samesite='Lax',
    )
    return response


@login_required
def progress(request):
    try:
        days = int(request.GET.get('days', 30))
    except (TypeError, ValueError):
        days = 30
    days = max(1, min(days, 365))

    today = timezone.localdate()
    start_date = today - timedelta(days=days - 1)

    daily = (
        PumpingSession.objects
        .filter(user=request.user, date__date__gte=start_date, date__date__lte=today)
        .annotate(day=TruncDate('date'))
        .values('day')
        .annotate(minutes=Sum('duration_minutes'), ml=Sum('total_ml'), n=Count('id'))
        .order_by('day')
    )
    by_day = {row['day']: row for row in daily}

    chart_labels = []
    chart_values = []
    table_rows = []
    total_minutes = 0
    total_sessions = 0
    total_ml = 0

    for offset in range(days):
        d = start_date + timedelta(days=offset)
        row = by_day.get(d)
        minutes = row['minutes'] if row else 0
        ml = row['ml'] if row else 0
        n = row['n'] if row else 0

        chart_labels.append(f"{d:%b} {d.day}")
        chart_values.append(minutes)
        total_minutes += minutes
        total_sessions += n
        total_ml += ml
        if n > 0:
            table_rows.append({'date': d, 'minutes': minutes, 'ml': ml, 'sessions': n})

    table_rows.reverse()

    return render(request, 'progress.html', {
        'days': days,
        'chart_labels': chart_labels,
        'chart_values': chart_values,
        'table_rows': table_rows,
        'total_minutes': total_minutes,
        'total_sessions': total_sessions,
        'total_ml': total_ml,
        'window_options': [7, 30, 90],
    })


@login_required
def export_csv(request):
    user = request.user
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="mooo_data.csv"'

    writer = csv.writer(response)
    writer.writerow([
        'Date',
        'Type',
        'Duration (min)',
        'Left (ml)',
        'Right (ml)',
        'Total (ml)',
        'Mood',
        'Breast feeling',
        'Notes',
    ])

    for session in PumpingSession.objects.filter(user=user).order_by('date'):
        writer.writerow([
            session.date.strftime('%Y-%m-%d %H:%M'),
            'Pumping',
            session.duration_minutes,
            session.left_ml,
            session.right_ml,
            session.total_ml,
            '',
            '',
            session.notes,
        ])

    for log in DailyLog.objects.filter(user=user).order_by('date'):
        writer.writerow([
            log.date.strftime('%Y-%m-%d'),
            'Daily Log',
            '',
            '',
            '',
            '',
            log.mood,
            log.breast_feeling,
            log.notes,
        ])

    return response


# --- T2: Stripe purchase gate -----------------------------------------

def _stripe_configured():
    """True when both server-side keys are present. Publishable key is
    fine to expose in HTML; the price ID is a Product ref, not a secret."""
    return bool(settings.STRIPE_SECRET_KEY and settings.STRIPE_PRICE_ID)


@login_required
def purchase(request):
    """Landing page for the paywall.

    GET  → renders purchase.html with a "Buy" button (posts back here).
    POST → creates a Stripe Checkout Session server-side and redirects
           the user to Stripe's hosted page.
    """
    profile = getattr(request.user, 'profile', None)
    if profile is not None and profile.has_paid:
        return redirect('home')

    if request.method == 'POST':
        if not _stripe_configured():
            return render(request, 'purchase.html', {
                'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
                'error': (
                    'Payment is not configured on the server yet. '
                    'Please try again later.'
                ),
            }, status=503)

        stripe.api_key = settings.STRIPE_SECRET_KEY
        session = stripe.checkout.Session.create(
            mode='payment',
            line_items=[{'price': settings.STRIPE_PRICE_ID, 'quantity': 1}],
            success_url=(
                request.build_absolute_uri(reverse('purchase_success'))
                + '?session_id={CHECKOUT_SESSION_ID}'
            ),
            cancel_url=request.build_absolute_uri(reverse('purchase_cancel')),
            client_reference_id=str(request.user.id),
            customer_email=request.user.email or None,
        )
        return redirect(session.url, permanent=False)

    return render(request, 'purchase.html', {
        'stripe_publishable_key': settings.STRIPE_PUBLISHABLE_KEY,
        'stripe_configured': _stripe_configured(),
    })


@login_required
def purchase_success(request):
    """Post-purchase welcome / onboarding page.

    Stripe redirects here after a successful checkout. Marking has_paid
    happens in the webhook, NOT here — this page is untrusted. The
    session_id query param is ignored beyond display.
    """
    return render(request, 'purchase_success.html', {})


@login_required
def purchase_cancel(request):
    """Landing after a canceled Stripe Checkout."""
    return render(request, 'purchase_cancel.html', {})


@csrf_exempt
@require_POST
def stripe_webhook(request):
    """Handle Stripe webhook events.

    We care about `checkout.session.completed` — mark the referenced
    user as paid, record the Stripe customer ID and paid_at timestamp.

    Signature verification uses STRIPE_WEBHOOK_SECRET. Without it, we
    fail closed (503) — a webhook we can't verify is not a webhook we
    should trust.
    """
    if not settings.STRIPE_WEBHOOK_SECRET or not settings.STRIPE_SECRET_KEY:
        return HttpResponse(status=503)

    payload = request.body
    sig_header = request.headers.get('Stripe-Signature', '')
    stripe.api_key = settings.STRIPE_SECRET_KEY

    try:
        event = stripe.Webhook.construct_event(
            payload, sig_header, settings.STRIPE_WEBHOOK_SECRET,
        )
    except ValueError:
        return HttpResponse(status=400)
    except Exception:
        # SignatureVerificationError — catch broadly since its import
        # path shifted between stripe-python major versions.
        return HttpResponse(status=400)

    if event.get('type') == 'checkout.session.completed':
        session = event['data']['object']
        user_id = session.get('client_reference_id')
        customer_id = session.get('customer', '') or ''
        if user_id:
            try:
                user = User.objects.get(id=int(user_id))
            except (User.DoesNotExist, ValueError, TypeError):
                return HttpResponse(status=200)
            profile, _ = UserProfile.objects.get_or_create(user=user)
            profile.has_paid = True
            profile.paid_at = timezone.now()
            if customer_id:
                profile.stripe_customer_id = customer_id
            profile.save()

    return HttpResponse(status=200)
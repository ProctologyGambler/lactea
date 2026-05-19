from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, HttpResponseNotAllowed
from django.utils import timezone
from django.db.models import Sum, Count
from django.db.models.functions import TruncDate
from datetime import timedelta
import csv
from .models import PumpingSession, DailyLog, Supplement, SupplementLog
from .forms import PumpingSessionForm, SupplementForm, DailyLogForm


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


def home(request):
    today = timezone.localdate()

    today_sessions_qs = PumpingSession.objects.filter(date__date=today)
    today_minutes = today_sessions_qs.aggregate(total=Sum('duration_minutes'))['total'] or 0
    today_sessions = today_sessions_qs.count()

    today_supps_taken = SupplementLog.objects.filter(date=today, taken=True).count()
    total_supps = Supplement.objects.count()

    lifetime_minutes = PumpingSession.objects.aggregate(
        total=Sum('duration_minutes')
    )['total'] or 0

    recent_sessions = PumpingSession.objects.all()[:5]

    return render(request, 'home.html', {
        'today_minutes': today_minutes,
        'today_sessions': today_sessions,
        'today_supps_taken': today_supps_taken,
        'total_supps': total_supps,
        'lifetime_minutes': lifetime_minutes,
        'recent_sessions': recent_sessions,
    })


def pump_timer(request):
    if request.method == 'POST':
        form = PumpingSessionForm(request.POST)
        if form.is_valid():
            session = form.save(commit=False)
            session.total_ml = (session.left_ml or 0) + (session.right_ml or 0)
            session.save()
            return redirect('pump_timer')
    else:
        form = PumpingSessionForm()

    today = timezone.localdate()
    today_sessions_qs = PumpingSession.objects.filter(date__date=today)
    today_minutes = today_sessions_qs.aggregate(total=Sum('duration_minutes'))['total'] or 0
    today_sessions = today_sessions_qs.count()

    return render(request, 'pump_timer.html', {
        'form': form,
        'today_minutes': today_minutes,
        'today_sessions': today_sessions,
    })


def daily_log(request):
    today = timezone.localdate()
    existing = DailyLog.objects.filter(date=today).first()

    if request.method == 'POST':
        form = DailyLogForm(request.POST, instance=existing)
        if form.is_valid():
            log = form.save(commit=False)
            log.date = today
            log.mood = _combine_words(
                request.POST.getlist('mood_presets'),
                request.POST.get('mood_custom', ''),
            )
            log.breast_feeling = _combine_words(
                request.POST.getlist('breast_presets'),
                request.POST.get('breast_custom', ''),
            )
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

    recent_logs = DailyLog.objects.exclude(date=today)[:14]

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
    })


def supplements(request):
    if request.method == 'POST':
        form = SupplementForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('supplements')
    else:
        form = SupplementForm()

    today = timezone.localdate()
    taken_today_ids = set(
        SupplementLog.objects
        .filter(date=today, taken=True)
        .values_list('supplement_id', flat=True)
    )

    supplement_list = []
    for supp in Supplement.objects.all().order_by('name'):
        supplement_list.append({
            'obj': supp,
            'taken_today': supp.id in taken_today_ids,
        })

    quick_add_names = [
        'Fenugreek',
        'Blessed Thistle',
        "Goat's Rue",
        'Moringa',
        'Domperidone',
        'Shatavari',
    ]

    return render(request, 'supplements.html', {
        'form': form,
        'supplement_list': supplement_list,
        'quick_add_names': quick_add_names,
    })


def supplement_guide(request):
    return render(request, 'supplement_guide.html')


def supplement_toggle(request, pk):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    supp = get_object_or_404(Supplement, pk=pk)
    today = timezone.localdate()
    log, created = SupplementLog.objects.get_or_create(
        supplement=supp, date=today, defaults={'taken': True}
    )
    if not created:
        log.delete()
    return redirect('supplements')


def supplement_delete(request, pk):
    if request.method != 'POST':
        return HttpResponseNotAllowed(['POST'])
    get_object_or_404(Supplement, pk=pk).delete()
    return redirect('supplements')


def privacy(request):
    return render(request, 'privacy.html')


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
        .filter(date__date__gte=start_date, date__date__lte=today)
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


def export_csv(request):
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

    for session in PumpingSession.objects.all().order_by('date'):
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

    for log in DailyLog.objects.all().order_by('date'):
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
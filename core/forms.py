from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from .models import PumpingSession, Supplement, DailyLog

# Shared CSS classes — use skin-neutral names, styled via CSS variables
_input_cls = 'skin-input w-full rounded-2xl px-4 py-3'
_textarea_cls = 'skin-input w-full rounded-3xl px-4 py-3'


class PumpingSessionForm(forms.ModelForm):
    class Meta:
        model = PumpingSession
        fields = ['duration_minutes', 'left_ml', 'right_ml', 'notes']
        widgets = {
            'duration_minutes': forms.HiddenInput(),
            'left_ml': forms.NumberInput(attrs={
                'class': _input_cls,
                'placeholder': '0',
                'min': '0',
            }),
            'right_ml': forms.NumberInput(attrs={
                'class': _input_cls,
                'placeholder': '0',
                'min': '0',
            }),
            'notes': forms.Textarea(attrs={
                'class': _textarea_cls,
                'placeholder': 'Felt good today...',
                'rows': 3,
            }),
        }


class SupplementForm(forms.ModelForm):
    class Meta:
        model = Supplement
        fields = ['name', 'dosage', 'frequency', 'notes']
        widgets = {
            'name': forms.TextInput(attrs={
                'class': _input_cls,
                'placeholder': 'Fenugreek',
            }),
            'dosage': forms.TextInput(attrs={
                'class': _input_cls,
                'placeholder': '610 mg',
            }),
            'frequency': forms.TextInput(attrs={
                'class': _input_cls,
                'placeholder': 'three times daily',
            }),
            'notes': forms.Textarea(attrs={
                'class': _textarea_cls,
                'placeholder': 'with meals',
                'rows': 2,
            }),
        }


class DailyLogForm(forms.ModelForm):
    """Handles notes + the new field-journal fields.
    Mood and breast_feeling are posted as separate preset-checkbox +
    custom-text inputs and combined into comma-strings in the view."""

    class Meta:
        model = DailyLog
        fields = ['energy', 'sleep_quality', 'hydration', 'stress', 'tags', 'notes']
        widgets = {
            # energy/sleep_quality/hydration/stress are rendered manually in the
            # template as styled radio scales (see .skin-scale in skins.css), so
            # we don't configure widgets for them here — they only need to be in
            # `fields` above so the ModelForm picks up their POST values on save.
            'tags': forms.TextInput(attrs={
                'class': _input_cls,
                'placeholder': 'Custom tags — comma-separated (e.g. cycle-day-14, new-pump)',
            }),
            'notes': forms.Textarea(attrs={
                'class': _textarea_cls,
                'placeholder': "How are you feeling? Anything to remember about today?",
                'rows': 4,
            }),
        }


class SignupForm(UserCreationForm):
    email = forms.EmailField(
        required=True,
        widget=forms.EmailInput(attrs={
            'class': _input_cls,
            'placeholder': 'you@example.com',
        }),
    )
    data_pooling_consent = forms.BooleanField(
        required=False,
        label="Improve the insight engine for people like me by contributing anonymized session data.",
    )

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': _input_cls,
                'placeholder': 'username',
                'autocomplete': 'username',
            }),
        }

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # UserCreationForm builds password1/password2 in __init__, so we
        # style them here rather than in Meta.widgets.
        self.fields['password1'].widget.attrs.update({
            'class': _input_cls,
            'autocomplete': 'new-password',
        })
        self.fields['password2'].widget.attrs.update({
            'class': _input_cls,
            'autocomplete': 'new-password',
        })

    def clean_email(self):
        email = self.cleaned_data.get('email', '').strip().lower()
        if email and User.objects.filter(email__iexact=email).exists():
            raise forms.ValidationError("An account with this email already exists.")
        return email

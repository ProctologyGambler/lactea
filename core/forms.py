from django import forms
from .models import PumpingSession, Supplement, DailyLog


class PumpingSessionForm(forms.ModelForm):
    class Meta:
        model = PumpingSession
        fields = ['duration_minutes', 'left_ml', 'right_ml', 'notes']
        widgets = {
            'duration_minutes': forms.HiddenInput(),
            'left_ml': forms.NumberInput(attrs={
                'class': 'w-full border border-pink-300 rounded-2xl px-4 py-3',
                'placeholder': '0',
                'min': '0',
            }),
            'right_ml': forms.NumberInput(attrs={
                'class': 'w-full border border-pink-300 rounded-2xl px-4 py-3',
                'placeholder': '0',
                'min': '0',
            }),
            'notes': forms.Textarea(attrs={
                'class': 'w-full border border-pink-300 rounded-3xl px-4 py-3',
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
                'class': 'w-full border border-pink-300 rounded-2xl px-4 py-3',
                'placeholder': 'Fenugreek',
            }),
            'dosage': forms.TextInput(attrs={
                'class': 'w-full border border-pink-300 rounded-2xl px-4 py-3',
                'placeholder': '610 mg',
            }),
            'frequency': forms.TextInput(attrs={
                'class': 'w-full border border-pink-300 rounded-2xl px-4 py-3',
                'placeholder': 'three times daily',
            }),
            'notes': forms.Textarea(attrs={
                'class': 'w-full border border-pink-300 rounded-3xl px-4 py-3',
                'placeholder': 'with meals',
                'rows': 2,
            }),
        }


class DailyLogForm(forms.ModelForm):
    """Handles the notes field of DailyLog. Mood and breast_feeling are
    posted as separate preset-checkbox + custom-text inputs and combined
    into comma-strings in the view."""

    class Meta:
        model = DailyLog
        fields = ['notes']
        widgets = {
            'notes': forms.Textarea(attrs={
                'class': 'w-full border border-pink-300 rounded-3xl px-4 py-3',
                'placeholder': "How are you feeling? Anything to remember about today?",
                'rows': 4,
            }),
        }

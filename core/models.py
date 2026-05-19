from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class Profile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Profile"


class PumpingSession(models.Model):
    date = models.DateTimeField(default=timezone.now)
    duration_minutes = models.PositiveIntegerField()
    left_ml = models.PositiveIntegerField(default=0)
    right_ml = models.PositiveIntegerField(default=0)
    total_ml = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.date.date()} - {self.total_ml}ml"


class DailyLog(models.Model):
    date = models.DateField(unique=True)
    breast_feeling = models.CharField(max_length=200, blank=True)
    mood = models.CharField(max_length=200, blank=True)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return str(self.date)

    @property
    def mood_list(self):
        return [p.strip() for p in self.mood.split(',') if p.strip()] if self.mood else []

    @property
    def breast_feeling_list(self):
        return [p.strip() for p in self.breast_feeling.split(',') if p.strip()] if self.breast_feeling else []


class Supplement(models.Model):
    name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100, blank=True)
    start_date = models.DateField(default=timezone.now)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name


class SupplementLog(models.Model):
    supplement = models.ForeignKey(Supplement, on_delete=models.CASCADE)
    date = models.DateField()
    taken = models.BooleanField(default=True)
    notes = models.TextField(blank=True)

    class Meta:
        unique_together = ('supplement', 'date')
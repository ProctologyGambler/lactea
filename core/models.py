from django.db import models
from django.utils import timezone
from django.contrib.auth.models import User


class UserProfile(models.Model):
    """Per-user metadata beyond what django.contrib.auth ships. Consent
    lives here; monetization fields (has_paid, paid_at, stripe_customer_id,
    refunded_at) land here in T2."""

    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    data_pooling_consent = models.BooleanField(default=False)
    data_pooling_consent_at = models.DateTimeField(null=True, blank=True)

    # Reserved for T2 (Stripe gate). Kept nullable so pre-launch accounts
    # don't need a schema change when payment ships.
    has_paid = models.BooleanField(default=False)
    paid_at = models.DateTimeField(null=True, blank=True)
    stripe_customer_id = models.CharField(max_length=64, blank=True, default='')
    refunded_at = models.DateTimeField(null=True, blank=True)

    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Profile: {self.user.username}"


class PumpingSession(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='pumping_sessions')
    date = models.DateTimeField(default=timezone.now)
    duration_minutes = models.PositiveIntegerField()
    left_ml = models.PositiveIntegerField(default=0)
    right_ml = models.PositiveIntegerField(default=0)
    total_ml = models.PositiveIntegerField(default=0)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    source_skin = models.CharField(max_length=32, db_index=True, default='unknown')

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return f"{self.date.date()} - {self.total_ml}ml"


class DailyLog(models.Model):
    ENERGY_CHOICES = [
        (1, 'Very low'),
        (2, 'Low'),
        (3, 'Moderate'),
        (4, 'Good'),
        (5, 'Great'),
    ]
    SLEEP_CHOICES = [
        (1, 'Terrible'),
        (2, 'Poor'),
        (3, 'Okay'),
        (4, 'Good'),
        (5, 'Great'),
    ]
    HYDRATION_CHOICES = [
        (1, 'Dehydrated'),
        (2, 'Could be better'),
        (3, 'Well hydrated'),
    ]
    STRESS_CHOICES = [
        (1, 'Very low'),
        (2, 'Low'),
        (3, 'Moderate'),
        (4, 'High'),
        (5, 'Very high'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='daily_logs')
    date = models.DateField()
    breast_feeling = models.CharField(max_length=200, blank=True)
    mood = models.CharField(max_length=200, blank=True)
    energy = models.PositiveSmallIntegerField(choices=ENERGY_CHOICES, null=True, blank=True)
    sleep_quality = models.PositiveSmallIntegerField(choices=SLEEP_CHOICES, null=True, blank=True)
    hydration = models.PositiveSmallIntegerField(choices=HYDRATION_CHOICES, null=True, blank=True)
    stress = models.PositiveSmallIntegerField(choices=STRESS_CHOICES, null=True, blank=True)
    tags = models.CharField(max_length=500, blank=True, help_text="Comma-separated custom tags")
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    source_skin = models.CharField(max_length=32, db_index=True, default='unknown')

    class Meta:
        ordering = ['-date']
        constraints = [
            models.UniqueConstraint(fields=['user', 'date'], name='unique_dailylog_per_user_date'),
        ]

    def __str__(self):
        return str(self.date)

    @property
    def mood_list(self):
        return [p.strip() for p in self.mood.split(',') if p.strip()] if self.mood else []

    @property
    def breast_feeling_list(self):
        return [p.strip() for p in self.breast_feeling.split(',') if p.strip()] if self.breast_feeling else []

    @property
    def tags_list(self):
        return [t.strip() for t in self.tags.split(',') if t.strip()] if self.tags else []


class Supplement(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='supplements')
    name = models.CharField(max_length=100)
    dosage = models.CharField(max_length=100)
    frequency = models.CharField(max_length=100, blank=True)
    start_date = models.DateField(default=timezone.now)
    notes = models.TextField(blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    source_skin = models.CharField(max_length=32, db_index=True, default='unknown')

    def __str__(self):
        return self.name


class SupplementSuggestion(models.Model):
    """Quick-add suggestions shown on the supplements page. Editable via
    admin so the list can grow with community input without a code deploy."""

    name = models.CharField(max_length=100, unique=True)
    display_order = models.PositiveSmallIntegerField(default=100)
    is_active = models.BooleanField(default=True)

    class Meta:
        ordering = ['display_order', 'name']

    def __str__(self):
        return self.name


class SupplementLog(models.Model):
    user = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True, related_name='supplement_logs')
    supplement = models.ForeignKey(Supplement, on_delete=models.CASCADE)
    date = models.DateField()
    taken = models.BooleanField(default=True)
    notes = models.TextField(blank=True)
    source_skin = models.CharField(max_length=32, db_index=True, default='unknown')

    class Meta:
        unique_together = ('supplement', 'date')

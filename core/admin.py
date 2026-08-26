from django.contrib import admin
from .models import PumpingSession, DailyLog, Supplement, SupplementLog, SupplementSuggestion, UserProfile


@admin.register(PumpingSession)
class PumpingSessionAdmin(admin.ModelAdmin):
    list_display = ('date', 'user', 'duration_minutes', 'total_ml', 'left_ml', 'right_ml', 'source_skin', 'notes')
    list_filter = ('user', 'source_skin', 'date')
    search_fields = ('notes', 'user__username')
    ordering = ('-date',)


@admin.register(DailyLog)
class DailyLogAdmin(admin.ModelAdmin):
    list_display = ('date', 'user', 'mood', 'breast_feeling', 'energy', 'sleep_quality', 'hydration', 'stress', 'tags', 'source_skin', 'notes')
    list_filter = ('user', 'source_skin', 'date', 'energy', 'sleep_quality', 'hydration', 'stress')
    search_fields = ('mood', 'breast_feeling', 'tags', 'notes', 'user__username')
    ordering = ('-date',)


@admin.register(Supplement)
class SupplementAdmin(admin.ModelAdmin):
    list_display = ('name', 'user', 'dosage', 'frequency', 'start_date', 'source_skin')
    list_filter = ('user', 'source_skin')
    search_fields = ('name', 'notes', 'user__username')
    ordering = ('name',)


@admin.register(SupplementLog)
class SupplementLogAdmin(admin.ModelAdmin):
    list_display = ('supplement', 'user', 'date', 'taken', 'source_skin')
    list_filter = ('user', 'source_skin', 'date', 'taken')
    ordering = ('-date',)


@admin.register(SupplementSuggestion)
class SupplementSuggestionAdmin(admin.ModelAdmin):
    list_display = ('name', 'display_order', 'is_active')
    list_editable = ('display_order', 'is_active')
    list_filter = ('is_active',)
    search_fields = ('name',)
    ordering = ('display_order', 'name')


@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ('user', 'data_pooling_consent', 'data_pooling_consent_at', 'has_paid', 'paid_at', 'refunded_at')
    list_filter = ('data_pooling_consent', 'has_paid')
    search_fields = ('user__username', 'user__email', 'stripe_customer_id')
    readonly_fields = ('created_at',)

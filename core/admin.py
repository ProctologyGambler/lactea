from django.contrib import admin
from .models import PumpingSession, DailyLog, Supplement, SupplementLog


@admin.register(PumpingSession)
class PumpingSessionAdmin(admin.ModelAdmin):
    list_display = ('date', 'duration_minutes', 'total_ml', 'left_ml', 'right_ml', 'notes')
    list_filter = ('date',)
    search_fields = ('notes',)
    ordering = ('-date',)


@admin.register(DailyLog)
class DailyLogAdmin(admin.ModelAdmin):
    list_display = ('date', 'mood', 'breast_feeling', 'notes')
    list_filter = ('date',)
    search_fields = ('mood', 'breast_feeling', 'notes')
    ordering = ('-date',)


@admin.register(Supplement)
class SupplementAdmin(admin.ModelAdmin):
    list_display = ('name', 'dosage', 'frequency', 'start_date')
    search_fields = ('name', 'notes')
    ordering = ('name',)


@admin.register(SupplementLog)
class SupplementLogAdmin(admin.ModelAdmin):
    list_display = ('supplement', 'date', 'taken')
    list_filter = ('date', 'taken')
    ordering = ('-date',)

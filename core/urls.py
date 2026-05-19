from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('pump/', views.pump_timer, name='pump_timer'),
    path('daily-log/', views.daily_log, name='daily_log'),
    path('supplements/', views.supplements, name='supplements'),
    path('supplements/guide/', views.supplement_guide, name='supplement_guide'),
    path('supplements/<int:pk>/toggle/', views.supplement_toggle, name='supplement_toggle'),
    path('supplements/<int:pk>/delete/', views.supplement_delete, name='supplement_delete'),
    path('progress/', views.progress, name='progress'),
    path('privacy/', views.privacy, name='privacy'),
    path('export/', views.export_csv, name='export_csv'),
]
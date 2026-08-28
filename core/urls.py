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
    path('theme/<str:skin>/', views.set_skin, name='set_skin'),
    path('signup/', views.signup, name='signup'),

    # T2: Stripe purchase gate (Galactra skin only, enforced in middleware).
    path('purchase/', views.purchase, name='purchase'),
    path('purchase/success/', views.purchase_success, name='purchase_success'),
    path('purchase/cancel/', views.purchase_cancel, name='purchase_cancel'),
    path('stripe/webhook/', views.stripe_webhook, name='stripe_webhook'),
]
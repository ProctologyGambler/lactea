"""
URL configuration for lactea_backend project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/6.0/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.views.generic import TemplateView

urlpatterns = [
    path('admin/', admin.site.urls),
    # Django's built-in auth: login, logout, password_change, password_reset flow.
    # Signup lives in core.urls (Django doesn't ship one).
    path('accounts/', include('django.contrib.auth.urls')),
    # Service worker must be served from site root so it can control the whole site.
    # Served as a Django template so the cache list can use {% url %} and {% static %}.
    path('sw.js', TemplateView.as_view(
        template_name='sw.js',
        content_type='application/javascript',
    ), name='service_worker'),
    path('', include('core.urls')),   # This connects to our main app
]
"""
core/middleware.py — Skin middleware.

Two ways a request gets a skin, in priority order:

  1. Hostname lock (production). settings.SKIN_BY_HOST maps a host string
     to a skin name; if the request's Host matches, that skin is forced
     and request.skin_locked is True. This is how separate marketing
     domains (lactea.app, vialactea.app, galactra.health) end up serving
     three discrete products from one Django process — and how a Galactra
     visitor is prevented from ever encountering the Lactea brand.

  2. Cookie toggle (dev / unmapped hosts). The `skin` cookie picks the
     skin; invalid or missing values fall back to SKIN_DEFAULT. This is
     what the footer skin picker uses.

Either way, the active skin is stashed in skins.runtime via
set_current_skin() so the SkinOverlayLoader can read it when resolving
templates. Cleared in a finally block so a hung view can't leak state
into the next request on the same thread.
"""

from django.conf import settings

from skins.loader import get_available_skins
from skins.runtime import set_current_skin, clear_current_skin

SKIN_COOKIE = "skin"
SKIN_DEFAULT = "via_lactea"

# Built once at import time from the skins/ directory contents.
# Add a skin folder → restart the dev server.
SKIN_CHOICES = tuple(s["name"] for s in get_available_skins()) or (SKIN_DEFAULT,)


def is_valid_skin(value):
    return value in SKIN_CHOICES


def _host_skin(request):
    """Return the skin forced by request.Host, or None."""
    skin_by_host = getattr(settings, "SKIN_BY_HOST", {}) or {}
    if not skin_by_host:
        return None
    host = request.get_host().split(":", 1)[0].lower()
    forced = skin_by_host.get(host)
    if forced and is_valid_skin(forced):
        return forced
    return None


class SkinMiddleware:
    def __init__(self, get_response):
        self.get_response = get_response

    def __call__(self, request):
        forced = _host_skin(request)
        if forced:
            request.skin = forced
            request.skin_locked = True
        else:
            value = request.COOKIES.get(SKIN_COOKIE)
            request.skin = value if is_valid_skin(value) else SKIN_DEFAULT
            request.skin_locked = False

        set_current_skin(request.skin)
        try:
            return self.get_response(request)
        finally:
            clear_current_skin()

"""
core/context_processors.py — Inject skin data into every template context.

Provides:
    {{ c.<underscored_key> }} — flat copy dict (dots → underscores so Django
                                templates can dot-access keys)
    {{ skin_config }}         — full skin.json dict (palette, features, sounds, pwa)
    {{ skin_features }}       — just the features dict for convenience
    {{ available_skins }}     — list of all installed skins (for theme picker)
    {{ skin_sound_urls }}     — slot → resolved static URL, ready to be JSON-scripted
                                so the sound layer can play any slot
"""

from django.templatetags.static import static
from skins.loader import get_skin_copy, get_skin_config, get_skin_features, get_available_skins


def skin_context(request):
    """Add skin copy + config to the template context."""
    skin_name = getattr(request, "skin", "via_lactea")

    raw_copy = get_skin_copy(skin_name)
    c = {key.replace(".", "_"): value for key, value in raw_copy.items()}

    config = get_skin_config(skin_name)
    sound_urls = {
        slot: static(f"sounds/{filename}")
        for slot, filename in config.get("sounds", {}).items()
    }

    return {
        "c": c,
        "skin_config": config,
        "skin_features": get_skin_features(skin_name),
        "available_skins": get_available_skins(),
        "skin_sound_urls": sound_urls,
    }

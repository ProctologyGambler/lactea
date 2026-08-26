"""
skins/loader.py — Load and cache skin configuration + copy.

Usage:
    from skins.loader import get_skin_config, get_skin_copy

    config = get_skin_config("cow")   # dict from skin.json
    copy   = get_skin_copy("cow")     # base copy merged with skin overrides

Adding a new skin:
    1. Create  skins/<name>/skin.json   (palette, features, sounds, pwa)
    2. Create  skins/<name>/copy.py     (COPY dict — only override what differs)
    3. Create  templates/skins/<name>/  with the partial templates
    4. Add  "<name>"  to  SKIN_CHOICES  in  core/middleware.py
    Done.
"""

import json
import importlib
from pathlib import Path
from functools import lru_cache

SKINS_DIR = Path(__file__).resolve().parent


@lru_cache(maxsize=None)
def get_skin_config(skin_name: str) -> dict:
    """Load and cache skin.json for the given skin."""
    skin_json = SKINS_DIR / skin_name / "skin.json"
    if not skin_json.exists():
        return {}
    with open(skin_json) as f:
        return json.load(f)


@lru_cache(maxsize=None)
def _load_copy_module(skin_name: str) -> dict:
    """Import a skin's copy.py and return its COPY dict."""
    try:
        mod = importlib.import_module(f"skins.{skin_name}.copy")
        return getattr(mod, "COPY", {})
    except (ImportError, ModuleNotFoundError):
        return {}


@lru_cache(maxsize=None)
def get_skin_copy(skin_name: str) -> dict:
    """Return base copy merged with skin-specific overrides."""
    base = _load_copy_module("_base")
    skin = _load_copy_module(skin_name) if skin_name != "_base" else {}
    return {**base, **skin}


def get_skin_features(skin_name: str) -> dict:
    """Convenience: return just the features dict from skin.json."""
    config = get_skin_config(skin_name)
    return config.get("features", {})


def get_skin_palette(skin_name: str) -> dict:
    """Convenience: return just the palette dict from skin.json."""
    config = get_skin_config(skin_name)
    return config.get("palette", {})


def get_available_skins() -> list[dict]:
    """Return a list of {name, display_name, description} for all installed skins."""
    skins = []
    for child in sorted(SKINS_DIR.iterdir()):
        if child.is_dir() and not child.name.startswith("_") and (child / "skin.json").exists():
            config = get_skin_config(child.name)
            skins.append({
                "name": child.name,
                "display_name": config.get("display_name", child.name),
                "description": config.get("description", ""),
            })
    return skins

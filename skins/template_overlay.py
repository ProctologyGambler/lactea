"""
skins/template_overlay.py — Custom Django filesystem template loader that
makes every template lookup skin-aware.

For each request, the loader prepends `templates/skins/<current_skin>/`
to its search path. So:

    {% extends "base.html" %}
    {% include "_brand_nav.html" %}
    render(request, "home.html", ...)

all resolve to the active skin's version if one exists, otherwise fall
through to the shared `templates/<name>` file. This means a skin can
override anything from a single partial up to a whole page — without
any `{% if request.skin == "..." %}` branches in shared templates.

The skin name comes from skins.runtime.get_current_skin(), which the
SkinMiddleware sets per request.

Setup (in settings.TEMPLATES):

    'OPTIONS': {
        'loaders': [
            'skins.template_overlay.SkinOverlayLoader',
            'django.template.loaders.app_directories.Loader',
        ],
        ...
    }

Note: when using explicit 'loaders', you must also set 'APP_DIRS': False
on the template engine (Django enforces they are mutually exclusive).
"""

from pathlib import Path

from django.template.loaders.filesystem import Loader as FilesystemLoader

from skins.runtime import get_current_skin


class SkinOverlayLoader(FilesystemLoader):
    """
    Filesystem loader that searches templates/skins/<current_skin>/ first.

    Falls back to the engine's configured DIRS (i.e. templates/) when no
    skin is active or when the skin doesn't have a file by that name.
    """

    def get_dirs(self):
        base_dirs = list(self.engine.dirs)
        skin = get_current_skin()
        if not skin:
            return base_dirs
        overlay_dirs = [Path(d) / "skins" / skin for d in base_dirs]
        return overlay_dirs + base_dirs

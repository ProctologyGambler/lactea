"""
skins/runtime.py — Per-request skin state, made available to the template
loader and any other code that doesn't naturally have request access.

The SkinMiddleware calls set_current_skin() at the start of each request
and clears it at the end. The SkinOverlayLoader reads it via
get_current_skin() to decide which overlay directory to search first.

Thread-local because Django can serve concurrent requests from a single
process (e.g. under gunicorn workers with threads, or async views). A
plain module global would leak the previous request's skin into whichever
request happened to run next on the same thread.
"""

import threading

_local = threading.local()


def set_current_skin(skin_name):
    """Stash the active skin for the current request/thread."""
    _local.skin = skin_name


def get_current_skin():
    """Return the active skin name, or None if no request is in progress."""
    return getattr(_local, "skin", None)


def clear_current_skin():
    """Drop the per-request skin state. Call at the end of each request."""
    if hasattr(_local, "skin"):
        del _local.skin

# Lactea — Codebase Snapshot

**Last updated:** 2026-05-23

A gentle Django web app for people inducing lactation without pregnancy. Tracks pumping sessions, supplements, and daily mood/body state, with a research-backed supplement guide and CSV export. Single-user prototype today; longer-term direction is local-first (data on device). MIT licensed.

This document is the fast path from zero to productive contributor. For user-facing docs see [`README.md`](README.md). For ongoing strategy/decision notes see [`task.md`](task.md).

---

## TL;DR for a new contributor

- **Stack:** Django 5 + SQLite + django-htmx + Tailwind (Play CDN, vendored locally) + Chart.js. WhiteNoise + Gunicorn for prod. PWA via manifest + service worker.
- **One Django app:** `core/`. One settings module: `mooo_backend/`.
- **No tests yet** (`core/tests.py` is empty). No CI. Single developer, single SQLite file.
- **Active work-in-progress on `main` (uncommitted):** a **skin system** that lets the UI swap between named themes (currently `plain` and `cow`). This is the architectural centerpiece of where the product is going. See [Skin system](#the-skin-system) below.
- **Auth:** none yet. Anyone hitting the server is treated as the single user. A `Profile` model exists but is unused.

---

## Quick start

```bash
git clone <repo> lactea && cd lactea
python -m venv venv && source venv/bin/activate
pip install -r requirements.txt

cp .env.example .env
# Replace SECRET_KEY in .env with:
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

python manage.py migrate
python manage.py createsuperuser   # optional, for /admin/
python manage.py runserver
```

Open <http://127.0.0.1:8000>.

**Env vars** (`.env`): `SECRET_KEY`, `DEBUG` (default `True`), `ALLOWED_HOSTS` (default `127.0.0.1,localhost`).

---

## Project layout

```
mooo_prototype1/
├── core/                       # The one Django app
│   ├── models.py               # PumpingSession, DailyLog, Supplement, SupplementLog, Profile
│   ├── views.py                # All views (function-based)
│   ├── forms.py                # ModelForms for pumping, supplement, daily log
│   ├── urls.py                 # App-level routes
│   ├── admin.py                # Django admin registrations
│   ├── middleware.py           # SkinMiddleware — reads `skin` cookie → request.skin
│   └── migrations/
├── mooo_backend/               # Django project (settings + root urls)
│   ├── settings.py
│   └── urls.py                 # Mounts /admin, /sw.js, and includes core.urls at /
├── templates/
│   ├── base.html               # Layout: nav, footer, theme toggle, SW registration
│   ├── home.html
│   ├── pump_timer.html
│   ├── daily_log.html
│   ├── supplements.html
│   ├── supplement_guide.html
│   ├── progress.html
│   ├── privacy.html
│   ├── sw.js                   # Service worker (templated so it can use {% static %})
│   └── skins/                  # Per-skin partials (NEW, uncommitted)
│       ├── cow/   {_brand_head, _brand_nav, _end_sound, _pump_button}.html
│       └── plain/ {_brand_head, _brand_nav, _end_sound, _pump_button}.html
├── static/
│   ├── css/skins.css           # Skin CSS variables / per-skin overrides (NEW)
│   ├── js/                     # timer.js, charts.js, vendored tailwind.js + chart.min.js
│   ├── images/                 # cow-*.svg, drop-icon.svg (NEW for plain skin)
│   ├── sounds/                 # lactea.mp3, chime.mp3 (NEW for plain skin)
│   └── manifest.json           # PWA manifest
├── db.sqlite3                  # Local dev DB (gitignored in practice; currently present)
├── .env / .env.example
├── manage.py
├── requirements.txt
├── README.md                   # User-facing intro & setup
├── task.md                     # Decision log / conversation summaries
└── ONBOARDING.md               # This file
```

---

## Data model (`core/models.py`)

| Model              | Purpose                                                       | Notable fields                                                                 |
| ------------------ | ------------------------------------------------------------- | ------------------------------------------------------------------------------ |
| `PumpingSession`   | One pumping session                                           | `date` (datetime), `duration_minutes`, `left_ml`, `right_ml`, `total_ml`, `notes` |
| `DailyLog`         | One row per day (`unique=True` on date)                       | `mood` (comma-string), `breast_feeling` (comma-string), `notes`               |
| `Supplement`       | A supplement the user is taking                               | `name`, `dosage`, `frequency`, `start_date`, `notes`                          |
| `SupplementLog`    | Did the user take supplement X on day Y? (`unique_together`)  | FK → Supplement, `date`, `taken`                                              |
| `Profile`          | Defined but unused                                            | OneToOne with `User`                                                          |

**Conventions worth knowing:**
- `mood` and `breast_feeling` on `DailyLog` are stored as comma-separated strings, not a many-to-many. Helpers in `views.py` (`_combine_words`, `_split_presets`) handle the merge of preset checkboxes + custom free-text. Convenience properties `mood_list` / `breast_feeling_list` parse them back.
- `PumpingSession.total_ml` is computed in the view (`pump_timer`) as `left_ml + right_ml`, not on the model. Don't double-set it elsewhere.
- `SupplementLog` toggling: if a log row exists for `(supplement, today)` and you POST to the toggle endpoint, the row is **deleted** rather than flipped to `taken=False`. The presence of a row means "taken today."

---

## URL → view → template map

All routes are function-based views in `core/views.py`. Routes are included at root from `mooo_backend/urls.py`.

| Path                                  | View                  | Template                  | Method      |
| ------------------------------------- | --------------------- | ------------------------- | ----------- |
| `/`                                   | `home`                | `home.html`               | GET         |
| `/pump/`                              | `pump_timer`          | `pump_timer.html`         | GET, POST   |
| `/daily-log/`                         | `daily_log`           | `daily_log.html`          | GET, POST   |
| `/supplements/`                       | `supplements`         | `supplements.html`        | GET, POST   |
| `/supplements/guide/`                 | `supplement_guide`    | `supplement_guide.html`   | GET         |
| `/supplements/<pk>/toggle/`           | `supplement_toggle`   | — (redirects)             | POST only   |
| `/supplements/<pk>/delete/`           | `supplement_delete`   | — (redirects)             | POST only   |
| `/progress/?days=7|30|90`             | `progress`            | `progress.html`           | GET         |
| `/privacy/`                           | `privacy`             | `privacy.html`            | GET         |
| `/export/`                            | `export_csv`          | — (CSV response)          | GET         |
| `/theme/<skin>/?next=/some/path`      | `set_skin`            | — (sets cookie, redirects)| GET         |
| `/sw.js`                              | `TemplateView`        | `sw.js`                   | GET         |
| `/admin/`                             | Django admin          | —                         | —           |

---

## The skin system

This is the centerpiece of where the product is heading. **Status: half-built, uncommitted on `main`.**

**Goal:** one codebase, multiple swappable skins so we can serve distinct niche communities of practice (different aesthetics, language, iconography, sound) without forking. See `task.md` for product rationale.

**How it works today:**

1. **Middleware** — `core/middleware.py` (`SkinMiddleware`) reads the `skin` cookie on every request and attaches `request.skin` (defaults to `plain`; only values in `SKIN_CHOICES = ("plain", "cow")` are accepted).
2. **View** — `set_skin(request, skin)` at `/theme/<skin>/` sets the cookie (1-year max-age, `SameSite=Lax`) and redirects back to `?next=` (validated with Django's `url_has_allowed_host_and_scheme` to prevent open-redirect).
3. **Templates** — `base.html` includes per-skin partials via `{% include "skins/"|add:request.skin|add:"/_brand_head.html" %}` for `_brand_head`, `_brand_nav`, `_end_sound`, `_pump_button`. Other templates (`home.html`, `pump_timer.html`) include the relevant partial in place of the previously hardcoded cow asset.
4. **CSS** — `static/css/skins.css` carries skin-specific styles; the `<body data-skin="…">` attribute lets selectors scope by skin.
5. **Toggle UI** — the footer in `base.html` shows a Plain / Cow link pair.

**Design intent (where this is heading, per current strategy notes):**
- Skins should differ in **copy** too, not just visuals. Plan: small Python dict per skin (`skins/<name>/copy.py`) loaded via context processor.
- Skins should be **drop-in**: a `skins/<name>/skin.json` manifest declaring display name, palette, copy overrides, and which optional features show up. Adding a niche = drop a folder.
- Skin partials should never contain core business logic — only branding/copy/asset choices.

**Known small bug** — `set_skin` returns `HttpResponseNotAllowed(['POST', 'GET'])` (HTTP 405) when the skin name is invalid. 405 means "wrong HTTP method." Should be `HttpResponseBadRequest` (400) or `Http404`.

---

## PWA setup

- **Manifest:** `static/manifest.json` (linked from `base.html`).
- **Service worker:** `templates/sw.js` served at `/sw.js` via `TemplateView` so it lives at site root (required to control the whole origin) **and** can use `{% static %}` for cache URLs.
- **Registration:** inline `<script>` at the bottom of `base.html`.
- **Caching tier:** Tier 1 — caches the app shell. Offline *reads* work after first visit; offline *writes* are not implemented yet.
- Future direction: local-first (data on device). PWA infra is already in place to support that pivot.

---

## Production notes

- **Static files:** `STATICFILES_STORAGE = 'whitenoise.storage.CompressedManifestStaticFilesStorage'`. Run `manage.py collectstatic` before deploy; serves from `STATIC_ROOT = staticfiles/`.
- **WSGI:** `mooo_backend.wsgi.application`. Use `gunicorn mooo_backend.wsgi` in prod.
- **Secrets:** `.env` is loaded by a small inline parser in `settings.py` (no `python-dotenv` dependency). Required: `SECRET_KEY`. Recommended in prod: `DEBUG=False`, explicit `ALLOWED_HOSTS`.
- **Time zone:** `TIME_ZONE = 'UTC'`, `USE_TZ = True`. Date-bucketing in views uses `timezone.localdate()` and `TruncDate`.
- **Database:** SQLite, single file (`db.sqlite3`). Fine for single-user; will need migration plan if/when multi-user or local-first storage is introduced.

---

## What's committed vs. what's not (as of 2026-05-23)

Recent commits:
- `8f1514b` Register models in Django admin
- `88ce7b1` Initial commit: lactea prototype

**Uncommitted on `main`** (this is the in-flight skin system):

```
 M core/urls.py                 # adds /theme/<skin>/ route
 M core/views.py                # adds set_skin view + safe redirect
 M mooo_backend/settings.py     # registers SkinMiddleware
 M templates/base.html          # uses skin partials + theme toggle in footer
 M templates/home.html          # uses skin partial
 M templates/pump_timer.html    # uses skin partial
?? core/middleware.py           # SkinMiddleware + SKIN_* constants
?? static/css/                  # skins.css
?? static/images/drop-icon.svg  # plain-skin alt to cow-icon.svg
?? static/sounds/chime.mp3      # plain-skin alt to lactea.mp3
?? templates/skins/             # cow/ and plain/ partial folders
```

Suggested commit ordering when wrapping up: middleware + settings + view + urls together (the plumbing); then templates + skin partials + assets (the swap); then the bug fix for `set_skin`'s 405.

---

## Known issues / cleanup punch-list

1. **`set_skin` returns HTTP 405 on invalid skin name.** Should be 400 or 404. (See [Skin system](#the-skin-system).)
2. **No tests.** `core/tests.py` is empty. At minimum: a smoke test per view, model `__str__`/property tests, and a test that exercises the skin middleware + cookie round-trip.
3. **No CI.**
4. **`Profile` model is unused.** Either wire it up (auth path forward) or remove it.
5. **`base.html` has hardcoded emoji in nav** (🏠 ⏰ 💊 📝 📈). These are visual branding and ideally would move into a per-skin partial or copy dict so non-cow skins can change them.
6. **Quick-add supplement names** (`Fenugreek`, `Domperidone`, etc.) are hardcoded in `views.supplements`. Candidate for per-skin override.
7. **Hardcoded pink-themed Tailwind classes in `forms.py` widget attrs** (`border-pink-300`). Locks form styling to one aesthetic; a skin shouldn't have to override these via CSS specificity. Consider neutral classes + skin CSS, or move widget classes out of `forms.py` into templates.
8. **`mooo_backend/urls.py` docstring references Django 6.0.5** (probably from `django-admin startproject`); actual requirement is `Django>=5.1`. Cosmetic.
9. **No `.env`-to-git safety:** `.env` is present in the working tree. Confirm `.gitignore` excludes it (it should).

---

## Conventions

- **Views:** function-based, simple template renders, no class-based views or DRF. Keep it that way unless there's a reason.
- **Forms:** Django `ModelForm` with Tailwind classes embedded in widget `attrs`. (See cleanup item 7 — this may move.)
- **HTMX:** `django-htmx` is installed and middleware registered, but no view currently branches on `request.htmx`. Available when we want partial updates.
- **No JS framework.** Vanilla JS in `static/js/`. Chart.js for the progress chart. Keep new interactivity minimal — server-render first, HTMX where it helps.
- **Naming:** snake_case for views and URL names; PascalCase models.

---

## Where to look next

- **Strategy / decision log:** [`task.md`](task.md) — dated entries on direction, open questions, what we picked and why.
- **User-facing intro:** [`README.md`](README.md).
- **Privacy stance:** `templates/privacy.html` (also visible at `/privacy/` in-app).
- **Django admin:** `/admin/` once you've created a superuser — useful for poking at data without writing a shell.

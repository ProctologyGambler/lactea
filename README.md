# Mooo 🐮

A gentle Django web app for people inducing lactation without pregnancy. Track pumping sessions, supplements, and how you're feeling each day. Includes a research-backed supplement guide and a CSV export of all your data.

> ⚕️ **This is not medical advice.** Mooo is an informational and personal-tracking tool. Inducing lactation should always be done under the supervision of a healthcare provider or International Board Certified Lactation Consultant (IBCLC). See the in-app `/privacy/` page for what happens to your data.

## Features

- **⏰ Pump timer** — stopwatch-style logging with per-breast ml and notes. Today's totals visible at a glance.
- **💊 Supplement tracker** — daily checklist, quick-add presets for common galactagogues, and per-day toggle.
- **📖 Supplement guide** — research-backed reference of herbal and pharmaceutical galactagogues with dosages, evidence strength, side effects, and sourced citations.
- **📝 Daily log** — multi-select mood and body check-in, plus free-text custom adjectives.
- **📈 Progress** — bar chart of pumping minutes per day over 7/30/90 days, with a daily breakdown table.
- **📤 CSV export** — download all your data anytime as a single CSV.
- **📱 PWA-ready** — installable to Android / iOS home screens. Service worker caches the app shell so it loads offline after first visit.

## Tech stack

- **Backend:** Django 5.x, SQLite (single-user prototype)
- **Frontend:** Tailwind CSS (Play CDN, vendored locally), Chart.js 4.x
- **PWA:** Web App Manifest + service worker (Tier 1 offline cache; offline writes are a future upgrade)
- **Production helpers:** WhiteNoise for static files, Gunicorn for the WSGI server

## Setup (local development)

```bash
# Clone
git clone <your-repo-url> mooo
cd mooo

# Virtualenv
python -m venv venv
source venv/bin/activate     # Windows: venv\Scripts\activate

# Dependencies
pip install -r requirements.txt

# Environment variables
cp .env.example .env
# Open .env and replace SECRET_KEY with a fresh value:
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Database
python manage.py migrate

# Optional: create an admin user for /admin/
python manage.py createsuperuser

# Run
python manage.py runserver
```

Open http://127.0.0.1:8000 in your browser.

## Project structure

```
mooo-prototype-grok-django/
├── core/                     # Main app
│   ├── models.py             # PumpingSession, DailyLog, Supplement, SupplementLog
│   ├── views.py              # All views
│   ├── forms.py              # ModelForms
│   ├── urls.py
│   └── migrations/
├── mooo_backend/             # Django project settings
│   ├── settings.py
│   └── urls.py
├── static/
│   ├── images/               # cow-icon.svg, cow-start.svg, cow-stop.svg
│   ├── js/                   # timer.js, charts.js, vendored tailwind.js + chart.min.js
│   ├── sounds/               # mooo.mp3
│   └── manifest.json         # PWA manifest
├── templates/
│   ├── base.html             # Layout with nav + footer
│   ├── sw.js                 # Service worker template (served at /sw.js)
│   └── *.html                # Page templates
├── .env.example              # Template for environment variables
├── .gitignore
├── LICENSE                   # MIT
├── manage.py
├── README.md
└── requirements.txt
```

## Privacy stance

Today the app stores data on the server (SQLite file). No third-party analytics, no tracking, no external CDNs at runtime — Tailwind and Chart.js are vendored locally. See `/privacy/` for the current policy.

The longer-term direction is a **local-first** architecture where data lives entirely on the user's device. The PWA infrastructure is already in place for that transition.

## Status

Personal prototype, single user, under active development. Not production-ready, not lawyer-reviewed, not on an app store.

## License

[MIT](LICENSE) — do what you want, no warranty.

# Lactea 🥛

**A gentle, private tracker for people inducing lactation without pregnancy.**

Log pumping sessions, supplements, and how your body and mood feel each day — backed by a research-sourced galactagogue guide, and wrapped in a skin that speaks *your* community's language.

![Django](https://img.shields.io/badge/Django-5.x-092E20?logo=django&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.11+-3776AB?logo=python&logoColor=white)
![PWA](https://img.shields.io/badge/PWA-installable-5A0FC8?logo=pwa&logoColor=white)
![Privacy](https://img.shields.io/badge/data-local--first-2ea44f)
![License](https://img.shields.io/badge/License-MIT-blue)
![Status](https://img.shields.io/badge/status-active%20prototype-orange)

> ⚕️ **This is not medical advice.** Lactea is an informational and personal-tracking tool, nothing more. Inducing lactation should be done under the care of a healthcare provider or an International Board Certified Lactation Consultant (IBCLC). The guide summarizes published research — it does not prescribe, diagnose, or account for your medications, conditions, or dosages. See the in-app `/privacy/` page for exactly what happens to your data.

---

## Who it's for

Inducing lactation isn't only a postpartum story. Lactea is built to feel warm and non-clinical for anyone doing this work, including:

- adoptive and intended parents preparing to nurse
- trans women and transfeminine people
- partners who want to share feeding with a nursing parent
- surrogacy and co-parenting arrangements
- anyone relactating or inducing without a current pregnancy

The through-line: **mechanical stimulation does the heavy lifting, and the rest of your routine plays a supporting role.** Lactea is designed to make that routine easy to keep, not to make promises.

---

## Features

- **⏰ Pump timer** — stopwatch-style logging with per-breast ml and notes. Today's totals sit at the top so you always know where you are.
- **💊 Supplement tracker** — a daily checklist with quick-add presets for common galactagogues, and a simple per-day toggle.
- **📖 Supplement guide** — a research-sourced reference of herbal and pharmaceutical galactagogues: typical dosages, evidence strength, side effects, interaction flags, and citations you can actually follow.
- **📝 Daily log** — a multi-select mood and body check-in, plus free-text room for your own words.
- **📈 Progress** — pumping minutes per day over 7 / 30 / 90 days, as a chart with a matching daily breakdown table.
- **📤 CSV export** — your whole dataset, one download, anytime. No lock-in.
- **📱 PWA-ready** — installable to Android / iOS home screens. The service worker caches the app shell so it loads offline after the first visit.

---

## 🎨 Skins — the heart of the project

Communities of practice don't want the same app with a different logo. They want an app that *sounds like them*. Lactea's answer is **skins**: one codebase, many faces.

A skin is more than a color swap. Each one bundles:

- **Voice & copy** — a per-skin dictionary, so the words fit the community (clinical, playful, tender, matter-of-fact).
- **Palette & type** — driven entirely by CSS variables, no forked templates.
- **Sound & imagery** — icons and audio cues that match the mood.
- **Feature emphasis** — which tools feel front-and-center can differ by skin.

Everything is described in a per-skin `skin.json` manifest, so adding a community is meant to be *drop a folder, register it, done* — not a rewrite.

The original cow theme (**Moo**) becomes one skin among many rather than the whole identity — that's the resolution to the "the cow is polarizing" feedback. A neutral **Plain** skin ships alongside it for clinical or IBCLC-supervised contexts, and community-shaped skins follow from there.

> **On the name:** *Lactea* is the working project/codename while the public rebrand is still being finalized (the direction is "milky, not bovine"). It's isolated to one config value plus the default skin, so it's a one-line swap when the name lands.

---

## 🔒 Privacy & local-first

For an app about your body, privacy isn't a feature — it's the premise.

- **No third-party analytics, no tracking, no runtime CDNs.** Tailwind and Chart.js are vendored locally, so the app doesn't phone home.
- **Your data is yours.** The CSV export exists so you can walk away with everything at any moment.
- **Local-first is the destination.** Today data lives in a server-side SQLite file (single-user prototype). The intended direction is data that lives entirely on *your* device — and the PWA groundwork for that is already in place.

See `/privacy/` in-app for the current, plain-language policy.

---

## 🧱 Tech stack

- **Backend:** Django 5.x · SQLite (single-user prototype)
- **Frontend:** Tailwind CSS (vendored locally) · Chart.js 4.x
- **PWA:** Web App Manifest + service worker (Tier-1 offline shell cache; offline *writes* are on the roadmap)
- **Production helpers:** WhiteNoise (static files) · Gunicorn (WSGI)
- **Mobile path:** PWA now, optional Capacitor wrap later for app-store presence — same codebase, native shell, no React Native / Flutter rewrite.

---

## 🚀 Setup (local development)

```bash
# Clone
git clone <your-repo-url> lactea
cd lactea

# Virtualenv
python -m venv venv
source venv/bin/activate         # Windows: venv\Scripts\activate

# Dependencies
pip install -r requirements.txt

# Environment variables
cp .env.example .env
# Open .env and drop in a fresh SECRET_KEY:
python -c "from django.core.management.utils import get_random_secret_key; print(get_random_secret_key())"

# Database
python manage.py migrate

# Optional: admin user for /admin/
python manage.py createsuperuser

# Run
python manage.py runserver
```

Then open http://127.0.0.1:8000.

---

## 🗂 Project structure

```
lactea/
├── core/                     # Main app
│   ├── models.py             # PumpingSession, DailyLog, Supplement, SupplementLog
│   ├── views.py              # All views
│   ├── forms.py              # ModelForms
│   ├── urls.py
│   └── migrations/
├── lactea_backend/             # Django project settings
│   ├── settings.py
│   └── urls.py
├── skins/                    # ← skin system (in progress)
│   ├── moo/                  #   default cow skin
│   │   ├── skin.json         #   manifest: palette, fonts, copy, assets, sounds
│   │   ├── copy.py           #   per-skin word dictionary
│   │   ├── images/           #   icons + start/stop art
│   │   └── sounds/           #   e.g. lactea.mp3
│   └── plain/                #   neutral / clinical skin
├── static/
│   ├── css/                  # CSS variables consumed by skins
│   ├── js/                   # timer.js, charts.js, compiled tailwind.css + chart.min.js
│   └── manifest.json         # PWA manifest
├── templates/
│   ├── base.html             # Layout with nav + footer
│   ├── sw.js                 # Service worker template (served at /sw.js)
│   └── *.html                # Page templates
├── .env.example
├── .gitignore
├── LICENSE                   # MIT
├── manage.py
├── README.md
└── requirements.txt
```

*(The `skins/` layout is the target shape as the skin work lands; assets currently living under `static/images` and `static/sounds` migrate into their skin folder.)*

---

## 🗺 Roadmap

- [ ] **Finish + commit the skin system** end-to-end (Moo + Plain), so skins are the real architecture, not a half-branch.
- [ ] **Per-skin copy dictionaries** — skins differ in *words*, not just pictures.
- [ ] **Formalize the `skin.json` manifest** so a new community skin is "drop a folder."
- [ ] **Local-first data** — on-device storage and offline writes, building on the existing PWA layer.
- [ ] **Optional Capacitor wrap** for app-store presence when it matters.

---

## 📌 Status

Personal prototype, single user, under active development. Not production-ready, not lawyer-reviewed, not on an app store. Built with care and a lot of iteration.

## 📄 License

MIT — see [`LICENSE`](./LICENSE).

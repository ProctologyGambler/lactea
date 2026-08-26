# Lactea — Working Log

A running summary of conversations, decisions, and where things stand. Updated by Claude as we work together. Read this any time you want to remember "what were we doing?" or "why did we pick that?"

---

## 2026-05-23 (session 3) — Scaffolding built

**What we did**
- Read through the entire codebase: models, views, forms, middleware, all templates, CSS, JS, skin partials, service worker, manifest, settings.
- Built the skin system architecture end-to-end:
  - `skins/` directory at project root with `_base/`, `cow/`, `plain/`
  - `skins/loader.py` — loads `skin.json` + `copy.py`, merges base → skin with `lru_cache`
  - `skins/_base/copy.py` — ~80 user-facing strings, dot-namespaced
  - Per-skin `copy.py` overrides (cow: playful/emoji, plain: minimal)
  - Per-skin `skin.json` manifests (palette, fonts, features, sounds, PWA config)
  - `core/context_processors.py` — injects `{{ c.key }}`, `{{ skin_config }}`, `{{ skin_features }}`, `{{ available_skins }}` into every template
- Refactored every template to use the copy system (no more `{% if request.skin == 'cow' %}` conditionals)
- Replaced all hardcoded `border-pink-300` / `text-pink-700` classes with skin-neutral CSS classes (`.skin-input`, `.skin-card`, `.skin-tag`, `.skin-btn-primary`, `.skin-scale`, etc.)
- Expanded `skins.css` from 66 → ~250 lines of CSS-variable-driven component styles
- Made `charts.js` read CSS variables for colors
- Expanded `DailyLog` model with field journal fields: `energy`, `sleep_quality`, `hydration`, `stress`, `tags`
- Created migration `0003_dailylog_field_journal.py`
- Updated `daily_log` view to pass choice tuples
- Updated `daily_log.html` with scale selectors and custom tags
- Fixed the 405 bug (`set_skin` now raises `Http404` on invalid skin)
- Updated middleware to auto-discover skins from the `skins/` directory

**Architecture notes**
- Adding a new skin = create `skins/<name>/` with `skin.json`, `copy.py`, and `templates/skins/<name>/` partials. Add name to `SKIN_CHOICES` (auto-detected from directory). Zero changes to views, models, or URLs.
- Copy inheritance: `_base/copy.py` has every string. Skin `copy.py` only overrides what it changes. Merge: `{**base, **skin}`.
- CSS variables drive all visual theming. Tailwind utility classes handle layout. Skin-specific classes (`.skin-input`, `.skin-card`, etc.) read `var(--palette-key)`.
- Templates use `{{ c.key_name }}` (dots replaced with underscores by the context processor).
- `skin_features` dict available in templates for conditional feature visibility.

**Files changed**
- New: `skins/` (entire directory), `core/context_processors.py`, `core/migrations/0003_dailylog_field_journal.py`
- Modified: `core/models.py`, `core/views.py`, `core/forms.py`, `core/middleware.py`, `mooo_backend/settings.py`
- Refactored: `templates/base.html`, `templates/home.html`, `templates/pump_timer.html`, `templates/daily_log.html`, `templates/supplements.html`, `templates/progress.html`
- Refactored: `static/css/skins.css`, `static/js/charts.js`

**Still needs work**
- `supplement_guide.html` and `privacy.html` still have hardcoded pink classes (not yet refactored)
- HTMX on supplement toggle (installed but unused — easiest interactive win)
- `/insights/` view (the correlation engine)
- Third skin (clinical) to prove the architecture scales
- Service worker cache list doesn't include `skins.css` yet

**After you unzip**
1. Copy `skins/` directory to project root
2. Replace modified `core/` and `mooo_backend/` files
3. Replace templates and static files
4. `python manage.py migrate` (runs 0003)
5. Test both skins at `http://127.0.0.1:8000`

---

## 2026-05-23 (session 2) — Design brief & product vision

**What we did**
- Shifted from "help me code" to "help me think." Established Claude's role as design partner / idea-bouncer / theoretical continuity checker.
- Produced `DESIGN_BRIEF.md` — captures the full product vision, skin system architecture, field log concept, evidence presentation philosophy, and PWA ambitions.

**Key ideas that crystallized**
- Skins are experiential frames, not themes. They change visuals, copy, sound, information hierarchy, and epistemological stance.
- The field log is participatory self-study. Users are ethnographers of their own bodies.
- The insight engine is the killer feature: correlations, lagged correlations, pattern narration.
- Evidence should be accessible and honest, not authoritative and hiding.
- Worth paying for = understood + informed + saved time.

---

## 2026-05-23 — Project orientation & strategy

**What we did**
- Walked through the repo. Django 5 app, SQLite, PWA-ready, skin system half-built.
- Discussed the bigger goal: support niche communities through swappable skins.

**Key decisions**
- Skins are the core differentiator.
- PWA first, Capacitor later.
- Per-skin copy + palette + fonts via CSS variables.
- `skin.json` manifest per skin so adding one is "drop a folder."

---

## 2026-05-23 (session 4) — Scaffolding extracted + design vision articulated

**What we did**
- Reviewed the other developer's scaffolded work (delivered as `lactea-scaffolded.zip`). Verdict: strong architectural step. Loader pattern with `@lru_cache`, dict-merge inheritance for copy, filesystem auto-discovery for `SKIN_CHOICES`, CSS variables driven by `[data-skin]`, `charts.js` reading CSS variables, context processor injecting `c`/`skin_config`/`skin_features`/`available_skins`. The 405→404 set_skin fix landed.
- Flagged loose ends from the review: stale service worker cache, dozen-or-so hardcoded copy/emoji leaks across templates, inline style on timer-display, dead RadioSelect widget config, unused `supps.delete_confirm` copy key, unused `Profile` model, admin not updated for new fields, untouched `supplement_guide.html` / `privacy.html`, no form error rendering.
- Extracted the zip into the working tree. Preserved `task.md` (zip's version was stale), `DESIGN_BRIEF.md`, `codebase_snapshot.md`, and the .zip files themselves. Django check passes cleanly.
- User has **not yet run** `venv/bin/python manage.py migrate` for the new `DailyLog` fields (energy / sleep_quality / hydration / stress / tags).

**Design vision — articulated this session**

| Axis | Choice | Implication |
|---|---|---|
| Skin differentiation | **Skin-specific UI patterns** | Same data, genuinely different shapes per skin. Clinical might be dense single-page; Cow might be card-feed. Skin partials directory grows. |
| Gamification | **Daily field-journal prompt only** | One gentle question per day. No streaks, no badges, no points. Engagement is the data. |
| Polish priority | **Sound design beyond session-end** | Audio palette before illustrations or animation. Add slots: tap / save / milestone. Each skin gets a sonic identity. Must be mute-able. |

These three choices together mean skins aren't a *theme system*, they're an *experience system*. Each skin has its own layouts, its own daily prompt voice, its own sonic identity.

**Next**
1. Fix the punch-list loose ends (small, mechanical — informed by the vision: e.g., when expanding the sound system slots, do it now rather than later).
2. Draft a phased plan for the bigger design arc (skin-specific UI patterns + daily prompt feature + sound system expansion). Show plan, get sign-off, execute in tranches.

---

## 2026-05-23 (session 5) — Punch-list fixes applied

**Files changed:** `templates/sw.js`, `templates/home.html`, `templates/supplements.html` (×3 edits), `templates/progress.html`, `templates/daily_log.html` (×4 edits), `templates/pump_timer.html` (×2 edits), `skins/_base/copy.py` (×6 edits), `skins/cow/skin.json`, `skins/plain/skin.json`, `static/css/skins.css`, `core/forms.py`, `core/admin.py`.

**What got fixed**

| Item | Change |
|---|---|
| Service worker stale cache | Added `skins.css`, `drop-icon.svg`, `chime.mp3` to APP_SHELL. Bumped `CACHE_NAME` from `lactea-v2` → `lactea-v3`. Plain skin now works offline. |
| Sound system architecture | Each `skin.json` now declares 4 sound slots (`tap`, `save`, `milestone`, `session_end`). All four default to the existing single file per skin — no breakage, ready for sound work. |
| Hardcoded copy/emoji leaks | New copy keys for `home.start_session_icon`, `supps.guide_link_icon`, `progress.volume_icon`, `supps.form_name_label` / `dosage` / `frequency` / `notes`, `daily.past_mood_label`, `daily.past_breast_label`, `daily.tags_label`. All template hardcodings replaced with `{{ c.* }}` lookups. |
| `supps.delete_confirm` unused key | Confirm dialog now uses the copy key. Removed the `{name}` placeholder (Django templates can't .format()); copy is now skin-overridable. |
| Inline style on timer-display | Added `.skin-timer-display` class to `skins.css`; removed inline style. |
| Dead `RadioSelect` widget config in `forms.py` | Removed the four unused widget configs. Comment explains why the fields stay in `fields=[...]` (for POST processing). |
| `core/admin.py` not updated for field-journal fields | `list_display`, `list_filter`, `search_fields` now include `energy`, `sleep_quality`, `hydration`, `stress`, `tags`. |
| No form error rendering | Added `.skin-error-box` CSS class and per-form error display to `pump_timer.html`, `daily_log.html`, `supplements.html`. Pump-timer form now stays *visible* if POST returns with errors (was previously hidden by `class="hidden"` regardless). |

**Deliberately not done** (waiting for explicit go-ahead):
- Delete the `Profile` model — needs a destructive migration to drop the table.
- Refactor `supplement_guide.html` and `privacy.html` (still have hardcoded pink classes). These are bigger surface areas; better tackled with the upcoming design phase.
- Per-skin overrides of the new copy keys (e.g., plain skin choosing simpler icons than cow). Defaults are sensible; per-skin polish belongs to the design phase.

**Verification**
- `venv/bin/python manage.py check` → 0 issues.
- Migration `0003_dailylog_field_journal` still pending (user runs `venv/bin/python manage.py migrate` when ready).

**Next**
- Task #6: plan the bigger design + gamification phase (skin-specific UI patterns, daily field-journal prompt feature, sound system expansion). Surface the plan, get sign-off, execute in tranches.

---

## 2026-05-23 (session 6) — Design phase plan drafted

Saved [`design_plan.md`](design_plan.md) — phased plan for the bigger design arc anchored to the three session-4 choices.

**Phases at a glance:**
- **A. Sound system** (polish priority #1) — JS sound layer + mute toggle + per-skin sonic identity at 4 trigger points
- **B. Daily prompt** (the gamification) — home-page card, one gentle question per day, per-skin prompt pool, new model for responses
- **C. Skin-specific UI patterns** (the differentiator) — `templates/skins/<skin>/daily_log_body.html` pattern; cow as card-feed, plain as compact form; repeat on home
- **D. Documentation** — ongoing
- **E. Parking lot** — illustrations, animations, typography, insight engine, offline writes (not now)

**Seven open questions** parked in `design_plan.md` for the user to lock in before Phase A coding starts. Recommendations attached to each but not assumed.

**Not implemented yet** — this is a planning artifact. Execution begins after open questions are resolved.

---

## 2026-05-23 (session 7) — Phase A/B/C decisions locked

User answered all 7 open questions from [`design_plan.md`](design_plan.md). Six matched recommendations; one departure.

**The seven picks:**
1. Mute UX = global toggle
2. **Sound assets = single placeholder per skin, defer audio decision** (departure from rec — smart; un-blocks architecture from asset sourcing)
3. Default state = off, with smart prompt on first save
4. Prompt pool size = 30 per skin
5. Prompt storage = new `DailyPromptResponse` model (new migration `0004`)
6. First UI-shape screen = daily log
7. Differentiation depth = daily log + home only

`design_plan.md` updated with locked decisions and implementation implications. Memory saved (`design_phase_decisions.md`) so future sessions don't re-prompt.

**Next:** Phase A coding — JS sound layer (`static/js/sounds.js`), wire triggers, global mute toggle, smart first-save prompt. Awaiting user go-ahead before starting.

---

## 2026-05-23 (session 8) — Phase A built (sound system)

**Files touched:** `static/js/sounds.js` (new, ~85 lines), `core/context_processors.py`, `core/views.py`, `templates/base.html`, `templates/pump_timer.html`, `templates/daily_log.html`, `templates/supplements.html`, `templates/sw.js`, `static/js/timer.js`, `static/css/skins.css`, `DESIGN_BRIEF.md`. **Deleted:** `templates/skins/{cow,plain}/_end_sound.html`.

**What's now working**

| Piece | How |
|---|---|
| Sound URLs in JS | `core/context_processors.py` resolves each slot's static URL; `base.html` ships them via `\{\{ skin_sound_urls\|json_script:"skin-sounds" \}\}` |
| `playSkinSound(slot)` | New `static/js/sounds.js`. Reads URLs from the JSON-script element, caches one `Audio` per slot (so a tap doesn't restart a save mid-play), respects mute, silently no-ops if missing |
| Global mute | Speaker-icon button in footer. `localStorage`-backed. Toggles 🔊 / 🔇. Persists across sessions |
| `tap` trigger | Supplement toggle form submit; quick-add buttons |
| `save` trigger | Pump session form, daily log form, supplement add form (all `onsubmit`) |
| `session_end` trigger | Pump timer Stop button (was using a per-skin `<audio>` element; refactored to `playSkinSound('session_end')`) |
| Smart first-save prompt | `pump_timer` view redirects to `?just_pumped=1` after save; sounds.js checks URL + `localStorage` and shows a one-time card asking "Want sound feedback? Enable / Not now" |
| Service worker cache | `sounds.js` added to APP_SHELL; `CACHE_NAME` bumped to `lactea-v4` |
| Documented sonic identities | New "Per-skin sonic identity" subsection in `DESIGN_BRIEF.md` describing what each of the six planned skins should sound like, plus the four implementation rules |

**Architecture characteristics worth knowing**
- Per-slot Audio cache means same-file-across-slots placeholder phase doesn't sound broken (no overlap, no abrupt restarts).
- Sound layer fails silently if `skin-sounds` JSON element is missing or a slot URL is empty — the rest of the app keeps working.
- Mute decision is global (one toggle, all slots), per session 7 decision #1.
- First-save prompt only fires when sounds are still muted AND the URL has `just_pumped=1` AND localStorage hasn't recorded resolution — three guards.

**Deliberately not built yet** (intentional placeholders or follow-ups)
- Real audio assets — all four slots per skin still point to existing `lactea.mp3` (cow) or `chime.mp3` (plain). Asset sourcing is a separate concern per session 7 decision #2.
- `milestone` trigger has no firing site yet — needs a server-side rule for "first ever / every 10th / first 30 days" and a way to signal the client. Defer to its own session.
- Theme-picker links don't play `tap` (would be jarring during navigation).

**Verification**
- `venv/bin/python manage.py check` → 0 issues.
- Migration `0003_dailylog_field_journal` still pending (run `venv/bin/python manage.py migrate` to apply).

**Next:** Phase B — the daily field-journal prompt. New model, prompt pool per skin, home-page card, deterministic rotation, prompt-history view.

---

## 2026-05-23 (session 9) — Iteration 2 in progress

**2A — Clinical skin: DONE.** New `skins/clinical/` folder with palette (white/slate/navy-800), `copy.py` (evidence-forward voice, no emoji, clinical taxonomy: Overview/Session/Supplements/Log/Data), `skin.json`, three partials, `clinical-icon.svg` (a simple slate-blue droplet path). Density overrides in `skins.css`: tighter card corners (0.5rem), 1px slate dividers, square button corners. Auto-discovered by the loader — three skins now visible in the theme picker. Service worker bumped to `lactea-v5` and clinical icon added to cache.

**2B — Lactans painting starter set: APPROVED at 16 paintings.** See [[skin-iteration-2]] memory for the locked list. Coverage: Europe ×8, Americas ×3, Africa ×2, Asia ×3.

**Proof rendered (hard-coded on Plain skin):** Cassatt's *Mother About to Wash Her Sleepy Child* (1880, LACMA, downloaded 947 KB from Wikimedia) wired as a `[data-skin="plain"]` body background watermark with a cream-gradient overlay. Italic caption in bottom-right corner: title / artist+year / source attribution. User reviewing.

**Next:** await user reaction to the proof (opacity / size / caption placement / general feel). Then do the full 2B build — rename `plain/` → `lactans/`, build the painting rotation system, download remaining 15 paintings, add divider/motif treatment.

---

## 2026-05-24 (session 10) — Three-skin baseline shipped: Lactea · Via Lactea · Galactra®

**Renames**
- `skins/plain/` → `skins/via_lactea/` (folder, templates, CSS selector `[data-skin="plain"]` → `[data-skin="via_lactea"]`).
- `skins/clinical/` → `skins/galactra/` (folder, templates, CSS selector, brand strings, favicon `clinical-icon.svg` → `galactra-icon.svg`).
- `core/middleware.py`: `SKIN_DEFAULT = "via_lactea"`.
- `core/context_processors.py`: fallback default updated.
- Service worker `CACHE_NAME` bumped `lactea-v5` → `lactea-v6`; APP_SHELL swaps `drop-icon.svg` and `clinical-icon.svg` for the new files.
- Orphaned `static/images/drop-icon.svg` removed.

**Via Lactea (the "Pearl Drop" rename)**
- Display name `Via Lactea ✦`; tagline *"A quiet sky for a slow practice."*
- Voice: spare, celestial, mythopoetic without being precious. ~35 base-copy keys overridden. Sample: home welcome is *"Welcome to the night sky"*; "Course" replaces "Progress"; "Tonight" replaces "Today" on the home card.
- New favicon: `static/images/via-lactea-icon.svg` (four-pointed star with radial glow on a dark plate).
- Starfield polish: body background now layers a 115° diagonal galactic-plane band + a warm off-center bulge over the base sky gradient (skins.css ~line 142). The existing dual-layer `::before/::after` twinkling starfield is unchanged.
- `skin.json` palette + PWA colors aligned to the night-sky values (was still warm pinks from Pearl Drop).

**Galactra® (the "clinical" rename + full pharma re-voice)**
- Display name `Galactra®`; tagline *"A precision tracker for induced lactation protocols."* Wordmark uppercase, ® superscripted in nav.
- Pharma copy voice across all surfaces: "affect / mood", "yield (mL)", "active regimen", "galactagogue", "administered" vs "taken", "perceived stress (1–5)", etc. Mood/breast labels reframed; supplements page restyled as "Active regimen" / "monograph reference" / "Discontinue this agent" etc.
- **Consult-physician disclaimer** carried in `footer.message`: full ISI-style sentence ("Galactra is an observational self-tracking tool. It does not diagnose, treat, cure, or prevent any condition. Consult your physician, IBCLC, or qualified healthcare provider…"). Rendered as a left-aligned 56rem band with a 2px accent rule, regulatory-register typography.
- Pharma typography rules added under `[data-skin="galactra"]`: uppercase tracked wordmark/headings/buttons; tabular-lining numerals on stat values and timer; sharp corners (0.125–0.25rem); 1px rules on cards/dividers; Inter (system fallback) as the body font; white nav bar with thin underline.
- `skin.json` palette tightened (surface-1 → `#ffffff`, accent-soft → `#eef2f7`), font stack set to Inter.

**Verification**
- `venv/bin/python manage.py check` → 0 issues.
- Local server smoke test: all three skins render at `/` with their cookie set via `/theme/<skin>/?next=/`. Verified wordmark, body data-skin attribute, Galactra's "IMPORTANT SAFETY INFORMATION…" footer, and the three options in the footer skin picker.
- `skins.loader.get_available_skins()` returns `[cow, galactra, via_lactea]` (alphabetical).

**Deliberately not touched**
- `supplement_guide.html` and `privacy.html` still carry hardcoded pink Tailwind classes — pre-existing tech debt called out in earlier sessions. The Galactra disclaimer in the supplement guide title would benefit from a sweep here, but it's a separate, larger refactor.
- Real audio asset sourcing per skin — still chime.mp3/lactea.mp3 placeholders.
- Skin-specific layout shapes (Phase C) and Phase B daily-prompt feature.

**Files touched** (full list)
- Renamed: `skins/{plain → via_lactea}/`, `templates/skins/{plain → via_lactea}/`, `skins/{clinical → galactra}/`, `templates/skins/{clinical → galactra}/`, `static/images/{clinical → galactra}-icon.svg`.
- Rewritten: `skins/via_lactea/{skin.json,copy.py}`, `templates/skins/via_lactea/{_brand_head,_brand_nav}.html`, `skins/galactra/{skin.json,copy.py}`, `templates/skins/galactra/{_brand_head,_brand_nav}.html`.
- New: `static/images/via-lactea-icon.svg`.
- Edited: `static/css/skins.css` (selector renames, galactic-plane band, full Galactra pharma block), `core/middleware.py`, `core/context_processors.py`, `templates/sw.js`.
- Removed: `static/images/drop-icon.svg`.

**Next**
- Visual review of all three skins side-by-side in a browser (especially Galactra typography and the Via Lactea galactic-plane band — looks right in code, deserves an eyeball pass).
- Decide whether to do the supplement_guide.html / privacy.html sweep now (clean up pink classes; apply Galactra disclaimer voice there too) before moving on to Phase B (daily prompt) or Phase C (skin-specific layouts).
- Re-deferred: paintings rotation for Via Lactea, real audio per skin, custom font self-hosting.

---

## 2026-05-24 (session 11) — Multi-product foundation shipped

**The pivot.** User decided each skin should be its own absolute version of the app — not a re-skinned shared product. Different page set, different flows per demographic, no cross-contamination (a Galactra visitor must not accidentally land on Lactea). Backend stays shared; data pools across skins for trend analysis. Privacy will disclose the pooling.

**Foundation delivered this session** (engineering only — no divergent pages written yet):

1. **Template overlay loader** — `skins/template_overlay.py::SkinOverlayLoader` (subclass of Django's `FilesystemLoader`) prepends `templates/skins/<current_skin>/` to the search path. Thread-local skin context lives in `skins/runtime.py` (`set_current_skin` / `get_current_skin` / `clear_current_skin`). Wired into `settings.TEMPLATES` with explicit `loaders` list (had to flip `APP_DIRS` to `False`; `AppDirectoriesLoader` is included so admin etc. still works). Verified: `get_template('_overlay_test.html')` resolves to the galactra-specific file when current_skin='galactra', falls through cleanly otherwise.

2. **Hostname-aware skin selection** — `settings.SKIN_BY_HOST` maps host string → skin name; populated from `SKIN_BY_HOST` env var (`"lactea.app=cow,vialactea.app=via_lactea,..."`). Middleware checks host first; if matched, skin is forced and `request.skin_locked = True`. Cookie continues to work on unmapped hosts. Verified: `Host: galactra.local` → serves galactra even with `skin=cow` cookie set.

3. **Footer picker auto-hides when locked** — base.html theme picker wrapped in `{% if not request.skin_locked %}`. Verified: 0 `/theme/` links on host-locked Galactra; 2 links on unlocked default page (the two skins that aren't currently active).

4. **`source_skin` column for cohort analytics** — migration `0004_*_source_skin*.py` adds `source_skin = CharField(max_length=32, db_index=True, default='unknown')` to `PumpingSession`, `DailyLog`, `Supplement`, `SupplementLog`. Views set it from `request.skin` at save time. `DailyLog` preserves source_skin on edits (only sets on first save) so cohort attribution is stable per-row. Verified via round-trip POSTs: pump sessions saved as cow → `source_skin='cow'`; as via_lactea → `source_skin='via_lactea'`. Pre-existing rows get `'unknown'` from the migration default.

**Files changed**
- New: `skins/runtime.py`, `skins/template_overlay.py`, `core/migrations/0004_dailylog_source_skin_pumpingsession_source_skin_and_more.py`.
- Edited: `mooo_backend/settings.py` (TEMPLATES → explicit loaders, SKIN_BY_HOST), `core/middleware.py` (host lookup, skin_locked, runtime hooks), `core/models.py` (source_skin on 4 models), `core/views.py` (4 save sites set source_skin), `templates/base.html` (picker conditional on skin_locked).

**Verification**
- `manage.py migrate` → 0004 applied cleanly.
- `manage.py check` → 0 issues.
- Smoke test passed for: default render, cookie switch, host-lock override, source_skin cohort tagging on save round-trip, overlay loader resolution.

**Deliberately deferred (the proof-of-divergence step)**
- A genuinely-different Galactra home / pump_timer / log page that shows the overlay loader is doing real work, not just routing identical templates. The architecture is in but unproven for end-users until at least one page actually diverges.
- Per-skin privacy.html — required before any production launch (must disclose cross-skin data pooling).
- Per-skin landing pages, per-skin onboarding, per-skin Open Graph meta.
- Migrating existing `{% include "skins/cow/_brand_nav.html" %}` paths to the simpler `{% include "_brand_nav.html" %}` (overlay loader handles the lookup). Old paths still work via fallthrough; cleanup is optional.

**Next options to pitch to user**
1. Pick one page (Galactra home, probably) and design genuinely-different IA — different stat tiles, different CTA framing, ISI band at top, "cycle / day" tracking instead of "today" tracking. Proves the overlay works for product, not just for code.
2. Per-skin privacy.html — required, but bureaucratic. Could batch with #1 if doing a Galactra-focused tranche.
3. Sequence question: which skin launches first? Marketing burden is real even if engineering is cheap.

---

## 2026-05-24 (session 12) — Galactra home divergence proven

Galactra's home page now genuinely diverges from the shared `home.html` via the template overlay loader built in session 11. Same view, same context, different page rendered per skin based on which template file exists.

**What renders on Galactra's home now**
1. Accent-coloured **protocol header band**: "PROTOCOL OVERVIEW · Induced lactation tracking · DAY N" (N computed from earliest PumpingSession). When no sessions exist: "Not yet initiated."
2. Amber **brief ISI band** below the header, linked to /privacy/. Pairs with the full ISI in the footer (pharma convention: brief top + full bottom).
3. **Today's metric strip** as a tabular 4-column data table — Sessions / Duration / Yield / Adherence. Tabular numerals, lining figures, accent-coloured values, gray small-caps headers, thin rules.
4. **Next session card** with a status badge (Recent ≤1h · Due 1–3h · Overdue >3h · Not started). Shows "Last session N h M min ago", "Target interval: 2–3 h", and a primary "Initiate session ▸" CTA.
5. **Active regimen inline list** — agent name, dosage · frequency, check/circle mark for today's administration. Empty state with link to /supplements/ when no agents are tracked.
6. **Recent records table** — tabular session log with monospace numerics. Date · Dur · L · R · Total columns.
7. **Today's observation log status row** — pharma-coded patient-reported-outcomes check-in with a link to /daily-log/.

**Files touched**
- `core/views.py` — `home()` view extended with `protocol_day`, `today_ml`, `adherence_pct`, `minutes_since_last`, `time_since_last` (pre-formatted), `session_status`, `regimen_inline`, `today_log`. Helper `_format_h_m()` for hour/minute formatting. New keys are inert for non-galactra templates (they ignore them).
- `skins/galactra/copy.py` — ~35 new pharma-coded copy keys under the `home.*` namespace: protocol_header, isi_*, today_section, col_*, next_section, status_*, cta_initiate, regimen_*, records_*, log_*.
- `templates/skins/galactra/home.html` — new overlay template (first one in the project). Extends shared `base.html`; replaces only the content block.
- `static/css/skins.css` — new `.pharma-*` component block scoped to `[data-skin="galactra"]`: protocol_header (with eyebrow/indication/day variants), isi_brief, section_title, metric_table + records_table (shared cell/header styles), status_badge with recent/due/overdue/not_started colour variants, meta with label/value variants, cta, link, regimen list with row/mark/name/dose subcomponents.

**Verified end-to-end** (host-locked via SKIN_BY_HOST env var):
- Galactra home renders the new overlay: 5 `pharma-protocol-header` hits, "Day 6" rendered, "Recent" status badge, "28 min ago" computed time delta, populated recent-records table, picker hidden (0 `/theme/` links).
- Lactea home renders the shared `home.html` unchanged: 0 pharma-* markers, "Start a session" CTA, data-skin="cow".
- Via Lactea home renders the shared `home.html` unchanged: 0 pharma-* markers, "Begin a session" CTA (from the Via Lactea copy.py override), data-skin="via_lactea".

**Proven**: a skin can fork an arbitrary page by dropping a single file at the right path. No `{% if %}` branches added to shared code. The shared view computes a union of context keys; each skin's template consumes only what it needs.

**Still to do for Galactra (not in this tranche)**
- Per-skin pump_timer.html, daily_log.html, supplements.html, progress.html — same overlay pattern. Each diverges genuinely (e.g., supplements page becomes a "Regimen" page with dosing schedule + side-effect monograph callouts).
- Per-skin privacy.html with cross-skin data-pooling disclosure. Required before any production launch.
- Per-skin base.html (optional) if Galactra wants a different nav structure (e.g., breadcrumb-style "Overview > Session > Records" instead of the current 5-tab nav).
- Eyeball pass in a browser — typography, status badge contrast on a real screen, ISI band amber on a real screen, regimen row alignment.
- Decide which page to diverge next on Galactra (probably pump_timer — that's the daily-action page).

---

## 2026-07-02 (session 13) — Monetization plan locked + T1 shipped (auth foundation)

**The pivot.** User returned wanting to monetize. Locked the shape: **Galactra® ships first, one-time $29 with 30-day money-back guarantee, paid before first use, US-only, weeks-horizon soft launch.** Six tranches (T1–T6). Consent copy locked verbatim: *"Improve the insight engine for people like me by contributing anonymized session data."*

**Operational decisions:** LLC in user's state (parallel with build), hosting Fly.io, domain `galactra.app` (check availability + register), support email `support@galactra.app` forwarded to Proton, Termly free-tier for legal boilerplate + Claude customization, hard opt-in checkbox with positive framing but never pre-checked.

**T1 shipped (auth + per-user data foundation).** Everything downstream now has an authenticated user context to hang off.

**Model changes** (`core/models.py`):
- Deleted unused `Profile` model.
- Added `UserProfile` with `data_pooling_consent`, `data_pooling_consent_at`, and monetization-reserved fields (`has_paid`, `paid_at`, `stripe_customer_id`, `refunded_at`) so T2 doesn't need another schema change.
- Added `user = ForeignKey(User, null=True, blank=True, on_delete=CASCADE)` to `PumpingSession`, `DailyLog`, `Supplement`, `SupplementLog`. Kept nullable to leave room for future demo/anonymous flows.
- `DailyLog.date` lost `unique=True`; replaced with `UniqueConstraint(fields=['user', 'date'])` so two users can both have a log for the same date.

**Migration `0005_user_ownership.py`:** schema changes + `RunPython` op that creates the founder superuser (`testusr` / `proctologygambler@proton.me` / unusable password via `make_password(None)`) and backfills all `user=NULL` rows to them. Reversible.

**Auth surface** (`core/forms.py`, `core/views.py`, `core/urls.py`, `mooo_backend/urls.py`, `mooo_backend/settings.py`):
- `SignupForm(UserCreationForm)` — username + email + password + password confirm + the locked consent checkbox with the approved copy.
- `signup(request)` view — validates form, creates User + UserProfile with consent metadata, auto-logs in, redirects to home.
- `/signup/` route in `core/urls.py`; `django.contrib.auth.urls` wired at `/accounts/` in `mooo_backend/urls.py`.
- Settings: `LOGIN_URL=login`, `LOGIN_REDIRECT_URL=home`, `LOGOUT_REDIRECT_URL=login`, `EMAIL_BACKEND=console` for dev (real SMTP in T5), `DEFAULT_FROM_EMAIL=support@galactra.app`.

**Views auth-gated** (all data pages):
- `@login_required` on `home`, `pump_timer`, `daily_log`, `supplements`, `supplement_toggle`, `supplement_delete`, `progress`, `export_csv`.
- Every query filters by `request.user`; every save sets `user = request.user`.
- `_galactra_protocol_context(user)` refactored to take a user argument — now scoped per-user.
- Public routes preserved: `/signup/`, `/accounts/login/`, `/privacy/`, `/supplements/guide/`, `/theme/*`, password reset flow.

**Templates** (`templates/auth_base.html`, `templates/registration/*.html`):
- `auth_base.html` — minimal shell for unauthenticated pages (skin-aware brand head/nav but no data links).
- `login.html`, `signup.html`, `logged_out.html`, `password_reset_form.html`, `password_reset_done.html`, `password_reset_confirm.html`, `password_reset_complete.html` — all skin-neutral, use existing `.skin-*` component classes.
- `base.html` — added logout button (POST form) in the footer, visible only when authenticated.

**Admin updates** (`core/admin.py`): user filter + column on all four data models. `UserProfile` registered with consent/payment fields visible.

**Verified** (`manage.py check` = 0 issues, migration plan + apply clean):
- testusr created: superuser=True, staff=True, unusable password (needs `changepassword`), profile row auto-created
- Backfill: 4 pumping sessions + 1 daily log all reassigned to testusr, 0 orphans
- End-to-end smoke test (Django test client): unauthenticated → 302 to login; signup creates user + profile with consent flag and timestamp; new user's data invisible to other users (testusr's session count unchanged); logout re-gates access; all 5 auth templates render 200

**Before user tests in browser:**
- Run `venv/bin/python manage.py changepassword testusr` to set a real password
- Server: `venv/bin/python manage.py runserver` → visit `/accounts/login/`

**Files touched**
- Edited: `core/models.py`, `core/views.py`, `core/forms.py`, `core/urls.py`, `core/admin.py`, `mooo_backend/urls.py`, `mooo_backend/settings.py`, `templates/base.html`
- New: `core/migrations/0005_user_ownership.py`, `templates/auth_base.html`, `templates/registration/{login,signup,logged_out,password_reset_form,password_reset_done,password_reset_confirm,password_reset_complete}.html`

**Next: T2 (Stripe Checkout + gate).** The UserProfile fields are already there; T2 wires the purchase page, Stripe Checkout redirect, `checkout.session.completed` webhook, refund handler, and middleware gate that shunts authenticated-but-unpaid users to `/purchase/`.

**Post-launch parking lot** (deliberately deferred from T1's scope): Phase B daily prompt, Phase C per-skin layouts, real audio assets, insight engine, `supplement_guide.html`/`privacy.html` pink-class cleanup, per-skin privacy overlay (that lands in T3).

---

<!-- New entries go above this line. Most recent on top. -->

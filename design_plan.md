# Lactea — Design Phase Plan

**Created:** 2026-05-23
**Anchored to:** the three load-bearing design choices from session 4 — skin-specific UI patterns, single daily field-journal prompt, sound design first. See [`task.md`](task.md) session 4 and [`DESIGN_BRIEF.md`](DESIGN_BRIEF.md).

The phases are sequenced so each one's output is usable on its own. You can stop after any phase and still have a more polished app than today.

---

## Phase A — The sound system (polish priority #1)

**Why first:** sound architecture has the smallest visible surface but the largest emotional payoff per line of code. It unlocks the "skins as experiences" promise more viscerally than any visual change.

**What it produces:** a working audio layer where every skin has its own sonic identity at four trigger points (`tap` / `save` / `milestone` / `session_end`), with a mute toggle the user controls.

**Steps:**

1. **Define the trigger taxonomy** (~30 min, no code). Document exactly where each sound fires. E.g., "tap" on supplement toggle and quick-add buttons; "save" on form submit success; "milestone" on first-ever session, every 10th session, first 30-day stretch; "session_end" on stop button. This list is documentation, not code, and it pays dividends — every later sound decision references it.
2. **Build a tiny JS sound layer** (`static/js/sounds.js`). A single `playSkinSound('tap')` function that reads the skin's sound config (already exposed via `skin_config.sounds`), respects the mute setting, silently no-ops if the file is missing. ~30 lines.
3. **Wire the triggers** — add `onclick="playSkinSound('tap')"` and equivalent on the right buttons. Form submits use a tiny JS listener.
4. **Add the mute toggle** — small speaker icon in the footer or header, persisted in `localStorage`. Greys when muted.
5. **Pick placeholder assets**. Each skin needs 4 distinct sounds. Until real sound design happens, the existing files (`lactea.mp3`, `chime.mp3`) can stand in for all four slots per skin (already wired). The real work is later: commissioning or sourcing tasteful short sounds.
6. **Write each skin's sonic identity in prose** (in `DESIGN_BRIEF.md`). E.g., "Cow: warm, organic, slightly playful — wooden, soft, never electronic. Plain: clean, minimal, breath-like — single tones, never melodic." Guides whoever sources the assets.

**Decisions:**
- **Mute UX** — global toggle (one switch) vs. per-trigger. *Rec: global for v1.*
- **Sound assets source** — commissioned (~$200–500), library (freesound.org), or AI-generated. *Rec: curated library now, commission for the launch-ready skins later.*
- **Default state** — sounds on or off by default. *Rec: off by default, surface the toggle prominently the first time the user saves a session.*

---

## Phase B — The daily field-journal prompt (engagement loop)

**Why second:** sound gives the app a *feel*; the daily prompt gives it a *reason to return tomorrow*. Without sound, prompts feel like nagging; with sound, they have texture.

**What it produces:** a small, dismissable card on the home page that asks one gentle question per day. The user can answer (one tap, or a sentence) or skip. The answer becomes part of their field journal. Different skins ask different questions in different voices.

**Steps:**

1. **Design the prompt pool** (~1–2 hours, no code). For each skin, write 30–60 prompts. Cow: warm, curious, sometimes silly. Plain: clean, observational. Rotate deterministically — same prompt for everyone-on-that-skin on a given day. Store in `skins/<name>/prompts.py`.
2. **Add the data model** — either a new model `DailyPromptResponse(date, prompt_id, skin, response_text)` OR add `prompt_id` + `prompt_response` to `DailyLog`. *Rec: separate model.* Prompts are skin-attributed; merging into DailyLog couples two concerns.
3. **Build the rotation function** — `get_today_prompt(skin)` returns the prompt deterministically based on date hash + pool size. Pure function, easy to test.
4. **Build the home-page prompt card** — appears above the "Today summary" tile. Small text input + "save" / "skip" buttons. After engagement, the card transforms into a quiet "Today's note: '<their answer>'" — editable but no longer asking.
5. **Build a prompt-history view** — small section on the progress page that scrolls through past prompts and answers. The field journal made visible.
6. **Wire to sound** — answering plays `save`. The rotation itself is silent; only the user's action makes sound.

**Decisions:**
- **Pool size** — 30 (monthly rotation), 60 (~bimonthly), 365 (daily). *Rec: 30 per skin, expand based on user reaction.*
- **Skip vs. dismiss** — does skipping count? *Rec: silently skip with no data trace. Engagement is opt-in; we're not counting compliance.*
- **Edit window** — once they answer, can they edit later that day? Next day? *Rec: edit any time the entry is still "today's"; after midnight, locked into history.*
- **Where prompts surface** — only home, or also a card on the daily log? *Rec: only home page, to keep the daily log focused on its dense data role.*

---

## Phase C — Skin-specific UI patterns (the differentiator)

**Why third:** deepest architectural change. Doing it after sound and prompt means those features inherit skin variation naturally. UI shapes first would mean writing two versions of skeletons that have no content yet.

**What it produces:** the daily log screen has genuinely different *shapes* per skin.
- **Cow**: card feed, one question per scrollable card, big tap targets, playful copy.
- **Plain**: clean single page, all fields visible, calm.
- **(Future Clinical)**: dense data form, side-by-side columns, evidence panel.

**The pattern:**

```
templates/
  daily_log.html              # thin shell: includes the right body
  skins/
    cow/
      daily_log_body.html     # card-feed shape
    plain/
      daily_log_body.html     # single-page shape
```

`daily_log.html` becomes ~10 lines that pick the body. The view stays unchanged. Same data, different shape. This is the architectural promise from session 4 made real.

**Steps:**

1. **Refactor `daily_log.html`** to delegate to `templates/skins/<skin>/daily_log_body.html`. The current template's content becomes the *base*, copied into both `cow/daily_log_body.html` and `plain/daily_log_body.html` as starting points.
2. **Reshape cow's variant** to a card-feed pattern. Each section (mood, breasts, energy, sleep, hydration, stress, tags, notes) becomes its own card. Scrollable. Big tap targets. One question dominant at a time.
3. **Refine plain's variant** to be more visually quiet — denser, less padding, no decorative emoji, smaller type scale.
4. **Verify identical POST behavior** — both shapes submit the same form to the same view. Same data lands.
5. **Repeat the pattern on home** — cow's home is encouraging-and-celebratory; plain's is just "what's today." Each gets its own `home_body.html`.

**Decisions:**
- **Which screen first** — daily log or home. *Rec: daily log, because that's where the field-journal philosophy lives.*
- **How different is "pretty differently"** — totally different layouts everywhere, or daily-log + home only? *Rec: daily-log + home only. Don't over-fragment.*

---

## Phase D — Documentation maintenance (small, ongoing)

After each phase: update `DESIGN_BRIEF.md`, `codebase_snapshot.md`, `task.md`. Add a `skins/README.md` explaining "how to make a new skin" once Phase C lands. The template will be: drop a folder with `skin.json`, `copy.py`, `prompts.py`, and the body templates you want to override.

---

## Phase E — Parking lot (not now, but named so we don't forget)

These were in the original polish menu but sound came first. Keep them on the radar:

- Custom illustrations per skin (vector art, empty-state scenes, skin-specific motifs)
- Animation & microinteractions (page transitions, button feedback, timer pulses)
- Typography rigor (custom font pairings per skin, real type hierarchy)
- Insight engine (from design brief: correlations, lagged correlations, pattern narration)
- Offline writes (Tier 2 PWA — IndexedDB queue + background sync)

---

## Effort estimate

| Phase | Rough effort | Output |
|---|---|---|
| A. Sound system | ~1 focused weekend | Real sonic identity per skin, mute toggle |
| B. Daily prompt | ~1 focused weekend | Real engagement loop, deeper field journal |
| C. UI patterns (daily log + home) | ~1–2 focused weekends | Skins finally feel like different experiences |
| D. Documentation | Rolling | Future-you and contributors aren't lost |

By the end of A–C, Lactea is **a different category of app** than what it is today — niche-community-aware, sonically distinctive, with a gentle engagement loop, and skins that genuinely differ in shape.

---

## Locked decisions (2026-05-23)

| # | Decision | Pick |
|---|---|---|
| 1 | Phase A — Mute UX | **Global toggle.** Single speaker icon in the footer, on/off, persisted in `localStorage`. |
| 2 | Phase A — Sound asset source | **Single placeholder per skin, defer audio decision.** Build the architecture; existing `lactea.mp3` / `chime.mp3` cover all four slots per skin until real audio sourcing happens as a separate concern. |
| 3 | Phase A — Default state | **Off by default, smart prompt on first save.** First-time prompt after first saved session: "Want sound feedback? Tap to enable." Persistent choice. |
| 4 | Phase B — Prompt pool size | **30 per skin, expand later.** Roughly monthly rotation. |
| 5 | Phase B — Prompt storage | **New `DailyPromptResponse` model.** Separate table with `date`, `prompt_id`, `skin`, `response_text`. Keeps DailyLog focused on dense field-journal data. |
| 6 | Phase C — First UI-shape screen | **Daily log first.** Sets the pattern; highest payoff for the field-journal philosophy. |
| 7 | Phase C — Differentiation depth | **Daily log + home only.** Two screens get truly different shapes per skin. Everything else shares one shape, varies in palette/copy/density. |

**Implications for Phase A implementation:**
- No asset commissioning, library scavenging, or AI-generation work needed now. Pure architecture.
- All four sound slots per skin currently point to one file. The system needs to handle this gracefully (same sound for tap, save, milestone, session_end on a given skin) without feeling broken — probably means short fade-outs and avoiding overlapping plays.
- Document each skin's *planned* sonic identity in `DESIGN_BRIEF.md` (cow = warm/organic/playful; plain = clean/breath-like/minimal) so whoever sources audio later has guidance.

**Implications for Phase B implementation:**
- New model means new migration (`0004_dailypromptresponse`).
- Initial prompt pool: 30 prompts × 2 skins = 60 strings to write. Plain skin can borrow neutrally-worded prompts from cow's pool where appropriate (inheritance, not duplication — though `prompts.py` doesn't follow the `copy.py` merge pattern; needs its own merge mechanism or per-skin pool).

**Implications for Phase C implementation:**
- Only `daily_log.html` and `home.html` get the per-skin body partial pattern. Other screens stay shared.
- Two body partials per skin (cow, plain) for daily log = 4 new files; same for home = 4 more. 8 new template files total. Maintainable.

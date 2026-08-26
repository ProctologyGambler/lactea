# Lactea — Design Brief for Developers

**Author:** Product owner + design partner (Claude, Anthropic)
**Date:** 2026-05-23
**Audience:** Any developer (human or AI) working on this codebase

This document captures the *why* behind every *what*. If you're about to make an implementation decision and this document has an opinion, follow it. If it's silent, use your judgment and flag the decision in `task.md`.

---

## 1. What Lactea is

Lactea is a personal tracking tool for people **inducing lactation without pregnancy**. That includes adoptive parents, trans women, non-gestational parents in queer families, surrogacy situations, people in kink/ANR relationships, and people under clinical IBCLC supervision. These communities overlap but experience the practice through very different cultural frames, vocabularies, and relationships to medical authority.

**The core insight:** all these people are doing roughly the same physical work (pumping, supplements, patience) but no app speaks to any of them specifically. Generic breastfeeding apps assume pregnancy. Clinical tools assume a medical context. Lactea meets each community where they are, using language and aesthetics that say *this was made for you.*

## 2. The product's personality

Lactea is **warm, knowledgeable, and unstuffy.** Think: a friend who happens to have done a lot of research. Not a doctor's office. Not a mommy blog. Not a clinical trial. The voice should feel like someone who takes the practice seriously without taking themselves too seriously.

Even in the most clinical skin, the tone is "let me show you what the evidence says" rather than "per the literature." Evidence is *accessible and situated in realistic communication* — meaning: real language, honest about uncertainty, never condescending, never hiding behind jargon.

## 3. The skin system — what it really is

### Not a theme picker

A skin is not a color swap. A skin is a **complete experiential frame** that changes:

| Layer | What changes | Example |
|---|---|---|
| **Visual** | Colors, typography, iconography, illustrations, layout emphasis | Cow skin: playful pink palette, cow illustrations, bouncy. Clinical skin: clean white/navy, no illustrations, dense information. |
| **Copy** | Every piece of user-facing text — labels, headings, empty states, encouragement messages, error text | Cow skin: "Time to moo! 🐮" → Clinical skin: "Begin session" |
| **Sound** | Audio cues (session end, milestones) | Cow skin: lactea.mp3. Clinical skin: clean chime. ANR skin: maybe silence by default. |
| **Information hierarchy** | Which features feel primary, which are tucked away | Clinical skin: supplement guide is front-and-center, evidence grades prominent. Community skin: daily log and streaks are primary. |
| **Epistemological stance** | How evidence and advice are framed | Clinical: citations, evidence grades, "consult your IBCLC." Community: "here's what people report," experiential knowledge centered. |

### How skins work architecturally

**Current state:** Middleware reads a `skin` cookie → `request.skin`. Templates include per-skin partials from `templates/skins/<name>/`. CSS variables in `skins.css` scope visual differences. This is correct scaffolding.

**Target state:**

```
skins/
├── cow/
│   ├── skin.json          # Manifest: display name, palette, font stack, feature flags
│   ├── copy.py            # Python dict of ALL user-facing strings for this skin
│   ├── partials/          # Template fragments (brand head, nav, pump button, etc.)
│   ├── assets/            # Images, sounds, icons specific to this skin
│   └── evidence.py        # How this skin frames evidence (citation style, language)
├── clinical/
│   ├── skin.json
│   ├── copy.py
│   └── ...
└── _base/
    └── copy.py            # Default copy; skins override keys they care about, inherit the rest
```

**`skin.json` manifest format:**

```json
{
  "name": "cow",
  "display_name": "Lactea 🐮",
  "description": "Playful and encouraging. For anyone who wants lactation tracking with personality.",
  "palette": {
    "primary": "#ec4899",
    "primary-light": "#fce7f3",
    "surface": "#fffbeb",
    "text": "#1f2937",
    "accent": "#f59e0b",
    "success": "#10b981",
    "border": "#f9a8d4"
  },
  "fonts": {
    "display": "'Baloo 2', cursive",
    "body": "'Nunito', sans-serif"
  },
  "features": {
    "show_evidence_grades": false,
    "show_citations_inline": false,
    "show_streaks": true,
    "show_encouragement": true,
    "show_field_log_framing": false,
    "supplement_guide_prominence": "secondary",
    "daily_log_prominence": "primary"
  },
  "sounds": {
    "session_end": "lactea.mp3",
    "milestone": "cowbell.mp3"
  }
}
```

**Guiding rules for skin implementation:**

1. **No business logic in skin code.** Skins change presentation, never behavior. The pump timer works identically in every skin; only what the button says and looks like changes.
2. **Inheritance, not duplication.** `_base/copy.py` has every string. A skin's `copy.py` only overrides what it changes. Rendering: `base_copy | skin_copy` (Python dict merge, skin wins).
3. **Drop-in test:** adding a new skin should require zero changes to views, models, or URLs. Drop a folder in `skins/`, add the name to `SKIN_CHOICES`, done.
4. **Skins are opt-in, not segmenting.** Any user can switch skins anytime. Don't gate features behind skins — use `features` flags to change *prominence*, not *availability*.

### Per-skin sonic identity

Sound is the fourth design layer (visual, copy, sound, info hierarchy). The architecture supports four sound slots per skin: **`tap`** (light affordance for selection actions like supplement toggle, quick-add), **`save`** (form submit confirmation), **`milestone`** (rare, meaningful — first session, every 10th session, first 30-day stretch), **`session_end`** (pump timer stop).

Sounds default to muted; the user is offered to enable them after their first saved session. A single global mute toggle lives in the footer.

Each skin should have a recognizable sonic identity — not a sound library, an *aesthetic*:

| Skin | Sonic identity (for whoever sources the audio) |
|---|---|
| **cow** | Warm, organic, slightly playful. Wooden, soft, never electronic. Think: a small acoustic mallet on hollow wood, a brief gentle "moo," a barn-soft bell. Not whimsical to the point of distraction. |
| **plain** | Clean, breath-like, minimal. Single tones, never melodic. Think: a single tasteful chime, a soft pluck, a felt-tipped piano note. The sonic equivalent of a well-set table. |
| **clinical** (future) | Neutral, professional, restrained. Defaults to silent except for save and session_end. When sound plays, it's a short utility tone — UI feedback, not personality. Think: medical-device-quality unobtrusive. |
| **bloom** (future) | Soft, affirming, slightly resonant. Natural materials — bells, water, breath. Sounds should feel like exhales, not punctuation. |
| **bond** (future) | Low, intimate, tasteful. Closer to silence than to chime. Sounds should never feel "app-y" — closer to a soft physical click than a notification. |
| **nest** (future) | Warm, soft, present. Wooden bowl sounds, a quiet wind chime, a single piano note. Conveys patience and presence without urgency. |

**Sonic implementation rules:**

1. **Skins set their own files.** Each skin's `skin.json` declares filenames for each slot. The JS sound layer reads these via the context processor; no per-skin JS.
2. **Same file across slots is OK during placeholder phase.** Currently all four slots per skin point to the existing `lactea.mp3` / `chime.mp3` placeholder. The architecture handles this gracefully (per-slot Audio instances avoid playback collisions).
3. **Mute is global, not per-trigger.** One switch, persisted in `localStorage`.
4. **Sounds are off by default.** First-saved-session prompt offers to enable them. After that, the footer toggle is the only control.

### Planned skins (in rough priority order)

| Skin | Audience | Aesthetic | Voice | Key emphasis |
|---|---|---|---|---|
| **cow** (exists) | General / playful | Pink, warm, illustrated cows, bouncy | Encouraging, lighthearted, emoji-friendly | Streaks, encouragement, celebration |
| **plain** (exists, minimal) | Anyone who wants less whimsy | Clean, neutral palette | Straightforward, warm but minimal | Balanced feature set |
| **clinical** | IBCLC-supervised, medical context | White/navy, no illustrations, information-dense | Professional, evidence-first, precise | Supplement guide with full citations, evidence grades, IBCLC-compatible export |
| **bloom** | Trans women, queer families | Soft botanical palette, floral motifs, gentle gradients | Affirming, celebratory of identity, never pathologizing | Hormone tracking integration (future), milestone celebrations, community framing |
| **bond** | ANR/kink-informed | Warm earth tones, intimate, tasteful | Matter-of-fact, no shame, no medicalization | Partner involvement features (future), session comfort tracking |
| **nest** | Adoptive parents, surrogacy | Warm amber/sage, nesting imagery | Hopeful, patient, acknowledging the wait | Timeline-to-first-drops milestones, bonding emphasis |

## 4. The Field Log — daily tracking reimagined

### Current state

The daily log captures mood (multi-select presets + free text) and breast feeling (same pattern) plus notes. It works, but it's passive — "how do you feel?" with no feedback loop.

### Vision: participatory self-study

Reframe the daily log as a **field journal**. The user is the researcher and the subject. Their body is the field site. Each day's entry is a field note.

This isn't just a framing trick — it changes what you build:

**What to track (expand the daily log model):**

- Mood and body state (already exists)
- **Energy level** (simple 1–5 or low/medium/high)
- **Sleep quality** (same)
- **Hydration** (rough sense: dehydrated / okay / well-hydrated)
- **Stress level** (1–5)
- **Menstrual cycle day** (optional, relevant to hormone fluctuation)
- **Hormone doses** (optional, for people on prescribed regimens — future feature, sensitive data, needs careful UX)
- **Custom tags** (user-defined, freeform — the ethnographer's notebook)

**What to surface (the insight engine):**

This is the feature nobody else has. The data is already there (pumping sessions + supplements + daily log). Connect them:

1. **Simple correlations** (build first):
   - Average output on days supplement X was taken vs. not taken
   - Average output by mood category
   - Average output by energy/sleep/hydration level
   - Output trend over time overlaid with supplement start dates

2. **Lagged correlations** (build second):
   - "Your output tends to increase 2–3 days after starting fenugreek" (supplements don't work instantly; a naive same-day correlation misses this)
   - "Your highest-output days follow nights you reported good sleep"

3. **Pattern narration** (build third, this is the magic):
   - Instead of just showing a chart, generate a plain-language summary: "Over the past 30 days, your average session output was 12ml. On days you took both fenugreek and moringa, your average was 18ml. You've logged 'hopeful' 8 times this month — that's more than last month."
   - This narration should be skin-aware. Clinical skin: "Data suggests a positive association between fenugreek supplementation and output volume." Cow skin: "Looks like fenugreek is your friend! 🌿"

**Important caveat to surface in all skins:** "Correlation is not causation. Many factors affect lactation. These patterns are observations from your own data, not medical conclusions." Clinical skin says this prominently; other skins say it gently but still say it.

### Implementation notes for the insight engine

- All computation happens server-side in Python. No client-side stats libraries needed.
- Start with simple aggregations using Django ORM (`annotate`, `aggregate`, `Case/When`).
- For lagged correlations: query supplement logs and pumping sessions, shift dates by N days, compare group means. This is ~20 lines of Python, not a data science project.
- Pattern narration: template strings with computed values. Not LLM-generated (keep it deterministic and auditable). A dict of narration templates per skin.
- New view: `/insights/` — the progress page currently shows pumping minutes over time. Keep that. Add a new page that focuses on cross-variable patterns.

## 5. PWA — pushing the boundaries

### Current state
Tier 1: app shell cached, loads offline after first visit. Offline writes not implemented.

### What "premium PWA" looks like

The goal is an app that feels native enough that people forget it's a website. This means:

**Tier 2: Offline writes (priority)**
- Use IndexedDB (via `idb` library or raw API) to store form submissions when offline
- Background Sync API to flush queued writes when connectivity returns
- UI indicator: subtle "saved locally, will sync" badge when offline
- This is critical for pumping — people pump in cars, hospital rooms, basements

**Tier 3: Push notifications (later)**
- "Time to pump!" reminders at user-configured intervals
- Supplement reminders
- Requires VAPID keys and a push server, but Django packages exist (`django-webpush`)

**Tier 4: Share Target API (later)**
- Let users share text/links to Lactea from other apps (e.g., a supplement recommendation from a forum → quick-add to supplement list)

### PWA polish that matters

- **Splash screen** that matches the active skin (manifest `background_color` + skin-specific icon)
- **Standalone display mode** (already in manifest — verify it's set)
- **Theme-color meta tag** that updates per skin (so the browser chrome / status bar matches)
- **Touch feedback**: `:active` states on all tappable elements, haptic-weight visual response
- **Pull-to-refresh** (native in standalone PWA, but make sure the app doesn't fight it)
- **Bottom nav** instead of top nav on mobile — thumb-reachable, app-like
- **Transition animations** between pages (HTMX + CSS transitions can fake SPA-like page changes)

## 6. Evidence presentation — doing it right

### Philosophy

"Research-backed" is meaningless if the user can't evaluate the research. Lactea doesn't just cite studies — it helps people understand what the evidence actually shows, with honesty about its limits.

### Per-supplement evidence card (supplement guide)

Each supplement in the guide should present:

- **What it is** — 1–2 sentences, plain language
- **What the evidence says** — summary of available research, in accessible language
- **Evidence quality** — a simple rating (strong / moderate / limited / anecdotal) with a one-line explanation of what that means
- **Common dosages** — what's reported in literature and community practice
- **How people take it** — practical notes (with food? time of day? ramp up?)
- **Side effects & interactions** — honest, specific, not buried
- **Source citations** — linked where possible, but don't let citations dominate the visual hierarchy

### Skin-specific evidence framing

- **Clinical skin:** Evidence grades prominent, citations inline, language like "randomized controlled trial (n=50) found..." Professional enough that an IBCLC could look over someone's shoulder and nod.
- **Community skins (cow, bloom, nest, bond):** Evidence quality shown but not leading. Language like "one study with 50 participants found..." Citations available on tap/expand, not inline. Community experience acknowledged: "Many people in online communities report..."
- **All skins:** Never hide negative evidence. Never overstate weak evidence. The app's credibility comes from honesty.

## 7. What "worth paying for" means

People pay for apps that do one of three things exceptionally:

1. **Save time they're already spending** — Lactea saves time vs. spreadsheets, paper logs, scattered notes
2. **Show them something they couldn't see alone** — the insight engine, correlations, pattern narration
3. **Make them feel understood** — the skin system, the copy, the entire emotional design

### Monetization model (tentative, for future planning)

- **Free tier:** Full tracking, one or two skins, 30-day insight history
- **Paid tier ($3–5/month or $30/year):** All skins, full insight history, CSV/PDF export, notification reminders
- **Skin packs or community editions** (alternative model): base app free, individual skins are $2–5 one-time

Don't build payment infrastructure yet. But design features with the free/paid boundary in mind so the migration isn't painful later.

## 8. Design principles — the short version

1. **Warm, not cute.** The cow skin can be playful; the system beneath is serious and respectful.
2. **Evidence-honest.** Never overstate. Never hide. Help people evaluate, don't evaluate for them.
3. **Community-aware.** Different people, different words, different comfort levels. Skins handle this.
4. **Offline-real.** If it doesn't work without signal, it doesn't work for pumping parents.
5. **Field-journal spirit.** The user is studying themselves. Give them good tools for that.
6. **No feature gatekeeping by identity.** Anyone can use any skin. Skins change prominence and framing, never lock features.
7. **One codebase, zero forks.** Every skin runs the same views, models, and URLs. Skin logic is strictly presentation.

## 9. Technical guardrails

- **Django function-based views.** No class-based views or DRF unless there's a specific reason.
- **HTMX for interactivity.** Not a JS framework. Server-render first, HTMX for partial updates where the UX demands it (pump timer, supplement toggle, field log save).
- **Vanilla JS only.** Chart.js for charts. No React, no Vue, no build step. The PWA service worker is the most complex JS in the app.
- **SQLite for now.** Single-user prototype. The local-first pivot (IndexedDB on device) is the long-term direction, not Postgres.
- **Tailwind via vendored Play CDN.** No build step. When/if the CSS gets unwieldy, consider switching to a static Tailwind build, but not yet.
- **Mobile-first responsive.** Design for a phone screen held one-handed while pumping. Desktop is nice-to-have.

## 10. Immediate next steps

In priority order:

1. **Finish and commit the skin system** — the cow/plain work that's sitting uncommitted. Fix the 405 bug.
2. **Implement `skin.json` + `copy.py` pattern** — so skins differ in words, not just visuals. Start with cow and plain having distinct copy.
3. **HTMX-ify the pump timer** — no full page reload on session log. Partial update, satisfying feedback.
4. **Expand the daily log** — add energy, sleep quality, hydration, stress. Keep it fast (one screen, tappable, < 30 seconds to complete).
5. **Build `/insights/`** — simple correlations first. "Your average output on fenugreek days vs. non-fenugreek days."
6. **Design the clinical skin** — this is the hardest skin because it requires the most distinct information hierarchy. If the system supports clinical + cow, it can support anything.
7. **Offline writes** — IndexedDB queue + background sync. This is what makes the PWA real.

---

*This document is alive. Update it as decisions are made. If a section becomes wrong, fix it — don't just append contradictions.*

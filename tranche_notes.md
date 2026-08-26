# Launch tranche notes

Scratch pad for augmenting the six-tranche plan.

---

## Locked decisions (2026-07-02)

| Decision | Choice |
|---|---|
| Launch skin | **Galactra®** first (Lactea + Via Lactea deferred) |
| Model | One-time purchase |
| Price | **$29** USD |
| Gate | Paid before first use + 30-day money-back guarantee |
| Consent copy | *"Improve the insight engine for people like me by contributing anonymized session data."* |
| Consent UX | Hard opt-in checkbox, positively framed, never pre-checked |
| Market | US-only at launch |
| Entity | LLC in your state (in parallel with build) |
| Hosting | Fly.io |
| Domain | `galactra.app` (fallback `getgalactra.com`) |
| Support email | `support@galactra.app` → forwarded to Proton, visible in footer |
| Legal | Termly free tier + I customize; no lawyer review |
| Founder account | `testusr` / `proctologygambler@proton.me` |
| Month-one success | 3–10 buyers = validation signal |
| Positioning | **Keep pharma aesthetic** with plainer tagline in tracked/uppercase type |
| Gate scope | Only Galactra host (Lactea + Via Lactea stay ungated for founder use) |
| Post-purchase UX | Welcome/onboarding page (new template + `has_seen_onboarding` flag) |
| Pre-launch content | Educational lactation page + expanded supplement guide (both in T3) |
| Supp suggestions | Moved to DB (`SupplementSuggestion`), editable via admin |
| Audio work | **Killed** (removed from parking lot) |

---

## T1 — Auth & per-user data foundation ✅ SHIPPED

---

## Original raw notes — tracked to completion

Preserved verbatim from your 2026-07-02 pass through this doc. Each item
carries a status marker; kept in this file until every marker flips to ✅.

### T2 notes

- ✅ **"only the Galactra host"** — locked as gate scope
- ⏳ **"i do not already have a stripe account"** — sign-up walkthrough will happen inside T2 when we need the API keys
- ✅ **"welcome/onboarding page is good"** — locked as post-purchase UX

### T3 notes

- ⚠ **"maybe support email just visible in settings?"** — my rec was to keep it in the footer (5-second path for frustrated paying users; SaaS convention). *Not confirmed by you yet — flag if you disagree.*

### T4 notes

- ✅ **"what is hero in this context?"** — answered: the top above-the-fold section (tagline + supporting line + primary CTA + often a screenshot). Definition also added to the T4 section below.

### Parking-lot notes

- ✅ **"what is the added cost of the insight engine?"** — answered: L1 ~2 sessions (rollups), L2 ~4 sessions (lagged correlations), L3 ~10+ sessions (LLM narrative). Documented in the parking lot.
- ✅ **"i don't think we need audio assets any longer"** — killed from the parking lot.

### Unsorted observations

- ✅ **Overview link on the Galactra logo** — brand nav is now clickable across all three skins, links to `home` (the Galactra Overview page).
- ✅ **ISI only in footer, not repeated at top** — top ISI band deleted from `templates/skins/galactra/home.html`; persistent footer ISI unchanged.
- ✅ **Tagline "a simple induced lactation tracker" in small letters that look professional** — set as `brand.tagline` in `skins/galactra/copy.py`, rendered as a tracked uppercase subtitle under the GALACTRA® wordmark in `_brand_nav.html`.
- ⏳ **Another tab with Cleveland Clinic-style lactation content** — planned for **T3**. Cannot copy CC content directly (copyright); I'll draft an original plain-language page in your voice, evidence-cited to CC + academic sources. *~1 session, pre-launch.*
- ⏳ **A page listing supplements people take for lactation induction with per-supplement info** — planned for **T3**. Expands existing `supplement_guide.html` into a monograph-style reference: every `SupplementSuggestion` gets purpose / evidence quality / dosages / side effects / citations. *~1–2 sessions, pre-launch.*
- ✅ **Add Saw Palmetto, Shatavari, Alfalfa to the supplements list** — Shatavari was already there; added Saw Palmetto + Alfalfa via `SupplementSuggestion` (migration `0006_supplement_suggestions.py`).
- ✅ **Room to add more supplements as your lactation group shares experiences** — `SupplementSuggestion` is now a real DB model, editable from Django admin (`/admin/core/supplementsuggestion/`). Add / reorder / retire without a code deploy.

**Legend:** ✅ done · ⏳ scheduled for a later tranche · ⚠ needs your confirmation

---

## Housekeeping (shipped 2026-07-02, session 13 second pass)

- Galactra tagline changed to *"A simple induced lactation tracker"* in `skins/galactra/copy.py`
- New brand nav on all three skins: whole brand block (icon + wordmark) is now clickable, links to `home`
- Galactra brand nav gets a small uppercase-tracked tagline line under the wordmark (pharma-humble register)
- Top ISI band removed from Galactra `home.html` (full ISI still lives in the persistent footer)
- New `SupplementSuggestion` model + migration `0006_supplement_suggestions.py`; seeded with the 6 originals + **Saw Palmetto** + **Alfalfa**. View + admin updated. You can now add/edit/reorder suggestions from Django admin.

---

## T2 — Stripe Checkout + purchase gate

- Stripe account: **not yet created** — sign-up walkthrough coming when needed
- Gate scope: **Galactra host only**
- Post-purchase: **welcome/onboarding page** (new UI to design)

Rest of the tranche unchanged: `stripe` package, env vars, `/purchase/` + success + cancel routes, `/stripe/webhook/`, `PaywallMiddleware`, three templates.

**Notes / changes:**

<!-- your thoughts here -->

---

## T3 — Legal, privacy, support surface + PRE-LAUNCH CONTENT

Expanded from the original T3.

- Per-skin Galactra `privacy.html` overlay (cross-skin data pooling disclosure, retention, exports, refunds)
- Terms of service — health-adjacent + paid + 30-day refund policy inline
- Support email in footer (Stripe / SaaS convention; frustrated paying users need a 5-second path)
- Landing page copy drafted here (locked before we build in T4)
- **Educational lactation page** — original plain-language content in Galactra's voice, biology + methods + timelines + expected challenges, evidence-cited to CC + academic sources. Cannot copy Cleveland Clinic directly (copyright).
- **Expanded supplement guide** — full monograph-style entries for each `SupplementSuggestion`: purpose, evidence quality, common dosages, side effects, sourced citations. Replaces the existing `supplement_guide.html` which was pre-existing tech debt.

**Notes / changes:**

<!-- your thoughts here -->

---

## T4 — Landing page

- Unauthenticated `/` on `galactra.app` — separate route from the app
- **Hero section** = the top-of-page above-the-fold section (tagline + supporting line + primary CTA + often a screenshot)
- Screenshots from a seeded demo account
- Sections: hero, who it's for, how it works, honest FAQ, pricing, refund guarantee, link to educational page + supplement guide
- The pharma aesthetic (ISI band, tabular tables, tracked type) is the marketing

**Notes / changes:**

<!-- your thoughts here -->

---

## T5 — Deploy + Postgres + monitoring

- Fly.io (~$3–10/mo) — small VM + managed Postgres
- SQLite → Postgres migration
- Env vars (secrets, Stripe keys, `SKIN_BY_HOST`)
- HTTPS via provider
- Sentry free tier for errors
- Domain registered + DNS pointed
- Deploy behind a "coming soon" gate first for end-to-end testing

**Notes / changes:**

<!-- your thoughts here -->

---

## T6 — Pre-launch smoke test + soft launch

- End-to-end round-trip: signup → purchase (real card) → use → refund → verify access revoked
- Test Stripe receipt email
- Runbook: how to check payments, handle a support email, issue a refund
- Announce quietly to IBCLC groups, adoption forums, LGBT parenting communities, r/lactationinducement etc.

**Notes / changes:**

<!-- your thoughts here -->

---

## Post-launch parking lot

- **Insight engine** — three levels of depth, ~2 sessions for L1 (simple rollups), ~4 for L2 (lagged correlations), ~10+ for L3 (LLM narrative summaries)
- Phase B — daily field-journal prompt feature
- Phase C — per-skin `pump_timer.html`, `daily_log.html`, `supplements.html`, `progress.html` overlays
- Via Lactea paintings rotation (16-painting starter set approved)
- Lactea + Via Lactea monetization
- `privacy.html` still carries hardcoded pink Tailwind classes (partly resolved by T3 Galactra overlay)

**Removed from parking lot:**
- ~~Real audio assets per skin~~ (killed 2026-07-02)
- ~~`supplement_guide.html` refactor~~ (subsumed into T3 expansion)

**Notes / changes:**

<!-- your thoughts here -->

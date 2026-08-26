# Resume here — Stripe walkthrough paused mid-T2

**Paused:** 2026-07-02, during T2 (Stripe Checkout + purchase gate).

**Where we are:**
- T1 shipped and verified (auth + per-user data foundation)
- Session-13 housekeeping done (Galactra tagline, brand nav → clickable, top-ISI removed, Saw Palmetto + Alfalfa + DB-driven `SupplementSuggestion`)
- T2 tasks created in the task list
- **In-flight:** Stripe account walkthrough Phases 1-3 (user creating Stripe account, getting test keys, creating the $29 product)

**To resume — hand Claude these three values and say "ready to wire it up":**
```
STRIPE_PUBLISHABLE_KEY=pk_test_...
STRIPE_SECRET_KEY=sk_test_...
STRIPE_PRICE_ID=price_...
```

Instructions for getting them are in the chat transcript under "Stripe account walkthrough — Phases 1-3", but the short version:
1. **stripe.com/register** — sign up, verify email, ignore "activate account" nudge
2. Dashboard → **Developers → API keys** → copy publishable + reveal/copy secret (both `_test_` variants)
3. Dashboard → **Products → + Add product** → name "Galactra® — Lifetime access", type **One-off**, price **$29.00 USD** → copy the `price_...` ID

**Once Claude has the three values, the next actions (T2 tasks #9–#15):**
1. `pip install stripe`, add to requirements, wire settings from env
2. Add `has_seen_onboarding` field to `UserProfile` + migration
3. Build `/purchase/`, `/success/`, `/cancel/` views
4. Build webhook handler for `checkout.session.completed` + `charge.refunded`
5. Build `PaywallMiddleware` (Galactra host only, superuser bypass)
6. Build purchase / success / cancel / onboarding templates
7. Verify with Stripe CLI + test card `4242 4242 4242 4242` + refund round-trip

**Anchor documents to re-read on return:**
- `task.md` (session 13 entry) — what's shipped
- `tranche_notes.md` — locked decisions + your original raw notes tracked to completion
- Task list — T2 sub-tasks pre-created

**No pending code state:** all housekeeping edits saved, migration 0006 applied, `manage.py check` clean, dev server can be restarted anytime with `venv/bin/python manage.py runserver`.

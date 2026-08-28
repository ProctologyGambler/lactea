# Design pivot — unified Via Lactea (2026-08-27)

Decided by PG with Relay, 2026-08-27. This supersedes the "Galactra ships first"
launch decision in `tranche_notes.md`. Everything else in the tranche plan
(pricing, gate, consent, hosting, legal) carries over, pointed at one product.

---

## The decision

**One unified Milky Way product.** The three-skin strategy collapses: the
`via_lactea` celestial aesthetic becomes THE app. Galactra and cow are retired
from the launch path (keep the code — possible marketing material or future
return, but no further maintenance).

**Why this brand:** *galaxy* comes from Greek *gala* — milk. The Milky Way is
literally named for lactation; *galactagogue* shares the root. No competitor
can claim the metaphor.

**Naming/domain status:** `lactea.app` is registered by a third party (checked
2026-08-27). `vialactea.app` appears unregistered — confirm at a registrar and
lock it (~$14–20/yr). The app's display name can remain "Lactea" or
"Via Lactea" regardless of domain — to be re-locked with PG.

**Price:** $29 one-time carries over, pending PG's confirmation for the
unified product.

---

## The engagement mechanic — rules of the sky

These are product rules, not suggestions. PG's explicit requirement: induction
takes months before measurable output, and users at the *beginning* of the
journey must see lights, stars, and beautiful things immediately. Never gate
celebration on milliliters.

1. **Stars mark sessions, never milliliters.** Every logged pumping session
   adds a star to the user's sky, from night one. The sky rewards the only
   thing the user controls: showing up.
2. **The nebula is the nursery.** Every session also feeds a personal nebula —
   wisps of gas and color that visibly deepen with consistency. The
   pre-lactation months read as growth, not absence. (Real astronomy: stars
   form inside nebulas.)
3. **First measurable drops = ignition.** A star kindles *inside* the nebula
   the user spent months building. Copy anchor: "Every star in the sky was
   born in a cloud like this one."
4. **Skies don't go backward.** Output adds brightness; it never subtracts.
   There is no failure state anywhere in this design — only accumulation.
5. **Consistency becomes geometry.** Weekly session clusters draw
   constellation lines; streaks earn comets. The progress page becomes a
   personal star map, replacing the Chart.js bar charts.

**Mockup:** `design/mockups/nebula-first-light.html` in this repo — open it in
a browser. Three home screens (Day 3 / Day 40 / Day 112) showing the
nebula-to-first-light progression, fully animated. All CSS/SVG, no images, no
libraries — the same techniques the production app will use. Typography in the
mockup is Fraunces (candidate display face; the mockup loads it from Google
Fonts, but production must vendor/self-host it — no CDN dependency).

---

## Approved feature: the ✦ push notification

Silent web push at the user's scheduled session times.

- Payload is near-empty — just "✦", no sound, no words. **Privacy is the
  feature:** nothing on a lock screen says "lactation," and nothing sensitive
  transits the Google/Apple push relays.
- Vibration is OS-owned (web Vibration API is foreground-only; absent on iOS).
  Include a one-time hint pointing users at their phone's vibrate-only
  notification setting.
- Implementation: server-side scheduled push, Django + pywebpush/VAPID — free,
  no Firebase. iOS requires the PWA installed to home screen (16.4+).
- Same-family bonus: Screen Wake Lock API to keep the screen dimly on during
  an active pump session (foreground-only, works today).

---

## Tech debt — fix BEFORE visual work (~1 session)

`static/js/tailwind.js` is the 400KB Tailwind **Play CDN browser-JIT build** —
it recompiles CSS in the browser on every page load. Not supported for
production, and slowest on exactly the old/cheap phones the app is for.
Replace with Tailwind CLI compiled static CSS (same classes, same look).
When the star map lands, `chart.min.js` (204KB) can be dropped too.

---

## Build sequence

1. Re-lock unified decisions with PG: name/domain, price confirmation
2. Cleanup session: `via_lactea` as default + sole exposed skin; Tailwind CLI
   compile replacing the Play CDN build
3. Star map / nebula build per the mockup (home + progress)
4. Typography + iconography pass (vendored display face; SVG glyph set —
   star, moon phases, comet)
5. ✦ push notification feature
6. Resume T2 Stripe against the unified product (`PaywallMiddleware` re-scoped
   from Galactra-host-only to the unified host)

Framework verdict, for the record: **Django stays.** The aesthetic lives
entirely in templates/CSS; the backend is sound (T1 shipped). All redesign
work is CSS, SVG, and vendored fonts — zero new libraries, zero new services,
nothing recurring until deploy.

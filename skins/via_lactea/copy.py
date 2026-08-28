# skins/via_lactea/copy.py
# ──────────────────────────────────────────────────────────────────────
# Lactea — "the Milky Way." A quiet night sky for a slow practice.
# (Internal skin identifier remains `via_lactea` to avoid a data
# migration on the source_skin field; user-facing brand is "Lactea"
# per docs/design-pivot-2026-08-27.md.)
# Voice: spare, intentional, mythopoetic without being precious.
# Celestial vocabulary (sky, night, light, dust, drift, course) used
# sparingly. Override _base only where the new voice lands.
# ──────────────────────────────────────────────────────────────────────

COPY = {
    # ── Brand ──────────────────────────────────────────────────────
    "brand.name":                  "Lactea",
    "brand.tagline":               "A quiet sky for a slow practice.",
    "brand.emoji":                 "✦",

    # ── Nav ────────────────────────────────────────────────────────
    "nav.home":                    "Home",
    "nav.pump":                    "Session",
    "nav.supplements":             "Supplements",
    "nav.daily":                   "Log",
    "nav.progress":                "Course",

    # ── Home ───────────────────────────────────────────────────────
    "home.welcome":                "Welcome to the night sky",
    "home.start_session":          "Begin a session",
    "home.start_session_sub":      "When the moment finds you.",
    "home.start_session_icon":     "✦",
    "home.today":                  "Tonight",
    "home.min_pumped":             "Minutes",
    "home.sessions":               "Sessions",
    "home.supplements":            "Supplements",
    "home.recent_sessions":        "Recent sessions",
    "home.lifetime_prefix":        "Across all your nights, you've gathered",
    "home.lifetime_suffix":        "minutes",
    "home.no_sessions_yet":        "No sessions yet. The sky is patient.",

    # ── Pump ───────────────────────────────────────────────────────
    "pump.title":                  "Session",
    "pump.subtitle":               "Settle in. Begin when you're ready.",
    "pump.ready":                  "Ready when you are.",
    "pump.log_title":              "Mark this session",
    "pump.notes_label":            "Notes",

    # ── Daily log ──────────────────────────────────────────────────
    "daily.title":                 "Field log",
    "daily.subtitle":              "A small record of the day's weather.",
    "daily.log_today":             "Log today",
    "daily.notes_placeholder":     "What was today like?",
    "daily.past_entries":          "Earlier entries",
    "daily.no_entries":            "Nothing logged yet. The first entry can be tonight.",

    # ── Supplements ────────────────────────────────────────────────
    "supps.title":                 "Supplements",
    "supps.subtitle":              "Your daily regimen, kept simple.",
    "supps.guide_link":            "Open the supplement reference",
    "supps.guide_link_icon":       "✦",

    # ── Progress ───────────────────────────────────────────────────
    "progress.title":              "Course",
    "progress.subtitle":           "The shape of your weeks, the drift of your days.",
    "progress.volume_icon":        "·",

    # ── Footer ─────────────────────────────────────────────────────
    "footer.message":              "Kept quietly · stays on your device",

    # ── Encouragement (subtle; never effusive) ─────────────────────
    "encourage.first_session":     "First session marked.",
    "encourage.streak_3":          "Three nights running.",
    "encourage.streak_7":          "A week of sessions. Steady.",
    "encourage.output_increase":   "Output is trending upward.",
    "encourage.keep_going":        "This is slow work, done well.",
}

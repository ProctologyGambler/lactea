# skins/_base/copy.py
# ──────────────────────────────────────────────────────────────────────
# Every user-facing string in Lactea lives here.  Skin-specific copy.py
# files override whichever keys they want; everything else inherits.
#
# Keys are flat and dot-namespaced:  "page.element.variant"
# Values are plain strings — no HTML, no template tags.
# ──────────────────────────────────────────────────────────────────────

COPY = {
    # ── Global / brand ──────────────────────────────────────────────
    "brand.name":                  "Lactea",
    "brand.tagline":               "Your gentle lactation companion",
    "brand.emoji":                 "",

    # ── Nav labels ──────────────────────────────────────────────────
    "nav.home":                    "Home",
    "nav.pump":                    "Pump",
    "nav.supplements":             "Supplements",
    "nav.daily":                   "Daily",
    "nav.progress":                "Progress",

    # ── Home page ───────────────────────────────────────────────────
    "home.welcome":                "Welcome",
    "home.start_session":          "Start a session",
    "home.start_session_sub":      "Whenever you're ready",
    "home.start_session_icon":     "⏰",
    "home.today":                  "Today",
    "home.min_pumped":             "Min pumped",
    "home.sessions":               "Sessions",
    "home.supplements":            "Supplements",
    "home.recent_sessions":        "Recent sessions",
    "home.lifetime_prefix":        "You've pumped a lifetime total of",
    "home.lifetime_suffix":        "minutes",
    "home.no_sessions_yet":        "No sessions yet — you've got this.",

    # ── Pump timer ──────────────────────────────────────────────────
    "pump.title":                  "Pumping Session",
    "pump.subtitle":               "Start whenever you're ready",
    "pump.ready":                  "Ready when you are",
    "pump.today_label":            "Today:",
    "pump.start":                  "START",
    "pump.stop":                   "STOP",
    "pump.reset":                  "RESET",
    "pump.log_title":              "Log this session",
    "pump.notes_label":            "Notes",
    "pump.left_label":             "Left breast (ml)",
    "pump.right_label":            "Right breast (ml)",
    "pump.save":                   "Save session",
    "pump.cancel":                 "Cancel",
    "pump.form_errors_intro":      "Couldn't save your session:",

    # ── Daily log (field journal) ───────────────────────────────────
    "daily.title":                 "Daily Log",
    "daily.subtitle":              "A quick check-in on how today's going",
    "daily.log_today":             "Log today",
    "daily.update_today":          "Update today's log",
    "daily.mood_label":            "How's your mood?",
    "daily.mood_hint":             "pick any combination, or add your own",
    "daily.mood_custom_placeholder": "Or add your own — comma-separated (e.g. anxious, hopeful)",
    "daily.breast_label":          "How do your breasts feel?",
    "daily.breast_hint":           "pick any combination, or add your own",
    "daily.breast_custom_placeholder": "Or add your own — comma-separated (e.g. tingly, achy)",
    "daily.energy_label":          "Energy level",
    "daily.sleep_label":           "How did you sleep?",
    "daily.hydration_label":       "Hydration",
    "daily.stress_label":          "Stress level",
    "daily.tags_label":            "Custom tags",
    "daily.notes_label":           "Notes",
    "daily.notes_placeholder":     "How are you feeling? Anything to remember about today?",
    "daily.form_errors_intro":     "Couldn't save your log:",
    "daily.save":                  "Save today's log",
    "daily.update":                "Update",
    "daily.past_entries":          "Past entries",
    "daily.no_entries":            "No past entries yet — your daily log starts today.",
    "daily.past_mood_label":       "Mood",
    "daily.past_breast_label":     "Breasts",

    # ── Supplements ─────────────────────────────────────────────────
    "supps.title":                 "Supplements",
    "supps.subtitle":              "Track what you're taking and your daily compliance",
    "supps.guide_link":            "Read the supplement guide",
    "supps.guide_link_icon":       "📖",
    "supps.today_checklist":       "Today's checklist",
    "supps.taken_today":           "Taken today",
    "supps.mark_taken":            "Mark taken today",
    "supps.no_supps":              "No supplements tracked yet.",
    "supps.no_supps_hint":         "Add one below to start tracking.",
    "supps.quick_add":             "Quick add",
    "supps.quick_add_hint":        "These fill the name only — you'll add your own dosage and frequency.",
    "supps.add_title":             "Add a supplement",
    "supps.add_button":            "Add to my regimen",
    "supps.form_errors_intro":     "Couldn't add the supplement:",
    "supps.delete_confirm":        "Remove this supplement from your regimen?",
    "supps.form_name_label":       "Name",
    "supps.form_dosage_label":     "Dosage",
    "supps.form_frequency_label":  "Frequency",
    "supps.form_notes_label":      "Notes",

    # ── Supplement guide ────────────────────────────────────────────
    "guide.title":                 "Supplement Guide for Inducing Lactation Without Pregnancy",
    "guide.subtitle":              "A research-backed reference covering herbal galactagogues and pharmaceutical options.",
    "guide.disclaimer_title":      "Important: This Is Not Medical Advice",
    "guide.back_link":             "Back to supplements tracker",

    # ── Progress ────────────────────────────────────────────────────
    "progress.title":              "Progress",
    "progress.subtitle":           "Your pumping trends over time",
    "progress.total_time":         "Total time",
    "progress.sessions":           "Sessions",
    "progress.volume_tracked":     "Volume tracked",
    "progress.volume_icon":        "💧",
    "progress.minutes_per_day":    "Minutes per day",
    "progress.no_sessions":        "No pumping sessions logged yet. Start a session to see your progress here.",
    "progress.daily_breakdown":    "Daily breakdown",
    "progress.no_data_window":     "Nothing logged in this window yet.",

    # ── Footer ──────────────────────────────────────────────────────
    "footer.message":              "Made with care for your lactation journey · All data stays private",
    "footer.export":               "Export all data as CSV",
    "footer.privacy":              "Privacy",
    "footer.theme_label":          "Theme:",

    # ── Encouragement (shown contextually) ──────────────────────────
    "encourage.first_session":     "You did it — first session logged!",
    "encourage.streak_3":          "Three days in a row. Consistency is everything.",
    "encourage.streak_7":          "A full week of sessions. You're building something real.",
    "encourage.output_increase":   "Your output is trending up. Your body is responding.",
    "encourage.keep_going":        "This takes time and patience. You're doing the work.",
}

"""
AutoHand Configuration
======================
Central config for API keys, model settings, and action schema.
LLM: Google Gemini (google-genai >= 1.0)
"""

import os

# --- API CONFIG (HARDCODED FOR DEMO) ---
GOOGLE_API_KEY = "AQ.Ab8RN6LjTiaMDYrfzbznrCQukKniiNXDQ9GRSoXBnZdRaEsNig"
GEMINI_MODEL = "gemini-1.5-flash"

# ─── Safety ───────────────────────────────────────────────────────────────────
SAFE_MODE = True   # restrict to whitelisted actions only

# ─── Allowed Actions (whitelist for planner) ──────────────────────────────────
ALLOWED_ACTIONS = {
    "open_app",
    "type_text",
    "press_keys",
    "save_file",
    "create_excel_file",
    "open_vscode",
    "write_code",
    "create_text_file",
    "wait",
    "take_screenshot",
}

# ─── Flask ────────────────────────────────────────────────────────────────────
FLASK_PORT  = 5000
FLASK_DEBUG = False

# ─── Timing ───────────────────────────────────────────────────────────────────
TYPING_INTERVAL    = 0.04   # seconds between keystrokes
APP_LAUNCH_WAIT    = 2      # seconds after launching an app
ACTION_RETRY_COUNT = 1      # retry once on failure

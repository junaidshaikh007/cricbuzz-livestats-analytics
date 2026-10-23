"""
Cricbuzz LiveStats Configuration Module
Defines system-wide constants, database paths, and API settings.
"""

import os
from pathlib import Path

# Base Paths
BASE_DIR = Path(__file__).resolve().parent
DATABASE_DIR = BASE_DIR / "database"
DATABASE_PATH = DATABASE_DIR / "cricbuzz.db"
SCHEMA_PATH = DATABASE_DIR / "schema.sql"
SQL_DIR = BASE_DIR / "sql"
ASSETS_DIR = BASE_DIR / "assets"
CSS_PATH = ASSETS_DIR / "style.css"

# Ensure runtime directories exist
DATABASE_DIR.mkdir(parents=True, exist_ok=True)
SQL_DIR.mkdir(parents=True, exist_ok=True)
ASSETS_DIR.mkdir(parents=True, exist_ok=True)

# RapidAPI Cricbuzz Configuration
RAPIDAPI_KEY = os.getenv("CRICBUZZ_API_KEY", "")
RAPIDAPI_HOST = "cricbuzz-cricket.p.rapidapi.com"
RAPIDAPI_BASE_URL = f"https://{RAPIDAPI_HOST}"

# App Branding
APP_TITLE = "Cricbuzz LiveStats"
APP_SUBTITLE = "Real-Time Cricket Insights & SQL-Based Analytics"
APP_ICON = "🏏"
APP_VERSION = "2.5.0"

# Color Palette (Dark Stadium Neon Theme)
COLORS = {
    "primary": "#14B8A6",       # Vibrant Teal
    "primary_dark": "#0F766E",
    "accent_gold": "#E8A33D",    # Gold
    "accent_fire": "#E879F9",    # Party/Neon
    "bg_dark": "#0B1220",        # Deep Navy Black
    "card_dark": "#131C2E",      # Elevated Surface
    "card_border": "#1F2C42",
    "text_main": "#E5E7EB",
    "text_muted": "#8A97AB",
    "success": "#3FB950",
    "danger": "#F0616D"
}

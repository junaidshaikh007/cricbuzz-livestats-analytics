"""
Cricbuzz LiveStats - Settings & Diagnostics Page
Configures API credentials, manages database reseeding, and provides full data exports.
"""

import streamlit as st
import pandas as pd
import sqlite3
import os
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

import config
from utils.helpers import load_custom_css
from api.cricbuzz_api import CricbuzzAPIClient
from database.db_connection import reseed_database, get_database_stats, execute_query

st.set_page_config(page_title="Settings | Cricbuzz LiveStats", page_icon="⚙️", layout="wide")
load_custom_css()

st.markdown("""
    <div class="app-header-badge">⚙️ System Configuration</div>
    <h2 style="font-weight:800; margin-bottom:4px;">Application Settings & Diagnostics</h2>
    <p style="color:#94A3B8; font-size:14px;">Configure RapidAPI keys, reset databases, and export analytics telemetry.</p>
""", unsafe_allow_html=True)

col1, col2 = st.columns([1.5, 1.5])

# -------------------------------------------------------------
# API CONFIGURATION
# -------------------------------------------------------------
with col1:
    st.markdown("### 🌐 Cricbuzz RapidAPI Setup")
    st.markdown("""
        You can connect your free RapidAPI Cricbuzz key to stream live Cricbuzz server feeds.
        *(If omitted, the platform runs on high-fidelity built-in live telemetry).*
    """)

    curr_key = os.getenv("CRICBUZZ_API_KEY", "")
    user_api_key = st.text_input("RapidAPI Key (optional)", value=curr_key, type="password", placeholder="Enter your RapidAPI key here...")

    c_test, c_save = st.columns([1, 1])
    if c_test.button("🧪 Test Connection", use_container_width=True):
        client = CricbuzzAPIClient(api_key=user_api_key)
        res = client.test_connection()
        if res["status"] == "connected":
            st.success(res["message"])
        elif res["status"] == "offline_mode":
            st.info(res["message"])
        else:
            st.error(res["message"])

    if c_save.button("💾 Apply API Key", use_container_width=True):
        os.environ["CRICBUZZ_API_KEY"] = user_api_key.strip()
        st.success("API Key updated in runtime environment!")

    st.markdown("---")

    # -------------------------------------------------------------
    # DATABASE CONTROLS & RESEED
    # -------------------------------------------------------------
    st.markdown("### 🗄️ Database Management")
    stats = get_database_stats()
    st.write(f"**Database Location:** `{config.DATABASE_PATH}`")
    st.write(f"**Current Records:** {stats.get('players', 0)} Players, {stats.get('matches', 0)} Matches, {stats.get('venues', 0)} Venues.")

    st.warning("Need to restore the original 40+ player and 50+ match test dataset?")
    if st.button("🔄 Reset & Reseed Database to Factory Defaults", use_container_width=True):
        with st.spinner("Seeding database..."):
            success = reseed_database()
            if success:
                st.success("Database successfully re-initialized and seeded with fresh data!")
                st.rerun()
            else:
                st.error("Failed to reseed database.")

# -------------------------------------------------------------
# DATA EXPORT CENTER
# -------------------------------------------------------------
with col2:
    st.markdown("### 📥 Data Export Center")
    st.markdown("Download full tables from the database in CSV format for offline reporting.")

    export_table = st.selectbox("Select Table to Export", ["players", "matches", "venues", "teams", "player_format_stats", "partnerships"])
    df_exp = execute_query(f"SELECT * FROM {export_table}")
    
    st.dataframe(df_exp.head(5), use_container_width=True, hide_index=True)
    csv_bytes = df_exp.to_csv(index=False).encode('utf-8')

    st.download_button(
        label=f"📥 Download {export_table.upper()} (CSV)",
        data=csv_bytes,
        file_name=f"cricbuzz_{export_table}.csv",
        mime="text/csv",
        use_container_width=True
    )

    st.markdown("---")

    # -------------------------------------------------------------
    # SYSTEM TELEMETRY
    # -------------------------------------------------------------
    st.markdown("### ℹ️ Environment Info")
    st.markdown(f"""
        - **Python Version:** `{sys.version.split()[0]}`
        - **Streamlit Version:** `{st.__version__}`
        - **SQLite Version:** `{sqlite3.sqlite_version}`
        - **App Version:** `{config.APP_VERSION}`
        - **Theme Mode:** `Dark Sports Glassmorphism`
    """)

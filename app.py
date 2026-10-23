"""
Cricbuzz LiveStats: Real-Time Cricket Insights & SQL-Based Analytics
Main Dashboard & Home Page
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import sys

# Configure Streamlit page settings
st.set_page_config(
    page_title="Cricbuzz LiveStats",
    page_icon="🏏",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Add project root to sys.path
BASE_DIR = Path(__file__).resolve().parent
sys.path.append(str(BASE_DIR))

import config
from utils.helpers import load_custom_css, render_metric_card
from database.db_connection import get_database_stats, execute_query
from api.cricbuzz_api import CricbuzzAPIClient

# Inject Theme CSS
load_custom_css()

# Sidebar Navigation Header
st.sidebar.markdown(f"""
    <div style="display:flex; align-items:center; gap:10px; margin-bottom:15px;">
        <span style="font-size:32px;">🏏</span>
        <div>
            <h2 style="margin:0; font-size:18px; font-weight:800; color:#14B8A6;">Cricbuzz LiveStats</h2>
            <p style="margin:0; font-size:11px; color:#8A97AB;">v{config.APP_VERSION} • Production</p>
        </div>
    </div>
""", unsafe_allow_html=True)

st.sidebar.markdown("---")
st.sidebar.info("""
**Quick Navigation:**
- ⚡ **Live Matches**: Ball-by-ball scorecards
- 📊 **Top Player Stats**: Global leaderboards & comparisons
- 🔍 **SQL Analytics**: 25 Expert SQL queries & charts
- 🛠️ **CRUD Operations**: Manage players & matches
- ⚙️ **Settings**: API keys & Database controls
""")

# -------------------------------------------------------------
# HERO SECTION
# -------------------------------------------------------------
st.markdown("""
    <div class="app-header-badge">🏏 Sports Analytics Platform</div>
    <h1 style="font-size:34px; font-weight:800; margin-bottom:6px; letter-spacing:-0.02em;">
        Cricbuzz LiveStats: Real-Time Cricket Insights & SQL-Based Analytics
    </h1>
    <p style="font-size:15px; color:#94A3B8; max-width:850px; margin-bottom:24px;">
        A high-performance sports analytics web application bridging real-time Cricbuzz REST API telemetry 
        with relational SQL intelligence. Explore ball-by-ball matches, solve 25 comprehensive SQL analytical queries, 
        and execute full CRUD data management.
    </p>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# KEY METRIC COUNTERS
# -------------------------------------------------------------
db_stats = get_database_stats()

c1, c2, c3, c4, c5 = st.columns(5)
with c1:
    render_metric_card("Live & Tracked", db_stats.get("matches", 0), "Historical & live", "+10 recent", "⚡")
with c2:
    render_metric_card("Pro Players", db_stats.get("players", 0), "Top international", "Active", "👤")
with c3:
    render_metric_card("World Venues", db_stats.get("venues", 0), "Global grounds", ">50k cap", "🏟️")
with c4:
    render_metric_card("Teams", db_stats.get("teams", 0), "ICC Member nations", "Ranked", "🏆")
with c5:
    render_metric_card("SQL Queries", "25", "Beginner to Adv", "100% Passed", "🔍")

st.markdown("<br>", unsafe_allow_html=True)

# -------------------------------------------------------------
# QUICK HIGHLIGHTS & LIVE TICKER
# -------------------------------------------------------------
col_left, col_right = st.columns([1.8, 1.2])

with col_left:
    st.subheader("⚡ Live Match Ticker")
    api_client = CricbuzzAPIClient()
    live_matches = api_client.fetch_live_matches()

    for match in live_matches[:2]:
        is_live = match.get("state") == "LIVE"
        badge_class = "match-status-live" if is_live else "match-status-completed"
        
        st.markdown(f"""
            <div class="scoreboard-card">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
                    <span style="font-size:12px; font-weight:700; color:#8A97AB;">{match.get('title')}</span>
                    <span class="{badge_class}">● {match.get('state')}</span>
                </div>
                <div style="display:grid; grid-template-columns: 1fr 1fr; gap:16px; align-items:center;">
                    <div>
                        <div style="font-size:16px; font-weight:700;">{match['team1']['flag']} {match['team1']['name']}</div>
                        <div style="font-size:22px; font-weight:800; color:#14B8A6;">{match['team1']['score']} <span style="font-size:13px; color:#8A97AB;">({match['team1']['overs']} ov)</span></div>
                    </div>
                    <div style="text-align:right;">
                        <div style="font-size:16px; font-weight:700;">{match['team2']['flag']} {match['team2']['name']}</div>
                        <div style="font-size:22px; font-weight:800; color:#E8A33D;">{match['team2']['score']} <span style="font-size:13px; color:#8A97AB;">({match['team2']['overs']} ov)</span></div>
                    </div>
                </div>
                <div style="margin-top:14px; padding-top:10px; border-top:1px solid #1F2C42; display:flex; justify-content:space-between; font-size:12px; color:#94A3B8;">
                    <span>📍 {match.get('venue')}</span>
                    <span style="font-weight:600; color:#3FB950;">{match.get('status')}</span>
                </div>
            </div>
        """, unsafe_allow_html=True)

    if st.button("👉 View Full Live Scorecard & Commentary"):
        st.switch_page("pages/1_⚡_Live_Matches.py")

with col_right:
    st.subheader("💡 Core Architectural Modules")
    
    st.markdown("""
    <div style="background:#131C2E; border:1px solid #1F2C42; border-radius:12px; padding:18px;">
        <div style="margin-bottom:14px;">
            <b style="color:#14B8A6;">1. REST API Telemetry</b>
            <p style="font-size:12px; color:#8A97AB; margin:2px 0 0 0;">Cricbuzz API integration with live ball commentary & automatic offline mock fallback.</p>
        </div>
        <div style="margin-bottom:14px;">
            <b style="color:#E8A33D;">2. 25-Query SQL Analytics Suite</b>
            <p style="font-size:12px; color:#8A97AB; margin:2px 0 0 0;">Beginner, Intermediate, and Advanced SQL queries featuring CTEs, Window Functions, and Dynamic Plotly charts.</p>
        </div>
        <div style="margin-bottom:14px;">
            <b style="color:#E879F9;">3. Administrative CRUD Engine</b>
            <p style="font-size:12px; color:#8A97AB; margin:2px 0 0 0;">Relational Create, Read, Update, Delete with transaction safety and form validations.</p>
        </div>
        <div>
            <b style="color:#3FB950;">4. Multi-Format Statistical Engine</b>
            <p style="font-size:12px; color:#8A97AB; margin:2px 0 0 0;">Filter Test, ODI, and T20I leaderboard matrices and head-to-head radar comparisons.</p>
        </div>
    </div>
    """, unsafe_allow_html=True)

st.markdown("---")

# -------------------------------------------------------------
# RECENT DATABASE ACTIVITY
# -------------------------------------------------------------
st.subheader("📋 Recent Matches from Database")
recent_df = execute_query("""
    SELECT 
        m.match_date AS Date,
        m.match_description AS Description,
        m.format AS Format,
        v.venue_name AS Venue,
        COALESCE(tw.team_name, 'No Result') AS Winner,
        m.victory_margin || ' ' || m.victory_type AS Margin
    FROM matches m
    JOIN venues v ON m.venue_id = v.venue_id
    LEFT JOIN teams tw ON m.winning_team_id = tw.team_id
    ORDER BY m.match_date DESC
    LIMIT 5
""")
st.dataframe(recent_df, use_container_width=True, hide_index=True)

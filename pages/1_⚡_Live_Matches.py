"""
Cricbuzz LiveStats - Live Match Telemetry Page
Displays live scorecards, current batsmen/bowler status, ball-by-ball commentary, and match charts.
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

import config
from utils.helpers import load_custom_css
from api.cricbuzz_api import CricbuzzAPIClient
import plotly.graph_objects as go

st.set_page_config(page_title="Live Matches | Cricbuzz LiveStats", page_icon="⚡", layout="wide")
load_custom_css()

st.markdown("""
    <div class="app-header-badge">⚡ Real-Time Cricbuzz Telemetry</div>
    <h2 style="font-weight:800; margin-bottom:4px;">Live Match Centre</h2>
    <p style="color:#94A3B8; font-size:14px;">Instant match scorecards, player strike rates, ball-by-ball commentary, and telemetry.</p>
""", unsafe_allow_html=True)

api_client = CricbuzzAPIClient()
matches = api_client.fetch_live_matches()

if not matches:
    st.warning("No active matches found. Check your API settings or retry.")
    st.stop()

# Match Selector Dropdown
match_titles = [f"{m['team1']['name']} vs {m['team2']['name']} ({m.get('format', 'T20')}) - {m.get('title')}" for m in matches]
selected_idx = st.selectbox("Select Active Match", range(len(matches)), format_func=lambda i: match_titles[i])
match = matches[selected_idx]

# -------------------------------------------------------------
# MAIN SCORECARD BANNER
# -------------------------------------------------------------
is_live = match.get("state") == "LIVE"
status_badge = '<span class="match-status-live">● LIVE MATCH</span>' if is_live else f'<span class="match-status-completed">● {match.get("state")}</span>'

st.markdown(f"""
<div class="scoreboard-card">
    <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:12px;">
        <span style="font-size:13px; font-weight:700; color:#8A97AB;">{match.get('title')} • {match.get('format')}</span>
        {status_badge}
    </div>
    <div style="display:grid; grid-template-columns: 1fr auto 1fr; gap:20px; align-items:center;">
        <div>
            <div style="font-size:20px; font-weight:800;">{match['team1']['flag']} {match['team1']['name']}</div>
            <div style="font-size:32px; font-weight:900; color:#14B8A6; font-variant-numeric:tabular-nums;">
                {match['team1']['score']} 
                <span style="font-size:15px; font-weight:500; color:#8A97AB;">({match['team1']['overs']} ov)</span>
            </div>
        </div>
        <div style="text-align:center; padding:0 20px;">
            <span style="font-size:20px; font-weight:800; color:#64748B;">VS</span>
            <div style="font-size:12px; color:#8A97AB; margin-top:4px;">CRR: {match.get('crr', '-')} | RRR: {match.get('rrr', '-')}</div>
        </div>
        <div style="text-align:right;">
            <div style="font-size:20px; font-weight:800;">{match['team2']['flag']} {match['team2']['name']}</div>
            <div style="font-size:32px; font-weight:900; color:#E8A33D; font-variant-numeric:tabular-nums;">
                {match['team2']['score']} 
                <span style="font-size:15px; font-weight:500; color:#8A97AB;">({match['team2']['overs']} ov)</span>
            </div>
        </div>
    </div>
    <div style="margin-top:16px; padding-top:12px; border-top:1px solid #1F2C42; display:flex; justify-content:space-between; align-items:center; flex-wrap:wrap;">
        <span style="font-size:13px; color:#94A3B8;">📍 <b>Venue:</b> {match.get('venue')}</span>
        <span style="font-size:13px; color:#14B8A6; font-weight:600;">🪙 {match.get('toss', '')}</span>
        <span style="font-size:14px; font-weight:700; color:#3FB950;">📢 {match.get('status')}</span>
    </div>
</div>
""", unsafe_allow_html=True)

# -------------------------------------------------------------
# CURRENT BATSMEN & BOWLER + RECENT BALLS
# -------------------------------------------------------------
col1, col2 = st.columns([1.6, 1.4])

with col1:
    st.subheader("🏏 Batsmen at Crease")
    batsmen = match.get("current_batsmen", [])
    if batsmen:
        b_data = []
        for b in batsmen:
            b_data.append({
                "Batsman": f"{b['name']} {'⭐ (Strike)' if b.get('on_strike') else ''}",
                "Runs": b.get("runs", 0),
                "Balls": b.get("balls", 0),
                "4s": b.get("fours", 0),
                "6s": b.get("sixes", 0),
                "SR": b.get("sr", 0.0)
            })
        st.dataframe(pd.DataFrame(b_data), use_container_width=True, hide_index=True)
    else:
        st.info("Innings summary available in historical log.")

    st.subheader("🎯 Bowler in Action")
    bowler = match.get("current_bowler", {})
    if bowler:
        bw_df = pd.DataFrame([{
            "Bowler": bowler.get("name"),
            "Overs": bowler.get("overs"),
            "Maidens": bowler.get("maidens"),
            "Runs": bowler.get("runs"),
            "Wickets": bowler.get("wickets"),
            "Econ": bowler.get("econ")
        }])
        st.dataframe(bw_df, use_container_width=True, hide_index=True)

with col2:
    st.subheader("⏱️ Recent Balls in Current Over")
    recent = match.get("recent_balls", [])
    badges_html = '<div style="display:flex; align-items:center; gap:8px; margin-bottom:18px;">'
    for ball in recent:
        if ball == "4":
            bclass = "ball-dot ball-four"
        elif ball == "6":
            bclass = "ball-dot ball-six"
        elif ball == "W":
            bclass = "ball-dot ball-wicket"
        else:
            bclass = "ball-dot ball-normal"
        badges_html += f'<span class="{bclass}">{ball}</span>'
    badges_html += '</div>'
    st.markdown(badges_html, unsafe_allow_html=True)

    st.subheader("🎙️ Ball-by-Ball Commentary")
    comm_list = match.get("commentary", [])
    if comm_list:
        for c in comm_list:
            st.markdown(f"""
                <div style="padding:8px 12px; background:#131C2E; border-left:3px solid #14B8A6; border-radius:4px; margin-bottom:8px; font-size:13px;">
                    <b style="color:#14B8A6;">{c.get('ball')}</b> - <span style="color:#E5E7EB;">{c.get('comm')}</span>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.info("Live commentary awaiting next over.")

st.markdown("---")

# -------------------------------------------------------------
# RUN RATE & INNINGS PROGRESSION CHART
# -------------------------------------------------------------
st.subheader("📈 Innings Run Rate Progression")
# Generate match worm chart
overs = list(range(1, 21))
team1_worm = [int(i * 8.8 + (i % 3) * 2) for i in overs]
team2_worm = [int(i * 8.4 + (i % 2) * 3) for i in overs]

fig = go.Figure()
fig.add_trace(go.Scatter(x=overs, y=team1_worm, mode="lines+markers", name=match['team1']['name'], line=dict(color="#14B8A6", width=3)))
fig.add_trace(go.Scatter(x=overs, y=team2_worm, mode="lines+markers", name=match['team2']['name'], line=dict(color="#E8A33D", width=3, dash="dash")))

fig.update_layout(
    title=f"Run Progression Comparison: {match['team1']['name']} vs {match['team2']['name']}",
    xaxis_title="Overs",
    yaxis_title="Total Runs",
    paper_bgcolor="rgba(0,0,0,0)",
    plot_bgcolor="rgba(0,0,0,0)",
    font={"color": "#E5E7EB"},
    gridcolor="#1F2C42"
)
st.plotly_chart(fig, use_container_width=True)

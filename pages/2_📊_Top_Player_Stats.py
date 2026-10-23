"""
Cricbuzz LiveStats - Top Player Statistics Page
Provides global leaderboards, format filters, head-to-head radar comparisons, and player dossiers.
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

import config
from utils.helpers import load_custom_css
from database.db_connection import execute_query
from utils.visualization import plot_bar, plot_radar_comparison

st.set_page_config(page_title="Top Player Stats | Cricbuzz LiveStats", page_icon="📊", layout="wide")
load_custom_css()

st.markdown("""
    <div class="app-header-badge">📊 Global Cricket Leaderboards</div>
    <h2 style="font-weight:800; margin-bottom:4px;">Top Player Statistics & Comparisons</h2>
    <p style="color:#94A3B8; font-size:14px;">Analyze global batting and bowling leaderboards, cross-format matrices, and player head-to-heads.</p>
""", unsafe_allow_html=True)

tab1, tab2, tab3 = st.tabs(["🏆 Leaderboards", "⚔️ Head-to-Head Radar", "👤 Player Dossier"])

# -------------------------------------------------------------
# TAB 1: LEADERBOARDS
# -------------------------------------------------------------
with tab1:
    c1, c2 = st.columns([1, 1])
    with c1:
        stat_metric = st.selectbox("Select Metric Category", ["Most Runs", "Most Wickets", "Highest Individual Score", "Best Batting Average", "Best Bowling Economy"])
    with c2:
        format_filter = st.selectbox("Select Cricket Format", ["ODI", "Test", "T20I"])

    if stat_metric == "Most Runs":
        query = """
            SELECT 
                p.full_name AS Player,
                p.country AS Country,
                pfs.matches AS Matches,
                pfs.innings AS Innings,
                pfs.runs AS [Total Runs],
                pfs.batting_average AS [Batting Avg],
                pfs.strike_rate AS [Strike Rate],
                pfs.centuries AS [100s],
                pfs.half_centuries AS [50s]
            FROM player_format_stats pfs
            JOIN players p ON pfs.player_id = p.player_id
            WHERE pfs.format = ?
            ORDER BY pfs.runs DESC
            LIMIT 15
        """
        df = execute_query(query, (format_filter,))
        st.dataframe(df, use_container_width=True, hide_index=True)
        if not df.empty:
            fig = plot_bar(df.head(10), x="Player", y="Total Runs", title=f"Top 10 Run Scorers ({format_filter})")
            st.plotly_chart(fig, use_container_width=True)

    elif stat_metric == "Most Wickets":
        query = """
            SELECT 
                p.full_name AS Player,
                p.country AS Country,
                pfs.matches AS Matches,
                pfs.wickets AS [Total Wickets],
                pfs.bowling_average AS [Bowling Avg],
                pfs.economy_rate AS [Economy],
                pfs.catches AS Catches
            FROM player_format_stats pfs
            JOIN players p ON pfs.player_id = p.player_id
            WHERE pfs.format = ? AND pfs.wickets > 0
            ORDER BY pfs.wickets DESC
            LIMIT 15
        """
        df = execute_query(query, (format_filter,))
        st.dataframe(df, use_container_width=True, hide_index=True)
        if not df.empty:
            fig = plot_bar(df.head(10), x="Player", y="Total Wickets", title=f"Top Wicket Takers ({format_filter})")
            st.plotly_chart(fig, use_container_width=True)

    elif stat_metric == "Highest Individual Score":
        query = """
            SELECT 
                p.full_name AS Player,
                p.country AS Country,
                pfs.highest_score AS [Highest Score],
                pfs.runs AS [Career Runs],
                pfs.format AS Format
            FROM player_format_stats pfs
            JOIN players p ON pfs.player_id = p.player_id
            WHERE pfs.format = ?
            ORDER BY pfs.highest_score DESC
            LIMIT 15
        """
        df = execute_query(query, (format_filter,))
        st.dataframe(df, use_container_width=True, hide_index=True)
        if not df.empty:
            fig = plot_bar(df.head(10), x="Player", y="Highest Score", title=f"Top Individual Innings ({format_filter})")
            st.plotly_chart(fig, use_container_width=True)

    elif stat_metric == "Best Batting Average":
        query = """
            SELECT 
                p.full_name AS Player,
                p.country AS Country,
                pfs.batting_average AS [Batting Average],
                pfs.runs AS [Career Runs],
                pfs.matches AS Matches
            FROM player_format_stats pfs
            JOIN players p ON pfs.player_id = p.player_id
            WHERE pfs.format = ? AND pfs.matches >= 10
            ORDER BY pfs.batting_average DESC
            LIMIT 15
        """
        df = execute_query(query, (format_filter,))
        st.dataframe(df, use_container_width=True, hide_index=True)
        if not df.empty:
            fig = plot_bar(df.head(10), x="Player", y="Batting Average", title=f"Best Batting Averages ({format_filter})")
            st.plotly_chart(fig, use_container_width=True)

    else:
        query = """
            SELECT 
                p.full_name AS Player,
                p.country AS Country,
                pfs.economy_rate AS [Economy Rate],
                pfs.wickets AS [Wickets],
                pfs.matches AS Matches
            FROM player_format_stats pfs
            JOIN players p ON pfs.player_id = p.player_id
            WHERE pfs.format = ? AND pfs.economy_rate > 0 AND pfs.matches >= 10
            ORDER BY pfs.economy_rate ASC
            LIMIT 15
        """
        df = execute_query(query, (format_filter,))
        st.dataframe(df, use_container_width=True, hide_index=True)
        if not df.empty:
            fig = plot_bar(df.head(10), x="Player", y="Economy Rate", title=f"Most Miserly Bowlers ({format_filter})")
            st.plotly_chart(fig, use_container_width=True)

# -------------------------------------------------------------
# TAB 2: HEAD-TO-HEAD RADAR COMPARISON
# -------------------------------------------------------------
with tab2:
    st.subheader("⚔️ Player vs Player Radar Matrix")
    all_players = execute_query("SELECT player_id, full_name, country FROM players ORDER BY full_name ASC").to_dict("records")
    player_names = [f"{p['full_name']} ({p['country']})" for p in all_players]

    rc1, rc2, rc3 = st.columns([1.2, 1.2, 1])
    with rc1:
        p1_idx = st.selectbox("Select Player 1", range(len(all_players)), index=0, format_func=lambda i: player_names[i])
    with rc2:
        # Default to another player
        p2_idx = st.selectbox("Select Player 2", range(len(all_players)), index=min(1, len(all_players)-1), format_func=lambda i: player_names[i])
    with rc3:
        comp_format = st.selectbox("Comparison Format", ["ODI", "Test", "T20I"], key="radar_fmt")

    p1_id = all_players[p1_idx]["player_id"]
    p2_id = all_players[p2_idx]["player_id"]

    stats_q = """
        SELECT 
            pfs.player_id,
            p.full_name,
            pfs.batting_average,
            pfs.strike_rate,
            pfs.centuries * 10 AS century_factor,
            pfs.wickets,
            CASE WHEN pfs.economy_rate > 0 THEN (12.0 - pfs.economy_rate) * 5 ELSE 0 END AS economy_factor,
            pfs.catches * 2 AS fielding_factor
        FROM player_format_stats pfs
        JOIN players p ON pfs.player_id = p.player_id
        WHERE pfs.player_id IN (?, ?) AND pfs.format = ?
    """
    comp_df = execute_query(stats_q, (p1_id, p2_id, comp_format))

    if len(comp_df) == 2:
        r1 = comp_df[comp_df["player_id"] == p1_id].iloc[0]
        r2 = comp_df[comp_df["player_id"] == p2_id].iloc[0]

        dict1 = {
            "Batting Avg": float(r1["batting_average"]),
            "Strike Rate": min(160.0, float(r1["strike_rate"])),
            "Centuries": float(r1["century_factor"]),
            "Wickets": min(100.0, float(r1["wickets"])),
            "Bowling Econ": float(r1["economy_factor"]),
            "Fielding": float(r1["fielding_factor"])
        }
        dict2 = {
            "Batting Avg": float(r2["batting_average"]),
            "Strike Rate": min(160.0, float(r2["strike_rate"])),
            "Centuries": float(r2["century_factor"]),
            "Wickets": min(100.0, float(r2["wickets"])),
            "Bowling Econ": float(r2["economy_factor"]),
            "Fielding": float(r2["fielding_factor"])
        }

        radar_fig = plot_radar_comparison(r1["full_name"], dict1, r2["full_name"], dict2)
        st.plotly_chart(radar_fig, use_container_width=True)
    else:
        st.info(f"One or both players do not have recorded career data in {comp_format} format.")

# -------------------------------------------------------------
# TAB 3: PLAYER DOSSIER
# -------------------------------------------------------------
with tab3:
    st.subheader("👤 Career Dossier & Profile Search")
    selected_p = st.selectbox("Search Any Player", range(len(all_players)), format_func=lambda i: player_names[i], key="dossier_p")
    target_pid = all_players[selected_p]["player_id"]

    p_info = execute_query("SELECT * FROM players WHERE player_id = ?", (target_pid,)).iloc[0]
    p_stats = execute_query("SELECT format, matches, innings, runs, highest_score, batting_average, strike_rate, centuries, half_centuries, wickets, economy_rate FROM player_format_stats WHERE player_id = ?", (target_pid,))

    st.markdown(f"""
        <div style="background:#131C2E; border:1px solid #1F2C42; border-radius:12px; padding:20px; margin-bottom:20px;">
            <div style="display:flex; justify-content:space-between; align-items:center;">
                <div>
                    <h2 style="margin:0; font-size:24px; font-weight:800; color:#14B8A6;">{p_info['full_name']}</h2>
                    <p style="margin:4px 0 0 0; color:#8A97AB;">{p_info['country']} • {p_info['playing_role']}</p>
                </div>
                <div style="text-align:right;">
                    <span style="background:rgba(20,184,166,0.15); color:#14B8A6; padding:4px 12px; border-radius:99px; font-weight:700; font-size:12px;">ACTIVE SQUAD</span>
                </div>
            </div>
            <div style="display:grid; grid-template-columns: repeat(4, 1fr); gap:14px; margin-top:18px;">
                <div><span style="color:#8A97AB; font-size:11px;">BATTING STYLE</span><br><b>{p_info['batting_style']}</b></div>
                <div><span style="color:#8A97AB; font-size:11px;">BOWLING STYLE</span><br><b>{p_info['bowling_style']}</b></div>
                <div><span style="color:#8A97AB; font-size:11px;">DATE OF BIRTH</span><br><b>{p_info['dob']}</b></div>
                <div><span style="color:#8A97AB; font-size:11px;">ROLE CODE</span><br><b>{p_info['playing_role']}</b></div>
            </div>
        </div>
    """, unsafe_allow_html=True)

    st.markdown("#### Multi-Format Career Record")
    st.dataframe(p_stats, use_container_width=True, hide_index=True)

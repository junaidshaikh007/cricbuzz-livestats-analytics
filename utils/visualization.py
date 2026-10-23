"""
Visualization Utility Module
Generates modern, interactive Plotly visualizations for cricket analytics.
Uses high-contrast dark theme colors, crisp typography, and responsive tooltips.
"""

import plotly.express as px
import plotly.graph_objects as go
import pandas as pd
from typing import Optional, Dict, Any, List
import config

THEME_BG = "#0B1220"
THEME_CARD = "#131C2E"
THEME_LINE = "#1F2C42"
TEXT_COLOR = "#E5E7EB"
TEAL = "#14B8A6"
GOLD = "#E8A33D"
PURPLE = "#E879F9"
GREEN = "#3FB950"
RED = "#F0616D"


def _apply_dark_theme(fig: go.Figure, title: str = "") -> go.Figure:
    """Applies unified dark theme styling across all Plotly figures."""
    fig.update_layout(
        title={
            "text": title,
            "y": 0.95,
            "x": 0.5,
            "xanchor": "center",
            "yanchor": "top",
            "font": {"size": 16, "color": TEXT_COLOR, "family": "Inter, sans-serif"}
        },
        paper_bgcolor="rgba(0,0,0,0)",
        plot_bgcolor="rgba(0,0,0,0)",
        font={"color": TEXT_COLOR, "family": "Inter, sans-serif"},
        margin=dict(l=40, r=40, t=50, b=40),
        legend=dict(
            bgcolor="rgba(19, 28, 46, 0.7)",
            bordercolor=THEME_LINE,
            borderwidth=1,
            font={"size": 11, "color": TEXT_COLOR}
        )
    )
    fig.update_xaxes(
        gridcolor=THEME_LINE,
        zerolinecolor=THEME_LINE,
        tickfont={"size": 11, "color": "#8A97AB"}
    )
    fig.update_yaxes(
        gridcolor=THEME_LINE,
        zerolinecolor=THEME_LINE,
        tickfont={"size": 11, "color": "#8A97AB"}
    )
    return fig


def plot_bar(df: pd.DataFrame, x: str, y: str, title: str, color: Optional[str] = None, orientation: str = "v") -> go.Figure:
    """Builds sleek bar chart."""
    if orientation == "h":
        fig = px.bar(df, x=x, y=y, orientation="h", color=color, color_discrete_sequence=[TEAL, GOLD, PURPLE])
    else:
        fig = px.bar(df, x=x, y=y, color=color, color_discrete_sequence=[TEAL, GOLD, PURPLE])
    fig.update_traces(marker_line_width=0, opacity=0.9)
    return _apply_dark_theme(fig, title)


def plot_pie(df: pd.DataFrame, names: str, values: str, title: str) -> go.Figure:
    """Builds interactive donut chart."""
    fig = px.pie(
        df, names=names, values=values, hole=0.55,
        color_discrete_sequence=[TEAL, GOLD, PURPLE, "#38BDF8", "#F43F5E", "#A855F7"]
    )
    fig.update_traces(textposition='inside', textinfo='percent+label', marker=dict(line=dict(color=THEME_CARD, width=2)))
    return _apply_dark_theme(fig, title)


def plot_scatter(df: pd.DataFrame, x: str, y: str, title: str, hover_name: Optional[str] = None, size: Optional[str] = None, color: Optional[str] = None) -> go.Figure:
    """Builds interactive scatter/bubble chart."""
    fig = px.scatter(
        df, x=x, y=y, hover_name=hover_name, size=size, color=color,
        color_discrete_sequence=[TEAL, GOLD, PURPLE],
        size_max=22
    )
    fig.update_traces(marker=dict(line=dict(width=1, color=TEXT_COLOR)))
    return _apply_dark_theme(fig, title)


def plot_line(df: pd.DataFrame, x: str, y: str, title: str, color: Optional[str] = None) -> go.Figure:
    """Builds multi-line or single trendline chart."""
    fig = px.line(
        df, x=x, y=y, color=color, markers=True,
        color_discrete_sequence=[TEAL, GOLD, PURPLE, "#38BDF8"]
    )
    fig.update_traces(line=dict(width=3), marker=dict(size=8))
    return _apply_dark_theme(fig, title)


def plot_radar_comparison(player1_name: str, p1_stats: Dict[str, float], player2_name: str, p2_stats: Dict[str, float]) -> go.Figure:
    """Generates head-to-head radar comparison chart."""
    categories = list(p1_stats.keys())
    fig = go.Figure()

    fig.add_trace(go.Scatterpolar(
        r=[p1_stats[c] for c in categories] + [p1_stats[categories[0]]],
        theta=categories + [categories[0]],
        fill='toself',
        name=player1_name,
        line=dict(color=TEAL, width=2),
        fillcolor='rgba(20, 184, 166, 0.3)'
    ))

    fig.add_trace(go.Scatterpolar(
        r=[p2_stats[c] for c in categories] + [p2_stats[categories[0]]],
        theta=categories + [categories[0]],
        fill='toself',
        name=player2_name,
        line=dict(color=GOLD, width=2),
        fillcolor='rgba(232, 163, 61, 0.3)'
    ))

    fig.update_layout(
        polar=dict(
            radialaxis=dict(visible=True, showline=False, gridcolor=THEME_LINE, tickfont=dict(color="#8A97AB")),
            angularaxis=dict(gridcolor=THEME_LINE, linecolor=THEME_LINE, tickfont=dict(color=TEXT_COLOR))
        ),
        paper_bgcolor="rgba(0,0,0,0)",
        font={"color": TEXT_COLOR, "family": "Inter, sans-serif"},
        margin=dict(l=40, r=40, t=40, b=40)
    )
    return fig


def plot_question_chart(question_meta: Dict[str, Any], df: pd.DataFrame) -> Optional[go.Figure]:
    """Dynamically returns the best matched visualization for a given SQL practice question."""
    if df.empty:
        return None

    ctype = question_meta.get("chart_type", "table")
    title = question_meta.get("title", "")

    if ctype == "bar_runs":
        return plot_bar(df, x="player_name", y="total_runs", title=f"Top ODI Run Scorers - {title}")
    elif ctype == "bar_capacity":
        return plot_bar(df, x="venue_name", y="capacity", title=f"Venue Capacity Comparison - {title}")
    elif ctype == "bar_wins":
        return plot_bar(df, x="team_name", y="total_wins", title=f"Total Match Wins by Team - {title}")
    elif ctype == "pie_roles":
        return plot_pie(df, names="playing_role", values="total_players", title=f"Squad Role Composition - {title}")
    elif ctype == "bar_scores":
        return plot_bar(df, x="format", y="highest_individual_score", title=f"Highest Score by Format - {title}")
    elif ctype == "scatter_allrounders":
        return plot_scatter(df, x="total_runs", y="total_wickets", hover_name="player_name", color="format", title=f"All-Rounder Matrix (Runs vs Wickets) - {title}")
    elif ctype == "bar_cross_format":
        melted = pd.melt(df, id_vars=["player_name"], value_vars=["test_runs", "odi_runs", "t20i_runs"], var_name="Format", value_name="Runs")
        return plot_bar(melted, x="player_name", y="Runs", color="Format", title=f"Cross-Format Run Breakdown - {title}")
    elif ctype == "bar_home_away":
        melted = pd.melt(df, id_vars=["team_name"], value_vars=["home_wins", "away_wins"], var_name="Condition", value_name="Wins")
        return plot_bar(melted, x="team_name", y="Wins", color="Condition", title=f"Home vs Away Win Analysis - {title}")
    elif ctype == "scatter_bowling":
        return plot_scatter(df, x="avg_economy_rate", y="total_wickets", hover_name="bowler_name", color="venue_name", title=f"Bowling Economy vs Wickets by Venue - {title}")
    elif ctype == "bar_clutch":
        return plot_bar(df, x="player_name", y="avg_runs_close_matches", title=f"Clutch Batting Averages in Thrillers - {title}")
    elif ctype == "line_yearly":
        return plot_line(df, x="match_year", y="avg_runs_per_match", color="player_name", title=f"Annual Batting Average Trends Since 2020 - {title}")
    elif ctype == "bar_toss":
        return plot_bar(df, x="toss_decision", y="win_percentage", title=f"Win Percentage by Toss Decision - {title}")
    elif ctype == "scatter_econ":
        return plot_scatter(df, x="overall_economy_rate", y="total_wickets", hover_name="bowler_name", title=f"Economy Rate vs Total Wickets - {title}")
    elif ctype == "scatter_consistency":
        return plot_scatter(df, x="run_std_dev", y="average_runs", hover_name="batsman_name", title=f"Consistency Quadrant (Std Dev vs Avg Runs) - {title}")
    elif ctype == "bar_ranking":
        return plot_bar(df, x="player_name", y="total_score", color="format", title=f"Comprehensive Player Performance Ranking - {title}")
    elif ctype == "bar_h2h":
        return plot_bar(df, x="team_a", y="team_a_win_pct", title=f"Head to Head Win Percentage - {title}")
    elif ctype == "bar_form":
        return plot_bar(df, x="player_name", y="avg_runs_last_5", color="current_form_status", title=f"Recent Batting Momentum - {title}")
    elif ctype == "bar_partnerships":
        df["pair"] = df["batsman_1"] + " & " + df["batsman_2"]
        return plot_bar(df, x="pair", y="avg_partnership_runs", title=f"Average Partnership Stand - {title}")
    elif ctype == "line_trajectory":
        return plot_line(df, x="quarter_year", y="current_q_runs", color="player_name", title=f"Quarterly Performance Trajectory - {title}")
    return None

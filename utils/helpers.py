"""
Helper Utilities Module
Provides Streamlit UI style injection, badge renderers, and formatters.
"""

import streamlit as st
from pathlib import Path
import config


def load_custom_css():
    """Injects custom high-end CSS styling into Streamlit."""
    css_file = config.CSS_PATH
    if css_file.exists():
        with open(css_file, "r", encoding="utf-8") as f:
            css_code = f.read()
        st.markdown(f"<style>{css_code}</style>", unsafe_allow_html=True)


def render_metric_card(title: str, value: Any, subtext: str = "", delta: str = "", icon: str = "🏏"):
    """Renders a modern glassmorphic metric card."""
    st.markdown(f"""
        <div class="metric-card">
            <div class="metric-header">
                <span class="metric-title">{title}</span>
                <span class="metric-icon">{icon}</span>
            </div>
            <div class="metric-value">{value}</div>
            <div class="metric-subtext">{subtext} <span class="metric-delta">{delta}</span></div>
        </div>
    """, unsafe_allow_html=True)


def format_role_badge(role: str) -> str:
    """Returns styled HTML badge for playing roles."""
    colors = {
        "Batsman": "#00A9B4",
        "Bowler": "#E8A33D",
        "All-rounder": "#14B8A6",
        "Wicket-keeper": "#E879F9"
    }
    col = colors.get(role, "#64748B")
    return f'<span style="background:{col}22; color:{col}; border:1px solid {col}55; padding:2px 8px; border-radius:12px; font-size:11px; font-weight:600;">{role}</span>'

"""
Cricbuzz LiveStats - 25 SQL Practice Questions & Interactive Analytics
Beginner (Q1-Q8), Intermediate (Q9-Q16), Advanced (Q17-Q25), plus Custom SQL Playground.
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

import config
from utils.helpers import load_custom_css
from services.analytics_service import AnalyticsService, SQL_QUESTIONS
from utils.visualization import plot_question_chart
from database.db_connection import get_table_names, get_table_schema

st.set_page_config(page_title="SQL Analytics | Cricbuzz LiveStats", page_icon="🔍", layout="wide")
load_custom_css()

st.markdown("""
    <div class="app-header-badge">🔍 SQL Analytical Engine</div>
    <h2 style="font-weight:800; margin-bottom:4px;">25 SQL Practice Queries & Insights</h2>
    <p style="color:#94A3B8; font-size:14px;">Master cricket data analytics across Beginner, Intermediate, and Advanced SQL challenges.</p>
""", unsafe_allow_html=True)

tab_practice, tab_playground = st.tabs(["📚 25 Guided SQL Practice Questions", "💻 Custom SQL Playground"])

# -------------------------------------------------------------
# TAB 1: 25 GUIDED QUESTIONS
# -------------------------------------------------------------
with tab_practice:
    c1, c2 = st.columns([1, 2.5])
    
    with c1:
        difficulty_filter = st.radio(
            "Select Difficulty Tier",
            ["All 25 Questions", "Beginner (Q1 - Q8)", "Intermediate (Q9 - Q16)", "Advanced (Q17 - Q25)"],
            horizontal=False
        )

        filtered_questions = SQL_QUESTIONS
        if difficulty_filter == "Beginner (Q1 - Q8)":
            filtered_questions = [q for q in SQL_QUESTIONS if q["level"] == "Beginner"]
        elif difficulty_filter == "Intermediate (Q9 - Q16)":
            filtered_questions = [q for q in SQL_QUESTIONS if q["level"] == "Intermediate"]
        elif difficulty_filter == "Advanced (Q17 - Q25)":
            filtered_questions = [q for q in SQL_QUESTIONS if q["level"] == "Advanced"]

        q_options = [f"Q{q['id']}: {q['title']} ({q['level']})" for q in filtered_questions]
        selected_q_idx = st.selectbox("Choose Question", range(len(filtered_questions)), format_func=lambda i: q_options[i])
        current_q = filtered_questions[selected_q_idx]

    with c2:
        # Question Header Box
        level_colors = {"Beginner": "#3FB950", "Intermediate": "#E8A33D", "Advanced": "#E879F9"}
        tag_color = level_colors.get(current_q["level"], "#14B8A6")

        st.markdown(f"""
            <div style="background:#131C2E; border:1px solid #1F2C42; border-radius:12px; padding:18px; margin-bottom:16px;">
                <div style="display:flex; justify-content:space-between; align-items:center; margin-bottom:8px;">
                    <span style="font-size:18px; font-weight:800; color:#14B8A6;">Question {current_q['id']}: {current_q['title']}</span>
                    <span style="background:{tag_color}22; color:{tag_color}; border:1px solid {tag_color}55; padding:3px 10px; border-radius:12px; font-size:11px; font-weight:700;">{current_q['level']}</span>
                </div>
                <div style="color:#F3F4F6; font-size:14px; margin-bottom:10px;"><b>🎯 Business Problem:</b><br>{current_q['problem']}</div>
                <div style="display:grid; grid-template-columns: 1fr 1fr; gap:12px; font-size:12px; color:#8A97AB; border-top:1px solid #1F2C42; padding-top:8px;">
                    <div><b>🧠 SQL Concepts:</b> {current_q['concepts']}</div>
                    <div><b>🗄️ Tables:</b> {current_q['tables']}</div>
                </div>
            </div>
        """, unsafe_allow_html=True)

        st.markdown("#### SQL Query Code")
        st.code(current_q["query"], language="sql")

        col_exec, col_dl = st.columns([1, 1])
        run_clicked = col_exec.button("▶️ Execute Query Live", use_container_width=True)

        # Automatic execution on load or click
        res = AnalyticsService.execute_question(current_q["id"])
        df_result = res["data"]

        st.markdown(f"""
            <div style="display:flex; justify-content:space-between; align-items:center; margin:12px 0 8px 0; font-size:12px; color:#8A97AB;">
                <span>⚡ <b>Execution Time:</b> <span style="color:#3FB950;">{res['execution_time_ms']} ms</span></span>
                <span>📊 <b>Rows Returned:</b> <span style="color:#14B8A6;">{res['rows']}</span></span>
            </div>
        """, unsafe_allow_html=True)

        # Result Dataframe
        st.dataframe(df_result, use_container_width=True, hide_index=True)

        # CSV Download Button
        csv_data = df_result.to_csv(index=False).encode('utf-8')
        col_dl.download_button(
            label="📥 Download CSV Results",
            data=csv_data,
            file_name=f"cricbuzz_q{current_q['id']}_results.csv",
            mime="text/csv",
            use_container_width=True
        )

        # Visual Chart for the question
        chart = plot_question_chart(current_q, df_result)
        if chart:
            st.markdown("#### 📊 Interactive Visualization")
            st.plotly_chart(chart, use_container_width=True)

# -------------------------------------------------------------
# TAB 2: CUSTOM SQL PLAYGROUND
# -------------------------------------------------------------
with tab_playground:
    st.subheader("💻 Interactive SQL Runner")
    st.markdown("Write any read-only `SELECT` query against the live database tables: `players`, `matches`, `player_format_stats`, `player_match_performances`, `partnerships`, `teams`, `venues`, `series`.")

    col_schema, col_editor = st.columns([1, 2.5])
    
    with col_schema:
        st.markdown("#### 🗄️ Schema Explorer")
        tables = get_table_names()
        selected_tbl = st.selectbox("Inspect Table Schema", tables)
        schema_df = get_table_schema(selected_tbl)
        st.dataframe(schema_df[["name", "type", "notnull"]], use_container_width=True, hide_index=True)

    with col_editor:
        default_query = "SELECT full_name, country, playing_role FROM players WHERE country = 'Australia' LIMIT 10;"
        custom_sql = st.text_area("SQL Editor", value=default_query, height=140)

        if st.button("🚀 Run Custom Query", use_container_width=True):
            try:
                custom_res = AnalyticsService.execute_custom_sql(custom_sql)
                cdf = custom_res["data"]
                st.success(f"Executed successfully in {custom_res['execution_time_ms']} ms! ({custom_res['rows']} rows returned)")
                st.dataframe(cdf, use_container_width=True, hide_index=True)

                c_csv = cdf.to_csv(index=False).encode('utf-8')
                st.download_button(
                    label="📥 Download Query Result CSV",
                    data=c_csv,
                    file_name="custom_query_result.csv",
                    mime="text/csv"
                )
            except Exception as e:
                st.error(f"SQL Error: {str(e)}")

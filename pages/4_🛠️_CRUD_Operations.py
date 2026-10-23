"""
Cricbuzz LiveStats - Administrative CRUD Operations Page
Comprehensive form-based UI for Creating, Reading, Updating, and Deleting Players & Matches.
"""

import streamlit as st
import pandas as pd
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

import config
from utils.helpers import load_custom_css
from services.crud_service import CRUDService

st.set_page_config(page_title="CRUD Operations | Cricbuzz LiveStats", page_icon="🛠️", layout="wide")
load_custom_css()

st.markdown("""
    <div class="app-header-badge">🛠️ Database Management</div>
    <h2 style="font-weight:800; margin-bottom:4px;">Relational CRUD Operations</h2>
    <p style="color:#94A3B8; font-size:14px;">Form-based Create, Read, Update, and Delete engine for players, matches, and squad profiles.</p>
""", unsafe_allow_html=True)

tab_players, tab_matches = st.tabs(["👤 Manage Players", "🏏 Manage Matches"])

# -------------------------------------------------------------
# TAB 1: PLAYER CRUD
# -------------------------------------------------------------
with tab_players:
    st.markdown("### 📋 Player Directory & Operations")

    col_search, col_country = st.columns([2, 1])
    search_q = col_search.text_input("🔍 Search Players by Name", "")
    country_choice = col_country.selectbox("Filter Country", ["All", "India", "Australia", "England", "South Africa", "Pakistan", "New Zealand", "Afghanistan", "Bangladesh", "West Indies", "Sri Lanka"])

    players_df = CRUDService.get_all_players(search_query=search_q, country_filter=country_choice)
    st.dataframe(players_df, use_container_width=True, hide_index=True)

    st.markdown("---")

    p_action = st.radio("Choose Player Operation", ["➕ Add New Player", "✏️ Edit Existing Player", "🗑️ Delete Player"], horizontal=True)

    # 1. ADD NEW PLAYER
    if p_action == "➕ Add New Player":
        st.markdown("#### ➕ Create New Player Profile")
        with st.form("add_player_form", clear_on_submit=True):
            f_col1, f_col2 = st.columns(2)
            with f_col1:
                new_name = st.text_input("Full Name *", placeholder="e.g. Yashasvi Jaiswal")
                new_country = st.selectbox("National Team *", ["India", "Australia", "England", "South Africa", "Pakistan", "New Zealand", "West Indies", "Sri Lanka", "Afghanistan", "Bangladesh"])
                new_role = st.selectbox("Playing Role *", ["Batsman", "Bowler", "All-rounder", "Wicket-keeper"])
            with f_col2:
                new_bat = st.selectbox("Batting Style *", ["Right-hand bat", "Left-hand bat"])
                new_bowl = st.selectbox("Bowling Style *", ["Right-arm fast", "Right-arm fast-medium", "Left-arm fast", "Slow left-arm orthodox", "Right-arm offbreak", "Right-arm legbreak", "None"])
                new_dob = st.date_input("Date of Birth", value=pd.to_datetime("2000-01-01"))

            submitted = st.form_submit_button("💾 Save Player to Database")
            if submitted:
                if not new_name.strip():
                    st.error("Player name cannot be empty.")
                else:
                    try:
                        pid = CRUDService.create_player(
                            full_name=new_name,
                            country=new_country,
                            playing_role=new_role,
                            batting_style=new_bat,
                            bowling_style=new_bowl,
                            dob=str(new_dob)
                        )
                        st.success(f"Player '{new_name}' created successfully with Player ID: {pid}!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error creating player: {e}")

    # 2. EDIT PLAYER
    elif p_action == "✏️ Edit Existing Player":
        st.markdown("#### ✏️ Update Player Attributes")
        player_list = players_df.to_dict(orient="records")
        if not player_list:
            st.warning("No players found to edit.")
        else:
            p_opts = [f"ID {p['player_id']} - {p['full_name']} ({p['country']})" for p in player_list]
            selected_edit_idx = st.selectbox("Select Player to Edit", range(len(player_list)), format_func=lambda i: p_opts[i])
            chosen_player = player_list[selected_edit_idx]

            with st.form("edit_player_form"):
                e_col1, e_col2 = st.columns(2)
                with e_col1:
                    edit_name = st.text_input("Full Name", value=chosen_player["full_name"])
                    countries = ["India", "Australia", "England", "South Africa", "Pakistan", "New Zealand", "West Indies", "Sri Lanka", "Afghanistan", "Bangladesh"]
                    c_idx = countries.index(chosen_player["country"]) if chosen_player["country"] in countries else 0
                    edit_country = st.selectbox("Country", countries, index=c_idx)
                    
                    roles = ["Batsman", "Bowler", "All-rounder", "Wicket-keeper"]
                    r_idx = roles.index(chosen_player["playing_role"]) if chosen_player["playing_role"] in roles else 0
                    edit_role = st.selectbox("Role", roles, index=r_idx)

                with e_col2:
                    bats = ["Right-hand bat", "Left-hand bat"]
                    b_idx = bats.index(chosen_player["batting_style"]) if chosen_player["batting_style"] in bats else 0
                    edit_bat = st.selectbox("Batting Style", bats, index=b_idx)

                    bowls = ["Right-arm fast", "Right-arm fast-medium", "Left-arm fast", "Slow left-arm orthodox", "Right-arm offbreak", "Right-arm legbreak", "None"]
                    bw_idx = bowls.index(chosen_player["bowling_style"]) if chosen_player["bowling_style"] in bowls else 0
                    edit_bowl = st.selectbox("Bowling Style", bowls, index=bw_idx)

                    edit_active = st.checkbox("Is Active Squad Member", value=bool(chosen_player["is_active"]))

                update_btn = st.form_submit_button("🔄 Update Player Record")
                if update_btn:
                    try:
                        success = CRUDService.update_player(
                            player_id=chosen_player["player_id"],
                            full_name=edit_name,
                            country=edit_country,
                            playing_role=edit_role,
                            batting_style=edit_bat,
                            bowling_style=edit_bowl,
                            dob=str(chosen_player["dob"]),
                            is_active=1 if edit_active else 0
                        )
                        if success:
                            st.success(f"Player ID {chosen_player['player_id']} successfully updated!")
                            st.rerun()
                    except Exception as e:
                        st.error(f"Failed to update player: {e}")

    # 3. DELETE PLAYER
    else:
        st.markdown("#### 🗑️ Remove Player from Database")
        player_list = players_df.to_dict(orient="records")
        if not player_list:
            st.warning("No players available for deletion.")
        else:
            p_opts = [f"ID {p['player_id']} - {p['full_name']} ({p['country']})" for p in player_list]
            del_idx = st.selectbox("Select Player to Delete", range(len(player_list)), format_func=lambda i: p_opts[i], key="del_sel")
            target_del = player_list[del_idx]

            st.warning(f"⚠️ Action Warning: Deleting **{target_del['full_name']}** will cascade and permanently remove their career format stats, match performances, and partnership records.")
            
            confirm = st.checkbox(f"I confirm permanent deletion of {target_del['full_name']} (ID: {target_del['player_id']})")
            if st.button("🚨 Delete Player Permanently", disabled=not confirm):
                try:
                    ok = CRUDService.delete_player(target_del["player_id"])
                    if ok:
                        st.success(f"Player {target_del['full_name']} successfully deleted.")
                        st.rerun()
                except Exception as e:
                    st.error(f"Deletion failed: {e}")

# -------------------------------------------------------------
# TAB 2: MATCH CRUD
# -------------------------------------------------------------
with tab_matches:
    st.markdown("### 🏏 Match Records & Scheduler")

    matches_df = CRUDService.get_all_matches(limit=50)
    st.dataframe(matches_df, use_container_width=True, hide_index=True)

    st.markdown("---")
    m_action = st.radio("Choose Match Operation", ["➕ Schedule / Log New Match", "🗑️ Delete Match"], horizontal=True)

    teams = CRUDService.get_teams_dropdown()
    venues = CRUDService.get_venues_dropdown()
    series_list = CRUDService.get_series_dropdown()

    team_names = [t["team_name"] for t in teams]
    venue_names = [f"{v['venue_name']} ({v['city']})" for v in venues]
    series_names = [s["series_name"] for s in series_list]

    if m_action == "➕ Schedule / Log New Match":
        st.markdown("#### ➕ Add New Match Result")
        with st.form("add_match_form", clear_on_submit=True):
            mc1, mc2 = st.columns(2)
            with mc1:
                m_desc = st.text_input("Match Description *", placeholder="e.g. India vs Australia 1st ODI 2024")
                s_idx = st.selectbox("Linked Series", range(len(series_list)), format_func=lambda i: series_names[i])
                t1_idx = st.selectbox("Team 1", range(len(teams)), index=0, format_func=lambda i: team_names[i])
                t2_idx = st.selectbox("Team 2", range(len(teams)), index=1, format_func=lambda i: team_names[i])
                v_idx = st.selectbox("Venue", range(len(venues)), format_func=lambda i: venue_names[i])

            with mc2:
                m_fmt = st.selectbox("Match Format", ["T20I", "ODI", "Test"])
                m_dt = st.date_input("Match Date", value=pd.to_datetime("today"))
                toss_w_idx = st.selectbox("Toss Winner", range(len(teams)), format_func=lambda i: team_names[i])
                toss_dec = st.selectbox("Toss Decision", ["Bat", "Bowl"])
                winner_idx = st.selectbox("Match Winner", range(len(teams)), format_func=lambda i: team_names[i])
                v_margin = st.number_input("Victory Margin", min_value=1, max_value=500, value=25)
                v_type = st.selectbox("Victory Type", ["runs", "wickets"])

            m_submit = st.form_submit_button("💾 Save Match to Database")
            if m_submit:
                if not m_desc.strip():
                    st.error("Match description is required.")
                elif t1_idx == t2_idx:
                    st.error("Team 1 and Team 2 cannot be the same team.")
                else:
                    try:
                        mid = CRUDService.create_match(
                            series_id=series_list[s_idx]["series_id"],
                            description=m_desc,
                            team1_id=teams[t1_idx]["team_id"],
                            team2_id=teams[t2_idx]["team_id"],
                            venue_id=venues[v_idx]["venue_id"],
                            match_date=str(m_dt),
                            match_format=m_fmt,
                            toss_winner_id=teams[toss_w_idx]["team_id"],
                            toss_decision=toss_dec,
                            winning_team_id=teams[winner_idx]["team_id"],
                            victory_margin=int(v_margin),
                            victory_type=v_type
                        )
                        st.success(f"Match successfully logged with Match ID: {mid}!")
                        st.rerun()
                    except Exception as e:
                        st.error(f"Error logging match: {e}")

    else:
        st.markdown("#### 🗑️ Delete Match Record")
        m_records = matches_df.to_dict(orient="records")
        if not m_records:
            st.warning("No matches available to delete.")
        else:
            m_opts = [f"ID {m['match_id']}: {m['match_description']} ({m['match_date']})" for m in m_records]
            del_m_idx = st.selectbox("Select Match to Delete", range(len(m_records)), format_func=lambda i: m_opts[i])
            m_target = m_records[del_m_idx]

            st.warning(f"⚠️ Are you sure you want to delete match **{m_target['match_description']}**?")
            conf_m = st.checkbox(f"Confirm deletion of Match ID {m_target['match_id']}")
            if st.button("🚨 Delete Match", disabled=not conf_m):
                try:
                    ok = CRUDService.delete_match(m_target["match_id"])
                    if ok:
                        st.success("Match deleted successfully.")
                        st.rerun()
                except Exception as e:
                    st.error(f"Failed to delete match: {e}")

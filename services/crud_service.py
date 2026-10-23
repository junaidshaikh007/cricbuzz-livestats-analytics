"""
CRUD Service Module
Handles Create, Read, Update, and Delete operations on players, matches,
venues, and career stats with validation and transaction safety.
"""

import pandas as pd
from typing import Dict, Any, Optional, List
from database.db_connection import execute_query, execute_statement


class CRUDService:
    """Provides validated business logic for managing database records."""

    # -------------------------------------------------------------
    # PLAYER CRUD
    # -------------------------------------------------------------
    @staticmethod
    def get_all_players(search_query: str = "", country_filter: str = "All") -> pd.DataFrame:
        """Retrieves list of players with optional search and country filter."""
        sql = """
            SELECT 
                player_id,
                full_name,
                country,
                playing_role,
                batting_style,
                bowling_style,
                dob,
                is_active
            FROM players
            WHERE 1=1
        """
        params = []
        if search_query.strip():
            sql += " AND full_name LIKE ?"
            params.append(f"%{search_query.strip()}%")
        if country_filter != "All":
            sql += " AND country = ?"
            params.append(country_filter)
        
        sql += " ORDER BY player_id DESC"
        return execute_query(sql, tuple(params) if params else None)

    @staticmethod
    def get_player_by_id(player_id: int) -> Optional[Dict[str, Any]]:
        """Fetches full player details and stats by ID."""
        sql = "SELECT * FROM players WHERE player_id = ?"
        df = execute_query(sql, (player_id,))
        if df.empty:
            return None
        return df.iloc[0].to_dict()

    @staticmethod
    def create_player(
        full_name: str,
        country: str,
        playing_role: str,
        batting_style: str,
        bowling_style: str,
        dob: str = "1995-01-01"
    ) -> int:
        """Inserts a new player and initializes empty career records."""
        if not full_name.strip():
            raise ValueError("Player full name is required.")

        sql = """
            INSERT INTO players (full_name, country, playing_role, batting_style, bowling_style, dob, is_active)
            VALUES (?, ?, ?, ?, ?, ?, 1)
        """
        player_id = execute_statement(sql, (
            full_name.strip(), country.strip(), playing_role, batting_style, bowling_style, dob
        ))

        # Initialize default format records
        for fmt in ["Test", "ODI", "T20I"]:
            execute_statement("""
                INSERT OR IGNORE INTO player_format_stats (player_id, format, matches, runs, wickets)
                VALUES (?, ?, 0, 0, 0)
            """, (player_id, fmt))

        return player_id

    @staticmethod
    def update_player(
        player_id: int,
        full_name: str,
        country: str,
        playing_role: str,
        batting_style: str,
        bowling_style: str,
        dob: str,
        is_active: int
    ) -> bool:
        """Updates an existing player's profile."""
        sql = """
            UPDATE players
            SET full_name = ?, country = ?, playing_role = ?, batting_style = ?, bowling_style = ?, dob = ?, is_active = ?
            WHERE player_id = ?
        """
        rows = execute_statement(sql, (
            full_name.strip(), country, playing_role, batting_style, bowling_style, dob, is_active, player_id
        ))
        return rows > 0

    @staticmethod
    def delete_player(player_id: int) -> bool:
        """Deletes a player and cascades to format stats and performances."""
        # Clean up related records
        execute_statement("DELETE FROM player_format_stats WHERE player_id = ?", (player_id,))
        execute_statement("DELETE FROM player_match_performances WHERE player_id = ?", (player_id,))
        execute_statement("DELETE FROM partnerships WHERE player1_id = ? OR player2_id = ?", (player_id, player_id))
        rows = execute_statement("DELETE FROM players WHERE player_id = ?", (player_id,))
        return rows > 0

    # -------------------------------------------------------------
    # MATCH CRUD
    # -------------------------------------------------------------
    @staticmethod
    def get_all_matches(limit: int = 50) -> pd.DataFrame:
        """Retrieves matches joined with team and venue details."""
        sql = """
            SELECT 
                m.match_id,
                m.match_description,
                t1.team_name AS team_1,
                t2.team_name AS team_2,
                v.venue_name,
                m.format,
                m.match_date,
                COALESCE(tw.team_name, 'No Result') AS winner,
                m.victory_margin || ' ' || m.victory_type AS margin,
                m.status
            FROM matches m
            JOIN teams t1 ON m.team1_id = t1.team_id
            JOIN teams t2 ON m.team2_id = t2.team_id
            JOIN venues v ON m.venue_id = v.venue_id
            LEFT JOIN teams tw ON m.winning_team_id = tw.team_id
            ORDER BY m.match_date DESC
            LIMIT ?
        """
        return execute_query(sql, (limit,))

    @staticmethod
    def create_match(
        series_id: int,
        description: str,
        team1_id: int,
        team2_id: int,
        venue_id: int,
        match_date: str,
        match_format: str,
        toss_winner_id: int,
        toss_decision: str,
        winning_team_id: int,
        victory_margin: int,
        victory_type: str
    ) -> int:
        """Inserts a new match record."""
        sql = """
            INSERT INTO matches 
            (series_id, match_description, team1_id, team2_id, venue_id, match_date, format, toss_winner_id, toss_decision, winning_team_id, victory_margin, victory_type, status)
            VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, 'Completed')
        """
        return execute_statement(sql, (
            series_id, description, team1_id, team2_id, venue_id, match_date, match_format,
            toss_winner_id, toss_decision, winning_team_id, victory_margin, victory_type
        ))

    @staticmethod
    def delete_match(match_id: int) -> bool:
        """Deletes a match and its linked performances."""
        execute_statement("DELETE FROM player_match_performances WHERE match_id = ?", (match_id,))
        execute_statement("DELETE FROM partnerships WHERE match_id = ?", (match_id,))
        rows = execute_statement("DELETE FROM matches WHERE match_id = ?", (match_id,))
        return rows > 0

    # -------------------------------------------------------------
    # LOOKUP HELPERS
    # -------------------------------------------------------------
    @staticmethod
    def get_teams_dropdown() -> List[Dict[str, Any]]:
        """Returns list of teams for select boxes."""
        df = execute_query("SELECT team_id, team_name FROM teams ORDER BY team_name ASC")
        return df.to_dict(orient="records")

    @staticmethod
    def get_venues_dropdown() -> List[Dict[str, Any]]:
        """Returns list of venues for select boxes."""
        df = execute_query("SELECT venue_id, venue_name, city FROM venues ORDER BY venue_name ASC")
        return df.to_dict(orient="records")

    @staticmethod
    def get_series_dropdown() -> List[Dict[str, Any]]:
        """Returns list of series for select boxes."""
        df = execute_query("SELECT series_id, series_name FROM series ORDER BY series_name ASC")
        return df.to_dict(orient="records")

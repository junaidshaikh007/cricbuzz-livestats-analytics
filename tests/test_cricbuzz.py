"""
Automated Test Suite for Cricbuzz LiveStats
Covers Database integrity, CRUD functionality, 25 SQL Queries, and API client fallback.
"""

import unittest
import sqlite3
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))

import config
from database.db_connection import get_connection, execute_query, execute_statement, get_database_stats
from services.crud_service import CRUDService
from services.analytics_service import AnalyticsService, SQL_QUESTIONS
from api.cricbuzz_api import CricbuzzAPIClient


class TestCricbuzzLiveStats(unittest.TestCase):

    def test_database_connection(self):
        """Verifies database connection can be established."""
        conn = get_connection()
        self.assertIsNotNone(conn)
        conn.close()

    def test_database_seeded_counts(self):
        """Ensures key tables have loaded records."""
        stats = get_database_stats()
        self.assertGreaterEqual(stats.get("teams", 0), 10)
        self.assertGreaterEqual(stats.get("players", 0), 40)
        self.assertGreaterEqual(stats.get("venues", 0), 10)
        self.assertGreaterEqual(stats.get("matches", 0), 40)

    def test_player_crud_cycle(self):
        """Tests complete Create, Read, Update, Delete lifecycle for a player."""
        # Create
        test_name = "Unit Test Player"
        pid = CRUDService.create_player(
            full_name=test_name,
            country="India",
            playing_role="Batsman",
            batting_style="Right-hand bat",
            bowling_style="None",
            dob="2002-05-15"
        )
        self.assertIsNotNone(pid)
        self.assertGreater(pid, 0)

        # Read
        p = CRUDService.get_player_by_id(pid)
        self.assertIsNotNone(p)
        self.assertEqual(p["full_name"], test_name)

        # Update
        updated = CRUDService.update_player(
            player_id=pid,
            full_name="Updated Test Player",
            country="India",
            playing_role="All-rounder",
            batting_style="Left-hand bat",
            bowling_style="Right-arm fast",
            dob="2002-05-15",
            is_active=1
        )
        self.assertTrue(updated)
        p_up = CRUDService.get_player_by_id(pid)
        self.assertEqual(p_up["full_name"], "Updated Test Player")
        self.assertEqual(p_up["playing_role"], "All-rounder")

        # Delete
        deleted = CRUDService.delete_player(pid)
        self.assertTrue(deleted)
        p_del = CRUDService.get_player_by_id(pid)
        self.assertIsNone(p_del)

    def test_all_25_sql_queries(self):
        """Verifies all 25 guided SQL practice queries execute and return rows."""
        self.assertEqual(len(SQL_QUESTIONS), 25)
        for q in SQL_QUESTIONS:
            res = AnalyticsService.execute_question(q["id"])
            self.assertIn("data", res)
            self.assertGreater(res["rows"], 0, f"Query ID {q['id']} ({q['title']}) returned 0 rows!")

    def test_api_client_mock_fallback(self):
        """Verifies API client returns mock data in offline mode."""
        client = CricbuzzAPIClient()
        matches = client.fetch_live_matches()
        self.assertIsInstance(matches, list)
        self.assertGreater(len(matches), 0)
        self.assertIn("team1", matches[0])
        self.assertIn("team2", matches[0])


if __name__ == "__main__":
    unittest.main()

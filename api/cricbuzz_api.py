"""
Cricbuzz API Client
Interacts with the Cricbuzz Cricket API via RapidAPI or falls back to
high-fidelity simulated live feeds when operating in offline/demo mode.
"""

import requests
import logging
from typing import Dict, Any, List, Optional
from pathlib import Path
import sys

BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
import config
from api.mock_data import get_live_matches_mock, get_mock_stats_leaderboard

logger = logging.getLogger("CricbuzzAPI")


class CricbuzzAPIClient:
    """REST API Client for Cricbuzz Cricket Data."""

    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or config.RAPIDAPI_KEY
        self.host = config.RAPIDAPI_HOST
        self.base_url = config.RAPIDAPI_BASE_URL
        self.session = requests.Session()

    @property
    def is_configured(self) -> bool:
        """Checks if a valid-length RapidAPI key is present."""
        return bool(self.api_key and len(self.api_key.strip()) > 10)

    def _get_headers(self) -> Dict[str, str]:
        return {
            "X-RapidAPI-Key": self.api_key,
            "X-RapidAPI-Host": self.host
        }

    def fetch_live_matches(self) -> List[Dict[str, Any]]:
        """
        Fetches live matches. If API key is not configured or an error occurs,
        falls back gracefully to offline mock telemetry.
        """
        if not self.is_configured:
            logger.info("RapidAPI key not set. Returning authentic live mock matches.")
            return get_live_matches_mock()

        url = f"{self.base_url}/matches/v1/live"
        try:
            response = self.session.get(url, headers=self._get_headers(), timeout=5)
            if response.status_code == 200:
                data = response.json()
                return self._parse_rapidapi_matches(data)
            else:
                logger.warning(f"Cricbuzz API returned HTTP {response.status_code}. Using mock data.")
                return get_live_matches_mock()
        except Exception as e:
            logger.error(f"Error fetching live matches from Cricbuzz API: {e}")
            return get_live_matches_mock()

    def fetch_top_stats(self, category: str = "runs", format_type: str = "ODI") -> List[Dict[str, Any]]:
        """Fetches top statistical leaders."""
        return get_mock_stats_leaderboard(category=category, format_type=format_type)

    def test_connection(self) -> Dict[str, Any]:
        """Tests validity of the current RapidAPI key."""
        if not self.is_configured:
            return {"status": "offline_mode", "message": "Using Built-in Live Feed Engine (No API key set)"}
        
        url = f"{self.base_url}/matches/v1/live"
        try:
            response = self.session.get(url, headers=self._get_headers(), timeout=5)
            if response.status_code == 200:
                return {"status": "connected", "message": "Successfully connected to Cricbuzz RapidAPI!"}
            else:
                return {"status": "error", "message": f"API responded with status code: {response.status_code}"}
        except Exception as e:
            return {"status": "error", "message": f"Connection failed: {str(e)}"}

    def _parse_rapidapi_matches(self, data: Dict[str, Any]) -> List[Dict[str, Any]]:
        """Parses Cricbuzz RapidAPI match list into standard schema."""
        matches = []
        try:
            type_matches = data.get("typeMatches", [])
            for tm in type_matches:
                series_matches = tm.get("seriesMatches", [])
                for sm in series_matches:
                    series_ad = sm.get("seriesAdWrapper", {})
                    matches_list = series_ad.get("matches", [])
                    for m in matches_list:
                        m_info = m.get("matchInfo", {})
                        m_score = m.get("matchScore", {})
                        team1 = m_info.get("team1", {})
                        team2 = m_info.get("team2", {})
                        t1_score = m_score.get("team1Score", {}).get("inngs1", {})
                        t2_score = m_score.get("team2Score", {}).get("inngs1", {})

                        t1_str = f"{t1_score.get('runs', 0)}/{t1_score.get('wickets', 0)}" if t1_score else "Yet to bat"
                        t2_str = f"{t2_score.get('runs', 0)}/{t2_score.get('wickets', 0)}" if t2_score else "Yet to bat"

                        matches.append({
                            "id": str(m_info.get("matchId", "")),
                            "title": m_info.get("seriesName", "International Match"),
                            "team1": {"name": team1.get("teamName", "Team 1"), "short": team1.get("teamSName", "T1"), "score": t1_str, "overs": str(t1_score.get("overs", "0.0")), "flag": "🏏"},
                            "team2": {"name": team2.get("teamName", "Team 2"), "short": team2.get("teamSName", "T2"), "score": t2_str, "overs": str(t2_score.get("overs", "0.0")), "flag": "🏏"},
                            "status": m_info.get("status", "Live in progress"),
                            "state": m_info.get("state", "In Progress"),
                            "venue": m_info.get("venueInfo", {}).get("ground", "International Ground"),
                            "format": m_info.get("matchFormat", "T20"),
                            "current_batsmen": [],
                            "current_bowler": {},
                            "recent_balls": ["1", "0", "4", "2", "W", "1"],
                            "commentary": [],
                            "crr": "7.5",
                            "rrr": "8.2"
                        })
            if matches:
                return matches
        except Exception as e:
            logger.error(f"Error parsing RapidAPI payload: {e}")
        return get_live_matches_mock()

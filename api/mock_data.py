"""
Cricbuzz Mock Data Module
Provides realistic live cricket match telemetry, scorecards, and commentary feeds.
Ensures the dashboard works out of the box with zero external API dependencies.
"""

import random
import datetime

LIVE_MATCHES_FEED = [
    {
        "id": "live-101",
        "title": "ICC Men's T20 World Cup - Final",
        "team1": {"name": "India", "short": "IND", "score": "176/7", "overs": "20.0", "flag": "🇮🇳"},
        "team2": {"name": "South Africa", "short": "SA", "score": "169/8", "overs": "20.0", "flag": "🇿🇦"},
        "status": "India won by 7 runs",
        "state": "Completed / Classic Highlights",
        "venue": "Kensington Oval, Bridgetown, Barbados",
        "format": "T20I",
        "toss": "India won the toss and elected to bat",
        "current_batsmen": [
            {"name": "Virat Kohli", "runs": 76, "balls": 59, "fours": 6, "sixes": 2, "sr": 128.8, "on_strike": True},
            {"name": "Axar Patel", "runs": 47, "balls": 31, "fours": 1, "sixes": 4, "sr": 151.6, "on_strike": False}
        ],
        "current_bowler": {"name": "Anrich Nortje", "overs": "4.0", "maidens": 0, "runs": 26, "wickets": 2, "econ": 6.50},
        "recent_balls": ["1", "4", "2", "6", "W", "1"],
        "commentary": [
            {"ball": "19.6", "comm": "Hardik to Rabada, OUT! Caught by Suryakumar Yadav! India are the World Champions!"},
            {"ball": "19.5", "comm": "Hardik to Rabada, 1 run, drilled down to long off."},
            {"ball": "19.4", "comm": "Hardik to Maharaj, 1 run, squeezed through backward point."},
            {"ball": "19.3", "comm": "Hardik to Maharaj, wide called outside off."},
            {"ball": "19.2", "comm": "Hardik to Maharaj, dot ball, beaten by the slower bouncer outside off!"},
            {"ball": "19.1", "comm": "Hardik to Miller, OUT! WHAT A CATCH! Suryakumar Yadav with an unforgettable boundary catch!"}
        ],
        "crr": "8.80",
        "rrr": "-"
    },
    {
        "id": "live-102",
        "title": "Border-Gavaskar Trophy - 1st Test (Day 3)",
        "team1": {"name": "Australia", "short": "AUS", "score": "338 & 214/5", "overs": "62.4", "flag": "🇦🇺"},
        "team2": {"name": "India", "short": "IND", "score": "295", "overs": "91.2", "flag": "🇮🇳"},
        "status": "Australia lead by 257 runs",
        "state": "LIVE",
        "venue": "Optus Stadium, Perth",
        "format": "Test",
        "toss": "Australia won the toss and elected to bat",
        "current_batsmen": [
            {"name": "Travis Head", "runs": 89, "balls": 101, "fours": 11, "sixes": 2, "sr": 88.1, "on_strike": True},
            {"name": "Alex Carey", "runs": 32, "balls": 48, "fours": 4, "sixes": 0, "sr": 66.7, "on_strike": False}
        ],
        "current_bowler": {"name": "Jasprit Bumrah", "overs": "18.4", "maidens": 4, "runs": 52, "wickets": 3, "econ": 2.78},
        "recent_balls": ["0", "4", "0", "1", "0", "0"],
        "commentary": [
            {"ball": "62.4", "comm": "Bumrah to Head, FOUR! Leans into a full delivery and caresses it through extra cover!"},
            {"ball": "62.3", "comm": "Bumrah to Head, no run, solid forward defensive push toward mid-on."},
            {"ball": "62.2", "comm": "Bumrah to Head, no run, beaten on the outside edge! Terrific seam movement."},
            {"ball": "62.1", "comm": "Bumrah to Carey, 1 run, worked off his pads behind square."}
        ],
        "crr": "3.41",
        "rrr": "-"
    },
    {
        "id": "live-103",
        "title": "England vs Pakistan - 2nd ODI",
        "team1": {"name": "Pakistan", "short": "PAK", "score": "285/7", "overs": "50.0", "flag": "🇵🇰"},
        "team2": {"name": "England", "short": "ENG", "score": "218/4", "overs": "38.2", "flag": "🏴󠁧󠁢󠁥󠁮󠁧󠁿"},
        "status": "England need 68 runs in 70 balls",
        "state": "LIVE",
        "venue": "Lord's Cricket Ground, London",
        "format": "ODI",
        "toss": "England won the toss and chose to bowl",
        "current_batsmen": [
            {"name": "Harry Brook", "runs": 64, "balls": 58, "fours": 7, "sixes": 1, "sr": 110.3, "on_strike": True},
            {"name": "Ben Stokes", "runs": 38, "balls": 41, "fours": 3, "sixes": 1, "sr": 92.7, "on_strike": False}
        ],
        "current_bowler": {"name": "Shaheen Afridi", "overs": "8.2", "maidens": 1, "runs": 48, "wickets": 2, "econ": 5.76},
        "recent_balls": ["1", "2", "4", "0", "1", "1"],
        "commentary": [
            {"ball": "38.2", "comm": "Shaheen to Brook, FOUR! Slashed over backward point with ferocious power!"},
            {"ball": "38.1", "comm": "Shaheen to Stokes, 1 run, dabbed gently toward third man."}
        ],
        "crr": "5.68",
        "rrr": "5.82"
    }
]


def get_live_matches_mock():
    """Returns dynamic mock list of live/recent matches."""
    return LIVE_MATCHES_FEED


def get_mock_stats_leaderboard(category="runs", format_type="ODI"):
    """Returns top player stats list."""
    if category == "runs":
        return [
            {"Rank": 1, "Player": "Virat Kohli", "Team": "IND", "Runs": 13906, "Avg": 58.18, "SR": 93.54, "100s": 50},
            {"Rank": 2, "Player": "Rohit Sharma", "Team": "IND", "Runs": 10866, "Avg": 49.16, "SR": 92.44, "100s": 31},
            {"Rank": 3, "Player": "Kane Williamson", "Team": "NZ", "Runs": 6810, "Avg": 48.64, "SR": 81.36, "100s": 13},
            {"Rank": 4, "Player": "Quinton de Kock", "Team": "SA", "Runs": 6770, "Avg": 45.74, "SR": 96.64, "100s": 21},
            {"Rank": 5, "Player": "Joe Root", "Team": "ENG", "Runs": 6522, "Avg": 47.60, "SR": 86.93, "100s": 16},
            {"Rank": 6, "Player": "Babar Azam", "Team": "PAK", "Runs": 5729, "Avg": 56.72, "SR": 88.75, "100s": 19},
            {"Rank": 7, "Player": "Steve Smith", "Team": "AUS", "Runs": 5446, "Avg": 43.91, "SR": 87.33, "100s": 12},
            {"Rank": 8, "Player": "Jos Buttler", "Team": "ENG", "Runs": 5022, "Avg": 39.54, "SR": 117.11, "100s": 11}
        ]
    elif category == "wickets":
        return [
            {"Rank": 1, "Player": "Mitchell Starc", "Team": "AUS", "Wickets": 236, "Avg": 22.96, "Econ": 5.15, "BBI": "6/28"},
            {"Rank": 2, "Player": "Ravindra Jadeja", "Team": "IND", "Wickets": 220, "Avg": 36.07, "Econ": 4.88, "BBI": "5/36"},
            {"Rank": 3, "Player": "Mohammed Shami", "Team": "IND", "Wickets": 195, "Avg": 23.68, "Econ": 5.55, "BBI": "7/57"},
            {"Rank": 4, "Player": "Rashid Khan", "Team": "AFG", "Wickets": 182, "Avg": 18.52, "Econ": 4.16, "BBI": "7/18"},
            {"Rank": 5, "Player": "Jasprit Bumrah", "Team": "IND", "Wickets": 149, "Avg": 23.55, "Econ": 4.59, "BBI": "6/19"},
            {"Rank": 6, "Player": "Pat Cummins", "Team": "AUS", "Wickets": 141, "Avg": 28.16, "Econ": 5.25, "BBI": "5/70"}
        ]
    else:
        return [
            {"Rank": 1, "Player": "Rohit Sharma", "Score": "264", "Opposition": "Sri Lanka", "Venue": "Eden Gardens", "Year": 2014},
            {"Rank": 2, "Player": "Martin Guptill", "Score": "237*", "Opposition": "West Indies", "Venue": "Wellington", "Year": 2015},
            {"Rank": 3, "Player": "Virender Sehwag", "Score": "219", "Opposition": "West Indies", "Venue": "Indore", "Year": 2011},
            {"Rank": 4, "Player": "Chris Gayle", "Score": "215", "Opposition": "Zimbabwe", "Venue": "Canberra", "Year": 2015},
            {"Rank": 5, "Player": "Fakhar Zaman", "Score": "210*", "Opposition": "Zimbabwe", "Venue": "Bulawayo", "Year": 2018},
            {"Rank": 6, "Player": "Glenn Maxwell", "Score": "201*", "Opposition": "Afghanistan", "Venue": "Wankhede", "Year": 2023}
        ]

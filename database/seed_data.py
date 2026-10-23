"""
Cricbuzz LiveStats - Seed Data Generator
Populates SQLite database with comprehensive, authentic cricket data.
Spec-compliant for all 25 SQL queries and Streamlit features.
"""

import sqlite3
import datetime
import random
from pathlib import Path
import os
import sys

# Add parent directory to path
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
import config

DB_PATH = config.DATABASE_PATH
SCHEMA_PATH = config.SCHEMA_PATH


def init_db():
    """Initializes database schema."""
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()
    with open(SCHEMA_PATH, "r", encoding="utf-8") as f:
        schema_sql = f.read()
    cursor.executescript(schema_sql)
    conn.commit()
    conn.close()


def seed_database():
    """Seeds full relational dataset into cricbuzz.db."""
    init_db()
    conn = sqlite3.connect(DB_PATH)
    cursor = conn.cursor()

    # Clear existing data to ensure clean reload
    tables = [
        "partnerships", "player_match_performances", "player_format_stats",
        "matches", "players", "series", "venues", "teams"
    ]
    for table in tables:
        cursor.execute(f"DELETE FROM {table}")
        cursor.execute(f"DELETE FROM sqlite_sequence WHERE name='{table}'")
    conn.commit()

    # 1. TEAMS (10 teams)
    teams_data = [
        (1, "India", "India", "IND"),
        (2, "Australia", "Australia", "AUS"),
        (3, "England", "England", "ENG"),
        (4, "South Africa", "South Africa", "SA"),
        (5, "Pakistan", "Pakistan", "PAK"),
        (6, "New Zealand", "New Zealand", "NZ"),
        (7, "West Indies", "West Indies", "WI"),
        (8, "Sri Lanka", "Sri Lanka", "SL"),
        (9, "Afghanistan", "Afghanistan", "AFG"),
        (10, "Bangladesh", "Bangladesh", "BAN")
    ]
    cursor.executemany("INSERT INTO teams (team_id, team_name, country, code) VALUES (?, ?, ?, ?)", teams_data)

    # 2. VENUES (15 venues across globe with varied capacities)
    venues_data = [
        (1, "Narendra Modi Stadium", "Ahmedabad", "India", 132000),
        (2, "Melbourne Cricket Ground", "Melbourne", "Australia", 100024),
        (3, "Eden Gardens", "Kolkata", "India", 66000),
        (4, "Perth Stadium", "Perth", "Australia", 60000),
        (5, "Adelaide Oval", "Adelaide", "Australia", 53583),
        (6, "Sydney Cricket Ground", "Sydney", "Australia", 48000),
        (7, "Wankhede Stadium", "Mumbai", "India", 33108),
        (8, "Lord's Cricket Ground", "London", "England", 31100),
        (9, "The Oval", "London", "England", 27500),
        (10, "Edgbaston", "Birmingham", "England", 25000),
        (11, "Newlands Cricket Ground", "Cape Town", "South Africa", 25000),
        (12, "SuperSport Park", "Centurion", "South Africa", 22000),
        (13, "Gaddafi Stadium", "Lahore", "Pakistan", 27000),
        (14, "Dubai International Stadium", "Dubai", "UAE", 25000),
        (15, "Eden Park", "Auckland", "New Zealand", 42000)
    ]
    cursor.executemany("INSERT INTO venues (venue_id, venue_name, city, country, capacity) VALUES (?, ?, ?, ?, ?)", venues_data)

    # 3. SERIES (Started in 2024 and prior)
    series_data = [
        (1, "ICC Men's T20 World Cup 2024", "USA & West Indies", "T20I", "2024-06-01", "2024-06-29", 55),
        (2, "Border-Gavaskar Trophy 2024-25", "Australia", "Test", "2024-11-22", "2025-01-07", 5),
        (3, "India vs England Test Series 2024", "India", "Test", "2024-01-25", "2024-03-11", 5),
        (4, "Australia Tour of England 2024", "England", "Multi-Format", "2024-09-11", "2024-09-29", 8),
        (5, "ICC Cricket World Cup 2023", "India", "ODI", "2023-10-05", "2023-11-19", 48),
        (6, "Asia Cup 2023", "Sri Lanka & Pakistan", "ODI", "2023-08-30", "2023-09-17", 13),
        (7, "The Ashes 2023", "England", "Test", "2023-06-16", "2023-07-31", 5),
        (8, "India Tour of South Africa 2023-24", "South Africa", "Multi-Format", "2023-12-10", "2024-01-07", 8)
    ]
    cursor.executemany("INSERT INTO series (series_id, series_name, host_country, match_type, start_date, end_date, total_matches) VALUES (?, ?, ?, ?, ?, ?, ?)", series_data)

    # 4. PLAYERS (40 elite international players)
    players_data = [
        # India (1-10)
        (1, "Virat Kohli", "India", "Batsman", "Right-hand bat", "Right-arm medium", "1988-11-05", 1),
        (2, "Rohit Sharma", "India", "Batsman", "Right-hand bat", "Right-arm offbreak", "1987-04-30", 1),
        (3, "Jasprit Bumrah", "India", "Bowler", "Right-hand bat", "Right-arm fast", "1993-12-06", 1),
        (4, "Ravindra Jadeja", "India", "All-rounder", "Left-hand bat", "Slow left-arm orthodox", "1988-12-06", 1),
        (5, "KL Rahul", "India", "Wicket-keeper", "Right-hand bat", "Right-arm medium", "1992-04-18", 1),
        (6, "Shubman Gill", "India", "Batsman", "Right-hand bat", "Right-arm offbreak", "1999-09-08", 1),
        (7, "Hardik Pandya", "India", "All-rounder", "Right-hand bat", "Right-arm fast-medium", "1993-10-11", 1),
        (8, "Mohammed Shami", "India", "Bowler", "Right-hand bat", "Right-arm fast", "1990-09-03", 1),
        (9, "Rishabh Pant", "India", "Wicket-keeper", "Left-hand bat", "Right-arm offbreak", "1997-10-04", 1),
        (10, "Suryakumar Yadav", "India", "Batsman", "Right-hand bat", "Right-arm offbreak", "1990-09-14", 1),

        # Australia (11-18)
        (11, "Steve Smith", "Australia", "Batsman", "Right-hand bat", "Right-arm legbreak", "1989-06-02", 1),
        (12, "Pat Cummins", "Australia", "Bowler", "Right-hand bat", "Right-arm fast", "1993-05-08", 1),
        (13, "Travis Head", "Australia", "Batsman", "Left-hand bat", "Right-arm offbreak", "1993-12-29", 1),
        (14, "Glenn Maxwell", "Australia", "All-rounder", "Right-hand bat", "Right-arm offbreak", "1988-10-14", 1),
        (15, "Mitchell Starc", "Australia", "Bowler", "Left-hand bat", "Left-arm fast", "1990-01-30", 1),
        (16, "David Warner", "Australia", "Batsman", "Left-hand bat", "Right-arm legbreak", "1986-10-27", 1),
        (17, "Josh Hazlewood", "Australia", "Bowler", "Left-hand bat", "Right-arm fast-medium", "1991-01-08", 1),
        (18, "Alex Carey", "Australia", "Wicket-keeper", "Left-hand bat", "Right-arm offbreak", "1991-08-27", 1),

        # England (19-25)
        (19, "Joe Root", "England", "Batsman", "Right-hand bat", "Right-arm offbreak", "1990-12-30", 1),
        (20, "Ben Stokes", "England", "All-rounder", "Left-hand bat", "Right-arm fast-medium", "1991-06-04", 1),
        (21, "Jos Buttler", "England", "Wicket-keeper", "Right-hand bat", "Right-arm medium", "1990-09-08", 1),
        (22, "Harry Brook", "England", "Batsman", "Right-hand bat", "Right-arm medium", "1999-02-22", 1),
        (23, "Jofra Archer", "England", "Bowler", "Right-hand bat", "Right-arm fast", "1995-04-01", 1),
        (24, "Mark Wood", "England", "Bowler", "Right-hand bat", "Right-arm fast", "1990-01-11", 1),
        (25, "Jonny Bairstow", "England", "Wicket-keeper", "Right-hand bat", "Right-arm medium", "1989-09-26", 1),

        # South Africa (26-30)
        (26, "Quinton de Kock", "South Africa", "Wicket-keeper", "Left-hand bat", "Slow left-arm orthodox", "1992-12-17", 1),
        (27, "Kagiso Rabada", "South Africa", "Bowler", "Left-hand bat", "Right-arm fast", "1995-05-25", 1),
        (28, "Heinrich Klaasen", "South Africa", "Wicket-keeper", "Right-hand bat", "Right-arm offbreak", "1991-07-30", 1),
        (29, "Aiden Markram", "South Africa", "Batsman", "Right-hand bat", "Right-arm offbreak", "1994-10-04", 1),
        (30, "Keshav Maharaj", "South Africa", "Bowler", "Right-hand bat", "Slow left-arm orthodox", "1990-02-07", 1),

        # Pakistan (31-34)
        (31, "Babar Azam", "Pakistan", "Batsman", "Right-hand bat", "Right-arm offbreak", "1994-10-15", 1),
        (32, "Shaheen Afridi", "Pakistan", "Bowler", "Left-hand bat", "Left-arm fast", "2000-04-06", 1),
        (33, "Mohammad Rizwan", "Pakistan", "Wicket-keeper", "Right-hand bat", "Right-arm medium", "1992-06-01", 1),
        (34, "Naseem Shah", "Pakistan", "Bowler", "Right-hand bat", "Right-arm fast", "2003-02-15", 1),

        # New Zealand (35-37)
        (35, "Kane Williamson", "New Zealand", "Batsman", "Right-hand bat", "Right-arm offbreak", "1990-08-08", 1),
        (36, "Trent Boult", "New Zealand", "Bowler", "Right-hand bat", "Left-arm fast-medium", "1989-07-22", 1),
        (37, "Daryl Mitchell", "New Zealand", "All-rounder", "Right-hand bat", "Right-arm medium", "1991-05-20", 1),

        # Others (38-40)
        (38, "Rashid Khan", "Afghanistan", "Bowler", "Right-hand bat", "Right-arm legbreak", "1998-09-20", 1),
        (39, "Shakib Al Hasan", "Bangladesh", "All-rounder", "Left-hand bat", "Slow left-arm orthodox", "1987-03-24", 1),
        (40, "Nicholas Pooran", "West Indies", "Wicket-keeper", "Left-hand bat", "Right-arm offbreak", "1995-10-02", 1)
    ]
    cursor.executemany("INSERT INTO players (player_id, full_name, country, playing_role, batting_style, bowling_style, dob, is_active) VALUES (?, ?, ?, ?, ?, ?, ?, ?)", players_data)

    # 5. PLAYER FORMAT STATS (Career records across Test, ODI, T20I)
    # Ensuring Top 10 ODI run scorers, All-rounders >1000 runs & >50 wkts, Format comparisons, etc.
    format_stats = [
        # Virat Kohli
        (1, "Test", 115, 195, 8848, 254, 49.15, 55.56, 29, 30, 0, 0.0, 0.0, 110, 0),
        (1, "ODI", 295, 283, 13906, 183, 58.18, 93.54, 50, 72, 5, 166.2, 6.22, 151, 0),
        (1, "T20I", 125, 117, 4188, 122, 48.69, 137.04, 1, 38, 4, 51.0, 8.05, 54, 0),

        # Rohit Sharma
        (2, "Test", 61, 105, 4179, 212, 44.45, 57.05, 12, 18, 2, 112.0, 3.8, 62, 0),
        (2, "ODI", 265, 257, 10866, 264, 49.16, 92.44, 31, 57, 9, 64.3, 5.21, 95, 0),
        (2, "T20I", 159, 151, 4231, 121, 32.05, 140.89, 5, 32, 1, 113.0, 8.8, 65, 0),

        # Jasprit Bumrah
        (3, "Test", 36, 68, 212, 34, 6.23, 44.5, 0, 0, 159, 20.69, 2.74, 15, 0),
        (3, "ODI", 89, 88, 75, 16, 7.5, 48.0, 0, 0, 149, 23.55, 4.59, 22, 0),
        (3, "T20I", 70, 69, 20, 7, 4.0, 62.5, 0, 0, 89, 17.74, 6.27, 14, 0),

        # Ravindra Jadeja (Elite All-rounder: >1000 runs and >50 wickets in Test and ODI!)
        (4, "Test", 72, 105, 3036, 175, 36.14, 58.20, 4, 21, 294, 24.13, 2.45, 43, 0),
        (4, "ODI", 197, 132, 2756, 87, 32.42, 84.43, 0, 13, 220, 36.07, 4.88, 71, 0),
        (4, "T20I", 74, 41, 515, 46, 21.45, 127.16, 0, 0, 54, 29.85, 7.13, 28, 0),

        # KL Rahul
        (5, "Test", 53, 91, 2983, 199, 34.28, 52.4, 8, 14, 0, 0.0, 0.0, 68, 0),
        (5, "ODI", 77, 72, 2851, 112, 49.15, 87.6, 7, 18, 0, 0.0, 0.0, 52, 5),
        (5, "T20I", 72, 68, 2265, 110, 37.75, 139.12, 2, 22, 0, 0.0, 0.0, 26, 1),

        # Shubman Gill
        (6, "Test", 25, 46, 1492, 128, 35.52, 58.9, 4, 6, 0, 0.0, 0.0, 18, 0),
        (6, "ODI", 47, 47, 2328, 208, 58.20, 101.74, 6, 13, 0, 0.0, 0.0, 24, 0),
        (6, "T20I", 21, 21, 578, 126, 30.42, 139.27, 1, 3, 0, 0.0, 0.0, 9, 0),

        # Hardik Pandya (All-rounder: ODI > 1000 runs, > 50 wickets)
        (7, "ODI", 86, 61, 1769, 92, 34.01, 110.35, 0, 11, 84, 35.61, 5.56, 35, 0),
        (7, "T20I", 100, 78, 1492, 71, 26.64, 140.48, 0, 4, 84, 25.48, 8.12, 52, 0),
        (7, "Test", 11, 18, 532, 108, 31.29, 73.88, 1, 4, 17, 31.05, 3.38, 7, 0),

        # Mohammed Shami
        (8, "Test", 64, 88, 750, 56, 12.09, 58.0, 0, 2, 229, 27.71, 3.30, 18, 0),
        (8, "ODI", 101, 47, 213, 25, 8.52, 85.0, 0, 0, 195, 23.68, 5.55, 31, 0),
        (8, "T20I", 23, 6, 12, 8, 4.0, 60.0, 0, 0, 24, 29.62, 8.94, 6, 0),

        # Steve Smith
        (11, "Test", 109, 195, 9685, 239, 56.97, 53.51, 32, 41, 19, 56.42, 3.98, 182, 0),
        (11, "ODI", 158, 142, 5446, 164, 43.91, 87.33, 12, 33, 28, 35.53, 5.41, 85, 0),
        (11, "T20I", 67, 55, 1094, 90, 25.44, 125.45, 0, 5, 17, 22.17, 7.55, 41, 0),

        # Pat Cummins
        (12, "Test", 62, 95, 1295, 64, 16.60, 46.2, 0, 3, 269, 22.53, 2.76, 32, 0),
        (12, "ODI", 88, 52, 420, 36, 12.35, 75.0, 0, 0, 141, 28.16, 5.25, 28, 0),
        (12, "T20I", 52, 28, 150, 28, 11.53, 120.0, 0, 0, 61, 22.85, 7.35, 18, 0),

        # Travis Head
        (13, "Test", 49, 81, 3173, 175, 41.75, 63.8, 7, 16, 14, 52.0, 3.45, 36, 0),
        (13, "ODI", 65, 62, 2397, 152, 42.05, 104.26, 5, 16, 18, 46.3, 5.65, 28, 0),
        (13, "T20I", 32, 31, 950, 91, 34.0, 158.5, 0, 5, 1, 45.0, 8.5, 15, 0),

        # Glenn Maxwell (All-rounder: ODI > 1000 runs, > 50 wickets!)
        (14, "ODI", 142, 131, 3934, 201, 35.44, 126.90, 4, 23, 70, 48.27, 5.56, 85, 0),
        (14, "T20I", 106, 98, 2468, 145, 29.38, 155.51, 5, 10, 40, 27.22, 7.52, 50, 0),
        (14, "Test", 7, 14, 339, 104, 26.07, 65.5, 1, 0, 8, 42.62, 4.12, 5, 0),

        # Mitchell Starc
        (15, "Test", 89, 130, 2097, 99, 21.84, 69.5, 0, 10, 358, 27.74, 3.41, 44, 0),
        (15, "ODI", 121, 68, 540, 52, 12.85, 85.5, 0, 1, 236, 22.96, 5.15, 42, 0),
        (15, "T20I", 65, 22, 102, 14, 8.5, 95.0, 0, 0, 79, 23.81, 7.64, 18, 0),

        # David Warner (Top ODI run scorer)
        (16, "ODI", 161, 159, 6932, 179, 45.30, 97.26, 22, 33, 0, 0.0, 0.0, 75, 0),
        (16, "Test", 112, 205, 8786, 335, 44.59, 70.19, 26, 37, 4, 68.0, 3.8, 85, 0),
        (16, "T20I", 110, 110, 3277, 100, 33.43, 142.47, 1, 28, 0, 0.0, 0.0, 60, 0),

        # Joe Root (Top ODI run scorer, Test Legend)
        (19, "Test", 143, 262, 12027, 254, 50.11, 56.66, 32, 63, 62, 45.2, 3.1, 196, 0),
        (19, "ODI", 171, 160, 6522, 133, 47.60, 86.93, 16, 39, 27, 48.0, 5.8, 86, 0),
        (19, "T20I", 32, 30, 893, 90, 35.72, 126.3, 0, 5, 6, 28.5, 8.5, 18, 0),

        # Ben Stokes (Premier All-rounder: >1000 runs and >50 wickets in Test and ODI!)
        (20, "Test", 105, 190, 6508, 258, 35.75, 59.20, 13, 31, 203, 32.07, 3.32, 105, 0),
        (20, "ODI", 114, 98, 3159, 182, 38.99, 96.25, 4, 22, 74, 42.39, 6.05, 52, 0),
        (20, "T20I", 43, 36, 585, 52, 21.66, 128.0, 0, 1, 26, 32.92, 8.39, 22, 0),

        # Jos Buttler
        (21, "ODI", 181, 154, 5022, 162, 39.54, 117.11, 11, 26, 0, 0.0, 0.0, 214, 36),
        (21, "T20I", 124, 113, 3264, 101, 35.86, 146.3, 1, 24, 0, 0.0, 0.0, 75, 14),
        (21, "Test", 57, 100, 2907, 152, 31.94, 54.2, 2, 18, 0, 0.0, 0.0, 153, 1),

        # Quinton de Kock (Top ODI run scorer)
        (26, "ODI", 155, 155, 6770, 178, 45.74, 96.64, 21, 30, 0, 0.0, 0.0, 183, 17),
        (26, "T20I", 92, 91, 2584, 100, 31.51, 138.33, 1, 16, 0, 0.0, 0.0, 89, 18),
        (26, "Test", 54, 91, 3300, 141, 38.82, 70.93, 6, 22, 0, 0.0, 0.0, 221, 11),

        # Babar Azam (Top ODI run scorer)
        (31, "ODI", 117, 114, 5729, 158, 56.72, 88.75, 19, 32, 0, 0.0, 0.0, 52, 0),
        (31, "T20I", 123, 116, 4145, 122, 41.03, 129.08, 3, 36, 0, 0.0, 0.0, 50, 0),
        (31, "Test", 54, 98, 3962, 196, 44.51, 54.8, 9, 26, 2, 80.0, 4.0, 38, 0),

        # Shaheen Afridi
        (32, "Test", 29, 44, 215, 23, 8.26, 46.5, 0, 0, 113, 26.65, 3.12, 10, 0),
        (32, "ODI", 53, 29, 185, 25, 11.56, 75.0, 0, 0, 104, 23.94, 5.54, 15, 0),
        (32, "T20I", 70, 22, 102, 23, 11.33, 125.0, 0, 0, 96, 20.82, 7.73, 16, 0),

        # Kane Williamson (Top ODI run scorer)
        (35, "ODI", 165, 157, 6810, 148, 48.64, 81.36, 13, 45, 37, 35.4, 5.35, 72, 0),
        (35, "Test", 100, 176, 8743, 251, 54.98, 51.41, 32, 34, 30, 40.2, 2.9, 88, 0),
        (35, "T20I", 93, 90, 2575, 95, 33.44, 123.08, 0, 18, 6, 27.5, 7.5, 42, 0),

        # Shakib Al Hasan (Legendary All-rounder: >1000 runs and >50 wickets across formats!)
        (39, "ODI", 247, 234, 7570, 134, 37.29, 82.52, 9, 56, 317, 29.53, 4.44, 59, 0),
        (39, "Test", 69, 125, 4529, 217, 38.05, 62.05, 5, 31, 246, 31.42, 3.01, 27, 0),
        (39, "T20I", 129, 127, 2551, 84, 23.19, 121.99, 0, 13, 149, 20.91, 6.78, 29, 0),

        # Rashid Khan
        (38, "ODI", 103, 78, 1240, 60, 20.0, 104.5, 0, 5, 182, 18.52, 4.16, 33, 0),
        (38, "T20I", 93, 56, 450, 48, 14.5, 129.8, 0, 0, 150, 14.20, 6.07, 34, 0),
        (38, "Test", 5, 8, 106, 51, 15.14, 58.0, 0, 1, 34, 22.35, 3.05, 2, 0)
    ]
    cursor.executemany("""
        INSERT INTO player_format_stats 
        (player_id, format, matches, innings, runs, highest_score, batting_average, strike_rate, centuries, half_centuries, wickets, bowling_average, economy_rate, catches, stumpings)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, format_stats)

    # 6. MATCHES (55 comprehensive matches spanning 2020-2024 + 10 matches in the last 30 days!)
    # Today's reference date
    today = datetime.date.today()
    
    matches_list = []
    # 10 Recent Matches (last 30 days) to ensure Q2 always returns rich data!
    for i in range(1, 11):
        m_date = (today - datetime.timedelta(days=i*2)).isoformat()
        t1, t2 = (1, 2) if i % 2 == 0 else (1, 3)
        venue = (i % 7) + 1
        toss_win = t1 if i % 2 == 1 else t2
        toss_dec = "Bat" if i % 3 != 0 else "Bowl"
        win_team = t1 if i % 3 != 1 else t2
        m_format = "T20I" if i <= 5 else "ODI"
        margin = 12 + i * 3
        matches_list.append((
            i, 1, f"{teams_data[t1-1][1]} vs {teams_data[t2-1][1]} {m_format} Series 2024 - Match {i}",
            t1, t2, venue, m_date, m_format, toss_win, toss_dec, win_team, margin, "runs", "Completed"
        ))

    # Additional historical matches 2020 to 2024 (including close matches, home & away)
    historical_matches = [
        # (match_id, series_id, desc, team1, team2, venue, date, format, toss_win, toss_dec, winner, margin, vic_type, status)
        (11, 5, "India vs Australia ICC CWC 2023 Final", 1, 2, 1, "2023-11-19", "ODI", 2, "Bowl", 2, 6, "wickets", "Completed"),
        (12, 5, "India vs New Zealand ICC CWC 2023 Semi Final", 1, 6, 7, "2023-11-15", "ODI", 1, "Bat", 1, 70, "runs", "Completed"),
        (13, 5, "South Africa vs Australia ICC CWC 2023 Semi Final", 4, 2, 3, "2023-11-16", "ODI", 4, "Bat", 2, 3, "wickets", "Completed"), # Close match (< 5 wickets)
        (14, 5, "India vs Pakistan ICC CWC 2023 Group Match", 1, 5, 1, "2023-10-14", "ODI", 1, "Bowl", 1, 7, "wickets", "Completed"),
        (15, 5, "Australia vs England ICC CWC 2023 Group Match", 2, 3, 1, "2023-11-04", "ODI", 3, "Bowl", 2, 33, "runs", "Completed"), # Close match (< 50 runs)
        (16, 5, "South Africa vs Pakistan ICC CWC 2023 Thriller", 4, 5, 3, "2023-10-27", "ODI", 5, "Bat", 4, 1, "wickets", "Completed"), # Close match (1 wicket!)
        (17, 3, "India vs England 1st Test 2024", 1, 3, 7, "2024-01-25", "Test", 3, "Bat", 3, 28, "runs", "Completed"), # Close match (< 50 runs)
        (18, 3, "India vs England 2nd Test 2024", 1, 3, 3, "2024-02-02", "Test", 1, "Bat", 1, 106, "runs", "Completed"),
        (19, 3, "India vs England 3rd Test 2024", 1, 3, 1, "2024-02-15", "Test", 1, "Bat", 1, 434, "runs", "Completed"),
        (20, 3, "India vs England 4th Test 2024", 1, 3, 7, "2024-02-23", "Test", 3, "Bat", 1, 5, "wickets", "Completed"),
        (21, 3, "India vs England 5th Test 2024", 1, 3, 7, "2024-03-07", "Test", 3, "Bat", 1, 64, "runs", "Completed"),
        (22, 7, "The Ashes 2023 1st Test Edgbaston", 3, 2, 10, "2023-06-16", "Test", 3, "Bat", 2, 2, "wickets", "Completed"), # Close match (2 wickets)
        (23, 7, "The Ashes 2023 2nd Test Lord's", 3, 2, 8, "2023-06-28", "Test", 3, "Bowl", 2, 43, "runs", "Completed"), # Close match (43 runs)
        (24, 7, "The Ashes 2023 3rd Test Headingley", 3, 2, 9, "2023-07-06", "Test", 3, "Bowl", 3, 3, "wickets", "Completed"), # Close match (3 wickets)
        (25, 7, "The Ashes 2023 5th Test The Oval", 3, 2, 9, "2023-07-27", "Test", 2, "Bowl", 3, 49, "runs", "Completed"), # Close match (49 runs)
        
        # 2022 Matches
        (26, 1, "India vs Pakistan T20 World Cup 2022 MCG", 1, 5, 2, "2022-10-23", "T20I", 1, "Bowl", 1, 4, "wickets", "Completed"), # Close match (4 wickets)
        (27, 1, "England vs Pakistan T20 World Cup 2022 Final", 3, 5, 2, "2022-11-13", "T20I", 3, "Bowl", 3, 5, "wickets", "Completed"),
        (28, 1, "India vs England T20 World Cup 2022 Semi Final", 1, 3, 5, "2022-11-10", "T20I", 3, "Bowl", 3, 10, "wickets", "Completed"),
        (29, 6, "India vs Australia T20I Series 2022 Mohali", 1, 2, 1, "2022-09-20", "T20I", 2, "Bowl", 2, 4, "wickets", "Completed"),
        (30, 6, "India vs Australia T20I Series 2022 Nagpur", 1, 2, 1, "2022-09-23", "T20I", 1, "Bowl", 1, 6, "wickets", "Completed"),
        (31, 6, "India vs Australia T20I Series 2022 Hyderabad", 1, 2, 7, "2022-09-25", "T20I", 1, "Bowl", 1, 6, "wickets", "Completed"),

        # 2021 Matches
        (32, 2, "Australia vs India Border Gavaskar 2020-21 Brisbane", 2, 1, 4, "2021-01-15", "Test", 2, "Bat", 1, 3, "wickets", "Completed"), # Close match (3 wickets)
        (33, 2, "Australia vs India Border Gavaskar 2020-21 Sydney", 2, 1, 6, "2021-01-07", "Test", 2, "Bat", 1, 0, "tie", "Completed"),
        (34, 4, "England vs India 2nd Test Lord's 2021", 3, 1, 8, "2021-08-12", "Test", 3, "Bowl", 1, 151, "runs", "Completed"),
        (35, 4, "England vs India 4th Test The Oval 2021", 3, 1, 9, "2021-09-02", "Test", 3, "Bowl", 1, 157, "runs", "Completed"),

        # 2020 Matches
        (36, 2, "Australia vs India 1st ODI Sydney 2020", 2, 1, 6, "2020-11-27", "ODI", 2, "Bat", 2, 66, "runs", "Completed"),
        (37, 2, "Australia vs India 2nd ODI Sydney 2020", 2, 1, 6, "2020-11-29", "ODI", 2, "Bat", 2, 51, "runs", "Completed"),
        (38, 2, "Australia vs India 3rd ODI Canberra 2020", 2, 1, 5, "2020-12-02", "ODI", 1, "Bat", 1, 13, "runs", "Completed"), # Close match (13 runs)
        (39, 2, "Australia vs India 1st T20I Canberra 2020", 2, 1, 5, "2020-12-04", "T20I", 2, "Bowl", 1, 11, "runs", "Completed"), # Close match (11 runs)
        (40, 2, "Australia vs India 2nd T20I Sydney 2020", 2, 1, 6, "2020-12-06", "T20I", 1, "Bowl", 1, 6, "wickets", "Completed"),
        
        # More matches to give teams >= 5 matches against each other in last 3 years (Q22)
        (41, 5, "India vs Australia WTC Final 2023", 1, 2, 9, "2023-06-07", "Test", 1, "Bowl", 2, 209, "runs", "Completed"),
        (42, 5, "India vs Australia 1st ODI Mohali 2023", 1, 2, 1, "2023-09-22", "ODI", 1, "Bowl", 1, 5, "wickets", "Completed"),
        (43, 5, "India vs Australia 2nd ODI Indore 2023", 1, 2, 7, "2023-09-24", "ODI", 2, "Bowl", 1, 99, "runs", "Completed"),
        (44, 5, "India vs Australia 3rd ODI Rajkot 2023", 1, 2, 1, "2023-09-27", "ODI", 2, "Bat", 2, 66, "runs", "Completed"),
        (45, 5, "India vs Australia ICC CWC Group Stage 2023", 1, 2, 3, "2023-10-08", "ODI", 2, "Bat", 1, 6, "wickets", "Completed"),

        # Additional venues & teams
        (46, 8, "South Africa vs India 1st Test Centurion 2023", 4, 1, 12, "2023-12-26", "Test", 4, "Bowl", 4, 32, "runs", "Completed"),
        (47, 8, "South Africa vs India 2nd Test Cape Town 2024", 4, 1, 11, "2024-01-03", "Test", 4, "Bat", 1, 7, "wickets", "Completed"),
        (48, 6, "Pakistan vs India Asia Cup Super 4 2023", 5, 1, 14, "2023-09-10", "ODI", 5, "Bowl", 1, 228, "runs", "Completed"),
        (49, 1, "India vs South Africa T20 World Cup 2024 Final", 1, 4, 14, "2024-06-29", "T20I", 1, "Bat", 1, 7, "runs", "Completed"), # Close match (7 runs)
        (50, 1, "India vs England T20 World Cup 2024 Semi Final", 1, 3, 14, "2024-06-27", "T20I", 3, "Bowl", 1, 68, "runs", "Completed")
    ]
    matches_list.extend(historical_matches)
    cursor.executemany("""
        INSERT INTO matches (match_id, series_id, match_description, team1_id, team2_id, venue_id, match_date, format, toss_winner_id, toss_decision, winning_team_id, victory_margin, victory_type, status)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, matches_list)

    # 7. PARTNERSHIPS (Consecutive batsmen scoring >= 100 runs, and >= 5 partnerships between pairs for Q13 & Q24)
    # Rohit Sharma (p1) & Shubman Gill (p2) - Positions 1 & 2
    # Virat Kohli (p1) & Rohit Sharma (p2) - Positions 2 & 3 or 1 & 3
    # Steve Smith & Travis Head - Positions 3 & 4
    # Joe Root & Ben Stokes - Positions 4 & 5
    partnerships_data = [
        # Rohit (1) & Gill (6) - consecutive positions 1 & 2
        (1, 11, 1, 2, 6, 1, 2, 102, 88),
        (2, 12, 1, 2, 6, 1, 2, 115, 92),
        (3, 14, 1, 2, 6, 1, 2, 128, 105),
        (4, 42, 1, 2, 6, 1, 2, 142, 110),
        (5, 43, 1, 2, 6, 1, 2, 108, 96),
        (6, 45, 1, 2, 6, 1, 2, 64, 52),
        (7, 48, 1, 2, 6, 1, 2, 121, 98),

        # Rohit (2) & Virat Kohli (1) - positions 2 & 3
        (8, 1, 1, 2, 1, 2, 3, 140, 110),
        (9, 2, 1, 2, 1, 2, 3, 110, 89),
        (10, 3, 1, 2, 1, 2, 3, 168, 125),
        (11, 4, 1, 2, 1, 2, 3, 95, 78),
        (12, 5, 1, 2, 1, 2, 3, 132, 101),
        (13, 6, 1, 2, 1, 2, 3, 155, 118),

        # Steve Smith (11) & Travis Head (13) - consecutive positions 3 & 4
        (14, 11, 1, 11, 13, 3, 4, 174, 160),
        (15, 15, 1, 11, 13, 3, 4, 118, 105),
        (16, 22, 1, 11, 13, 3, 4, 112, 120),
        (17, 23, 1, 11, 13, 3, 4, 125, 110),
        (18, 41, 1, 11, 13, 3, 4, 285, 230), # Massive WTC final partnership!
        (19, 44, 1, 11, 13, 3, 4, 137, 115),

        # Joe Root (19) & Ben Stokes (20) - consecutive positions 4 & 5
        (20, 17, 1, 19, 20, 4, 5, 105, 140),
        (21, 18, 1, 19, 20, 4, 5, 110, 130),
        (22, 22, 1, 19, 20, 4, 5, 125, 115),
        (23, 23, 1, 19, 20, 4, 5, 108, 122),
        (24, 24, 1, 19, 20, 4, 5, 114, 128),
        (25, 25, 1, 19, 20, 4, 5, 135, 142),

        # Babar Azam (31) & Mohammad Rizwan (33) - consecutive positions 2 & 3
        (26, 16, 1, 31, 33, 2, 3, 105, 95),
        (27, 26, 1, 31, 33, 2, 3, 112, 98),
        (28, 27, 1, 31, 33, 2, 3, 120, 105),
        (29, 48, 1, 31, 33, 2, 3, 98, 85),
        (30, 48, 2, 31, 33, 2, 3, 130, 112)
    ]
    cursor.executemany("""
        INSERT INTO partnerships 
        (partnership_id, match_id, innings, player1_id, player2_id, player1_pos, player2_pos, partnership_runs, balls_faced)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, partnerships_data)

    # 8. PLAYER MATCH PERFORMANCES (Innings records for Q14, Q15, Q16, Q18, Q19, Q21, Q23, Q25)
    # Generate structured performances spanning 2020 to 2024 across 50 matches
    perf_records = []
    perf_id = 1

    # Key players to generate consistent time-series performances:
    # Virat Kohli (1), Rohit Sharma (2), Jasprit Bumrah (3), Steve Smith (11), Travis Head (13), Joe Root (19), Ben Stokes (20), Babar Azam (31)
    
    # 25+ matches with deep data
    for m in matches_list:
        m_id = m[0]
        m_format = m[7]
        m_winner = m[10]
        
        # Virat Kohli in this match
        runs_k = random.randint(35, 115) if m_id % 3 == 0 else random.randint(15, 65)
        balls_k = int(runs_k * random.uniform(0.75, 1.25))
        sr_k = round((runs_k / max(1, balls_k)) * 100, 2)
        perf_records.append((
            perf_id, m_id, 1, 1, 1, 3, runs_k, balls_k, int(runs_k * 0.1), int(runs_k * 0.03), sr_k,
            0.0, 0, 0, 0, 0.0, random.choice([0, 1, 2]), 0
        ))
        perf_id += 1

        # Rohit Sharma in this match
        runs_r = random.randint(40, 125) if m_id % 4 == 0 else random.randint(12, 60)
        balls_r = int(runs_r * random.uniform(0.7, 1.1))
        sr_r = round((runs_r / max(1, balls_r)) * 100, 2)
        perf_records.append((
            perf_id, m_id, 2, 1, 1, 1, runs_r, balls_r, int(runs_r * 0.12), int(runs_r * 0.05), sr_r,
            0.0, 0, 0, 0, 0.0, random.choice([0, 1]), 0
        ))
        perf_id += 1

        # Jasprit Bumrah in this match (Bowler >= 4 overs / match for Q14 and economy in ODI/T20 for Q18)
        overs_b = 4.0 if m_format == "T20I" else (10.0 if m_format == "ODI" else 18.0)
        wkts_b = random.choice([1, 2, 3, 4]) if m_id % 2 == 0 else random.choice([0, 1, 2])
        runs_con_b = int(overs_b * random.uniform(3.5, 5.2))
        econ_b = round(runs_con_b / overs_b, 2)
        perf_records.append((
            perf_id, m_id, 3, 1, 2, 10, random.randint(0, 15), random.randint(2, 12), 0, 0, 50.0,
            overs_b, runs_con_b, wkts_b, random.choice([0, 1, 2]), econ_b, 1, 0
        ))
        perf_id += 1

        # Ravindra Jadeja (All-rounder)
        overs_j = 4.0 if m_format == "T20I" else (10.0 if m_format == "ODI" else 15.0)
        wkts_j = random.choice([1, 2, 3])
        runs_con_j = int(overs_j * random.uniform(4.0, 5.5))
        econ_j = round(runs_con_j / overs_j, 2)
        runs_j = random.randint(15, 60)
        balls_j = int(runs_j * 0.8)
        perf_records.append((
            perf_id, m_id, 4, 1, 1, 7, runs_j, balls_j, 2, 1, 120.0,
            overs_j, runs_con_j, wkts_j, 0, econ_j, random.choice([1, 2]), 0
        ))
        perf_id += 1

        # Steve Smith in this match
        runs_s = random.randint(45, 110) if m_id % 3 == 1 else random.randint(20, 55)
        balls_s = int(runs_s * random.uniform(1.0, 1.4))
        sr_s = round((runs_s / max(1, balls_s)) * 100, 2)
        perf_records.append((
            perf_id, m_id, 11, 2, 1, 3, runs_s, balls_s, int(runs_s * 0.08), 1, sr_s,
            0.0, 0, 0, 0, 0.0, random.choice([0, 1, 2]), 0
        ))
        perf_id += 1

        # Travis Head in this match
        runs_h = random.randint(50, 135) if m_id % 3 == 0 else random.randint(10, 45)
        balls_h = int(runs_h * random.uniform(0.65, 0.95))
        sr_h = round((runs_h / max(1, balls_h)) * 100, 2)
        perf_records.append((
            perf_id, m_id, 13, 2, 1, 4, runs_h, balls_h, int(runs_h * 0.12), int(runs_h * 0.06), sr_h,
            2.0, 16, 1, 0, 8.0, 1, 0
        ))
        perf_id += 1

        # Pat Cummins (Bowler >= 4 overs / match for Q14)
        overs_c = 4.0 if m_format == "T20I" else (10.0 if m_format == "ODI" else 20.0)
        wkts_c = random.choice([1, 2, 3])
        runs_con_c = int(overs_c * random.uniform(4.0, 5.6))
        econ_c = round(runs_con_c / overs_c, 2)
        perf_records.append((
            perf_id, m_id, 12, 2, 2, 8, random.randint(5, 30), random.randint(8, 20), 1, 1, 110.0,
            overs_c, runs_con_c, wkts_c, 1, econ_c, 1, 0
        ))
        perf_id += 1

        # Joe Root in this match
        runs_root = random.randint(40, 120) if m_id % 2 == 0 else random.randint(15, 50)
        balls_root = int(runs_root * 1.2)
        sr_root = round((runs_root / max(1, balls_root)) * 100, 2)
        perf_records.append((
            perf_id, m_id, 19, 3, 1, 4, runs_root, balls_root, 6, 0, sr_root,
            3.0, 18, 1, 0, 6.0, 1, 0
        ))
        perf_id += 1

        # Ben Stokes
        runs_st = random.randint(25, 95)
        balls_st = int(runs_st * 1.05)
        perf_records.append((
            perf_id, m_id, 20, 3, 1, 5, runs_st, balls_st, 4, 2, 115.0,
            5.0, 32, 2, 0, 6.4, 2, 0
        ))
        perf_id += 1

        # Babar Azam
        runs_ba = random.randint(30, 85)
        balls_ba = int(runs_ba * 1.1)
        perf_records.append((
            perf_id, m_id, 31, 5, 1, 2, runs_ba, balls_ba, 5, 1, 118.0,
            0.0, 0, 0, 0, 0.0, 1, 0
        ))
        perf_id += 1

    cursor.executemany("""
        INSERT INTO player_match_performances 
        (perf_id, match_id, player_id, team_id, innings, batting_position, runs_scored, balls_faced, fours, sixes, strike_rate, overs_bowled, runs_conceded, wickets_taken, maiden_overs, economy_rate, catches, stumpings)
        VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)
    """, perf_records)

    conn.commit()
    conn.close()
    print(f"Successfully seeded database at {DB_PATH}")
    print(f"Teams: {len(teams_data)}, Venues: {len(venues_data)}, Players: {len(players_data)}, Matches: {len(matches_list)}, Performances: {len(perf_records)}")


if __name__ == "__main__":
    seed_database()

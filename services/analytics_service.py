"""
Analytics Service Module
Contains the comprehensive repository of all 25 SQL practice questions,
including business context, SQL concepts, execution plans, and recommended charts.
"""

import time
import pandas as pd
from typing import Dict, Any, List
from database.db_connection import execute_query

SQL_QUESTIONS: List[Dict[str, Any]] = [
    # ------------------ BEGINNER (Q1 - Q8) ------------------
    {
        "id": 1,
        "level": "Beginner",
        "title": "Indian National Team Roster",
        "problem": "Find all players who represent India. Display their full name, playing role, batting style, and bowling style.",
        "concepts": "SELECT, WHERE filter, ORDER BY alphabetical sorting",
        "tables": "players",
        "query": """SELECT 
    full_name,
    playing_role,
    batting_style,
    bowling_style
FROM players
WHERE country = 'India'
ORDER BY full_name ASC;""",
        "chart_type": "table"
    },
    {
        "id": 2,
        "level": "Beginner",
        "title": "Matches Played in Last 30 Days",
        "problem": "Show all cricket matches that were played in the last 30 days. Include match description, both team names, venue name with city, and match date. Sort by most recent matches first.",
        "concepts": "INNER JOIN (multi-table), DATE functions (DATE('now', '-30 days')), ORDER BY DESC",
        "tables": "matches, teams, venues",
        "query": """SELECT 
    m.match_description,
    t1.team_name AS team_1,
    t2.team_name AS team_2,
    v.venue_name || ', ' || v.city AS venue_location,
    m.match_date
FROM matches m
JOIN teams t1 ON m.team1_id = t1.team_id
JOIN teams t2 ON m.team2_id = t2.team_id
JOIN venues v ON m.venue_id = v.venue_id
WHERE m.match_date >= DATE('now', '-30 days')
ORDER BY m.match_date DESC;""",
        "chart_type": "table"
    },
    {
        "id": 3,
        "level": "Beginner",
        "title": "Top 10 ODI Run Scorers",
        "problem": "List the top 10 highest run scorers in ODI cricket. Show player name, total runs scored, batting average, and number of centuries. Display the highest run scorer first.",
        "concepts": "JOIN, WHERE format condition, ORDER BY, LIMIT clause",
        "tables": "player_format_stats, players",
        "query": """SELECT 
    p.full_name AS player_name,
    pfs.runs AS total_runs,
    pfs.batting_average,
    pfs.centuries
FROM player_format_stats pfs
JOIN players p ON pfs.player_id = p.player_id
WHERE pfs.format = 'ODI'
ORDER BY pfs.runs DESC
LIMIT 10;""",
        "chart_type": "bar_runs"
    },
    {
        "id": 4,
        "level": "Beginner",
        "title": "Mega Stadiums (>50k Capacity)",
        "problem": "Display all cricket venues that have a seating capacity of more than 50,000 spectators. Show venue name, city, country, and capacity. Order by largest capacity first.",
        "concepts": "Numerical filtering (WHERE capacity > 50000), ORDER BY DESC",
        "tables": "venues",
        "query": """SELECT 
    venue_name,
    city,
    country,
    capacity
FROM venues
WHERE capacity > 50000
ORDER BY capacity DESC;""",
        "chart_type": "bar_capacity"
    },
    {
        "id": 5,
        "level": "Beginner",
        "title": "Total Wins by Team",
        "problem": "Calculate how many matches each team has won. Show team name and total number of wins. Display teams with most wins first.",
        "concepts": "LEFT JOIN, COUNT aggregate, GROUP BY, ORDER BY DESC",
        "tables": "teams, matches",
        "query": """SELECT 
    t.team_name,
    COUNT(m.match_id) AS total_wins
FROM teams t
LEFT JOIN matches m ON t.team_id = m.winning_team_id
GROUP BY t.team_id, t.team_name
ORDER BY total_wins DESC;""",
        "chart_type": "bar_wins"
    },
    {
        "id": 6,
        "level": "Beginner",
        "title": "Player Role Distribution",
        "problem": "Count how many players belong to each playing role (Batsman, Bowler, All-rounder, Wicket-keeper). Show the role and count of players for each role.",
        "concepts": "GROUP BY categorical grouping, COUNT aggregate",
        "tables": "players",
        "query": """SELECT 
    playing_role,
    COUNT(player_id) AS total_players
FROM players
GROUP BY playing_role
ORDER BY total_players DESC;""",
        "chart_type": "pie_roles"
    },
    {
        "id": 7,
        "level": "Beginner",
        "title": "Highest Score by Format",
        "problem": "Find the highest individual batting score achieved in each cricket format (Test, ODI, T20I). Display format and highest score.",
        "concepts": "MAX aggregate function, GROUP BY format",
        "tables": "player_format_stats",
        "query": """SELECT 
    format,
    MAX(highest_score) AS highest_individual_score
FROM player_format_stats
GROUP BY format
ORDER BY highest_individual_score DESC;""",
        "chart_type": "bar_scores"
    },
    {
        "id": 8,
        "level": "Beginner",
        "title": "Series Commenced in 2024",
        "problem": "Show all cricket series that started in the year 2024. Include series name, host country, match type, start date, and total number of matches planned.",
        "concepts": "Date string extraction strftime('%Y', start_date), filtering",
        "tables": "series",
        "query": """SELECT 
    series_name,
    host_country,
    match_type,
    start_date,
    total_matches
FROM series
WHERE strftime('%Y', start_date) = '2024'
ORDER BY start_date ASC;""",
        "chart_type": "table"
    },

    # ------------------ INTERMEDIATE (Q9 - Q16) ------------------
    {
        "id": 9,
        "level": "Intermediate",
        "title": "Elite All-Rounders (1000+ Runs & 50+ Wickets)",
        "problem": "Find all-rounder players who have scored more than 1000 runs AND taken more than 50 wickets in their career. Display player name, total runs, total wickets, and format.",
        "concepts": "Multi-conditional filtering with AND, relational JOIN",
        "tables": "player_format_stats, players",
        "query": """SELECT 
    p.full_name AS player_name,
    pfs.format,
    pfs.runs AS total_runs,
    pfs.wickets AS total_wickets
FROM player_format_stats pfs
JOIN players p ON pfs.player_id = p.player_id
WHERE p.playing_role = 'All-rounder' 
  AND pfs.runs > 1000 
  AND pfs.wickets > 50
ORDER BY pfs.runs DESC;""",
        "chart_type": "scatter_allrounders"
    },
    {
        "id": 10,
        "level": "Intermediate",
        "title": "Last 20 Completed Match Results",
        "problem": "Get details of the last 20 completed matches. Show match description, both team names, winning team, victory margin, victory type (runs/wickets), and venue name.",
        "concepts": "String concatenation (||), multiple table JOINs, LIMIT 20",
        "tables": "matches, teams, venues",
        "query": """SELECT 
    m.match_description,
    t1.team_name AS team_1,
    t2.team_name AS team_2,
    tw.team_name AS winning_team,
    m.victory_margin || ' ' || m.victory_type AS victory_result,
    v.venue_name
FROM matches m
JOIN teams t1 ON m.team1_id = t1.team_id
JOIN teams t2 ON m.team2_id = t2.team_id
LEFT JOIN teams tw ON m.winning_team_id = tw.team_id
JOIN venues v ON m.venue_id = v.venue_id
WHERE m.status = 'Completed'
ORDER BY m.match_date DESC
LIMIT 20;""",
        "chart_type": "table"
    },
    {
        "id": 11,
        "level": "Intermediate",
        "title": "Cross-Format Performance Matrix",
        "problem": "Compare each player's performance across different cricket formats. For players who have played at least 2 different formats, show their total runs in Test, ODI, and T20I, along with overall batting average.",
        "concepts": "Conditional aggregation (CASE WHEN), HAVING COUNT(DISTINCT format) >= 2",
        "tables": "players, player_format_stats",
        "query": """SELECT 
    p.full_name AS player_name,
    COALESCE(SUM(CASE WHEN pfs.format = 'Test' THEN pfs.runs END), 0) AS test_runs,
    COALESCE(SUM(CASE WHEN pfs.format = 'ODI' THEN pfs.runs END), 0) AS odi_runs,
    COALESCE(SUM(CASE WHEN pfs.format = 'T20I' THEN pfs.runs END), 0) AS t20i_runs,
    ROUND(SUM(pfs.runs * 1.0) / NULLIF(SUM(CASE WHEN pfs.batting_average > 0 THEN pfs.runs / pfs.batting_average ELSE 1 END), 0), 2) AS overall_batting_avg
FROM players p
JOIN player_format_stats pfs ON p.player_id = pfs.player_id
GROUP BY p.player_id, p.full_name
HAVING COUNT(DISTINCT pfs.format) >= 2
ORDER BY (test_runs + odi_runs + t20i_runs) DESC;""",
        "chart_type": "bar_cross_format"
    },
    {
        "id": 12,
        "level": "Intermediate",
        "title": "Home vs Away Win Analysis",
        "problem": "Analyze each international team's performance when playing at home versus playing away. Determine whether each team played at home or away based on venue country.",
        "concepts": "Complex CASE expression matching venue country against team country, grouping",
        "tables": "teams, matches, venues",
        "query": """SELECT 
    t.team_name,
    SUM(CASE WHEN v.country = t.country AND m.winning_team_id = t.team_id THEN 1 ELSE 0 END) AS home_wins,
    SUM(CASE WHEN v.country != t.country AND m.winning_team_id = t.team_id THEN 1 ELSE 0 END) AS away_wins,
    COUNT(CASE WHEN m.winning_team_id = t.team_id THEN 1 END) AS total_wins
FROM teams t
JOIN matches m ON t.team_id = m.team1_id OR t.team_id = m.team2_id
JOIN venues v ON m.venue_id = v.venue_id
GROUP BY t.team_id, t.team_name
ORDER BY total_wins DESC;""",
        "chart_type": "bar_home_away"
    },
    {
        "id": 13,
        "level": "Intermediate",
        "title": "Century Batting Partnerships (Adjacent Batsmen)",
        "problem": "Identify batting partnerships where two consecutive batsmen (batting positions next to each other) scored a combined total of 100 or more runs in the same innings.",
        "concepts": "Mathematical condition ABS(pos1 - pos2) = 1, self-joins on players",
        "tables": "partnerships, players",
        "query": """SELECT 
    p1.full_name AS batsman_1,
    p2.full_name AS batsman_2,
    pt.partnership_runs,
    pt.match_id,
    pt.innings
FROM partnerships pt
JOIN players p1 ON pt.player1_id = p1.player_id
JOIN players p2 ON pt.player2_id = p2.player_id
WHERE ABS(pt.player1_pos - pt.player2_pos) = 1 
  AND pt.partnership_runs >= 100
ORDER BY pt.partnership_runs DESC;""",
        "chart_type": "table"
    },
    {
        "id": 14,
        "level": "Intermediate",
        "title": "Venue-Specific Bowling Analysis",
        "problem": "Examine bowling performance at different venues. For bowlers who played at least 3 matches at the same venue, calculate average economy rate, total wickets, and matches bowled (overs >= 4).",
        "concepts": "Multi-column GROUP BY, HAVING COUNT(DISTINCT match_id) >= 3, AVG economy",
        "tables": "player_match_performances, players, matches, venues",
        "query": """SELECT 
    p.full_name AS bowler_name,
    v.venue_name,
    COUNT(DISTINCT pmp.match_id) AS matches_played,
    SUM(pmp.wickets_taken) AS total_wickets,
    ROUND(AVG(pmp.economy_rate), 2) AS avg_economy_rate
FROM player_match_performances pmp
JOIN players p ON pmp.player_id = p.player_id
JOIN matches m ON pmp.match_id = m.match_id
JOIN venues v ON m.venue_id = v.venue_id
WHERE pmp.overs_bowled >= 4.0
GROUP BY p.player_id, v.venue_id
HAVING COUNT(DISTINCT pmp.match_id) >= 3
ORDER BY total_wickets DESC, avg_economy_rate ASC;""",
        "chart_type": "scatter_bowling"
    },
    {
        "id": 15,
        "level": "Intermediate",
        "title": "Clutch Performers in Close Matches",
        "problem": "Identify players who perform exceptionally well in close matches (< 50 runs OR < 5 wickets). Calculate average runs, close matches played, and how many close matches team won.",
        "concepts": "Compound boolean logic in WHERE clause, conditional SUM for wins",
        "tables": "player_match_performances, players, matches",
        "query": """SELECT 
    p.full_name AS player_name,
    COUNT(pmp.match_id) AS close_matches_played,
    ROUND(AVG(pmp.runs_scored), 2) AS avg_runs_close_matches,
    SUM(CASE WHEN m.winning_team_id = pmp.team_id THEN 1 ELSE 0 END) AS close_match_wins_when_batted
FROM player_match_performances pmp
JOIN players p ON pmp.player_id = p.player_id
JOIN matches m ON pmp.match_id = m.match_id
WHERE (m.victory_type = 'runs' AND m.victory_margin < 50)
   OR (m.victory_type = 'wickets' AND m.victory_margin < 5)
GROUP BY p.player_id, p.full_name
HAVING COUNT(pmp.match_id) >= 3
ORDER BY avg_runs_close_matches DESC;""",
        "chart_type": "bar_clutch"
    },
    {
        "id": 16,
        "level": "Intermediate",
        "title": "Batting Evolution Over Years (Since 2020)",
        "problem": "Track how players' batting performance changes over different years. For matches since 2020, show average runs per match and average strike rate for each year (>= 5 matches/year).",
        "concepts": "Temporal grouping by year strftime('%Y', match_date), HAVING filter",
        "tables": "player_match_performances, players, matches",
        "query": """SELECT 
    p.full_name AS player_name,
    strftime('%Y', m.match_date) AS match_year,
    COUNT(pmp.match_id) AS matches_played,
    ROUND(AVG(pmp.runs_scored), 2) AS avg_runs_per_match,
    ROUND(AVG(pmp.strike_rate), 2) AS avg_strike_rate
FROM player_match_performances pmp
JOIN players p ON pmp.player_id = p.player_id
JOIN matches m ON pmp.match_id = m.match_id
WHERE strftime('%Y', m.match_date) >= '2020'
GROUP BY p.player_id, match_year
HAVING COUNT(pmp.match_id) >= 5
ORDER BY player_name ASC, match_year DESC;""",
        "chart_type": "line_yearly"
    },

    # ------------------ ADVANCED (Q17 - Q25) ------------------
    {
        "id": 17,
        "level": "Advanced",
        "title": "Toss Decision Advantage Analytics",
        "problem": "Investigate whether winning the toss gives teams an advantage. Calculate what percentage of matches are won by the toss winner, broken down by toss decision (batting vs bowling first).",
        "concepts": "Percentage conversion, conditional aggregation, GROUP BY toss_decision",
        "tables": "matches",
        "query": """SELECT 
    toss_decision,
    COUNT(match_id) AS total_matches,
    SUM(CASE WHEN toss_winner_id = winning_team_id THEN 1 ELSE 0 END) AS matches_won_by_toss_winner,
    ROUND(SUM(CASE WHEN toss_winner_id = winning_team_id THEN 1.0 ELSE 0.0 END) * 100.0 / COUNT(match_id), 2) AS win_percentage
FROM matches
WHERE toss_decision IS NOT NULL AND winning_team_id IS NOT NULL
GROUP BY toss_decision;""",
        "chart_type": "bar_toss"
    },
    {
        "id": 18,
        "level": "Advanced",
        "title": "Most Economical Bowlers in Limited-Overs",
        "problem": "Find the most economical bowlers in limited-overs cricket (ODI and T20). Calculate overall economy rate and wickets taken (>= 10 matches, >= 2 overs/match on avg).",
        "concepts": "NULLIF division safeguard, multi-aggregate filtering in HAVING",
        "tables": "player_match_performances, players, matches",
        "query": """SELECT 
    p.full_name AS bowler_name,
    COUNT(DISTINCT pmp.match_id) AS matches_bowled,
    ROUND(SUM(pmp.runs_conceded * 1.0) / NULLIF(SUM(pmp.overs_bowled), 0), 2) AS overall_economy_rate,
    SUM(pmp.wickets_taken) AS total_wickets
FROM player_match_performances pmp
JOIN players p ON pmp.player_id = p.player_id
JOIN matches m ON pmp.match_id = m.match_id
WHERE m.format IN ('ODI', 'T20I') AND pmp.overs_bowled > 0
GROUP BY p.player_id, p.full_name
HAVING COUNT(DISTINCT pmp.match_id) >= 10 AND AVG(pmp.overs_bowled) >= 2.0
ORDER BY overall_economy_rate ASC;""",
        "chart_type": "scatter_econ"
    },
    {
        "id": 19,
        "level": "Advanced",
        "title": "Batsmen Consistency & Standard Deviation",
        "problem": "Determine which batsmen are most consistent in their scoring. Calculate average runs and standard deviation of runs for players who faced >= 10 balls per innings since 2022.",
        "concepts": "Common Table Expressions (CTE), Window Function AVG() OVER(), variance calculation",
        "tables": "player_match_performances, players, matches",
        "query": """WITH BatsmanStats AS (
    SELECT 
        p.player_id,
        p.full_name AS batsman_name,
        pmp.runs_scored,
        AVG(pmp.runs_scored) OVER(PARTITION BY p.player_id) AS avg_runs
    FROM player_match_performances pmp
    JOIN players p ON pmp.player_id = p.player_id
    JOIN matches m ON pmp.match_id = m.match_id
    WHERE pmp.balls_faced >= 10 AND m.match_date >= '2022-01-01'
)
SELECT 
    batsman_name,
    ROUND(AVG(runs_scored), 2) AS average_runs,
    ROUND(SQRT(AVG((runs_scored - avg_runs) * (runs_scored - avg_runs))), 2) AS run_std_dev,
    COUNT(*) AS innings_counted
FROM BatsmanStats
GROUP BY player_id, batsman_name
HAVING COUNT(*) >= 5
ORDER BY run_std_dev ASC, average_runs DESC;""",
        "chart_type": "scatter_consistency"
    },
    {
        "id": 20,
        "level": "Advanced",
        "title": "All-Format Veteran Breakdown (>= 20 Matches)",
        "problem": "Analyze how many matches each player has played in different cricket formats and their batting average in each format for players with at least 20 total career matches.",
        "concepts": "Pivoting rows into columns with conditional MAX(CASE WHEN), HAVING filter",
        "tables": "players, player_format_stats",
        "query": """SELECT 
    p.full_name AS player_name,
    COALESCE(MAX(CASE WHEN pfs.format = 'Test' THEN pfs.matches END), 0) AS test_matches,
    COALESCE(MAX(CASE WHEN pfs.format = 'Test' THEN pfs.batting_average END), 0.0) AS test_batting_avg,
    COALESCE(MAX(CASE WHEN pfs.format = 'ODI' THEN pfs.matches END), 0) AS odi_matches,
    COALESCE(MAX(CASE WHEN pfs.format = 'ODI' THEN pfs.batting_average END), 0.0) AS odi_batting_avg,
    COALESCE(MAX(CASE WHEN pfs.format = 'T20I' THEN pfs.matches END), 0) AS t20i_matches,
    COALESCE(MAX(CASE WHEN pfs.format = 'T20I' THEN pfs.batting_average END), 0.0) AS t20i_batting_avg,
    SUM(pfs.matches) AS total_career_matches
FROM players p
JOIN player_format_stats pfs ON p.player_id = pfs.player_id
GROUP BY p.player_id, p.full_name
HAVING SUM(pfs.matches) >= 20
ORDER BY total_career_matches DESC;""",
        "chart_type": "table"
    },
    {
        "id": 21,
        "level": "Advanced",
        "title": "Multi-Dimensional Player Ranking System",
        "problem": "Create a comprehensive performance ranking system combining batting, bowling, and fielding into a single weighted score per format: Batting: (runs*0.01 + avg*0.5 + sr*0.3), Bowling: (wkts*2 + (50-avg)*0.5 + (6-econ)*2), Fielding: (catches*3 + stumpings*5).",
        "concepts": "Window Function RANK() OVER(PARTITION BY format ORDER BY points), weighted arithmetic scoring",
        "tables": "player_format_stats, players",
        "query": """SELECT 
    p.full_name AS player_name,
    pfs.format,
    ROUND((pfs.runs * 0.01) + (pfs.batting_average * 0.5) + (pfs.strike_rate * 0.3), 2) AS batting_points,
    ROUND((pfs.wickets * 2.0) + ((50.0 - pfs.bowling_average) * 0.5) + ((6.0 - pfs.economy_rate) * 2.0), 2) AS bowling_points,
    ROUND((pfs.catches * 3.0) + (pfs.stumpings * 5.0), 2) AS fielding_points,
    ROUND(
        ((pfs.runs * 0.01) + (pfs.batting_average * 0.5) + (pfs.strike_rate * 0.3)) +
        ((pfs.wickets * 2.0) + ((50.0 - pfs.bowling_average) * 0.5) + ((6.0 - pfs.economy_rate) * 2.0)) +
        ((pfs.catches * 3.0) + (pfs.stumpings * 5.0)), 2
    ) AS total_score,
    RANK() OVER (PARTITION BY pfs.format ORDER BY 
        ((pfs.runs * 0.01) + (pfs.batting_average * 0.5) + (pfs.strike_rate * 0.3)) +
        ((pfs.wickets * 2.0) + ((50.0 - pfs.bowling_average) * 0.5) + ((6.0 - pfs.economy_rate) * 2.0)) +
        ((pfs.catches * 3.0) + (pfs.stumpings * 5.0)) DESC
    ) AS format_rank
FROM player_format_stats pfs
JOIN players p ON pfs.player_id = p.player_id
ORDER BY pfs.format, format_rank ASC;""",
        "chart_type": "bar_ranking"
    },
    {
        "id": 22,
        "level": "Advanced",
        "title": "Head-to-Head Team Match Predictions",
        "problem": "Build a head-to-head match prediction analysis between teams that played at least 5 matches against each other in the last 3 years: total matches, wins, avg victory margin, and win percentage.",
        "concepts": "Symmetric pair canonicalization with CASE expressions, subqueries in aggregation",
        "tables": "matches, teams",
        "query": """SELECT 
    CASE WHEN t1.team_name < t2.team_name THEN t1.team_name ELSE t2.team_name END AS team_a,
    CASE WHEN t1.team_name < t2.team_name THEN t2.team_name ELSE t1.team_name END AS team_b,
    COUNT(m.match_id) AS total_head_to_head_matches,
    SUM(CASE WHEN m.winning_team_id = (SELECT team_id FROM teams WHERE team_name = CASE WHEN t1.team_name < t2.team_name THEN t1.team_name ELSE t2.team_name END) THEN 1 ELSE 0 END) AS wins_team_a,
    SUM(CASE WHEN m.winning_team_id = (SELECT team_id FROM teams WHERE team_name = CASE WHEN t1.team_name < t2.team_name THEN t2.team_name ELSE t1.team_name END) THEN 1 ELSE 0 END) AS wins_team_b,
    ROUND(AVG(m.victory_margin), 1) AS avg_victory_margin,
    ROUND(SUM(CASE WHEN m.winning_team_id = (SELECT team_id FROM teams WHERE team_name = CASE WHEN t1.team_name < t2.team_name THEN t1.team_name ELSE t2.team_name END) THEN 1.0 ELSE 0.0 END) * 100.0 / COUNT(m.match_id), 1) AS team_a_win_pct
FROM matches m
JOIN teams t1 ON m.team1_id = t1.team_id
JOIN teams t2 ON m.team2_id = t2.team_id
WHERE m.match_date >= DATE('now', '-3 years')
GROUP BY team_a, team_b
HAVING COUNT(m.match_id) >= 5
ORDER BY total_head_to_head_matches DESC;""",
        "chart_type": "bar_h2h"
    },
    {
        "id": 23,
        "level": "Advanced",
        "title": "Recent Player Form & Momentum Tracker",
        "problem": "Analyze recent player form and momentum across last 10 batting performances: avg runs last 5 vs last 10, recent strike rate, 50+ scores count, and categorical form status ('Excellent Form', 'Good Form', etc.).",
        "concepts": "CTE with ROW_NUMBER() OVER(PARTITION BY player ORDER BY match_date DESC), conditional classification",
        "tables": "player_match_performances, players, matches",
        "query": """WITH RankedInnings AS (
    SELECT 
        p.player_id,
        p.full_name AS player_name,
        pmp.runs_scored,
        pmp.strike_rate,
        ROW_NUMBER() OVER (PARTITION BY p.player_id ORDER BY m.match_date DESC) AS innings_recency
    FROM player_match_performances pmp
    JOIN players p ON pmp.player_id = p.player_id
    JOIN matches m ON pmp.match_id = m.match_id
    WHERE pmp.batting_position IS NOT NULL
)
SELECT 
    player_name,
    ROUND(AVG(CASE WHEN innings_recency <= 5 THEN runs_scored END), 2) AS avg_runs_last_5,
    ROUND(AVG(CASE WHEN innings_recency <= 10 THEN runs_scored END), 2) AS avg_runs_last_10,
    ROUND(AVG(CASE WHEN innings_recency <= 5 THEN strike_rate END), 2) AS recent_strike_rate,
    SUM(CASE WHEN innings_recency <= 10 AND runs_scored >= 50 THEN 1 ELSE 0 END) AS scores_above_50_last_10,
    CASE 
        WHEN AVG(CASE WHEN innings_recency <= 5 THEN runs_scored END) >= 50 THEN 'Excellent Form'
        WHEN AVG(CASE WHEN innings_recency <= 5 THEN runs_scored END) >= 35 THEN 'Good Form'
        WHEN AVG(CASE WHEN innings_recency <= 5 THEN runs_scored END) >= 20 THEN 'Average Form'
        ELSE 'Poor Form'
    END AS current_form_status
FROM RankedInnings
WHERE innings_recency <= 10
GROUP BY player_id, player_name
HAVING COUNT(innings_recency) >= 8
ORDER BY avg_runs_last_5 DESC;""",
        "chart_type": "bar_form"
    },
    {
        "id": 24,
        "level": "Advanced",
        "title": "Batting Partnership Success Evaluation",
        "problem": "Study successful batting partnerships for pairs of consecutive batsmen with at least 5 partnerships: calculate avg partnership runs, count of 50+ stands, highest score, success rate, and rank.",
        "concepts": "Pair grouping, DENSE_RANK() OVER(ORDER BY avg runs DESC), success rate percentage",
        "tables": "partnerships, players",
        "query": """SELECT 
    p1.full_name AS batsman_1,
    p2.full_name AS batsman_2,
    COUNT(pt.partnership_id) AS total_partnerships,
    ROUND(AVG(pt.partnership_runs), 2) AS avg_partnership_runs,
    SUM(CASE WHEN pt.partnership_runs >= 50 THEN 1 ELSE 0 END) AS partnerships_above_50,
    MAX(pt.partnership_runs) AS highest_partnership_score,
    ROUND(SUM(CASE WHEN pt.partnership_runs >= 50 THEN 1.0 ELSE 0.0 END) * 100.0 / COUNT(pt.partnership_id), 1) AS success_rate_pct,
    DENSE_RANK() OVER (ORDER BY AVG(pt.partnership_runs) DESC) AS partnership_rank
FROM partnerships pt
JOIN players p1 ON pt.player1_id = p1.player_id
JOIN players p2 ON pt.player2_id = p2.player_id
WHERE ABS(pt.player1_pos - pt.player2_pos) = 1
GROUP BY pt.player1_id, pt.player2_id, p1.full_name, p2.full_name
HAVING COUNT(pt.partnership_id) >= 5
ORDER BY avg_partnership_runs DESC;""",
        "chart_type": "bar_partnerships"
    },
    {
        "id": 25,
        "level": "Advanced",
        "title": "Time-Series Career Trajectory & Trajectory Shifts",
        "problem": "Perform a time-series analysis of player performance evolution: quarterly averages for runs and strike rate, quarter-over-quarter difference using LAG(), trend identification and career phase category.",
        "concepts": "Multi-tier CTEs, Window Function LAG() OVER(PARTITION BY player ORDER BY quarter), trajectory classification",
        "tables": "player_match_performances, players, matches",
        "query": """WITH QuarterlyPlayerStats AS (
    SELECT 
        p.player_id,
        p.full_name AS player_name,
        strftime('%Y', m.match_date) || '-Q' || ((CAST(strftime('%m', m.match_date) AS INTEGER) + 2) / 3) AS quarter_year,
        COUNT(pmp.match_id) AS matches_in_quarter,
        AVG(pmp.runs_scored) AS avg_quarter_runs,
        AVG(pmp.strike_rate) AS avg_quarter_sr
    FROM player_match_performances pmp
    JOIN players p ON pmp.player_id = p.player_id
    JOIN matches m ON pmp.match_id = m.match_id
    GROUP BY p.player_id, quarter_year
),
QuarterlyDiffs AS (
    SELECT 
        player_id,
        player_name,
        quarter_year,
        matches_in_quarter,
        ROUND(avg_quarter_runs, 2) AS current_q_runs,
        ROUND(LAG(avg_quarter_runs) OVER (PARTITION BY player_id ORDER BY quarter_year), 2) AS prev_q_runs,
        ROUND(avg_quarter_runs - LAG(avg_quarter_runs) OVER (PARTITION BY player_id ORDER BY quarter_year), 2) AS quarter_run_delta,
        ROUND(avg_quarter_sr, 2) AS quarter_strike_rate
    FROM QuarterlyPlayerStats
)
SELECT 
    player_name,
    quarter_year,
    matches_in_quarter,
    current_q_runs,
    prev_q_runs,
    quarter_run_delta,
    quarter_strike_rate,
    CASE 
        WHEN quarter_run_delta > 10 THEN 'Improving'
        WHEN quarter_run_delta < -10 THEN 'Declining'
        ELSE 'Stable'
    END AS quarter_trend,
    CASE 
        WHEN current_q_runs >= 45 THEN 'Career Ascending'
        WHEN current_q_runs <= 25 THEN 'Career Declining'
        ELSE 'Career Stable'
    END AS career_phase
FROM QuarterlyDiffs
WHERE player_id IN (1, 2, 11, 13, 19)
ORDER BY player_name, quarter_year DESC;""",
        "chart_type": "line_trajectory"
    }
]


class AnalyticsService:
    """Provides methods to retrieve questions and run SQL analytics."""

    @staticmethod
    def get_all_questions() -> List[Dict[str, Any]]:
        return SQL_QUESTIONS

    @staticmethod
    def get_question_by_id(qid: int) -> Optional[Dict[str, Any]]:
        for q in SQL_QUESTIONS:
            if q["id"] == qid:
                return q
        return None

    @staticmethod
    def execute_question(qid: int) -> Dict[str, Any]:
        """Runs the query for question ID and returns dataframe, duration, and metadata."""
        q = AnalyticsService.get_question_by_id(qid)
        if not q:
            raise ValueError(f"Question ID {qid} not found.")

        start_time = time.perf_counter()
        df = execute_query(q["query"])
        duration_ms = (time.perf_counter() - start_time) * 1000

        return {
            "question": q,
            "data": df,
            "rows": len(df),
            "execution_time_ms": round(duration_ms, 2)
        }

    @staticmethod
    def execute_custom_sql(custom_sql: str) -> Dict[str, Any]:
        """Executes custom SELECT query provided by user in playground."""
        trimmed = custom_sql.strip()
        if not trimmed.upper().startswith("SELECT") and not trimmed.upper().startswith("WITH"):
            raise ValueError("Only read-only SELECT and WITH queries are permitted in the analytics playground.")

        start_time = time.perf_counter()
        df = execute_query(trimmed)
        duration_ms = (time.perf_counter() - start_time) * 1000

        return {
            "data": df,
            "rows": len(df),
            "execution_time_ms": round(duration_ms, 2)
        }

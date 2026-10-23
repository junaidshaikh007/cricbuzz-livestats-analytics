-- ====================================================================
-- Cricbuzz LiveStats - 25 Comprehensive SQL Practice Queries
-- Beginner (Q1 - Q8), Intermediate (Q9 - Q16), Advanced (Q17 - Q25)
-- ====================================================================

-- --------------------------------------------------------------------
-- BEGINNER LEVEL (Questions 1 - 8)
-- --------------------------------------------------------------------

-- Question 1: Find all players who represent India. Display their full name, playing role, batting style, and bowling style.
SELECT 
    full_name,
    playing_role,
    batting_style,
    bowling_style
FROM players
WHERE country = 'India'
ORDER BY full_name ASC;

-- Question 2: Show all cricket matches that were played in the last 30 days. Include match description, both team names, venue name with city, and match date. Sort by most recent matches first.
SELECT 
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
ORDER BY m.match_date DESC;

-- Question 3: List the top 10 highest run scorers in ODI cricket. Show player name, total runs scored, batting average, and number of centuries. Display highest run scorer first.
SELECT 
    p.full_name AS player_name,
    pfs.runs AS total_runs,
    pfs.batting_average,
    pfs.centuries
FROM player_format_stats pfs
JOIN players p ON pfs.player_id = p.player_id
WHERE pfs.format = 'ODI'
ORDER BY pfs.runs DESC
LIMIT 10;

-- Question 4: Display all cricket venues that have a seating capacity of more than 50,000 spectators. Show venue name, city, country, and capacity. Order by largest capacity first.
SELECT 
    venue_name,
    city,
    country,
    capacity
FROM venues
WHERE capacity > 50000
ORDER BY capacity DESC;

-- Question 5: Calculate how many matches each team has won. Show team name and total number of wins. Display teams with most wins first.
SELECT 
    t.team_name,
    COUNT(m.match_id) AS total_wins
FROM teams t
LEFT JOIN matches m ON t.team_id = m.winning_team_id
GROUP BY t.team_id, t.team_name
ORDER BY total_wins DESC;

-- Question 6: Count how many players belong to each playing role (like Batsman, Bowler, All-rounder, Wicket-keeper). Show the role and count of players for each role.
SELECT 
    playing_role,
    COUNT(player_id) AS total_players
FROM players
GROUP BY playing_role
ORDER BY total_players DESC;

-- Question 7: Find the highest individual batting score achieved in each cricket format (Test, ODI, T20I). Display format and highest score.
SELECT 
    format,
    MAX(highest_score) AS highest_individual_score
FROM player_format_stats
GROUP BY format
ORDER BY highest_individual_score DESC;

-- Question 8: Show all cricket series that started in the year 2024. Include series name, host country, match type, start date, and total number of matches planned.
SELECT 
    series_name,
    host_country,
    match_type,
    start_date,
    total_matches
FROM series
WHERE strftime('%Y', start_date) = '2024'
ORDER BY start_date ASC;

-- --------------------------------------------------------------------
-- INTERMEDIATE LEVEL (Questions 9 - 16)
-- --------------------------------------------------------------------

-- Question 9: Find all-rounder players who have scored more than 1000 runs AND taken more than 50 wickets in their career. Display player name, total runs, total wickets, and cricket format.
SELECT 
    p.full_name AS player_name,
    pfs.format,
    pfs.runs AS total_runs,
    pfs.wickets AS total_wickets
FROM player_format_stats pfs
JOIN players p ON pfs.player_id = p.player_id
WHERE p.playing_role = 'All-rounder' 
  AND pfs.runs > 1000 
  AND pfs.wickets > 50
ORDER BY pfs.runs DESC;

-- Question 10: Get details of the last 20 completed matches. Show match description, both team names, winning team, victory margin, victory type (runs/wickets), and venue name. Display most recent matches first.
SELECT 
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
LIMIT 20;

-- Question 11: Compare each player's performance across different cricket formats. For players who have played at least 2 different formats, show their total runs in Test, ODI, and T20I, along with overall batting average.
SELECT 
    p.full_name AS player_name,
    COALESCE(SUM(CASE WHEN pfs.format = 'Test' THEN pfs.runs END), 0) AS test_runs,
    COALESCE(SUM(CASE WHEN pfs.format = 'ODI' THEN pfs.runs END), 0) AS odi_runs,
    COALESCE(SUM(CASE WHEN pfs.format = 'T20I' THEN pfs.runs END), 0) AS t20i_runs,
    ROUND(SUM(pfs.runs * 1.0) / NULLIF(SUM(CASE WHEN pfs.batting_average > 0 THEN pfs.runs / pfs.batting_average ELSE 1 END), 0), 2) AS overall_batting_avg
FROM players p
JOIN player_format_stats pfs ON p.player_id = pfs.player_id
GROUP BY p.player_id, p.full_name
HAVING COUNT(DISTINCT pfs.format) >= 2
ORDER BY (test_runs + odi_runs + t20i_runs) DESC;

-- Question 12: Analyze each international team's performance when playing at home versus playing away. Count wins for each team in both home and away conditions.
SELECT 
    t.team_name,
    SUM(CASE WHEN v.country = t.country AND m.winning_team_id = t.team_id THEN 1 ELSE 0 END) AS home_wins,
    SUM(CASE WHEN v.country != t.country AND m.winning_team_id = t.team_id THEN 1 ELSE 0 END) AS away_wins,
    COUNT(CASE WHEN m.winning_team_id = t.team_id THEN 1 END) AS total_wins
FROM teams t
JOIN matches m ON t.team_id = m.team1_id OR t.team_id = m.team2_id
JOIN venues v ON m.venue_id = v.venue_id
GROUP BY t.team_id, t.team_name
ORDER BY total_wins DESC;

-- Question 13: Identify batting partnerships where two consecutive batsmen (batting positions next to each other) scored a combined total of 100 or more runs in the same innings.
SELECT 
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
ORDER BY pt.partnership_runs DESC;

-- Question 14: Examine bowling performance at different venues. For bowlers who have played at least 3 matches at the same venue, calculate their average economy rate, total wickets taken, and number of matches played at each venue (bowled >= 4 overs).
SELECT 
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
ORDER BY total_wickets DESC, avg_economy_rate ASC;

-- Question 15: Identify players who perform exceptionally well in close matches (decided by less than 50 runs OR less than 5 wickets). Calculate average runs, close matches played, and how many close matches team won when they batted.
SELECT 
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
ORDER BY avg_runs_close_matches DESC;

-- Question 16: Track how players' batting performance changes over different years. For matches since 2020, show each player's average runs per match and average strike rate for each year (at least 5 matches in that year).
SELECT 
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
ORDER BY player_name ASC, match_year DESC;

-- --------------------------------------------------------------------
-- ADVANCED LEVEL (Questions 17 - 25)
-- --------------------------------------------------------------------

-- Question 17: Investigate whether winning the toss gives teams an advantage in winning matches. Calculate percentage of matches won by toss winner, broken down by toss decision (bat vs bowl).
SELECT 
    toss_decision,
    COUNT(match_id) AS total_matches,
    SUM(CASE WHEN toss_winner_id = winning_team_id THEN 1 ELSE 0 END) AS matches_won_by_toss_winner,
    ROUND(SUM(CASE WHEN toss_winner_id = winning_team_id THEN 1.0 ELSE 0.0 END) * 100.0 / COUNT(match_id), 2) AS win_percentage
FROM matches
WHERE toss_decision IS NOT NULL AND winning_team_id IS NOT NULL
GROUP BY toss_decision;

-- Question 18: Find the most economical bowlers in limited-overs cricket (ODI and T20 formats). Calculate overall economy rate and total wickets taken (bowled in >= 10 matches and >= 2 overs per match on avg).
SELECT 
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
ORDER BY overall_economy_rate ASC;

-- Question 19: Determine which batsmen are most consistent in their scoring. Calculate average runs and standard deviation of runs for players who faced >= 10 balls per innings since 2022.
WITH BatsmanStats AS (
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
ORDER BY run_std_dev ASC, average_runs DESC;

-- Question 20: Analyze how many matches each player has played in different cricket formats and their batting average in each format (at least 20 total matches across all formats).
SELECT 
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
ORDER BY total_career_matches DESC;

-- Question 21: Comprehensive performance ranking system combining batting, bowling, and fielding into a single weighted score per format.
SELECT 
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
ORDER BY pfs.format, format_rank ASC;

-- Question 22: Build a head-to-head match prediction analysis between teams that have played at least 5 matches against each other in the last 3 years.
SELECT 
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
ORDER BY total_head_to_head_matches DESC;

-- Question 23: Analyze recent player form and momentum (last 10 batting performances: avg last 5 vs last 10, strike rate trends, 50+ scores count, form categorization).
WITH RankedInnings AS (
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
ORDER BY avg_runs_last_5 DESC;

-- Question 24: Study successful batting partnerships to identify best player combinations (pairs batting together as consecutive batsmen in at least 5 partnerships).
SELECT 
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
ORDER BY avg_partnership_runs DESC;

-- Question 25: Time-series analysis of player performance evolution: quarterly averages for runs and strike rate, quarter-over-quarter comparison, career trajectory categorization.
WITH QuarterlyPlayerStats AS (
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
ORDER BY player_name, quarter_year DESC;

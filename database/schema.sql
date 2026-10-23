-- ====================================================================
-- Cricbuzz LiveStats - Database Schema
-- Supports relational integrity, indexes, and full 25 SQL queries
-- ====================================================================

-- 1. Teams Table
CREATE TABLE IF NOT EXISTS teams (
    team_id INTEGER PRIMARY KEY AUTOINCREMENT,
    team_name TEXT NOT NULL UNIQUE,
    country TEXT NOT NULL,
    code TEXT NOT NULL UNIQUE
);

-- 2. Venues Table
CREATE TABLE IF NOT EXISTS venues (
    venue_id INTEGER PRIMARY KEY AUTOINCREMENT,
    venue_name TEXT NOT NULL,
    city TEXT NOT NULL,
    country TEXT NOT NULL,
    capacity INTEGER NOT NULL DEFAULT 25000
);

-- 3. Series Table
CREATE TABLE IF NOT EXISTS series (
    series_id INTEGER PRIMARY KEY AUTOINCREMENT,
    series_name TEXT NOT NULL,
    host_country TEXT NOT NULL,
    match_type TEXT NOT NULL, -- 'Test', 'ODI', 'T20I', 'Multi-Format'
    start_date DATE NOT NULL,
    end_date DATE NOT NULL,
    total_matches INTEGER NOT NULL DEFAULT 1
);

-- 4. Players Table
CREATE TABLE IF NOT EXISTS players (
    player_id INTEGER PRIMARY KEY AUTOINCREMENT,
    full_name TEXT NOT NULL,
    country TEXT NOT NULL,
    playing_role TEXT NOT NULL, -- 'Batsman', 'Bowler', 'All-rounder', 'Wicket-keeper'
    batting_style TEXT NOT NULL, -- 'Right-hand bat', 'Left-hand bat'
    bowling_style TEXT NOT NULL, -- 'Right-arm fast', 'Slow left-arm orthodox', etc.
    dob DATE,
    is_active INTEGER DEFAULT 1
);

-- 5. Matches Table
CREATE TABLE IF NOT EXISTS matches (
    match_id INTEGER PRIMARY KEY AUTOINCREMENT,
    series_id INTEGER,
    match_description TEXT NOT NULL,
    team1_id INTEGER NOT NULL,
    team2_id INTEGER NOT NULL,
    venue_id INTEGER NOT NULL,
    match_date DATE NOT NULL,
    format TEXT NOT NULL, -- 'Test', 'ODI', 'T20I'
    toss_winner_id INTEGER,
    toss_decision TEXT, -- 'Bat', 'Bowl'
    winning_team_id INTEGER,
    victory_margin INTEGER,
    victory_type TEXT, -- 'runs', 'wickets', 'tie', 'no result'
    status TEXT DEFAULT 'Completed', -- 'Scheduled', 'Live', 'Completed', 'Abandoned'
    FOREIGN KEY (series_id) REFERENCES series(series_id),
    FOREIGN KEY (team1_id) REFERENCES teams(team_id),
    FOREIGN KEY (team2_id) REFERENCES teams(team_id),
    FOREIGN KEY (venue_id) REFERENCES venues(venue_id),
    FOREIGN KEY (toss_winner_id) REFERENCES teams(team_id),
    FOREIGN KEY (winning_team_id) REFERENCES teams(team_id)
);

-- 6. Player Format Career Statistics
CREATE TABLE IF NOT EXISTS player_format_stats (
    stat_id INTEGER PRIMARY KEY AUTOINCREMENT,
    player_id INTEGER NOT NULL,
    format TEXT NOT NULL, -- 'Test', 'ODI', 'T20I'
    matches INTEGER DEFAULT 0,
    innings INTEGER DEFAULT 0,
    runs INTEGER DEFAULT 0,
    highest_score INTEGER DEFAULT 0,
    batting_average REAL DEFAULT 0.0,
    strike_rate REAL DEFAULT 0.0,
    centuries INTEGER DEFAULT 0,
    half_centuries INTEGER DEFAULT 0,
    wickets INTEGER DEFAULT 0,
    bowling_average REAL DEFAULT 0.0,
    economy_rate REAL DEFAULT 0.0,
    catches INTEGER DEFAULT 0,
    stumpings INTEGER DEFAULT 0,
    FOREIGN KEY (player_id) REFERENCES players(player_id) ON DELETE CASCADE,
    UNIQUE(player_id, format)
);

-- 7. Player Match Performances (Innings by Innings)
CREATE TABLE IF NOT EXISTS player_match_performances (
    perf_id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_id INTEGER NOT NULL,
    player_id INTEGER NOT NULL,
    team_id INTEGER NOT NULL,
    innings INTEGER NOT NULL DEFAULT 1,
    batting_position INTEGER,
    runs_scored INTEGER DEFAULT 0,
    balls_faced INTEGER DEFAULT 0,
    fours INTEGER DEFAULT 0,
    sixes INTEGER DEFAULT 0,
    strike_rate REAL DEFAULT 0.0,
    overs_bowled REAL DEFAULT 0.0,
    runs_conceded INTEGER DEFAULT 0,
    wickets_taken INTEGER DEFAULT 0,
    maiden_overs INTEGER DEFAULT 0,
    economy_rate REAL DEFAULT 0.0,
    catches INTEGER DEFAULT 0,
    stumpings INTEGER DEFAULT 0,
    FOREIGN KEY (match_id) REFERENCES matches(match_id) ON DELETE CASCADE,
    FOREIGN KEY (player_id) REFERENCES players(player_id) ON DELETE CASCADE,
    FOREIGN KEY (team_id) REFERENCES teams(team_id)
);

-- 8. Batting Partnerships Table
CREATE TABLE IF NOT EXISTS partnerships (
    partnership_id INTEGER PRIMARY KEY AUTOINCREMENT,
    match_id INTEGER NOT NULL,
    innings INTEGER NOT NULL DEFAULT 1,
    player1_id INTEGER NOT NULL,
    player2_id INTEGER NOT NULL,
    player1_pos INTEGER NOT NULL,
    player2_pos INTEGER NOT NULL,
    partnership_runs INTEGER NOT NULL,
    balls_faced INTEGER DEFAULT 0,
    FOREIGN KEY (match_id) REFERENCES matches(match_id) ON DELETE CASCADE,
    FOREIGN KEY (player1_id) REFERENCES players(player_id) ON DELETE CASCADE,
    FOREIGN KEY (player2_id) REFERENCES players(player_id) ON DELETE CASCADE
);

-- ====================================================================
-- Performance Indexes
-- ====================================================================
CREATE INDEX IF NOT EXISTS idx_matches_date ON matches(match_date);
CREATE INDEX IF NOT EXISTS idx_matches_format ON matches(format);
CREATE INDEX IF NOT EXISTS idx_players_country ON players(country);
CREATE INDEX IF NOT EXISTS idx_perf_player_match ON player_match_performances(player_id, match_id);
CREATE INDEX IF NOT EXISTS idx_perf_match_innings ON player_match_performances(match_id, innings);
CREATE INDEX IF NOT EXISTS idx_pfs_player_format ON player_format_stats(player_id, format);
CREATE INDEX IF NOT EXISTS idx_partnerships_players ON partnerships(player1_id, player2_id);

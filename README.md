# 🏏 Cricbuzz LiveStats: Real-Time Cricket Insights & SQL-Based Analytics

[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python)](https://python.org)
[![Streamlit](https://img.shields.io/badge/Streamlit-1.30%2B-FF4B4B?logo=streamlit)](https://streamlit.io)
[![SQL](https://img.shields.io/badge/SQL-SQLite%20%7C%20PostgreSQL-orange?logo=sqlite)](https://sqlite.org)
[![License](https://img.shields.io/badge/License-MIT-green)](LICENSE)

An end-to-end sports analytics web platform integrating real-time **Cricbuzz REST API** telemetry with a normalized **SQL database** engine. Delivers real-time ball-by-ball match updates, multi-format player statistics, 25 advanced SQL analytical queries with dynamic visualizations, and full CRUD administrative operations.

---

## 🚀 Live Local URL
Access the running dashboard locally at:
👉 **[http://localhost:8501](http://localhost:8501)**

---

## 🌟 Key Features

### 1. ⚡ Real-Time Live Match Telemetry (`/pages/1_⚡_Live_Matches.py`)
- Instant live scorecards, innings run rate, current run rate (CRR), and required run rate (RRR).
- Batsmen tracking (strike rates, boundaries, active striker badge).
- Bowler analytics (overs, maidens, wickets, economy).
- Live ball-by-ball colored badge tracker and real-time commentary feed.
- Innings progression & worm comparison chart.

### 2. 📊 Top Player Statistics & Radar Matrix (`/pages/2_📊_Top_Player_Stats.py`)
- Multi-format leaderboards (Test, ODI, T20I) for most runs, centuries, wickets, best averages, and economy rates.
- **Head-to-Head Radar Comparison**: Compare two players across 6 dimensions simultaneously.
- **Player Dossier**: Deep dive into individual player career profiles.

### 3. 🔍 25-Question SQL Analytical Engine (`/pages/3_🔍_SQL_Analytics.py`)
- Complete solution suite for **25 SQL practice questions** organized across 3 difficulty tiers:
  - **Beginner (Q1–Q8):** Filtering, multi-table joins, aggregates (`COUNT`, `MAX`), string formatting.
  - **Intermediate (Q9–Q16):** Multi-conditional filters, format pivots, clutch analysis, yearly grouping.
  - **Advanced (Q17–Q25):** Window functions (`RANK()`, `ROW_NUMBER()`, `LAG()`), CTEs, toss advantage calculation, standard deviation scoring, and career trajectory classification.
- Interactive SQL Query Runner & Custom SQL Playground with CSV export.

### 4. 🛠️ Administrative CRUD Operations (`/pages/4_🛠️_CRUD_Operations.py`)
- **Player Management**: Form-based creation, profile editing, and safe cascading deletion.
- **Match Management**: Schedule and log match outcomes, victory margins, toss results, and venues.

### 5. ⚙️ System Settings & Data Export (`/pages/5_⚙️_Settings.py`)
- RapidAPI Cricbuzz credentials configuration with live latency test.
- One-click database factory reset & seeder.
- Single-click CSV data export for all tables.

---

## 📁 Project Architecture

```
project/
├── app.py                      # Main Streamlit application & home page
├── config.py                   # Global configuration, constants & color palette
├── requirements.txt            # Python dependencies
├── README.md                   # Complete documentation
│
├── api/
│   ├── cricbuzz_api.py         # Cricbuzz REST API client with RapidAPI support
│   └── mock_data.py            # High-fidelity live fallback telemetry engine
│
├── database/
│   ├── db_connection.py        # SQLite connection pooling & query executor
│   ├── schema.sql              # Normalized relational schema with indexes
│   ├── seed_data.py            # Authentic cricket database seeder
│   └── cricbuzz.db             # Pre-seeded SQLite database
│
├── services/
│   ├── analytics_service.py    # 25 SQL queries repository & execution plan
│   └── crud_service.py         # Transactional CRUD business logic
│
├── pages/
│   ├── 1_⚡_Live_Matches.py    # Live scorecards & ball commentary
│   ├── 2_📊_Top_Player_Stats.py# Leaderboards & radar comparisons
│   ├── 3_🔍_SQL_Analytics.py   # 25 SQL queries & interactive playground
│   ├── 4_🛠️_CRUD_Operations.py # Player & match management
│   └── 5_⚙️_Settings.py        # API configuration & DB controls
│
├── utils/
│   ├── helpers.py              # CSS injectors & metric card formatters
│   └── visualization.py        # Dark theme Plotly chart generators
│
├── sql/
│   └── queries_25.sql          # All 25 standalone SQL queries
│
└── tests/
    └── test_cricbuzz.py        # Automated test suite (100% pass)
```

---

## 🛠️ Installation & Setup

1. **Clone the repository:**
   ```bash
   git clone https://github.com/<your-username>/cricbuzz-livestats-analytics.git
   cd cricbuzz-livestats-analytics
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Initialize the database:**
   ```bash
   python database/seed_data.py
   ```

4. **Launch the application:**
   ```bash
   streamlit run app.py
   ```

5. **Open in browser:**
   ```
   http://localhost:8501
   ```

---

## 🧪 Automated Testing
Run the automated test suite verifying database integrity, CRUD operations, all 25 SQL queries, and API fallback:
```bash
python -m unittest tests/test_cricbuzz.py
```

---

## 📜 25 SQL Practice Questions Overview

| # | Tier | Title | Key SQL Concepts |
|---|---|---|---|
| Q1 | Beginner | Indian National Team Roster | `SELECT`, `WHERE`, `ORDER BY` |
| Q2 | Beginner | Matches Played in Last 30 Days | Multi-table `JOIN`, `DATE('now', '-30 days')` |
| Q3 | Beginner | Top 10 ODI Run Scorers | `JOIN`, `ORDER BY DESC`, `LIMIT 10` |
| Q4 | Beginner | Stadiums with >50,000 Capacity | Numerical filtering, `ORDER BY` |
| Q5 | Beginner | Total Match Wins by Team | `LEFT JOIN`, `COUNT()`, `GROUP BY` |
| Q6 | Beginner | Player Playing Role Distribution | `GROUP BY`, `COUNT(player_id)` |
| Q7 | Beginner | Format-wise Highest Individual Score | `MAX(highest_score)`, `GROUP BY format` |
| Q8 | Beginner | Series Starting in 2024 | `strftime('%Y', start_date) = '2024'` |
| Q9 | Intermediate | All-Rounders (>1000 Runs & >50 Wickets) | Multi-column filter `AND`, `JOIN` |
| Q10 | Intermediate | Last 20 Completed Matches | String concatenation `||`, `LIMIT 20` |
| Q11 | Intermediate | Cross-Format Performance Matrix | Conditional aggregation `CASE WHEN`, `HAVING` |
| Q12 | Intermediate | Home vs Away Win Analysis | Conditional `CASE` matching venue vs team country |
| Q13 | Intermediate | Adjacent Batsmen Century Partnerships | `ABS(pos1 - pos2) = 1`, `WHERE runs >= 100` |
| Q14 | Intermediate | Venue Bowling Performance Analysis | Multi-column `GROUP BY`, `AVG(economy_rate)` |
| Q15 | Intermediate | Clutch Performers in Close Matches | Compound boolean logic (`<50 runs` OR `<5 wkts`) |
| Q16 | Intermediate | Annual Batting Evolution (Since 2020) | Temporal grouping `strftime('%Y')`, `HAVING` |
| Q17 | Advanced | Toss Decision Advantage Analytics | Percentage win rate calculation by toss decision |
| Q18 | Advanced | Limited-Overs Economical Bowlers | Division safeguard `NULLIF()`, `HAVING` |
| Q19 | Advanced | Batsmen Scoring Consistency & Std Dev | Common Table Expressions (CTE), `AVG() OVER()` |
| Q20 | Advanced | Format Breakdown for Veterans (>=20 Matches)| Cross-tabulation pivot `MAX(CASE WHEN)` |
| Q21 | Advanced | Multi-Dimensional Player Ranking Score | Weighted scoring formula, `RANK() OVER()` |
| Q22 | Advanced | Head-to-Head Match Predictions | Canonical team pairing `CASE WHEN`, subqueries |
| Q23 | Advanced | Recent Form & Momentum Classification | `ROW_NUMBER() OVER()`, categorical form rules |
| Q24 | Advanced | Consecutive Partnership Success Ranking | `DENSE_RANK() OVER()`, success rate percentage |
| Q25 | Advanced | Time-Series Career Trajectory & Shifts | Multi-tier CTEs, `LAG() OVER()`, quarter diffs |

---

## 📄 License
This project is open-source and available under the [MIT License](LICENSE).

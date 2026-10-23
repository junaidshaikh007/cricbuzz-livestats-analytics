"""
Database Connection and Query Execution Module
Provides centralized SQLite connection handling, safe parameter binding,
transaction management, and DataFrame integration for Cricbuzz LiveStats.
"""

import sqlite3
import pandas as pd
from typing import Optional, Tuple, Any, List, Dict
import logging
from pathlib import Path
import sys

# Add root directory
BASE_DIR = Path(__file__).resolve().parent.parent
sys.path.append(str(BASE_DIR))
import config

logger = logging.getLogger("CricbuzzDB")
logging.basicConfig(level=logging.INFO)


def get_connection(db_path: Optional[str] = None) -> sqlite3.Connection:
    """Creates and returns a connection to the SQLite database."""
    target_path = db_path or str(config.DATABASE_PATH)
    conn = sqlite3.connect(target_path, check_same_thread=False)
    conn.row_factory = sqlite3.Row
    # Enable foreign keys
    conn.execute("PRAGMA foreign_keys = ON;")
    return conn


def execute_query(sql: str, params: Optional[Tuple[Any, ...]] = None) -> pd.DataFrame:
    """
    Executes a SELECT SQL query and returns results as a pandas DataFrame.
    Gracefully handles exceptions and logs queries.
    """
    conn = get_connection()
    try:
        if params:
            df = pd.read_sql_query(sql, conn, params=params)
        else:
            df = pd.read_sql_query(sql, conn)
        return df
    except Exception as e:
        logger.error(f"Error executing query: {sql}\nError: {e}")
        raise e
    finally:
        conn.close()


def execute_statement(sql: str, params: Optional[Tuple[Any, ...]] = None) -> int:
    """
    Executes an INSERT, UPDATE, or DELETE SQL statement within a transaction.
    Returns the lastrowid for INSERT or rowcount for UPDATE/DELETE.
    """
    conn = get_connection()
    try:
        cursor = conn.cursor()
        if params:
            cursor.execute(sql, params)
        else:
            cursor.execute(sql)
        conn.commit()
        return cursor.lastrowid if cursor.lastrowid else cursor.rowcount
    except Exception as e:
        conn.rollback()
        logger.error(f"Database transaction error: {e}")
        raise e
    finally:
        conn.close()


def get_database_stats() -> Dict[str, int]:
    """Returns total counts of players, matches, venues, and teams in the database."""
    conn = get_connection()
    stats = {}
    try:
        cursor = conn.cursor()
        for tbl in ["players", "matches", "venues", "teams", "series"]:
            cursor.execute(f"SELECT COUNT(*) FROM {tbl}")
            stats[tbl] = cursor.fetchone()[0]
        return stats
    finally:
        conn.close()


def get_table_names() -> List[str]:
    """Returns all user table names in the database."""
    conn = get_connection()
    try:
        cursor = conn.cursor()
        cursor.execute("SELECT name FROM sqlite_master WHERE type='table' AND name NOT LIKE 'sqlite_%';")
        return [row[0] for row in cursor.fetchall()]
    finally:
        conn.close()


def get_table_schema(table_name: str) -> pd.DataFrame:
    """Returns the column definitions for a given table."""
    conn = get_connection()
    try:
        return pd.read_sql_query(f"PRAGMA table_info({table_name});", conn)
    finally:
        conn.close()


def reseed_database() -> bool:
    """Resets and reseeds database with fresh sample data."""
    try:
        from database.seed_data import seed_database
        seed_database()
        return True
    except Exception as e:
        logger.error(f"Failed to reseed database: {e}")
        return False

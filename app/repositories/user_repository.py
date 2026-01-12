"""
user_repository.py
Akses database user (SQLite)
"""

import sqlite3
from typing import Optional

from core.cms_bash_folder import DB_PATH
from app.models.user_model import User


def _get_db():
    return sqlite3.connect(DB_PATH)


def init_user_table():
    conn = _get_db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS users (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        username TEXT UNIQUE NOT NULL,
        password_hash TEXT NOT NULL,
        role TEXT NOT NULL,
        created_at TEXT NOT NULL
    )
    """)

    conn.commit()
    conn.close()


def create_user(username, password_hash, role, created_at):
    conn = _get_db()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO users (username, password_hash, role, created_at)
        VALUES (?, ?, ?, ?)
        """,
        (username, password_hash, role, created_at)
    )

    conn.commit()
    conn.close()


def get_user_by_username(username) -> Optional[User]:
    conn = _get_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT id, username, password_hash, role, created_at FROM users WHERE username = ?",
        (username,)
    )

    row = cur.fetchone()
    conn.close()

    if not row:
        return None

    return User(*row)
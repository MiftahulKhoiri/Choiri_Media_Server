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
      must_change_password INTEGER DEFAULT 0,
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

def list_users():
    conn = _get_db()
    cur = conn.cursor()
    cur.execute(
        "SELECT id, username, role, must_change_password FROM users"
    )
    rows = cur.fetchall()
    conn.close()
    return rows


def delete_user(username):
    conn = _get_db()
    cur = conn.cursor()
    cur.execute(
        "DELETE FROM users WHERE username = ? AND username != 'root'",
        (username,)
    )
    conn.commit()
    conn.close()


def update_user_role(username, role):
    conn = _get_db()
    cur = conn.cursor()
    cur.execute(
        "UPDATE users SET role = ? WHERE username = ?",
        (role, username)
    )
    conn.commit()
    conn.close()


def update_password(username, password_hash, force_change=0):
    conn = _get_db()
    cur = conn.cursor()
    cur.execute(
        """
        UPDATE users
        SET password_hash = ?, must_change_password = ?
        WHERE username = ?
        """,
        (password_hash, force_change, username)
    )
    conn.commit()
    conn.close()
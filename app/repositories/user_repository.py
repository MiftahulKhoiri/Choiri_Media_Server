"""
user_repository.py
Akses database user (SQLite)
"""

import sqlite3
from typing import Optional

from core.cms_bash_folder import DB_PATH
from app.models.user_model import User
from app.repositories.db import get_db


# =====================================================
# DB HELPER
# =====================================================



# =====================================================
# INIT TABLE
# =====================================================

def init_user_table():
    conn = get_db()
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
    migrate_users_table()

# =====================================================
# CREATE USER
# =====================================================

def create_user(
    username,
    password_hash,
    role,
    created_at,
    must_change_password=0
):
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO users
        (username, password_hash, role, must_change_password, created_at)
        VALUES (?, ?, ?, ?, ?)
        """,
        (
            username,
            password_hash,
            role,
            must_change_password,
            created_at
        )
    )

    conn.commit()
    conn.close()


# =====================================================
# GET USER
# =====================================================

def get_user_by_username(username):
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT
            id,
            username,
            password_hash,
            role,
            is_active,
            must_change_password,
            created_at
        FROM users
        WHERE username = ?
        """,
        (username,)
    )

    row = cur.fetchone()
    conn.close()

    if not row:
        return None

    return User(*row)


# =====================================================
# LIST / UPDATE / DELETE / migration 
# =====================================================

def list_users():
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT id, username, role, must_change_password FROM users"
    )
    rows = cur.fetchall()

    conn.close()
    return rows


def delete_user(username):
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "DELETE FROM users WHERE username = ? AND username != 'root'",
        (username,)
    )

    conn.commit()
    conn.close()


def update_user_role(username, role):
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        "UPDATE users SET role = ? WHERE username = ?",
        (role, username)
    )

    conn.commit()
    conn.close()


def update_password(username, password_hash, force_change=0):
    conn = get_db()
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

def set_user_active(username, active: bool):
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE users
        SET is_active = ?
        WHERE username = ?
        """,
        (1 if active else 0, username)
    )

    conn.commit()
    conn.close()

def reset_user_password(username, password_hash):
    """
    Reset password user & paksa ganti password saat login berikutnya
    """
    conn = get_db()
    cur = conn.cursor()

    cur.execute(
        """
        UPDATE users
        SET password_hash = ?, must_change_password = 1
        WHERE username = ?
        """,
        (password_hash, username)
    )

    conn.commit()
    conn.close()

def migrate_users_table():
    conn = get_db()
    cur = conn.cursor()

    cur.execute("PRAGMA table_info(users)")
    columns = [row[1] for row in cur.fetchall()]

    if "is_active" not in columns:
        cur.execute(
            "ALTER TABLE users ADD COLUMN is_active INTEGER DEFAULT 1"
        )

    if "must_change_password" not in columns:
        cur.execute(
            "ALTER TABLE users ADD COLUMN must_change_password INTEGER DEFAULT 0"
        )

    conn.commit()
    conn.close()
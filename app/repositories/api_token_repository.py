"""
api_token_repository.py
Akses database API token
"""

import sqlite3
from typing import Optional

from core.cms_bash_folder import DB_PATH


def _get_db():
    return sqlite3.connect(DB_PATH)


def init_token_table():
    conn = _get_db()
    cur = conn.cursor()

    cur.execute("""
    CREATE TABLE IF NOT EXISTS api_tokens (
        id INTEGER PRIMARY KEY AUTOINCREMENT,
        user TEXT NOT NULL,
        token_hash TEXT NOT NULL,
        created_at TEXT NOT NULL,
        revoked INTEGER DEFAULT 0
    )
    """)

    conn.commit()
    conn.close()


def save_token(user, token_hash, created_at):
    conn = _get_db()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO api_tokens (user, token_hash, created_at)
        VALUES (?, ?, ?)
        """,
        (user, token_hash, created_at)
    )

    conn.commit()
    conn.close()


def get_active_tokens(user):
    conn = _get_db()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT id, created_at FROM api_tokens
        WHERE user = ? AND revoked = 0
        """,
        (user,)
    )

    rows = cur.fetchall()
    conn.close()
    return rows


def revoke_token(token_id):
    conn = _get_db()
    cur = conn.cursor()

    cur.execute(
        "UPDATE api_tokens SET revoked = 1 WHERE id = ?",
        (token_id,)
    )

    conn.commit()
    conn.close()


def find_token_hash(token_hash) -> Optional[str]:
    conn = _get_db()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT user FROM api_tokens
        WHERE token_hash = ? AND revoked = 0
        """,
        (token_hash,)
    )

    row = cur.fetchone()
    conn.close()

    return row[0] if row else None
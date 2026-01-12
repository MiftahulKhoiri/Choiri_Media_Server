"""
auth_service.py
Business logic autentikasi CMS
"""

import os
import sqlite3
import json
from datetime import datetime

from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from flask import session

from core.cms_bash_folder import DB_PATH, DB_FOLDER


# =====================================================
# DATABASE
# =====================================================

def _get_db():
    return sqlite3.connect(DB_PATH)


def init_auth_db():
    """
    Inisialisasi tabel user (jika belum ada)
    """
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


# =====================================================
# USER MANAGEMENT
# =====================================================

def create_user(username: str, password: str, role: str = "user"):
    """
    Membuat user baru
    """
    password_hash = generate_password_hash(password)
    created_at = datetime.utcnow().isoformat()

    conn = _get_db()
    cur = conn.cursor()

    try:
        cur.execute(
            """
            INSERT INTO users (username, password_hash, role, created_at)
            VALUES (?, ?, ?, ?)
            """,
            (username, password_hash, role, created_at)
        )
        conn.commit()
    except sqlite3.IntegrityError:
        raise ValueError("Username sudah terdaftar")
    finally:
        conn.close()

    _create_user_folder(username, role)


def _create_user_folder(username: str, role: str):
    """
    Membuat folder data per user
    """
    users_dir = os.path.join(DB_FOLDER, "users")
    user_dir = os.path.join(users_dir, username)

    os.makedirs(user_dir, exist_ok=True)

    data_file = os.path.join(user_dir, "data.json")
    if not os.path.exists(data_file):
        with open(data_file, "w") as f:
            json.dump(
                {
                    "username": username,
                    "role": role,
                    "created_at": datetime.utcnow().isoformat()
                },
                f,
                indent=4
            )


# =====================================================
# AUTHENTICATION
# =====================================================

def verify_login(username: str, password: str) -> bool:
    """
    Verifikasi username & password
    """
    conn = _get_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT password_hash FROM users WHERE username = ?",
        (username,)
    )
    row = cur.fetchone()
    conn.close()

    if not row:
        return False

    return check_password_hash(row[0], password)


def login_user(username: str) -> bool:
    """
    Login user → simpan ke session
    """
    conn = _get_db()
    cur = conn.cursor()

    cur.execute(
        "SELECT role FROM users WHERE username = ?",
        (username,)
    )
    row = cur.fetchone()
    conn.close()

    if not row:
        return False

    session.clear()
    session["user"] = username
    session["role"] = row[0]
    session["logged_in"] = True
    return True


def logout_user():
    """
    Logout user (hapus session)
    """
    session.clear()


# =====================================================
# AUTH CHECK
# =====================================================

def is_logged_in() -> bool:
    return session.get("logged_in", False)


def is_root() -> bool:
    return session.get("role") == "root"


def current_user():
    return session.get("user")
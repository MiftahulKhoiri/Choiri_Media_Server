"""
auth_service.py
Business logic autentikasi
"""
import os
from datetime import datetime
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from app.repositories.user_repository import (
    init_user_table,
    create_user,
    get_user_by_username,
)

from app.services.session_service import login_session
from app.services.audit_service import log_login, log_logout
from core.cms_bash_folder import DB_FOLDER

def init_auth():
    """
    Dipanggil sekali saat app start
    """
    init_user_table()


def register_user(username, password, role="user"):
    password_hash = generate_password_hash(password)
    created_at = datetime.utcnow().isoformat()

    create_user(username, password_hash, role, created_at)


def verify_login(username, password) -> bool:
    user = get_user_by_username(username)
    if not user:
        return False

    return check_password_hash(user.password_hash, password)


def login_user(username) -> bool:
    user = get_user_by_username(username)
    if not user:
        return False

    login_session(user.username, user.role)
    log_login(user.username)
    return True

def logout_user():
    username = session.get("user")
    session.clear()
    if username:
        log_logout(username)

def bootstrap_root_user():
    """
    Membuat user root pertama (HANYA SEKALI)
    - Skip jika root sudah ada
    - Password WAJIB dari environment variable
    - Aman untuk production
    """

    # -------------------------------------------------
    # 1️⃣ SKIP JIKA ROOT SUDAH ADA (IDEMPOTENT)
    # -------------------------------------------------
    if get_user_by_username("root"):
        return

    # -------------------------------------------------
    # 2️⃣ AMBIL PASSWORD DARI ENV (BUKAN HARDCODE)
    # -------------------------------------------------
    password = os.environ.get("CMS_ROOT_PASSWORD")
    if not password:
        raise RuntimeError(
            "CMS_ROOT_PASSWORD belum diset. "
            "Set environment variable terlebih dahulu."
        )

    # -------------------------------------------------
    # 3️⃣ CREATE ROOT USER
    # -------------------------------------------------
    password_hash = generate_password_hash(password)
    created_at = datetime.utcnow().isoformat()

    create_user(
        username="root",
        password_hash=password_hash,
        role="root",
        created_at=created_at
    )

    # -------------------------------------------------
    # 4️⃣ LOG BOOTSTRAP (TANPA CETAK PASSWORD)
    # -------------------------------------------------
    print("✔ ROOT USER berhasil dibuat")
    print("⚠ Segera ganti password root setelah login pertama")
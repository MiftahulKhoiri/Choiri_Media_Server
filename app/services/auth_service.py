"""
auth_service.py
Business logic autentikasi
"""

import os
from flask import session
from datetime import datetime
from getpass import getpass
from werkzeug.security import (
    generate_password_hash,
    check_password_hash
)

from app.repositories.user_repository import (
    init_user_table,
    create_user,
    get_user_by_username,
    reset_user_password,
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

def login_user(username, ip_address=None):
    user = get_user_by_username(username)
    if not user:
        return False

    if not user.is_active:
        raise ValueError("Akun Anda telah dikunci oleh admin")

    session["logged_in"] = True
    session["username"] = user.username
    session["role"] = user.role

    log_login(user.username, ip_address)
    return True

def logout_user():
    username = session.get("user")
    session.clear()
    if username:
        log_logout(username)

def bootstrap_root_user():
    """
    Membuat user root pertama kali
    - Skip jika root sudah ada
    - Password diminta via prompt (aman)
    - Hanya dijalankan sekali
    """

    # -------------------------------------------------
    # 1️⃣ SKIP JIKA ROOT SUDAH ADA
    # -------------------------------------------------
    if get_user_by_username("root"):
        return

    print("=" * 50)
    print("⚠  ROOT USER BELUM ADA")
    print("Buat password untuk user ROOT (admin)")
    print("=" * 50)

    # -------------------------------------------------
    # 2️⃣ INPUT PASSWORD (AMAN, TIDAK TERLIHAT)
    # -------------------------------------------------
    while True:
        password = getpass("Masukkan password root: ")
        confirm = getpass("Ulangi password root   : ")

        if not password:
            print("❌ Password tidak boleh kosong")
            continue

        if password != confirm:
            print("❌ Password tidak cocok, ulangi")
            continue

        if len(password) < 8:
            print("❌ Password minimal 8 karakter")
            continue

        break

    # -------------------------------------------------
    # 3️⃣ BUAT USER ROOT
    # -------------------------------------------------
    password_hash = generate_password_hash(password)
    created_at = datetime.utcnow().isoformat()

    create_user(
       username="root",
       password_hash=password_hash,
       role="root",
       created_at=created_at,
       must_change_password=1
    )

    print("✔ ROOT USER berhasil dibuat")
    print("✔ Simpan password dengan aman")
    print("✔ Login menggunakan username: root")

def must_change_password(username):
    user = get_user_by_username(username)
    return user.must_change_password == 1


# =====================================================
# ADMIN SERVICE
# =====================================================

def create_user_by_admin(username, password, role):
    """
    Buat user oleh admin/root
    """

    if not username or not password or not role:
        raise ValueError("Semua field wajib diisi")

    if role not in ("user", "root"):
        raise ValueError("Role tidak valid")

    if len(password) < 8:
        raise ValueError("Password minimal 8 karakter")

    if get_user_by_username(username):
        raise ValueError("Username sudah ada")

    password_hash = generate_password_hash(password)
    created_at = datetime.utcnow().isoformat()

    create_user(
        username=username,
        password_hash=password_hash,
        role=role,
        created_at=created_at,
        must_change_password=1  # user WAJIB ganti password saat login pertama
    )

def reset_password_by_admin(username, new_password):
    if not new_password or len(new_password) < 8:
        raise ValueError("Password minimal 8 karakter")

    user = get_user_by_username(username)
    if not user:
        raise ValueError("User tidak ditemukan")

    if user.username == "root":
        raise ValueError("Password root tidak boleh di-reset dari sini")

    password_hash = generate_password_hash(new_password)
    reset_user_password(username, password_hash)
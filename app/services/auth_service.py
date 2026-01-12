"""
auth_service.py
Business logic autentikasi
"""

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
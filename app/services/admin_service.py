"""
admin_service.py
Business logic admin panel
"""

from datetime import datetime
from werkzeug.security import generate_password_hash

from app.repositories.user_repository import create_user, get_user_by_username


def create_user_by_admin(username, password, role):
    if get_user_by_username(username):
        raise ValueError("Username sudah ada")

    if len(password) < 8:
        raise ValueError("Password minimal 8 karakter")

    password_hash = generate_password_hash(password)
    created_at = datetime.utcnow().isoformat()

    create_user(
        username=username,
        password_hash=password_hash,
        role=role,
        created_at=created_at,
        must_change_password=1  # user dipaksa ganti password
    )
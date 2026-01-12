"""
auth_decorators.py
Decorator keamanan autentikasi & role
"""

from functools import wraps
from flask import redirect, url_for

from app.services.session_service import (
    is_logged_in,
    is_root,
)


def login_required(func):
    """
    Pastikan user sudah login
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not is_logged_in():
            return redirect(url_for("auth.login"))
        return func(*args, **kwargs)
    return wrapper


def root_required(func):
    """
    Pastikan user adalah root/admin
    """
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not is_logged_in():
            return redirect(url_for("auth.login"))
        if not is_root():
            return "Akses ditolak (root only)", 403
        return func(*args, **kwargs)
    return wrapper
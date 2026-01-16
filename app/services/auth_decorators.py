"""
auth_decorators.py
Decorator keamanan autentikasi & role
"""

from functools import wraps
from flask import session, redirect, url_for, flash 

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
    @wraps(func)
    def wrapper(*args, **kwargs):
        if not session.get("logged_in"):
            flash("Silakan login", "error")
            return redirect("/login")

        if session.get("role") != "root":
            flash("Akses ditolak", "error")
            return redirect("/dashboard")

        return func(*args, **kwargs)

    return wrapper
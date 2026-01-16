"""
session_service.py
Manajemen session login
"""

from flask import session
from datetime import datetime, timedelta

SESSION_TIMEOUT = timedelta(minutes=30)


def login_session(username, role):
    session.clear()
    session["logged_in"] = True
    session["user"] = username
    session["role"] = role
    session["login_time"] = datetime.utcnow().isoformat()


def logout_session():
    session.clear()


def is_logged_in():
    if not session.get("logged_in"):
        return False

    login_time = session.get("login_time")
    if not login_time:
        return False

    login_time = datetime.fromisoformat(login_time)
    if datetime.utcnow() - login_time > SESSION_TIMEOUT:
        session.clear()
        return False

    return True


def is_root():
    return session.get("role") == "root"


def current_user():
    return session.get("user")

def current_role():
    return session.get("role")
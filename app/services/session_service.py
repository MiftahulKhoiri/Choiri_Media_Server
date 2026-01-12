"""
session_service.py
Manajemen session login
"""

from flask import session


def login_session(username, role):
    session.clear()
    session["logged_in"] = True
    session["user"] = username
    session["role"] = role


def logout_session():
    session.clear()


def is_logged_in():
    return session.get("logged_in", False)


def is_root():
    return session.get("role") == "root"


def current_user():
    return session.get("user")
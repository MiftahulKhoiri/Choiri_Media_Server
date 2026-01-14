"""
api_auth_decorator.py
Proteksi endpoint API via token
"""

from functools import wraps
from flask import request, jsonify

from app.services.api_token_service import verify_token


def api_token_required(func):
    @wraps(func)
    def wrapper(*args, **kwargs):
        auth = request.headers.get("Authorization", "")

        if not auth.startswith("Bearer "):
            return jsonify({"error": "Token required"}), 401

        token = auth.split(" ", 1)[1]
        user = verify_token(token)

        if not user:
            return jsonify({"error": "Invalid token"}), 401

        request.api_user = user
        return func(*args, **kwargs)

    return wrapper
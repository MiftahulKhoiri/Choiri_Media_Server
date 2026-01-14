"""
api_token_service.py
Business logic API token
"""

import secrets
import hashlib
from datetime import datetime

from app.repositories.api_token_repository import (
    init_token_table,
    save_token,
    find_token_hash,
)


def init_api_token():
    init_token_table()


def _hash_token(token: str) -> str:
    return hashlib.sha256(token.encode()).hexdigest()


def generate_token(username: str) -> str:
    token = secrets.token_urlsafe(32)
    token_hash = _hash_token(token)

    save_token(
        user=username,
        token_hash=token_hash,
        created_at=datetime.utcnow().isoformat()
    )

    return token  # ⚠ dikembalikan SEKALI saja


def verify_token(token: str):
    token_hash = _hash_token(token)
    return find_token_hash(token_hash)
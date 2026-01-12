"""
user_model.py
Representasi data user
"""

from dataclasses import dataclass


@dataclass
class User:
    id: int
    username: str
    password_hash: str
    role: str
    created_at: str
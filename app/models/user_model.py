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
    must_change_password: int
    created_at: str
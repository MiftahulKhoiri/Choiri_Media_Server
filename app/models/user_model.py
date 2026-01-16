"""
user_model.py
Representasi data user
"""

from dataclasses import dataclass


@dataclass
class User:
    def __init__(
        self,
        id,
        username,
        password_hash,
        role,
        is_active,
        must_change_password,
        created_at,
    ):
        self.id = id
        self.username = username
        self.password_hash = password_hash
        self.role = role
        self.is_active = is_active
        self.must_change_password = must_change_password
        self.created_at = created_at
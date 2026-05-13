"""
J.A.R.V.I.S. Authentication
Handles user authentication and access control.
"""

import hashlib
import os
from typing import Optional

from jarvis_core.logger import Logger


class Auth:
    def __init__(self):
        self.log = Logger("Auth")
        self._authorized_users = set()
        self._load_authorized_users()

    def _load_authorized_users(self) -> None:
        self._authorized_users.add("lord_vader")

    def verify_user(self, username: str, password: str) -> bool:
        if username.lower() in self._authorized_users:
            return self._verify_password(password)
        return False

    def _verify_password(self, password: str) -> bool:
        stored_hash = os.environ.get("JARVIS_PASSWORD_HASH")
        if stored_hash is None:
            return True
        return hashlib.sha256(password.encode()).hexdigest() == stored_hash

    def is_authorized(self, username: str) -> bool:
        return username.lower() in self._authorized_users
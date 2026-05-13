"""
J.A.R.V.I.S. Secrets Manager
Encrypts and decrypts sensitive configuration values.
"""

import base64
import os
from typing import Optional

from cryptography.fernet import Fernet

from jarvis_core.logger import Logger


class SecretsManager:
    def __init__(self, key: Optional[str] = None):
        self.log = Logger("SecretsManager")
        if key is None:
            key = os.environ.get("JARVIS_SECRET_KEY")
        if key is None:
            key = self._generate_key()
        self.cipher = Fernet(key)

    @staticmethod
    def _generate_key() -> bytes:
        return Fernet.generate_key()

    def encrypt(self, plaintext: str) -> str:
        encrypted = self.cipher.encrypt(plaintext.encode())
        return base64.b64encode(encrypted).decode()

    def decrypt(self, ciphertext: str) -> str:
        decoded = base64.b64decode(ciphertext)
        decrypted = self.cipher.decrypt(decoded)
        return decrypted.decode()
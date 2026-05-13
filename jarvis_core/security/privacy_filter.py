"""
J.A.R.V.I.S. Privacy Filter
Redacts sensitive data from logs and outputs.
"""

import re
from typing import List


class PrivacyFilter:
    def __init__(self):
        self._patterns: List[str] = [
            r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
            r'\b\d{3}[-.]?\d{3}[-.]?\d{4}\b',
            r'\b\d{3}[-.]?\d{2}[-.]?\d{4}\b',
            r'\b(?:\d[ -]*?){13,16}\b',
            r'password\s*[=:]\s*\S+',
            r'secret\s*[=:]\s*\S+',
            r'token\s*[=:]\s*\S+',
            r'key\s*[=:]\s*\S+',
            r'api[_-]?key\s*[=:]\s*\S+',
        ]

    def filter(self, text: str) -> str:
        filtered = text
        for pattern in self._patterns:
            filtered = re.sub(pattern, "[REDACTED]", filtered, flags=re.IGNORECASE)
        return filtered

    def filter_dict(self, data: dict) -> dict:
        filtered = {}
        for key, value in data.items():
            if isinstance(value, str):
                filtered[key] = self.filter(value)
            elif isinstance(value, dict):
                filtered[key] = self.filter_dict(value)
            else:
                filtered[key] = value
        return filtered
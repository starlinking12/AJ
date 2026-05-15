"""
J.A.R.V.I.S. System Cache
Caches system metrics to reduce polling overhead.
"""

import time
from typing import Dict, Any, Optional

from jarvis_core.logger import Logger


class SystemCache:
    def __init__(self, ttl: int = 2):
        self.log = Logger("SystemCache")
        self.ttl = ttl
        self._cache: Dict[str, Dict[str, Any]] = {}

    def get(self, key: str) -> Optional[Dict]:
        if key in self._cache:
            entry = self._cache[key]
            if time.time() < entry["expires_at"]:
                return entry["data"]
            del self._cache[key]
        return None

    def set(self, key: str, data: Any) -> None:
        self._cache[key] = {
            "data": data,
            "expires_at": time.time() + self.ttl,
        }

    def clear(self) -> None:
        self._cache.clear()
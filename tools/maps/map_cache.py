"""
J.A.R.V.I.S. Map Cache
Caches geocoding results to reduce API calls.
"""

import time
from typing import Dict, Any, Optional

from jarvis_core.logger import Logger


class MapCache:
    def __init__(self, ttl: int = 86400):
        self.log = Logger("MapCache")
        self.ttl = ttl
        self._cache: Dict[str, Dict[str, Any]] = {}

    def get(self, key: str) -> Optional[Dict]:
        normalized = key.lower().strip()
        if normalized in self._cache:
            entry = self._cache[normalized]
            if time.time() < entry["expires_at"]:
                return entry["data"]
            del self._cache[normalized]
        return None

    def set(self, key: str, data: Dict) -> None:
        normalized = key.lower().strip()
        self._cache[normalized] = {
            "data": data,
            "expires_at": time.time() + self.ttl,
        }

    def clear(self) -> None:
        self._cache.clear()

    def get_stats(self) -> Dict:
        return {
            "total_entries": len(self._cache),
            "ttl_hours": self.ttl / 3600,
        }
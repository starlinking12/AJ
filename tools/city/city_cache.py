"""
J.A.R.V.I.S. City Cache
Caches city data to reduce API calls.
City data cached for 7 days by default.
"""

import time
from typing import Dict, Any, Optional

from jarvis_core.logger import Logger


class CityCache:
    def __init__(self, ttl: int = 604800):
        self.log = Logger("CityCache")
        self.ttl = ttl
        self._cache: Dict[str, Dict[str, Any]] = {}

    def get(self, key: str) -> Optional[Dict]:
        normalized = key.lower().strip()
        if normalized in self._cache:
            entry = self._cache[normalized]
            if time.time() < entry["expires_at"]:
                self.log.debug(f"City cache hit: {key}")
                return entry["data"]
            del self._cache[normalized]
        return None

    def set(self, key: str, data: Dict) -> None:
        normalized = key.lower().strip()
        self._cache[normalized] = {
            "data": data,
            "expires_at": time.time() + self.ttl,
            "cached_at": time.time(),
        }

    def clear(self) -> None:
        self._cache.clear()

    def get_stats(self) -> Dict:
        return {
            "total_entries": len(self._cache),
            "ttl_days": self.ttl / 86400,
        }
"""
J.A.R.V.I.S. Weather Cache
Caches weather data to reduce API calls.
Weather cached for 15 minutes by default.
"""

import time
from typing import Dict, Any, Optional

from jarvis_core.logger import Logger


class WeatherCache:
    def __init__(self, ttl: int = 900):
        self.log = Logger("WeatherCache")
        self.ttl = ttl
        self._cache: Dict[str, Dict[str, Any]] = {}

    def get(self, key: str) -> Optional[Dict]:
        normalized = key.lower().strip()
        if normalized in self._cache:
            entry = self._cache[normalized]
            if time.time() < entry["expires_at"]:
                self.log.debug(f"Weather cache hit: {key[:30]}")
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
            "ttl_minutes": self.ttl / 60,
        }
"""
J.A.R.V.I.S. Search Cache
Caches search results to reduce API calls.
"""

import time
from typing import Dict, Any, Optional

from jarvis_core.logger import Logger


class SearchCache:
    def __init__(self, ttl: int = 3600):
        self.log = Logger("SearchCache")
        self.ttl = ttl
        self._cache: Dict[str, Dict[str, Any]] = {}

    def get(self, query: str) -> Optional[Dict]:
        key = query.lower().strip()
        if key in self._cache:
            entry = self._cache[key]
            if time.time() < entry["expires_at"]:
                self.log.debug(f"Cache hit: {query[:50]}")
                return entry["data"]
            del self._cache[key]
        return None

    def set(self, query: str, data: Dict) -> None:
        key = query.lower().strip()
        self._cache[key] = {
            "data": data,
            "expires_at": time.time() + self.ttl,
            "cached_at": time.time(),
        }

    def clear(self) -> None:
        self._cache.clear()

    def get_stats(self) -> Dict:
        return {
            "total_entries": len(self._cache),
            "ttl_seconds": self.ttl,
        }
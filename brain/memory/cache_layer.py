"""
J.A.R.V.I.S. Cache Layer
In-memory cache for frequently accessed data.
"""

import time
from typing import Any, Dict, Optional

from jarvis_core.logger import Logger


class CacheLayer:
    def __init__(self, default_ttl: int = 300):
        self.log = Logger("CacheLayer")
        self.default_ttl = default_ttl        self._cache: Dict[str, Dict[str, Any]] = {}

    def get(self, key: str) -> Optional[Any]:
        if key not in self._cache:
            return None

        entry = self._cache[key]
        if time.time() > entry["expires_at"]:
            del self._cache[key]
            return None

        return entry["value"]

    def set(self, key: str, value: Any, ttl: int = None) -> None:
        if ttl is None:
            ttl = self.default_ttl

        self._cache[key] = {
            "value": value,
            "expires_at": time.time() + ttl,
            "created_at": time.time(),
        }

    def delete(self, key: str) -> bool:
        if key in self._cache:
            del self._cache[key]
            return True
        return False

    def clear(self) -> None:
        self._cache.clear()

    def get_stats(self) -> Dict:
        current_time = time.time()
        total = len(self._cache)
        expired = sum(
            1 for entry in self._cache.values()
            if entry["expires_at"] <= current_time
        )
        return {
            "total_entries": total,
            "expired_entries": expired,
            "active_entries": total - expired,
        }

    def cleanup_expired(self) -> int:
        current_time = time.time()
        expired_keys = [
            k for k, v in self._cache.items()
            if v["expires_at"] <= current_time
        ]
        for key in expired_keys:
            del self._cache[key]
        return len(expired_keys)
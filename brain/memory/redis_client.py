"""
J.A.R.V.I.S. Redis Client
Optional Redis-based caching and pub/sub for distributed memory.
"""

from typing import Any, Optional

from jarvis_core.logger import Logger


class RedisClient:
    def __init__(self, host: str = "localhost", port: int = 6379, db: int = 0):
        self.log = Logger("RedisClient")
        self.host = host
        self.port = port
        self.db = db
        self._client = None
        self._initialized = False

    def initialize(self) -> bool:
        try:
            import redis
            self._client = redis.Redis(
                host=self.host,
                port=self.port,
                db=self.db,
                decode_responses=True,
            )
            self._client.ping()
            self._initialized = True
            self.log.info(f"Redis client ready: {self.host}:{self.port}")
            return True
        except ImportError:
            self.log.warn("redis not installed. Redis features disabled.")
            return False
        except Exception as e:
            self.log.warn(f"Redis connection failed: {e}")
            return False

    def get(self, key: str) -> Optional[str]:
        if not self._initialized or self._client is None:
            return None
        try:
            return self._client.get(key)
        except Exception:
            return None

    def set(self, key: str, value: str, ttl: int = None) -> bool:
        if not self._initialized or self._client is None:
            return False
        try:
            if ttl:
                self._client.setex(key, ttl, value)
            else:
                self._client.set(key, value)
            return True
        except Exception:
            return False

    def delete(self, key: str) -> bool:
        if not self._initialized:
            return False
        try:
            self._client.delete(key)
            return True
        except Exception:
            return False

    def publish(self, channel: str, message: str) -> bool:
        if not self._initialized or self._client is None:
            return False
        try:
            self._client.publish(channel, message)
            return True
        except Exception:
            return False

    def close(self) -> None:
        if self._client:
            self._client.close()
            self._client = None
        self._initialized = False
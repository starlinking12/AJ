"""
J.A.R.V.I.S. Audio Ring Buffer
Circular buffer for efficient audio data management.
"""

import threading
from typing import Optional

from jarvis_core.logger import Logger


class AudioRingBuffer:
    def __init__(self, max_size_bytes: int = 1024 * 1024):
        self.log = Logger("RingBuffer")
        self.max_size = max_size_bytes
        self._buffer = bytearray()
        self._lock = threading.Lock()
        self._total_written = 0
        self._total_read = 0

    def write(self, data: bytes) -> None:
        with self._lock:
            self._buffer.extend(data)
            self._total_written += len(data)

            while len(self._buffer) > self.max_size:
                excess = len(self._buffer) - self.max_size
                self._buffer = self._buffer[excess:]
                self._total_read += excess

    def read(self, size: int) -> bytes:
        with self._lock:
            if len(self._buffer) < size:
                size = len(self._buffer)

            data = bytes(self._buffer[:size])
            self._buffer = self._buffer[size:]
            self._total_read += len(data)
            return data

    def read_all(self) -> bytes:
        with self._lock:
            data = bytes(self._buffer)
            self._buffer.clear()
            self._total_read += len(data)
            return data

    def peek(self, size: Optional[int] = None) -> bytes:
        with self._lock:
            if size is None or size >= len(self._buffer):
                return bytes(self._buffer)
            return bytes(self._buffer[:size])

    def clear(self) -> None:
        with self._lock:
            self._buffer.clear()

    def get_size(self) -> int:
        return len(self._buffer)

    def get_available(self) -> int:
        return len(self._buffer)

    def get_usage_percent(self) -> float:
        return (len(self._buffer) / self.max_size) * 100.0

    def is_empty(self) -> bool:
        return len(self._buffer) == 0

    def is_full(self) -> bool:
        return len(self._buffer) >= self.max_size
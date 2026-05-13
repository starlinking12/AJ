"""
J.A.R.V.I.S. Streaming Synthesizer
Handles streaming text-to-speech for low-latency response.
Jarvis starts speaking before the full response is generated.
"""

from typing import Optional

from jarvis_core.logger import Logger


class StreamingSynthesizer:
    def __init__(self, chunk_size: int = 50):
        self.log = Logger("StreamingSynth")
        self.chunk_size = chunk_size
        self._buffer = ""
        self._last_spoken = ""

    def process_text(self, text: str) -> Optional[str]:
        self._buffer += text

        if len(self._buffer) >= self.chunk_size:
            last_period = self._buffer.rfind(".")
            last_comma = self._buffer.rfind(",")
            last_question = self._buffer.rfind("?")
            last_exclamation = self._buffer.rfind("!")

            split_points = [
                p for p in [last_period, last_question, last_exclamation, last_comma]
                if p > 0
            ]

            if split_points:
                split_at = max(split_points) + 1
                chunk = self._buffer[:split_at].strip()
                self._buffer = self._buffer[split_at:]
                self._last_spoken = chunk
                return chunk

            if len(self._buffer) >= self.chunk_size * 2:
                words = self._buffer.split()
                mid = len(words) // 2
                chunk = " ".join(words[:mid])
                self._buffer = " ".join(words[mid:])
                self._last_spoken = chunk
                return chunk

        return None

    def finalize(self) -> str:
        remaining = self._buffer.strip()
        self._buffer = ""
        self._last_spoken = remaining
        return remaining

    def reset(self) -> None:
        self._buffer = ""
        self._last_spoken = ""
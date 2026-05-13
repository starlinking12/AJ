"""
J.A.R.V.I.S. Streaming Decoder
Provides real-time partial transcription as the user speaks.
"""

from collections import deque
from typing import Optional

from jarvis_core.logger import Logger


class StreamingDecoder:
    def __init__(self, max_buffer_size: int = 480000):
        self.log = Logger("StreamingDecoder")
        self._buffer = deque(maxlen=max_buffer_size)
        self._current_text = ""
        self._stable_text = ""

    def process_chunk(self, audio_chunk: bytes) -> Optional[str]:
        self._buffer.extend(audio_chunk)
        return self._current_text if self._current_text != self._stable_text else None

    def update_text(self, text: str) -> None:
        self._stable_text = self._current_text
        self._current_text = text

    def finalize(self) -> str:
        result = self._current_text
        self.reset()
        return result

    def reset(self) -> None:
        self._buffer.clear()
        self._current_text = ""
        self._stable_text = ""
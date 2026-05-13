"""
J.A.R.V.I.S. Buffer Manager
Manages a sliding audio buffer for speech detection.
"""

import struct
import time
from collections import deque
from typing import List, Tuple

from jarvis_core.logger import Logger


class BufferManager:
    def __init__(self, sample_rate: int = 16000, pre_speech_buffer_ms: int = 500):
        self.log = Logger("BufferManager")
        self.sample_rate = sample_rate
        self.pre_speech_buffer_ms = pre_speech_buffer_ms
        self._frames: List[Tuple[bytes, bool, float]] = []
        self._start_time: float = 0.0

    def add_frame(self, audio_frame: bytes, is_speech: bool) -> None:
        timestamp = time.time()
        self._frames.append((audio_frame, is_speech, timestamp))

    def get_speech_segment(self) -> bytes:
        speech_frames = []

        pre_buffer_frames = int(
            (self.pre_speech_buffer_ms / 1000.0) * self.sample_rate /
            (len(self._frames[0][0]) // 2 if self._frames else 160)
        )

        first_speech_index = 0
        for i, (_, is_speech, _) in enumerate(self._frames):
            if is_speech:
                first_speech_index = i
                break

        start_index = max(0, first_speech_index - pre_buffer_frames)

        for i in range(start_index, len(self._frames)):
            frame, _, _ = self._frames[i]
            speech_frames.append(frame)

        return b"".join(speech_frames)

    def get_all_audio(self) -> bytes:
        return b"".join(frame for frame, _, _ in self._frames)

    def get_duration_ms(self) -> float:
        if not self._frames:
            return 0.0
        bytes_per_sample = 2
        total_bytes = sum(len(frame) for frame, _, _ in self._frames)
        num_samples = total_bytes / bytes_per_sample
        return (num_samples / self.sample_rate) * 1000.0

    def clear(self) -> None:
        self._frames.clear()
        self._start_time = time.time()

    def is_empty(self) -> bool:
        return len(self._frames) == 0
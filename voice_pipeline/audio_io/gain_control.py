"""
J.A.R.V.I.S. Gain Control
Automatic gain control for consistent input levels.
"""

import struct
from typing import Optional

from jarvis_core.logger import Logger


class GainControl:
    def __init__(self, target_level: float = 1000.0, max_gain: float = 5.0):
        self.log = Logger("GainControl")
        self.target_level = target_level
        self.max_gain = max_gain
        self._current_gain = 1.0
        self._initialized = False

    def initialize(self) -> bool:
        self._initialized = True
        self.log.info(f"AGC ready. Target: {self.target_level}, Max gain: {self.max_gain}")
        return True

    def apply(self, audio_data: bytes) -> bytes:
        if not self._initialized:
            return audio_data

        try:
            samples = list(struct.unpack_from("h" * (len(audio_data) // 2), audio_data))

            if not samples:
                return audio_data

            current_level = sum(abs(s) for s in samples) / len(samples)

            if current_level > 0:
                target_gain = self.target_level / current_level
                target_gain = max(0.1, min(self.max_gain, target_gain))

                smoothing = 0.3
                self._current_gain = (
                    self._current_gain * (1 - smoothing) +
                    target_gain * smoothing
                )

            adjusted = [int(s * self._current_gain) for s in samples]
            return struct.pack("h" * len(adjusted), *adjusted)

        except Exception as e:
            self.log.error(f"Gain control failed: {e}")
            return audio_data

    def reset(self) -> None:
        self._current_gain = 1.0

    def get_current_gain(self) -> float:
        return self._current_gain
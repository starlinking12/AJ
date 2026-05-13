"""
J.A.R.V.I.S. Noise Suppression
Reduces background noise from microphone input.
"""

import struct
from typing import Optional

from jarvis_core.logger import Logger


class NoiseSuppression:
    def __init__(self, sample_rate: int = 16000, reduction_level: float = 0.7):
        self.log = Logger("NoiseSuppression")
        self.sample_rate = sample_rate
        self.reduction_level = reduction_level
        self._initialized = False
        self._noise_profile: Optional[list] = None

    def initialize(self) -> bool:
        self._initialized = True
        self.log.info(f"Noise suppression ready. Level: {self.reduction_level}")
        return True

    def calibrate(self, audio_data: bytes) -> None:
        samples = struct.unpack_from("h" * (len(audio_data) // 2), audio_data)
        self._noise_profile = [abs(s) for s in samples]
        self.log.info("Noise profile calibrated.")

    def suppress(self, audio_data: bytes) -> bytes:
        if not self._initialized:
            return audio_data

        try:
            samples = list(struct.unpack_from("h" * (len(audio_data) // 2), audio_data))

            if self._noise_profile and len(self._noise_profile) == len(samples):
                for i in range(len(samples)):
                    threshold = self._noise_profile[i] * 1.5
                    if abs(samples[i]) < threshold:
                        samples[i] = int(samples[i] * (1 - self.reduction_level))

            return struct.pack("h" * len(samples), *samples)

        except Exception as e:
            self.log.error(f"Noise suppression failed: {e}")
            return audio_data

    def set_level(self, level: float) -> None:
        self.reduction_level = max(0.0, min(1.0, level))
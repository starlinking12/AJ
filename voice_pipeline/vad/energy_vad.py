"""
J.A.R.V.I.S. Energy VAD Engine
Simple energy-based voice activity detection.
Fallback when other engines are unavailable.
"""

import struct

from jarvis_core.logger import Logger


class EnergyVAD:
    def __init__(self, sample_rate: int = 16000, threshold: float = 500.0):
        self.log = Logger("EnergyVAD")
        self.sample_rate = sample_rate
        self.threshold = threshold
        self._initialized = True

    def initialize(self) -> bool:
        self.log.info("Energy VAD initialized (always available).")
        return True

    def detect_speech(self, audio_frame: bytes) -> bool:
        try:
            samples = struct.unpack_from("h" * (len(audio_frame) // 2), audio_frame)
            energy = sum(abs(s) for s in samples) / len(samples)
            return energy > self.threshold
        except Exception:
            return False

    def set_threshold(self, threshold: float) -> None:
        self.threshold = threshold
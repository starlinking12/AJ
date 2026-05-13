"""
J.A.R.V.I.S. Silero VAD Engine
Uses the Silero VAD model for high-accuracy speech detection.
Neural network based. Works well in noisy environments.
"""

import struct
from typing import Optional

from jarvis_core.logger import Logger


class SileroVAD:
    def __init__(self, sample_rate: int = 16000, threshold: float = 0.5):
        self.log = Logger("SileroVAD")
        self.sample_rate = sample_rate
        self.threshold = threshold
        self._model = None
        self._utils = None
        self._initialized = False
        self._context = None

    def initialize(self) -> bool:
        try:
            import torch
            import torchaudio

            self._model, self._utils = torch.hub.load(
                repo_or_dir='snakers4/silero-vad',
                model='silero_vad',
                force_reload=False
            )
            self._model.eval()
            self._context = torch.zeros(1, 1)
            self._initialized = True
            self.log.info("Silero VAD initialized.")
            return True

        except ImportError:
            self.log.warn("torch or torchaudio not installed.")
            return False
        except Exception as e:
            self.log.warn(f"Silero VAD init failed: {e}")
            return False

    def detect_speech(self, audio_frame: bytes) -> bool:
        if not self._initialized:
            return False

        try:
            import torch

            samples = struct.unpack_from("h" * (len(audio_frame) // 2), audio_frame)
            audio_tensor = torch.tensor(samples, dtype=torch.float32) / 32768.0
            audio_tensor = audio_tensor.unsqueeze(0)

            speech_prob = self._model(audio_tensor, self.sample_rate).item()
            return speech_prob > self.threshold

        except Exception:
            return False
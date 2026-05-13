"""
J.A.R.V.I.S. WebRTC VAD Engine
Uses the WebRTC Voice Activity Detector.
Lightweight, fast, and widely used.
"""

import struct
from typing import Optional

import pyaudio

from jarvis_core.logger import Logger


class WebRTCVAD:
    def __init__(self, sample_rate: int = 16000, aggressiveness: int = 2):
        self.log = Logger("WebRTCVAD")
        self.sample_rate = sample_rate
        self.aggressiveness = aggressiveness
        self._vad = None
        self._initialized = False

    def initialize(self) -> bool:
        try:
            import webrtcvad
            self._vad = webrtcvad.Vad(self.aggressiveness)
            self._initialized = True
            self.log.info("WebRTC VAD initialized.")
            return True
        except ImportError:
            self.log.warn("webrtcvad not installed.")
            return False
        except Exception as e:
            self.log.warn(f"WebRTC VAD init failed: {e}")
            return False

    def detect_speech(self, audio_frame: bytes) -> bool:
        if not self._initialized or self._vad is None:
            return False

        try:
            return self._vad.is_speech(audio_frame, self.sample_rate)
        except Exception:
            return False
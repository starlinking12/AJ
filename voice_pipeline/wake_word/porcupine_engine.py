"""
J.A.R.V.I.S. Porcupine Wake Word Engine
Uses Picovoice Porcupine for wake word detection.
Free tier supports 3 custom wake words.
"""

import os
import struct
from pathlib import Path
from typing import List, Optional

import pyaudio

from jarvis_core.logger import Logger


class PorcupineEngine:
    def __init__(self, keywords: List[str], sensitivity: float = 0.5):
        self.log = Logger("PorcupineEngine")
        self.keywords = keywords
        self.sensitivity = sensitivity
        self._handle = None
        self._audio: Optional[pyaudio.PyAudio] = None
        self._stream = None
        self._initialized = False

    def initialize(self) -> bool:
        try:
            import pvporcupine

            self._handle = pvporcupine.create(
                keywords=self.keywords,
                sensitivities=[self.sensitivity] * len(self.keywords)
            )

            self._audio = pyaudio.PyAudio()
            self._stream = self._audio.open(
                rate=self._handle.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=self._handle.frame_length
            )

            self._initialized = True
            self.log.info(f"Porcupine ready. Keywords: {self.keywords}")
            return True

        except ImportError:
            self.log.warn("pvporcupine not installed.")
            return False
        except Exception as e:
            self.log.warn(f"Porcupine initialization failed: {e}")
            return False

    def process_frame(self) -> bool:
        if not self._initialized or self._stream is None:
            return False

        try:
            pcm = self._stream.read(
                self._handle.frame_length,
                exception_on_overflow=False
            )
            pcm = struct.unpack_from("h" * self._handle.frame_length, pcm)
            result = self._handle.process(pcm)
            return result >= 0
        except Exception:
            return False

    def set_sensitivity(self, value: float) -> None:
        self.sensitivity = value

    def release(self) -> None:
        if self._handle:
            self._handle.delete()
            self._handle = None
        if self._stream:
            self._stream.stop_stream()
            self._stream.close()
            self._stream = None
        if self._audio:
            self._audio.terminate()
            self._audio = None
        self._initialized = False
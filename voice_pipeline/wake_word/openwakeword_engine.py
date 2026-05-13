"""
J.A.R.V.I.S. OpenWakeWord Engine
Uses openwakeword for wake word detection.
Fully offline, free, no API key required.
"""

import struct
from typing import List, Optional

import pyaudio

from jarvis_core.logger import Logger


class OpenWakeWordEngine:
    def __init__(self, keywords: List[str], sensitivity: float = 0.5):
        self.log = Logger("OpenWakeWordEngine")
        self.keywords = keywords
        self.sensitivity = sensitivity
        self._model = None
        self._audio: Optional[pyaudio.PyAudio] = None
        self._stream = None
        self._initialized = False

    def initialize(self) -> bool:
        try:
            import openwakeword

            self._model = openwakeword.Model(
                wakeword_models=self.keywords,
                inference_framework="tflite"
            )

            self._audio = pyaudio.PyAudio()
            self._stream = self._audio.open(
                rate=16000,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                frames_per_buffer=1280
            )

            self._initialized = True
            self.log.info(f"OpenWakeWord ready. Keywords: {self.keywords}")
            return True

        except ImportError:
            self.log.warn("openwakeword not installed.")
            return False
        except Exception as e:
            self.log.warn(f"OpenWakeWord initialization failed: {e}")
            return False

    def process_frame(self) -> bool:
        if not self._initialized or self._stream is None:
            return False

        try:
            frame = self._stream.read(1280, exception_on_overflow=False)
            pcm = struct.unpack_from("h" * 1280, frame)

            predictions = self._model.predict(pcm)
            for keyword, score in predictions.items():
                if score > self.sensitivity:
                    return True
            return False

        except Exception:
            return False

    def set_sensitivity(self, value: float) -> None:
        self.sensitivity = value

    def release(self) -> None:
        if self._stream:
            self._stream.stop_stream()
            self._stream.close()
            self._stream = None
        if self._audio:
            self._audio.terminate()
            self._audio = None
        self._model = None
        self._initialized = False
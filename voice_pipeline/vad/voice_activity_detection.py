"""
J.A.R.V.I.S. Voice Activity Detection
Detects when the user starts and stops speaking.
Uses multiple engines with automatic fallback.
"""

import threading
import time
from typing import Callable, Optional

from voice_pipeline.vad.webrtc_vad import WebRTCVAD
from voice_pipeline.vad.silero_vad import SileroVAD
from voice_pipeline.vad.energy_vad import EnergyVAD
from voice_pipeline.vad.speech_segment import SpeechSegment
from voice_pipeline.vad.buffer_manager import BufferManager
from voice_pipeline.vad.endpoint_detection import EndpointDetector

from jarvis_core.logger import Logger


class VoiceActivityDetector:
    """
    Detects speech segments from an audio stream.
    Records until silence is detected, then returns the audio segment.
    """

    def __init__(self, sample_rate: int = 16000, silence_threshold: float = 1.0):
        self.log = Logger("VAD")
        self.sample_rate = sample_rate
        self.silence_threshold = silence_threshold
        self._engine = None
        self._buffer = BufferManager(sample_rate)
        self._endpoint = EndpointDetector(silence_threshold)
        self._on_speech_start: Optional[Callable] = None
        self._on_speech_end: Optional[Callable] = None
        self._on_speech_segment: Optional[Callable] = None
        self._running = False
        self._initialized = False

    def initialize(self) -> bool:
        self.log.info("Initializing VAD...")

        engines = [SileroVAD, WebRTCVAD, EnergyVAD]
        for engine_class in engines:
            try:
                self._engine = engine_class(self.sample_rate)
                if self._engine.initialize():
                    self.log.info(f"VAD engine: {engine_class.__name__}")
                    self._initialized = True
                    return True
            except Exception as e:
                self.log.warn(f"{engine_class.__name__} unavailable: {e}")

        self.log.error("No VAD engine available.")
        return False

    def set_callbacks(
        self,
        on_start: Optional[Callable] = None,
        on_end: Optional[Callable] = None,
        on_segment: Optional[Callable] = None
    ) -> None:
        self._on_speech_start = on_start
        self._on_speech_end = on_end
        self._on_speech_segment = on_segment

    def start(self) -> None:
        if not self._initialized:
            self.log.error("VAD not initialized.")
            return
        self._running = True
        self._buffer.clear()
        self._endpoint.reset()
        self.log.info("VAD started.")

    def stop(self) -> None:
        self._running = False
        self.log.info("VAD stopped.")

    def process_frame(self, audio_frame: bytes) -> Optional[SpeechSegment]:
        if not self._running:
            return None

        is_speech = self._engine.detect_speech(audio_frame)
        self._buffer.add_frame(audio_frame, is_speech)

        if is_speech and not self._endpoint.is_speaking:
            self._endpoint.speech_started()
            if self._on_speech_start:
                self._on_speech_start()

        if is_speech:
            self._endpoint.speech_continued()

        if not is_speech and self._endpoint.is_speaking:
            self._endpoint.silence_detected()
            if self._endpoint.is_speech_complete():
                segment = self._buffer.get_speech_segment()
                self._endpoint.speech_ended()
                self._buffer.clear()
                if self._on_speech_end:
                    self._on_speech_end()
                if self._on_speech_segment:
                    self._on_speech_segment(segment)
                return segment

        return None

    def get_current_audio(self) -> bytes:
        return self._buffer.get_all_audio()

    def reset(self) -> None:
        self._buffer.clear()
        self._endpoint.reset()
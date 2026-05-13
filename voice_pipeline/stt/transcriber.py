"""
J.A.R.V.I.S. STT Transcriber
Main speech-to-text interface. Routes audio to the best available engine.
"""

import threading
from typing import Callable, Optional

from voice_pipeline.stt.faster_whisper_engine import FasterWhisperEngine
from voice_pipeline.stt.whisper_cpp_engine import WhisperCppEngine
from voice_pipeline.stt.streaming_decoder import StreamingDecoder
from voice_pipeline.stt.punctuation import PunctuationRestorer
from voice_pipeline.stt.language_detector import LanguageDetector

from jarvis_core.logger import Logger


class Transcriber:
    """
    Transcribes speech audio to text.
    Uses FasterWhisper as primary engine, WhisperCpp as fallback.
    Supports streaming transcription for real-time feedback.
    """

    def __init__(self, model_size: str = "base", language: str = "en"):
        self.log = Logger("Transcriber")
        self.model_size = model_size
        self.language = language
        self._engine = None
        self._streaming = StreamingDecoder()
        self._punctuation = PunctuationRestorer()
        self._language_detector = LanguageDetector()
        self._initialized = False
        self._on_partial: Optional[Callable] = None
        self._on_final: Optional[Callable] = None

    def initialize(self) -> bool:
        self.log.info(f"Initializing transcriber (model: {self.model_size})...")

        try:
            self._engine = FasterWhisperEngine(
                model_size=self.model_size,
                language=self.language
            )
            if self._engine.initialize():
                self._initialized = True
                self.log.info("FasterWhisper engine ready.")
                return True
        except Exception as e:
            self.log.warn(f"FasterWhisper unavailable: {e}")

        try:
            self._engine = WhisperCppEngine(
                model_size=self.model_size,
                language=self.language
            )
            if self._engine.initialize():
                self._initialized = True
                self.log.info("WhisperCpp engine ready.")
                return True
        except Exception as e:
            self.log.warn(f"WhisperCpp unavailable: {e}")

        self.log.error("No STT engine available.")
        return False

    def set_callbacks(
        self,
        on_partial: Optional[Callable] = None,
        on_final: Optional[Callable] = None
    ) -> None:
        self._on_partial = on_partial
        self._on_final = on_final

    def transcribe(self, audio_data: bytes) -> str:
        if not self._initialized or self._engine is None:
            self.log.error("Transcriber not initialized.")
            return ""

        try:
            text = self._engine.transcribe(audio_data)
            text = self._punctuation.restore(text)
            return text.strip()
        except Exception as e:
            self.log.error(f"Transcription failed: {e}")
            return ""

    def transcribe_streaming(self, audio_chunk: bytes) -> Optional[str]:
        if not self._initialized:
            return None

        partial = self._streaming.process_chunk(audio_chunk)
        if partial and self._on_partial:
            self._on_partial(partial)
        return partial

    def finalize_streaming(self) -> str:
        final_text = self._streaming.finalize()
        final_text = self._punctuation.restore(final_text)
        if final_text and self._on_final:
            self._on_final(final_text)
        return final_text

    def detect_language(self, audio_data: bytes) -> str:
        return self._language_detector.detect(audio_data)

    def get_available_models(self) -> list:
        return ["tiny", "base", "small", "medium", "large-v2", "large-v3"]
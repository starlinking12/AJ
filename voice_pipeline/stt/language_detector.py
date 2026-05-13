"""
J.A.R.V.I.S. Language Detector
Detects the spoken language from audio.
"""

from typing import Optional

from jarvis_core.logger import Logger


class LanguageDetector:
    def __init__(self):
        self.log = Logger("LanguageDetector")
        self._initialized = False
        self._model = None
        self._supported_languages = [
            "en", "es", "fr", "de", "it", "pt", "ja", "ko", "zh", "ru", "ar", "hi"
        ]

    def initialize(self) -> bool:
        try:
            import whisper
            self._model = whisper.load_model("tiny")
            self._initialized = True
            self.log.info("Language detector loaded.")
            return True
        except ImportError:
            self.log.warn("whisper not installed. Language detection limited.")
            self._initialized = True
            return True
        except Exception as e:
            self.log.warn(f"Language detector init failed: {e}")
            self._initialized = True
            return True

    def detect(self, audio_data: bytes) -> str:
        if self._model is None:
            return "en"

        try:
            import tempfile
            import wave

            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
                with wave.open(f, "wb") as wf:
                    wf.setnchannels(1)
                    wf.setsampwidth(2)
                    wf.setframerate(16000)
                    wf.writeframes(audio_data)

            audio = self._model.load_audio(f.name)
            audio = self._model.pad_or_trim(audio)
            mel = self._model.log_mel_spectrogram(audio).to(self._model.device)
            _, probs = self._model.detect_language(mel)

            return max(probs, key=probs.get)

        except Exception as e:
            self.log.debug(f"Language detection failed: {e}")
            return "en"

    def get_supported_languages(self) -> list:
        return self._supported_languages
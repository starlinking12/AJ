"""
J.A.R.V.I.S. Piper TTS Engine
Uses Piper TTS for fast, local, high-quality speech synthesis.
Supports custom voice models including Jarvis British Male.
"""

from pathlib import Path
from typing import List, Optional

from jarvis_core.logger import Logger


class PiperEngine:
    def __init__(self, voice: str = "jarvis_british_male"):
        self.log = Logger("PiperEngine")
        self.voice = voice
        self._model = None
        self._voice_path: Optional[Path] = None
        self._initialized = False

    def initialize(self) -> bool:
        try:
            import piper

            models_dir = Path(__file__).resolve().parent / "models"

            voice_file = models_dir / f"{self.voice}.onnx"
            config_file = models_dir / f"{self.voice}.json"

            if not voice_file.exists():
                self.log.warn(f"Voice model not found: {voice_file}")
                voice_file = self._download_voice()

            if voice_file and voice_file.exists():
                self._voice_path = voice_file
                self._model = piper.PiperVoice(
                    str(voice_file),
                    str(config_file) if config_file.exists() else None
                )
                self._initialized = True
                self.log.info(f"Piper TTS ready. Voice: {self.voice}")
                return True

            self.log.error("Failed to load Piper voice.")
            return False

        except ImportError:
            self.log.warn("piper-tts not installed.")
            return False
        except Exception as e:
            self.log.warn(f"Piper TTS init failed: {e}")
            return False

    def synthesize(self, text: str) -> bytes:
        if not self._initialized or self._model is None:
            return b""

        try:
            import io
            import wave

            audio_buffer = io.BytesIO()
            with wave.open(audio_buffer, "wb") as wf:
                self._model.synthesize(text, wf)
            return audio_buffer.getvalue()

        except Exception as e:
            self.log.error(f"Piper synthesis failed: {e}")
            return b""

    def set_voice(self, voice_name: str) -> bool:
        self.voice = voice_name
        return self.initialize()

    def get_available_voices(self) -> List[str]:
        models_dir = Path(__file__).resolve().parent / "models"
        if not models_dir.exists():
            return []
        return [
            f.stem for f in models_dir.glob("*.onnx")
        ]

    def _download_voice(self) -> Optional[Path]:
        return None
"""
J.A.R.V.I.S. WhisperCpp Engine
Uses whisper.cpp for transcription.
Lightweight, runs on CPU, good fallback option.
"""

import subprocess
import tempfile
import wave
from pathlib import Path
from typing import Optional

from jarvis_core.logger import Logger


class WhisperCppEngine:
    def __init__(self, model_size: str = "base", language: str = "en"):
        self.log = Logger("WhisperCpp")
        self.model_size = model_size
        self.language = language
        self._model_path: Optional[str] = None
        self._executable: Optional[str] = None
        self._initialized = False

    def initialize(self) -> bool:
        model_dir = Path(__file__).resolve().parent / "models"
        model_file = model_dir / f"ggml-{self.model_size}.bin"

        if model_file.exists():
            self._model_path = str(model_file)
            self._executable = "whisper-cpp"
            self._initialized = True
            self.log.info(f"WhisperCpp loaded: {self.model_size}")
            return True

        self.log.warn(f"Model not found: {model_file}")
        return False

    def transcribe(self, audio_data: bytes) -> str:
        if not self._initialized or self._model_path is None:
            return ""

        temp_path = None
        try:
            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
                temp_path = f.name
                with wave.open(f, "wb") as wf:
                    wf.setnchannels(1)
                    wf.setsampwidth(2)
                    wf.setframerate(16000)
                    wf.writeframes(audio_data)

            result = subprocess.run(
                [
                    self._executable,
                    "-m", self._model_path,
                    "-f", temp_path,
                    "-l", self.language,
                    "--no-timestamps",
                    "-otxt"
                ],
                capture_output=True,
                text=True,
                timeout=30
            )

            if result.returncode == 0:
                return result.stdout.strip()
            return ""

        except Exception as e:
            self.log.error(f"WhisperCpp error: {e}")
            return ""
        finally:
            if temp_path:
                try:
                    Path(temp_path).unlink()
                except Exception:
                    pass
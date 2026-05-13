"""
J.A.R.V.I.S. FasterWhisper Engine
Uses faster-whisper for fast, accurate transcription.
Optimized with CTranslate2.
"""

import tempfile
import wave
from pathlib import Path
from typing import Optional

from jarvis_core.logger import Logger


class FasterWhisperEngine:
    def __init__(self, model_size: str = "base", language: str = "en", device: str = "auto"):
        self.log = Logger("FasterWhisper")
        self.model_size = model_size
        self.language = language
        self.device = device
        self._model = None
        self._initialized = False

    def initialize(self) -> bool:
        try:
            from faster_whisper import WhisperModel

            compute_type = "int8"
            try:
                import torch
                if torch.cuda.is_available():
                    compute_type = "float16"
            except ImportError:
                pass

            self._model = WhisperModel(
                self.model_size,
                device=self.device,
                compute_type=compute_type
            )
            self._initialized = True
            self.log.info(f"FasterWhisper loaded: {self.model_size}")
            return True

        except ImportError:
            self.log.warn("faster-whisper not installed.")
            return False
        except Exception as e:
            self.log.warn(f"FasterWhisper init failed: {e}")
            return False

    def transcribe(self, audio_data: bytes) -> str:
        if not self._initialized or self._model is None:
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

            segments, _ = self._model.transcribe(
                temp_path,
                language=self.language,
                beam_size=5,
                vad_filter=True
            )

            full_text = " ".join(segment.text for segment in segments)
            return full_text.strip()

        except Exception as e:
            self.log.error(f"Transcription error: {e}")
            return ""
        finally:
            if temp_path:
                try:
                    Path(temp_path).unlink()
                except Exception:
                    pass
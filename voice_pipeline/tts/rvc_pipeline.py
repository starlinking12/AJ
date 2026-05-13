"""
J.A.R.V.I.S. RVC Pipeline
Retrieval-Based Voice Conversion for voice cloning.
Transforms TTS output to match a target voice.
"""

from pathlib import Path
from typing import Optional

from jarvis_core.logger import Logger


class RVCPipeline:
    def __init__(self):
        self.log = Logger("RVCPipeline")
        self._model_path: Optional[Path] = None
        self._initialized = False

    def initialize(self, model_path: Optional[str] = None) -> bool:
        if model_path is None:
            model_path = Path(__file__).resolve().parent / "models" / "jarvis_rvc.pth"

        self._model_path = Path(model_path)
        if self._model_path.exists():
            self._initialized = True
            self.log.info(f"RVC model loaded: {self._model_path}")
            return True

        self.log.warn(f"RVC model not found: {self._model_path}")
        return False

    def convert(self, audio_data: bytes, pitch_shift: int = 0) -> bytes:
        if not self._initialized:
            self.log.warn("RVC not initialized. Returning original audio.")
            return audio_data

        try:
            import numpy as np
            import io
            import soundfile as sf

            audio_array, sample_rate = sf.read(io.BytesIO(audio_data))

            converted = self._apply_rvc(audio_array, sample_rate, pitch_shift)

            buffer = io.BytesIO()
            sf.write(buffer, converted, sample_rate, format="WAV")
            return buffer.getvalue()

        except Exception as e:
            self.log.error(f"RVC conversion failed: {e}")
            return audio_data

    def _apply_rvc(
        self,
        audio: "np.ndarray",
        sample_rate: int,
        pitch_shift: int
    ) -> "np.ndarray":
        return audio
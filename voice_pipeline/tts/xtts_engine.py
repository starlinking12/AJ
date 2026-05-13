"""
J.A.R.V.I.S. XTTS Engine
Uses Coqui XTTSv2 for high-quality voice cloning.
Supports cloning voices from short audio samples.
"""

from pathlib import Path
from typing import List, Optional

from jarvis_core.logger import Logger


class XTTSEngine:
    def __init__(self, voice: str = "jarvis"):
        self.log = Logger("XTTS")
        self.voice = voice
        self._model = None
        self._speaker_embedding = None
        self._initialized = False

    def initialize(self) -> bool:
        try:
            from TTS.api import TTS

            self._model = TTS(
                model_name="tts_models/multilingual/multi-dataset/xtts_v2",
                progress_bar=False
            )

            models_dir = Path(__file__).resolve().parent / "models" / "jarvis_xtts"
            if models_dir.exists():
                speaker_wav = models_dir / "speaker.wav"
                if speaker_wav.exists():
                    self._speaker_embedding = self._model.synthesize(
                        "test",
                        speaker_wav=str(speaker_wav),
                        language="en"
                    )

            self._initialized = True
            self.log.info(f"XTTSv2 ready. Voice: {self.voice}")
            return True

        except ImportError:
            self.log.warn("TTS (Coqui) not installed.")
            return False
        except Exception as e:
            self.log.warn(f"XTTS init failed: {e}")
            return False

    def synthesize(self, text: str) -> bytes:
        if not self._initialized or self._model is None:
            return b""

        try:
            import io
            import soundfile as sf
            import numpy as np

            speaker_wav = self._get_speaker_wav()

            output = self._model.tts(
                text=text,
                speaker_wav=speaker_wav,
                language="en"
            )

            audio_array = np.array(output, dtype=np.float32)

            buffer = io.BytesIO()
            sf.write(buffer, audio_array, 24000, format="WAV")
            return buffer.getvalue()

        except Exception as e:
            self.log.error(f"XTTS synthesis failed: {e}")
            return b""

    def _get_speaker_wav(self) -> Optional[str]:
        models_dir = Path(__file__).resolve().parent / "models" / "jarvis_xtts"
        speaker_wav = models_dir / "speaker.wav"
        if speaker_wav.exists():
            return str(speaker_wav)
        return None

    def set_voice(self, voice_name: str) -> bool:
        self.voice = voice_name
        return self.initialize()

    def get_available_voices(self) -> List[str]:
        models_dir = Path(__file__).resolve().parent / "models"
        return ["jarvis"]
"""
J.A.R.V.I.S. Voice Cloner
Clones voices from audio samples using RVC or XTTS.
"""

from pathlib import Path
from typing import Optional

from jarvis_core.logger import Logger


class VoiceCloner:
    def __init__(self):
        self.log = Logger("VoiceCloner")
        self._samples_dir = Path(__file__).resolve().parent / "models" / "jarvis_xtts"

    def clone_from_file(self, audio_path: str, voice_name: str = "jarvis") -> bool:
        import shutil

        try:
            dest = self._samples_dir / "speaker.wav"
            self._samples_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy(audio_path, dest)
            self.log.info(f"Voice sample saved for: {voice_name}")
            return True
        except Exception as e:
            self.log.error(f"Voice cloning failed: {e}")
            return False

    def clone_from_samples(self, audio_files: list, voice_name: str = "jarvis") -> bool:
        try:
            from pydub import AudioSegment

            combined = AudioSegment.empty()
            for file in audio_files:
                segment = AudioSegment.from_file(file)
                combined += segment

            output_path = self._samples_dir / "speaker.wav"
            combined.export(str(output_path), format="wav")
            self.log.info(f"Combined voice sample saved: {voice_name}")
            return True

        except ImportError:
            self.log.warn("pydub not installed.")
            return False
        except Exception as e:
            self.log.error(f"Sample combination failed: {e}")
            return False

    def has_voice_sample(self, voice_name: str = "jarvis") -> bool:
        sample_path = self._samples_dir / "speaker.wav"
        return sample_path.exists()
"""
J.A.R.V.I.S. Diarization
Identifies different speakers in audio.
Answers the question: who spoke when?
"""

from typing import List, Dict

from jarvis_core.logger import Logger


class Diarization:
    def __init__(self):
        self.log = Logger("Diarization")
        self._initialized = False
        self._pipeline = None

    def initialize(self) -> bool:
        try:
            from pyannote.audio import Pipeline
            self._pipeline = Pipeline.from_pretrained(
                "pyannote/speaker-diarization-3.1"
            )
            self._initialized = True
            self.log.info("Diarization pipeline loaded.")
            return True
        except ImportError:
            self.log.warn("pyannote not installed. Diarization disabled.")
            return False
        except Exception as e:
            self.log.warn(f"Diarization init failed: {e}")
            return False

    def identify_speakers(self, audio_file: str) -> List[Dict]:
        if not self._initialized or self._pipeline is None:
            return []

        try:
            diarization = self._pipeline(audio_file)
            segments = []
            for turn, _, speaker in diarization.itertracks(yield_label=True):
                segments.append({
                    "speaker": speaker,
                    "start": turn.start,
                    "end": turn.end,
                    "duration": turn.end - turn.start
                })
            return segments
        except Exception as e:
            self.log.error(f"Diarization failed: {e}")
            return []
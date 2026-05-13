"""
J.A.R.V.I.S. Speed Controller
Adjusts the playback speed of synthesized speech.
"""

from jarvis_core.logger import Logger


class SpeedController:
    def __init__(self, default_speed: float = 1.0):
        self.log = Logger("SpeedController")
        self.default_speed = default_speed
        self._min_speed = 0.5
        self._max_speed = 3.0

    def adjust(self, audio_data: bytes, speed_factor: float) -> bytes:
        if speed_factor == 1.0:
            return audio_data

        speed_factor = max(self._min_speed, min(self._max_speed, speed_factor))

        try:
            from pydub import AudioSegment
            import io

            segment = AudioSegment.from_file(io.BytesIO(audio_data), format="wav")

            adjusted = segment.speedup(
                playback_speed=speed_factor,
                chunk_size=50,
                crossfade=10
            )

            buffer = io.BytesIO()
            adjusted.export(buffer, format="wav")
            return buffer.getvalue()

        except ImportError:
            return audio_data
        except Exception as e:
            self.log.error(f"Speed adjustment failed: {e}")
            return audio_data
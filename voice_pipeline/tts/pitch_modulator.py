"""
J.A.R.V.I.S. Pitch Modulator
Adjusts the pitch of synthesized speech.
"""

from jarvis_core.logger import Logger


class PitchModulator:
    def __init__(self, default_pitch: float = 1.0):
        self.log = Logger("PitchModulator")
        self.default_pitch = default_pitch
        self._min_pitch = 0.5
        self._max_pitch = 2.0

    def modulate(self, audio_data: bytes, pitch_factor: float) -> bytes:
        if pitch_factor == 1.0:
            return audio_data

        pitch_factor = max(self._min_pitch, min(self._max_pitch, pitch_factor))

        try:
            from pydub import AudioSegment
            import io

            segment = AudioSegment.from_file(io.BytesIO(audio_data), format="wav")

            new_sample_rate = int(segment.frame_rate * pitch_factor)
            adjusted = segment._spawn(
                segment.raw_data,
                overrides={"frame_rate": new_sample_rate}
            )
            adjusted = adjusted.set_frame_rate(segment.frame_rate)

            buffer = io.BytesIO()
            adjusted.export(buffer, format="wav")
            return buffer.getvalue()

        except ImportError:
            return audio_data
        except Exception as e:
            self.log.error(f"Pitch modulation failed: {e}")
            return audio_data
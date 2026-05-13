"""
J.A.R.V.I.S. Audio Post-Processor
Applies audio effects to create the signature J.A.R.V.I.S. voice.
Highpass filter, treble boost, subtle echo for HUD clarity.
"""

from jarvis_core.logger import Logger


class AudioPostProcessor:
    def __init__(
        self,
        highpass_freq: float = 200.0,
        treble_boost_db: float = 6.0,
        echo_amount: float = 0.1
    ):
        self.log = Logger("AudioPost")
        self.highpass_freq = highpass_freq
        self.treble_boost_db = treble_boost_db
        self.echo_amount = echo_amount

    def process(self, audio_data: bytes) -> bytes:
        try:
            from pydub import AudioSegment
            from pydub.effects import high_pass_filter
            import io

            segment = AudioSegment.from_file(io.BytesIO(audio_data), format="wav")

            segment = high_pass_filter(segment, self.highpass_freq)

            segment = segment + self.treble_boost_db

            if self.echo_amount > 0:
                echo = segment - (10 * (1 - self.echo_amount))
                echo = echo[:int(len(echo) * self.echo_amount)]
                segment = segment.overlay(echo, position=50)

            buffer = io.BytesIO()
            segment.export(buffer, format="wav")
            return buffer.getvalue()

        except ImportError:
            return audio_data
        except Exception as e:
            self.log.error(f"Post-processing failed: {e}")
            return audio_data

    def set_jarvis_preset(self) -> None:
        self.highpass_freq = 200.0
        self.treble_boost_db = 6.0
        self.echo_amount = 0.08

    def set_natural_preset(self) -> None:
        self.highpass_freq = 80.0
        self.treble_boost_db = 2.0
        self.echo_amount = 0.0
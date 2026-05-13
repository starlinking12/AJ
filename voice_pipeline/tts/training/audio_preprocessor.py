"""
J.A.R.V.I.S. Audio Preprocessor
Prepares audio files for voice cloning training.
Normalizes volume, removes silence, resamples.
"""

from pathlib import Path
from typing import Optional

from jarvis_core.logger import Logger


class AudioPreprocessor:
    def __init__(self, target_sample_rate: int = 22050):
        self.log = Logger("AudioPreprocessor")
        self.target_sample_rate = target_sample_rate

    def process(self, input_path: str, output_path: Optional[str] = None) -> Optional[str]:
        if output_path is None:
            input_file = Path(input_path)
            output_path = str(
                input_file.parent / f"{input_file.stem}_processed{input_file.suffix}"
            )

        try:
            from pydub import AudioSegment
            from pydub.effects import normalize, strip_silence

            audio = AudioSegment.from_file(input_path)
            audio = audio.set_frame_rate(self.target_sample_rate)
            audio = audio.set_channels(1)
            audio = normalize(audio)
            audio = strip_silence(audio, silence_thresh=-40, silence_len=200)

            audio.export(output_path, format="wav")

            self.log.info(f"Audio processed: {output_path}")
            return output_path

        except ImportError:
            self.log.warn("pydub not installed. Cannot preprocess audio.")
            return None
        except Exception as e:
            self.log.error(f"Audio preprocessing failed: {e}")
            return None

    def batch_process(self, input_dir: str, output_dir: str) -> int:
        input_path = Path(input_dir)
        output_path = Path(output_dir)
        output_path.mkdir(parents=True, exist_ok=True)

        processed = 0
        for audio_file in input_path.glob("*.wav"):
            out = str(output_path / audio_file.name)
            if self.process(str(audio_file), out):
                processed += 1

        self.log.info(f"Batch processed: {processed} files")
        return processed
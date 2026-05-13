"""
J.A.R.V.I.S. Dataset Builder
Builds training datasets for voice cloning.
"""

from pathlib import Path
from typing import List, Optional

from jarvis_core.logger import Logger


class DatasetBuilder:
    def __init__(self, output_dir: Optional[str] = None):
        self.log = Logger("DatasetBuilder")
        if output_dir is None:
            output_dir = Path(__file__).resolve().parent.parent / "models" / "training_data"
        self.output_dir = Path(output_dir)
        self.output_dir.mkdir(parents=True, exist_ok=True)

    def build_from_audio_files(
        self,
        audio_files: List[str],
        transcriptions: List[str]
    ) -> bool:
        if len(audio_files) != len(transcriptions):
            self.log.error("Audio files and transcriptions count mismatch.")
            return False

        try:
            import json

            metadata = []
            for i, (audio_path, text) in enumerate(zip(audio_files, transcriptions)):
                dest = self.output_dir / f"sample_{i:04d}.wav"
                import shutil
                shutil.copy(audio_path, dest)
                metadata.append({
                    "audio": str(dest.name),
                    "text": text
                })

            with open(self.output_dir / "metadata.json", "w") as f:
                json.dump(metadata, f, indent=2)

            self.log.info(f"Dataset built: {len(metadata)} samples")
            return True

        except Exception as e:
            self.log.error(f"Dataset build failed: {e}")
            return False

    def get_sample_count(self) -> int:
        metadata_path = self.output_dir / "metadata.json"
        if not metadata_path.exists():
            return 0
        import json
        with open(metadata_path, "r") as f:
            data = json.load(f)
        return len(data)
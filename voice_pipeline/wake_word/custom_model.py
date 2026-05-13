"""
J.A.R.V.I.S. Custom Wake Word Model
Handles loading and managing custom .ppn wake word files.
"""

from pathlib import Path
from typing import Optional

from jarvis_core.logger import Logger


class CustomWakeWordModel:
    def __init__(self, model_dir: Optional[str] = None):
        self.log = Logger("CustomModel")
        if model_dir is None:
            model_dir = Path(__file__).resolve().parent / "models"
        self.model_dir = Path(model_dir)
        self._loaded_models = {}

    def load_model(self, name: str) -> Optional[str]:
        if name in self._loaded_models:
            return self._loaded_models[name]

        model_path = self.model_dir / f"{name}.ppn"
        if model_path.exists():
            self._loaded_models[name] = str(model_path)
            self.log.info(f"Custom model loaded: {name}")
            return str(model_path)

        self.log.warn(f"Custom model not found: {name}")
        return None

    def list_available_models(self) -> list:
        if not self.model_dir.exists():
            return []
        return [
            f.stem for f in self.model_dir.glob("*.ppn")
        ]

    def add_model(self, name: str, file_path: str) -> bool:
        import shutil
        try:
            dest = self.model_dir / f"{name}.ppn"
            self.model_dir.mkdir(parents=True, exist_ok=True)
            shutil.copy(file_path, dest)
            self.log.info(f"Model added: {name}")
            return True
        except Exception as e:
            self.log.error(f"Failed to add model {name}: {e}")
            return False
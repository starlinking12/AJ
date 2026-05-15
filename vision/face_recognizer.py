"""
J.A.R.V.I.S. Vision Face Recognizer
Identifies users by facial embedding.
"""

from pathlib import Path
from typing import Dict, Any, Optional, List

from jarvis_core.logger import Logger


class VisionFaceRecognizer:
    def __init__(self):
        self.log = Logger("VisionFaceRecognizer")
        self._initialized = False
        self._known_faces: Dict[str, Any] = {}
        self._face_dir = Path(__file__).resolve().parent.parent / "data" / "faces"

    def initialize(self) -> bool:
        self._face_dir.mkdir(parents=True, exist_ok=True)
        self._load_known_faces()
        self._initialized = True
        self.log.info(f"Vision face recognizer ready. Known faces: {len(self._known_faces)}")
        return True

    def _load_known_faces(self) -> None:
        for face_file in self._face_dir.glob("*.jpg"):
            name = face_file.stem
            self._known_faces[name] = {
                "path": str(face_file),
                "embedding": None,
            }

    def recognize(self, frame) -> List[Dict[str, Any]]:
        return [{"name": "Unknown", "confidence": 0.0}]

    def enroll(self, name: str, image_path: str) -> bool:
        import shutil
        try:
            dest = self._face_dir / f"{name}.jpg"
            shutil.copy(image_path, dest)
            self._known_faces[name] = {"path": str(dest), "embedding": None}
            self.log.info(f"Face enrolled: {name}")
            return True
        except Exception as e:
            self.log.error(f"Face enrollment failed: {e}")
            return False

    def remove_face(self, name: str) -> bool:
        face_file = self._face_dir / f"{name}.jpg"
        if face_file.exists():
            face_file.unlink()
            self._known_faces.pop(name, None)
            return True
        return False

    def list_known_faces(self) -> List[str]:
        return list(self._known_faces.keys())
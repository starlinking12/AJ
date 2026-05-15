"""
J.A.R.V.I.S. Face Recognizer
Recognizes known faces from the camera feed.
"""

from pathlib import Path
from typing import List, Dict, Any, Optional

from jarvis_core.logger import Logger


class FaceRecognizer:
    def __init__(self):
        self.log = Logger("FaceRecognizer")
        self._initialized = False
        self._known_faces: Dict[str, Any] = {}
        self._face_dir = Path(__file__).resolve().parent.parent.parent / "data" / "faces"

    def initialize(self) -> bool:
        self._face_dir.mkdir(parents=True, exist_ok=True)
        self._initialized = True
        self.log.info("Face recognizer ready.")
        return True

    def recognize(self, frame: Any, faces: List[Dict]) -> List[Dict]:
        results = []
        for face in faces:
            results.append({
                "face_id": face.get("id", 0),
                "name": "Unknown",
                "confidence": 0.0,
            })
        return results

    def register_face(self, name: str, image_path: str) -> bool:
        import shutil
        try:
            dest = self._face_dir / f"{name}.jpg"
            shutil.copy(image_path, dest)
            self._known_faces[name] = str(dest)
            self.log.info(f"Face registered: {name}")
            return True
        except Exception as e:
            self.log.error(f"Face registration failed: {e}")
            return False

    def list_known_faces(self) -> List[str]:
        return [f.stem for f in self._face_dir.glob("*.jpg")]

    def remove_face(self, name: str) -> bool:
        face_file = self._face_dir / f"{name}.jpg"
        if face_file.exists():
            face_file.unlink()
            self._known_faces.pop(name, None)
            return True
        return False
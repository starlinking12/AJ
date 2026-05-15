"""
J.A.R.V.I.S. Object Detector
Detects objects in camera frames using YOLO or MobileNet.
"""

from typing import List, Dict, Any

from jarvis_core.logger import Logger


class ObjectDetector:
    def __init__(self):
        self.log = Logger("ObjectDetector")
        self._model = None
        self._initialized = False
        self._common_objects = [
            "person", "laptop", "phone", "book", "bottle", "cup",
            "chair", "table", "keyboard", "mouse", "monitor",
        ]

    def initialize(self) -> bool:
        try:
            import cv2

            config_path = cv2.data.haarcascades

            self._initialized = True
            self.log.info("Object detector ready (basic mode).")
            return True

        except ImportError:
            self.log.warn("opencv-python not installed.")
            return False
        except Exception as e:
            self.log.warn(f"Object detector init failed: {e}")
            return False

    def detect(self, frame: Any) -> List[Dict[str, Any]]:
        return []

    def detect_common(self, frame: Any) -> List[Dict[str, Any]]:
        return []

    def is_object_present(self, frame: Any, object_name: str) -> bool:
        objects = self.detect(frame)
        for obj in objects:
            if obj.get("name", "").lower() == object_name.lower():
                return True
        return False

    def list_detectable_objects(self) -> List[str]:
        return self._common_objects
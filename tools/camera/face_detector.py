"""
J.A.R.V.I.S. Face Detector
Detects faces in camera frames using OpenCV.
"""

from typing import List, Dict, Any

from jarvis_core.logger import Logger


class FaceDetector:
    def __init__(self):
        self.log = Logger("FaceDetector")
        self._classifier = None
        self._initialized = False

    def initialize(self) -> bool:
        try:
            import cv2

            cascade_path = cv2.data.haarcascades + "haarcascade_frontalface_default.xml"
            self._classifier = cv2.CascadeClassifier(cascade_path)

            if self._classifier.empty():
                self.log.error("Failed to load face cascade classifier.")
                return False

            self._initialized = True
            self.log.info("Face detector ready.")
            return True

        except ImportError:
            self.log.warn("opencv-python not installed.")
            return False
        except Exception as e:
            self.log.warn(f"Face detector init failed: {e}")
            return False

    def detect(self, frame: Any) -> List[Dict[str, Any]]:
        if not self._initialized or self._classifier is None:
            return []

        try:
            import cv2

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            faces = self._classifier.detectMultiScale(
                gray,
                scaleFactor=1.1,
                minNeighbors=5,
                minSize=(30, 30),
            )

            results = []
            for i, (x, y, w, h) in enumerate(faces):
                results.append({
                    "id": i,
                    "x": int(x),
                    "y": int(y),
                    "width": int(w),
                    "height": int(h),
                    "center_x": int(x + w / 2),
                    "center_y": int(y + h / 2),
                })

            return results

        except Exception as e:
            self.log.error(f"Face detection failed: {e}")
            return []

    def draw_faces(self, frame: Any, faces: List[Dict]) -> Any:
        try:
            import cv2

            for face in faces:
                x, y, w, h = face["x"], face["y"], face["width"], face["height"]
                cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 212, 255), 2)

            return frame
        except Exception:
            return frame
"""
J.A.R.V.I.S. OpenCV Capture
Handles webcam capture using OpenCV.
"""

from typing import Optional, Any

from jarvis_core.logger import Logger


class OpenCVCapture:
    def __init__(self, camera_index: int = 0):
        self.log = Logger("OpenCVCapture")
        self.camera_index = camera_index
        self._cap = None
        self._initialized = False

    def initialize(self) -> bool:
        try:
            import cv2

            self._cap = cv2.VideoCapture(self.camera_index)
            if not self._cap.isOpened():
                self.log.error(f"Cannot open camera {self.camera_index}")
                return False

            self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self._cap.set(cv2.CAP_PROP_FPS, 30)

            self._initialized = True
            self.log.info(f"Camera {self.camera_index} initialized.")
            return True

        except ImportError:
            self.log.warn("opencv-python not installed.")
            return False
        except Exception as e:
            self.log.error(f"Camera init failed: {e}")
            return False

    def read(self) -> Optional[Any]:
        if not self._initialized or self._cap is None:
            return None

        try:
            ret, frame = self._cap.read()
            if ret:
                return frame
            return None
        except Exception as e:
            self.log.error(f"Frame read failed: {e}")
            return None

    def get_property(self, prop_id: int) -> Optional[float]:
        if self._cap is None:
            return None
        return self._cap.get(prop_id)

    def set_property(self, prop_id: int, value: float) -> bool:
        if self._cap is None:
            return False
        return self._cap.set(prop_id, value)

    def release(self) -> None:
        if self._cap:
            self._cap.release()
            self._cap = None
        self._initialized = False
        self.log.info("Camera released.")
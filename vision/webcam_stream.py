"""
J.A.R.V.I.S. Webcam Stream
Handles webcam streaming for real-time vision analysis.
"""

from typing import Optional, Any, Callable

from jarvis_core.logger import Logger


class WebcamStream:
    def __init__(self, camera_index: int = 0):
        self.log = Logger("WebcamStream")
        self.camera_index = camera_index
        self._cap = None
        self._initialized = False
        self._running = False
        self._on_frame: Optional[Callable] = None

    def initialize(self) -> bool:
        try:
            import cv2

            self._cap = cv2.VideoCapture(self.camera_index)
            if not self._cap.isOpened():
                self.log.error(f"Cannot open camera {self.camera_index}")
                return False

            self._cap.set(cv2.CAP_PROP_FRAME_WIDTH, 640)
            self._cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 480)
            self._initialized = True
            self.log.info(f"Webcam stream ready. Camera: {self.camera_index}")
            return True

        except ImportError:
            self.log.warn("opencv-python not installed.")
            return False
        except Exception as e:
            self.log.error(f"Webcam stream init failed: {e}")
            return False

    def set_frame_callback(self, callback: Callable) -> None:
        self._on_frame = callback

    def read(self) -> Optional[Any]:
        if not self._initialized or self._cap is None:
            return None

        try:
            ret, frame = self._cap.read()
            if ret:
                if self._on_frame:
                    self._on_frame(frame)
                return frame
            return None
        except Exception as e:
            self.log.error(f"Frame read failed: {e}")
            return None

    def start(self) -> None:
        self._running = True
        self.log.info("Webcam stream started.")

    def stop(self) -> None:
        self._running = False
        self.log.info("Webcam stream stopped.")

    def release(self) -> None:
        self.stop()
        if self._cap:
            self._cap.release()
            self._cap = None
        self._initialized = False
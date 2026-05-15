"""
J.A.R.V.I.S. Camera Manager
Controls camera operations. Open, close, capture, analyze.
Camera activates ONLY on command. Never watches without being asked.
"""

from typing import Dict, Any, Optional, Callable

from tools.camera.opencv_capture import OpenCVCapture
from tools.camera.face_detector import FaceDetector
from tools.camera.face_recognizer import FaceRecognizer
from tools.camera.object_detector import ObjectDetector
from tools.camera.motion_detector import MotionDetector
from tools.camera.snapshot import Snapshot
from tools.camera.streaming_server import StreamingServer

from jarvis_core.logger import Logger


class CameraManager:
    """
    Manages all camera operations.
    Camera is OFF by default. Only activates when user commands.
    """

    def __init__(self):
        self.log = Logger("CameraManager")
        self.capture = OpenCVCapture()
        self.face_detector = FaceDetector()
        self.face_recognizer = FaceRecognizer()
        self.object_detector = ObjectDetector()
        self.motion_detector = MotionDetector()
        self.snapshot = Snapshot()
        self.streaming = StreamingServer()
        self._active = False
        self._initialized = False

    def initialize(self) -> bool:
        self._initialized = True
        self.log.info("Camera manager ready. Camera is OFF.")
        return True

    def open(self) -> bool:
        if self._active:
            self.log.warn("Camera is already open.")
            return True

        if self.capture.initialize():
            self._active = True
            self.log.info("Camera opened.")
            return True

        self.log.error("Failed to open camera.")
        return False

    def close(self) -> bool:
        if not self._active:
            return True

        self.capture.release()
        self._active = False
        self.log.info("Camera closed.")
        return True

    def is_active(self) -> bool:
        return self._active

    def get_frame(self) -> Optional[Any]:
        if not self._active:
            return None
        return self.capture.read()

    def detect_faces(self) -> Dict[str, Any]:
        if not self._active:
            return {"error": "Camera is not active."}

        frame = self.capture.read()
        if frame is None:
            return {"error": "No frame available."}

        faces = self.face_detector.detect(frame)
        return {"faces": faces, "count": len(faces)}

    def detect_objects(self) -> Dict[str, Any]:
        if not self._active:
            return {"error": "Camera is not active."}

        frame = self.capture.read()
        if frame is None:
            return {"error": "No frame available."}

        objects = self.object_detector.detect(frame)
        return {"objects": objects, "count": len(objects)}

    def detect_motion(self) -> Dict[str, Any]:
        if not self._active:
            return {"error": "Camera is not active."}

        frame = self.capture.read()
        if frame is None:
            return {"error": "No frame available."}

        motion_detected = self.motion_detector.detect(frame)
        return {"motion_detected": motion_detected}

    def take_snapshot(self) -> Optional[str]:
        if not self._active:
            frame = self.capture.read()
            if frame is not None:
                return self.snapshot.save(frame)
            return None

        frame = self.capture.read()
        if frame is not None:
            return self.snapshot.save(frame)
        return None

    def recognize_face(self) -> Dict[str, Any]:
        if not self._active:
            return {"error": "Camera is not active."}

        frame = self.capture.read()
        if frame is None:
            return {"error": "No frame available."}

        faces = self.face_detector.detect(frame)
        if not faces:
            return {"recognized": [], "message": "No faces detected."}

        recognized = self.face_recognizer.recognize(frame, faces)
        return {"recognized": recognized}

    def start_streaming(self, port: int = 8080) -> bool:
        if not self._active:
            self.open()

        return self.streaming.start(self.capture, port)

    def stop_streaming(self) -> None:
        self.streaming.stop()
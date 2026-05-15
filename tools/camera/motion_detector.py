"""
J.A.R.V.I.S. Motion Detector
Detects motion by comparing consecutive frames.
"""

from typing import Any

from jarvis_core.logger import Logger


class MotionDetector:
    def __init__(self, threshold: int = 25):
        self.log = Logger("MotionDetector")
        self.threshold = threshold
        self._previous_frame = None
        self._initialized = False

    def initialize(self) -> bool:
        self._initialized = True
        self.log.info("Motion detector ready.")
        return True

    def detect(self, frame: Any) -> bool:
        if not self._initialized:
            return False

        try:
            import cv2
            import numpy as np

            gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
            gray = cv2.GaussianBlur(gray, (21, 21), 0)

            if self._previous_frame is None:
                self._previous_frame = gray
                return False

            frame_delta = cv2.absdiff(self._previous_frame, gray)
            thresh = cv2.threshold(frame_delta, self.threshold, 255, cv2.THRESH_BINARY)[1]
            thresh = cv2.dilate(thresh, None, iterations=2)

            contours, _ = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

            motion_detected = False
            for contour in contours:
                if cv2.contourArea(contour) > 500:
                    motion_detected = True
                    break

            self._previous_frame = gray
            return motion_detected

        except ImportError:
            return False
        except Exception as e:
            self.log.error(f"Motion detection failed: {e}")
            return False

    def reset(self) -> None:
        self._previous_frame = None
"""
J.A.R.V.I.S. Endpoint Detection
Determines when a speech segment has ended based on silence duration.
"""

import time

from jarvis_core.logger import Logger


class EndpointDetector:
    def __init__(self, silence_threshold_seconds: float = 1.0):
        self.log = Logger("EndpointDetector")
        self.silence_threshold = silence_threshold_seconds
        self.is_speaking = False
        self._speech_start_time: float = 0.0
        self._last_speech_time: float = 0.0
        self._silence_start_time: float = 0.0
        self._silence_detected = False

    def speech_started(self) -> None:
        self.is_speaking = True
        self._speech_start_time = time.time()
        self._last_speech_time = time.time()
        self._silence_detected = False

    def speech_continued(self) -> None:
        self._last_speech_time = time.time()
        self._silence_detected = False

    def silence_detected(self) -> None:
        if not self._silence_detected:
            self._silence_start_time = time.time()
            self._silence_detected = True

    def is_speech_complete(self) -> bool:
        if not self.is_speaking:
            return False
        if not self._silence_detected:
            return False

        silence_duration = time.time() - self._silence_start_time
        return silence_duration >= self.silence_threshold

    def speech_ended(self) -> None:
        duration = time.time() - self._speech_start_time
        self.log.debug(f"Speech segment ended. Duration: {duration:.2f}s")
        self.is_speaking = False
        self._silence_detected = False

    def reset(self) -> None:
        self.is_speaking = False
        self._speech_start_time = 0.0
        self._last_speech_time = 0.0
        self._silence_start_time = 0.0
        self._silence_detected = False

    def get_speech_duration(self) -> float:
        if self._speech_start_time == 0.0:
            return 0.0
        if self.is_speaking:
            return time.time() - self._speech_start_time
        return self._last_speech_time - self._speech_start_time
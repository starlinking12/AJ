"""
J.A.R.V.I.S. Wake Word Detector
Listens continuously for the wake word and triggers activation.
"""

import threading
import time
from typing import Callable, Optional

from voice_pipeline.wake_word.openwakeword_engine import OpenWakeWordEngine
from voice_pipeline.wake_word.porcupine_engine import PorcupineEngine
from voice_pipeline.wake_word.sensitivity import Sensitivity
from voice_pipeline.wake_word.calibration import Calibration

from jarvis_core.logger import Logger


class WakeWordDetector:
    """
    Continuous wake word listener.
    Runs in a background thread. Emits callback when wake word is detected.
    """

    def __init__(self, wake_words: list = None, sensitivity: float = 0.5):
        self.log = Logger("WakeWordDetector")
        self.wake_words = wake_words or ["wake up"]
        self.sensitivity = Sensitivity(sensitivity)
        self.calibration = Calibration()
        self._engine = None
        self._callback: Optional[Callable] = None
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._detected = False

    def initialize(self) -> bool:
        self.log.info("Initializing wake word detector...")

        try:
            self._engine = PorcupineEngine(
                keywords=self.wake_words,
                sensitivity=self.sensitivity.value
            )
            if self._engine.initialize():
                self.log.info("Porcupine engine initialized.")
                return True
        except Exception as e:
            self.log.warn(f"Porcupine unavailable: {e}")

        try:
            self._engine = OpenWakeWordEngine(
                keywords=self.wake_words,
                sensitivity=self.sensitivity.value
            )
            if self._engine.initialize():
                self.log.info("OpenWakeWord engine initialized.")
                return True
        except Exception as e:
            self.log.warn(f"OpenWakeWord unavailable: {e}")

        self.log.error("No wake word engine available.")
        return False

    def set_callback(self, callback: Callable) -> None:
        self._callback = callback

    def start(self) -> None:
        if self._engine is None:
            self.log.error("Cannot start: no engine initialized.")
            return

        self._running = True
        self._thread = threading.Thread(target=self._listen_loop, daemon=True)
        self._thread.start()
        self.log.info(f"Wake word detector started. Listening for: {self.wake_words}")

    def stop(self) -> None:
        self._running = False
        if self._thread:
            self._thread.join(timeout=3)
        if self._engine:
            self._engine.release()
        self.log.info("Wake word detector stopped.")

    def _listen_loop(self) -> None:
        cooldown_frames = int(1.5 * 100)
        cooldown_counter = 0

        while self._running:
            try:
                detected = self._engine.process_frame()

                if cooldown_counter > 0:
                    cooldown_counter -= 1
                    continue

                if detected:
                    self.log.info("Wake word detected.")
                    cooldown_counter = cooldown_frames
                    if self._callback:
                        threading.Thread(target=self._callback, daemon=True).start()

                time.sleep(0.01)

            except Exception as e:
                self.log.error(f"Error in listen loop: {e}")
                time.sleep(0.1)

    def adjust_sensitivity(self, value: float) -> None:
        self.sensitivity.set(value)
        if self._engine:
            self._engine.set_sensitivity(value)
        self.log.info(f"Sensitivity adjusted to {value}")

    def calibrate(self, duration_seconds: int = 10) -> float:
        noise_level = self.calibration.measure_ambient_noise(duration_seconds)
        optimal_sensitivity = self.calibration.calculate_optimal_sensitivity(noise_level)
        self.adjust_sensitivity(optimal_sensitivity)
        return optimal_sensitivity
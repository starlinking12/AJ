"""
J.A.R.V.I.S. Wake Word Calibration
Measures ambient noise and calculates optimal sensitivity.
"""

import struct
import time
from typing import Optional

import pyaudio

from jarvis_core.logger import Logger


class Calibration:
    def __init__(self):
        self.log = Logger("Calibration")
        self._audio: Optional[pyaudio.PyAudio] = None

    def measure_ambient_noise(self, duration_seconds: int = 10) -> float:
        self.log.info(f"Measuring ambient noise for {duration_seconds} seconds...")

        audio = pyaudio.PyAudio()
        stream = audio.open(
            rate=16000,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=1024
        )

        total_energy = 0.0
        frames_recorded = 0
        end_time = time.time() + duration_seconds

        while time.time() < end_time:
            try:
                data = stream.read(1024, exception_on_overflow=False)
                samples = struct.unpack_from("h" * 1024, data)
                energy = sum(abs(s) for s in samples) / len(samples)
                total_energy += energy
                frames_recorded += 1
            except Exception:
                break

        stream.stop_stream()
        stream.close()
        audio.terminate()

        if frames_recorded == 0:
            self.log.warn("No audio frames recorded during calibration.")
            return 100.0

        avg_noise = total_energy / frames_recorded
        self.log.info(f"Ambient noise level: {avg_noise:.2f}")
        return avg_noise

    def calculate_optimal_sensitivity(self, noise_level: float) -> float:
        if noise_level < 50:
            sensitivity = 0.5
        elif noise_level < 150:
            sensitivity = 0.45
        elif noise_level < 300:
            sensitivity = 0.4
        elif noise_level < 500:
            sensitivity = 0.35
        else:
            sensitivity = 0.3

        self.log.info(f"Optimal sensitivity calculated: {sensitivity}")
        return sensitivity
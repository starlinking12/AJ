"""
J.A.R.V.I.S. Echo Cancellation
Prevents Jarvis from hearing his own voice as a command.
"""

import struct
from typing import Optional

from jarvis_core.logger import Logger


class EchoCancellation:
    def __init__(self, sample_rate: int = 16000, filter_length: int = 100):
        self.log = Logger("EchoCancellation")
        self.sample_rate = sample_rate
        self.filter_length = filter_length
        self._initialized = False
        self._last_output: Optional[bytes] = None

    def initialize(self) -> bool:
        self._initialized = True
        self.log.info("Echo cancellation ready.")
        return True

    def set_reference(self, output_audio: bytes) -> None:
        self._last_output = output_audio

    def cancel(self, input_audio: bytes) -> bytes:
        if not self._initialized or self._last_output is None:
            return input_audio

        try:
            input_samples = list(struct.unpack_from("h" * (len(input_audio) // 2), input_audio))
            output_samples = list(struct.unpack_from("h" * (len(self._last_output) // 2), self._last_output))

            if len(output_samples) > len(input_samples):
                output_samples = output_samples[:len(input_samples)]
            else:
                input_samples = input_samples[:len(output_samples)]

            attenuation = 0.5
            for i in range(len(output_samples)):
                echo_estimate = int(output_samples[i] * attenuation)
                input_samples[i] = input_samples[i] - echo_estimate

            return struct.pack("h" * len(input_samples), *input_samples)

        except Exception as e:
            self.log.error(f"Echo cancellation failed: {e}")
            return input_audio

    def reset(self) -> None:
        self._last_output = None
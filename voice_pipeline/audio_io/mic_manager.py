"""
J.A.R.V.I.S. Microphone Manager
Manages microphone input with device selection and level monitoring.
"""

import struct
import threading
import time
from typing import Callable, Optional

import pyaudio

from jarvis_core.logger import Logger


class MicrophoneManager:
    def __init__(self, sample_rate: int = 16000, chunk_size: int = 1024):
        self.log = Logger("MicManager")
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        self._audio: Optional[pyaudio.PyAudio] = None
        self._stream = None
        self._device_index: Optional[int] = None
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._on_audio: Optional[Callable] = None
        self._muted = False
        self._volume = 1.0

    def initialize(self, device_index: Optional[int] = None) -> bool:
        try:
            self._audio = pyaudio.PyAudio()

            if device_index is None:
                device_index = self._find_default_input()

            self._device_index = device_index
            self._stream = self._audio.open(
                rate=self.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                input=True,
                input_device_index=self._device_index,
                frames_per_buffer=self.chunk_size
            )

            self.log.info(f"Microphone ready. Device: {self._device_index}")
            return True

        except Exception as e:
            self.log.error(f"Microphone init failed: {e}")
            return False

    def set_callback(self, callback: Callable[[bytes], None]) -> None:
        self._on_audio = callback

    def start(self) -> None:
        if self._stream is None:
            self.log.error("Microphone not initialized.")
            return

        self._running = True
        self._thread = threading.Thread(target=self._capture_loop, daemon=True)
        self._thread.start()
        self.log.info("Microphone capture started.")

    def stop(self) -> None:
        self._running = False
        if self._thread:
            self._thread.join(timeout=3)
        self.log.info("Microphone capture stopped.")

    def read_chunk(self) -> Optional[bytes]:
        if self._stream is None or self._muted:
            return None

        try:
            data = self._stream.read(self.chunk_size, exception_on_overflow=False)
            if self._volume != 1.0:
                data = self._apply_volume(data)
            return data
        except Exception as e:
            self.log.error(f"Mic read error: {e}")
            return None

    def _capture_loop(self) -> None:
        while self._running:
            data = self.read_chunk()
            if data and self._on_audio:
                self._on_audio(data)
            time.sleep(0.001)

    def mute(self) -> None:
        self._muted = True
        self.log.info("Microphone muted.")

    def unmute(self) -> None:
        self._muted = False
        self.log.info("Microphone unmuted.")

    def set_volume(self, volume: float) -> None:
        self._volume = max(0.0, min(2.0, volume))

    def _apply_volume(self, data: bytes) -> bytes:
        samples = struct.unpack_from("h" * (len(data) // 2), data)
        adjusted = [int(s * self._volume) for s in samples]
        return struct.pack("h" * len(adjusted), *adjusted)

    def _find_default_input(self) -> Optional[int]:
        if self._audio is None:
            return None
        try:
            default = self._audio.get_default_input_device_info()
            return default.get("index")
        except Exception:
            return None

    def get_level(self) -> float:
        data = self.read_chunk()
        if data is None:
            return 0.0
        samples = struct.unpack_from("h" * (len(data) // 2), data)
        return sum(abs(s) for s in samples) / len(samples)

    def release(self) -> None:
        self.stop()
        if self._stream:
            self._stream.stop_stream()
            self._stream.close()
            self._stream = None
        if self._audio:
            self._audio.terminate()
            self._audio = None
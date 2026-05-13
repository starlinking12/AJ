"""
J.A.R.V.I.S. Speaker Manager
Manages audio output with device selection and playback control.
"""

import struct
import threading
import time
from collections import deque
from typing import Optional

import pyaudio

from jarvis_core.logger import Logger


class SpeakerManager:
    def __init__(self, sample_rate: int = 22050, chunk_size: int = 1024):
        self.log = Logger("SpeakerManager")
        self.sample_rate = sample_rate
        self.chunk_size = chunk_size
        self._audio: Optional[pyaudio.PyAudio] = None
        self._stream = None
        self._device_index: Optional[int] = None
        self._queue = deque()
        self._running = False
        self._thread: Optional[threading.Thread] = None
        self._volume = 1.0
        self._is_playing = False

    def initialize(self, device_index: Optional[int] = None) -> bool:
        try:
            self._audio = pyaudio.PyAudio()

            if device_index is None:
                device_index = self._find_default_output()

            self._device_index = device_index
            self._stream = self._audio.open(
                rate=self.sample_rate,
                channels=1,
                format=pyaudio.paInt16,
                output=True,
                output_device_index=self._device_index,
                frames_per_buffer=self.chunk_size
            )

            self.log.info(f"Speaker ready. Device: {self._device_index}")
            return True

        except Exception as e:
            self.log.error(f"Speaker init failed: {e}")
            return False

    def start(self) -> None:
        self._running = True
        self._thread = threading.Thread(target=self._playback_loop, daemon=True)
        self._thread.start()
        self.log.info("Speaker playback started.")

    def stop(self) -> None:
        self._running = False
        if self._thread:
            self._thread.join(timeout=3)
        self.log.info("Speaker playback stopped.")

    def play(self, audio_data: bytes) -> None:
        self._queue.append(audio_data)

    def play_immediate(self, audio_data: bytes) -> None:
        if self._stream is None:
            return

        try:
            if self._volume != 1.0:
                samples = struct.unpack_from("h" * (len(audio_data) // 2), audio_data)
                adjusted = [int(s * self._volume) for s in samples]
                audio_data = struct.pack("h" * len(adjusted), *adjusted)

            self._stream.write(audio_data)
        except Exception as e:
            self.log.error(f"Playback error: {e}")

    def _playback_loop(self) -> None:
        while self._running:
            if self._queue:
                self._is_playing = True
                audio_data = self._queue.popleft()
                self.play_immediate(audio_data)
                self._is_playing = False
            else:
                time.sleep(0.01)

    def set_volume(self, volume: float) -> None:
        self._volume = max(0.0, min(1.0, volume))

    def is_playing(self) -> bool:
        return self._is_playing or len(self._queue) > 0

    def clear_queue(self) -> None:
        self._queue.clear()

    def _find_default_output(self) -> Optional[int]:
        if self._audio is None:
            return None
        try:
            default = self._audio.get_default_output_device_info()
            return default.get("index")
        except Exception:
            return None

    def release(self) -> None:
        self.stop()
        if self._stream:
            self._stream.stop_stream()
            self._stream.close()
            self._stream = None
        if self._audio:
            self._audio.terminate()
            self._audio = None
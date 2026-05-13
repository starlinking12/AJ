"""
J.A.R.V.I.S. TTS Synthesizer
Main text-to-speech interface. Routes text to the best available engine.
Supports Piper (primary), XTTS (secondary), and MeloTTS (fallback).
"""

import threading
from typing import Callable, Optional

from voice_pipeline.tts.piper_engine import PiperEngine
from voice_pipeline.tts.xtts_engine import XTTSEngine
from voice_pipeline.tts.streaming_synthesizer import StreamingSynthesizer
from voice_pipeline.tts.audio_postprocessor import AudioPostProcessor
from voice_pipeline.tts.pitch_modulator import PitchModulator
from voice_pipeline.tts.speed_controller import SpeedController
from voice_pipeline.tts.emotion_injector import EmotionInjector

from jarvis_core.config.loader import Config
from jarvis_core.logger import Logger


class Synthesizer:
    """
    Converts text to spoken audio.
    Primary engine: Piper TTS (fast, local, British voice).
    Secondary: XTTS (high quality voice cloning).
    Fallback: MeloTTS.
    """

    def __init__(self, config: Config):
        self.log = Logger("Synthesizer")
        self.config = config
        self.engine_name = getattr(config, 'tts_engine', 'piper')
        self.voice_model = getattr(config, 'tts_voice', 'jarvis_british_male')
        self._engine = None
        self._streaming = StreamingSynthesizer()
        self._postprocessor = AudioPostProcessor()
        self._pitch = PitchModulator()
        self._speed = SpeedController()
        self._emotion = EmotionInjector()
        self._initialized = False
        self._on_speech_start: Optional[Callable] = None
        self._on_speech_end: Optional[Callable] = None

    def initialize(self) -> bool:
        self.log.info(f"Initializing TTS (engine: {self.engine_name})...")

        if self.engine_name == "piper":
            self._engine = PiperEngine(voice=self.voice_model)
        elif self.engine_name == "xtts":
            self._engine = XTTSEngine(voice=self.voice_model)
        else:
            self._engine = PiperEngine(voice=self.voice_model)

        if self._engine.initialize():
            self._initialized = True
            self.log.info(f"TTS engine ready: {self.engine_name}")
            return True

        self.log.warn(f"{self.engine_name} failed. Trying Piper fallback...")
        self._engine = PiperEngine(voice="jarvis_british_male")
        if self._engine.initialize():
            self._initialized = True
            self.log.info("Fallback to Piper TTS successful.")
            return True

        self.log.error("No TTS engine available.")
        return False

    def set_callbacks(
        self,
        on_start: Optional[Callable] = None,
        on_end: Optional[Callable] = None
    ) -> None:
        self._on_speech_start = on_start
        self._on_speech_end = on_end

    def synthesize(self, text: str, speed: float = 1.0, pitch: float = 1.0) -> bytes:
        if not self._initialized or self._engine is None:
            self.log.error("Synthesizer not initialized.")
            return b""

        text = self._emotion.process(text)

        audio = self._engine.synthesize(text)

        audio = self._pitch.modulate(audio, pitch)
        audio = self._speed.adjust(audio, speed)
        audio = self._postprocessor.process(audio)

        return audio

    def synthesize_streaming(self, text: str) -> Optional[bytes]:
        if not self._initialized or self._engine is None:
            return None

        chunk = self._streaming.process_text(text)
        if chunk:
            chunk = self._postprocessor.process(chunk)
        return chunk

    def speak(self, text: str, speed: float = 1.0, pitch: float = 1.0) -> None:
        if self._on_speech_start:
            self._on_speech_start()

        audio = self.synthesize(text, speed, pitch)

        if audio:
            self._play_audio(audio)

        if self._on_speech_end:
            self._on_speech_end()

    def _play_audio(self, audio: bytes) -> None:
        try:
            import pyaudio
            import wave
            import tempfile
            from pathlib import Path

            with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as f:
                temp_path = f.name
                with wave.open(f, "wb") as wf:
                    wf.setnchannels(1)
                    wf.setsampwidth(2)
                    wf.setframerate(22050)
                    wf.writeframes(audio)

            import subprocess
            import platform

            system = platform.system()
            if system == "Darwin":
                subprocess.run(["afplay", temp_path])
            elif system == "Linux":
                subprocess.run(["aplay", temp_path])
            elif system == "Windows":
                import winsound
                winsound.PlaySound(temp_path, winsound.SND_FILENAME)

            Path(temp_path).unlink(missing_ok=True)

        except Exception as e:
            self.log.error(f"Audio playback failed: {e}")

    def set_voice(self, voice_name: str) -> bool:
        if self._engine:
            return self._engine.set_voice(voice_name)
        return False

    def get_available_voices(self) -> list:
        if self._engine:
            return self._engine.get_available_voices()
        return []
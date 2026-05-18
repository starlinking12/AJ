"""Tests for text-to-speech."""

import pytest
from voice_pipeline.tts.emotion_injector import EmotionInjector
from voice_pipeline.tts.streaming_synthesizer import StreamingSynthesizer


class TestEmotionInjector:
    def test_process_basic(self):
        ei = EmotionInjector()
        result = ei.process("Hello Sir.")
        assert len(result) > 0

    def test_normalize_text(self):
        ei = EmotionInjector()
        result = ei.process("Good morning, Mr. Smith.")
        assert "Mister" in result

    def test_get_emotions(self):
        ei = EmotionInjector()
        emotions = ei.get_available_emotions()
        assert len(emotions) > 0
        assert "happy" in emotions


class TestStreamingSynthesizer:
    def test_process_text_short(self):
        ss = StreamingSynthesizer(chunk_size=50)
        result = ss.process_text("Hello")
        assert result is None

    def test_process_text_long(self):
        ss = StreamingSynthesizer(chunk_size=10)
        result = ss.process_text("Hello world this is a longer sentence.")
        assert result is not None or ss._buffer != ""

    def test_finalize(self):
        ss = StreamingSynthesizer()
        ss.process_text("Test sentence.")
        final = ss.finalize()
        assert isinstance(final, str)

    def test_reset(self):
        ss = StreamingSynthesizer()
        ss.process_text("Some text here.")
        ss.reset()
        assert ss._buffer == ""
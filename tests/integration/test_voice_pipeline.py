"""Integration tests for the voice pipeline."""

import pytest


class TestVoicePipelineIntegration:
    def test_vad_initializes(self):
        from voice_pipeline.vad.voice_activity_detection import VoiceActivityDetector
        vad = VoiceActivityDetector()
        result = vad.initialize()
        assert result is True

    def test_wake_word_sensitivity_chain(self):
        from voice_pipeline.wake_word.sensitivity import Sensitivity
        from voice_pipeline.wake_word.calibration import Calibration

        sensitivity = Sensitivity(0.5)
        calibration = Calibration()
        optimal = calibration.calculate_optimal_sensitivity(noise_level=100)
        sensitivity.set(optimal)
        assert 0.1 <= sensitivity.value <= 0.9

    def test_stt_tts_chain(self):
        from voice_pipeline.stt.punctuation import PunctuationRestorer
        from voice_pipeline.tts.emotion_injector import EmotionInjector

        pr = PunctuationRestorer()
        pr.initialize()
        text = pr.restore("what is the weather")

        ei = EmotionInjector()
        processed = ei.process(text)
        assert len(processed) > 0
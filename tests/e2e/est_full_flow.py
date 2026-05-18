"""End-to-end test for the full J.A.R.V.I.S. flow."""

import pytest


class TestFullFlow:
    def test_wake_to_response_flow(self):
        from voice_pipeline.wake_word.sensitivity import Sensitivity
        from voice_pipeline.stt.punctuation import PunctuationRestorer
        from brain.intent_classifier.keyword_matcher import KeywordMatcher
        from brain.guardrails.output_validator import OutputValidator
        from voice_pipeline.tts.emotion_injector import EmotionInjector

        wake_sensitivity = Sensitivity(0.5)
        assert 0.1 <= wake_sensitivity.value <= 0.9

        pr = PunctuationRestorer()
        pr.initialize()
        transcribed = pr.restore("what is the weather in london")
        assert len(transcribed) > 0

        matcher = KeywordMatcher()
        matcher.initialize()
        intent, confidence = matcher.match(transcribed)
        assert intent == "weather"

        response = "Current conditions in London show 15 degrees Celsius, Sir."
        validator = OutputValidator()
        validator.initialize()
        validated = validator.validate(response)
        assert "Sir" in validated

        ei = EmotionInjector()
        final = ei.process(validated)
        assert len(final) > 0

    def test_system_command_flow(self):
        from brain.intent_classifier.keyword_matcher import KeywordMatcher
        from brain.guardrails.command_sanitizer import CommandSanitizer
        from brain.guardrails.safety_filter import SafetyFilter

        matcher = KeywordMatcher()
        matcher.initialize()
        intent, _ = matcher.match("open chrome")
        assert intent == "system"

        sanitizer = CommandSanitizer()
        safety = SafetyFilter()

        safe = safety.check_command("open chrome")
        assert safe is True

        sanitized, allowed = sanitizer.sanitize("open chrome")
        assert allowed is True
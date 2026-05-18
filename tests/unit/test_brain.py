"""Tests for brain modules."""

import pytest
from brain.guardrails.output_validator import OutputValidator
from brain.guardrails.safety_filter import SafetyFilter
from brain.fallback_manager import FallbackManager


class TestOutputValidator:
    def test_validate_normal(self):
        ov = OutputValidator()
        ov.initialize()
        result = ov.validate("Hello Sir.")
        assert "Sir" in result

    def test_blocked_phrase(self):
        ov = OutputValidator()
        ov.initialize()
        result = ov.validate("As an AI, I cannot help with that.")
        assert "J.A.R.V.I.S." in result

    def test_adds_sir(self):
        ov = OutputValidator()
        ov.initialize()
        result = ov.validate("Hello")
        assert "Sir" in result

    def test_empty_response(self):
        ov = OutputValidator()
        ov.initialize()
        result = ov.validate("")
        assert len(result) > 0


class TestSafetyFilter:
    def test_safe_text(self):
        sf = SafetyFilter()
        assert sf.check_text("Hello world") is True

    def test_dangerous_command(self):
        sf = SafetyFilter()
        assert sf.check_command("rm -rf /") is False

    def test_safe_command(self):
        sf = SafetyFilter()
        assert sf.check_command("echo hello") is True

    def test_filter_response(self):
        sf = SafetyFilter()
        result = sf.filter_response("rm -rf / should not pass")
        assert "cannot" in result.lower()


class TestFallbackManager:
    def test_get_search_fallback(self):
        fm = FallbackManager()
        response = fm.get_fallback_response("search_offline")
        assert "Sir" in response

    def test_get_llm_timeout(self):
        fm = FallbackManager()
        response = fm.get_fallback_response("llm_timeout")
        assert "Sir" in response

    def test_unknown_error_type(self):
        fm = FallbackManager()
        response = fm.get_fallback_response("unknown_error")
        assert "Sir" in response

    def test_handle_error(self):
        fm = FallbackManager()
        result = fm.handle_error("tool_error", Exception("Test error"))
        assert result["is_fallback"] is True
        assert "text" in result
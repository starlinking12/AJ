"""Integration tests for the brain orchestrator."""

import pytest


class TestBrainIntegration:
    def test_intent_to_template_chain(self):
        from brain.intent_classifier.keyword_matcher import KeywordMatcher
        from brain.prompt_engine.template_manager import TemplateManager

        matcher = KeywordMatcher()
        matcher.initialize()
        intent, _ = matcher.match("hello jarvis")

        templates = TemplateManager()
        greeting = templates.get_greeting_for_time(10)
        assert len(greeting) > 0

    def test_memory_chain(self):
        from brain.memory.short_term import ShortTermMemory
        from brain.memory.working_memory import WorkingMemory

        stm = ShortTermMemory()
        wm = WorkingMemory()

        stm.add("user1", "What is the weather?", "It is sunny, Sir.")
        wm.set("last_intent", "weather")

        recent = stm.get_recent("user1")
        assert len(recent) > 0
        assert wm.get("last_intent") == "weather"

    def test_guardrail_chain(self):
        from brain.guardrails.output_validator import OutputValidator
        from brain.guardrails.safety_filter import SafetyFilter

        validator = OutputValidator()
        validator.initialize()
        safety = SafetyFilter()

        response = validator.validate("Here is the information, Sir.")
        safe = safety.check_text(response)
        assert safe is True
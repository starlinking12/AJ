"""End-to-end test for multi-turn conversations."""

import pytest


class TestMultiTurn:
    def test_conversation_flow(self):
        from brain.memory.short_term import ShortTermMemory
        from brain.memory.working_memory import WorkingMemory
        from brain.intent_classifier.keyword_matcher import KeywordMatcher

        stm = ShortTermMemory()
        wm = WorkingMemory()
        matcher = KeywordMatcher()
        matcher.initialize()

        turns = [
            ("Hello Jarvis", "conversation", "Good morning, Sir."),
            ("What is the weather in Paris", "weather", "Paris is 18 degrees, Sir."),
            ("Thank you", "conversation", "Always a pleasure, Sir."),
        ]

        for user_text, expected_intent, response in turns:
            intent, _ = matcher.match(user_text)
            assert intent == expected_intent

            stm.add("user1", user_text, response)
            wm.set("last_intent", intent)

        history = stm.get_recent("user1")
        assert len(history) >= 4
        assert wm.get("last_intent") == "conversation"

    def test_context_preservation(self):
        from brain.memory.short_term import ShortTermMemory

        stm = ShortTermMemory(max_turns=10)

        stm.add("user1", "Search for Python", "Here are Python results, Sir.")
        stm.add("user1", "Show me the first one", "Opening first result, Sir.")

        history = stm.get_recent("user1", limit=10)
        assert len(history) >= 2

        last_user = ""
        for msg in reversed(history):
            if msg["role"] == "user":
                last_user = msg["content"]
                break

        assert len(last_user) > 0
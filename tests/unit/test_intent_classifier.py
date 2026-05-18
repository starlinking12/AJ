"""Tests for intent classification."""

import pytest
from brain.intent_classifier.keyword_matcher import KeywordMatcher
from brain.intent_classifier.intent_labels import IntentLabels


class TestKeywordMatcher:
    def setup_method(self):
        self.matcher = KeywordMatcher()
        self.matcher.initialize()

    def test_search_intent(self):
        intent, confidence = self.matcher.match("search for python tutorials")
        assert intent == "search"

    def test_weather_intent(self):
        intent, confidence = self.matcher.match("what is the weather today")
        assert intent == "weather"

    def test_news_intent(self):
        intent, confidence = self.matcher.match("show me the headlines")
        assert intent == "news"

    def test_map_intent(self):
        intent, confidence = self.matcher.match("show map of paris")
        assert intent == "map"

    def test_system_intent(self):
        intent, confidence = self.matcher.match("open chrome")
        assert intent == "system"

    def test_camera_intent(self):
        intent, confidence = self.matcher.match("open the camera")
        assert intent == "camera"

    def test_music_intent(self):
        intent, confidence = self.matcher.match("play some jazz")
        assert intent == "music"

    def test_conversation_intent(self):
        intent, confidence = self.matcher.match("hello how are you")
        assert intent == "conversation"

    def test_unknown_returns_conversation(self):
        intent, confidence = self.matcher.match("xyzzy random")
        assert intent == "conversation"


class TestIntentLabels:
    def test_get_all_intents(self):
        labels = IntentLabels()
        intents = labels.get_all_intents()
        assert "search" in intents
        assert "weather" in intents
        assert "news" in intents
        assert "conversation" in intents

    def test_requires_display(self):
        labels = IntentLabels()
        assert labels.requires_display("map") is True
        assert labels.requires_display("conversation") is False

    def test_get_label(self):
        labels = IntentLabels()
        assert labels.get_label("search") == "Web Search"

    def test_get_examples(self):
        labels = IntentLabels()
        examples = labels.get_examples("weather")
        assert len(examples) > 0
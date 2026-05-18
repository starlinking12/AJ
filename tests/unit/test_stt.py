"""Tests for speech-to-text."""

import pytest
from voice_pipeline.stt.punctuation import PunctuationRestorer
from voice_pipeline.stt.hotword_boosting import HotwordBooster
from voice_pipeline.stt.beam_search import BeamSearch
from voice_pipeline.stt.language_model import LanguageModel


class TestPunctuation:
    def test_restore_basic(self):
        pr = PunctuationRestorer()
        pr.initialize()
        result = pr.restore("hello world")
        assert len(result) > 0
        assert result[0].isupper()

    def test_restore_question(self):
        pr = PunctuationRestorer()
        pr.initialize()
        result = pr.restore("what is the weather")
        assert "?" in result

    def test_restore_empty(self):
        pr = PunctuationRestorer()
        result = pr.restore("")
        assert result == ""


class TestHotwordBooster:
    def test_get_boost_list(self):
        booster = HotwordBooster()
        boosts = booster.get_boost_list()
        assert len(boosts) > 0

    def test_add_hotword(self):
        booster = HotwordBooster()
        booster.add_hotword("test", 3.0)
        boost = booster.get_boost_for("test")
        assert boost == 3.0

    def test_get_boost_default(self):
        booster = HotwordBooster()
        boost = booster.get_boost_for("unknown")
        assert boost == 1.0


class TestBeamSearch:
    def test_search_returns_best(self):
        bs = BeamSearch(beam_width=3)
        candidates = [("a", 0.5), ("b", 0.9), ("c", 0.7), ("d", 0.3)]
        result = bs.search(candidates)
        assert len(result) <= 3

    def test_get_best(self):
        bs = BeamSearch()
        bs.search([("winner", 0.99), ("loser", 0.1)])
        best_text, best_score = bs.get_best()
        assert best_text == "winner"


class TestLanguageModel:
    def test_score_text(self):
        lm = LanguageModel()
        lm.initialize()
        score = lm.score("jarvis open chrome")
        assert score > 0.0

    def test_correct_text(self):
        lm = LanguageModel()
        lm.initialize()
        corrected = lm.correct("jarvi wake up")
        assert "Jarvis" in corrected
"""Tests for wake word detection."""

import pytest
from voice_pipeline.wake_word.sensitivity import Sensitivity
from voice_pipeline.wake_word.custom_model import CustomWakeWordModel


class TestSensitivity:
    def test_default_value(self):
        s = Sensitivity()
        assert s.value == 0.5

    def test_clamp_min(self):
        s = Sensitivity(0.0)
        assert s.value == 0.1

    def test_clamp_max(self):
        s = Sensitivity(1.0)
        assert s.value == 0.9

    def test_increase(self):
        s = Sensitivity(0.5)
        s.increase(0.2)
        assert s.value == 0.7

    def test_decrease(self):
        s = Sensitivity(0.5)
        s.decrease(0.2)
        assert s.value == 0.3

    def test_description(self):
        s = Sensitivity(0.5)
        desc = s.to_description()
        assert "Medium" in desc


class TestCustomWakeWordModel:
    def test_list_models_empty(self):
        model = CustomWakeWordModel(model_dir="/tmp/nonexistent")
        models = model.list_available_models()
        assert isinstance(models, list)

    def test_load_nonexistent_model(self):
        model = CustomWakeWordModel(model_dir="/tmp/nonexistent")
        result = model.load_model("nonexistent")
        assert result is None
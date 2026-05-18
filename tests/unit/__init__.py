"""Tests for configuration loading."""

import pytest
from jarvis_core.config.loader import Config
from jarvis_core.config.schema import ConfigSchema


class TestConfig:
    def test_config_loads_defaults(self):
        config = Config.load()
        assert config is not None
        assert config.get("jarvis_name") == "J.A.R.V.I.S."

    def test_config_has_wake_word(self):
        config = Config.load()
        assert "wake up" in config.get("wake_word", "")

    def test_config_has_ollama_host(self):
        config = Config.load()
        assert config.get("ollama_host") is not None

    def test_config_schema_validates(self):
        schema = ConfigSchema({"jarvis_name": "Test"})
        result = schema.validate()
        assert result["jarvis_name"] == "Test"

    def test_config_schema_defaults(self):
        schema = ConfigSchema({})
        result = schema.validate()
        assert result["wake_word"] == "wake up"
        assert result["user_title"] == "Sir"


class TestEnvLoader:
    def test_env_loader_empty(self):
        from jarvis_core.config.env_loader import EnvLoader
        data = EnvLoader.load()
        assert isinstance(data, dict)
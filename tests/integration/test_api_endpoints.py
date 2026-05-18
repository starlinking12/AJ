"""Integration tests for API endpoint patterns."""

import pytest


class TestAPIEndpoints:
    def test_config_api_structure(self):
        from jarvis_core.config.loader import Config
        config = Config.load()

        assert config.get("jarvis_name") is not None
        assert config.get("wake_word") is not None
        assert config.get("ollama_model") is not None

    def test_event_bus_api_pattern(self):
        from jarvis_core.events.event_bus import EventBus
        from jarvis_core.events.event_types import JARVIS_READY

        bus = EventBus()
        results = []

        bus.subscribe(JARVIS_READY, lambda d: results.append(d))
        bus.emit(JARVIS_READY, {"status": "ready"})

        assert len(results) == 1
        assert results[0]["status"] == "ready"
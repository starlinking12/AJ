"""Tests for the event bus system."""

import pytest
from jarvis_core.events.event_bus import EventBus
from jarvis_core.events.event_types import (
    JARVIS_READY, JARVIS_STATE_CHANGED, VOICE_WAKE_WORD_DETECTED
)


class TestEventBus:
    def test_subscribe_and_emit(self, event_bus):
        received = []

        def handler(data):
            received.append(data)

        event_bus.subscribe("test.event", handler)
        event_bus.emit("test.event", {"message": "hello"})

        assert len(received) == 1
        assert received[0]["message"] == "hello"

    def test_multiple_subscribers(self, event_bus):
        results = []

        def handler1(data):
            results.append(1)

        def handler2(data):
            results.append(2)

        event_bus.subscribe("test.multi", handler1)
        event_bus.subscribe("test.multi", handler2)
        event_bus.emit("test.multi", {})

        assert len(results) == 2
        assert 1 in results
        assert 2 in results

    def test_unsubscribe(self, event_bus):
        received = []

        def handler(data):
            received.append(data)

        event_bus.subscribe("test.unsub", handler)
        event_bus.unsubscribe("test.unsub", handler)
        event_bus.emit("test.unsub", {})

        assert len(received) == 0

    def test_event_history(self, event_bus):
        event_bus.emit("test.history", {"value": 42})

        history = event_bus.get_history("test.history")
        assert len(history) == 1
        assert history[0]["data"]["value"] == 42

    def test_jarvis_ready_event(self, event_bus):
        received = []

        def handler(data):
            received.append(data)

        event_bus.subscribe(JARVIS_READY, handler)
        event_bus.emit(JARVIS_READY, {"message": "At your service, Sir."})

        assert len(received) == 1
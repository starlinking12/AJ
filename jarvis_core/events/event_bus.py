"""
J.A.R.V.I.S. Event Bus
Central pub/sub event system for inter-module communication.
"""

from typing import Any, Callable, Dict, List

from jarvis_core.logger import Logger


class EventBus:
    def __init__(self):
        self.log = Logger("EventBus")
        self._listeners: Dict[str, List[Callable]] = {}
        self._history: List[Dict] = []

    def subscribe(self, event_type: str, callback: Callable) -> None:
        if event_type not in self._listeners:
            self._listeners[event_type] = []
        self._listeners[event_type].append(callback)
        self.log.debug(f"Subscribed to {event_type}")

    def unsubscribe(self, event_type: str, callback: Callable) -> None:
        if event_type in self._listeners:
            self._listeners[event_type] = [
                cb for cb in self._listeners[event_type] if cb != callback
            ]
            self.log.debug(f"Unsubscribed from {event_type}")

    def emit(self, event_type: str, data: Dict[str, Any]) -> None:
        event = {
            "type": event_type,
            "data": data
        }
        self._history.append(event)

        if event_type in self._listeners:
            for callback in self._listeners[event_type]:
                try:
                    callback(data)
                except Exception as e:
                    self.log.error(f"Event handler failed for {event_type}: {e}")

        self.log.debug(f"Event emitted: {event_type}")

    def get_history(self, event_type: str = None) -> List[Dict]:
        if event_type:
            return [e for e in self._history if e["type"] == event_type]
        return self._history

    def clear_history(self) -> None:
        self._history = []
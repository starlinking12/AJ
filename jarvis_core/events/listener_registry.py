"""
J.A.R.V.I.S. Listener Registry
Manages event listener registration and lifecycle.
"""

from typing import Dict, List

from jarvis_core.events.event_bus import EventBus
from jarvis_core.logger import Logger


class ListenerRegistry:
    def __init__(self, event_bus: EventBus):
        self.event_bus = event_bus
        self.log = Logger("ListenerRegistry")
        self._registry: Dict[str, List[str]] = {}

    def register(self, module: str, event_type: str, callback) -> None:
        self.event_bus.subscribe(event_type, callback)
        if module not in self._registry:
            self._registry[module] = []
        self._registry[module].append(event_type)
        self.log.info(f"Registered {module} -> {event_type}")

    def unregister_module(self, module: str) -> None:
        if module in self._registry:
            for event_type in self._registry[module]:
                self.event_bus.unsubscribe(event_type, None)
            del self._registry[module]
            self.log.info(f"Unregistered module: {module}")

    def list_listeners(self) -> Dict[str, List[str]]:
        return self._registry.copy()
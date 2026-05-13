"""
J.A.R.V.I.S. Lifecycle Manager
Controls the main run loop and state transitions.
"""

import time
from enum import Enum

from jarvis_core.config.loader import Config
from jarvis_core.events.event_bus import EventBus
from jarvis_core.logger import Logger


class JarvisState(Enum):
    SLEEPING = "sleeping"
    AWAKE = "awake"
    LISTENING = "listening"
    THINKING = "thinking"
    SPEAKING = "speaking"
    TASK = "task"
    ERROR = "error"
    SHUTDOWN = "shutdown"


class LifecycleManager:
    def __init__(self, config: Config, event_bus: EventBus):
        self.config = config
        self.event_bus = event_bus
        self.log = Logger("Lifecycle")
        self.state = JarvisState.SLEEPING
        self._running = False

    def transition_to(self, new_state: JarvisState) -> None:
        old_state = self.state
        self.state = new_state
        self.log.info(f"State: {old_state.value} -> {new_state.value}")
        self.event_bus.emit("jarvis.state_changed", {
            "old": old_state.value,
            "new": new_state.value
        })

    def run(self) -> None:
        self._running = True
        self.transition_to(JarvisState.SLEEPING)
        self.log.info("J.A.R.V.I.S. sleeping. Waiting for 'Wake up'...")

        try:
            while self._running:
                time.sleep(0.1)
        except KeyboardInterrupt:
            self.stop()

    def stop(self) -> None:
        self._running = False
        self.transition_to(JarvisState.SHUTDOWN)
        self.log.info("Lifecycle stopped.")
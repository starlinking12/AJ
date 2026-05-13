"""
J.A.R.V.I.S. Bootloader
Sequentially initializes all system components.
"""

from jarvis_core.config.loader import Config
from jarvis_core.events.event_bus import EventBus
from jarvis_core.logger import Logger


class Bootloader:
    def __init__(self, config: Config, event_bus: EventBus):
        self.config = config
        self.event_bus = event_bus
        self.log = Logger("Bootloader")

    def boot_core(self) -> None:
        self.log.info("Booting core systems...")
        self.event_bus.emit("boot.core.started", {})
        self.event_bus.emit("boot.core.complete", {})

    def boot_voice(self) -> None:
        self.log.info("Booting voice pipeline...")
        self.event_bus.emit("boot.voice.started", {})
        self.event_bus.emit("boot.voice.complete", {})

    def boot_brain(self) -> None:
        self.log.info("Booting brain...")
        self.event_bus.emit("boot.brain.started", {})
        self.event_bus.emit("boot.brain.complete", {})

    def boot_tools(self) -> None:
        self.log.info("Booting tool ecosystem...")
        self.event_bus.emit("boot.tools.started", {})
        self.event_bus.emit("boot.tools.complete", {})

    def boot_ui(self) -> None:
        self.log.info("Booting arc reactor UI...")
        self.event_bus.emit("boot.ui.started", {})
        self.event_bus.emit("boot.ui.complete", {})
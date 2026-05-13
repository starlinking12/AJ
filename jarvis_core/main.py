"""
J.A.R.V.I.S. Core Main
Initializes and runs the J.A.R.V.I.S. core system.
"""

import asyncio
import signal
import sys
from pathlib import Path
from typing import Optional

PROJECT_ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(PROJECT_ROOT))

from jarvis_core.config.loader import Config
from jarvis_core.events.event_bus import EventBus
from jarvis_core.bootloader import Bootloader
from jarvis_core.lifecycle_manager import LifecycleManager
from jarvis_core.crash_handler import CrashHandler
from jarvis_core.logger import Logger


class JARVISCore:
    """
    Core J.A.R.V.I.S. system.
    Initializes all subsystems and manages the main lifecycle.
    """

    def __init__(self):
        self.log = Logger("JARVIS.Core")
        self.config: Optional[Config] = None
        self.event_bus: Optional[EventBus] = None
        self.bootloader: Optional[Bootloader] = None
        self.lifecycle: Optional[LifecycleManager] = None
        self.crash_handler: Optional[CrashHandler] = None
        self._running = False

    def initialize(self) -> None:
        self.log.info("Initializing J.A.R.V.I.S. Core System...")

        self.config = Config.load()
        self.log.info("Configuration loaded.")

        self.event_bus = EventBus()
        self.log.info("Event bus initialized.")

        self.crash_handler = CrashHandler(self.config)
        self.log.info("Crash handler armed.")

        self.bootloader = Bootloader(self.config, self.event_bus)
        self.lifecycle = LifecycleManager(self.config, self.event_bus)
        self.log.info("All subsystems ready.")

    def start(self) -> None:
        self._running = True
        self.log.info("Starting J.A.R.V.I.S. boot sequence...")

        try:
            self.bootloader.boot_core()
            self.bootloader.boot_voice()
            self.bootloader.boot_brain()
            self.bootloader.boot_tools()
            self.bootloader.boot_ui()
        except Exception as e:
            self.log.error(f"Boot sequence failed: {e}")
            self.crash_handler.handle_crash(e)
            return

        self.log.info("All systems online. Entering main loop.")
        self.event_bus.emit("jarvis.ready", {"message": "At your service, Sir."})
        self.lifecycle.run()

    def shutdown(self, signal_received=None, frame=None) -> None:
        self.log.info("Shutdown signal received.")
        self._running = False
        if self.lifecycle:
            self.lifecycle.stop()
        self.event_bus.emit("jarvis.shutdown", {})
        self.log.info("J.A.R.V.I.S. offline.")
        sys.exit(0)

    def run(self) -> None:
        signal.signal(signal.SIGINT, self.shutdown)
        signal.signal(signal.SIGTERM, self.shutdown)

        self.initialize()
        self.crash_handler.execute(self.start)


def main():
    core = JARVISCore()
    core.run()


if __name__ == "__main__":
    main()
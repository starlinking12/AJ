"""
J.A.R.V.I.S. System Tray
Manages the system tray icon and menu.
"""

from typing import Callable, Optional

from jarvis_core.logger import Logger


class SystemTray:
    def __init__(self):
        self.log = Logger("SystemTray")
        self._on_wake: Optional[Callable] = None
        self._on_sleep: Optional[Callable] = None
        self._on_exit: Optional[Callable] = None
        self._running = False

    def set_wake_callback(self, callback: Callable) -> None:
        self._on_wake = callback

    def set_sleep_callback(self, callback: Callable) -> None:
        self._on_sleep = callback

    def set_exit_callback(self, callback: Callable) -> None:
        self._on_exit = callback

    def start(self) -> None:
        self._running = True
        self.log.info("System tray started.")

    def stop(self) -> None:
        self._running = False
        self.log.info("System tray stopped.")
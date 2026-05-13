"""
J.A.R.V.I.S. Crash Handler
Graceful crash recovery and error reporting.
"""

import traceback
from typing import Callable

from jarvis_core.config.loader import Config
from jarvis_core.logger import Logger


class CrashHandler:
    def __init__(self, config: Config):
        self.config = config
        self.log = Logger("CrashHandler")
        self.max_restarts = getattr(config, 'max_restarts', 3)
        self.restart_count = 0

    def execute(self, func: Callable) -> None:
        while self.restart_count < self.max_restarts:
            try:
                func()
                break
            except Exception as e:
                self.restart_count += 1
                self.log.error(f"Crash detected (attempt {self.restart_count}/{self.max_restarts}): {e}")
                traceback.print_exc()

                if self.restart_count >= self.max_restarts:
                    self.log.error("Max restarts reached. Shutting down.")
                    raise

    def handle_crash(self, error: Exception) -> None:
        self.log.error(f"Handling crash: {error}")
        traceback.print_exc()
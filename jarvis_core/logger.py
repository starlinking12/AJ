"""
J.A.R.V.I.S. Core Logger
Simple structured logging for the core system.
"""

import sys
import time
from datetime import datetime


class Logger:
    def __init__(self, name: str):
        self.name = name

    def _log(self, level: str, message: str) -> None:
        timestamp = datetime.now().isoformat()
        output = f"[{timestamp}] [{level}] [{self.name}] {message}"
        print(output, file=sys.stderr)

    def info(self, message: str) -> None:
        self._log("INFO", message)

    def warn(self, message: str) -> None:
        self._log("WARN", message)

    def error(self, message: str) -> None:
        self._log("ERROR", message)

    def debug(self, message: str) -> None:
        self._log("DEBUG", message)
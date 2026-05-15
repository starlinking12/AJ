"""
J.A.R.V.I.S. Clipboard Manager
Reads from and writes to the system clipboard.
"""

import subprocess
import platform
from typing import Optional

from jarvis_core.logger import Logger


class ClipboardManager:
    def __init__(self):
        self.log = Logger("ClipboardManager")
        self._system = platform.system()
        self._initialized = False

    def initialize(self) -> bool:
        self._initialized = True
        self.log.info("Clipboard manager ready.")
        return True

    def get_text(self) -> Optional[str]:
        try:
            if self._system == "Windows":
                result = subprocess.run(
                    ["powershell", "-command", "Get-Clipboard"],
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
                return result.stdout.strip() if result.returncode == 0 else None

            elif self._system == "Darwin":
                result = subprocess.run(
                    ["pbpaste"],
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
                return result.stdout.strip() if result.returncode == 0 else None

            else:
                result = subprocess.run(
                    ["xclip", "-selection", "clipboard", "-o"],
                    capture_output=True,
                    text=True,
                    timeout=5,
                )
                return result.stdout.strip() if result.returncode == 0 else None

        except Exception as e:
            self.log.error(f"Clipboard read failed: {e}")
            return None

    def set_text(self, text: str) -> bool:
        try:
            if self._system == "Windows":
                process = subprocess.Popen(
                    ["clip"],
                    stdin=subprocess.PIPE,
                )
                process.communicate(input=text.encode("utf-8"))
                return process.returncode == 0

            elif self._system == "Darwin":
                process = subprocess.Popen(
                    ["pbcopy"],
                    stdin=subprocess.PIPE,
                )
                process.communicate(input=text.encode("utf-8"))
                return process.returncode == 0

            else:
                process = subprocess.Popen(
                    ["xclip", "-selection", "clipboard"],
                    stdin=subprocess.PIPE,
                )
                process.communicate(input=text.encode("utf-8"))
                return process.returncode == 0

        except Exception as e:
            self.log.error(f"Clipboard write failed: {e}")
            return False
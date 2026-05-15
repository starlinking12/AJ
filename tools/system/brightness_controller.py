"""
J.A.R.V.I.S. Brightness Controller
Controls screen brightness across platforms.
"""

import subprocess
import platform
from typing import Optional

from jarvis_core.logger import Logger


class BrightnessController:
    def __init__(self):
        self.log = Logger("BrightnessController")
        self._system = platform.system()
        self._initialized = False

    def initialize(self) -> bool:
        self._initialized = True
        self.log.info(f"Brightness controller ready. Platform: {self._system}")
        return True

    def set_brightness(self, level: int) -> bool:
        level = max(0, min(100, level))

        try:
            if self._system == "Windows":
                import screen_brightness_control as sbc
                sbc.set_brightness(level)
                return True

            elif self._system == "Darwin":
                brightness = level / 100.0
                subprocess.run([
                    "osascript",
                    "-e",
                    f'tell application "System Events" to tell every screen to set brightness to {brightness}'
                ])
                return True

            else:
                subprocess.run(["brightnessctl", "set", f"{level}%"])
                return True

        except ImportError:
            self.log.warn("Brightness control library not available.")
            return False
        except Exception as e:
            self.log.error(f"Brightness set failed: {e}")
            return False

    def get_brightness(self) -> Optional[int]:
        try:
            if self._system == "Windows":
                import screen_brightness_control as sbc
                return sbc.get_brightness()[0]

            elif self._system == "Darwin":
                result = subprocess.run(
                    ["osascript", "-e", "get brightness of screen 1"],
                    capture_output=True,
                    text=True,
                )
                return int(float(result.stdout.strip()) * 100)

            else:
                result = subprocess.run(
                    ["brightnessctl", "get"],
                    capture_output=True,
                    text=True,
                )
                return int(result.stdout.strip())

        except Exception:
            return None

    def decrease(self, step: int = 10) -> bool:
        current = self.get_brightness() or 50
        return self.set_brightness(current - step)

    def increase(self, step: int = 10) -> bool:
        current = self.get_brightness() or 50
        return self.set_brightness(current + step)
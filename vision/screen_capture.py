"""
J.A.R.V.I.S. Screen Capture
Captures screen frames for real-time analysis.
Uses MSS for fast cross-platform screen grabbing.
"""

from typing import Optional, Any
from pathlib import Path
import time

from jarvis_core.logger import Logger


class ScreenCapture:
    def __init__(self):
        self.log = Logger("ScreenCapture")
        self._sct = None
        self._monitor = None
        self._initialized = False
        self._output_dir = Path.home() / "Pictures" / "JARVIS_Screens"

    def initialize(self, monitor_index: int = 1) -> bool:
        try:
            import mss

            self._sct = mss.mss()
            monitors = self._sct.monitors

            if monitor_index < len(monitors):
                self._monitor = monitors[monitor_index]
            else:
                self._monitor = monitors[1] if len(monitors) > 1 else monitors[0]

            self._output_dir.mkdir(parents=True, exist_ok=True)
            self._initialized = True
            self.log.info(f"Screen capture ready. Monitor: {self._monitor}")
            return True

        except ImportError:
            self.log.warn("mss not installed.")
            return False
        except Exception as e:
            self.log.error(f"Screen capture init failed: {e}")
            return False

    def capture(self) -> Optional[Any]:
        if not self._initialized or self._sct is None:
            return None

        try:
            return self._sct.grab(self._monitor)
        except Exception as e:
            self.log.error(f"Screen capture failed: {e}")
            return None

    def capture_to_file(self, filename: str = None) -> Optional[str]:
        if not self._initialized or self._sct is None:
            return None

        try:
            if filename is None:
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                filename = f"screen_{timestamp}.png"

            output_path = self._output_dir / filename
            self._sct.shot(output=str(output_path))
            return str(output_path)

        except Exception as e:
            self.log.error(f"Screen capture to file failed: {e}")
            return None

    def capture_region(self, left: int, top: int, width: int, height: int) -> Optional[Any]:
        if not self._initialized or self._sct is None:
            return None

        try:
            region = {"left": left, "top": top, "width": width, "height": height}
            return self._sct.grab(region)
        except Exception as e:
            self.log.error(f"Region capture failed: {e}")
            return None

    def get_monitor_info(self) -> dict:
        if self._monitor is None:
            return {}
        return {
            "width": self._monitor.get("width", 0),
            "height": self._monitor.get("height", 0),
            "left": self._monitor.get("left", 0),
            "top": self._monitor.get("top", 0),
        }

    def release(self) -> None:
        if self._sct:
            self._sct.close()
            self._sct = None
        self._initialized = False
"""
J.A.R.V.I.S. Screenshot Taker
Captures screenshots using MSS (cross-platform).
"""

from pathlib import Path
from typing import Optional

from jarvis_core.logger import Logger


class ScreenshotTaker:
    def __init__(self):
        self.log = Logger("ScreenshotTaker")
        self._output_dir = Path.home() / "Pictures" / "JARVIS_Screenshots"
        self._initialized = False

    def initialize(self) -> bool:
        self._output_dir.mkdir(parents=True, exist_ok=True)
        self._initialized = True
        self.log.info(f"Screenshot taker ready. Output: {self._output_dir}")
        return True

    def capture(self, filename: str = None) -> Optional[str]:
        try:
            import mss
            import time

            if filename is None:
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                filename = f"jarvis_screenshot_{timestamp}.png"

            output_path = self._output_dir / filename

            with mss.mss() as sct:
                sct.shot(output=str(output_path))

            self.log.info(f"Screenshot saved: {output_path}")
            return str(output_path)

        except ImportError:
            self.log.warn("mss not installed.")
            return None
        except Exception as e:
            self.log.error(f"Screenshot failed: {e}")
            return None

    def capture_region(self, left: int, top: int, width: int, height: int, filename: str = None) -> Optional[str]:
        try:
            import mss
            import mss.tools
            import time

            if filename is None:
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                filename = f"jarvis_region_{timestamp}.png"

            output_path = self._output_dir / filename

            monitor = {"left": left, "top": top, "width": width, "height": height}

            with mss.mss() as sct:
                screenshot = sct.grab(monitor)
                mss.tools.to_png(screenshot.rgb, screenshot.size, output=str(output_path))

            self.log.info(f"Region screenshot saved: {output_path}")
            return str(output_path)

        except ImportError:
            self.log.warn("mss not installed.")
            return None
        except Exception as e:
            self.log.error(f"Region screenshot failed: {e}")
            return None

    def get_latest_screenshot(self) -> Optional[str]:
        files = sorted(self._output_dir.glob("*.png"), key=lambda f: f.stat().st_mtime, reverse=True)
        return str(files[0]) if files else None
"""
J.A.R.V.I.S. Snapshot
Captures and saves individual frames from the camera.
"""

import time
from pathlib import Path
from typing import Optional, Any

from jarvis_core.logger import Logger


class Snapshot:
    def __init__(self):
        self.log = Logger("Snapshot")
        self._output_dir = Path.home() / "Pictures" / "JARVIS_Snapshots"
        self._initialized = False

    def initialize(self) -> bool:
        self._output_dir.mkdir(parents=True, exist_ok=True)
        self._initialized = True
        self.log.info(f"Snapshot ready. Output: {self._output_dir}")
        return True

    def save(self, frame: Any, filename: str = None) -> Optional[str]:
        try:
            import cv2

            if filename is None:
                timestamp = time.strftime("%Y%m%d_%H%M%S")
                filename = f"jarvis_snap_{timestamp}.jpg"

            output_path = self._output_dir / filename
            cv2.imwrite(str(output_path), frame)

            self.log.info(f"Snapshot saved: {output_path}")
            return str(output_path)

        except ImportError:
            self.log.warn("opencv-python not installed.")
            return None
        except Exception as e:
            self.log.error(f"Snapshot failed: {e}")
            return None

    def get_latest(self) -> Optional[str]:
        files = sorted(
            self._output_dir.glob("*.jpg"),
            key=lambda f: f.stat().st_mtime,
            reverse=True
        )
        return str(files[0]) if files else None

    def list_snapshots(self, limit: int = 20) -> list:
        files = sorted(
            self._output_dir.glob("*.jpg"),
            key=lambda f: f.stat().st_mtime,
            reverse=True
        )
        return [str(f) for f in files[:limit]]
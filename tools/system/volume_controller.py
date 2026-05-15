"""
J.A.R.V.I.S. Volume Controller
Controls system volume across platforms.
"""

import subprocess
import platform
from typing import Optional

from jarvis_core.logger import Logger


class VolumeController:
    def __init__(self):
        self.log = Logger("VolumeController")
        self._system = platform.system()
        self._initialized = False

    def initialize(self) -> bool:
        self._initialized = True
        self.log.info(f"Volume controller ready. Platform: {self._system}")
        return True

    def set_volume(self, level: int) -> bool:
        level = max(0, min(100, level))

        try:
            if self._system == "Windows":
                import ctypes
                from ctypes import cast, POINTER
                from comtypes import CLSCTX_ALL
                from pycaw.pycaw import AudioUtilities, IAudioEndpointVolume

                devices = AudioUtilities.GetSpeakers()
                interface = devices.Activate(IAudioEndpointVolume._iid_, CLSCTX_ALL, None)
                volume = cast(interface, POINTER(IAudioEndpointVolume))
                volume.SetMasterVolumeLevelScalar(level / 100.0, None)
                return True

            elif self._system == "Darwin":
                subprocess.run(["osascript", "-e", f"set volume output volume {level}"])
                return True

            else:
                subprocess.run(["pactl", "set-sink-volume", "@DEFAULT_SINK@", f"{level}%"])
                return True

        except Exception as e:
            self.log.error(f"Volume set failed: {e}")
            return False

    def get_volume(self) -> Optional[int]:
        try:
            if self._system == "Darwin":
                result = subprocess.run(
                    ["osascript", "-e", "output volume of (get volume settings)"],
                    capture_output=True,
                    text=True,
                )
                return int(result.stdout.strip())

            return None

        except Exception as e:
            self.log.error(f"Volume get failed: {e}")
            return None

    def mute(self) -> bool:
        try:
            if self._system == "Darwin":
                subprocess.run(["osascript", "-e", "set volume with output muted"])
            else:
                self.set_volume(0)
            return True
        except Exception as e:
            self.log.error(f"Mute failed: {e}")
            return False

    def unmute(self) -> bool:
        return self.set_volume(50)
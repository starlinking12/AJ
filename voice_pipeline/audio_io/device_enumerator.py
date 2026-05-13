"""
J.A.R.V.I.S. Device Enumerator
Lists available audio input and output devices.
"""

from typing import List, Dict, Optional

import pyaudio

from jarvis_core.logger import Logger


class DeviceEnumerator:
    def __init__(self):
        self.log = Logger("DeviceEnumerator")
        self._audio: Optional[pyaudio.PyAudio] = None

    def initialize(self) -> bool:
        try:
            self._audio = pyaudio.PyAudio()
            return True
        except Exception as e:
            self.log.error(f"Device enumeration failed: {e}")
            return False

    def list_input_devices(self) -> List[Dict]:
        return self._list_devices(is_input=True)

    def list_output_devices(self) -> List[Dict]:
        return self._list_devices(is_input=False)

    def list_all_devices(self) -> Dict[str, List[Dict]]:
        return {
            "input": self.list_input_devices(),
            "output": self.list_output_devices(),
        }

    def get_default_input(self) -> Optional[Dict]:
        if self._audio is None:
            return None
        try:
            return self._audio.get_default_input_device_info()
        except Exception:
            return None

    def get_default_output(self) -> Optional[Dict]:
        if self._audio is None:
            return None
        try:
            return self._audio.get_default_output_device_info()
        except Exception:
            return None

    def get_device_by_name(self, name: str) -> Optional[Dict]:
        for device in self.list_all_devices().get("input", []) + self.list_all_devices().get("output", []):
            if name.lower() in device.get("name", "").lower():
                return device
        return None

    def _list_devices(self, is_input: bool) -> List[Dict]:
        if self._audio is None:
            return []

        devices = []
        try:
            count = self._audio.get_device_count()
            for i in range(count):
                info = self._audio.get_device_info_by_index(i)
                if is_input and info.get("maxInputChannels", 0) > 0:
                    devices.append({
                        "index": i,
                        "name": info.get("name", "Unknown"),
                        "channels": info.get("maxInputChannels"),
                        "sample_rate": int(info.get("defaultSampleRate", 0)),
                        "is_default": info.get("name") == self.get_default_input().get("name") if self.get_default_input() else False,
                    })
                elif not is_input and info.get("maxOutputChannels", 0) > 0:
                    devices.append({
                        "index": i,
                        "name": info.get("name", "Unknown"),
                        "channels": info.get("maxOutputChannels"),
                        "sample_rate": int(info.get("defaultSampleRate", 0)),
                        "is_default": info.get("name") == self.get_default_output().get("name") if self.get_default_output() else False,
                    })
        except Exception as e:
            self.log.error(f"Error listing devices: {e}")

        return devices

    def release(self) -> None:
        if self._audio:
            self._audio.terminate()
            self._audio = None
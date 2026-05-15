"""
J.A.R.V.I.S. Application Launcher
Opens applications by name across Windows, macOS, and Linux.
"""

import subprocess
import platform
from typing import Optional

from jarvis_core.logger import Logger


class ApplicationLauncher:
    def __init__(self):
        self.log = Logger("ApplicationLauncher")
        self._system = platform.system()
        self._app_map = {}
        self._load_app_map()
        self._initialized = False

    def initialize(self) -> bool:
        self._initialized = True
        self.log.info(f"Application launcher ready. Platform: {self._system}")
        return True

    def _load_app_map(self) -> None:
        common_apps = {
            "chrome": {
                "Windows": "chrome",
                "Darwin": "open -a 'Google Chrome'",
                "Linux": "google-chrome",
            },
            "firefox": {
                "Windows": "firefox",
                "Darwin": "open -a Firefox",
                "Linux": "firefox",
            },
            "brave": {
                "Windows": "brave",
                "Darwin": "open -a Brave",
                "Linux": "brave-browser",
            },
            "edge": {
                "Windows": "msedge",
                "Darwin": "open -a 'Microsoft Edge'",
                "Linux": "microsoft-edge",
            },
            "code": {
                "Windows": "code",
                "Darwin": "open -a 'Visual Studio Code'",
                "Linux": "code",
            },
            "terminal": {
                "Windows": "wt",
                "Darwin": "open -a Terminal",
                "Linux": "gnome-terminal",
            },
            "spotify": {
                "Windows": "spotify",
                "Darwin": "open -a Spotify",
                "Linux": "spotify",
            },
            "vlc": {
                "Windows": "vlc",
                "Darwin": "open -a VLC",
                "Linux": "vlc",
            },
            "notepad": {
                "Windows": "notepad",
                "Darwin": "open -a TextEdit",
                "Linux": "gedit",
            },
            "calculator": {
                "Windows": "calc",
                "Darwin": "open -a Calculator",
                "Linux": "gnome-calculator",
            },
            "finder": {
                "Darwin": "open -a Finder",
            },
            "explorer": {
                "Windows": "explorer",
            },
            "settings": {
                "Windows": "start ms-settings:",
                "Darwin": "open -a 'System Settings'",
                "Linux": "gnome-control-center",
            },
        }

        for app_name, commands in common_apps.items():
            if self._system in commands:
                self._app_map[app_name] = commands[self._system]

    def open(self, app_name: str) -> bool:
        if not self._initialized:
            self.log.error("Application launcher not initialized.")
            return False

        app_name_lower = app_name.lower().strip()

        if app_name_lower in self._app_map:
            command = self._app_map[app_name_lower]
            return self._execute(command)

        return self._execute(app_name)

    def _execute(self, command: str) -> bool:
        try:
            if self._system == "Windows":
                subprocess.Popen(command, shell=True)
            elif self._system == "Darwin":
                subprocess.Popen(command, shell=True)
            else:
                subprocess.Popen(command, shell=True)

            self.log.info(f"Launched: {command}")
            return True

        except Exception as e:
            self.log.error(f"Launch failed for '{command}': {e}")
            return False

    def list_available_apps(self) -> list:
        return list(self._app_map.keys())

    def add_app(self, name: str, command: str) -> None:
        self._app_map[name.lower()] = command
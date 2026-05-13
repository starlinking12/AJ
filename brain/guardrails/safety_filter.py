"""
J.A.R.V.I.S. Safety Filter
Prevents harmful, dangerous, or inappropriate outputs.
"""

from typing import List, Optional

from jarvis_core.logger import Logger


class SafetyFilter:
    def __init__(self):
        self.log = Logger("SafetyFilter")
        self._dangerous_patterns: List[str] = []
        self._load_patterns()

    def _load_patterns(self) -> None:
        self._dangerous_patterns = [
            "rm -rf /",
            "rm -rf ~",
            "sudo rm",
            "mkfs",
            "dd if=/dev/zero",
            "format c:",
            "del /f /s",
            "rd /s /q",
            "shutdown -h now",
            "shutdown -r now",
            "reboot",
            "chmod 777 /",
            "chown -R root /",
            "> /dev/sda",
            "diskpart",
            "fdisk",
        ]

    def check_text(self, text: str) -> bool:
        text_lower = text.lower()
        for pattern in self._dangerous_patterns:
            if pattern.lower() in text_lower:
                self.log.warn(f"Dangerous pattern detected: '{pattern}'")
                return False
        return True

    def check_command(self, command: str) -> bool:
        if not self.check_text(command):
            return False

        dangerous_prefixes = [
            "rm ", "sudo rm", "mkfs", "dd ", "fdisk", "format",
            "shutdown", "reboot", "halt", "poweroff",
        ]
        command_lower = command.lower().strip()
        for prefix in dangerous_prefixes:
            if command_lower.startswith(prefix):
                self.log.warn(f"Dangerous command blocked: '{command}'")
                return False

        return True

    def filter_response(self, response: str) -> str:
        if not self.check_text(response):
            return "I cannot provide that information, Sir. It may be unsafe."
        return response

    def get_safe_alternative(self, dangerous_command: str) -> Optional[str]:
        alternatives = {
            "shutdown": "I recommend using the system menu to shut down, Sir.",
            "reboot": "I recommend using the system menu to restart, Sir.",
            "rm -rf": "I cannot execute destructive delete commands, Sir.",
        }
        for key, alt in alternatives.items():
            if key in dangerous_command.lower():
                return alt
        return None

    def add_pattern(self, pattern: str) -> None:
        self._dangerous_patterns.append(pattern)
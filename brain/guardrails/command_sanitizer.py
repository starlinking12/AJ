"""
J.A.R.V.I.S. Command Sanitizer
Sanitizes system commands before execution.
Prevents injection attacks and dangerous operations.
"""

import re
from typing import Tuple, Optional

from jarvis_core.logger import Logger


class CommandSanitizer:
    def __init__(self):
        self.log = Logger("CommandSanitizer")
        self._allowed_commands = [
            "open", "xdg-open", "start", "code", "python", "pip",
            "git", "docker", "curl", "wget", "ls", "dir", "pwd",
            "cd", "cp", "mv", "mkdir", "touch", "cat", "head", "tail",
            "echo", "date", "whoami", "hostname", "ping",
            "ps", "kill", "spotify", "vlc", "firefox", "chrome",
            "brave", "edge", "notepad", "calc", "explorer", "finder",
        ]
        self._injection_patterns = [
            r"\;.*",
            r"\&\&.*",
            r"\|\|.*",
            r"\`.*\`",
            r"\$\(.*\)",
            r"\|\s*.*",
            r">\s*/dev/",
            r"<\s*/dev/",
        ]

    def sanitize(self, command: str) -> Tuple[str, bool]:
        original = command
        command = command.strip()

        if not command:
            return "", False

        for pattern in self._injection_patterns:
            if re.search(pattern, command):
                self.log.warn(f"Injection pattern detected: '{original}'")
                return "", False

        command_parts = command.split()
        if not command_parts:
            return "", False

        base_command = command_parts[0].lower()

        if base_command not in self._allowed_commands:
            self.log.warn(f"Command not in whitelist: '{base_command}'")
            return "", False

        sanitized = " ".join(command_parts)
        return sanitized, True

    def is_allowed(self, command: str) -> bool:
        _, allowed = self.sanitize(command)
        return allowed

    def add_allowed_command(self, command: str) -> None:
        if command.lower() not in self._allowed_commands:
            self._allowed_commands.append(command.lower())

    def remove_allowed_command(self, command: str) -> bool:
        if command.lower() in self._allowed_commands:
            self._allowed_commands.remove(command.lower())
            return True
        return False

    def get_allowed_commands(self) -> list:
        return self._allowed_commands.copy()

    def escape_argument(self, arg: str) -> str:
        if re.search(r'[^\w\-\.\/]', arg):
            return f'"{arg}"'
        return arg
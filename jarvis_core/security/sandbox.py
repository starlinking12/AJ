"""
J.A.R.V.I.S. Sandbox
Restricts command execution to safe directories and operations.
"""

import os
import subprocess
from pathlib import Path
from typing import List, Optional

from jarvis_core.logger import Logger


class Sandbox:
    def __init__(self, allowed_paths: Optional[List[str]] = None):
        self.log = Logger("Sandbox")
        self.allowed_paths = allowed_paths or [
            str(Path.home()),
            "/tmp",
            "/var/tmp",
        ]
        self.blocked_commands = [
            "rm -rf /",
            "mkfs",
            "dd if=",
            ":(){ :|:& };:",
        ]

    def is_path_allowed(self, path: str) -> bool:
        resolved = str(Path(path).resolve())
        for allowed in self.allowed_paths:
            if resolved.startswith(allowed):
                return True
        return False

    def is_command_allowed(self, command: str) -> bool:
        for blocked in self.blocked_commands:
            if blocked in command.lower():
                self.log.warn(f"Blocked dangerous command: {command}")
                return False
        return True

    def execute(self, command: str, cwd: Optional[str] = None) -> subprocess.CompletedProcess:
        if not self.is_command_allowed(command):
            raise ValueError(f"Command blocked by sandbox: {command}")

        if cwd and not self.is_path_allowed(cwd):
            raise ValueError(f"Path not allowed: {cwd}")

        return subprocess.run(
            command,
            shell=True,
            capture_output=True,
            text=True,
            cwd=cwd,
            timeout=30
        )
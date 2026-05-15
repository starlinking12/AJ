"""
J.A.R.V.I.S. Shell Executor
Executes system shell commands with safety checks.
"""

import subprocess
import platform
from typing import Dict, Any, Optional

from brain.guardrails.command_sanitizer import CommandSanitizer
from brain.guardrails.safety_filter import SafetyFilter

from jarvis_core.logger import Logger


class ShellExecutor:
    def __init__(self):
        self.log = Logger("ShellExecutor")
        self.sanitizer = CommandSanitizer()
        self.safety = SafetyFilter()
        self._timeout = 30
        self._initialized = False

    def initialize(self) -> bool:
        self._initialized = True
        self.log.info("Shell executor ready.")
        return True

    def execute(self, command: str, cwd: str = None) -> Dict[str, Any]:
        if not self._initialized:
            return {"success": False, "error": "Shell executor not initialized."}

        if not self.safety.check_command(command):
            return {"success": False, "error": "Command blocked by safety filter."}

        sanitized, allowed = self.sanitizer.sanitize(command)
        if not allowed:
            return {"success": False, "error": "Command failed sanitization."}

        try:
            result = subprocess.run(
                sanitized,
                shell=True,
                capture_output=True,
                text=True,
                timeout=self._timeout,
                cwd=cwd,
            )

            return {
                "success": result.returncode == 0,
                "stdout": result.stdout.strip(),
                "stderr": result.stderr.strip(),
                "returncode": result.returncode,
            }

        except subprocess.TimeoutExpired:
            return {"success": False, "error": f"Command timed out after {self._timeout}s."}
        except Exception as e:
            return {"success": False, "error": str(e)}

    def execute_safe(self, command: str) -> str:
        result = self.execute(command)
        if result.get("success"):
            return result.get("stdout", "Command executed, Sir.")
        else:
            return f"Command failed, Sir. {result.get('error', result.get('stderr', ''))}"

    def set_timeout(self, seconds: int) -> None:
        self._timeout = seconds
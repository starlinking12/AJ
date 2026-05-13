"""
J.A.R.V.I.S. Updater
Handles automatic updates from the GitHub repository.
"""

import subprocess
from typing import Optional

from jarvis_core.logger import Logger


class Updater:
    def __init__(self, repo_path: str = "."):
        self.repo_path = repo_path
        self.log = Logger("Updater")

    def check_for_updates(self) -> Optional[str]:
        try:
            result = subprocess.run(
                ["git", "fetch", "origin"],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            if result.returncode != 0:
                self.log.warn(f"Git fetch failed: {result.stderr}")
                return None

            result = subprocess.run(
                ["git", "rev-list", "HEAD...origin/main", "--count"],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            count = int(result.stdout.strip())
            if count > 0:
                self.log.info(f"Updates available: {count} commits behind.")
                return result.stdout.strip()
            return None
        except Exception as e:
            self.log.error(f"Update check failed: {e}")
            return None

    def update(self) -> bool:
        try:
            result = subprocess.run(
                ["git", "pull", "origin", "main"],
                cwd=self.repo_path,
                capture_output=True,
                text=True
            )
            if result.returncode == 0:
                self.log.info("Update successful.")
                return True
            self.log.error(f"Update failed: {result.stderr}")
            return False
        except Exception as e:
            self.log.error(f"Update failed: {e}")
            return False
"""
J.A.R.V.I.S. File Search
Searches for files by name or content.
"""

import os
from pathlib import Path
from typing import List, Dict, Optional

from jarvis_core.logger import Logger


class FileSearch:
    def __init__(self):
        self.log = Logger("FileSearch")
        self._initialized = False

    def initialize(self) -> bool:
        self._initialized = True
        self.log.info("File search ready.")
        return True

    def search_by_name(
        self,
        query: str,
        directory: str = None,
        max_results: int = 20
    ) -> List[Dict]:
        if directory is None:
            directory = str(Path.home())

        results = []
        query_lower = query.lower()

        try:
            for root, dirs, files in os.walk(directory):
                for name in files + dirs:
                    if query_lower in name.lower():
                        full_path = os.path.join(root, name)
                        results.append({
                            "name": name,
                            "path": full_path,
                            "is_file": os.path.isfile(full_path),
                            "size": os.path.getsize(full_path) if os.path.isfile(full_path) else 0,
                        })
                        if len(results) >= max_results:
                            return results
                if len(results) >= max_results:
                    break
        except Exception as e:
            self.log.error(f"File search failed: {e}")

        return results

    def search_by_content(
        self,
        text: str,
        directory: str = None,
        file_pattern: str = "*.txt",
        max_results: int = 10
    ) -> List[Dict]:
        if directory is None:
            directory = str(Path.home())

        results = []
        text_lower = text.lower()

        try:
            for root, dirs, files in os.walk(directory):
                for name in files:
                    if name.endswith(file_pattern.replace("*", "")):
                        full_path = os.path.join(root, name)
                        try:
                            with open(full_path, "r", encoding="utf-8", errors="ignore") as f:
                                content = f.read()
                                if text_lower in content.lower():
                                    results.append({
                                        "name": name,
                                        "path": full_path,
                                        "match": content[
                                            max(0, content.lower().index(text_lower) - 50):
                                            content.lower().index(text_lower) + len(text_lower) + 50
                                        ],
                                    })
                                    if len(results) >= max_results:
                                        return results
                        except Exception:
                            continue
        except Exception as e:
            self.log.error(f"Content search failed: {e}")

        return results
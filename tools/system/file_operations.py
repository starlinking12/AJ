"""
J.A.R.V.I.S. File Operations
Read, write, copy, move, and delete files.
"""

import os
import shutil
from pathlib import Path
from typing import Optional, List

from jarvis_core.logger import Logger


class FileOperations:
    def __init__(self):
        self.log = Logger("FileOperations")
        self._initialized = False

    def initialize(self) -> bool:
        self._initialized = True
        self.log.info("File operations ready.")
        return True

    def read_file(self, path: str) -> Optional[str]:
        try:
            with open(path, "r", encoding="utf-8") as f:
                content = f.read()
            self.log.info(f"Read file: {path}")
            return content
        except Exception as e:
            self.log.error(f"Read failed: {e}")
            return None

    def write_file(self, path: str, content: str) -> bool:
        try:
            Path(path).parent.mkdir(parents=True, exist_ok=True)
            with open(path, "w", encoding="utf-8") as f:
                f.write(content)
            self.log.info(f"Written file: {path}")
            return True
        except Exception as e:
            self.log.error(f"Write failed: {e}")
            return False

    def copy_file(self, source: str, destination: str) -> bool:
        try:
            shutil.copy2(source, destination)
            self.log.info(f"Copied: {source} -> {destination}")
            return True
        except Exception as e:
            self.log.error(f"Copy failed: {e}")
            return False

    def move_file(self, source: str, destination: str) -> bool:
        try:
            shutil.move(source, destination)
            self.log.info(f"Moved: {source} -> {destination}")
            return True
        except Exception as e:
            self.log.error(f"Move failed: {e}")
            return False

    def delete_file(self, path: str) -> bool:
        try:
            if os.path.isfile(path):
                os.remove(path)
            elif os.path.isdir(path):
                shutil.rmtree(path)
            self.log.info(f"Deleted: {path}")
            return True
        except Exception as e:
            self.log.error(f"Delete failed: {e}")
            return False

    def list_directory(self, path: str) -> List[Dict]:
        try:
            items = []
            for item in os.listdir(path):
                full_path = os.path.join(path, item)
                items.append({
                    "name": item,
                    "path": full_path,
                    "is_file": os.path.isfile(full_path),
                    "is_dir": os.path.isdir(full_path),
                    "size": os.path.getsize(full_path) if os.path.isfile(full_path) else 0,
                })
            return items
        except Exception as e:
            self.log.error(f"List directory failed: {e}")
            return []

    def get_file_info(self, path: str) -> Optional[Dict]:
        try:
            stat = os.stat(path)
            return {
                "name": os.path.basename(path),
                "path": path,
                "size": stat.st_size,
                "created": stat.st_ctime,
                "modified": stat.st_mtime,
                "is_file": os.path.isfile(path),
            }
        except Exception as e:
            self.log.error(f"File info failed: {e}")
            return None
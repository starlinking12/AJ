"""
J.A.R.V.I.S. ChromaDB Client
Direct client wrapper for ChromaDB operations.
"""

from typing import List, Dict, Any, Optional

from jarvis_core.logger import Logger


class ChromaDBClient:
    def __init__(self, persist_directory: str = None):
        self.log = Logger("ChromaDBClient")
        if persist_directory is None:
            from pathlib import Path
            persist_directory = str(
                Path(__file__).resolve().parent.parent.parent / "data" / "chromadb"
            )
        self.persist_directory = persist_directory
        self._client = None
        self._initialized = False

    def initialize(self) -> bool:
        try:
            import chromadb

            self._client = chromadb.PersistentClient(path=self.persist_directory)
            self._initialized = True
            self.log.info(f"ChromaDB client ready. Storage: {self.persist_directory}")
            return True
        except ImportError:
            self.log.warn("chromadb not installed.")
            return False
        except Exception as e:
            self.log.warn(f"ChromaDB client init failed: {e}")
            return False

    def get_or_create_collection(self, name: str):
        if not self._initialized:
            return None
        try:
            return self._client.get_or_create_collection(name)
        except Exception as e:
            self.log.error(f"Collection error: {e}")
            return None

    def list_collections(self) -> List[str]:
        if not self._initialized:
            return []
        try:
            return [c.name for c in self._client.list_collections()]
        except Exception:
            return []

    def delete_collection(self, name: str) -> bool:
        if not self._initialized:
            return False
        try:
            self._client.delete_collection(name)
            return True
        except Exception:
            return False

    def close(self) -> None:
        self._client = None
        self._initialized = False
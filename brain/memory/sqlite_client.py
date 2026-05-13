"""
J.A.R.V.I.S. SQLite Client
Direct SQLite client for structured data operations.
"""

import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional

from jarvis_core.logger import Logger


class SQLiteClient:
    def __init__(self, db_path: str = None):
        self.log = Logger("SQLiteClient")
        if db_path is None:
            db_path = Path(__file__).resolve().parent.parent.parent / "data" / "jarvis_memory.db"
        self.db_path = str(db_path)
        self._conn: Optional[sqlite3.Connection] = None
        self._initialized = False

    def initialize(self) -> bool:
        try:
            Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
            self._conn = sqlite3.connect(self.db_path)
            self._conn.row_factory = sqlite3.Row
            self._initialized = True
            self.log.info(f"SQLite client ready: {self.db_path}")
            return True
        except Exception as e:
            self.log.error(f"SQLite init failed: {e}")
            return False

    def execute(self, query: str, params: tuple = None) -> sqlite3.Cursor:
        if not self._initialized or self._conn is None:
            raise RuntimeError("SQLite not initialized.")
        cursor = self._conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        self._conn.commit()
        return cursor

    def fetch_all(self, query: str, params: tuple = None) -> List[Dict]:
        cursor = self.execute(query, params)
        return [dict(row) for row in cursor.fetchall()]

    def fetch_one(self, query: str, params: tuple = None) -> Optional[Dict]:
        cursor = self.execute(query, params)
        row = cursor.fetchone()
        return dict(row) if row else None

    def insert(self, table: str, data: Dict) -> int:
        columns = ", ".join(data.keys())
        placeholders = ", ".join(["?" for _ in data])
        query = f"INSERT INTO {table} ({columns}) VALUES ({placeholders})"
        cursor = self.execute(query, tuple(data.values()))
        return cursor.lastrowid

    def close(self) -> None:
        if self._conn:
            self._conn.close()
            self._conn = None
        self._initialized = False
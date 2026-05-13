"""
J.A.R.V.I.S. Relational Store
SQLite-based structured data storage for user profiles and settings.
"""

import sqlite3
from pathlib import Path
from typing import Any, Dict, List, Optional

from jarvis_core.logger import Logger


class RelationalStore:
    def __init__(self, db_path: str = None):
        self.log = Logger("RelationalStore")
        if db_path is None:
            db_path = Path(__file__).resolve().parent.parent.parent / "data" / "jarvis.db"
        self.db_path = str(db_path)
        self._conn: Optional[sqlite3.Connection] = None
        self._initialized = False

    def initialize(self) -> bool:
        try:
            Path(self.db_path).parent.mkdir(parents=True, exist_ok=True)
            self._conn = sqlite3.connect(self.db_path)
            self._conn.row_factory = sqlite3.Row
            self._create_tables()
            self._initialized = True
            self.log.info(f"Relational store ready: {self.db_path}")
            return True
        except Exception as e:
            self.log.error(f"Relational store init failed: {e}")
            return False

    def _create_tables(self) -> None:
        cursor = self._conn.cursor()
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS users (
                id TEXT PRIMARY KEY,
                name TEXT,
                created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS facts (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                user_id TEXT,
                key TEXT,
                value TEXT,
                updated_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        cursor.execute("""
            CREATE TABLE IF NOT EXISTS preferences (
                user_id TEXT PRIMARY KEY,
                data TEXT,
                FOREIGN KEY (user_id) REFERENCES users(id)
            )
        """)
        self._conn.commit()

    def execute(self, query: str, params: tuple = None) -> Any:
        if not self._initialized or self._conn is None:
            return None
        cursor = self._conn.cursor()
        if params:
            cursor.execute(query, params)
        else:
            cursor.execute(query)
        self._conn.commit()
        return cursor

    def close(self) -> None:
        if self._conn:
            self._conn.close()
            self._conn = None
        self._initialized = False
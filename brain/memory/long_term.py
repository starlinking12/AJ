"""
J.A.R.V.I.S. Long-Term Memory
Persistent storage for facts, preferences, and interaction history.
"""

import json
import time
from pathlib import Path
from typing import Dict, Any, List, Optional

from jarvis_core.logger import Logger


class LongTermMemory:
    def __init__(self, storage_dir: str = None):
        self.log = Logger("LongTermMemory")
        if storage_dir is None:
            storage_dir = Path(__file__).resolve().parent.parent.parent / "data" / "memory"
        self.storage_dir = Path(storage_dir)
        self.storage_dir.mkdir(parents=True, exist_ok=True)
        self._facts: Dict[str, Dict] = {}
        self._load_facts()

    def _load_facts(self) -> None:
        facts_file = self.storage_dir / "facts.json"
        if facts_file.exists():
            try:
                with open(facts_file, "r") as f:
                    self._facts = json.load(f)
            except Exception:
                self._facts = {}

    def _save_facts(self) -> None:
        facts_file = self.storage_dir / "facts.json"
        try:
            with open(facts_file, "w") as f:
                json.dump(self._facts, f, indent=2)
        except Exception as e:
            self.log.error(f"Failed to save facts: {e}")

    def store_fact(self, user_id: str, key: str, value: Any) -> None:
        if user_id not in self._facts:
            self._facts[user_id] = {}
        self._facts[user_id][key] = {
            "value": value,
            "timestamp": time.time(),
        }
        self._save_facts()

    def get_fact(self, user_id: str, key: str) -> Optional[Any]:
        user_facts = self._facts.get(user_id, {})
        fact = user_facts.get(key)
        if fact:
            return fact.get("value")
        return None

    def get_all_facts(self, user_id: str) -> Dict[str, Any]:
        user_facts = self._facts.get(user_id, {})
        return {k: v.get("value") for k, v in user_facts.items()}

    def store_interaction(
        self,
        user_id: str,
        user_text: str,
        response: str,
        intent: str
    ) -> None:
        log_file = self.storage_dir / f"{user_id}_history.jsonl"
        entry = {
            "timestamp": time.time(),
            "user": user_text,
            "response": response,
            "intent": intent,
        }
        try:
            with open(log_file, "a") as f:
                f.write(json.dumps(entry) + "\n")
        except Exception as e:
            self.log.error(f"Failed to store interaction: {e}")

    def delete_fact(self, user_id: str, key: str) -> bool:
        if user_id in self._facts and key in self._facts[user_id]:
            del self._facts[user_id][key]
            self._save_facts()
            return True
        return False
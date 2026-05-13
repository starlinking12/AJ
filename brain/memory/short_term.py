"""
J.A.R.V.I.S. Short-Term Memory
Stores recent conversation turns in memory.
"""

from collections import deque
from typing import Dict, List

from jarvis_core.logger import Logger


class ShortTermMemory:
    def __init__(self, max_turns: int = 50):
        self.log = Logger("ShortTermMemory")
        self.max_turns = max_turns
        self._conversations: Dict[str, deque] = {}

    def add(self, user_id: str, user_text: str, response: str) -> None:
        if user_id not in self._conversations:
            self._conversations[user_id] = deque(maxlen=self.max_turns)

        self._conversations[user_id].append({
            "role": "user",
            "content": user_text,
        })
        self._conversations[user_id].append({
            "role": "jarvis",
            "content": response,
        })

    def get_recent(self, user_id: str, limit: int = 20) -> List[Dict]:
        if user_id not in self._conversations:
            return []

        turns = list(self._conversations[user_id])
        return turns[-limit:]

    def get_last_user_message(self, user_id: str) -> str:
        if user_id not in self._conversations:
            return ""
        for turn in reversed(self._conversations[user_id]):
            if turn["role"] == "user":
                return turn["content"]
        return ""

    def get_last_response(self, user_id: str) -> str:
        if user_id not in self._conversations:
            return ""
        for turn in reversed(self._conversations[user_id]):
            if turn["role"] == "jarvis":
                return turn["content"]
        return ""

    def clear(self, user_id: str) -> None:
        if user_id in self._conversations:
            self._conversations[user_id].clear()

    def get_turn_count(self, user_id: str) -> int:
        if user_id not in self._conversations:
            return 0
        return len(self._conversations[user_id])
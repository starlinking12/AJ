"""
J.A.R.V.I.S. Episodic Memory
Stores complete episodes of interaction for later recall.
"""

import json
import time
from typing import Dict, List, Optional

from jarvis_core.logger import Logger


class EpisodicMemory:
    def __init__(self):
        self.log = Logger("EpisodicMemory")
        self._episodes: List[Dict] = []
        self._max_episodes = 100

    def store_episode(
        self,
        user_id: str,
        summary: str,
        details: Dict,
        importance: float = 0.5
    ) -> None:
        episode = {
            "user_id": user_id,
            "summary": summary,
            "details": details,
            "importance": importance,
            "timestamp": time.time(),
        }
        self._episodes.append(episode)

        if len(self._episodes) > self._max_episodes:
            self._episodes.sort(key=lambda e: e.get("importance", 0))
            self._episodes = self._episodes[-self._max_episodes:]

    def recall_episodes(self, user_id: str, query: str = None, limit: int = 5) -> List[Dict]:
        user_episodes = [e for e in self._episodes if e["user_id"] == user_id]
        user_episodes.sort(key=lambda e: e.get("timestamp", 0), reverse=True)
        return user_episodes[:limit]

    def recall_by_importance(self, user_id: str, min_importance: float = 0.7) -> List[Dict]:
        return [
            e for e in self._episodes
            if e["user_id"] == user_id and e.get("importance", 0) >= min_importance
        ]

    def clear(self, user_id: str = None) -> None:
        if user_id:
            self._episodes = [e for e in self._episodes if e["user_id"] != user_id]
        else:
            self._episodes = []
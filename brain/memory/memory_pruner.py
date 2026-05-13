"""
J.A.R.V.I.S. Memory Pruner
Removes low-value memories to maintain memory health.
"""

import time
from typing import List, Dict

from jarvis_core.logger import Logger


class MemoryPruner:
    def __init__(self):
        self.log = Logger("MemoryPruner")
        self._max_age_seconds = 30 * 24 * 60 * 60
        self._min_importance = 0.2

    def prune_by_age(self, items: List[Dict]) -> List[Dict]:
        current_time = time.time()
        cutoff = current_time - self._max_age_seconds

        kept = []
        pruned_count = 0
        for item in items:
            timestamp = item.get("timestamp", 0)
            if timestamp >= cutoff:
                kept.append(item)
            else:
                pruned_count += 1

        if pruned_count > 0:
            self.log.info(f"Pruned {pruned_count} old memories.")
        return kept

    def prune_by_importance(self, items: List[Dict]) -> List[Dict]:
        kept = []
        pruned_count = 0
        for item in items:
            importance = item.get("importance", 0.5)
            if importance >= self._min_importance:
                kept.append(item)
            else:
                pruned_count += 1

        if pruned_count > 0:
            self.log.info(f"Pruned {pruned_count} low-importance memories.")
        return kept

    def prune(self, items: List[Dict]) -> List[Dict]:
        items = self.prune_by_age(items)
        items = self.prune_by_importance(items)
        return items

    def set_max_age(self, days: int) -> None:
        self._max_age_seconds = days * 24 * 60 * 60

    def set_min_importance(self, importance: float) -> None:
        self._min_importance = max(0.0, min(1.0, importance))
"""
J.A.R.V.I.S. Context Compactor
Compresses and prunes stale context to prevent memory bloat.
"""

from typing import List, Dict

from jarvis_core.logger import Logger


class ContextCompactor:
    def __init__(self, max_items: int = 100):
        self.log = Logger("ContextCompactor")
        self.max_items = max_items

    def compact(self, items: List[Dict]) -> List[Dict]:
        if len(items) <= self.max_items:
            return items

        items.sort(key=lambda x: x.get("timestamp", 0), reverse=True)
        items = items[:self.max_items]

        items.sort(key=lambda x: x.get("importance", 0.5), reverse=True)
        return items

    def summarize_old(self, items: List[Dict], keep_recent: int = 20) -> List[Dict]:
        if len(items) <= keep_recent:
            return items

        recent = items[-keep_recent:]
        old = items[:-keep_recent]

        if old:
            summary = f"[{len(old)} earlier interactions summarized]"
            recent.insert(0, {
                "role": "system",
                "content": summary,
                "is_summary": True,
            })

        return recent

    def remove_duplicates(self, items: List[Dict]) -> List[Dict]:
        seen = set()
        unique = []
        for item in items:
            content = item.get("content", "")
            if content not in seen:
                seen.add(content)
                unique.append(item)
        return unique

    def get_compression_ratio(self, original_count: int, compacted_count: int) -> float:
        if original_count == 0:
            return 1.0
        return compacted_count / original_count
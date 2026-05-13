"""
J.A.R.V.I.S. Task Planner
Breaks complex commands into executable task sequences.
"""

from typing import Dict, Any, List, Optional

from jarvis_core.logger import Logger


class TaskPlanner:
    def __init__(self):
        self.log = Logger("TaskPlanner")
        self._tasks: List[Dict] = []
        self._initialized = False

    def initialize(self) -> bool:
        self._initialized = True
        self.log.info("Task planner ready.")
        return True

    def plan(self, user_text: str, intent: str) -> List[Dict[str, Any]]:
        self._tasks = []

        if intent == "search":
            self._tasks.append({
                "type": "search",
                "query": user_text,
                "priority": 1,
                "requires_display": True,
            })

        elif intent == "news":
            self._tasks.append({
                "type": "news",
                "action": "fetch_headlines",
                "priority": 1,
                "requires_display": True,
            })

        elif intent == "weather":
            self._tasks.append({
                "type": "weather",
                "action": "get_current",
                "priority": 1,
                "requires_display": True,
            })

        elif intent == "map":
            self._tasks.append({
                "type": "map",
                "action": "show_location",
                "query": user_text,
                "priority": 1,
                "requires_display": True,
            })

        elif intent == "system":
            self._tasks.append({
                "type": "system",
                "action": "execute",
                "command": user_text,
                "priority": 1,
                "requires_display": False,
            })

        elif intent == "camera":
            self._tasks.append({
                "type": "camera",
                "action": "open",
                "priority": 1,
                "requires_display": True,
            })

        elif intent == "music":
            self._tasks.append({
                "type": "music",
                "action": "play",
                "query": user_text,
                "priority": 1,
                "requires_display": False,
            })

        return self._tasks

    def get_actions(self) -> List[Dict]:
        return self._tasks

    def clear(self) -> None:
        self._tasks = []
"""
J.A.R.V.I.S. Working Memory
Holds active context for the current task.
"""

from typing import Dict, Any, Optional

from jarvis_core.logger import Logger


class WorkingMemory:
    def __init__(self):
        self.log = Logger("WorkingMemory")
        self._data: Dict[str, Any] = {}
        self._active_task: Optional[str] = None
        self._task_context: Dict[str, Any] = {}

    def set(self, key: str, value: Any) -> None:
        self._data[key] = value

    def get(self, key: str, default: Any = None) -> Any:
        return self._data.get(key, default)

    def set_task(self, task_name: str, context: Dict[str, Any] = None) -> None:
        self._active_task = task_name
        self._task_context = context or {}

    def get_active_task(self) -> Optional[str]:
        return self._active_task

    def get_task_context(self) -> Dict[str, Any]:
        return self._task_context

    def clear_task(self) -> None:
        self._active_task = None
        self._task_context = {}

    def clear(self) -> None:
        self._data = {}
        self._active_task = None
        self._task_context = {}

    def has(self, key: str) -> bool:
        return key in self._data
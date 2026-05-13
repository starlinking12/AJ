"""
J.A.R.V.I.S. Context Window Manager
Manages the LLM context window to prevent overflow and optimize performance.
"""

from typing import List, Dict

from jarvis_core.logger import Logger


class ContextWindowManager:
    def __init__(self, max_tokens: int = 4096):
        self.log = Logger("ContextWindow")
        self.max_tokens = max_tokens
        self._current_tokens = 0
        self._messages: List[Dict] = []

    def estimate_tokens(self, text: str) -> int:
        """Rough token estimation: ~4 characters per token."""
        return len(text) // 4

    def can_add(self, text: str) -> bool:
        estimated = self.estimate_tokens(text)
        return (self._current_tokens + estimated) <= self.max_tokens

    def add_message(self, role: str, content: str) -> bool:
        estimated = self.estimate_tokens(content)

        while (self._current_tokens + estimated) > self.max_tokens and self._messages:
            removed = self._messages.pop(0)
            self._current_tokens -= self.estimate_tokens(removed.get("content", ""))
            self.log.debug("Removed oldest message to free context space.")

        self._messages.append({"role": role, "content": content})
        self._current_tokens += estimated
        return True

    def get_messages(self) -> List[Dict]:
        return self._messages

    def get_usage_percent(self) -> float:
        return (self._current_tokens / self.max_tokens) * 100.0

    def clear(self) -> None:
        self._messages.clear()
        self._current_tokens = 0

    def set_max_tokens(self, max_tokens: int) -> None:
        self.max_tokens = max_tokens
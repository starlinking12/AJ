"""
J.A.R.V.I.S. Prompt Compressor
Compresses long prompts to fit within context window limits.
"""

from typing import List, Dict

from jarvis_core.logger import Logger


class PromptCompressor:
    def __init__(self, target_tokens: int = 2048):
        self.log = Logger("PromptCompressor")
        self.target_tokens = target_tokens

    def compress(self, text: str) -> str:
        if self._estimate_tokens(text) <= self.target_tokens:
            return text

        compressed = self._remove_redundancy(text)
        compressed = self._summarize_long_sections(compressed)
        compressed = self._truncate_oldest(compressed)

        return compressed

    def compress_messages(self, messages: List[Dict]) -> List[Dict]:
        total = sum(self._estimate_tokens(m.get("content", "")) for m in messages)

        if total <= self.target_tokens:
            return messages

        while messages and total > self.target_tokens:
            removed = messages.pop(0)
            total -= self._estimate_tokens(removed.get("content", ""))

        return messages

    def _estimate_tokens(self, text: str) -> int:
        return len(text) // 4

    def _remove_redundancy(self, text: str) -> str:
        lines = text.split("\n")
        seen = set()
        unique = []
        for line in lines:
            stripped = line.strip().lower()
            if stripped and stripped not in seen:
                unique.append(line)
                seen.add(stripped)
            elif not stripped:
                unique.append(line)
        return "\n".join(unique)

    def _summarize_long_sections(self, text: str) -> str:
        lines = text.split("\n")
        result = []
        for line in lines:
            if len(line) > 500:
                line = line[:497] + "..."
            result.append(line)
        return "\n".join(result)

    def _truncate_oldest(self, text: str) -> str:
        if self._estimate_tokens(text) <= self.target_tokens:
            return text
        return text[:self.target_tokens * 4] + "\n... [content truncated]"

    def get_compression_ratio(self, original: str, compressed: str) -> float:
        orig_tokens = self._estimate_tokens(original)
        comp_tokens = self._estimate_tokens(compressed)
        if orig_tokens == 0:
            return 1.0
        return comp_tokens / orig_tokens
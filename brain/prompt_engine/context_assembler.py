"""
J.A.R.V.I.S. Context Assembler
Builds the complete context payload for LLM inference.
"""

from typing import Dict, Any, List

from jarvis_core.logger import Logger


class ContextAssembler:
    def __init__(self, max_context_length: int = 4000):
        self.log = Logger("ContextAssembler")
        self.max_context_length = max_context_length

    def build(
        self,
        user_text: str,
        intent: str,
        memories: List[Dict],
        user_id: str = "lord_vader"
    ) -> str:
        sections = []

        sections.append(f"User: {user_id}")
        sections.append(f"Detected Intent: {intent}")

        if memories:
            memory_text = self._format_memories(memories)
            sections.append(f"Relevant Memories:\n{memory_text}")

        context = "\n\n".join(sections)

        if len(context) > self.max_context_length:
            context = self._truncate(context)

        return context

    def _format_memories(self, memories: List[Dict]) -> str:
        lines = []
        for mem in memories[:5]:
            content = mem.get("content", "")
            timestamp = mem.get("timestamp", "")
            if timestamp:
                lines.append(f"[{timestamp}] {content}")
            else:
                lines.append(f"- {content}")
        return "\n".join(lines)

    def build_conversation_history(
        self,
        messages: List[Dict],
        max_messages: int = 10
    ) -> str:
        recent = messages[-max_messages:]
        lines = []
        for msg in recent:
            role = msg.get("role", "unknown")
            content = msg.get("content", "")
            if role == "user":
                lines.append(f"User: {content}")
            elif role == "jarvis":
                lines.append(f"J.A.R.V.I.S.: {content}")
        return "\n".join(lines)

    def _truncate(self, text: str) -> str:
        if len(text) <= self.max_context_length:
            return text
        return text[:self.max_context_length - 3] + "..."

    def set_max_length(self, length: int) -> None:
        self.max_context_length = length
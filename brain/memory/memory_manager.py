"""
J.A.R.V.I.S. Memory Manager
Central memory coordinator. Manages short-term, long-term, and working memory.
"""

from typing import Dict, Any, List, Optional

from brain.memory.short_term import ShortTermMemory
from brain.memory.working_memory import WorkingMemory
from brain.memory.long_term import LongTermMemory
from brain.memory.vector_store import VectorStore
from brain.memory.relational_store import RelationalStore
from brain.memory.cache_layer import CacheLayer

from jarvis_core.logger import Logger


class MemoryManager:
    def __init__(self):
        self.log = Logger("MemoryManager")
        self.short_term = ShortTermMemory()
        self.working = WorkingMemory()
        self.long_term = LongTermMemory()
        self.vector_store = VectorStore()
        self.relational = RelationalStore()
        self.cache = CacheLayer()
        self._initialized = False

    def initialize(self) -> bool:
        self.log.info("Initializing memory systems...")

        try:
            self.vector_store.initialize()
            self.relational.initialize()
            self.log.info("Memory systems ready.")
            self._initialized = True
            return True
        except Exception as e:
            self.log.error(f"Memory init failed: {e}")
            return False

    def save_interaction(
        self,
        user_id: str,
        user_text: str,
        response: str,
        intent: str
    ) -> None:
        self.short_term.add(user_id, user_text, response)

        self.long_term.store_interaction(
            user_id=user_id,
            user_text=user_text,
            response=response,
            intent=intent
        )

        self.vector_store.add_document(
            text=f"User: {user_text}\nJarvis: {response}",
            metadata={
                "user_id": user_id,
                "intent": intent,
                "type": "interaction"
            }
        )

    def retrieve_relevant(self, query: str, user_id: str, limit: int = 5) -> List[Dict]:
        recent = self.short_term.get_recent(user_id, limit=3)

        similar = self.vector_store.search(query, limit=limit)

        memories = recent + similar
        seen = set()
        unique = []
        for mem in memories:
            content = mem.get("content", "")
            if content not in seen:
                seen.add(content)
                unique.append(mem)

        return unique[:limit]

    def get_conversation_history(self, user_id: str, limit: int = 20) -> List[Dict]:
        return self.short_term.get_recent(user_id, limit=limit)

    def save_fact(self, user_id: str, key: str, value: Any) -> None:
        self.long_term.store_fact(user_id, key, value)

    def get_fact(self, user_id: str, key: str) -> Optional[Any]:
        return self.long_term.get_fact(user_id, key)

    def clear_short_term(self, user_id: str) -> None:
        self.short_term.clear(user_id)

    def close(self) -> None:
        self.vector_store.close()
        self.relational.close()
        self.log.info("Memory systems closed.")
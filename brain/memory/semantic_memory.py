"""
J.A.R.V.I.S. Semantic Memory
Stores general knowledge and learned facts.
"""

from typing import Dict, List, Any, Optional

from jarvis_core.logger import Logger


class SemanticMemory:
    def __init__(self):
        self.log = Logger("SemanticMemory")
        self._knowledge: Dict[str, Any] = {}
        self._relationships: List[Dict] = []

    def store(self, entity: str, attribute: str, value: Any) -> None:
        if entity not in self._knowledge:
            self._knowledge[entity] = {}
        self._knowledge[entity][attribute] = value

    def retrieve(self, entity: str, attribute: str = None) -> Optional[Any]:
        if entity not in self._knowledge:
            return None
        if attribute:
            return self._knowledge[entity].get(attribute)
        return self._knowledge[entity]

    def add_relationship(self, entity_a: str, relation: str, entity_b: str) -> None:
        self._relationships.append({
            "entity_a": entity_a,
            "relation": relation,
            "entity_b": entity_b,
        })

    def query_relationships(self, entity: str) -> List[Dict]:
        return [
            r for r in self._relationships
            if r["entity_a"] == entity or r["entity_b"] == entity
        ]

    def search(self, keyword: str) -> List[str]:
        results = []
        for entity, attributes in self._knowledge.items():
            if keyword.lower() in entity.lower():
                results.append(entity)
            for attr, value in attributes.items():
                if keyword.lower() in str(value).lower():
                    results.append(f"{entity}.{attr}")
        return results

    def clear(self) -> None:
        self._knowledge = {}
        self._relationships = []
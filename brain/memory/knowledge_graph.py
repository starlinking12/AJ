"""
J.A.R.V.I.S. Knowledge Graph
Entity-relationship graph for structured knowledge representation.
"""

from typing import Dict, List, Set, Tuple, Any, Optional

from jarvis_core.logger import Logger


class KnowledgeGraph:
    def __init__(self):
        self.log = Logger("KnowledgeGraph")
        self._entities: Dict[str, Dict] = {}
        self._relationships: List[Tuple[str, str, str]] = []

    def add_entity(self, name: str, properties: Dict = None) -> None:
        if name not in self._entities:
            self._entities[name] = {}
        if properties:
            self._entities[name].update(properties)

    def add_relationship(self, entity_a: str, relation: str, entity_b: str) -> None:
        if entity_a not in self._entities:
            self._entities[entity_a] = {}
        if entity_b not in self._entities:
            self._entities[entity_b] = {}
        self._relationships.append((entity_a, relation, entity_b))

    def get_entity(self, name: str) -> Optional[Dict]:
        return self._entities.get(name)

    def get_relationships(self, entity: str) -> List[Dict]:
        results = []
        for a, r, b in self._relationships:
            if a == entity:
                results.append({"entity": b, "relation": r, "direction": "outgoing"})
            if b == entity:
                results.append({"entity": a, "relation": r, "direction": "incoming"})
        return results

    def search(self, keyword: str) -> List[str]:
        keyword_lower = keyword.lower()
        return [
            name for name in self._entities
            if keyword_lower in name.lower()
        ]

    def get_all_entities(self) -> List[str]:
        return list(self._entities.keys())

    def get_statistics(self) -> Dict:
        return {
            "entities": len(self._entities),
            "relationships": len(self._relationships),
        }
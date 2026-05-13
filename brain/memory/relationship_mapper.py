"""
J.A.R.V.I.S. Relationship Mapper
Discovers and maps relationships between entities.
"""

from typing import List, Dict, Tuple

from jarvis_core.logger import Logger


class RelationshipMapper:
    def __init__(self):
        self.log = Logger("RelationshipMapper")
        self._patterns = [
            ("is a", "TYPE_OF"),
            ("is the", "TYPE_OF"),
            ("lives in", "LOCATED_IN"),
            ("works at", "EMPLOYED_BY"),
            ("located in", "LOCATED_IN"),
            ("part of", "PART_OF"),
            ("belongs to", "OWNED_BY"),
            ("created by", "CREATED_BY"),
            ("built by", "CREATED_BY"),
            ("uses", "USES"),
        ]

    def map_relationships(self, text: str, entities: List[Dict]) -> List[Tuple[str, str, str]]:
        relationships = []

        text_lower = text.lower()

        if len(entities) >= 2:
            for i in range(len(entities)):
                for j in range(i + 1, len(entities)):
                    entity_a = entities[i]["text"]
                    entity_b = entities[j]["text"]

                    for pattern, relation in self._patterns:
                        if self._check_pattern(text_lower, entity_a.lower(), entity_b.lower(), pattern):
                            relationships.append((entity_a, relation, entity_b))
                            break

        return relationships

    def _check_pattern(
        self,
        text: str,
        entity_a: str,
        entity_b: str,
        pattern: str
    ) -> bool:
        if f"{entity_a} {pattern} {entity_b}" in text:
            return True
        if f"{entity_b} {pattern} {entity_a}" in text:
            return True
        return False

    def add_pattern(self, phrase: str, relation_type: str) -> None:
        self._patterns.append((phrase.lower(), relation_type))
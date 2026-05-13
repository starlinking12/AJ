"""
J.A.R.V.I.S. Entity Extractor
Extracts named entities from text for knowledge graph population.
"""

from typing import List, Dict

from jarvis_core.logger import Logger


class EntityExtractor:
    def __init__(self):
        self.log = Logger("EntityExtractor")
        self._initialized = False
        self._model = None

    def initialize(self) -> bool:
        try:
            import spacy
            self._model = spacy.load("en_core_web_sm")
            self._initialized = True
            self.log.info("Entity extractor ready.")
            return True
        except ImportError:
            self.log.warn("spacy not installed. Using basic extraction.")
            self._initialized = True
            return True
        except Exception as e:
            self.log.warn(f"Entity extractor init failed: {e}")
            self._initialized = True
            return True

    def extract(self, text: str) -> List[Dict]:
        entities = []

        if self._model:
            try:
                doc = self._model(text)
                for ent in doc.ents:
                    entities.append({
                        "text": ent.text,
                        "type": ent.label_,
                        "start": ent.start_char,
                        "end": ent.end_char,
                    })
                return entities
            except Exception:
                pass

        common_entities = {
            "Jarvis": "PERSON",
            "J.A.R.V.I.S.": "PERSON",
            "London": "GPE",
            "Paris": "GPE",
            "New York": "GPE",
            "Tokyo": "GPE",
            "Google": "ORG",
            "Microsoft": "ORG",
            "OpenAI": "ORG",
            "Monday": "DATE",
            "Tuesday": "DATE",
            "Wednesday": "DATE",
            "Thursday": "DATE",
            "Friday": "DATE",
            "Saturday": "DATE",
            "Sunday": "DATE",
        }

        for word, entity_type in common_entities.items():
            if word.lower() in text.lower():
                entities.append({
                    "text": word,
                    "type": entity_type,
                    "start": text.lower().index(word.lower()),
                    "end": text.lower().index(word.lower()) + len(word),
                })

        return entities
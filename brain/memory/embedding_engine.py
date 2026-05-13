"""
J.A.R.V.I.S. Embedding Engine
Generates vector embeddings for text.
"""

from typing import List, Optional

from jarvis_core.logger import Logger


class EmbeddingEngine:
    def __init__(self, model_name: str = "all-MiniLM-L6-v2"):
        self.log = Logger("EmbeddingEngine")
        self.model_name = model_name
        self._model = None
        self._initialized = False

    def initialize(self) -> bool:
        try:
            from sentence_transformers import SentenceTransformer
            self._model = SentenceTransformer(self.model_name)
            self._initialized = True
            self.log.info(f"Embedding engine ready. Model: {self.model_name}")
            return True
        except ImportError:
            self.log.warn("sentence-transformers not installed.")
            return False
        except Exception as e:
            self.log.warn(f"Embedding engine init failed: {e}")
            return False

    def embed(self, text: str) -> Optional[List[float]]:
        if not self._initialized or self._model is None:
            return None
        try:
            embedding = self._model.encode(text)
            return embedding.tolist()
        except Exception as e:
            self.log.error(f"Embedding failed: {e}")
            return None

    def embed_batch(self, texts: List[str]) -> List[List[float]]:
        if not self._initialized or self._model is None:
            return []
        try:
            embeddings = self._model.encode(texts)
            return embeddings.tolist()
        except Exception as e:
            self.log.error(f"Batch embedding failed: {e}")
            return []
"""
J.A.R.V.I.S. Vector Store
Semantic search using ChromaDB for similarity-based memory retrieval.
"""

from typing import List, Dict, Any, Optional

from jarvis_core.logger import Logger


class VectorStore:
    def __init__(self, collection_name: str = "jarvis_memory"):
        self.log = Logger("VectorStore")
        self.collection_name = collection_name
        self._client = None
        self._collection = None
        self._initialized = False

    def initialize(self) -> bool:
        try:
            import chromadb

            self._client = chromadb.Client()
            try:
                self._collection = self._client.get_collection(self.collection_name)
            except Exception:
                self._collection = self._client.create_collection(self.collection_name)

            self._initialized = True
            self.log.info(f"Vector store ready. Collection: {self.collection_name}")
            return True

        except ImportError:
            self.log.warn("chromadb not installed. Vector store disabled.")
            return False
        except Exception as e:
            self.log.warn(f"Vector store init failed: {e}")
            return False

    def add_document(self, text: str, metadata: Dict[str, Any], doc_id: str = None) -> bool:
        if not self._initialized or self._collection is None:
            return False

        try:
            import uuid

            if doc_id is None:
                doc_id = str(uuid.uuid4())

            self._collection.add(
                documents=[text],
                metadatas=[metadata],
                ids=[doc_id],
            )
            return True

        except Exception as e:
            self.log.error(f"Failed to add document: {e}")
            return False

    def search(self, query: str, limit: int = 5) -> List[Dict[str, Any]]:
        if not self._initialized or self._collection is None:
            return []

        try:
            results = self._collection.query(
                query_texts=[query],
                n_results=limit,
            )

            memories = []
            if results and results.get("documents"):
                for i, doc in enumerate(results["documents"][0]):
                    memory = {"content": doc}
                    if results.get("metadatas") and results["metadatas"][0]:
                        memory["metadata"] = results["metadatas"][0][i]
                    if results.get("distances") and results["distances"][0]:
                        memory["distance"] = results["distances"][0][i]
                    memories.append(memory)

            return memories

        except Exception as e:
            self.log.error(f"Vector search failed: {e}")
            return []

    def delete_collection(self) -> bool:
        if self._client:
            try:
                self._client.delete_collection(self.collection_name)
                return True
            except Exception:
                pass
        return False

    def close(self) -> None:
        self._client = None
        self._collection = None
        self._initialized = False
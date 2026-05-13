"""
J.A.R.V.I.S. Model Registry
Manages available LLM models and their capabilities.
"""

from typing import Dict, List, Optional

from jarvis_core.logger import Logger


class ModelRegistry:
    def __init__(self):
        self.log = Logger("ModelRegistry")
        self._models: Dict[str, Dict] = {}
        self._load_builtin_models()

    def _load_builtin_models(self) -> None:
        builtin = {
            "llama3.2:3b": {
                "provider": "meta",
                "size": "3B",
                "context_length": 128000,
                "strengths": ["fast", "chat", "general"],
                "memory_required": "4GB",
                "recommended": True,
            },
            "llama3.2:8b": {
                "provider": "meta",
                "size": "8B",
                "context_length": 128000,
                "strengths": ["reasoning", "code", "complex"],
                "memory_required": "8GB",
                "recommended": True,
            },
            "mistral:7b": {
                "provider": "mistral",
                "size": "7B",
                "context_length": 32768,
                "strengths": ["fast", "efficient", "multilingual"],
                "memory_required": "8GB",
                "recommended": True,
            },
            "phi3:3.8b": {
                "provider": "microsoft",
                "size": "3.8B",
                "context_length": 128000,
                "strengths": ["fast", "compact", "reasoning"],
                "memory_required": "4GB",
                "recommended": False,
            },
        }
        self._models.update(builtin)

    def register(self, name: str, info: Dict) -> None:
        self._models[name] = info
        self.log.info(f"Model registered: {name}")

    def get_model_info(self, name: str) -> Optional[Dict]:
        return self._models.get(name)

    def list_models(self) -> List[str]:
        return list(self._models.keys())

    def get_recommended(self) -> List[str]:
        return [name for name, info in self._models.items() if info.get("recommended")]

    def get_by_strength(self, strength: str) -> List[str]:
        return [
            name for name, info in self._models.items()
            if strength in info.get("strengths", [])
        ]

    def get_by_memory(self, max_memory_gb: int) -> List[str]:
        result = []
        for name, info in self._models.items():
            mem = info.get("memory_required", "999GB")
            try:
                mem_gb = int(mem.replace("GB", ""))
                if mem_gb <= max_memory_gb:
                    result.append(name)
            except ValueError:
                pass
        return result
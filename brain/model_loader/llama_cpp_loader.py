"""
J.A.R.V.I.S. LlamaCpp Loader
Alternative LLM loader using llama-cpp-python for direct model loading.
Useful when Ollama is not available.
"""

from pathlib import Path
from typing import Optional

from jarvis_core.logger import Logger


class LlamaCppLoader:
    def __init__(self):
        self.log = Logger("LlamaCppLoader")
        self._model = None
        self._model_path: Optional[Path] = None
        self._initialized = False

    def initialize(self, model_path: str) -> bool:
        try:
            from llama_cpp import Llama

            self._model_path = Path(model_path)
            if not self._model_path.exists():
                self.log.error(f"Model not found: {model_path}")
                return False

            self._model = Llama(
                model_path=str(self._model_path),
                n_ctx=4096,
                n_threads=4,
                verbose=False,
            )

            self._initialized = True
            self.log.info(f"LlamaCpp loaded: {self._model_path.name}")
            return True

        except ImportError:
            self.log.warn("llama-cpp-python not installed.")
            return False
        except Exception as e:
            self.log.warn(f"LlamaCpp init failed: {e}")
            return False

    def generate(self, prompt: str, max_tokens: int = 256) -> str:
        if not self._initialized or self._model is None:
            return ""

        try:
            output = self._model(
                prompt,
                max_tokens=max_tokens,
                stop=["User:", "J.A.R.V.I.S.:"],
                echo=False,
            )
            return output["choices"][0]["text"].strip()
        except Exception as e:
            self.log.error(f"LlamaCpp generation failed: {e}")
            return ""

    def close(self) -> None:
        if self._model:
            del self._model
            self._model = None
        self._initialized = False
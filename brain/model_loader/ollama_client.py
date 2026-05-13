"""
J.A.R.V.I.S. Ollama Client
Primary LLM interface using Ollama for local inference.
"""

import json
import time
from typing import Optional, Dict, Any, Generator

import requests

from jarvis_core.logger import Logger


class OllamaClient:
    def __init__(self, config):
        self.log = Logger("OllamaClient")
        self.host = getattr(config, 'ollama_host', 'http://localhost:11434')
        self.model = getattr(config, 'ollama_model', 'llama3.2:3b')
        self._initialized = False
        self._available = False
        self._timeout = 60

    def initialize(self) -> bool:
        self.log.info(f"Connecting to Ollama at {self.host}...")

        try:
            response = requests.get(f"{self.host}/api/tags", timeout=5)
            if response.status_code == 200:
                models = response.json().get("models", [])
                model_names = [m.get("name") for m in models]

                if self.model in model_names:
                    self._available = True
                    self._initialized = True
                    self.log.info(f"Ollama ready. Model: {self.model}")
                    return True

                if model_names:
                    self.log.warn(f"Model {self.model} not found. Available: {model_names}")
                    self.log.info(f"Pull with: ollama pull {self.model}")
                else:
                    self.log.warn("No models found. Pull one first.")
        except requests.exceptions.ConnectionError:
            self.log.error(f"Cannot connect to Ollama at {self.host}")
        except Exception as e:
            self.log.error(f"Ollama connection error: {e}")

        self._initialized = True
        return False

    def generate(
        self,
        system_prompt: str,
        user_message: str,
        context: str = "",
        temperature: float = 0.7
    ) -> str:
        if not self._available:
            return self._fallback_response(user_message)

        full_prompt = f"{system_prompt}\n\n{context}\n\nUser: {user_message}\nJ.A.R.V.I.S.:"

        try:
            payload = {
                "model": self.model,
                "prompt": full_prompt,
                "stream": False,
                "options": {
                    "temperature": temperature,
                    "num_predict": 256,
                }
            }

            response = requests.post(
                f"{self.host}/api/generate",
                json=payload,
                timeout=self._timeout
            )

            if response.status_code == 200:
                result = response.json()
                return result.get("response", "").strip()

            self.log.error(f"Ollama error: {response.status_code}")
            return self._fallback_response(user_message)

        except requests.exceptions.Timeout:
            self.log.error("Ollama request timed out.")
            return "My apologies, Sir. I seem to be thinking slowly."
        except Exception as e:
            self.log.error(f"Generation failed: {e}")
            return self._fallback_response(user_message)

    def generate_stream(self, system_prompt: str, user_message: str, context: str = ""):
        """Stream tokens as they are generated."""
        if not self._available:
            yield self._fallback_response(user_message)
            return

        full_prompt = f"{system_prompt}\n\n{context}\n\nUser: {user_message}\nJ.A.R.V.I.S.:"

        try:
            payload = {
                "model": self.model,
                "prompt": full_prompt,
                "stream": True,
            }

            response = requests.post(
                f"{self.host}/api/generate",
                json=payload,
                stream=True,
                timeout=self._timeout
            )

            for line in response.iter_lines():
                if line:
                    data = json.loads(line)
                    token = data.get("response", "")
                    if token:
                        yield token

        except Exception as e:
            self.log.error(f"Stream generation failed: {e}")
            yield self._fallback_response(user_message)

    def pull_model(self, model_name: str) -> bool:
        self.log.info(f"Pulling model: {model_name}")
        try:
            response = requests.post(
                f"{self.host}/api/pull",
                json={"name": model_name},
                timeout=300
            )
            return response.status_code == 200
        except Exception as e:
            self.log.error(f"Model pull failed: {e}")
            return False

    def list_models(self) -> list:
        try:
            response = requests.get(f"{self.host}/api/tags", timeout=5)
            if response.status_code == 200:
                return [m.get("name") for m in response.json().get("models", [])]
        except Exception:
            pass
        return []

    def is_available(self) -> bool:
        return self._available

    def close(self) -> None:
        self.log.info("Ollama client closed.")

    def _fallback_response(self, user_message: str) -> str:
        return "I am unable to process that at the moment, Sir. Please ensure Ollama is running with a model loaded."
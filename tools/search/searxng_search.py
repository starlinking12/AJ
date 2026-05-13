"""
J.A.R.V.I.S. SearXNG Search
Uses self-hosted or public SearXNG instances. Fully private, no API key needed.
"""

from typing import Dict, Any

import requests

from jarvis_core.logger import Logger


class SearXNGSearcher:
    def __init__(self, instance_url: str = "http://localhost:8080"):
        self.log = Logger("SearXNGSearcher")
        self.instance_url = instance_url
        self._initialized = False

    def initialize(self) -> bool:
        try:
            response = requests.get(f"{self.instance_url}/config", timeout=5)
            if response.status_code == 200:
                self._initialized = True
                self.log.info(f"SearXNG ready: {self.instance_url}")
                return True
        except Exception:
            pass

        self.log.warn("SearXNG not available.")
        return False

    def search(self, query: str, max_results: int = 5) -> Dict[str, Any]:
        if not self._initialized:
            return {"query": query, "results": []}

        try:
            params = {
                "q": query,
                "format": "json",
                "categories": "general",
            }

            response = requests.get(f"{self.instance_url}/search", params=params, timeout=15)
            if response.status_code == 200:
                data = response.json()
                results = []
                for r in data.get("results", [])[:max_results]:
                    results.append({
                        "title": r.get("title", ""),
                        "url": r.get("url", ""),
                        "content": r.get("content", r.get("snippet", "")),
                    })
                return {"query": query, "results": results, "source": "searxng"}

            return {"query": query, "results": []}

        except Exception as e:
            self.log.error(f"SearXNG search failed: {e}")
            return {"query": query, "results": [], "error": str(e)}
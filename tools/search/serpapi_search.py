"""
J.A.R.V.I.S. SerpAPI Search
Uses SerpAPI for broad search engine coverage.
"""

import os
from typing import Dict, Any

import requests

from jarvis_core.logger import Logger


class SerpAPISearch:
    def __init__(self):
        self.log = Logger("SerpAPISearch")
        self.api_key = os.environ.get("SERPAPI_API_KEY", "")
        self.base_url = "https://serpapi.com/search"
        self._initialized = False

    def initialize(self) -> bool:
        if not self.api_key:
            self.log.warn("SerpAPI key not set.")
            return False
        self._initialized = True
        return True

    def search(self, query: str, max_results: int = 5) -> Dict[str, Any]:
        if not self._initialized:
            return {"query": query, "results": []}

        try:
            params = {
                "api_key": self.api_key,
                "q": query,
                "num": max_results,
                "engine": "google",
            }

            response = requests.get(self.base_url, params=params, timeout=15)
            if response.status_code == 200:
                data = response.json()
                results = []
                for r in data.get("organic_results", [])[:max_results]:
                    results.append({
                        "title": r.get("title", ""),
                        "url": r.get("link", ""),
                        "content": r.get("snippet", ""),
                    })
                return {"query": query, "results": results, "source": "serpapi"}

            return {"query": query, "results": []}

        except Exception as e:
            self.log.error(f"SerpAPI search failed: {e}")
            return {"query": query, "results": [], "error": str(e)}
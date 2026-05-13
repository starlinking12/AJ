"""
J.A.R.V.I.S. Brave Search
Uses Brave Search API. Independent index, fast, privacy-focused.
Free tier available.
"""

import os
from typing import Dict, Any

import requests

from jarvis_core.logger import Logger


class BraveSearch:
    def __init__(self):
        self.log = Logger("BraveSearch")
        self.api_key = os.environ.get("BRAVE_API_KEY", "")
        self.base_url = "https://api.search.brave.com/res/v1/web/search"
        self._initialized = False

    def initialize(self) -> bool:
        if not self.api_key:
            self.log.warn("Brave API key not set.")
            return False
        self._initialized = True
        return True

    def search(self, query: str, max_results: int = 5) -> Dict[str, Any]:
        if not self._initialized:
            return {"query": query, "results": []}

        try:
            headers = {
                "Accept": "application/json",
                "Accept-Encoding": "gzip",
                "X-Subscription-Token": self.api_key,
            }
            params = {"q": query, "count": max_results}

            response = requests.get(self.base_url, headers=headers, params=params, timeout=15)
            if response.status_code == 200:
                data = response.json()
                results = []
                for r in data.get("web", {}).get("results", [])[:max_results]:
                    results.append({
                        "title": r.get("title", ""),
                        "url": r.get("url", ""),
                        "content": r.get("description", ""),
                    })
                return {"query": query, "results": results, "source": "brave"}

            return {"query": query, "results": []}

        except Exception as e:
            self.log.error(f"Brave search failed: {e}")
            return {"query": query, "results": [], "error": str(e)}
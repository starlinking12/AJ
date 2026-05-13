"""
J.A.R.V.I.S. Tavily Search
Uses Tavily API for AI-optimized web search.
Free tier: 1000 searches/month.
"""

import os
from typing import Dict, Any, List

import requests

from jarvis_core.logger import Logger


class TavilySearch:
    def __init__(self):
        self.log = Logger("TavilySearch")
        self.api_key = os.environ.get("TAVILY_API_KEY", "")
        self.base_url = "https://api.tavily.com/search"
        self._initialized = False

    def initialize(self) -> bool:
        if not self.api_key:
            self.log.warn("Tavily API key not set.")
            return False
        self._initialized = True
        return True

    def search(self, query: str, max_results: int = 5) -> Dict[str, Any]:
        if not self._initialized:
            return {"query": query, "results": []}

        try:
            payload = {
                "api_key": self.api_key,
                "query": query,
                "max_results": max_results,
                "search_depth": "basic",
            }

            response = requests.post(self.base_url, json=payload, timeout=15)
            if response.status_code == 200:
                data = response.json()
                results = []
                for r in data.get("results", []):
                    results.append({
                        "title": r.get("title", ""),
                        "url": r.get("url", ""),
                        "content": r.get("content", ""),
                        "score": r.get("score", 0),
                    })
                return {"query": query, "results": results, "source": "tavily"}

            return {"query": query, "results": [], "error": f"Status {response.status_code}"}

        except Exception as e:
            self.log.error(f"Tavily search failed: {e}")
            return {"query": query, "results": [], "error": str(e)}
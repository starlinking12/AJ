"""
J.A.R.V.I.S. Search Dispatcher
Routes search queries to the best available search engine.
"""

from typing import Dict, Any, List, Optional

from tools.search.tavily_search import TavilySearch
from tools.search.serpapi_search import SerpAPISearch
from tools.search.brave_search import BraveSearch
from tools.search.searxng_search import SearXNGSearcher
from tools.search.deep_search import DeepSearcher
from tools.search.search_cache import SearchCache

from jarvis_core.logger import Logger


class SearchDispatcher:
    def __init__(self):
        self.log = Logger("SearchDispatcher")
        self.cache = SearchCache()
        self._engines = []
        self._initialized = False

    def initialize(self) -> bool:
        self._engines = [
            TavilySearch(),
            SerpAPISearch(),
            BraveSearch(),
            SearXNGSearcher(),
        ]

        for engine in self._engines:
            try:
                if engine.initialize():
                    self.log.info(f"Search engine ready: {engine.__class__.__name__}")
            except Exception as e:
                self.log.warn(f"Search engine unavailable: {engine.__class__.__name__} - {e}")

        self._initialized = True
        return True

    def search(self, query: str, depth: str = "quick", max_results: int = 5) -> Dict[str, Any]:
        cached = self.cache.get(query)
        if cached:
            self.log.debug("Returning cached search results.")
            return cached

        for engine in self._engines:
            try:
                result = engine.search(query, max_results)
                if result and result.get("results"):
                    self.cache.set(query, result)
                    return result
            except Exception as e:
                self.log.warn(f"Engine {engine.__class__.__name__} failed: {e}")
                continue

        return {"query": query, "results": [], "error": "All search engines failed."}

    def deep_search(self, query: str) -> Dict[str, Any]:
        deep = DeepSearcher(self)
        return deep.search(query)
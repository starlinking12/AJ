"""
J.A.R.V.I.S. Place Search
Searches for places near a location using OSM Nominatim.
"""

import time
from typing import List, Dict, Optional

import requests

from jarvis_core.logger import Logger


class PlaceSearch:
    def __init__(self):
        self.log = Logger("PlaceSearch")
        self.base_url = "https://nominatim.openstreetmap.org/search"
        self._last_request = 0
        self._min_interval = 1.0
        self._initialized = False

    def initialize(self) -> bool:
        self._initialized = True
        self.log.info("Place search ready.")
        return True

    def search(
        self,
        query: str,
        lat: Optional[float] = None,
        lng: Optional[float] = None,
        limit: int = 5
    ) -> List[Dict]:
        if not self._initialized:
            return []

        self._rate_limit()

        try:
            params = {
                "q": query,
                "format": "json",
                "limit": limit,
            }
            headers = {
                "User-Agent": "JARVIS/1.0 (Lord Vader's Assistant)"
            }

            response = requests.get(
                self.base_url,
                params=params,
                headers=headers,
                timeout=10
            )

            if response.status_code == 200:
                results = []
                for r in response.json():
                    results.append({
                        "name": r.get("display_name", ""),
                        "lat": float(r.get("lat", 0)),
                        "lng": float(r.get("lon", 0)),
                        "type": r.get("type", ""),
                        "category": r.get("category", ""),
                    })
                return results

            return []

        except Exception as e:
            self.log.error(f"Place search failed: {e}")
            return []

    def _rate_limit(self) -> None:
        elapsed = time.time() - self._last_request
        if elapsed < self._min_interval:
            time.sleep(self._min_interval - elapsed)
        self._last_request = time.time()
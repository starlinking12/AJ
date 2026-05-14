"""
J.A.R.V.I.S. Nominatim Geocoder
Uses OpenStreetMap Nominatim for free geocoding.
No API key required. Rate limit: 1 request/second.
"""

import time
from typing import Dict, Any, Optional

import requests

from jarvis_core.logger import Logger


class NominatimGeocoder:
    def __init__(self):
        self.log = Logger("NominatimGeocoder")
        self.base_url = "https://nominatim.openstreetmap.org"
        self._last_request = 0
        self._min_interval = 1.0
        self._initialized = False

    def initialize(self) -> bool:
        self._initialized = True
        self.log.info("Nominatim geocoder ready (OpenStreetMap).")
        return True

    def geocode(self, address: str) -> Optional[Dict[str, Any]]:
        if not self._initialized:
            return None

        self._rate_limit()

        try:
            params = {
                "q": address,
                "format": "json",
                "limit": 1,
                "addressdetails": 1,
            }
            headers = {
                "User-Agent": "JARVIS/1.0 (Lord Vader's Assistant)"
            }

            response = requests.get(
                f"{self.base_url}/search",
                params=params,
                headers=headers,
                timeout=10
            )

            if response.status_code == 200:
                results = response.json()
                if results:
                    r = results[0]
                    return {
                        "lat": float(r.get("lat", 0)),
                        "lng": float(r.get("lon", 0)),
                        "display_name": r.get("display_name", ""),
                        "type": r.get("type", ""),
                        "importance": r.get("importance", 0),
                    }

            return None

        except Exception as e:
            self.log.error(f"Nominatim geocoding failed: {e}")
            return None

    def _rate_limit(self) -> None:
        elapsed = time.time() - self._last_request
        if elapsed < self._min_interval:
            time.sleep(self._min_interval - elapsed)
        self._last_request = time.time()
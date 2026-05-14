"""
J.A.R.V.I.S. Reverse Geocoder
Converts coordinates to addresses.
"""

import time
from typing import Dict, Any, Optional

import requests

from jarvis_core.logger import Logger


class ReverseGeocoder:
    def __init__(self):
        self.log = Logger("ReverseGeocoder")
        self.base_url = "https://nominatim.openstreetmap.org/reverse"
        self._last_request = 0
        self._min_interval = 1.0
        self._initialized = False

    def initialize(self) -> bool:
        self._initialized = True
        self.log.info("Reverse geocoder ready.")
        return True

    def lookup(self, lat: float, lng: float) -> Optional[Dict[str, Any]]:
        if not self._initialized:
            return None

        self._rate_limit()

        try:
            params = {
                "lat": lat,
                "lon": lng,
                "format": "json",
                "addressdetails": 1,
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
                data = response.json()
                return {
                    "lat": lat,
                    "lng": lng,
                    "display_name": data.get("display_name", ""),
                    "address": data.get("address", {}),
                    "type": data.get("type", ""),
                }

            return None

        except Exception as e:
            self.log.error(f"Reverse geocoding failed: {e}")
            return None

    def _rate_limit(self) -> None:
        elapsed = time.time() - self._last_request
        if elapsed < self._min_interval:
            time.sleep(self._min_interval - elapsed)
        self._last_request = time.time()
"""
J.A.R.V.I.S. Mapbox Geocoder
Uses Mapbox Geocoding API. Highly customizable map styling.
Free tier available.
"""

import os
from typing import Dict, Any, Optional

import requests

from jarvis_core.logger import Logger


class MapboxGeocoder:
    def __init__(self):
        self.log = Logger("MapboxGeocoder")
        self.api_key = os.environ.get("MAPBOX_API_KEY", "")
        self.base_url = "https://api.mapbox.com/geocoding/v5/mapbox.places"
        self._initialized = False

    def initialize(self) -> bool:
        if not self.api_key:
            self.log.warn("Mapbox API key not set.")
            return False
        self._initialized = True
        return True

    def geocode(self, address: str) -> Optional[Dict[str, Any]]:
        if not self._initialized:
            return None

        try:
            params = {
                "access_token": self.api_key,
                "limit": 1,
            }

            response = requests.get(
                f"{self.base_url}/{requests.utils.quote(address)}.json",
                params=params,
                timeout=10
            )

            if response.status_code == 200:
                data = response.json()
                features = data.get("features", [])
                if features:
                    f = features[0]
                    center = f.get("center", [0, 0])
                    return {
                        "lat": center[1],
                        "lng": center[0],
                        "display_name": f.get("place_name", ""),
                        "type": f.get("place_type", [""])[0] if f.get("place_type") else "",
                        "source": "mapbox",
                    }

            return None

        except Exception as e:
            self.log.error(f"Mapbox geocoding failed: {e}")
            return None
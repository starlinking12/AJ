"""
J.A.R.V.I.S. Elevation Data
Fetches elevation data for coordinates.
Uses Open-Meteo Elevation API. Free, no API key required.
"""

from typing import Optional

import requests

from jarvis_core.logger import Logger


class ElevationData:
    def __init__(self):
        self.log = Logger("ElevationData")
        self.base_url = "https://api.open-meteo.com/v1/elevation"
        self._initialized = False

    def initialize(self) -> bool:
        self._initialized = True
        self.log.info("Elevation data ready (Open-Meteo).")
        return True

    def get(self, lat: float, lng: float) -> Optional[float]:
        if not self._initialized:
            return None

        try:
            params = {
                "latitude": lat,
                "longitude": lng,
            }

            response = requests.get(self.base_url, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()
                elevation = data.get("elevation")
                if elevation is not None and isinstance(elevation, list) and len(elevation) > 0:
                    return float(elevation[0])
                return float(elevation) if elevation else None

            return None

        except Exception as e:
            self.log.error(f"Elevation fetch failed: {e}")
            return None

    def get_elevation_category(self, elevation_meters: float) -> str:
        if elevation_meters < 0:
            return "below sea level"
        elif elevation_meters < 100:
            return "low elevation"
        elif elevation_meters < 500:
            return "moderate elevation"
        elif elevation_meters < 1500:
            return "high elevation"
        elif elevation_meters < 3000:
            return "very high elevation"
        else:
            return "extreme elevation"

    def format_elevation(self, elevation_meters: float) -> str:
        feet = elevation_meters * 3.28084
        return f"{elevation_meters:.0f} meters ({feet:.0f} feet)"
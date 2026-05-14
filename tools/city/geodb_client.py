"""
J.A.R.V.I.S. GeoDB Cities Client
Uses GeoDB Cities API for city information.
Free tier available via RapidAPI.
"""

import os
from typing import Dict, Any, Optional, List

import requests

from jarvis_core.logger import Logger


class GeoDBClient:
    def __init__(self):
        self.log = Logger("GeoDBClient")
        self.api_key = os.environ.get("GEODB_API_KEY", "")
        self.base_url = "https://wft-geo-db.p.rapidapi.com/v1/geo/cities"
        self._initialized = False

    def initialize(self) -> bool:
        if not self.api_key:
            self.log.warn("GeoDB API key not set.")
            return False
        self._initialized = True
        self.log.info("GeoDB client ready.")
        return True

    def lookup(self, city_name: str, country: str = None) -> Optional[Dict[str, Any]]:
        if not self._initialized:
            return None

        try:
            headers = {
                "X-RapidAPI-Key": self.api_key,
                "X-RapidAPI-Host": "wft-geo-db.p.rapidapi.com",
            }
            params = {
                "namePrefix": city_name,
                "limit": 1,
                "sort": "-population",
            }

            if country:
                params["countryIds"] = country

            response = requests.get(self.base_url, headers=headers, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()
                cities = data.get("data", [])
                if cities:
                    c = cities[0]
                    return {
                        "name": c.get("name", city_name),
                        "country": c.get("country", ""),
                        "country_code": c.get("countryCode", ""),
                        "lat": float(c.get("latitude", 0)),
                        "lng": float(c.get("longitude", 0)),
                        "population": int(c.get("population", 0)),
                        "timezone": c.get("timezone", ""),
                        "region": c.get("region", ""),
                        "source": "geodb",
                    }

            return None

        except Exception as e:
            self.log.error(f"GeoDB lookup failed: {e}")
            return None

    def search(self, query: str, max_results: int = 5) -> List[Dict]:
        if not self._initialized:
            return []

        try:
            headers = {
                "X-RapidAPI-Key": self.api_key,
                "X-RapidAPI-Host": "wft-geo-db.p.rapidapi.com",
            }
            params = {
                "namePrefix": query,
                "limit": max_results,
                "sort": "-population",
            }

            response = requests.get(self.base_url, headers=headers, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()
                results = []
                for c in data.get("data", []):
                    results.append({
                        "name": c.get("name", ""),
                        "country": c.get("country", ""),
                        "lat": float(c.get("latitude", 0)),
                        "lng": float(c.get("longitude", 0)),
                        "population": int(c.get("population", 0)),
                    })
                return results

            return []

        except Exception as e:
            self.log.error(f"GeoDB search failed: {e}")
            return []
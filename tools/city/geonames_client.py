"""
J.A.R.V.I.S. GeoNames Client
Uses GeoNames API for comprehensive city data.
Free tier: 20,000 requests/day.
Features: coordinates, population, timezone, elevation, administrative divisions.
"""

import os
from typing import Dict, Any, Optional

import requests

from jarvis_core.logger import Logger


class GeoNamesClient:
    def __init__(self):
        self.log = Logger("GeoNamesClient")
        self.username = os.environ.get("GEONAMES_USERNAME", "demo")
        self.base_url = "http://api.geonames.org/searchJSON"
        self._initialized = False

    def initialize(self) -> bool:
        if self.username == "demo":
            self.log.warn("GeoNames using demo account. Create a free account at geonames.org for full access.")
        self._initialized = True
        self.log.info("GeoNames client ready.")
        return True

    def lookup(self, city_name: str, country: str = None) -> Optional[Dict[str, Any]]:
        if not self._initialized:
            return None

        try:
            params = {
                "q": city_name,
                "maxRows": 1,
                "username": self.username,
                "type": "json",
                "style": "FULL",
                "featureClass": "P",
            }

            if country:
                params["country"] = country

            response = requests.get(self.base_url, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()
                geonames = data.get("geonames", [])
                if geonames:
                    g = geonames[0]
                    return {
                        "name": g.get("name", city_name),
                        "country": g.get("countryName", ""),
                        "country_code": g.get("countryCode", ""),
                        "lat": float(g.get("lat", 0)),
                        "lng": float(g.get("lng", 0)),
                        "population": int(g.get("population", 0)),
                        "timezone": g.get("timezone", {}).get("timeZoneId", "") if isinstance(g.get("timezone"), dict) else "",
                        "elevation": float(g.get("elevation", 0)) if g.get("elevation") else None,
                        "admin_name": g.get("adminName1", ""),
                        "source": "geonames",
                    }

            return None

        except Exception as e:
            self.log.error(f"GeoNames lookup failed: {e}")
            return None

    def search(self, query: str, max_results: int = 5) -> list:
        if not self._initialized:
            return []

        try:
            params = {
                "q": query,
                "maxRows": max_results,
                "username": self.username,
                "type": "json",
                "style": "FULL",
                "featureClass": "P",
            }

            response = requests.get(self.base_url, params=params, timeout=10)

            if response.status_code == 200:
                data = response.json()
                results = []
                for g in data.get("geonames", []):
                    results.append({
                        "name": g.get("name", ""),
                        "country": g.get("countryName", ""),
                        "lat": float(g.get("lat", 0)),
                        "lng": float(g.get("lng", 0)),
                        "population": int(g.get("population", 0)),
                    })
                return results

            return []

        except Exception as e:
            self.log.error(f"GeoNames search failed: {e}")
            return []
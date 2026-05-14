"""
J.A.R.V.I.S. City Dispatcher
Routes city data requests to the best available source.
Primary: GeoNames (free, 20,000 requests/day).
Secondary: GeoDB Cities (free tier).
"""

from typing import Dict, Any, Optional

from tools.city.geonames_client import GeoNamesClient
from tools.city.geodb_client import GeoDBClient
from tools.city.population_data import PopulationData
from tools.city.timezone_lookup import TimezoneLookup
from tools.city.elevation_data import ElevationData
from tools.city.city_cache import CityCache

from jarvis_core.logger import Logger


class CityDispatcher:
    def __init__(self):
        self.log = Logger("CityDispatcher")
        self.cache = CityCache()
        self.population = PopulationData()
        self.timezone_lookup = TimezoneLookup()
        self.elevation = ElevationData()
        self._providers = []
        self._initialized = False

    def initialize(self) -> bool:
        self._providers = [
            GeoNamesClient(),
            GeoDBClient(),
        ]

        for provider in self._providers:
            try:
                if provider.initialize():
                    self.log.info(f"City provider ready: {provider.__class__.__name__}")
            except Exception as e:
                self.log.warn(f"City provider unavailable: {provider.__class__.__name__} - {e}")

        self._initialized = True
        self.log.info("City dispatcher ready.")
        return True

    def lookup(self, city_name: str, country: str = None) -> Dict[str, Any]:
        cache_key = f"{city_name}_{country or 'any'}"
        cached = self.cache.get(cache_key)
        if cached:
            return cached

        for provider in self._providers:
            try:
                result = provider.lookup(city_name, country)
                if result and result.get("name"):
                    self.cache.set(cache_key, result)
                    return result
            except Exception as e:
                self.log.warn(f"Provider {provider.__class__.__name__} failed: {e}")
                continue

        return {"error": f"City not found: {city_name}", "name": city_name}

    def get_population(self, city_name: str, country: str = None) -> Optional[int]:
        data = self.lookup(city_name, country)
        return data.get("population")

    def get_timezone(self, city_name: str, country: str = None) -> Optional[str]:
        data = self.lookup(city_name, country)
        return data.get("timezone")

    def get_elevation(self, city_name: str, country: str = None) -> Optional[float]:
        data = self.lookup(city_name, country)
        lat = data.get("lat")
        lng = data.get("lng")
        if lat and lng:
            return self.elevation.get(lat, lng)
        return None

    def format_for_voice(self, data: Dict[str, Any]) -> str:
        if data.get("error"):
            return f"I could not find information for {data.get('name', 'that city')}, Sir."

        name = data.get("name", "Unknown city")
        country = data.get("country", "")
        population = data.get("population")
        timezone = data.get("timezone")
        elevation = data.get("elevation")

        parts = [f"Information for {name}"]

        if country:
            parts.append(f"in {country}")

        if population:
            if population > 1000000:
                parts.append(f"Population of {population / 1000000:.1f} million")
            else:
                parts.append(f"Population of {population:,}")

        if timezone:
            parts.append(f"Timezone is {timezone}")

        if elevation is not None:
            parts.append(f"Elevation {elevation:.0f} meters")

        return ", ".join(parts) + ", Sir."
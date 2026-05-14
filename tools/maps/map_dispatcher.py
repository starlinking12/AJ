"""
J.A.R.V.I.S. Map Dispatcher
Routes map requests to the best available geocoder.
"""

from typing import Dict, Any, List, Optional

from tools.maps.nominatim_geocoder import NominatimGeocoder
from tools.maps.mapbox_geocoder import MapboxGeocoder
from tools.maps.reverse_geocoder import ReverseGeocoder
from tools.maps.route_planner import RoutePlanner
from tools.maps.place_search import PlaceSearch
from tools.maps.map_cache import MapCache

from jarvis_core.logger import Logger


class MapDispatcher:
    def __init__(self):
        self.log = Logger("MapDispatcher")
        self.cache = MapCache()
        self._geocoders = []
        self._reverse_geocoder = ReverseGeocoder()
        self._route_planner = RoutePlanner()
        self._place_search = PlaceSearch()
        self._initialized = False

    def initialize(self) -> bool:
        self._geocoders = [
            NominatimGeocoder(),
            MapboxGeocoder(),
        ]

        for geocoder in self._geocoders:
            try:
                if geocoder.initialize():
                    self.log.info(f"Geocoder ready: {geocoder.__class__.__name__}")
            except Exception as e:
                self.log.warn(f"Geocoder unavailable: {geocoder.__class__.__name__} - {e}")

        self._initialized = True
        self.log.info("Map dispatcher ready.")
        return True

    def geocode(self, address: str) -> Optional[Dict[str, Any]]:
        cached = self.cache.get(address)
        if cached:
            return cached

        for geocoder in self._geocoders:
            try:
                result = geocoder.geocode(address)
                if result:
                    self.cache.set(address, result)
                    return result
            except Exception as e:
                self.log.warn(f"Geocoder {geocoder.__class__.__name__} failed: {e}")
                continue

        return None

    def reverse_geocode(self, lat: float, lng: float) -> Optional[Dict[str, Any]]:
        return self._reverse_geocoder.lookup(lat, lng)

    def get_route(self, origin: str, destination: str) -> Optional[Dict[str, Any]]:
        origin_coords = self.geocode(origin)
        dest_coords = self.geocode(destination)

        if origin_coords and dest_coords:
            return self._route_planner.plan(
                origin_coords["lat"], origin_coords["lng"],
                dest_coords["lat"], dest_coords["lng"]
            )

        return None

    def search_places(self, query: str, near: str = None) -> List[Dict]:
        if near:
            coords = self.geocode(near)
            if coords:
                return self._place_search.search(query, coords["lat"], coords["lng"])
        return self._place_search.search(query)
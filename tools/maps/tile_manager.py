"""
J.A.R.V.I.S. Tile Manager
Manages map tile caching and sources.
"""

from typing import Dict, List

from jarvis_core.logger import Logger


class TileManager:
    def __init__(self):
        self.log = Logger("TileManager")
        self._tile_sources = {}
        self._initialized = False

    def initialize(self) -> bool:
        self._tile_sources = {
            "openstreetmap": {
                "url": "https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png",
                "attribution": "OpenStreetMap contributors",
                "max_zoom": 19,
                "free": True,
            },
            "cartodb": {
                "url": "https://{s}.basemaps.cartocdn.com/dark_all/{z}/{x}/{y}.png",
                "attribution": "CARTO",
                "max_zoom": 19,
                "free": True,
            },
        }
        self._initialized = True
        self.log.info(f"Tile manager ready. {len(self._tile_sources)} sources.")
        return True

    def get_source(self, name: str = "openstreetmap") -> Dict:
        return self._tile_sources.get(name, self._tile_sources["openstreetmap"])

    def list_sources(self) -> List[str]:
        return list(self._tile_sources.keys())

    def add_source(self, name: str, url: str, attribution: str = "", max_zoom: int = 19) -> None:
        self._tile_sources[name] = {
            "url": url,
            "attribution": attribution,
            "max_zoom": max_zoom,
            "free": True,
        }
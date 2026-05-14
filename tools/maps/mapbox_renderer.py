"""
J.A.R.V.I.S. Mapbox Renderer
Generates Mapbox GL JS HTML for styled maps.
"""

import os
from typing import Dict, Any, Optional

from jarvis_core.logger import Logger


class MapboxRenderer:
    def __init__(self):
        self.log = Logger("MapboxRenderer")
        self.api_key = os.environ.get("MAPBOX_API_KEY", "")
        self._initialized = False

    def initialize(self) -> bool:
        if not self.api_key:
            self.log.warn("Mapbox API key not set.")
            return False
        self._initialized = True
        return True

    def render_map(
        self,
        lat: float,
        lng: float,
        zoom: int = 13,
        style: str = "streets-v12",
        title: str = "Map"
    ) -> str:
        if not self._initialized:
            return ""

        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
    <script src="https://api.mapbox.com/mapbox-gl-js/v3.3.0/mapbox-gl.js"></script>
    <link href="https://api.mapbox.com/mapbox-gl-js/v3.3.0/mapbox-gl.css" rel="stylesheet" />
    <style>
        body {{ margin: 0; padding: 0; }}
        #map {{ width: 100vw; height: 100vh; }}
    </style>
</head>
<body>
    <div id="map"></div>
    <script>
        mapboxgl.accessToken = '{self.api_key}';
        var map = new mapboxgl.Map({{
            container: 'map',
            style: 'mapbox://styles/mapbox/{style}',
            center: [{lng}, {lat}],
            zoom: {zoom}
        }});
        new mapboxgl.Marker()
            .setLngLat([{lng}, {lat}])
            .setPopup(new mapboxgl.Popup().setText('{title}'))
            .addTo(map);
    </script>
</body>
</html>"""

        return html
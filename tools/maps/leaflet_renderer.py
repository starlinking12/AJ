"""
J.A.R.V.I.S. Leaflet Renderer
Generates Leaflet.js HTML for interactive maps.
"""

from typing import Dict, Any, Optional

from jarvis_core.logger import Logger


class LeafletRenderer:
    def __init__(self):
        self.log = Logger("LeafletRenderer")
        self._initialized = False

    def initialize(self) -> bool:
        self._initialized = True
        self.log.info("Leaflet renderer ready.")
        return True

    def render_map(
        self,
        lat: float,
        lng: float,
        zoom: int = 13,
        markers: list = None,
        title: str = "Map"
    ) -> str:
        if markers is None:
            markers = [{"lat": lat, "lng": lng, "title": title}]

        marker_js = ""
        for m in markers:
            marker_js += f"""
            L.marker([{m['lat']}, {m['lng']}])
                .addTo(map)
                .bindPopup("{m.get('title', 'Location')}");"""

        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <style>
        body {{ margin: 0; padding: 0; }}
        #map {{ width: 100vw; height: 100vh; }}
    </style>
</head>
<body>
    <div id="map"></div>
    <script>
        var map = L.map('map').setView([{lat}, {lng}], {zoom});
        L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
            attribution: '&copy; OpenStreetMap contributors',
            maxZoom: 19
        }}).addTo(map);
        {marker_js}
    </script>
</body>
</html>"""

        return html

    def render_route(
        self,
        route_data: Dict[str, Any],
        title: str = "Route"
    ) -> str:
        origin = route_data.get("origin", {"lat": 0, "lng": 0})
        destination = route_data.get("destination", {"lat": 0, "lng": 0})

        mid_lat = (origin["lat"] + destination["lat"]) / 2
        mid_lng = (origin["lng"] + destination["lng"]) / 2

        geometry = route_data.get("geometry", {})
        coordinates = geometry.get("coordinates", [])

        route_coords = ",\n                ".join(
            [f"[{c[1]}, {c[0]}]" for c in coordinates]
        )

        html = f"""<!DOCTYPE html>
<html>
<head>
    <title>{title}</title>
    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>
    <style>
        body {{ margin: 0; padding: 0; }}
        #map {{ width: 100vw; height: 100vh; }}
    </style>
</head>
<body>
    <div id="map"></div>
    <script>
        var map = L.map('map').setView([{mid_lat}, {mid_lng}], 12);
        L.tileLayer('https://{{s}}.tile.openstreetmap.org/{{z}}/{{x}}/{{y}}.png', {{
            attribution: '&copy; OpenStreetMap contributors',
            maxZoom: 19
        }}).addTo(map);

        var routeLine = L.polyline([
            {route_coords}
        ], {{ color: '#00d4ff', weight: 5 }}).addTo(map);

        L.marker([{origin["lat"]}, {origin["lng"]}])
            .addTo(map)
            .bindPopup('Origin');
        L.marker([{destination["lat"]}, {destination["lng"]}])
            .addTo(map)
            .bindPopup('Destination');

        map.fitBounds(routeLine.getBounds());
    </script>
</body>
</html>"""

        return html
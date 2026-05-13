"""
J.A.R.V.I.S. Jina Reader
Uses Jina AI Reader for clean content extraction from URLs.
Free tier available.
"""

import requests
from typing import Optional

from jarvis_core.logger import Logger


class JinaReader:
    def __init__(self):
        self.log = Logger("JinaReader")
        self.base_url = "https://r.jina.ai"

    def read(self, url: str) -> str:
        try:
            full_url = f"{self.base_url}/{url}"
            response = requests.get(full_url, timeout=20)

            if response.status_code == 200:
                return response.text[:5000]
            return ""

        except Exception as e:
            self.log.error(f"Jina Reader failed for {url}: {e}")
            return ""
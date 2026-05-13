"""
J.A.R.V.I.S. Web Scraper
Scrapes full page content from URLs.
"""

from typing import Optional

import requests

from jarvis_core.logger import Logger


class Scraper:
    def __init__(self, timeout: int = 15):
        self.log = Logger("Scraper")
        self.timeout = timeout

    def scrape(self, url: str) -> str:
        try:
            headers = {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
            }

            response = requests.get(url, headers=headers, timeout=self.timeout)
            response.raise_for_status()

            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.text, "html.parser")

            for element in soup(["script", "style", "nav", "footer", "header", "aside"]):
                element.decompose()

            text = soup.get_text(separator=" ", strip=True)
            lines = [line.strip() for line in text.splitlines() if line.strip()]
            return " ".join(lines)

        except ImportError:
            self.log.warn("beautifulsoup4 not installed.")
            return self._simple_scrape(url)
        except Exception as e:
            self.log.error(f"Scraping failed for {url}: {e}")
            return ""

    def _simple_scrape(self, url: str) -> str:
        try:
            response = requests.get(url, timeout=self.timeout)
            return response.text[:5000]
        except Exception:
            return ""
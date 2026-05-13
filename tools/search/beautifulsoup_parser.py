"""
J.A.R.V.I.S. BeautifulSoup Parser
HTML parsing and content extraction using BeautifulSoup.
"""

from typing import Optional, Dict, Any

from jarvis_core.logger import Logger


class BeautifulSoupParser:
    def __init__(self):
        self.log = Logger("BSParser")

    def parse(self, html: str) -> Dict[str, Any]:
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html, "html.parser")

            title = ""
            title_tag = soup.find("title")
            if title_tag:
                title = title_tag.get_text(strip=True)

            for tag in soup(["script", "style", "nav", "footer", "header"]):
                tag.decompose()

            text = soup.get_text(separator=" ", strip=True)

            links = []
            for a in soup.find_all("a", href=True):
                links.append({"text": a.get_text(strip=True), "href": a["href"]})

            return {
                "title": title,
                "text": text[:5000],
                "links": links[:20],
            }

        except ImportError:
            self.log.warn("beautifulsoup4 not installed.")
            return {"title": "", "text": html[:5000], "links": []}
        except Exception as e:
            self.log.error(f"Parsing failed: {e}")
            return {"title": "", "text": "", "links": []}
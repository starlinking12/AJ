"""
J.A.R.V.I.S. Readability Extractor
Extracts main content from web pages using readability algorithms.
"""

from typing import Optional

from jarvis_core.logger import Logger


class ReadabilityExtractor:
    def __init__(self):
        self.log = Logger("ReadabilityExtractor")

    def extract(self, html: str, url: str = "") -> dict:
        try:
            from bs4 import BeautifulSoup

            soup = BeautifulSoup(html, "html.parser")

            article = soup.find("article")
            if article:
                return {
                    "title": self._get_title(soup),
                    "content": article.get_text(separator=" ", strip=True)[:3000],
                    "url": url,
                }

            main = soup.find("main")
            if main:
                return {
                    "title": self._get_title(soup),
                    "content": main.get_text(separator=" ", strip=True)[:3000],
                    "url": url,
                }

            for tag in soup(["script", "style", "nav", "footer", "header", "aside"]):
                tag.decompose()

            body = soup.find("body")
            if body:
                text = body.get_text(separator=" ", strip=True)
                return {
                    "title": self._get_title(soup),
                    "content": text[:3000],
                    "url": url,
                }

            return {"title": "", "content": "", "url": url}

        except ImportError:
            return {"title": "", "content": html[:3000], "url": url}
        except Exception as e:
            self.log.error(f"Readability extraction failed: {e}")
            return {"title": "", "content": "", "url": url}

    def _get_title(self, soup) -> str:
        title_tag = soup.find("title")
        if title_tag:
            return title_tag.get_text(strip=True)
        h1 = soup.find("h1")
        if h1:
            return h1.get_text(strip=True)
        return ""
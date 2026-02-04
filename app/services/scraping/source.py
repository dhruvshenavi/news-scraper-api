from newspaper import Article, Config
from app.core.config import settings



import json
import re
import requests
from bs4 import BeautifulSoup
from urllib.parse import urlparse


def extract_news_source(url, timeout=10, headers=None):
    """
    Extracts the news source / publisher from a news article URL.

    Args:
        url (str): Article URL
        timeout (int): Request timeout in seconds
        headers (dict): Optional HTTP headers

    Returns:
        str: News source name (best guess)
    """

    default_headers = {
    "User-Agent": settings.USER_AGENT
}

    if headers:
        default_headers.update(headers)

    response = requests.get(url, headers=default_headers, timeout=timeout)
    response.raise_for_status()

    soup = BeautifulSoup(response.text, "html.parser")

    # Common meta tag patterns used by news sites
    meta_candidates = [
        {"property": "og:site_name"},
        {"name": "application-name"},
        {"name": "publisher"},
        {"name": "twitter:site"},
        {"itemprop": "publisher"},
    ]

    for attrs in meta_candidates:
        tag = soup.find("meta", attrs=attrs)
        if tag and tag.get("content"):
            return tag["content"].strip()

    # Schema.org JSON-LD fallback
    for script in soup.find_all("script", type="application/ld+json"):
        try:
            import json
            data = json.loads(script.string)

            if isinstance(data, dict):
                publisher = data.get("publisher")
                if isinstance(publisher, dict):
                    name = publisher.get("name")
                    if name:
                        return name.strip()
        except Exception:
            pass

    # Final fallback: derive from domain
    domain = urlparse(url).netloc
    return domain.replace("www.", "").split(".")[0].capitalize()
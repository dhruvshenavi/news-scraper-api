from newspaper import Article, Config
from app.core.config import settings
from app.services.scraping.cleaner import clean_text

def scrape_article(url: str) -> dict:
    try:
        config = Config()
        config.browser_user_agent = settings.USER_AGENT
        config.request_timeout = settings.REQUEST_TIMEOUT
        config.fetch_images = settings.FETCH_IMAGES

        article = Article(
            url,
            language=settings.DEFAULT_LANGUAGE,
            config=config
        )

        article.download()
        article.parse()

        title = clean_text(article.title)[:300]
        content = clean_text(article.text)

        if not content or len(content) < settings.MIN_CONTENT_CHARS:
            return {
                "title": title or None,
                "content": None,
                "url": url,
                "error": "content_too_short_or_empty"
            }

        content = content[:settings.MAX_CONTENT_CHARS]

        return {
            "title": title,
            "content": content,
            "url": url,
            "error": None
        }

    except Exception as e:
        return {
            "title": None,
            "content": None,
            "url": url,
            "error": "download_or_parse_failed"
        }

from newspaper import Article, Config
from app.core.config import settings
from app.services.scraping.cleaner import clean_text
from app.services.scraping.source import extract_news_source
from app.schemas.scrape import ScrapeResponse


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
        source = extract_news_source(url)
        # source="hello"

        if not content or len(content) < settings.MIN_CONTENT_CHARS:
            return ScrapeResponse(
                title=title or None,
                content=None,
                source=source or None,
                url=url,
                error_code=400,
                error_message="content_too_short_or_empty",
            )

        content = content[:settings.MAX_CONTENT_CHARS]

        return ScrapeResponse(
            title=title,
            content=content,
            source=source,
            url=url,
            error_code=None,
            error_message="",
        )

    except Exception as e:
        return ScrapeResponse(
            title=None,
            content=None,
            source=None,
            url=url,
            error_code=500,
            error_message="download_or_parse_failed: " + str(e),
        )

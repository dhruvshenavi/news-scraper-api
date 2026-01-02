from pydantic_settings import BaseSettings, SettingsConfigDict

class Settings(BaseSettings):
    # scraping behavior
    MAX_CONTENT_CHARS: int = 50000
    MIN_CONTENT_CHARS: int = 200
    DEFAULT_LANGUAGE: str | None = None   # None → auto-detect

    # network
    REQUEST_TIMEOUT: int = 12
    FETCH_IMAGES: bool = False
    USER_AGENT: str = (
        "Mozilla/5.0 (Windows NT 10.0; Win64; x64) "
        "AppleWebKit/537.36 (KHTML, like Gecko) "
        "Chrome/120.0.0.0 Safari/537.36"
    )

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore",
    )

settings = Settings()

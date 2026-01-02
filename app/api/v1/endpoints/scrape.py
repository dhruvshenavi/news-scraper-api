from fastapi import APIRouter
from starlette.concurrency import run_in_threadpool
from app.schemas.scrape import ScrapeRequest
from app.services.scraping.newspaper import scrape_article

router = APIRouter()

@router.post("/scrape")
async def scrape(data: ScrapeRequest):
    return await run_in_threadpool(scrape_article, str(data.url))

from fastapi import APIRouter
from app.api.v1.endpoints import health, scrape

api_router = APIRouter(prefix="/api/v1")
api_router.include_router(health.router, tags=["health"])
api_router.include_router(scrape.router, tags=["scrape"])

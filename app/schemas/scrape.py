from pydantic import BaseModel, HttpUrl

class ScrapeRequest(BaseModel):
    url: HttpUrl

class ScrapeResponse(BaseModel):

    title: str | None = None
    content: str | None = None
    url: str
    error_code: int | None = None
    error_message: str 


    

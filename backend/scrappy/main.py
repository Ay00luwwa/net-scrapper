from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from scraper import scrape_url

app = FastAPI()

class ScrapeRequest(BaseModel):
    url: str

@app.post("/scrape")
async def scrape(request: ScrapeRequest):
    try:
        print(f"Scraping URL: {request.url}")
        result = scrape_url(request.url)
        return {"status": "success", "data": result}
    except Exception as e:
        print(f"Error: {e}")
        raise HTTPException(status_code=500, detail=str(e))

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import sys
import os

# Add src to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scrapers import scrape_seek, scrape_others
from utils import parse_salary, filter_jobs

app = FastAPI()

# Allow CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # In production, specify the frontend domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class SearchRequest(BaseModel):
    role: str
    country: str = "AU"
    location: str = "Australia"
    salary: str
    limit: int = 10

class Job(BaseModel):
    id: str
    site: str
    title: str
    company: str
    location: str
    date_posted: Optional[str] = None
    job_url: str
    salary_range: Optional[str] = None
    company_url: Optional[str] = None

@app.post("/api/search", response_model=List[Job])
async def search_jobs(request: SearchRequest):
    try:
        min_sal, max_sal = parse_salary(request.salary)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    all_jobs = []

    # 1. Scrape Seek
    if request.country.upper() == 'AU':
        try:
            seek_jobs = scrape_seek(request.role, min_sal, max_sal, limit=request.limit)
            all_jobs.extend(seek_jobs)
        except Exception as e:
            print(f"Error scraping Seek: {e}")

    # 2. Scrape Others
    try:
        others_jobs = scrape_others(request.role, request.location, request.country, limit=request.limit)
        all_jobs.extend(others_jobs)
    except Exception as e:
        print(f"Error scraping other sites: {e}")

    # 3. Filter
    filtered_jobs = filter_jobs(all_jobs, request.role)
    
    return filtered_jobs

@app.get("/health")
def health_check():
    return {"status": "ok"}

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel, field_validator, field_serializer
from typing import List, Optional, Union, Any
from datetime import date
import math
import sys
import os

# Add src to path
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scrapers import scrape_seek, scrape_others
from utils import parse_salary, filter_jobs

app = FastAPI()


def is_nan(value: Any) -> bool:
    """Check if value is nan."""
    if value is None:
        return True
    if isinstance(value, float):
        try:
            return math.isnan(value)
        except (TypeError, ValueError):
            return False
    if isinstance(value, str) and value.lower() == 'nan':
        return True
    return False


def clean_value(value: Any) -> Optional[str]:
    """Convert nan/None values to None, otherwise return string."""
    if is_nan(value):
        return None
    return str(value)


def clean_date(value: Any) -> Optional[Union[str, date]]:
    """Clean date value, converting nan to None."""
    if is_nan(value):
        return None
    if isinstance(value, date):
        return value
    return str(value) if value else None

# Allow CORS for local development
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000", "http://127.0.0.1:3000"],
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
    location: Optional[str] = None
    date_posted: Optional[Union[str, date]] = None
    job_url: str
    salary_range: Optional[str] = None
    company_url: Optional[str] = None

    @field_validator('location', 'company', 'title', 'salary_range', 'company_url', mode='before')
    @classmethod
    def clean_nan_values(cls, v):
        return clean_value(v)

    @field_validator('date_posted', mode='before')
    @classmethod
    def clean_date_posted(cls, v):
        return clean_date(v)

    @field_serializer('date_posted')
    def serialize_date(self, value):
        if value is None:
            return None
        if isinstance(value, date):
            return value.isoformat()
        return str(value)

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

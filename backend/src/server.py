"""FastAPI server for Career Hunter API."""

from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .config import API_DESCRIPTION, API_TITLE, API_VERSION, CORS_ORIGINS
from .models import HealthResponse, Job, SearchRequest
from .scrapers import scrape_others, scrape_seek
from .utils import filter_by_work_type, filter_jobs, parse_salary

app = FastAPI(
    title=API_TITLE,
    description=API_DESCRIPTION,
    version=API_VERSION,
    contact={"name": "Career Hunter"},
    license_info={"name": "MIT"},
)

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


@app.post(
    "/api/search",
    response_model=List[Job],
    summary="Search for jobs",
    description="""
Search for jobs across multiple job boards.

**Workflow:**
1. Scrapes Seek (Australia only) and other job boards (LinkedIn, Indeed, Glassdoor)
2. Filters results by role relevance using smart keyword matching with synonyms
3. Filters by work type if specified
4. Returns unified job listings

**Salary Format Examples:**
- `140k-200k` (shorthand with 'k')
- `140000-200000` (full numbers)

**Work Type Options:**
- `all`: Show all jobs (default)
- `remote`: Only remote/work-from-home jobs
- `hybrid`: Only hybrid jobs
- `onsite`: Only on-site jobs
    """,
    tags=["Jobs"],
)
async def search_jobs(request: SearchRequest) -> List[Job]:
    """Search for jobs across multiple job boards."""
    try:
        min_sal, max_sal = parse_salary(request.salary)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))

    all_jobs = []

    # Scrape Seek (Australia only)
    if request.country.upper() == "AU":
        try:
            seek_jobs = scrape_seek(request.role, min_sal, max_sal, limit=request.limit)
            all_jobs.extend(seek_jobs)
        except Exception as e:
            print(f"Error scraping Seek: {e}")

    # Scrape other sites (LinkedIn, Indeed, Glassdoor)
    try:
        others_jobs = scrape_others(
            request.role, request.location, request.country, limit=request.limit
        )
        all_jobs.extend(others_jobs)
    except Exception as e:
        print(f"Error scraping other sites: {e}")

    # Apply filters
    filtered_jobs = filter_jobs(all_jobs, request.role)
    filtered_jobs = filter_by_work_type(filtered_jobs, request.work_type)

    return filtered_jobs


@app.get(
    "/health",
    response_model=HealthResponse,
    summary="Health check",
    description="Check if the API service is running and healthy.",
    tags=["System"],
)
def health_check() -> HealthResponse:
    """Return the health status of the API."""
    return HealthResponse(status="ok")

"""FastAPI server for Career Hunter API."""

import asyncio
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

    # Helper for safe Seek scraping
    async def safe_scrape_seek():
        if request.country.upper() == "AU":
            try:
                return await scrape_seek(request.role, min_sal, max_sal, limit=request.limit)
            except Exception as e:
                print(f"Error scraping Seek: {e}")
                return []
        return []

    # Helper for safe Others scraping
    def safe_scrape_others():
        try:
            return scrape_others(
                request.role, request.location, request.country, limit=request.limit
            )
        except Exception as e:
            print(f"Error scraping other sites: {e}")
            return []

    # Execute scrapers in parallel
    loop = asyncio.get_running_loop()

    seek_task = safe_scrape_seek()
    others_task = loop.run_in_executor(None, safe_scrape_others)

    results = await asyncio.gather(seek_task, others_task)

    # Combine results
    all_jobs = []
    for res in results:
        all_jobs.extend(res)

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

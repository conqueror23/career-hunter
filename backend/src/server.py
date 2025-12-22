"""FastAPI server for Career Hunter API."""

import asyncio
import hashlib
import logging
import time
from collections import OrderedDict
from typing import List

from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware

from .config import API_DESCRIPTION, API_TITLE, API_VERSION, CORS_ORIGINS
from .models import HealthResponse, Job, SearchRequest
from .scrapers import scrape_others, scrape_seek
from .utils import filter_by_work_type, filter_jobs, parse_salary

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)


class LRUCache:
    """LRU cache with TTL support and bounded size."""

    def __init__(self, maxsize: int = 100, ttl: int = 3600):
        self._cache: OrderedDict = OrderedDict()
        self._maxsize = maxsize
        self._ttl = ttl

    def _make_key(self, request: SearchRequest) -> str:
        """Generate normalized cache key from request."""
        key_data = (
            f"{request.role.lower().strip()}"
            f"-{request.country.upper()}"
            f"-{request.location.lower().strip()}"
            f"-{request.salary.lower().strip()}"
            f"-{request.work_type.lower()}"
            f"-{request.limit}"
        )
        return hashlib.md5(key_data.encode()).hexdigest()

    def get(self, request: SearchRequest) -> List | None:
        """Get cached result if valid."""
        key = self._make_key(request)
        if key not in self._cache:
            return None

        entry = self._cache[key]
        if time.time() - entry["timestamp"] >= self._ttl:
            del self._cache[key]
            return None

        # Move to end (most recently used)
        self._cache.move_to_end(key)
        return entry["data"]

    def set(self, request: SearchRequest, data: List) -> None:
        """Cache result with timestamp."""
        key = self._make_key(request)

        # Remove oldest if at capacity
        while len(self._cache) >= self._maxsize:
            self._cache.popitem(last=False)

        self._cache[key] = {"timestamp": time.time(), "data": data}

    def clear(self) -> int:
        """Clear all cached entries. Returns number of entries cleared."""
        count = len(self._cache)
        self._cache.clear()
        return count


# Bounded LRU cache with TTL (15 minutes)
search_cache = LRUCache(maxsize=100, ttl=900)

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
    # Check cache
    cached_result = search_cache.get(request)
    if cached_result is not None:
        logger.info("Cache hit for search: role=%s, location=%s", request.role, request.location)
        return cached_result

    logger.info(
        "Cache miss. Starting scrape: role=%s, country=%s, location=%s",
        request.role,
        request.country,
        request.location,
    )

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
                logger.error("Error scraping Seek: %s", e)
                return []
        return []

    # Helper for safe Others scraping
    def safe_scrape_others():
        try:
            return scrape_others(
                request.role, request.location, request.country, limit=request.limit
            )
        except Exception as e:
            logger.error("Error scraping other sites: %s", e)
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

    # Save to cache
    search_cache.set(request, filtered_jobs)

    logger.info("Search complete: found %d jobs", len(filtered_jobs))
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


@app.post(
    "/api/clear-cache",
    summary="Clear search cache",
    description="Clear all cached search results to force fresh data on next search.",
    tags=["System"],
)
def clear_cache() -> dict:
    """Clear the search cache and return the number of entries cleared."""
    count = search_cache.clear()
    logger.info("Cache cleared: %d entries removed", count)
    return {"cleared": count, "message": f"Cleared {count} cached entries"}

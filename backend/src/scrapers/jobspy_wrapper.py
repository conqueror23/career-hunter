"""JobSpy wrapper for scraping LinkedIn, Indeed, and Glassdoor."""

import logging
import os
from typing import Any, Dict, List, Optional

import pandas as pd
from jobspy import scrape_jobs

try:
    from .config import COUNTRY_MAP
except ImportError:
    from config import COUNTRY_MAP

logger = logging.getLogger(__name__)

# Proxy configuration from environment variable
# Format: comma-separated list of proxies, e.g., "user:pass@host:port,host2:port2"
PROXY_LIST: Optional[List[str]] = None
_proxy_env = os.environ.get("JOBSPY_PROXIES", "")
if _proxy_env:
    PROXY_LIST = [p.strip() for p in _proxy_env.split(",") if p.strip()]


def _get_country_name(country_code: str) -> str:
    """Convert country code to country name for JobSpy."""
    return COUNTRY_MAP.get(country_code.upper(), country_code.lower())


def _safe_get(row: pd.Series, key: str, default: Any = None) -> Any:
    """Safely get a value from a pandas Series, handling NaN."""
    value = row.get(key, default)
    if pd.isna(value):
        return default
    return value


def _format_job(row: pd.Series) -> Dict[str, Any]:
    """Format a job row from JobSpy into a standardized dictionary."""
    # Get company URL (prefer direct, then platform specific)
    company_url = _safe_get(row, "company_url_direct")
    if not company_url:
        company_url = _safe_get(row, "company_url", "N/A")

    return {
        "id": _safe_get(row, "id", "N/A"),
        "site": _safe_get(row, "site", "N/A"),
        "title": _safe_get(row, "title", "N/A"),
        "company": _safe_get(row, "company", "N/A"),
        "location": _safe_get(row, "location", "N/A"),
        "date_posted": _safe_get(row, "date_posted", "N/A"),
        "job_url": _safe_get(row, "job_url", "N/A"),
        "salary_range": _safe_get(row, "salary_range", "N/A"),
        "company_url": company_url,
        "description": _safe_get(row, "description", ""),
        "is_remote": _safe_get(row, "is_remote", False),
        "work_from_home_type": _safe_get(row, "work_from_home_type", ""),
    }


def scrape_others(
    role: str,
    location: str,
    country_code: str = "AU",
    limit: int = 25,
    hours_old: Optional[int] = None,
) -> List[Dict[str, Any]]:
    """
    Scrape jobs from LinkedIn, Indeed, and Glassdoor using JobSpy.

    Args:
        role: Job role/title to search for
        location: Location to search in
        country_code: Country code (AU, US, UK, etc.)
        limit: Maximum number of results per site (default 25)
        hours_old: Only return jobs posted within this many hours (optional)

    Returns:
        List of job dictionaries
    """
    logger.info(
        "Searching LinkedIn, Indeed, Glassdoor for '%s' in '%s' (limit=%d, hours_old=%s)",
        role,
        country_code,
        limit,
        hours_old,
    )

    country_name = _get_country_name(country_code)

    try:
        # Build scrape parameters
        scrape_params = {
            "site_name": ["indeed", "linkedin", "glassdoor"],
            "search_term": role,
            "location": location,
            "results_wanted": limit,
            "country_indeed": country_name,
            "linkedin_fetch_description": True,
            "description_format": "markdown",
        }

        # Add optional parameters
        if hours_old is not None:
            scrape_params["hours_old"] = hours_old

        if PROXY_LIST:
            scrape_params["proxies"] = PROXY_LIST
            logger.info("Using %d proxies for scraping", len(PROXY_LIST))

        jobs_df: pd.DataFrame = scrape_jobs(**scrape_params)

        if jobs_df.empty:
            return []

        logger.info("Scraped %d jobs from job boards", len(jobs_df))
        return [_format_job(row) for _, row in jobs_df.iterrows()]

    except Exception as e:
        logger.error("Error scraping other sites: %s", e)
        return []

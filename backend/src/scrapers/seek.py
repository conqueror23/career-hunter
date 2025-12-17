"""Seek.com.au job scraper."""

import re
from typing import Any, Dict, List

import requests
from bs4 import BeautifulSoup

from ..config import SEEK_BASE_URL, SEEK_USER_AGENT


def _extract_job_id(job_url: str) -> str:
    """Extract job ID from Seek URL."""
    match = re.search(r"/job/(\d+)", job_url)
    return f"seek_{match.group(1)}" if match else "seek_unknown"


def _extract_work_type(location: str) -> tuple:
    """Extract work type information from location string."""
    location_lower = location.lower() if location else ""
    is_remote = "remote" in location_lower or "work from home" in location_lower

    work_from_home_type = ""
    if "remote" in location_lower:
        work_from_home_type = "remote"
    elif "hybrid" in location_lower:
        work_from_home_type = "hybrid"

    return is_remote, work_from_home_type


def _parse_job_article(article: Any, salary_min: int, salary_max: int) -> Dict[str, Any] | None:
    """Parse a single job article element from Seek."""
    try:
        title_elem = article.find(attrs={"data-automation": "jobTitle"})
        company_elem = article.find(attrs={"data-automation": "jobCompany"})
        location_elem = article.find(attrs={"data-automation": "jobLocation"})

        # Get link element
        link_elem = None
        if title_elem:
            link_elem = title_elem if title_elem.name == "a" else title_elem.find("a")

        title = title_elem.text.strip() if title_elem else "N/A"
        company = company_elem.text.strip() if company_elem else "N/A"
        location = location_elem.text.strip() if location_elem else "N/A"
        job_url = f"https://www.seek.com.au{link_elem['href']}" if link_elem else "N/A"

        # Extract company URL
        company_link_elem = company_elem.find("a") if company_elem else None
        company_url = (
            f"https://www.seek.com.au{company_link_elem['href']}" if company_link_elem else "N/A"
        )

        # Extract description teaser
        teaser_elem = article.find(attrs={"data-automation": "jobShortDescription"})
        description = teaser_elem.text.strip() if teaser_elem else ""

        # Extract work type
        is_remote, work_from_home_type = _extract_work_type(location)

        return {
            "id": _extract_job_id(job_url),
            "site": "Seek",
            "title": title,
            "company": company,
            "location": location,
            "date_posted": "Recent",
            "job_url": job_url,
            "salary_range": f"{salary_min}-{salary_max}",
            "company_url": company_url,
            "description": description,
            "is_remote": is_remote,
            "work_from_home_type": work_from_home_type,
        }
    except Exception:
        return None


def scrape_seek(
    role: str, salary_min: int, salary_max: int, limit: int = 10
) -> List[Dict[str, Any]]:
    """
    Scrape job listings from Seek.com.au.

    Args:
        role: Job role/title to search for
        salary_min: Minimum salary
        salary_max: Maximum salary
        limit: Maximum number of results

    Returns:
        List of job dictionaries
    """
    print(f"Searching Seek.com.au for '{role}' with salary {salary_min}-{salary_max}...")

    params = {
        "keywords": role,
        "salaryrange": f"{salary_min}-{salary_max}",
        "salarytype": "annual",
        "sortmode": "ListedDate",
    }

    headers = {
        "User-Agent": SEEK_USER_AGENT,
        "Accept": (
            "text/html,application/xhtml+xml,application/xml;q=0.9,"
            "image/avif,image/webp,*/*;q=0.8"
        ),
    }

    jobs: List[Dict[str, Any]] = []

    try:
        response = requests.get(SEEK_BASE_URL, params=params, headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch Seek: Status {response.status_code}")
            return []

        soup = BeautifulSoup(response.text, "html.parser")

        # Find job articles
        articles = soup.find_all("article")
        if not articles:
            articles = soup.find_all(attrs={"data-automation": "job-card"})

        for article in articles[:limit]:
            job = _parse_job_article(article, salary_min, salary_max)
            if job:
                jobs.append(job)

    except Exception as e:
        print(f"Error scraping Seek: {e}")

    return jobs

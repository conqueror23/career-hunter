"""Application configuration and constants."""

from typing import Dict, Set

# CORS settings
CORS_ORIGINS = [
    "http://localhost:3000",
    "http://127.0.0.1:3000",
]

# API settings
API_TITLE = "Career Hunter API"
API_VERSION = "1.0.0"
API_DESCRIPTION = """
## Career Hunter - Job Search API

A powerful job aggregation API that scrapes multiple job boards and returns unified results.

### Features
- **Multi-source scraping**: Aggregates jobs from Seek, LinkedIn, Indeed, and Glassdoor
- **Smart filtering**: Filters jobs by role relevance using synonym matching
- **Work type filtering**: Filter by remote, hybrid, or on-site positions
- **Salary range**: Search within specific salary ranges

### Supported Job Boards
- Seek (Australia only)
- LinkedIn (Global)
- Indeed (Global)
- Glassdoor (Global)
"""

# Country mappings for job search
COUNTRY_MAP: Dict[str, str] = {
    "AU": "australia",
    "US": "usa",
    "UK": "united kingdom",
    "GB": "united kingdom",
    "NZ": "new zealand",
    "CA": "canada",
    "IN": "india",
    "SG": "singapore",
}

# Job filtering synonyms
JOB_SYNONYMS: Dict[str, Set[str]] = {
    "engineer": {"developer", "programmer", "coder", "architect", "engineering"},
    "developer": {"engineer", "programmer", "coder", "architect", "development"},
    "software": {"sw", "application", "app"},
    "manager": {"lead", "director", "head", "management"},
    "admin": {"administrator", "coordinator"},
    "administrator": {"admin", "coordinator"},
    "designer": {"artist", "creative", "design"},
    "data": {"analytics", "bi"},
    "devops": {"sre", "platform", "infrastructure"},
    "frontend": {"front-end", "ui", "react", "angular", "vue"},
    "backend": {"back-end", "api", "server"},
    "fullstack": {"full-stack", "full"},
}

# Stop words to ignore in job title matching
STOP_WORDS: Set[str] = {
    "senior",
    "junior",
    "mid",
    "level",
    "the",
    "a",
    "an",
    "and",
    "or",
    "of",
    "for",
    "in",
    "at",
}

# Work type keywords
WORK_TYPE_KEYWORDS = {
    "remote": ["remote", "work from home", "wfh"],
    "hybrid": ["hybrid"],
}

# Scraper settings
SEEK_BASE_URL = "https://www.seek.com.au/jobs"
SEEK_USER_AGENT = (
    "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) "
    "AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36"
)

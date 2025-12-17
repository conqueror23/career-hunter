# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Project Structure

```
career-hunter/
├── backend/                 # Python/FastAPI backend
│   ├── src/                 # Source code
│   │   ├── server.py        # FastAPI server
│   │   ├── main.py          # CLI entry point
│   │   ├── utils.py         # Job filtering logic
│   │   └── scrapers/        # Web scraping modules
│   ├── tests/               # Unit tests
│   └── requirements.txt     # Python dependencies
├── frontend/                # React/TypeScript frontend
│   ├── src/                 # React source code
│   ├── public/              # Static assets
│   └── package.json         # Node dependencies
├── Makefile                 # Build automation
└── README.md
```

## Build & Run Commands

All operations use the Makefile:

```bash
make install    # Setup venv + install Python & Node dependencies
make test       # Run Python unit tests
make start      # Start backend (port 8000) and frontend (port 3000)
make stop       # Stop all services
make clean      # Remove venv, node_modules, logs, pycache
```

Run a single test file:
```bash
backend/venv/bin/python -m unittest backend/tests/test_utils.py
```

CLI usage (after `make install`):
```bash
source backend/venv/bin/activate
python backend/src/main.py --role "Senior Software Engineer" --country "AU" --salary "140k-200k"
```

## Architecture

**Backend (Python/FastAPI)**
- `backend/src/server.py` - FastAPI server with single endpoint `POST /api/search`
- `backend/src/main.py` - CLI entry point
- `backend/src/utils.py` - Job filtering logic with title relevance matching and salary parsing
- `backend/src/scrapers/` - Web scraping modules:
  - `seek.py` - BeautifulSoup scraper for Seek.com.au
  - `jobspy_wrapper.py` - Wrapper for python-jobspy (Indeed, LinkedIn, Glassdoor)

**Frontend (React/TypeScript)**
- `frontend/src/App.tsx` - Main component with search form and results table
- Uses Material-UI for components
- Calls backend via axios at http://localhost:8000/api/search

**Data Flow**
1. Frontend sends search params to backend
2. Backend runs scrapers in sequence (Seek, then JobSpy multi-site)
3. Results filtered by `filter_jobs_by_role()` for relevance
4. Normalized Job objects returned with: id, site, title, company, location, date_posted, job_url, salary_range

## Key Implementation Details

- CORS enabled for localhost development
- Salary parsing handles flexible formats (140k, 140000, $140,000)
- Job filtering uses synonym expansion (engineer↔developer, etc.)
- Frontend color-codes results by source site

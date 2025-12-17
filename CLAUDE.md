# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

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
python -m src.main --role "Senior Software Engineer" --country "AU" --salary "140k-200k"
```

## Architecture

### Backend (Python/FastAPI)

```
backend/src/
├── server.py          # FastAPI app with API endpoints
├── config.py          # Configuration constants (CORS, synonyms, etc.)
├── models.py          # Pydantic models (Job, SearchRequest, etc.)
├── utils.py           # Job filtering and salary parsing
├── main.py            # CLI entry point
└── scrapers/
    ├── __init__.py    # Exports scrape_seek, scrape_others
    ├── seek.py        # BeautifulSoup scraper for Seek.com.au
    └── jobspy_wrapper.py  # Wrapper for python-jobspy
```

**Key modules:**
- `config.py` - All constants: CORS origins, country mappings, job synonyms, stop words
- `models.py` - Pydantic models with validators for NaN handling
- `utils.py` - `parse_salary()`, `filter_jobs()`, `filter_by_work_type()`

### Frontend (React/TypeScript)

```
frontend/src/
├── App.tsx            # Main app component
├── types/
│   └── index.ts       # TypeScript interfaces (Job, CompanyInfo, etc.)
├── hooks/
│   └── useJobSearch.ts # Custom hook for search state management
├── components/
│   ├── index.ts       # Component exports
│   ├── SearchForm.tsx # Search form with all filters
│   ├── JobsTable.tsx  # Jobs list with tooltips
│   ├── CompaniesTable.tsx # Companies aggregation view
│   ├── SourceBadge.tsx    # Styled source label
│   └── CompanyLinks.tsx   # Glassdoor/LinkedIn links
└── utils/
    └── index.ts       # Utilities (CSV download, source styling)
```

**Key patterns:**
- Custom hook `useJobSearch` manages all search state and API calls
- Components are small and focused on single responsibility
- Types are centralized in `types/index.ts`

### Data Flow

1. User enters search criteria in `SearchForm`
2. `useJobSearch` hook sends POST to `/api/search`
3. Backend scrapes Seek (AU only) + JobSpy (LinkedIn, Indeed, Glassdoor)
4. Results filtered by `filter_jobs()` for role relevance
5. Results filtered by `filter_by_work_type()` for work arrangement
6. `JobsTable` or `CompaniesTable` displays results based on active tab

## Key Implementation Details

- CORS enabled for localhost:3000
- Salary parsing handles flexible formats (140k, 140000, $140,000)
- Job filtering uses synonym expansion (engineer <-> developer, etc.)
- Frontend color-codes results by source site (Seek: pink, LinkedIn: blue, Indeed: blue)
- Company links auto-generate Glassdoor and LinkedIn URLs
- CSV download includes all job fields including description

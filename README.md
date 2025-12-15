# Career Hunter

A powerful job scraping tool with a CLI and Web UI.

## Features

- **Multi-Platform**: Scrapes Seek (AU/NZ), LinkedIn, Indeed, and Glassdoor.
- **Aggregated Results**: Combines results into a single list.
- **Smart Filtering**: Filters jobs based on relevance to your search role.
- **Modern UI**: React-based web interface to search and view jobs.
- **CLI**: Robust command-line interface for automation.

## Project Structure

```
career-hunter/
├── src/                 # Python Backend & Scrapers
│   ├── server.py        # FastAPI server
│   ├── main.py          # CLI Entry point
│   ├── utils.py         # Utilities
│   └── scrapers/        # Scraper modules
├── ui/                  # React Frontend
├── tests/               # Unit tests
├── bin/                 # Scripts
├── venv/                # Virtual environment
├── requirements.txt     # Dependencies
└── Makefile             # Automation
```

## Quick Start (Makefile)

The project includes a `Makefile` to simplify setup and usage.

1.  **Initialize & Install**: Sets up venv and installs all Python/Node dependencies.
    ```bash
    make install
    ```

2.  **Run Tests**:
    ```bash
    make test
    ```

3.  **Start Application**: Launches Backend (port 8000) and Frontend (port 3000).
    ```bash
    make start
    ```

4.  **Stop Application**: Stops all running services.
    ```bash
    make stop
    ```

## Manual Usage

### CLI
```bash
source venv/bin/activate
python src/main.py --role "Senior Software Engineer" --country "AU" --salary "140k-200k"
```

## Options (CLI)

- `--role` / `-r`: Job role (Required)
- `--country` / `-c`: Country code (e.g., AU, US, UK). Default: AU.
- `--salary` / `-s`: Salary range (e.g., 140k-200k).
- `--location` / `-l`: Specific location string (e.g., "Sydney", "Remote").
- `--limit` / `-n`: Number of results per site. Default: 10.

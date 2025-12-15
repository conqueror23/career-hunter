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
└── requirements.txt     # Dependencies
```

## Installation

1. **Backend Setup**:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   ```

2. **Frontend Setup**:
   ```bash
   cd ui
   npm install
   ```

## Usage

### Web UI (Recommended)

Run the start script to launch both backend and frontend:

```bash
./bin/start.sh
```
- Frontend: [http://localhost:3000](http://localhost:3000)
- Backend API: [http://localhost:8000](http://localhost:8000)

### CLI

Run the tool from the root directory:

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
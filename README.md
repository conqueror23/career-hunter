# Career Hunter

A powerful CLI tool to scrape job listings from Seek, LinkedIn, Indeed, and Glassdoor.

## Features

- **Multi-Platform**: Scrapes Seek (AU/NZ), LinkedIn, Indeed, and Glassdoor.
- **Aggregated Results**: Combines results into a single table and CSV file.
- **Salary Filtering**: (Seek only) Filters by salary range.
- **Country Support**: Optimized for Australia (AU), but supports US, UK, NZ, CA, etc. via JobSpy.

## Project Structure

```
career-hunter/
├── src/
│   ├── main.py          # Entry point
│   ├── utils.py         # Utilities
│   └── scrapers/        # Scraper modules
├── tests/               # Unit tests
├── venv/                # Virtual environment
└── requirements.txt     # Dependencies
```

## Installation

1. Create a virtual environment:
   ```bash
   python3 -m venv venv
   source venv/bin/activate
   ```

2. Install dependencies:
   ```bash
   pip install -r requirements.txt
   ```

## Usage

Run the tool from the `src` directory or root:

```bash
python src/main.py --role "JOB_ROLE" --country "COUNTRY_CODE" --salary "MIN-MAX"
```

### Examples

**Search for Senior Software Engineers in Australia with a salary of 140k-200k:**
```bash
python src/main.py --role "Senior Software Engineer" --country "AU" --salary "140k-200k"
```

## Running Tests

```bash
python -m unittest discover tests
```

## Options

- `--role` / `-r`: Job role (Required)
- `--country` / `-c`: Country code (e.g., AU, US, UK). Default: AU.
- `--salary` / `-s`: Salary range (e.g., 140k-200k).
- `--location` / `-l`: Specific location string (e.g., "Sydney", "Remote").
- `--limit` / `-n`: Number of results per site. Default: 10.

"""Career Hunter CLI - Job search from command line."""

import argparse
import asyncio

import pandas as pd
from tabulate import tabulate

from scrapers import scrape_others, scrape_seek
from utils import filter_jobs, parse_salary


async def run_search(role: str, country: str, location: str, salary: str, limit: int) -> None:
    """
    Run a job search and display results.

    Args:
        role: Job role/title to search for
        country: Country code (AU, US, UK, etc.)
        location: Location string
        salary: Salary range (e.g., '140k-200k')
        limit: Number of results per site
    """
    try:
        min_sal, max_sal = parse_salary(salary)
    except ValueError as e:
        print(f"Error parsing salary: {e}")
        return

    all_jobs = []

    # Scrape Seek (Australia only)
    if country.upper() == "AU":
        seek_jobs = await scrape_seek(role, min_sal, max_sal, limit=limit)
        all_jobs.extend(seek_jobs)
        print(f"Found {len(seek_jobs)} jobs on Seek")

    # Scrape other sites (LinkedIn, Indeed, Glassdoor)
    others_jobs = scrape_others(role, location, country, limit=limit)
    all_jobs.extend(others_jobs)
    print(f"Found {len(others_jobs)} jobs on other sites")

    if not all_jobs:
        print("No jobs found.")
        return

    # Filter jobs by role relevance
    initial_count = len(all_jobs)
    all_jobs = filter_jobs(all_jobs, role)
    filtered_count = initial_count - len(all_jobs)
    if filtered_count > 0:
        print(f"Filtered out {filtered_count} irrelevant jobs.")

    if not all_jobs:
        print("No jobs remaining after filtering.")
        return

    # Display results
    df = pd.DataFrame(all_jobs)
    display_cols = [
        "site",
        "title",
        "company",
        "location",
        "salary_range",
        "job_url",
        "company_url",
    ]

    print("\nSearch Results:")
    print(tabulate(df[display_cols], headers="keys", tablefmt="grid", showindex=False))

    # Save to CSV
    filename = f"jobs_{country}_{role.replace(' ', '_')}.csv"
    df.to_csv(filename, index=False)
    print(f"\nSaved results to {filename}")


def main() -> None:
    """CLI entry point."""
    parser = argparse.ArgumentParser(description="Career Hunter - Job Scraper CLI")
    parser.add_argument(
        "--role", "-r", required=True, help="Job role to search for (e.g. 'Software Engineer')"
    )
    parser.add_argument("--country", "-c", default="AU", help="Country code (default: AU)")
    parser.add_argument(
        "--location", "-l", default="Australia", help="Location string (default: Australia)"
    )
    parser.add_argument("--salary", "-s", required=True, help="Salary range (e.g. 140k-200k)")
    parser.add_argument(
        "--limit", "-n", type=int, default=10, help="Number of results per site (default: 10)"
    )

    args = parser.parse_args()
    asyncio.run(run_search(args.role, args.country, args.location, args.salary, args.limit))


if __name__ == "__main__":
    main()

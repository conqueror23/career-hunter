import argparse
import sys
import os
import pandas as pd
from tabulate import tabulate

# Add current directory to path to allow imports when running directly
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

from scrapers import scrape_seek, scrape_others
from utils import parse_salary

def run_search(role, country, location, salary, limit):
    # Parse salary
    try:
        min_sal, max_sal = parse_salary(salary)
    except ValueError as e:
        print(f"Error parsing salary: {e}")
        return

    all_jobs = []
    
    # 1. Scrape Seek (AU specific)
    if country.upper() == 'AU':
        seek_jobs = scrape_seek(role, min_sal, max_sal, limit=limit)
        all_jobs.extend(seek_jobs)
        print(f"Found {len(seek_jobs)} jobs on Seek")
    
    # 2. Scrape JobSpy (Indeed, LinkedIn, Glassdoor)
    others_jobs = scrape_others(role, location, country, limit=limit)
    all_jobs.extend(others_jobs)
    print(f"Found {len(others_jobs)} jobs on other sites")
    
    if not all_jobs:
        print("No jobs found.")
        return
        
    # 3. Process and Display
    df = pd.DataFrame(all_jobs)
    
    # Select columns to display
    display_cols = ['site', 'title', 'company', 'location', 'salary_range', 'job_url']
    
    # Print to console
    print("\nSearch Results:")
    print(tabulate(df[display_cols], headers='keys', tablefmt='grid', showindex=False))
    
    # Save to CSV
    filename = f"jobs_{country}_{role.replace(' ', '_')}.csv"
    df.to_csv(filename, index=False)
    print(f"\nSaved results to {filename}")

def main():
    parser = argparse.ArgumentParser(description="Career Hunter - Job Scraper CLI")
    parser.add_argument("--role", "-r", required=True, help="Job role to search for (e.g. 'Senior Software Engineer')")
    parser.add_argument("--country", "-c", default="AU", help="Country code (default: AU)")
    parser.add_argument("--location", "-l", default="Australia", help="Location string (default: Australia)")
    parser.add_argument("--salary", "-s", required=True, help="Salary range (e.g. 140k-200k)")
    parser.add_argument("--limit", "-n", type=int, default=10, help="Number of results per site (default: 10)")
    
    args = parser.parse_args()
    
    run_search(args.role, args.country, args.location, args.salary, args.limit)

if __name__ == "__main__":
    main()
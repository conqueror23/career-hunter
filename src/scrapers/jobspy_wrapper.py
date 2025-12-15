from jobspy import scrape_jobs
import pandas as pd

def scrape_others(role, location, country_code="AU", limit=10):
    """
    Scrapes LinkedIn, Indeed, Glassdoor using jobspy
    """
    print(f"Searching LinkedIn, Indeed, Glassdoor for '{role}' in '{country_code}'...")
    
    # Map common country codes to what jobspy/indeed expects
    country_map = {
        'AU': 'australia',
        'US': 'usa',
        'UK': 'united kingdom',
        'GB': 'united kingdom',
        'NZ': 'new zealand',
        'CA': 'canada',
        'IN': 'india',
        'SG': 'singapore'
    }
    
    country_name = country_map.get(country_code.upper(), country_code.lower())
    
    try:
        jobs: pd.DataFrame = scrape_jobs(
            site_name=["indeed", "linkedin", "glassdoor"],
            search_term=role,
            location=location,
            results_wanted=limit,
            country_indeed=country_name,
            # offset=0,
            # link_in_bio=False,
            # easy_apply=False
        )
        
        if jobs.empty:
            return []

        # Standardize output to match Seek scraper
        formatted_jobs = []
        for _, row in jobs.iterrows():
            formatted_jobs.append({
                "id": row.get('id', 'N/A'),
                "site": row.get('site', 'N/A'),
                "title": row.get('title', 'N/A'),
                "company": row.get('company', 'N/A'),
                "location": row.get('location', 'N/A'),
                "date_posted": row.get('date_posted', 'N/A'),
                "job_url": row.get('job_url', 'N/A'),
                "salary_range": row.get('salary_range', 'N/A') # Jobspy often captures this
            })
            
        return formatted_jobs

    except Exception as e:
        print(f"Error scraping other sites: {e}")
        return []

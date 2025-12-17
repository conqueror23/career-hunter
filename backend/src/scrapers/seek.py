import requests
from bs4 import BeautifulSoup
import urllib.parse
import re

def scrape_seek(role, salary_min, salary_max, limit=10):
    """
    Scrapes job listings from Seek.com.au
    """
    print(f"Searching Seek.com.au for '{role}' with salary {salary_min}-{salary_max}...")
    
    # Construct Seek URL
    # Seek uses a specific format. 
    # Example: https://www.seek.com.au/jobs?keywords=software%20engineer&salaryrange=100000-150000&salarytype=annual
    
    base_url = "https://www.seek.com.au/jobs"
    params = {
        "keywords": role,
        "salaryrange": f"{salary_min}-{salary_max}",
        "salarytype": "annual",
        "sortmode": "ListedDate" # Get latest
    }
    
    headers = {
        "User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
        "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8",
    }
    
    jobs = []
    
    try:
        response = requests.get(base_url, params=params, headers=headers)
        if response.status_code != 200:
            print(f"Failed to fetch Seek: Status {response.status_code}")
            return []

        soup = BeautifulSoup(response.text, 'html.parser')
        
        # Seek's class names are dynamic or obfuscated (e.g. _10e8200). 
        # We need to rely on attribute selectors or structure where possible.
        # However, usually articles are wrapped in <article> tags.
        
        articles = soup.find_all('article')
        
        if not articles:
            # Fallback for different DOM structures if <article> isn't used
            # Sometimes Seek uses specific data-automation attributes
            articles = soup.find_all(attrs={"data-automation": "job-card"})

        for article in articles[:limit]:
            try:
                title_elem = article.find(attrs={"data-automation": "jobTitle"})
                company_elem = article.find(attrs={"data-automation": "jobCompany"})
                location_elem = article.find(attrs={"data-automation": "jobLocation"})
                
                link_elem = None
                if title_elem:
                    if title_elem.name == 'a':
                        link_elem = title_elem
                    else:
                        link_elem = title_elem.find('a')
                
                title = title_elem.text.strip() if title_elem else "N/A"
                company = company_elem.text.strip() if company_elem else "N/A"
                location = location_elem.text.strip() if location_elem else "N/A"
                
                job_url = "https://www.seek.com.au" + link_elem['href'] if link_elem else "N/A"
                
                # Extract ID to be safe
                job_id = "seek_" + (re.search(r'/job/(\d+)', job_url).group(1) if re.search(r'/job/(\d+)', job_url) else "unknown")

                # Try to find company link
                company_link_elem = company_elem.find('a') if company_elem else None
                company_url = "https://www.seek.com.au" + company_link_elem['href'] if company_link_elem else "N/A"

                jobs.append({
                    "id": job_id,
                    "site": "Seek",
                    "title": title,
                    "company": company,
                    "location": location,
                    "date_posted": "Recent", # Seek relative dates are hard to parse reliably without more logic
                    "job_url": job_url,
                    "salary_range": f"{salary_min}-{salary_max}", # Echoing search params as exact salary often hidden
                    "company_url": company_url
                })
            except Exception as e:
                continue
                
    except Exception as e:
        print(f"Error scraping Seek: {e}")

    return jobs

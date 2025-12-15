from jobspy import scrape_jobs
import pandas as pd

def inspect_jobspy_columns():
    jobs: pd.DataFrame = scrape_jobs(
        site_name=["indeed", "linkedin", "glassdoor"],
        search_term="Software Engineer",
        location="Sydney, AU",
        results_wanted=3,
        country_indeed="australia"
    )
    
    if not jobs.empty:
        print("Columns available:", jobs.columns.tolist())
        # Print first row to see sample data
        print(jobs.iloc[0].to_dict())
    else:
        print("No jobs found to inspect.")

if __name__ == "__main__":
    inspect_jobspy_columns()

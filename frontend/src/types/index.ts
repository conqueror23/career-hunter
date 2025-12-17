/** Job listing from the API */
export interface Job {
  id: string;
  site: string;
  title: string;
  company: string;
  location: string;
  job_url: string;
  salary_range: string;
  company_url: string;
  description: string;
}

/** Aggregated company information derived from jobs */
export interface CompanyInfo {
  name: string;
  jobCount: number;
  locations: string[];
  sources: string[];
  jobs: Job[];
}

/** Search request parameters */
export interface SearchParams {
  role: string;
  country: string;
  location: string;
  salary: string;
  work_type: string;
  limit: number;
}

/** Work type filter options */
export type WorkType = 'all' | 'remote' | 'hybrid' | 'onsite';

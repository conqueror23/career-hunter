import { useState, useMemo, useCallback } from 'react';
import axios from 'axios';
import { Job, CompanyInfo, SearchParams } from '../types';

const API_URL = 'http://localhost:8000/api/search';

interface UseJobSearchReturn {
  jobs: Job[];
  companies: CompanyInfo[];
  loading: boolean;
  error: string;
  search: (params: SearchParams) => Promise<void>;
}

/** Hook for managing job search state and API calls */
export const useJobSearch = (): UseJobSearchReturn => {
  const [jobs, setJobs] = useState<Job[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const companies = useMemo<CompanyInfo[]>(() => {
    const companyMap = new Map<string, CompanyInfo>();

    jobs.forEach((job) => {
      const companyName = job.company || 'Unknown';
      if (!companyMap.has(companyName)) {
        companyMap.set(companyName, {
          name: companyName,
          jobCount: 0,
          locations: [],
          sources: [],
          jobs: [],
        });
      }

      const info = companyMap.get(companyName)!;
      info.jobCount++;
      info.jobs.push(job);

      if (job.location && !info.locations.includes(job.location)) {
        info.locations.push(job.location);
      }
      if (job.site && !info.sources.includes(job.site)) {
        info.sources.push(job.site);
      }
    });

    return Array.from(companyMap.values()).sort((a, b) => b.jobCount - a.jobCount);
  }, [jobs]);

  const search = useCallback(async (params: SearchParams) => {
    setLoading(true);
    setError('');
    setJobs([]);

    try {
      const response = await axios.post(API_URL, params);
      setJobs(response.data);
    } catch (err: any) {
      setError(err.message || 'An error occurred while fetching jobs');
    } finally {
      setLoading(false);
    }
  }, []);

  return { jobs, companies, loading, error, search };
};

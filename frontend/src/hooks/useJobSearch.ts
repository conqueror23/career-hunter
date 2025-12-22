import { useState, useMemo, useCallback, useRef } from 'react';
import axios from 'axios';
import { Job, CompanyInfo, SearchParams } from '../types';

const API_URL = process.env.REACT_APP_API_URL || 'http://localhost:8000/api/search';

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

  // Ref to store the current AbortController
  const abortControllerRef = useRef<AbortController | null>(null);
  // Counter to track the current request and detect stale responses
  const requestIdRef = useRef(0);

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
    // Cancel previous request if it exists
    if (abortControllerRef.current) {
      abortControllerRef.current.abort();
    }

    // Create new controller and increment request ID
    abortControllerRef.current = new AbortController();
    const currentRequestId = ++requestIdRef.current;

    setLoading(true);
    setError('');
    // Note: We do NOT clear jobs here to avoid UI flashing.
    // Old jobs remain visible until new ones arrive.

    try {
      const response = await axios.post(API_URL, params, {
        signal: abortControllerRef.current.signal,
      });
      // Only update state if this is still the current request
      if (currentRequestId === requestIdRef.current) {
        setJobs(response.data);
        setLoading(false);
      }
    } catch (err: unknown) {
      // Only update error state if this is still the current request
      if (currentRequestId === requestIdRef.current) {
        if (!axios.isCancel(err)) {
          const errorMessage =
            err instanceof Error ? err.message : 'An error occurred while fetching jobs';
          setError(errorMessage);
        }
        setLoading(false);
      }
    }
  }, []);

  return { jobs, companies, loading, error, search };
};

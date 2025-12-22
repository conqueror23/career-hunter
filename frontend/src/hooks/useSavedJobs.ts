import { useState, useEffect, useCallback } from 'react';

const STORAGE_KEY = 'career-hunter-saved-jobs';

export interface SavedJobInfo {
  jobId: string;
  fileName: string;
  savedAt: number;
}

interface UseSavedJobsReturn {
  savedJobs: Map<string, SavedJobInfo>;
  saveJob: (jobId: string, fileName: string) => void;
  unsaveJob: (jobId: string) => void;
  isJobSaved: (jobId: string) => boolean;
  getSavedJobInfo: (jobId: string) => SavedJobInfo | undefined;
}

/** Hook for managing saved jobs state in localStorage */
export const useSavedJobs = (): UseSavedJobsReturn => {
  const [savedJobs, setSavedJobs] = useState<Map<string, SavedJobInfo>>(new Map());

  // Load saved jobs from localStorage on mount
  useEffect(() => {
    try {
      const stored = localStorage.getItem(STORAGE_KEY);
      if (stored) {
        const parsed = JSON.parse(stored) as SavedJobInfo[];
        const jobsMap = new Map<string, SavedJobInfo>();
        parsed.forEach((job) => jobsMap.set(job.jobId, job));
        setSavedJobs(jobsMap);
      }
    } catch {
      // Failed to load saved jobs from localStorage - start fresh
    }
  }, []);

  // Persist to localStorage whenever savedJobs changes
  const persistToStorage = useCallback((jobs: Map<string, SavedJobInfo>) => {
    try {
      const jobsArray = Array.from(jobs.values());
      localStorage.setItem(STORAGE_KEY, JSON.stringify(jobsArray));
    } catch {
      // Failed to persist to localStorage - continue without saving
    }
  }, []);

  const saveJob = useCallback(
    (jobId: string, fileName: string) => {
      setSavedJobs((prev) => {
        const next = new Map(prev);
        next.set(jobId, {
          jobId,
          fileName,
          savedAt: Date.now(),
        });
        persistToStorage(next);
        return next;
      });
    },
    [persistToStorage]
  );

  const unsaveJob = useCallback(
    (jobId: string) => {
      setSavedJobs((prev) => {
        const next = new Map(prev);
        next.delete(jobId);
        persistToStorage(next);
        return next;
      });
    },
    [persistToStorage]
  );

  const isJobSaved = useCallback(
    (jobId: string): boolean => {
      return savedJobs.has(jobId);
    },
    [savedJobs]
  );

  const getSavedJobInfo = useCallback(
    (jobId: string): SavedJobInfo | undefined => {
      return savedJobs.get(jobId);
    },
    [savedJobs]
  );

  return { savedJobs, saveJob, unsaveJob, isJobSaved, getSavedJobInfo };
};

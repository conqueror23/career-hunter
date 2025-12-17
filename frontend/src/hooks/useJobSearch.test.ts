import { renderHook, act } from '@testing-library/react';

import { useJobSearch } from './useJobSearch';
import axios from 'axios';

// Mock axios before importing the hook
jest.mock('axios', () => ({
  post: jest.fn(),
}));

const mockedAxios = axios as jest.Mocked<typeof axios>;

describe('useJobSearch', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('initializes with empty state', () => {
    const { result } = renderHook(() => useJobSearch());

    expect(result.current.jobs).toEqual([]);
    expect(result.current.companies).toEqual([]);
    expect(result.current.loading).toBe(false);
    expect(result.current.error).toBe('');
  });

  test('sets loading state during search', async () => {
    mockedAxios.post.mockImplementation(() => new Promise(() => {}));

    const { result } = renderHook(() => useJobSearch());

    act(() => {
      result.current.search({
        role: 'Engineer',
        country: 'AU',
        location: 'Sydney',
        salary: '100k-150k',
        work_type: 'all',
        limit: 10,
      });
    });

    expect(result.current.loading).toBe(true);
  });

  test('updates jobs after successful search', async () => {
    const mockJobs = [
      {
        id: 'job_1',
        site: 'LinkedIn',
        title: 'Engineer',
        company: 'Tech Corp',
        location: 'Sydney',
        job_url: 'https://example.com',
        salary_range: '100k',
        company_url: '',
        description: '',
      },
    ];

    mockedAxios.post.mockResolvedValueOnce({ data: mockJobs });

    const { result } = renderHook(() => useJobSearch());

    await act(async () => {
      await result.current.search({
        role: 'Engineer',
        country: 'AU',
        location: 'Sydney',
        salary: '100k-150k',
        work_type: 'all',
        limit: 10,
      });
    });

    expect(result.current.jobs).toEqual(mockJobs);
    expect(result.current.loading).toBe(false);
    expect(result.current.error).toBe('');
  });

  test('sets error on failed search', async () => {
    mockedAxios.post.mockRejectedValueOnce(new Error('Network error'));

    const { result } = renderHook(() => useJobSearch());

    await act(async () => {
      await result.current.search({
        role: 'Engineer',
        country: 'AU',
        location: 'Sydney',
        salary: '100k-150k',
        work_type: 'all',
        limit: 10,
      });
    });

    expect(result.current.error).toBe('Network error');
    expect(result.current.jobs).toEqual([]);
    expect(result.current.loading).toBe(false);
  });

  test('computes companies from jobs', async () => {
    const mockJobs = [
      {
        id: 'job_1',
        site: 'LinkedIn',
        title: 'Engineer',
        company: 'Tech Corp',
        location: 'Sydney',
        job_url: 'https://example.com',
        salary_range: '100k',
        company_url: '',
        description: '',
      },
      {
        id: 'job_2',
        site: 'Indeed',
        title: 'Developer',
        company: 'Tech Corp',
        location: 'Melbourne',
        job_url: 'https://example.com/2',
        salary_range: '120k',
        company_url: '',
        description: '',
      },
      {
        id: 'job_3',
        site: 'Seek',
        title: 'Manager',
        company: 'Other Corp',
        location: 'Brisbane',
        job_url: 'https://example.com/3',
        salary_range: '150k',
        company_url: '',
        description: '',
      },
    ];

    mockedAxios.post.mockResolvedValueOnce({ data: mockJobs });

    const { result } = renderHook(() => useJobSearch());

    await act(async () => {
      await result.current.search({
        role: 'Engineer',
        country: 'AU',
        location: 'Sydney',
        salary: '100k-150k',
        work_type: 'all',
        limit: 10,
      });
    });

    expect(result.current.companies).toHaveLength(2);

    // Tech Corp has 2 jobs, should be first
    expect(result.current.companies[0].name).toBe('Tech Corp');
    expect(result.current.companies[0].jobCount).toBe(2);
    expect(result.current.companies[0].locations).toContain('Sydney');
    expect(result.current.companies[0].locations).toContain('Melbourne');
    expect(result.current.companies[0].sources).toContain('LinkedIn');
    expect(result.current.companies[0].sources).toContain('Indeed');

    // Other Corp has 1 job
    expect(result.current.companies[1].name).toBe('Other Corp');
    expect(result.current.companies[1].jobCount).toBe(1);
  });
});

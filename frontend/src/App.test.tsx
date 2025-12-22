import React from 'react';
import { render, screen, fireEvent, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import App from './App';

import axios from 'axios';

// Mock axios
jest.mock('axios', () => ({
  post: jest.fn(),
  isCancel: jest.fn(() => false),
}));
const mockedAxios = axios as jest.Mocked<typeof axios>;

describe('App', () => {
  beforeEach(() => {
    jest.clearAllMocks();
  });

  test('renders Career Hunter title', () => {
    render(<App />);
    expect(screen.getByText('Career Hunter')).toBeInTheDocument();
  });

  test('renders search form with default values', () => {
    render(<App />);

    expect(screen.getByLabelText(/Role/i)).toHaveValue('Engineer Manager');
    expect(screen.getByLabelText(/Country/i)).toHaveValue('AU');
    expect(screen.getByLabelText(/Location/i)).toHaveValue('Australia');
    expect(screen.getByLabelText(/Salary Range/i)).toHaveValue('200k-250k');
  });

  test('renders search button', () => {
    render(<App />);
    expect(screen.getByRole('button', { name: /Search/i })).toBeInTheDocument();
  });

  test('shows empty state message when no jobs', () => {
    render(<App />);
    expect(screen.getByText(/No jobs found/i)).toBeInTheDocument();
  });

  test('allows changing role input', async () => {
    render(<App />);
    const roleInput = screen.getByLabelText(/Role/i);

    await userEvent.clear(roleInput);
    await userEvent.type(roleInput, 'Software Engineer');

    expect(roleInput).toHaveValue('Software Engineer');
  });

  test('shows loading state when searching', async () => {
    mockedAxios.post.mockImplementation(() => new Promise(() => {})); // Never resolves

    render(<App />);
    const searchButton = screen.getByRole('button', { name: /Search/i });

    fireEvent.click(searchButton);

    expect(screen.getByText(/Searching/i)).toBeInTheDocument();
    expect(searchButton).toBeDisabled();
  });

  test('displays jobs after successful search', async () => {
    const mockJobs = [
      {
        id: 'job_1',
        site: 'LinkedIn',
        title: 'Software Engineer',
        company: 'Tech Corp',
        location: 'Sydney',
        job_url: 'https://example.com/job/1',
        salary_range: '150k-200k',
        company_url: 'https://example.com/company',
        description: 'Great job opportunity',
      },
    ];

    mockedAxios.post.mockResolvedValueOnce({ data: mockJobs });

    render(<App />);

    fireEvent.click(screen.getByRole('button', { name: /Search/i }));

    await waitFor(() => {
      expect(screen.getByText('Software Engineer')).toBeInTheDocument();
    });
    expect(screen.getByText('Tech Corp')).toBeInTheDocument();
    expect(screen.getByText('Sydney')).toBeInTheDocument();
  });

  test('displays error message on API failure', async () => {
    mockedAxios.post.mockRejectedValueOnce(new Error('Network error'));

    render(<App />);

    fireEvent.click(screen.getByRole('button', { name: /Search/i }));

    await waitFor(() => {
      expect(screen.getByText(/Network error/i)).toBeInTheDocument();
    });
  });

  test('shows tabs when jobs are loaded', async () => {
    const mockJobs = [
      {
        id: 'job_1',
        site: 'LinkedIn',
        title: 'Engineer',
        company: 'Corp',
        location: 'Sydney',
        job_url: 'https://example.com',
        salary_range: '100k',
        company_url: '',
        description: '',
      },
    ];

    mockedAxios.post.mockResolvedValueOnce({ data: mockJobs });

    render(<App />);
    fireEvent.click(screen.getByRole('button', { name: /Search/i }));

    await waitFor(() => {
      expect(screen.getByRole('tab', { name: /Jobs \(1\)/i })).toBeInTheDocument();
    });
    expect(screen.getByRole('tab', { name: /Companies \(1\)/i })).toBeInTheDocument();
  });

  test('can switch between Jobs and Companies tabs', async () => {
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

    render(<App />);
    fireEvent.click(screen.getByRole('button', { name: /Search/i }));

    await waitFor(() => {
      expect(screen.getByRole('tab', { name: /Companies/i })).toBeInTheDocument();
    });

    fireEvent.click(screen.getByRole('tab', { name: /Companies/i }));

    // Companies table should show company name
    await waitFor(() => {
      expect(screen.getByText('Tech Corp')).toBeInTheDocument();
    });
  });

  test('sends correct parameters to API', async () => {
    mockedAxios.post.mockResolvedValueOnce({ data: [] });

    render(<App />);

    // Change some values
    const roleInput = screen.getByLabelText(/Role/i);
    await userEvent.clear(roleInput);
    await userEvent.type(roleInput, 'Developer');

    fireEvent.click(screen.getByRole('button', { name: /Search/i }));

    await waitFor(() => {
      expect(mockedAxios.post).toHaveBeenCalledWith(
        'http://localhost:8000/api/search',
        expect.objectContaining({
          role: 'Developer',
          country: 'AU',
          location: 'Australia',
          salary: '200k-250k',
          work_type: 'all',
          limit: 25,
        }),
        expect.objectContaining({ signal: expect.any(AbortSignal) })
      );
    });
  });
});

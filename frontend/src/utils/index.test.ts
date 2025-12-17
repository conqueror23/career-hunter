import { downloadJobAsCSV, getCompanyLinks, getSourceStyle } from './index';
import { Job } from '../types';

// Mock DOM APIs
const mockCreateElement = jest.fn();
const mockAppendChild = jest.fn();
const mockRemoveChild = jest.fn();
const mockClick = jest.fn();

describe('getCompanyLinks', () => {
  test('generates correct Glassdoor URL', () => {
    const links = getCompanyLinks('Tech Corp');
    expect(links.glassdoor).toBe('https://www.glassdoor.com/Search/results.htm?keyword=Tech%20Corp');
  });

  test('generates correct LinkedIn URL', () => {
    const links = getCompanyLinks('Tech Corp');
    expect(links.linkedin).toBe('https://www.linkedin.com/company/tech-corp');
  });

  test('handles special characters in company name', () => {
    const links = getCompanyLinks('Company & Sons Inc.');
    expect(links.glassdoor).toContain('Company%20%26%20Sons%20Inc.');
    expect(links.linkedin).toBe('https://www.linkedin.com/company/company-sons-inc-');
  });

  test('handles empty company name', () => {
    const links = getCompanyLinks('');
    expect(links.glassdoor).toBe('https://www.glassdoor.com/Search/results.htm?keyword=');
    expect(links.linkedin).toBe('https://www.linkedin.com/company/');
  });
});

describe('getSourceStyle', () => {
  test('returns Seek style for Seek source', () => {
    const style = getSourceStyle('Seek');
    expect(style.color).toBe('#e6007e');
    expect(style.backgroundColor).toBe('#e6007e1a');
  });

  test('returns LinkedIn style for LinkedIn source', () => {
    const style = getSourceStyle('LinkedIn');
    expect(style.color).toBe('#0077b5');
    expect(style.backgroundColor).toBe('#0077b51a');
  });

  test('returns Indeed style for Indeed source', () => {
    const style = getSourceStyle('Indeed');
    expect(style.color).toBe('#2164f3');
    expect(style.backgroundColor).toBe('#2164f31a');
  });

  test('returns default style for unknown source', () => {
    const style = getSourceStyle('Unknown');
    expect(style.color).toBe('text.primary');
    expect(style.backgroundColor).toBe('#f0f0f0');
  });

  test('is case insensitive', () => {
    const seekStyle = getSourceStyle('SEEK');
    expect(seekStyle.color).toBe('#e6007e');

    const linkedinStyle = getSourceStyle('linkedin');
    expect(linkedinStyle.color).toBe('#0077b5');
  });
});

describe('downloadJobAsCSV', () => {
  let originalCreateObjectURL: typeof URL.createObjectURL;
  let originalRevokeObjectURL: typeof URL.revokeObjectURL;
  let mockLink: HTMLAnchorElement;

  beforeEach(() => {
    originalCreateObjectURL = URL.createObjectURL;
    originalRevokeObjectURL = URL.revokeObjectURL;
    URL.createObjectURL = jest.fn(() => 'blob:test-url');
    URL.revokeObjectURL = jest.fn();

    mockLink = {
      setAttribute: jest.fn(),
      click: mockClick,
    } as unknown as HTMLAnchorElement;

    jest.spyOn(document, 'createElement').mockReturnValue(mockLink);
    jest.spyOn(document.body, 'appendChild').mockImplementation(mockAppendChild);
    jest.spyOn(document.body, 'removeChild').mockImplementation(mockRemoveChild);
  });

  afterEach(() => {
    URL.createObjectURL = originalCreateObjectURL;
    URL.revokeObjectURL = originalRevokeObjectURL;
    jest.restoreAllMocks();
  });

  test('creates a download link with correct attributes', () => {
    const job: Job = {
      id: 'test_1',
      site: 'LinkedIn',
      title: 'Software Engineer',
      company: 'Tech Corp',
      location: 'Sydney',
      job_url: 'https://example.com/job',
      salary_range: '100k-150k',
      company_url: 'https://example.com/company',
      description: 'Great opportunity',
    };

    downloadJobAsCSV(job);

    expect(document.createElement).toHaveBeenCalledWith('a');
    expect(mockLink.setAttribute).toHaveBeenCalledWith('href', 'blob:test-url');
    expect(mockLink.setAttribute).toHaveBeenCalledWith(
      'download',
      expect.stringMatching(/^job_Tech_Corp_\d+\.csv$/)
    );
    expect(mockClick).toHaveBeenCalled();
  });

  test('handles job with special characters in company name', () => {
    const job: Job = {
      id: 'test_1',
      site: 'LinkedIn',
      title: 'Engineer',
      company: 'Company & Sons',
      location: 'Sydney',
      job_url: 'https://example.com',
      salary_range: '',
      company_url: '',
      description: '',
    };

    downloadJobAsCSV(job);

    expect(mockLink.setAttribute).toHaveBeenCalledWith(
      'download',
      expect.stringMatching(/^job_Company___Sons_\d+\.csv$/)
    );
  });

  test('handles job with quotes in description', () => {
    const job: Job = {
      id: 'test_1',
      site: 'LinkedIn',
      title: 'Engineer',
      company: 'Corp',
      location: 'Sydney',
      job_url: 'https://example.com',
      salary_range: '',
      company_url: '',
      description: 'Looking for "senior" developer',
    };

    // Should not throw
    expect(() => downloadJobAsCSV(job)).not.toThrow();
  });
});

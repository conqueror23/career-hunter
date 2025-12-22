import { Job } from '../types';

/** Escape CSV field value */
const escapeCSV = (value: string | undefined): string => {
  return `"${(value || '').replace(/"/g, '""')}"`;
};

/** Generate a filename for a job CSV */
export const generateJobFileName = (job: Job): string => {
  return `job_${job.company.replace(/[^a-zA-Z0-9]/g, '_')}_${Date.now()}.csv`;
};

/** Download a job as a CSV file and return the filename */
export const downloadJobAsCSV = (job: Job): string => {
  const headers = [
    'Title',
    'Company',
    'Location',
    'Salary',
    'Site',
    'Job URL',
    'Company URL',
    'Description',
  ];
  const row = [
    escapeCSV(job.title),
    escapeCSV(job.company),
    escapeCSV(job.location),
    escapeCSV(job.salary_range),
    escapeCSV(job.site),
    escapeCSV(job.job_url),
    escapeCSV(job.company_url),
    escapeCSV(job.description),
  ];

  const csvContent = headers.join(',') + '\n' + row.join(',');
  const blob = new Blob([csvContent], { type: 'text/csv;charset=utf-8;' });
  const url = URL.createObjectURL(blob);
  const link = document.createElement('a');
  const fileName = generateJobFileName(job);
  link.setAttribute('href', url);
  link.setAttribute('download', fileName);
  document.body.appendChild(link);
  link.click();
  document.body.removeChild(link);
  URL.revokeObjectURL(url);
  return fileName;
};

/** Generate company links for external sites */
export const getCompanyLinks = (companyName: string) => {
  const encodedName = encodeURIComponent(companyName);
  return {
    glassdoor: `https://www.glassdoor.com/Search/results.htm?keyword=${encodedName}`,
    linkedin: `https://www.linkedin.com/company/${companyName.toLowerCase().replace(/[^a-z0-9]+/g, '-')}`,
  };
};

/** Get source-specific styling */
export const getSourceStyle = (source: string) => {
  const sourceLower = source.toLowerCase();

  if (sourceLower.includes('seek')) {
    return { backgroundColor: '#e6007e1a', color: '#e6007e' };
  }
  if (sourceLower.includes('linkedin')) {
    return { backgroundColor: '#0077b51a', color: '#0077b5' };
  }
  if (sourceLower.includes('indeed')) {
    return { backgroundColor: '#2164f31a', color: '#2164f3' };
  }
  return { backgroundColor: '#f0f0f0', color: 'text.primary' };
};

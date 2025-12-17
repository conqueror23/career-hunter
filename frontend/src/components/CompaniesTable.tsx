import React from 'react';
import {
  Table,
  TableBody,
  TableCell,
  TableContainer,
  TableHead,
  TableRow,
  Paper,
  Tooltip,
  Link,
  Box,
  Typography,
  Chip,
} from '@mui/material';
import { CompanyInfo } from '../types';
import { SourceBadge } from './SourceBadge';
import { CompanyLinks } from './CompanyLinks';

interface CompaniesTableProps {
  companies: CompanyInfo[];
}

const MAX_VISIBLE_LOCATIONS = 3;

const CompanyJobsTooltip: React.FC<{ company: CompanyInfo }> = ({ company }) => (
  <Box sx={{ p: 1 }}>
    <Typography variant="subtitle2" sx={{ mb: 1 }}>
      Open Positions:
    </Typography>
    {company.jobs.map((job) => (
      <Box key={job.id} sx={{ mb: 0.5 }}>
        <Link
          href={job.job_url}
          target="_blank"
          rel="noopener"
          sx={{ color: '#90caf9', fontSize: '0.85rem' }}
        >
          {job.title}
        </Link>
      </Box>
    ))}
  </Box>
);

export const CompaniesTable: React.FC<CompaniesTableProps> = ({ companies }) => {
  return (
    <TableContainer component={Paper}>
      <Table sx={{ minWidth: 650 }} aria-label="companies table">
        <TableHead>
          <TableRow sx={{ backgroundColor: '#f5f5f5' }}>
            <TableCell><strong>Company</strong></TableCell>
            <TableCell><strong>Open Positions</strong></TableCell>
            <TableCell><strong>Locations</strong></TableCell>
            <TableCell><strong>Sources</strong></TableCell>
            <TableCell><strong>Links</strong></TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {companies.map((company) => (
            <TableRow key={company.name} sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
              <TableCell component="th" scope="row">
                <Tooltip title={<CompanyJobsTooltip company={company} />} arrow placement="right">
                  <Typography
                    sx={{
                      fontWeight: 'medium',
                      cursor: 'pointer',
                      '&:hover': { textDecoration: 'underline' },
                    }}
                  >
                    {company.name}
                  </Typography>
                </Tooltip>
              </TableCell>
              <TableCell>
                <Chip label={company.jobCount} size="small" color="primary" />
              </TableCell>
              <TableCell>
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                  {company.locations.slice(0, MAX_VISIBLE_LOCATIONS).map((loc, i) => (
                    <Chip key={i} label={loc} size="small" variant="outlined" />
                  ))}
                  {company.locations.length > MAX_VISIBLE_LOCATIONS && (
                    <Chip
                      label={`+${company.locations.length - MAX_VISIBLE_LOCATIONS}`}
                      size="small"
                      variant="outlined"
                    />
                  )}
                </Box>
              </TableCell>
              <TableCell>
                <Box sx={{ display: 'flex', flexWrap: 'wrap', gap: 0.5 }}>
                  {company.sources.map((source, i) => (
                    <SourceBadge key={i} source={source} size="small" />
                  ))}
                </Box>
              </TableCell>
              <TableCell>
                <CompanyLinks companyName={company.name} variant="inline" />
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

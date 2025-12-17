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
  Button,
} from '@mui/material';
import { Job } from '../types';
import { downloadJobAsCSV } from '../utils';
import { SourceBadge } from './SourceBadge';
import { CompanyLinks } from './CompanyLinks';

interface JobsTableProps {
  jobs: Job[];
}

const JobDescriptionTooltip: React.FC<{ description: string }> = ({ description }) => (
  <Box sx={{ maxWidth: 500, maxHeight: 400, overflow: 'auto', p: 1 }}>
    <Typography variant="body2" sx={{ whiteSpace: 'pre-wrap', fontSize: '0.85rem' }}>
      {description}
    </Typography>
  </Box>
);

export const JobsTable: React.FC<JobsTableProps> = ({ jobs }) => {
  return (
    <TableContainer component={Paper}>
      <Table sx={{ minWidth: 650 }} aria-label="jobs table">
        <TableHead>
          <TableRow sx={{ backgroundColor: '#f5f5f5' }}>
            <TableCell><strong>Title</strong></TableCell>
            <TableCell><strong>Company</strong></TableCell>
            <TableCell><strong>Location</strong></TableCell>
            <TableCell><strong>Salary</strong></TableCell>
            <TableCell><strong>Source</strong></TableCell>
            <TableCell><strong>Save</strong></TableCell>
          </TableRow>
        </TableHead>
        <TableBody>
          {jobs.map((job) => (
            <TableRow key={job.id} sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
              <TableCell component="th" scope="row">
                <Tooltip
                  title={
                    job.description ? (
                      <JobDescriptionTooltip description={job.description} />
                    ) : (
                      <Typography variant="body2">No description available</Typography>
                    )
                  }
                  arrow
                  placement="right"
                  enterDelay={300}
                  leaveDelay={200}
                  slotProps={{
                    tooltip: {
                      sx: {
                        maxWidth: 500,
                        maxHeight: 400,
                        backgroundColor: 'rgba(50, 50, 50, 0.95)',
                      },
                    },
                  }}
                >
                  <Link
                    href={job.job_url}
                    target="_blank"
                    rel="noopener"
                    underline="hover"
                    sx={{ fontWeight: 'medium' }}
                  >
                    {job.title}
                  </Link>
                </Tooltip>
              </TableCell>
              <TableCell>
                <Tooltip title={<CompanyLinks companyName={job.company} variant="tooltip" />} arrow placement="right">
                  <Box component="span" sx={{ cursor: 'pointer', '&:hover': { textDecoration: 'underline' } }}>
                    {job.company}
                  </Box>
                </Tooltip>
              </TableCell>
              <TableCell>{job.location}</TableCell>
              <TableCell>{job.salary_range || 'N/A'}</TableCell>
              <TableCell>
                <SourceBadge source={job.site} />
              </TableCell>
              <TableCell>
                <Button
                  variant="outlined"
                  size="small"
                  onClick={() => downloadJobAsCSV(job)}
                  sx={{ textTransform: 'none' }}
                >
                  Save
                </Button>
              </TableCell>
            </TableRow>
          ))}
        </TableBody>
      </Table>
    </TableContainer>
  );
};

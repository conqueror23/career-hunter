import React, { useState } from 'react';
import axios from 'axios';
import { 
  Container, Typography, TextField, Button, 
  Table, TableBody, TableCell, TableContainer, TableHead, TableRow, Paper, 
  LinearProgress, Link, Box, Grid, Alert
} from '@mui/material';

interface Job {
  id: string;
  site: string;
  title: string;
  company: string;
  location: string;
  job_url: string;
  salary_range: string;
  company_url: string;
}

function App() {
  const [role, setRole] = useState('Senior Software Engineer');
  const [country, setCountry] = useState('AU');
  const [location, setLocation] = useState('Australia');
  const [salary, setSalary] = useState('140k-200k');
  const [jobs, setJobs] = useState<Job[]>([]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState('');

  const handleSearch = async () => {
    setLoading(true);
    setError('');
    setJobs([]);

    try {
      const response = await axios.post('http://localhost:8000/api/search', {
        role,
        country,
        location,
        salary,
        limit: 10
      });
      setJobs(response.data);
    } catch (err: any) {
      setError(err.message || 'An error occurred while fetching jobs');
    } finally {
      setLoading(false);
    }
  };

  return (
    <Container maxWidth="lg" sx={{ mt: 4 }}>
      <Typography variant="h3" gutterBottom component="div" sx={{ mb: 4, fontWeight: 'bold' }}>
        Career Hunter
      </Typography>

      <Paper sx={{ p: 3, mb: 4 }}>
        <Grid container spacing={3} alignItems="flex-end">
          <Grid item xs={12} sm={3}>
            <TextField 
              fullWidth 
              label="Role" 
              value={role} 
              onChange={(e) => setRole(e.target.value)} 
            />
          </Grid>
          <Grid item xs={12} sm={2}>
            <TextField 
              fullWidth 
              label="Country" 
              value={country} 
              onChange={(e) => setCountry(e.target.value)} 
            />
          </Grid>
          <Grid item xs={12} sm={3}>
            <TextField 
              fullWidth 
              label="Location" 
              value={location} 
              onChange={(e) => setLocation(e.target.value)} 
            />
          </Grid>
          <Grid item xs={12} sm={2}>
            <TextField 
              fullWidth 
              label="Salary Range" 
              value={salary} 
              onChange={(e) => setSalary(e.target.value)} 
              helperText="e.g. 140k-200k"
            />
          </Grid>
          <Grid item xs={12} sm={2}>
            <Button 
              variant="contained" 
              size="large" 
              fullWidth 
              onClick={handleSearch}
              disabled={loading}
              sx={{ height: '56px' }}
            >
              {loading ? 'Searching...' : 'Search'}
            </Button>
          </Grid>
        </Grid>
      </Paper>

      {loading && <LinearProgress sx={{ mb: 2 }} />}
      
      {error && <Alert severity="error" sx={{ mb: 2 }}>{error}</Alert>}

      {!loading && jobs.length > 0 && (
        <TableContainer component={Paper}>
          <Table sx={{ minWidth: 650 }} aria-label="simple table">
            <TableHead>
              <TableRow sx={{ backgroundColor: '#f5f5f5' }}>
                <TableCell><strong>Title</strong></TableCell>
                <TableCell><strong>Company</strong></TableCell>
                <TableCell><strong>Location</strong></TableCell>
                <TableCell><strong>Salary</strong></TableCell>
                <TableCell><strong>Source</strong></TableCell>
              </TableRow>
            </TableHead>
            <TableBody>
              {jobs.map((job) => (
                <TableRow key={job.id} sx={{ '&:last-child td, &:last-child th': { border: 0 } }}>
                  <TableCell component="th" scope="row">
                    <Link href={job.job_url} target="_blank" rel="noopener" underline="hover" sx={{ fontWeight: 'medium' }}>
                      {job.title}
                    </Link>
                  </TableCell>
                  <TableCell>
                    {job.company_url && job.company_url !== 'N/A' ? (
                      <Link href={job.company_url} target="_blank" rel="noopener" color="inherit">
                        {job.company}
                      </Link>
                    ) : (
                      job.company
                    )}
                  </TableCell>
                  <TableCell>{job.location}</TableCell>
                  <TableCell>{job.salary_range || 'N/A'}</TableCell>
                  <TableCell>
                    <Box component="span" sx={{ 
                      textTransform: 'capitalize', 
                      px: 1, 
                      py: 0.5, 
                      borderRadius: 1,
                      fontSize: '0.8rem',
                      backgroundColor: job.site.toLowerCase().includes('seek') ? '#e6007e1a' : 
                                     job.site.toLowerCase().includes('linkedin') ? '#0077b51a' :
                                     job.site.toLowerCase().includes('indeed') ? '#2164f31a' : '#f0f0f0',
                      color: job.site.toLowerCase().includes('seek') ? '#e6007e' : 
                             job.site.toLowerCase().includes('linkedin') ? '#0077b5' :
                             job.site.toLowerCase().includes('indeed') ? '#2164f3' : 'text.primary'
                    }}>
                      {job.site}
                    </Box>
                  </TableCell>
                </TableRow>
              ))}
            </TableBody>
          </Table>
        </TableContainer>
      )}
      
      {!loading && jobs.length === 0 && !error && (
        <Box textAlign="center" py={5} color="text.secondary">
          <Typography>No jobs found. Try adjusting your search criteria.</Typography>
        </Box>
      )}
    </Container>
  );
}

export default App;
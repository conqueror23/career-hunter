import React, { useState } from 'react';
import { Container, Typography, LinearProgress, Box, Alert, Tabs, Tab } from '@mui/material';

import { WorkType } from './types';
import { useJobSearch } from './hooks/useJobSearch';
import { SearchForm, JobsTable, CompaniesTable } from './components';

const DEFAULT_ROLE = 'Engineer Manager';
const DEFAULT_COUNTRY = 'AU';
const DEFAULT_LOCATION = 'Australia';
const DEFAULT_SALARY = '200k-250k';
const DEFAULT_WORK_TYPE: WorkType = 'all';
const DEFAULT_LIMIT = 10;

function App() {
  const [role, setRole] = useState(DEFAULT_ROLE);
  const [country, setCountry] = useState(DEFAULT_COUNTRY);
  const [location, setLocation] = useState(DEFAULT_LOCATION);
  const [salary, setSalary] = useState(DEFAULT_SALARY);
  const [workType, setWorkType] = useState<WorkType>(DEFAULT_WORK_TYPE);
  const [activeTab, setActiveTab] = useState(0);

  const { jobs, companies, loading, error, search } = useJobSearch();

  const handleSearch = () => {
    search({
      role,
      country,
      location,
      salary,
      work_type: workType,
      limit: DEFAULT_LIMIT,
    });
  };

  const hasResults = !loading && jobs.length > 0;

  return (
    <Container maxWidth="lg" sx={{ mt: 4 }}>
      <Typography variant="h3" gutterBottom component="div" sx={{ mb: 4, fontWeight: 'bold' }}>
        Career Hunter
      </Typography>

      <SearchForm
        role={role}
        country={country}
        location={location}
        salary={salary}
        workType={workType}
        loading={loading}
        onRoleChange={setRole}
        onCountryChange={setCountry}
        onLocationChange={setLocation}
        onSalaryChange={setSalary}
        onWorkTypeChange={setWorkType}
        onSearch={handleSearch}
      />

      {loading && <LinearProgress sx={{ mb: 2 }} />}

      {error && (
        <Alert severity="error" sx={{ mb: 2 }}>
          {error}
        </Alert>
      )}

      {hasResults && (
        <>
          <Box sx={{ borderBottom: 1, borderColor: 'divider', mb: 2 }}>
            <Tabs value={activeTab} onChange={(_, v) => setActiveTab(v)}>
              <Tab label={`Jobs (${jobs.length})`} />
              <Tab label={`Companies (${companies.length})`} />
            </Tabs>
          </Box>

          {activeTab === 0 && <JobsTable jobs={jobs} />}
          {activeTab === 1 && <CompaniesTable companies={companies} />}
        </>
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

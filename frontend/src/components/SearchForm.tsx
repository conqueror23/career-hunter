import React from 'react';
import {
  Paper,
  Grid,
  TextField,
  FormControl,
  InputLabel,
  Select,
  MenuItem,
  Button,
  SelectChangeEvent,
  Tooltip,
} from '@mui/material';
import RefreshIcon from '@mui/icons-material/Refresh';
import { WorkType } from '../types';

interface SearchFormProps {
  role: string;
  country: string;
  location: string;
  salary: string;
  workType: WorkType;
  loading: boolean;
  onRoleChange: (value: string) => void;
  onCountryChange: (value: string) => void;
  onLocationChange: (value: string) => void;
  onSalaryChange: (value: string) => void;
  onWorkTypeChange: (value: WorkType) => void;
  onSearch: () => void;
  onRefresh?: () => void;
}

const WORK_TYPE_OPTIONS: { value: WorkType; label: string }[] = [
  { value: 'all', label: 'All' },
  { value: 'remote', label: 'Remote' },
  { value: 'hybrid', label: 'Hybrid' },
  { value: 'onsite', label: 'On-site' },
];

export const SearchForm: React.FC<SearchFormProps> = ({
  role,
  country,
  location,
  salary,
  workType,
  loading,
  onRoleChange,
  onCountryChange,
  onLocationChange,
  onSalaryChange,
  onWorkTypeChange,
  onSearch,
  onRefresh,
}) => {
  const handleWorkTypeChange = (e: SelectChangeEvent) => {
    onWorkTypeChange(e.target.value as WorkType);
  };

  return (
    <Paper sx={{ p: 3, mb: 4 }}>
      <Grid container spacing={2} alignItems="flex-start">
        <Grid size={{ xs: 12, sm: 2.5 }}>
          <TextField
            fullWidth
            label="Role"
            value={role}
            onChange={(e) => onRoleChange(e.target.value)}
          />
        </Grid>
        <Grid size={{ xs: 12, sm: 1.5 }}>
          <TextField
            fullWidth
            label="Country"
            value={country}
            onChange={(e) => onCountryChange(e.target.value)}
          />
        </Grid>
        <Grid size={{ xs: 12, sm: 2 }}>
          <TextField
            fullWidth
            label="Location"
            value={location}
            onChange={(e) => onLocationChange(e.target.value)}
          />
        </Grid>
        <Grid size={{ xs: 12, sm: 2 }}>
          <TextField
            fullWidth
            label="Salary Range"
            value={salary}
            onChange={(e) => onSalaryChange(e.target.value)}
          />
        </Grid>
        <Grid size={{ xs: 12, sm: 2 }}>
          <FormControl fullWidth>
            <InputLabel>Work Type</InputLabel>
            <Select value={workType} label="Work Type" onChange={handleWorkTypeChange}>
              {WORK_TYPE_OPTIONS.map((option) => (
                <MenuItem key={option.value} value={option.value}>
                  {option.label}
                </MenuItem>
              ))}
            </Select>
          </FormControl>
        </Grid>
        <Grid size={{ xs: 12, sm: 1.5 }}>
          <Button
            variant="contained"
            size="large"
            fullWidth
            onClick={onSearch}
            disabled={loading}
            sx={{ height: '56px' }}
          >
            {loading ? 'Searching...' : 'Search'}
          </Button>
        </Grid>
        {onRefresh && (
          <Grid size={{ xs: 12, sm: 0.5 }}>
            <Tooltip title="Clear cache and fetch fresh results" arrow>
              <span>
                <Button
                  variant="outlined"
                  size="large"
                  onClick={onRefresh}
                  disabled={loading}
                  sx={{ height: '56px', minWidth: '56px', p: 0 }}
                >
                  <RefreshIcon />
                </Button>
              </span>
            </Tooltip>
          </Grid>
        )}
      </Grid>
    </Paper>
  );
};

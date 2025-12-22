import React from 'react';
import { Button, Tooltip } from '@mui/material';
import { Job } from '../types';
import { downloadJobAsCSV } from '../utils';

interface SaveButtonProps {
  job: Job;
  isSaved: boolean;
  fileName?: string;
  onSave: (jobId: string, fileName: string) => void;
  onUnsave: (jobId: string) => void;
}

export const SaveButton: React.FC<SaveButtonProps> = ({
  job,
  isSaved,
  fileName,
  onSave,
  onUnsave,
}) => {
  const handleClick = () => {
    if (isSaved) {
      // If already saved, clicking "Saved" will unsave (mark as not saved)
      // User can then click "Save" again to re-download
      onUnsave(job.id);
    } else {
      // Download the file and mark as saved
      const downloadedFileName = downloadJobAsCSV(job);
      onSave(job.id, downloadedFileName);
    }
  };

  if (isSaved) {
    return (
      <Tooltip title={`Saved as: ${fileName}. Click to unsave.`} arrow placement="left">
        <Button
          variant="contained"
          size="small"
          onClick={handleClick}
          sx={{
            textTransform: 'none',
            backgroundColor: '#1976d2',
            color: '#fff',
            '&:hover': {
              backgroundColor: '#1565c0',
            },
          }}
        >
          Saved
        </Button>
      </Tooltip>
    );
  }

  return (
    <Button variant="outlined" size="small" onClick={handleClick} sx={{ textTransform: 'none' }}>
      Save
    </Button>
  );
};

import React from 'react';
import { Box } from '@mui/material';
import { getSourceStyle } from '../utils';

interface SourceBadgeProps {
  source: string;
  size?: 'small' | 'medium';
}

export const SourceBadge: React.FC<SourceBadgeProps> = ({ source, size = 'medium' }) => {
  const style = getSourceStyle(source);
  const fontSize = size === 'small' ? '0.75rem' : '0.8rem';
  const padding = size === 'small' ? { px: 1, py: 0.25 } : { px: 1, py: 0.5 };

  return (
    <Box
      component="span"
      sx={{
        textTransform: 'capitalize',
        ...padding,
        borderRadius: 1,
        fontSize,
        ...style,
      }}
    >
      {source}
    </Box>
  );
};

import React from 'react';
import { Stack, Link } from '@mui/material';
import { getCompanyLinks } from '../utils';

interface CompanyLinksProps {
  companyName: string;
  variant?: 'tooltip' | 'inline';
}

export const CompanyLinks: React.FC<CompanyLinksProps> = ({ companyName, variant = 'tooltip' }) => {
  const links = getCompanyLinks(companyName);

  const glassdoorColor = variant === 'tooltip' ? '#00e676' : '#0caa41';
  const linkedinColor = '#29b6f6';

  return (
    <Stack
      spacing={1}
      direction={variant === 'inline' ? 'row' : 'column'}
      sx={{ p: variant === 'tooltip' ? 0.5 : 0 }}
    >
      <Link
        href={links.glassdoor}
        target="_blank"
        rel="noopener"
        sx={{
          color: glassdoorColor,
          display: 'flex',
          alignItems: 'center',
          gap: 0.5,
          fontWeight: 'bold',
          fontSize: variant === 'inline' ? '0.85rem' : undefined,
        }}
      >
        Glassdoor
      </Link>
      <Link
        href={links.linkedin}
        target="_blank"
        rel="noopener"
        sx={{
          color: linkedinColor,
          display: 'flex',
          alignItems: 'center',
          gap: 0.5,
          fontWeight: 'bold',
          fontSize: variant === 'inline' ? '0.85rem' : undefined,
        }}
      >
        LinkedIn
      </Link>
    </Stack>
  );
};

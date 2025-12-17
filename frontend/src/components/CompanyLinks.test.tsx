import React from 'react';
import { render, screen } from '@testing-library/react';
import { CompanyLinks } from './CompanyLinks';

describe('CompanyLinks', () => {
  test('renders Glassdoor link', () => {
    render(<CompanyLinks companyName="Tech Corp" />);
    const glassdoorLink = screen.getByRole('link', { name: /Glassdoor/i });
    expect(glassdoorLink).toBeInTheDocument();
    expect(glassdoorLink).toHaveAttribute(
      'href',
      'https://www.glassdoor.com/Search/results.htm?keyword=Tech%20Corp'
    );
  });

  test('renders LinkedIn link', () => {
    render(<CompanyLinks companyName="Tech Corp" />);
    const linkedinLink = screen.getByRole('link', { name: /LinkedIn/i });
    expect(linkedinLink).toBeInTheDocument();
    expect(linkedinLink).toHaveAttribute('href', 'https://www.linkedin.com/company/tech-corp');
  });

  test('links open in new tab', () => {
    render(<CompanyLinks companyName="Tech Corp" />);
    const links = screen.getAllByRole('link');
    links.forEach((link) => {
      expect(link).toHaveAttribute('target', '_blank');
      expect(link).toHaveAttribute('rel', 'noopener');
    });
  });

  test('renders in tooltip variant by default', () => {
    const { container } = render(<CompanyLinks companyName="Tech Corp" />);
    // In tooltip variant, links are stacked vertically (column direction)
    const stack = container.firstChild;
    expect(stack).toHaveStyle({ flexDirection: 'column' });
  });

  test('renders in inline variant when specified', () => {
    const { container } = render(<CompanyLinks companyName="Tech Corp" variant="inline" />);
    // In inline variant, links are in a row
    const stack = container.firstChild;
    expect(stack).toHaveStyle({ flexDirection: 'row' });
  });

  test('handles company names with special characters', () => {
    render(<CompanyLinks companyName="Company & Sons Inc." />);
    const glassdoorLink = screen.getByRole('link', { name: /Glassdoor/i });
    expect(glassdoorLink).toHaveAttribute(
      'href',
      expect.stringContaining('Company%20%26%20Sons%20Inc.')
    );
  });
});

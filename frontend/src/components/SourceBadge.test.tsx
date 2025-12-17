import React from 'react';
import { render, screen } from '@testing-library/react';
import { SourceBadge } from './SourceBadge';

describe('SourceBadge', () => {
  test('renders source text', () => {
    render(<SourceBadge source="LinkedIn" />);
    expect(screen.getByText('LinkedIn')).toBeInTheDocument();
  });

  test('renders with medium size by default', () => {
    const { container } = render(<SourceBadge source="LinkedIn" />);
    const badge = container.firstChild;
    expect(badge).toHaveStyle({ fontSize: '0.8rem' });
  });

  test('renders with small size when specified', () => {
    const { container } = render(<SourceBadge source="LinkedIn" size="small" />);
    const badge = container.firstChild;
    expect(badge).toHaveStyle({ fontSize: '0.75rem' });
  });

  test('applies LinkedIn styling', () => {
    const { container } = render(<SourceBadge source="LinkedIn" />);
    const badge = container.firstChild;
    expect(badge).toHaveStyle({ backgroundColor: '#0077b51a' });
  });

  test('applies Seek styling', () => {
    const { container } = render(<SourceBadge source="Seek" />);
    const badge = container.firstChild;
    expect(badge).toHaveStyle({ backgroundColor: '#e6007e1a' });
  });

  test('applies Indeed styling', () => {
    const { container } = render(<SourceBadge source="Indeed" />);
    const badge = container.firstChild;
    expect(badge).toHaveStyle({ backgroundColor: '#2164f31a' });
  });

  test('applies default styling for unknown source', () => {
    const { container } = render(<SourceBadge source="Unknown" />);
    const badge = container.firstChild;
    expect(badge).toHaveStyle({ backgroundColor: '#f0f0f0' });
  });
});

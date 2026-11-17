import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { describe, expect, it } from 'vitest';
import { ButtonLink } from './ButtonLink';

describe('ButtonLink', () => {
    it('renders a styled link to the requested destination', () => {
        render(<MemoryRouter><ButtonLink to="/tasks" variant="secondary" size="sm">Open tasks</ButtonLink></MemoryRouter>);
        const link = screen.getByRole('link', { name: 'Open tasks' });
        expect(link).toHaveAttribute('href', '/tasks');
        expect(link).toHaveClass('btn', 'secondary', 'btn-secondary', 'sm');
    });
});

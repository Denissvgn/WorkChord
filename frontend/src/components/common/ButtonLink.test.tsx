import { render, screen } from '@testing-library/react';
import { MemoryRouter } from 'react-router-dom';
import { describe, expect, it } from 'vitest';
import { ButtonLink } from './ButtonLink';
import { Button } from './Button';

describe('ButtonLink', () => {
    it('renders a styled link to the requested destination', () => {
        render(<MemoryRouter><ButtonLink to="/tasks" variant="secondary" size="sm">Open tasks</ButtonLink></MemoryRouter>);
        const link = screen.getByRole('link', { name: 'Open tasks' });
        expect(link).toHaveAttribute('href', '/tasks');
        expect(link).toHaveClass('btn', 'secondary', 'btn-secondary', 'sm');
    });
});

describe('Button plain variant', () => {
    it('keeps text controls free of shared button box styles', () => {
        render(<Button variant="plain" className="text-left">Task title</Button>);
        const button = screen.getByRole('button', { name: 'Task title' });
        expect(button).toHaveClass('text-left', 'focus-visible:outline');
        expect(button).not.toHaveClass('btn', 'primary', 'btn-primary', 'min-h-9', 'px-4');
    });
});

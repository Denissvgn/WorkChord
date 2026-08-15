import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import { Input } from './Input';

describe('Input', () => {
    it('shows a visible required indicator while preserving native semantics', () => {
        render(<Input label="Project name" required />);

        expect(screen.getByText('Required')).toBeVisible();
        expect(screen.getByRole('textbox', { name: /project name/i })).toBeRequired();
    });

    it('does not show the indicator for optional fields', () => {
        render(<Input label="Description" />);

        expect(screen.queryByText('Required')).not.toBeInTheDocument();
    });
});

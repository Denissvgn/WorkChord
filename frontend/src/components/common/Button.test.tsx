import { render, screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import { Button } from './Button';

describe('Button', () => {
    it('keeps a loading action disabled and exposes its busy state', () => {
        const { container } = render(
            <Button isLoading disabled={false}>
                Save
            </Button>,
        );

        const button = screen.getByRole('button', { name: 'Save' });
        expect(button).toBeDisabled();
        expect(button).toHaveAttribute('aria-busy', 'true');
        expect(container.querySelector('svg')).toHaveAttribute('aria-hidden', 'true');
    });

    it('preserves an explicit busy state when it is not rendering a loading spinner', () => {
        render(<Button aria-busy="true">Synchronize</Button>);

        expect(screen.getByRole('button', { name: 'Synchronize' }))
            .toHaveAttribute('aria-busy', 'true');
    });
});

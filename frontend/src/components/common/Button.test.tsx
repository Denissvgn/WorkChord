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

    it('does not submit a surrounding form unless it is a submit button', () => {
        render(
            <form>
                <Button>Change status</Button>
                <Button type="submit">Save</Button>
            </form>,
        );

        expect(screen.getByRole('button', { name: 'Change status' })).toHaveAttribute('type', 'button');
        expect(screen.getByRole('button', { name: 'Save' })).toHaveAttribute('type', 'submit');
    });

    it('styles the outline variant without the outline utility class', () => {
        render(<Button variant="outline">Filters</Button>);

        const button = screen.getByRole('button', { name: 'Filters' });
        expect(button).toHaveClass('btn', 'btn-outline');
        expect(button).not.toHaveClass('outline');
    });

    it('shows an icon-only button name as its tooltip, and leaves labelled buttons alone', () => {
        render(<><Button aria-label="Close panel"><svg aria-hidden="true" /></Button><Button aria-label="Save draft">Save</Button></>);

        expect(screen.getByRole('button', { name: 'Close panel' })).toHaveAttribute('title', 'Close panel');
        expect(screen.getByRole('button', { name: 'Save draft' })).not.toHaveAttribute('title');
    });
});

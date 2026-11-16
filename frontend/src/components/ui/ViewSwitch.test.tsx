import { describe, expect, it } from 'vitest';
import { useState } from 'react';
import { screen } from '@testing-library/react';
import { renderWithProviders } from '../../test/renderWithProviders';
import { ViewSwitch } from './ViewSwitch';

const Harness = () => {
    const [view, setView] = useState<'list' | 'board' | 'calendar'>('list');
    return (
        <ViewSwitch
            label="Task view"
            value={view}
            onChange={setView}
            options={[
                { value: 'list', label: 'List' },
                { value: 'board', label: 'Board' },
                { value: 'calendar', label: 'Calendar' },
            ]}
        />
    );
};

describe('ViewSwitch', () => {
    it('exposes its options as a labelled group with pressed state', () => {
        renderWithProviders(<Harness />);

        const group = screen.getByRole('group', { name: 'Task view' });
        expect(group).toBeInTheDocument();
        expect(screen.getByRole('button', { name: 'List' })).toHaveAttribute('aria-pressed', 'true');
        expect(screen.getByRole('button', { name: 'Board' })).toHaveAttribute('aria-pressed', 'false');
    });

    it('moves to the next and previous view with the arrow keys and wraps at the ends', async () => {
        const { user } = renderWithProviders(<Harness />);

        await user.tab();
        expect(screen.getByRole('button', { name: 'List' })).toHaveFocus();

        await user.keyboard('{ArrowRight}');
        expect(screen.getByRole('button', { name: 'Board' })).toHaveFocus();
        expect(screen.getByRole('button', { name: 'Board' })).toHaveAttribute('aria-pressed', 'true');
        expect(screen.getByRole('button', { name: 'List' })).toHaveAttribute('aria-pressed', 'false');

        await user.keyboard('{ArrowLeft}{ArrowLeft}');
        expect(screen.getByRole('button', { name: 'Calendar' })).toHaveFocus();
        expect(screen.getByRole('button', { name: 'Calendar' })).toHaveAttribute('aria-pressed', 'true');

        await user.keyboard('{Home}');
        expect(screen.getByRole('button', { name: 'List' })).toHaveAttribute('aria-pressed', 'true');
    });

    it('keeps only the pressed view in the tab order', async () => {
        const { user } = renderWithProviders(<Harness />);

        await user.tab();
        await user.tab();
        expect(screen.getByRole('button', { name: 'List' })).not.toHaveFocus();
        expect(screen.getByRole('button', { name: 'Board' })).not.toHaveFocus();
    });
});

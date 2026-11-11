import { describe, expect, it, vi } from 'vitest';
import { screen } from '@testing-library/react';
import { renderWithProviders } from '../../test/renderWithProviders';
import { OverflowMenu } from './OverflowMenu';

describe('OverflowMenu', () => {
    it('moves through menu items with the keyboard and returns focus on Escape', async () => {
        const firstAction = vi.fn();
        const { user } = renderWithProviders(
            <OverflowMenu
                label="Item actions"
                items={[
                    { label: 'First action', onSelect: firstAction },
                    { label: 'Second action', onSelect: vi.fn() },
                ]}
            />,
        );

        const trigger = screen.getByRole('button', { name: 'Item actions' });
        await user.click(trigger);

        expect(screen.getByRole('menuitem', { name: 'First action' })).toHaveFocus();
        await user.keyboard('{ArrowDown}');
        expect(screen.getByRole('menuitem', { name: 'Second action' })).toHaveFocus();

        await user.keyboard('{Escape}');
        expect(screen.queryByRole('menu')).not.toBeInTheDocument();
        expect(trigger).toHaveFocus();
        expect(firstAction).not.toHaveBeenCalled();
    });

    it('keeps an unavailable action focusable so its recovery label can be read', async () => {
        const unavailableAction = vi.fn();
        const { user } = renderWithProviders(
            <OverflowMenu
                label="Calendar actions"
                items={[
                    {
                        label: 'Create another calendar before deleting this one',
                        onSelect: unavailableAction,
                        disabled: true,
                    },
                ]}
            />,
        );

        // A single action is a button, not a menu; unavailable, it stays focusable and inert.
        const action = screen.getByRole('button', {
            name: 'Create another calendar before deleting this one',
        });
        expect(action).toHaveAttribute('aria-disabled', 'true');
        action.focus();
        expect(action).toHaveFocus();

        await user.click(action);
        expect(unavailableAction).not.toHaveBeenCalled();
    });

    it('shows a single action as a labelled button instead of a menu', async () => {
        const remove = vi.fn();
        const { user } = renderWithProviders(<OverflowMenu label="Project actions" items={[{ label: 'Delete project', onSelect: remove, tone: 'danger' }]} />);

        expect(screen.queryByRole('button', { name: 'Project actions' })).not.toBeInTheDocument();
        await user.click(screen.getByRole('button', { name: 'Delete project' }));
        expect(remove).toHaveBeenCalledTimes(1);
    });
});

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

        await user.click(screen.getByRole('button', { name: 'Calendar actions' }));

        const menuItem = screen.getByRole('menuitem', {
            name: 'Create another calendar before deleting this one',
        });
        expect(menuItem).toHaveFocus();
        expect(menuItem).toHaveAttribute('aria-disabled', 'true');

        await user.click(menuItem);
        expect(unavailableAction).not.toHaveBeenCalled();
        expect(screen.getByRole('menu')).toBeVisible();
    });
});

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
});

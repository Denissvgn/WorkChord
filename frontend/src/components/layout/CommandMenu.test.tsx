import { beforeEach, describe, expect, it } from 'vitest';
import { screen, within } from '@testing-library/react';
import { useLocation } from 'react-router-dom';
import { renderWithProviders } from '../../test/renderWithProviders';
import { CommandMenu } from './CommandMenu';
import { SINGLE_KEY_SHORTCUTS_STORAGE_KEY } from '../../utils/singleKeyShortcutPreference';

const LocationProbe = () => {
    const location = useLocation();
    return <output data-testid="command-location">{`${location.pathname}${location.search}`}</output>;
};

describe('CommandMenu', () => {
    beforeEach(() => {
        window.localStorage.clear();
    });

    it('opens from the platform shortcut, filters commands, and navigates', async () => {
        const { user } = renderWithProviders(
            <>
                <CommandMenu />
                <LocationProbe />
            </>,
            { initialEntries: ['/tasks?view=12'] },
        );

        await user.keyboard('{Control>}k{/Control}');

        const dialog = screen.getByRole('dialog', { name: 'Command menu' });
        const search = within(dialog).getByRole('combobox', { name: 'Search commands' });
        await user.type(search, 'bulk');

        await user.click(within(dialog).getByRole('option', { name: /Bulk edit tasks/ }));

        expect(screen.queryByRole('dialog', { name: 'Command menu' })).not.toBeInTheDocument();
        expect(screen.getByTestId('command-location')).toHaveTextContent('/tasks?view=12&mode=bulk');
    });

    it('keeps single-key task shortcuts off until users opt in', async () => {
        const { user } = renderWithProviders(
            <>
                <CommandMenu />
                <LocationProbe />
            </>,
            { initialEntries: ['/tasks'] },
        );

        await user.keyboard('f');
        expect(screen.getByTestId('command-location')).toHaveTextContent('/tasks');

        await user.keyboard('{Control>}k{/Control}');
        const dialog = screen.getByRole('dialog', { name: 'Command menu' });
        expect(within(dialog).getByRole('checkbox', {
            name: 'Enable single-key task shortcuts',
        })).not.toBeChecked();
        const filterCommand = within(dialog).getByRole('option', {
            name: /Show task filters/,
        });
        expect(filterCommand).not.toHaveAttribute('aria-keyshortcuts');
        expect(filterCommand.querySelector('kbd')).not.toBeInTheDocument();
    });

    it('runs task shortcuts after an explicit stored opt-in', async () => {
        window.localStorage.setItem(SINGLE_KEY_SHORTCUTS_STORAGE_KEY, 'true');
        const { user } = renderWithProviders(
            <>
                <CommandMenu />
                <LocationProbe />
            </>,
            { initialEntries: ['/tasks'] },
        );

        await user.keyboard('f');
        expect(screen.getByTestId('command-location')).toHaveTextContent('/tasks?panel=filters');
    });

    it('lets users opt in and still ignores keys from controls', async () => {
        const { user } = renderWithProviders(
            <>
                <button type="button">Focused control</button>
                <div data-testid="neutral-target">Workspace canvas</div>
                <CommandMenu />
                <LocationProbe />
            </>,
            { initialEntries: ['/tasks'] },
        );

        await user.click(screen.getByRole('button', { name: 'Focused control' }));
        await user.keyboard('f');
        expect(screen.getByTestId('command-location')).toHaveTextContent('/tasks');

        await user.keyboard('{Control>}k{/Control}');
        const dialog = screen.getByRole('dialog', { name: 'Command menu' });
        const shortcutToggle = within(dialog).getByRole('checkbox', {
            name: 'Enable single-key task shortcuts',
        });
        expect(shortcutToggle).not.toBeChecked();
        await user.click(shortcutToggle);
        await user.keyboard('{Escape}');

        await user.click(screen.getByTestId('neutral-target'));
        await user.keyboard('f');
        expect(screen.getByTestId('command-location')).toHaveTextContent('/tasks?panel=filters');
        expect(window.localStorage.getItem(SINGLE_KEY_SHORTCUTS_STORAGE_KEY)).toBe('true');
    });

    it('does not run opted-in shortcuts while an application dialog is open', async () => {
        window.localStorage.setItem(SINGLE_KEY_SHORTCUTS_STORAGE_KEY, 'true');
        const { user } = renderWithProviders(
            <>
                <div role="dialog" aria-modal="true" aria-label="Protected workflow">
                    Protected workflow
                </div>
                <CommandMenu />
                <LocationProbe />
            </>,
            { initialEntries: ['/tasks'] },
        );

        await user.keyboard('f');
        expect(screen.getByTestId('command-location')).toHaveTextContent('/tasks');
    });

    it('exposes listbox navigation through the search combobox', async () => {
        const { user } = renderWithProviders(<CommandMenu />, { initialEntries: ['/tasks'] });

        await user.keyboard('{Control>}k{/Control}');
        const dialog = screen.getByRole('dialog', { name: 'Command menu' });
        const search = within(dialog).getByRole('combobox', { name: 'Search commands' });
        const options = within(dialog).getAllByRole('option');

        expect(within(dialog).getByRole('listbox', { name: 'Available commands' })).toBeVisible();
        expect(options[0]).toHaveAttribute('aria-selected', 'true');
        expect(search).toHaveAttribute('aria-activedescendant', options[0]?.id);

        await user.keyboard('{ArrowDown}');
        expect(options[1]).toHaveAttribute('aria-selected', 'true');
        expect(search).toHaveAttribute('aria-activedescendant', options[1]?.id);
    });

    it('reverses task layout and fullscreen commands from the current state', async () => {
        const { user } = renderWithProviders(
            <>
                <CommandMenu />
                <LocationProbe />
            </>,
            { initialEntries: ['/tasks?layout=board&fullscreen=1'] },
        );

        await user.keyboard('{Control>}k{/Control}');
        const dialog = screen.getByRole('dialog', { name: 'Command menu' });
        expect(within(dialog).getByRole('option', { name: /Open list view/ })).toBeVisible();

        await user.click(within(dialog).getByRole('option', { name: /Exit task focus mode/ }));
        expect(screen.getByTestId('command-location')).toHaveTextContent('/tasks?layout=board');
    });
});

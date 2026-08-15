import { beforeEach, describe, expect, it, vi } from 'vitest';
import { screen, within } from '@testing-library/react';
import { useLocation } from 'react-router-dom';
import { renderWithProviders } from '../../test/renderWithProviders';
import { CommandMenu, RECENT_COMMANDS_STORAGE_KEY } from './CommandMenu';
import { SINGLE_KEY_SHORTCUTS_STORAGE_KEY } from '../../utils/singleKeyShortcutPreference';

const LocationProbe = () => {
    const location = useLocation();
    return <output data-testid="command-location">{`${location.pathname}${location.search}`}</output>;
};

describe('CommandMenu', () => {
    beforeEach(() => {
        window.localStorage.clear();
        Element.prototype.scrollIntoView = vi.fn();
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

    it('opens with one contextual action and three relevant suggestions', async () => {
        const { user } = renderWithProviders(<CommandMenu />, { initialEntries: ['/settings'] });

        await user.keyboard('{Control>}k{/Control}');
        const dialog = screen.getByRole('dialog', { name: 'Command menu' });
        const options = within(dialog).getAllByRole('option');

        expect(options.map(option => option.textContent)).toEqual([
            expect.stringContaining('Open Resource & Settings home'),
            expect.stringContaining('Open Tasks'),
            expect.stringContaining('Open Gantt'),
            expect.stringContaining('Open Plan Work'),
        ]);
        expect(within(dialog).getAllByRole('heading', { level: 3 }).map(heading => heading.textContent))
            .toEqual(['Current workspace', 'Recent & relevant']);
        expect(within(dialog).getByText(
            'Showing what matters here and your recent commands.',
        )).toBeVisible();
    });

    it('keeps the complete catalog behind an explicit control', async () => {
        const { user } = renderWithProviders(<CommandMenu />, { initialEntries: ['/settings'] });

        await user.keyboard('{Control>}k{/Control}');
        const dialog = screen.getByRole('dialog', { name: 'Command menu' });
        expect(within(dialog).getAllByRole('option')).toHaveLength(4);

        await user.click(within(dialog).getByRole('button', { name: 'All commands' }));

        expect(within(dialog).getAllByRole('option')).toHaveLength(12);
        expect(within(dialog).getAllByRole('heading', { level: 3 }).map(heading => heading.textContent))
            .toEqual(['Current workspace', 'Go to', 'Task actions']);
        expect(within(dialog).getByRole('button', { name: 'Suggested commands' }))
            .toBeVisible();
    });

    it('keeps stable global destinations searchable beneath workspace context', async () => {
        const { user } = renderWithProviders(<CommandMenu />, { initialEntries: ['/plan'] });

        await user.keyboard('{Control>}k{/Control}');
        const dialog = screen.getByRole('dialog', { name: 'Command menu' });
        const search = within(dialog).getByRole('combobox', { name: 'Search commands' });
        await user.type(search, 'Plan Work');

        expect(within(dialog).getByRole('option', { name: /Continue Plan Work/ })).toBeVisible();
        expect(within(dialog).queryByRole('option', { name: /Open Plan Work/ }))
            .not.toBeInTheDocument();
    });

    it('turns the planning-home context into a productive default action', async () => {
        const { user } = renderWithProviders(
            <>
                <CommandMenu />
                <LocationProbe />
            </>,
            { initialEntries: ['/plan'] },
        );

        await user.keyboard('{Control>}k{/Control}');
        const dialog = screen.getByRole('dialog', { name: 'Command menu' });
        expect(within(dialog).getAllByRole('option')[0])
            .toHaveAccessibleName(/Continue Plan Work/);

        await user.keyboard('{Enter}');
        expect(screen.getByTestId('command-location')).toHaveTextContent('/plan/master');
    });

    it('keeps visual and keyboard command order aligned outside Tasks', async () => {
        const { user } = renderWithProviders(
            <>
                <CommandMenu />
                <LocationProbe />
            </>,
            { initialEntries: ['/settings'] },
        );

        await user.keyboard('{Control>}k{/Control}');
        const dialog = screen.getByRole('dialog', { name: 'Command menu' });
        const search = within(dialog).getByRole('combobox', { name: 'Search commands' });
        const options = within(dialog).getAllByRole('option');

        expect(options[0]).toHaveAttribute('aria-selected', 'true');
        expect(search).toHaveAttribute('aria-activedescendant', options[0]?.id);

        await user.keyboard('{ArrowDown}{Enter}');

        expect(screen.getByTestId('command-location')).toHaveTextContent('/tasks');
    });

    it('keeps the active keyboard command in view', async () => {
        const { user } = renderWithProviders(<CommandMenu />, { initialEntries: ['/tasks'] });

        await user.keyboard('{Control>}k{/Control}');
        await user.click(screen.getByRole('button', { name: 'All commands' }));
        await user.keyboard('{ArrowDown}{ArrowDown}{ArrowDown}{ArrowDown}{ArrowDown}{ArrowDown}{ArrowDown}');

        const activeOption = screen.getAllByRole('option')
            .find(option => option.getAttribute('aria-selected') === 'true');
        const scrollIntoView = Element.prototype.scrollIntoView as ReturnType<typeof vi.fn>;

        expect(activeOption).toBeDefined();
        expect(scrollIntoView).toHaveBeenLastCalledWith({ block: 'nearest' });
        expect(scrollIntoView.mock.contexts.at(-1)).toBe(activeOption);
    });

    it('opens the stable Plan Work launcher instead of skipping to Plan Master', async () => {
        const { user } = renderWithProviders(
            <>
                <CommandMenu />
                <LocationProbe />
            </>,
            { initialEntries: ['/settings'] },
        );

        await user.keyboard('{Control>}k{/Control}');
        const dialog = screen.getByRole('dialog', { name: 'Command menu' });
        await user.click(within(dialog).getByRole('option', { name: /Open Plan Work/ }));

        expect(screen.getByTestId('command-location')).toHaveTextContent('/plan');
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
        await user.click(within(dialog).getByRole('button', { name: 'All commands' }));
        expect(within(dialog).getByRole('option', { name: /Open list view/ })).toBeVisible();

        await user.click(within(dialog).getByRole('option', { name: /Exit task focus mode/ }));
        expect(screen.getByTestId('command-location')).toHaveTextContent('/tasks?layout=board');
    });

    it('treats nested task routes as part of the Tasks workspace', async () => {
        window.localStorage.setItem(SINGLE_KEY_SHORTCUTS_STORAGE_KEY, 'true');
        const { user } = renderWithProviders(
            <>
                <CommandMenu />
                <LocationProbe />
            </>,
            { initialEntries: ['/tasks/assigned'] },
        );

        await user.keyboard('f');
        expect(screen.getByTestId('command-location')).toHaveTextContent('/tasks?panel=filters');
    });

    it('promotes recently used commands on the next open', async () => {
        const firstRender = renderWithProviders(
            <>
                <CommandMenu />
                <LocationProbe />
            </>,
            { initialEntries: ['/settings'] },
        );

        await firstRender.user.keyboard('{Control>}k{/Control}');
        let dialog = screen.getByRole('dialog', { name: 'Command menu' });
        await firstRender.user.click(within(dialog).getByRole('button', { name: 'All commands' }));
        await firstRender.user.click(within(dialog).getByRole('option', { name: /Open Gantt/ }));
        expect(screen.getByTestId('command-location')).toHaveTextContent('/gantt');
        expect(window.localStorage.getItem(RECENT_COMMANDS_STORAGE_KEY))
            .toBe(JSON.stringify(['gantt']));

        firstRender.unmount();
        const secondRender = renderWithProviders(<CommandMenu />, {
            initialEntries: ['/settings'],
        });
        await secondRender.user.keyboard('{Control>}k{/Control}');
        dialog = screen.getByRole('dialog', { name: 'Command menu' });

        expect(within(dialog).getAllByRole('option')[1])
            .toHaveAccessibleName(/Open Gantt/);
    });
});

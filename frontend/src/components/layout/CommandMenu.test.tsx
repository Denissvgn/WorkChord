import { beforeEach, describe, expect, it, vi } from 'vitest';
import { screen, within } from '@testing-library/react';
import { useLocation } from 'react-router-dom';
import { renderWithProviders } from '../../test/renderWithProviders';
import { CommandMenu, RECENT_COMMANDS_STORAGE_KEY } from './CommandMenu';
import { SINGLE_KEY_SHORTCUTS_STORAGE_KEY } from '../../utils/singleKeyShortcutPreference';
import { useWorkScope } from '../../features/scope/useWorkScope';
import { useScopeStore } from '../../features/scope/scopeStore';
import { DESTINATIONS, DESTINATION_VIEWS } from '../../navigation/destinations';
import i18n from '../../i18n/i18n';

const lookup = vi.hoisted(() => vi.fn());
vi.mock('../../services/taskService', () => ({ taskService: { lookup } }));
const projects = vi.hoisted(() => vi.fn());
vi.mock('../../services/projectService', () => ({ projectService: { getAll: projects } }));
const savedViews = vi.hoisted(() => vi.fn());
vi.mock('../../services/savedViewService', () => ({ savedViewService: { getAll: savedViews } }));

const iterations = vi.hoisted(() => vi.fn());
vi.mock('../../services/iterationService', () => ({ iterationService: { getAll: iterations } }));

const ScopeProbe = () => {
    const scope = useWorkScope();
    return <output data-testid="shared-scope">{scope.project}/{scope.iteration}</output>;
};

const LocationProbe = () => {
    const location = useLocation();
    return <output data-testid="command-location">{`${location.pathname}${location.search}`}</output>;
};

describe('CommandMenu', () => {
    beforeEach(() => {
        window.localStorage.clear();
        useScopeStore.setState({ project: null, iteration: null });
        iterations.mockReset();
        iterations.mockResolvedValue([]);
        lookup.mockReset();
        lookup.mockResolvedValue({ items: [], has_more: false });
        projects.mockReset();
        projects.mockResolvedValue([]);
        savedViews.mockReset();
        savedViews.mockResolvedValue([]);
        Element.prototype.scrollIntoView = vi.fn();
    });

    it.each([...DESTINATIONS, ...DESTINATION_VIEWS])('opens $defaultLabel by typing its name', async destination => {
        const { user } = renderWithProviders(<><CommandMenu /><LocationProbe /></>, { initialEntries: ['/settings'] });
        await user.keyboard('{Control>}k{/Control}');
        await user.type(screen.getByRole('combobox', { name: 'Search commands' }), i18n.t(destination.labelKey, destination.defaultLabel));
        const options = screen.getAllByRole('option');
        const target = options.find(option => option.textContent?.includes(i18n.t(destination.labelKey, destination.defaultLabel)));
        expect(target).toBeDefined();
        await user.click(target!);
        expect(screen.getByTestId('command-location').textContent).toBe(destination.path);
    });

    it.each(['#42', 'Repair'])('finds tasks outside the current project by %s with their project names', async query => {
        lookup.mockResolvedValue({ items: [
            { id: 42, title: 'Repair endpoint', status: 'active', project_id: 2, project_name: 'Orchard', iteration_name: null },
            { id: 43, title: 'Repair dashboard', status: 'planned', project_id: 3, project_name: 'Harbour', iteration_name: null },
        ], has_more: false });
        const { user } = renderWithProviders(<CommandMenu />, { initialEntries: ['/tasks?project=1&iteration=backlog'] });
        await user.keyboard('{Control>}k{/Control}');
        await user.type(screen.getByRole('combobox', { name: 'Search commands' }), query);
        expect(await screen.findByRole('option', { name: /#42 · Repair endpoint.*Orchard/ })).toBeVisible();
        expect(screen.getByRole('option', { name: /#43 · Repair dashboard.*Harbour/ })).toBeVisible();
        expect(lookup).toHaveBeenLastCalledWith({ q: query, limit: 8 });
    });

    it('switches iteration in the shared scope without leaving the page', async () => {
        iterations.mockResolvedValue([
            { id: 11, name: 'November', project_id: 1, start_date: '2026-11-01', end_date: '2026-11-30' },
            { id: 12, name: 'December', project_id: 1, start_date: '2026-12-01', end_date: '2026-12-31' },
            { id: 21, name: 'Other project iteration', project_id: 2, start_date: '2026-11-01', end_date: '2026-11-30' },
        ]);
        const { user } = renderWithProviders(<><CommandMenu /><ScopeProbe /><LocationProbe /></>, { initialEntries: ['/tasks?project=1&iteration=11&layout=board'] });
        await user.keyboard('{Control>}k{/Control}');
        await user.type(screen.getByRole('combobox', { name: 'Search commands' }), 'Switch iteration');
        await user.click(screen.getByRole('option', { name: /Switch iteration/ }));
        expect(screen.queryByRole('option', { name: /Other project iteration/ })).not.toBeInTheDocument();
        await user.click(await screen.findByRole('option', { name: /December/ }));
        expect(screen.getByTestId('shared-scope')).toHaveTextContent('1/12');
        expect(screen.getByTestId('command-location')).toHaveTextContent('/tasks?project=1&iteration=12&layout=board');
        expect(useScopeStore.getState()).toMatchObject({ project: 1, iteration: 12 });
        await user.keyboard('{Control>}k{/Control}');
        await user.type(screen.getByRole('combobox', { name: 'Search commands' }), 'Switch iteration');
        await user.click(screen.getByRole('option', { name: /Switch iteration/ }));
        await user.click(screen.getByRole('option', { name: /Backlog/ }));
        expect(screen.getByTestId('shared-scope')).toHaveTextContent('1/backlog');
    });

    it('switches project and offers All projects without leaving the page', async () => {
        projects.mockResolvedValue([{ id: 2, name: 'Orchard' }]);
        const { user } = renderWithProviders(<><CommandMenu /><ScopeProbe /><LocationProbe /></>, { initialEntries: ['/tasks?project=1&iteration=backlog&layout=board'] });
        await user.keyboard('{Control>}k{/Control}');
        await user.type(screen.getByRole('combobox', { name: 'Search commands' }), 'Switch project');
        await user.click(screen.getByRole('option', { name: /Switch project/ }));
        expect(screen.getByRole('option', { name: 'All projects' })).toBeVisible();
        await user.click(await screen.findByRole('option', { name: 'Orchard' }));
        expect(screen.getByTestId('shared-scope')).toHaveTextContent('2/backlog');
        expect(screen.getByTestId('command-location')).toHaveTextContent('/tasks?project=2&iteration=backlog&layout=board');
    });

    it('finds projects and saved views and opens them', async () => {
        projects.mockResolvedValue([{ id: 7, name: 'Orchard rollout' }]);
        savedViews.mockImplementation(async ({ view_type }: { view_type: string }) => view_type === 'tasks'
            ? [{ id: 31, name: 'Orchard blockers', view_type: 'tasks', scope: 'personal' }] : []);
        const { user } = renderWithProviders(<><CommandMenu /><LocationProbe /></>, { initialEntries: ['/'] });
        await user.keyboard('{Control>}k{/Control}');
        await user.type(screen.getByRole('combobox', { name: 'Search commands' }), 'orchard');
        expect(await screen.findByRole('option', { name: /Orchard rollout/ })).toBeInTheDocument();
        await user.click(await screen.findByRole('option', { name: /Orchard blockers/ }));
        expect(screen.getByTestId('command-location')).toHaveTextContent('/tasks?view=31');
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

    it('opens an authorized task result by keyboard separately from commands', async () => {
        lookup.mockResolvedValue({ items: [{ id: 42, title: 'Repair endpoint', status: 'active', project_name: 'Delivery', iteration_name: null }], has_more: false });
        const { user } = renderWithProviders(<><CommandMenu /><LocationProbe /></>, { initialEntries: ['/tasks?view=12'] });
        await user.keyboard('{Control>}k{/Control}');
        await user.type(screen.getByRole('combobox', { name: 'Search commands' }), '#42');
        await screen.findByRole('option', { name: /Repair endpoint/ });
        expect(screen.getByRole('group', { name: 'Search results' })).toBeInTheDocument();
        await user.keyboard('{Enter}');
        expect(screen.getByTestId('command-location')).toHaveTextContent('/tasks?view=12&task=42');
    });

    it('runs single-key task shortcuts by default and shows their keys', async () => {
        const { user } = renderWithProviders(
            <>
                <CommandMenu />
                <LocationProbe />
            </>,
            { initialEntries: ['/tasks'] },
        );

        await user.keyboard('{Control>}k{/Control}');
        const dialog = screen.getByRole('dialog', { name: 'Command menu' });
        expect(within(dialog).getByRole('checkbox', {
            name: 'Single-key task shortcuts',
        })).toBeChecked();
        const filterCommand = within(dialog).getByRole('option', {
            name: /Show task filters/,
        });
        expect(filterCommand).toHaveAttribute('aria-keyshortcuts', 'F');
        expect(filterCommand.querySelector('kbd')).toHaveTextContent('F');
        await user.keyboard('{Escape}');

        await user.keyboard('f');
        expect(screen.getByTestId('command-location')).toHaveTextContent('/tasks?panel=filters');
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

    it('lets users turn shortcuts off and ignores keys from controls', async () => {
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
            name: 'Single-key task shortcuts',
        });
        expect(shortcutToggle).toBeChecked();
        await user.click(shortcutToggle);
        await user.keyboard('{Escape}');

        await user.click(screen.getByTestId('neutral-target'));
        await user.keyboard('f');
        expect(screen.getByTestId('command-location')).toHaveTextContent('/tasks');
        expect(screen.getByTestId('command-location')).not.toHaveTextContent('panel=filters');
        expect(window.localStorage.getItem(SINGLE_KEY_SHORTCUTS_STORAGE_KEY)).toBe('false');
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
            expect.stringContaining('Open Plan'),
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

        // Every registry destination except the workspace home already offered above, plus seven task actions and two scope commands.
        expect(within(dialog).getAllByRole('option')).toHaveLength(24);
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
        await user.type(search, 'Plan');

        expect(within(dialog).getByRole('option', { name: /Open Plan/ })).toBeVisible();
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
            .toHaveAccessibleName(/Continue Plan/);

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

    it('opens the stable Plan launcher instead of skipping to Plan Master', async () => {
        const { user } = renderWithProviders(
            <>
                <CommandMenu />
                <LocationProbe />
            </>,
            { initialEntries: ['/settings'] },
        );

        await user.keyboard('{Control>}k{/Control}');
        const dialog = screen.getByRole('dialog', { name: 'Command menu' });
        await user.click(within(dialog).getByRole('option', { name: /Open Plan/ }));

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

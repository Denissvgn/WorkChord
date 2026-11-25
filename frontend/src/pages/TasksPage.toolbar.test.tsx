import { readFileSync } from 'node:fs';
import { resolve } from 'node:path';
import { compile, optimize } from '@tailwindcss/node';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { cleanup, fireEvent, screen, waitFor, within } from '@testing-library/react';
import { useLocation } from 'react-router-dom';
import { renderWithProviders } from '../test/renderWithProviders';
import { expectPageChrome } from '../test/pageChrome';
import type { SavedView } from '../types/savedView';
import type { Task } from '../types/task';
import TasksPage from './TasksPage';
import i18n from '../i18n/i18n';

const workScopeMock = vi.hoisted(() => ({ iteration: 1 as number | 'backlog', setIteration: vi.fn() }));
const iterationServiceMock = vi.hoisted(() => ({ getAll: vi.fn(), getById: vi.fn() }));
const taskServiceMock = vi.hoisted(() => ({ getByIteration: vi.fn(), getById: vi.fn() }));
const savedViewServiceMock = vi.hoisted(() => ({ getAll: vi.fn(), create: vi.fn(), update: vi.fn(), delete: vi.fn() }));

vi.mock('../features/scope/useWorkScope', () => ({
    useWorkScope: () => workScopeMock,
    useSetWorkScope: () => ({ setProject: vi.fn(), setIteration: vi.fn(), setScope: vi.fn() }),
}));
vi.mock('../services/iterationService', () => ({ iterationService: iterationServiceMock }));
vi.mock('../services/taskService', () => ({ taskService: taskServiceMock }));
vi.mock('../services/savedViewService', () => ({ savedViewService: savedViewServiceMock }));
vi.mock('../services/sessionService', () => ({ sessionService: { getWhoAmI: vi.fn().mockResolvedValue({ id: 3, principal_id: null }) } }));
vi.mock('../services/labelService', () => ({ labelService: { getGroups: vi.fn().mockResolvedValue([]) } }));
vi.mock('../services/projectService', () => ({ projectService: { getAll: vi.fn().mockResolvedValue([]), getRoadmapMilestones: vi.fn().mockResolvedValue({ items: [], next_cursor: null }) } }));
vi.mock('../services/teamService', () => ({ teamService: { getByIteration: vi.fn().mockResolvedValue([{ id: 7, name: 'Ana' }]) } }));
vi.mock('../components/tasks/TaskAgentReadinessBadge', () => ({ TaskAgentReadinessBadge: () => null }));

const css = readFileSync(resolve(__dirname, '../styles/planning-masters.css'), 'utf8');

const ana = { id: 7, name: 'Ana' } as Task['assignee'];

const task = (id: number, title: string, overrides: Partial<Task> = {}): Task => ({
    id,
    iteration_id: 1,
    project_id: null,
    milestone_id: null,
    parent_id: null,
    title,
    description: '',
    priority: id,
    effort_days: 1,
    effort_hours: 8,
    project: null,
    milestone: null,
    assignee: null,
    status: 'planned',
    start_date: null,
    end_date: null,
    actual_start_date: null,
    actual_end_date: null,
    min_start_date: null,
    max_end_date: null,
    is_overdue: false,
    is_delayed: false,
    is_composite: false,
    is_optional: false,
    is_deferred: false,
    tags: [],
    sort_order: id,
    external_links: [],
    request_count: 0,
    agent_readiness: { is_ready: true, blockers: [], warnings: [], criteria: [] },
    version: 1,
    children: [],
    dependencies: [],
    ...overrides,
});

const TASKS = [
    task(1, 'Write launch notes'),
    task(2, 'Fix login bug', { assignee: ana, status: 'active' }),
    task(3, 'Ship release build', { assignee: ana }),
];

const anaPlannedView: SavedView = {
    id: 12,
    name: 'Ana planned',
    description: null,
    seed_key: null,
    view_type: 'tasks',
    scope: 'personal',
    filters_json: { assigneeId: 7, status: 'planned' },
    sort_json: { sortKey: 'priority' },
    columns_json: {},
    created_by_session_id: 3,
    owner_principal_id: null,
    schema_version: 1,
    is_valid: true,
    invalid_reason: null,
    created_at: '2026-11-01T00:00:00Z',
    updated_at: '2026-11-01T00:00:00Z',
};

const LocationProbe = () => <output data-testid="location-search">{useLocation().search}</output>;

const taskTitles = () => screen.queryAllByRole('button', { name: /^(Write launch notes|Fix login bug|Ship release build)$/ })
    .map(button => button.textContent);

describe('Tasks header and toolbar', () => {
    beforeEach(() => {
        workScopeMock.iteration = 1;
        iterationServiceMock.getAll.mockResolvedValue([{ id: 1, name: 'Iteration one', start_date: '2026-11-01', end_date: '2026-11-30' }]);
        taskServiceMock.getByIteration.mockResolvedValue(TASKS);
        savedViewServiceMock.getAll.mockResolvedValue([anaPlannedView]);
        savedViewServiceMock.create.mockReset();
        savedViewServiceMock.update.mockReset();
        savedViewServiceMock.delete.mockReset();
    });

    it('passes the page chrome check with one header, one toolbar and quick add as the first list row', async () => {
        const { container } = renderWithProviders(<TasksPage />, { initialEntries: ['/tasks'] });
        expect(await screen.findByRole('button', { name: 'Write launch notes' })).toBeInTheDocument();

        expectPageChrome(container);
        expect(screen.getByRole('heading', { level: 1, name: 'All tasks' })).toBeInTheDocument();
        expect(screen.getAllByTestId('page-toolbar')).toHaveLength(1);
        const toolbar = screen.getByTestId('page-toolbar');
        expect(within(toolbar).getByRole('searchbox', { name: 'Search this list' })).toBeInTheDocument();
        expect(within(toolbar).getByTestId('filter-bar')).toBeInTheDocument();
        expect(within(toolbar).getByRole('group', { name: 'Task layout' })).toHaveTextContent('ListBoardPipeline');
        expect(within(toolbar).getByRole('button', { name: 'View options' })).toBeInTheDocument();
        // The removed rows: cross-project search, the Backlog link, the view bar, Select and Merge.
        expect(screen.queryByRole('link', { name: 'Project backlog' })).not.toBeInTheDocument();
        expect(screen.queryByText('No active filters')).not.toBeInTheDocument();
        for (const name of ['Select', 'Merge tasks', 'Filters']) {
            expect(screen.queryByRole('button', { name })).not.toBeInTheDocument();
        }
        const quickAdd = screen.getByRole('form', { name: 'Quick add a task' });
        const firstTask = screen.getByRole('button', { name: 'Write launch notes' });
        expect(quickAdd.compareDocumentPosition(firstTask) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
    });

    it('keeps search, the five quick filters, More filters and the view controls on one row at 1024px and 1440px', async () => {
        renderWithProviders(<TasksPage />, { initialEntries: ['/tasks'] });
        expect(await screen.findByRole('button', { name: 'Write launch notes' })).toBeInTheDocument();

        const toolbar = screen.getByTestId('page-toolbar');
        expect(screen.getAllByTestId('page-toolbar')).toHaveLength(1);
        // The compact arrangement is the one that keeps a single row.
        expect(toolbar).toHaveClass('is-compact');
        const quickFilters = within(screen.getByTestId('filter-bar')).getAllByRole('combobox').map(control => control.getAttribute('aria-label'));
        expect(quickFilters).toEqual(['Assignee', 'Status', 'Label', 'Milestone', 'Needs attention']);
        const moreFilters = within(toolbar).getByRole('button', { name: /More filters/ });
        // View options is an icon button: it keeps its name and a tooltip, and shows no text of its own.
        const viewOptions = within(toolbar).getByRole('button', { name: 'View options' });
        expect(viewOptions).toHaveAttribute('title', 'View options');
        expect(viewOptions.textContent).toBe('');
        const layoutLabels = ['List', 'Board', 'Pipeline'];
        expect(within(toolbar).getByRole('group', { name: 'Task layout' })).toHaveTextContent(layoutLabels.join(''));

        // The layout rules that keep it on one row: filter controls do not wrap, search can shrink and grow,
        // quick filters size to their text, and the row only breaks below 900px of content.
        const rule = (selector: string) => new RegExp(`${selector.replace(/[.>]/g, '\\$&')} \\{([^}]*)\\}`).exec(css)?.[1] ?? '';
        const search = rule('.wc .wc-page-toolbar.is-compact .wc-page-toolbar-search');
        expect(search).toMatch(/flex: 1 1 (\d+)px/);
        const searchMin = Number(/min-width: (\d+)px/.exec(search)?.[1]);
        expect(searchMin).toBeLessThanOrEqual(140);
        expect(rule('.wc .wc-page-toolbar.is-compact .wc-filter-controls')).toContain('flex-wrap: nowrap');
        const select = rule('.wc .wc-page-toolbar.is-compact .wc-filter-controls > .wc-filter-select');
        expect(select).toContain('field-sizing: content');
        const breakpoint = Number(/@container \(max-width: (\d+)px\)\s*\{\s*\.wc \.wc-page-toolbar\.is-compact \.wc-page-toolbar-search/.exec(css)?.[1]);
        expect(breakpoint).toBeLessThanOrEqual(900);

        // Width budget from the real labels (about 7px a character in the interface font, close to what Chrome
        // measures) plus the padding the rules above give each control. Everything but search has to leave search
        // its minimum width inside the 992px a 1024px viewport leaves, with the icons of the view switch hidden.
        const glyph = 7;
        const text = (label: string) => label.length * glyph;
        const selectChrome = 8 + 22 + 2;
        const quick = quickFilters.reduce((sum, label) => sum + text(label ?? '') + selectChrome, 0);
        const more = text('More filters') + 10 * 2 + 2 + 4 + 16;
        const controls = quick + more + 5 * 6;
        const viewSwitch = layoutLabels.reduce((sum, label) => sum + text(label) + 8 * 2 + 2, 0) + 6;
        const end = viewSwitch + 6 + 34;
        const toolbarWidth = 1024 - 32;
        expect(moreFilters).toBeInTheDocument();
        expect(controls + end + 2 * 12 + searchMin).toBeLessThanOrEqual(toolbarWidth);
        expect(controls + end + 2 * 12 + searchMin).toBeLessThanOrEqual(1440 - 220 - 32);
    });

    it('shows a saved view as chips; removing one marks the view as changed and offers Save changes', async () => {
        savedViewServiceMock.update.mockResolvedValue({ ...anaPlannedView, filters_json: { assigneeId: 7 } });
        const { user } = renderWithProviders(<><TasksPage /><LocationProbe /></>, { initialEntries: ['/tasks?view=12'] });

        expect(await screen.findByRole('heading', { level: 1, name: 'Ana planned' })).toBeInTheDocument();
        const chips = await screen.findByRole('list', { name: 'Active filters' });
        await waitFor(() => expect(within(chips).getByText('Assignee: Ana')).toBeInTheDocument());
        expect(within(chips).getByText('Status: Planned')).toBeInTheDocument();
        await waitFor(() => expect(taskTitles()).toEqual(['Ship release build']));
        expect(screen.queryByText('Modified view')).not.toBeInTheDocument();
        expect(screen.queryByRole('button', { name: 'Save changes' })).not.toBeInTheDocument();

        await user.click(within(chips).getByRole('button', { name: 'Remove filter Status: Planned' }));

        expect(await screen.findByText('Modified view')).toBeInTheDocument();
        expect(taskTitles()).toEqual(['Fix login bug', 'Ship release build']);
        expect(screen.getByTestId('location-search')).toHaveTextContent('view=12');
        expect(screen.getByTestId('location-search')).not.toHaveTextContent('status=');
        const saveChanges = screen.getByRole('button', { name: 'Save changes' });

        await user.click(screen.getByRole('button', { name: 'Ana planned' }));
        expect(screen.getByRole('menuitem', { name: 'Save changes' })).not.toHaveAttribute('aria-disabled');
        await user.keyboard('{Escape}');

        await user.click(saveChanges);
        expect(savedViewServiceMock.update).toHaveBeenCalledWith(12, expect.objectContaining({
            filters_json: expect.objectContaining({ assigneeId: 7, status: null }),
        }));
    });

    it('keeps a saved view emptied of every condition after a reload and in a shared link', async () => {
        const first = renderWithProviders(<><TasksPage /><LocationProbe /></>, { initialEntries: ['/tasks?view=12'] });
        const chips = await screen.findByRole('list', { name: 'Active filters' });
        await waitFor(() => expect(within(chips).getByText('Status: Planned')).toBeInTheDocument());

        await first.user.click(within(chips).getByRole('button', { name: 'Remove filter Status: Planned' }));
        await first.user.click(within(screen.getByRole('list', { name: 'Active filters' })).getByRole('button', { name: 'Remove filter Assignee: Ana' }));

        expect(await screen.findByText('Modified view')).toBeInTheDocument();
        expect(screen.queryByRole('list', { name: 'Active filters' })).not.toBeInTheDocument();
        expect(screen.getByTestId('location-search')).toHaveTextContent(/^\?view=12&filters=none$/);
        const emptiedLink = `/tasks${screen.getByTestId('location-search').textContent}`;
        first.unmount();

        // A reload, or the same link opened by someone else, shows the emptied view, not the saved conditions.
        const { user } = renderWithProviders(<><TasksPage /><LocationProbe /></>, { initialEntries: [emptiedLink] });
        expect(await screen.findByRole('heading', { level: 1, name: 'Ana planned' })).toBeInTheDocument();
        await waitFor(() => expect(taskTitles()).toHaveLength(TASKS.length));
        expect(screen.queryByRole('list', { name: 'Active filters' })).not.toBeInTheDocument();
        expect(screen.getByText('Modified view')).toBeInTheDocument();
        expect(screen.getByRole('button', { name: 'Save changes' })).toBeInTheDocument();
        expect(screen.getByTestId('location-search')).toHaveTextContent(/^\?view=12&filters=none$/);

        // Adding a condition again drops the mark; the URL names the condition instead.
        await user.selectOptions(screen.getByRole('combobox', { name: 'Status' }), 'Active');
        await waitFor(() => expect(screen.getByTestId('location-search')).toHaveTextContent('status=active'));
        expect(screen.getByTestId('location-search')).not.toHaveTextContent('filters=none');
    });

    it('reopens both saved quick filters from the saved view response', async () => {
        const view = {
            ...anaPlannedView,
            filters_json: { assigneeId: 7, status: 'planned', milestoneId: 5, needsAttention: true },
        };
        savedViewServiceMock.getAll.mockResolvedValue([view]);

        const { user } = renderWithProviders(<TasksPage />, { initialEntries: ['/tasks'] });
        await user.click(await screen.findByRole('button', { name: 'All tasks' }));
        await user.click(await screen.findByRole('menuitemradio', { name: /Ana planned/ }));

        const chips = await screen.findByRole('list', { name: 'Active filters' });
        expect(await within(chips).findByText('Milestone: #5')).toBeInTheDocument();
        expect(within(chips).getByText('Needs attention: Yes')).toBeInTheDocument();
        expect(screen.queryByText('Modified view')).not.toBeInTheDocument();
    });

    it('shows a failed Save changes next to the Modified view notice', async () => {
        savedViewServiceMock.update.mockRejectedValue({ response: { status: 409, data: { detail: 'The view changed elsewhere' } } });
        const { user } = renderWithProviders(<TasksPage />, { initialEntries: ['/tasks?view=12'] });
        const chips = await screen.findByRole('list', { name: 'Active filters' });
        await waitFor(() => expect(within(chips).getByText('Status: Planned')).toBeInTheDocument());
        await user.click(within(chips).getByRole('button', { name: 'Remove filter Status: Planned' }));

        await user.click(await screen.findByRole('button', { name: 'Save changes' }));

        // The failed save leaves the view modified; both the notice and the failure are shown.
        expect(await screen.findByRole('alert')).toHaveTextContent('The view changed elsewhere');
        expect(screen.getByText('Modified view')).toBeInTheDocument();
        expect(screen.getByRole('button', { name: 'Save changes' })).toBeEnabled();

        savedViewServiceMock.update.mockResolvedValue({ ...anaPlannedView, filters_json: { assigneeId: 7 } });
        await user.click(screen.getByRole('button', { name: 'Save changes' }));
        await waitFor(() => expect(screen.queryByRole('alert')).not.toBeInTheDocument());
    });

    it('keeps a failed delete inside the open confirmation, also while the view is modified', async () => {
        savedViewServiceMock.delete.mockRejectedValue({ response: { status: 409, data: { detail: 'The view is in use' } } });
        const { user } = renderWithProviders(<><TasksPage /><LocationProbe /></>, { initialEntries: ['/tasks?view=12'] });
        const chips = await screen.findByRole('list', { name: 'Active filters' });
        await waitFor(() => expect(within(chips).getByText('Status: Planned')).toBeInTheDocument());
        await user.click(within(chips).getByRole('button', { name: 'Remove filter Status: Planned' }));
        expect(await screen.findByText('Modified view')).toBeInTheDocument();

        await user.click(screen.getByRole('button', { name: 'Ana planned' }));
        await user.click(await screen.findByRole('menuitem', { name: 'Delete' }));
        const dialog = await screen.findByRole('dialog', { name: 'Delete' });
        await user.click(within(dialog).getByRole('button', { name: 'Delete' }));

        expect(await within(dialog).findByRole('alert')).toHaveTextContent('The view is in use');
        expect(savedViewServiceMock.delete.mock.calls[0]?.[0]).toBe(12);
        expect(screen.getByTestId('location-search')).toHaveTextContent('view=12');

        await user.click(within(dialog).getByRole('button', { name: 'Cancel' }));
        await waitFor(() => expect(screen.queryByRole('dialog', { name: 'Delete' })).not.toBeInTheDocument());
        expect(screen.getByText('Modified view')).toBeInTheDocument();
    });

    it('clears the search as well as the filters when the empty list offers Clear filters', async () => {
        const { user } = renderWithProviders(<><TasksPage /><LocationProbe /></>, { initialEntries: ['/tasks?view=12&q=login'] });
        expect(await screen.findByRole('heading', { level: 1, name: 'Ana planned' })).toBeInTheDocument();
        expect(await screen.findByRole('heading', { level: 2, name: 'Nothing matches the filters' })).toBeInTheDocument();
        expect(taskTitles()).toEqual([]);

        await user.click(screen.getByRole('button', { name: 'Clear filters' }));

        await waitFor(() => expect(taskTitles()).toHaveLength(TASKS.length));
        expect(screen.getByRole('heading', { level: 1, name: 'All tasks' })).toBeInTheDocument();
        expect(screen.getByRole('searchbox', { name: 'Search this list' })).toHaveValue('');
        expect(screen.queryByRole('list', { name: 'Active filters' })).not.toBeInTheDocument();
        expect(screen.getByTestId('location-search')).toHaveTextContent(/^$/);
    });

    it('clears an unmatched search alone from the empty list', async () => {
        const { user } = renderWithProviders(<><TasksPage /><LocationProbe /></>, { initialEntries: ['/tasks?q=nothing-matches'] });
        await user.click(await screen.findByRole('button', { name: 'Clear filters' }));

        await waitFor(() => expect(taskTitles()).toHaveLength(TASKS.length));
        expect(screen.getByRole('searchbox', { name: 'Search this list' })).toHaveValue('');
        expect(screen.getByTestId('location-search')).not.toHaveTextContent('q=');
    });

    it('lists the saved views in the title menu with Save as, Save changes, Duplicate and Delete', async () => {
        const { user } = renderWithProviders(<><TasksPage /><LocationProbe /></>, { initialEntries: ['/tasks'] });
        await user.click(await screen.findByRole('button', { name: 'All tasks' }));

        const menu = screen.getByRole('menu', { name: 'Saved views' });
        expect(within(menu).getByRole('menuitemradio', { name: 'All tasks' })).toHaveAttribute('aria-checked', 'true');
        await waitFor(() => expect(within(menu).getByRole('menuitemradio', { name: /Ana planned/ })).toBeInTheDocument());
        for (const name of ['Save as…', 'Save changes', 'Duplicate', 'Delete']) {
            expect(within(menu).getByRole('menuitem', { name })).toBeInTheDocument();
        }

        await user.click(within(menu).getByRole('menuitemradio', { name: /Ana planned/ }));
        expect(await screen.findByRole('heading', { level: 1, name: 'Ana planned' })).toBeInTheDocument();
        expect(screen.getByTestId('location-search')).toHaveTextContent('?assignee=7&status=planned&view=12');
        await waitFor(() => expect(taskTitles()).toEqual(['Ship release build']));
    });

    it('saves Milestone and Needs attention with changes to a view', async () => {
        const updated = { ...anaPlannedView, filters_json: { assigneeId: 7, status: 'active', milestoneId: 5, needsAttention: true } };
        savedViewServiceMock.update.mockImplementation(async () => {
            savedViewServiceMock.getAll.mockResolvedValue([updated]);
            return updated;
        });
        const { user } = renderWithProviders(<><TasksPage /><LocationProbe /></>, {
            initialEntries: ['/tasks?assignee=7&status=active&milestone=5&attention=yes&view=12'],
        });

        expect(await screen.findByText('Modified view')).toBeInTheDocument();
        await user.click(screen.getByRole('button', { name: 'Save changes' }));

        await waitFor(() => expect(savedViewServiceMock.update).toHaveBeenCalled());
        const [id, payload] = savedViewServiceMock.update.mock.calls[0];
        expect(id).toBe(12);
        expect(payload.filters_json).toMatchObject({ assigneeId: 7, status: 'active', milestoneId: 5, needsAttention: true });
        expect(await screen.findByText('Saved view updated')).toBeInTheDocument();
    });

    it('marks a view modified when Milestone or Needs attention differ from it', async () => {
        renderWithProviders(<TasksPage />, { initialEntries: ['/tasks?assignee=7&status=planned&milestone=5&attention=yes&view=12'] });

        expect(await screen.findByRole('heading', { level: 1, name: 'Ana planned' })).toBeInTheDocument();
        expect(await screen.findByText('Modified view')).toBeInTheDocument();
        expect(screen.getByRole('button', { name: 'Save changes' })).toBeInTheDocument();
    });

    it('saves Needs attention with a new saved view', async () => {
        const created = { ...anaPlannedView, id: 13, name: 'Needs a look', filters_json: { status: 'active', needsAttention: true } };
        savedViewServiceMock.create.mockImplementation(async () => {
            savedViewServiceMock.getAll.mockResolvedValue([anaPlannedView, created]);
            return created;
        });
        const { user } = renderWithProviders(<TasksPage />, { initialEntries: ['/tasks?status=active&attention=yes'] });

        await user.click(await screen.findByRole('button', { name: 'Save as…' }));
        const dialog = screen.getByRole('dialog');
        expect(within(dialog).queryByRole('note')).not.toBeInTheDocument();
        await user.type(within(dialog).getByRole('textbox', { name: 'Name' }), 'Needs a look');
        await user.click(within(dialog).getByRole('button', { name: 'Save' }));

        await waitFor(() => expect(savedViewServiceMock.create).toHaveBeenCalled());
        const payload = savedViewServiceMock.create.mock.calls[0][0];
        expect(payload.filters_json).toMatchObject({ status: 'active', needsAttention: true });
        expect(await screen.findByText('Saved view created')).toBeInTheDocument();
    });

    it('narrows the visible list while typing in search and restores it when search is cleared', async () => {
        const { user } = renderWithProviders(<><TasksPage /><LocationProbe /></>, { initialEntries: ['/tasks'] });
        expect(await screen.findByRole('button', { name: 'Write launch notes' })).toBeInTheDocument();
        expect(taskTitles()).toHaveLength(3);

        const search = screen.getByRole('searchbox', { name: 'Search this list' });
        await user.type(search, 'login');
        expect(taskTitles()).toEqual(['Fix login bug']);
        expect(screen.getByTestId('location-search')).toHaveTextContent('q=login');

        await user.clear(search);
        expect(taskTitles()).toHaveLength(3);
        expect(screen.getByTestId('location-search')).not.toHaveTextContent('q=');
    });

    it('shows a hand-over from Plan as a chip without the modified-view warning', async () => {
        renderWithProviders(<TasksPage />, { initialEntries: ['/tasks?planningIssue=unassigned&iterationId=1&fromPlanStep=schedule'] });

        const chips = await screen.findByRole('list', { name: 'Active filters' });
        expect(within(chips).getByText('Planning readiness: Unassigned')).toBeInTheDocument();
        await waitFor(() => expect(taskTitles()).toEqual(['Write launch notes']));
        expect(screen.queryByText('Modified view')).not.toBeInTheDocument();
        expect(screen.queryByRole('button', { name: 'Save as…' })).not.toBeInTheDocument();
        expect(screen.getByRole('link', { name: 'Return to plan' })).toBeInTheDocument();
    });

    it('keeps the layout, grouping and order in the URL', async () => {
        const { user } = renderWithProviders(<><TasksPage /><LocationProbe /></>, { initialEntries: ['/tasks'] });
        expect(await screen.findByRole('button', { name: 'Write launch notes' })).toBeInTheDocument();

        await user.click(screen.getByRole('button', { name: 'View options' }));
        const options = screen.getByRole('dialog', { name: 'View options' });
        await user.selectOptions(within(options).getByRole('combobox', { name: 'Group by' }), 'none');
        await user.selectOptions(within(options).getByRole('combobox', { name: 'Sort by' }), 'title');
        expect(screen.getByTestId('location-search')).toHaveTextContent('?group=none&sort=title');
        expect(screen.queryByRole('heading', { level: 2, name: /Planned/ })).not.toBeInTheDocument();
        expect(taskTitles()).toEqual(['Fix login bug', 'Ship release build', 'Write launch notes']);
        await user.keyboard('{Escape}');

        await user.click(screen.getByRole('button', { name: 'Pipeline' }));
        expect(screen.getByTestId('location-search')).toHaveTextContent('layout=pipeline');
        expect(screen.getByText(i18n.t('agentPipeline.runLogsNeedKey'))).toBeInTheDocument();
        expect(screen.queryByRole('button', { name: 'View options' })).not.toBeInTheDocument();
    });
});

// jsdom has no layout engine, but it does apply stylesheets to getComputedStyle. These tests load the app's own
// rules (the Tailwind utilities the page uses, then planning-masters.css) and check what decides where rows sit:
// selecting may not change the layout styles of any box on the page, and whatever selecting adds must overlay the
// page in a positioned box that holds no task rows. A browser confirms the same with real coordinates:
// scripts/check-task-selection-layout.mjs.
const LAYOUT_PROPERTIES = [
    'display', 'position', 'float', 'top', 'bottom', 'transform', 'translate', 'scale', 'rotate', 'box-sizing',
    'width', 'min-width', 'max-width', 'height', 'min-height', 'max-height',
    'margin-top', 'margin-right', 'margin-bottom', 'margin-left',
    'padding-top', 'padding-right', 'padding-bottom', 'padding-left',
    'border-top-width', 'border-right-width', 'border-bottom-width', 'border-left-width',
    'font-size', 'line-height', 'white-space',
    'flex-direction', 'flex-wrap', 'flex-grow', 'flex-shrink', 'flex-basis', 'gap', 'row-gap', 'column-gap', 'grid-template-rows',
];
// jsdom caches computed styles, and a cached copy can lose a longhand set after a shorthand (the preflight's
// `padding: 0`, then `pr-2` or an inline padding). Adding a node clears that cache, so each element's style is read
// fresh once per pass and kept until `startStylePass` begins the next one.
let passStyles = new Map<Element, CSSStyleDeclaration>();
const startStylePass = () => { passStyles = new Map(); };
const freshStyle = (element: Element) => {
    let style = passStyles.get(element);
    if (!style) {
        const marker = document.createComment('');
        document.body.append(marker);
        marker.remove();
        style = getComputedStyle(element);
        passStyles.set(element, style);
    }
    return style;
};
// jsdom writes a zero length as "0" or "0px" depending on how the rule was read; both mean the same box.
const layoutOf = (element: Element) => {
    const style = freshStyle(element);
    return LAYOUT_PROPERTIES.map(property => `${property}:${style.getPropertyValue(property).replace(/(^|\s)0(px|rem|em)\b/g, '$10')}`);
};
const describeElement = (element: Element) => `<${element.tagName.toLowerCase()} class="${element.getAttribute('class') ?? ''}">`;

/** True when the element takes no space among the rows: hidden, or inside a positioned overlay that holds no task row. */
const overlaysPage = (element: Element, root: Element) => {
    const rows = [...root.querySelectorAll('[data-task-row]')];
    for (let node: Element | null = element; node && node !== root; node = node.parentElement) {
        const { position, display } = freshStyle(node);
        if (display === 'none') return true;
        if ((position === 'absolute' || position === 'fixed') && !rows.some(row => node.contains(row) || row.contains(node))) return true;
    }
    return false;
};

// jsdom ignores logical properties, and Tailwind writes px-*, my-*, inset-x-* and border-x with them, so the test
// stylesheet spells them out as the physical sides they mean in a left-to-right page.
const SIDES = { inline: ['left', 'right'], block: ['top', 'bottom'] } as const;
const physicalProperties = (stylesheet: string) => stylesheet.replace(
    /(^|[;{\s])(padding|margin|inset|scroll-padding|scroll-margin|border)-(inline|block)(-start|-end)?(-width|-style|-color)?\s*:\s*([^;}]+)/g,
    (_match, before: string, property: string, axis: 'inline' | 'block', edge: string | undefined, part: string | undefined, value: string) => {
        const sides = edge ? [SIDES[axis][edge === '-start' ? 0 : 1]] : SIDES[axis];
        const name = (side: string) => property === 'inset' ? side : `${property}-${side}${part ?? ''}`;
        return before + sides.map(side => `${name(side)}: ${value.trim()}`).join('; ');
    },
);

// Builds globals.css the way the Vite plugin does, for exactly the classes in `html`, with nesting flattened for jsdom.
const appStylesFor = async (html: string) => {
    const stylesDir = resolve(__dirname, '../styles');
    const compiler = await compile(readFileSync(resolve(stylesDir, 'globals.css'), 'utf8'), { base: stylesDir, onDependency: () => undefined });
    const parsed = new DOMParser().parseFromString(html, 'text/html');
    const candidates = new Set([...parsed.querySelectorAll('[class]')].flatMap(element => [...element.classList]));
    return `${physicalProperties(optimize(compiler.build([...candidates])).code)}\n${css}`;
};

/** Opens the page, ticks two tasks and opens Assign; `onRest` sees the page root before the first tick. */
const selectTwoAndAssign = async (fullScreen: boolean, onRest: (root: Element) => void = () => undefined) => {
    const { container } = renderWithProviders(<div className="wc"><TasksPage /></div>, { initialEntries: [fullScreen ? '/tasks?fullscreen=1' : '/tasks'] });
    await waitFor(() => expect(taskTitles()).toHaveLength(TASKS.length));
    const root = fullScreen ? container.querySelector('[data-fullscreen-workspace]') : container.firstElementChild;
    if (!root) throw new Error('The page did not render');
    onRest(root);
    // Plain clicks, so no hover or focus state changes the rows on its own.
    fireEvent.click(screen.getByRole('checkbox', { name: 'Select: Write launch notes' }));
    fireEvent.click(screen.getByRole('checkbox', { name: 'Select: Ship release build' }));
    const bar = await screen.findByTestId('task-bulk-operations');
    expect(bar).toHaveTextContent('Selected tasks: 2');
    fireEvent.click(within(bar).getByRole('button', { name: 'Assign' }));
    expect(await within(bar).findByRole('combobox', { name: 'Choose assignee' })).toBeInTheDocument();
    return { root, bar };
};

describe('Selecting tasks keeps the list still', () => {
    beforeEach(() => {
        workScopeMock.iteration = 1;
        iterationServiceMock.getAll.mockResolvedValue([{ id: 1, name: 'Iteration one', start_date: '2026-11-01', end_date: '2026-11-30' }]);
        iterationServiceMock.getById.mockResolvedValue({ id: 1, name: 'Iteration one', project_id: null });
        taskServiceMock.getByIteration.mockResolvedValue(TASKS);
        savedViewServiceMock.getAll.mockResolvedValue([]);
    });

    it.each([
        ['on the page, where the bar takes the toolbar\'s place', false],
        ['in full screen, where the bar covers the title', true],
    ])('changes no box that places the rows, and shows the selection bar over the page %s', async (_where, fullScreen) => {
        // A first pass collects the classes the page uses at rest and while selecting, for the stylesheet.
        let restHtml = '';
        const firstPass = await selectTwoAndAssign(fullScreen, root => { restHtml = root.outerHTML; });
        const stylesheet = await appStylesFor(`${restHtml}\n${firstPass.root.outerHTML}`);
        cleanup();

        const style = document.createElement('style');
        style.textContent = stylesheet;
        document.head.appendChild(style);
        try {
            const before = new Map<Element, { layout: string[]; overlay: boolean }>();
            const { root, bar } = await selectTwoAndAssign(fullScreen, rest => {
                startStylePass();
                for (const element of rest.querySelectorAll('*')) before.set(element, { layout: layoutOf(element), overlay: overlaysPage(element, rest) });
            });
            expect(root.querySelectorAll('[data-task-row]')).toHaveLength(TASKS.length);
            startStylePass();

            // The bar, its Assign editor and everything else selecting adds overlay the page.
            expect(overlaysPage(bar, root)).toBe(true);
            const added = [...root.querySelectorAll('*')].filter(element => !before.has(element));
            expect(added.length).toBeGreaterThan(0);
            expect(added.filter(element => !overlaysPage(element, root)).map(describeElement)).toEqual([]);
            // Nothing that took space is taken away.
            const removed = [...before].filter(([element, { overlay }]) => !root.contains(element) && !overlay);
            expect(removed.map(([element]) => describeElement(element))).toEqual([]);
            // No box that takes space changes its size, spacing or position rules.
            const changed = [...before].flatMap(([element, { layout, overlay }]) => {
                if (!root.contains(element) || (overlay && overlaysPage(element, root))) return [];
                const now = layoutOf(element);
                const changes = layout.map((entry, index) => entry === now[index] ? '' : `${entry} -> ${now[index]}`).filter(Boolean);
                return changes.length ? [{ element: describeElement(element), changes }] : [];
            });
            expect(changed).toEqual([]);
            // The toolbar the bar replaces keeps its place: hidden, not removed.
            if (!fullScreen) {
                const toolbar = screen.getByTestId('page-toolbar').closest('.wc-page-toolbar-frame');
                if (!toolbar) throw new Error('The toolbar frame is missing');
                expect(freshStyle(toolbar).visibility).toBe('hidden');
                expect(freshStyle(toolbar).display).not.toBe('none');
            }
        } finally {
            style.remove();
        }
    }, 30000);
});

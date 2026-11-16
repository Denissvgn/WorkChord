import { beforeEach, describe, expect, it, vi } from 'vitest';
import { screen, waitFor, within } from '@testing-library/react';
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
const savedViewServiceMock = vi.hoisted(() => ({ getAll: vi.fn(), update: vi.fn(), delete: vi.fn() }));

vi.mock('../features/scope/useWorkScope', () => ({
    useWorkScope: () => workScopeMock,
    useSetWorkScope: () => ({ setProject: vi.fn(), setIteration: vi.fn(), setScope: vi.fn() }),
}));
vi.mock('../services/iterationService', () => ({ iterationService: iterationServiceMock }));
vi.mock('../services/taskService', () => ({ taskService: taskServiceMock }));
vi.mock('../services/savedViewService', () => ({ savedViewService: savedViewServiceMock }));
vi.mock('../services/sessionService', () => ({ sessionService: { getWhoAmI: vi.fn().mockResolvedValue({ id: 3, principal_id: null }) } }));
vi.mock('../services/labelService', () => ({ labelService: { getGroups: vi.fn().mockResolvedValue([]) } }));
vi.mock('../services/projectService', () => ({ projectService: { getAll: vi.fn().mockResolvedValue([]) } }));
vi.mock('../services/teamService', () => ({ teamService: { getByIteration: vi.fn().mockResolvedValue([{ id: 7, name: 'Ana' }]) } }));
vi.mock('../components/tasks/TaskAgentReadinessBadge', () => ({ TaskAgentReadinessBadge: () => null }));

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
        expect(await screen.findByRole('heading', { level: 2, name: 'No tasks match this view' })).toBeInTheDocument();
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

import { beforeEach, describe, expect, it, vi } from 'vitest';
import { screen, waitFor, within } from '@testing-library/react';
import { useLocation } from 'react-router-dom';
import type { ReactNode } from 'react';
import { renderWithProviders } from '../test/renderWithProviders';
import type { Task } from '../types/task';
import TasksPage from './TasksPage';

const iterationServiceMock = vi.hoisted(() => ({
    getAll: vi.fn(),
}));

const iterationStoreMock = vi.hoisted(() => ({
    selectedIterationId: 1,
    setSelectedIterationId: vi.fn(),
}));
const savedViewServiceMock = vi.hoisted(() => ({
    getAll: vi.fn(),
}));
const taskServiceMock = vi.hoisted(() => ({
    getById: vi.fn(),
}));

vi.mock('../services/iterationService', () => ({
    iterationService: iterationServiceMock,
}));
vi.mock('../services/savedViewService', () => ({
    savedViewService: savedViewServiceMock,
}));
vi.mock('../services/taskService', () => ({
    taskService: taskServiceMock,
}));

vi.mock('../store/iterationStore', () => ({
    useIterationStore: () => iterationStoreMock,
}));

vi.mock('../components/tasks/TaskList', () => ({
    TaskList: ({
        requestedMode,
        filters,
    }: {
        requestedMode?: string | null;
        filters?: { planningIssue?: string | null };
    }) => (
        <div>
            Task list{requestedMode ? ` — ${requestedMode}` : ''}
            <output data-testid="task-planning-issue">
                {filters?.planningIssue ?? 'none'}
            </output>
        </div>
    ),
}));

vi.mock('../components/tasks/KanbanBoard/KanbanBoard', () => ({
    KanbanBoard: () => <div>Board</div>,
}));

vi.mock('../components/tasks/TaskFiltersBar', () => ({
    defaultFilters: {},
    TaskFiltersBar: () => <div>Filters</div>,
}));

vi.mock('../components/tasks/SavedViewsControl', () => ({
    SavedViewsControl: () => <div>Saved views</div>,
}));

vi.mock('../components/iteration/IterationSelector', () => ({
    IterationSelector: () => <div>Iteration selector</div>,
}));

vi.mock('../components/common/Modal', () => ({
    Modal: ({ open, children }: { open: boolean; children: ReactNode }) => open ? <div role="dialog">{children}</div> : null,
}));

vi.mock('../components/tasks/TaskForm', () => ({
    TaskForm: ({
        initialData,
        onCancel,
    }: {
        initialData?: Task;
        onCancel: () => void;
    }) => (
        <div>
            {initialData && <p>Editing {initialData.title}</p>}
            <button type="button" onClick={onCancel}>Cancel draft</button>
        </div>
    ),
}));

const LocationProbe = () => {
    const location = useLocation();
    return (
        <>
            <output data-testid="location-path">{location.pathname}</output>
            <output data-testid="location-search">{location.search}</output>
            <output data-testid="location-state">{JSON.stringify(location.state)}</output>
        </>
    );
};

const focusedTask = {
    id: 42,
    iteration_id: 1,
    title: 'Resolve launch blocker',
    status: 'active',
    effort_days: 2,
    effort_hours: 16,
    priority: 1,
    is_overdue: true,
    is_delayed: false,
    is_composite: false,
    is_optional: false,
    is_deferred: false,
    tags: [],
    sort_order: 0,
    external_links: [],
    request_count: 0,
    agent_readiness: {
        is_ready: false,
        blockers: [],
        warnings: [],
        criteria: [],
    },
    version: 1,
    children: [],
    dependencies: [],
} as Task;

describe('TasksPage', () => {
    beforeEach(() => {
        iterationStoreMock.selectedIterationId = 1;
        iterationStoreMock.setSelectedIterationId.mockReset();
        iterationServiceMock.getAll.mockReset();
        iterationServiceMock.getAll.mockResolvedValue([
            { id: 1, name: 'Iteration one', start_date: '2026-01-01', end_date: '2026-01-14' },
        ]);
        savedViewServiceMock.getAll.mockReset();
        savedViewServiceMock.getAll.mockResolvedValue([]);
        taskServiceMock.getById.mockReset();
        taskServiceMock.getById.mockResolvedValue(focusedTask);
    });

    it('clears create intent while preserving a Plan Master return checkpoint', async () => {
        const { user } = renderWithProviders(
            <>
                <TasksPage />
                <LocationProbe />
            </>,
            { initialEntries: ['/tasks?create=1&fromPlanStep=work'] },
        );

        expect(await screen.findByRole('dialog')).toBeInTheDocument();
        expect(screen.getByRole('button', { name: 'Cancel draft' })).toBeInTheDocument();
        expect(screen.getByRole('link', { name: 'Return to plan' }))
            .toHaveAttribute('href', '/plan/master?step=work');

        await user.click(screen.getByRole('button', { name: 'Cancel draft' }));

        expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
        expect(screen.getByTestId('location-search')).toHaveTextContent('?fromPlanStep=work');
    });

    it('applies a URL-selected saved view and keeps its context visible', async () => {
        savedViewServiceMock.getAll.mockResolvedValue([{
            id: 12,
            name: 'Needs owners',
            description: null,
            seed_key: null,
            view_type: 'tasks',
            scope: 'shared',
            filters_json: { assigneeId: -1 },
            sort_json: { sortKey: 'priority' },
            columns_json: {},
            created_by_session_id: null,
            schema_version: 1,
            is_valid: true,
            invalid_reason: null,
            created_at: '2026-08-01T00:00:00Z',
            updated_at: '2026-08-01T00:00:00Z',
        }]);

        renderWithProviders(<TasksPage />, {
            initialEntries: ['/tasks?view=12'],
        });

        expect(await screen.findByText('Needs owners')).toBeVisible();
        expect(screen.getByText('1 active filter')).toBeVisible();
        expect(screen.getByRole('button', { name: 'Clear view' })).toBeVisible();
        expect(savedViewServiceMock.getAll).toHaveBeenCalledWith({ view_type: 'tasks' });
    });

    it('hydrates an exact Planning issue and clears it without losing return context', async () => {
        const { user } = renderWithProviders(
            <>
                <TasksPage />
                <LocationProbe />
            </>,
            {
                initialEntries: [
                    '/tasks?panel=filters&planningIssue=unassigned&iterationId=1&fromPlanStep=schedule',
                ],
            },
        );

        expect(await screen.findByText(
            'Planning blockers · Needs assignees',
        )).toBeVisible();
        expect(screen.getByText(
            'Showing Plan Work tasks without an assignee.',
        )).toBeVisible();
        expect(screen.getByTestId('task-planning-issue')).toHaveTextContent(
            'unassigned',
        );
        expect(screen.getByRole('link', { name: 'Return to plan' }))
            .toHaveAttribute('href', '/plan/master?step=schedule');
        expect(screen.getByRole('dialog', { name: 'Filters' })).toBeVisible();

        await user.click(screen.getByRole('button', { name: 'Clear view' }));

        await waitFor(() => expect(
            screen.getByTestId('task-planning-issue'),
        ).toHaveTextContent('none'));
        expect(screen.getByTestId('location-search')).toHaveTextContent(
            '?panel=filters&iterationId=1&fromPlanStep=schedule',
        );
    });

    it('rejects an unknown Planning issue without changing the period or return checkpoint', async () => {
        renderWithProviders(
            <>
                <TasksPage />
                <LocationProbe />
            </>,
            {
                initialEntries: [
                    '/tasks?planningIssue=Unassigned&iterationId=1&fromPlanStep=blockers',
                ],
            },
        );

        await waitFor(() => expect(
            screen.getByTestId('location-search'),
        ).not.toHaveTextContent('planningIssue'));
        expect(screen.getByTestId('location-search')).toHaveTextContent(
            'iterationId=1',
        );
        expect(screen.getByTestId('location-search')).toHaveTextContent(
            'fromPlanStep=blockers',
        );
        expect(await screen.findByTestId('task-planning-issue')).toHaveTextContent(
            'none',
        );
    });

    it('opens expert task modes from URL commands', async () => {
        renderWithProviders(<TasksPage />, {
            initialEntries: ['/tasks?mode=bulk'],
        });

        expect(await screen.findByText('Task list — bulk')).toBeVisible();
        expect(screen.queryByRole('button', { name: 'Planning help' })).not.toBeInTheDocument();
    });

    it('opens filters and board layout from command URLs', async () => {
        renderWithProviders(<TasksPage />, {
            initialEntries: ['/tasks?panel=filters&layout=board'],
        });

        const viewContext = await screen.findByRole('region', { name: 'Task view context' });
        expect(within(viewContext).getByRole('button', { name: 'Board' }))
            .toHaveAttribute('aria-pressed', 'true');
        expect(within(viewContext).getByRole('button', { name: 'Filters' })).toBeVisible();
        expect(within(viewContext).getByRole('button', { name: 'List' })).toBeVisible();
        const newTaskAction = screen.getByRole('button', { name: 'New Task' });
        expect(newTaskAction.closest('.tasks-primary-slot')).not.toBeNull();
        expect(screen.getAllByRole('button', { name: 'New Task' })).toHaveLength(1);
        expect(screen.getByRole('dialog', { name: 'Filters' })).toBeVisible();
    });

    it('opens an exact Overview task in a drawer over the board and preserves return context', async () => {
        const { user } = renderWithProviders(
            <>
                <TasksPage />
                <LocationProbe />
            </>,
            {
                initialEntries: [
                    '/tasks?layout=board&task=42&from=overview&returnTask=42&thread=work-now',
                ],
            },
        );

        expect((await screen.findAllByText('Board')).some((element) => (
            element.tagName === 'DIV'
        ))).toBe(true);
        const drawer = await screen.findByRole('dialog', {
            name: 'Resolve launch blocker',
        });
        const closeTaskEditor = within(drawer).getByRole('button', {
            name: 'Close task editor',
        });
        const returnToOverview = screen.getByRole('link', {
            name: 'Return to Overview',
        });
        expect(drawer).toHaveAttribute('aria-modal', 'true');
        expect(drawer).toHaveAccessibleDescription('Planning thread · Work now');
        expect(drawer).toHaveClass('max-w-2xl');
        expect(drawer).not.toHaveClass('max-w-[480px]');
        expect(within(drawer).getByRole('heading', {
            level: 2,
            name: 'Resolve launch blocker',
        })).toBeVisible();
        await waitFor(() => expect(closeTaskEditor).toHaveFocus());
        expect(within(drawer).getByText('Editing Resolve launch blocker')).toBeVisible();
        expect(within(drawer).getByText('Planning thread · Work now')).toBeVisible();
        expect(screen.getByRole('complementary', {
            name: 'Planning thread from Overview',
        })).toHaveTextContent('Task #42 · Resolve launch blocker');

        await user.click(closeTaskEditor);

        expect(screen.queryByRole('dialog', {
            name: 'Resolve launch blocker',
        })).not.toBeInTheDocument();
        await waitFor(() => expect(returnToOverview).toHaveFocus());
        expect(screen.getByTestId('location-search')).toHaveTextContent(
            '?layout=board&from=overview&returnTask=42',
        );
        expect(screen.getByRole('complementary', {
            name: 'Planning thread from Overview',
        })).toHaveTextContent('Task #42 · Resolve launch blocker');

        await user.click(returnToOverview);

        expect(screen.getByTestId('location-path')).toHaveTextContent('/');
        expect(screen.getByTestId('location-state')).toHaveTextContent(
            'overview-task-42',
        );
    });

    it('keeps the exact task identity in the drawer when the task cannot be loaded', async () => {
        taskServiceMock.getById.mockReset();
        taskServiceMock.getById.mockRejectedValue(new Error('task unavailable'));

        renderWithProviders(<TasksPage />, {
            initialEntries: [
                '/tasks?layout=board&task=42&from=overview&returnTask=42&thread=work-now',
            ],
        });

        const drawer = await screen.findByRole('dialog', { name: 'Task #42' });
        expect(drawer).toHaveAccessibleDescription('Planning thread · Work now');
        expect(within(drawer).getByRole('heading', {
            level: 2,
            name: 'Task #42',
        })).toBeVisible();
        expect(await within(drawer).findByRole('alert')).toHaveTextContent(
            'The current task could not be loaded.',
        );
        expect(within(drawer).getByRole('button', { name: 'Retry' })).toBeVisible();
    });
});

import { beforeEach, describe, expect, it, vi } from 'vitest';
import { screen, waitFor, within } from '@testing-library/react';
import { useLocation } from 'react-router-dom';
import type { ReactNode } from 'react';
import { renderWithProviders } from '../test/renderWithProviders';
import type { Task } from '../types/task';
import TasksPage from './TasksPage';

import { Button } from '../components/common/Button';
const iterationServiceMock = vi.hoisted(() => ({
    getAll: vi.fn(),
}));

const workScopeMock = vi.hoisted(() => ({
    iteration: 1 as number | 'backlog',
    setIteration: vi.fn(),
}));
const savedViewServiceMock = vi.hoisted(() => ({
    getAll: vi.fn(),
}));
const taskServiceMock = vi.hoisted(() => ({
    getDetail: vi.fn(),
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

vi.mock('../features/scope/useWorkScope', () => ({
    useWorkScope: () => workScopeMock,
    useSetWorkScope: () => ({ setProject: vi.fn(), setIteration: vi.fn(), setScope: vi.fn() }),
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
    SavedViewPicker: ({ label }: { label: string }) => <span>{label}</span>,
}));

vi.mock('../services/sessionService', () => ({
    sessionService: { getWhoAmI: vi.fn().mockResolvedValue({ id: 1, principal_id: null }) },
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
            <Button type="button" onClick={onCancel} variant="secondary">Cancel draft</Button>
        </div>
    ),
}));

vi.mock('../components/tasks/TaskReadView', () => ({
    TASK_PART_PARAM: 'part',
    TaskReadView: ({ task }: { task: Task }) => <p>Reading {task.title}</p>,
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
        workScopeMock.iteration = 1;
        workScopeMock.setIteration.mockReset();
        iterationServiceMock.getAll.mockReset();
        iterationServiceMock.getAll.mockResolvedValue([
            { id: 1, name: 'Iteration one', start_date: '2026-01-01', end_date: '2026-01-14' },
        ]);
        savedViewServiceMock.getAll.mockReset();
        savedViewServiceMock.getAll.mockResolvedValue([]);
        taskServiceMock.getById.mockReset();
        taskServiceMock.getById.mockResolvedValue(focusedTask);
        taskServiceMock.getDetail.mockResolvedValue({ task: focusedTask, ancestors: [], ancestors_complete: true,
            children: { items: [], has_more: false, next_after_id: null, limit: 50 },
            dependencies: { items: [], has_more: false, next_after_id: null, limit: 50 }, execution_context_complete: false });
    });

    it('clears create intent while preserving a return to its Plan checkpoint', async () => {
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
            .toHaveAttribute('href', '/plan?step=work&returned=1');

        await user.click(screen.getByRole('button', { name: 'Cancel draft' }));

        expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
        expect(screen.getByTestId('location-search')).toHaveTextContent('?fromPlanStep=work');
    });

    it('applies a URL-selected saved view: its name is the title and its filters move into the URL', async () => {
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

        renderWithProviders(<><TasksPage /><LocationProbe /></>, {
            initialEntries: ['/tasks?view=12'],
        });

        expect(await screen.findByRole('heading', { level: 1, name: 'Needs owners' })).toBeVisible();
        await waitFor(() => expect(screen.getByTestId('location-search')).toHaveTextContent('?view=12&assignee=none'));
        expect(savedViewServiceMock.getAll).toHaveBeenCalledWith({ view_type: 'tasks' });
    });

    it('hydrates an exact Planning issue, keeps the return context and moves the Filters command to the toolbar', async () => {
        renderWithProviders(
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

        expect(await screen.findByTestId('task-planning-issue')).toHaveTextContent(
            'unassigned',
        );
        expect(screen.getByRole('link', { name: 'Return to plan' }))
            .toHaveAttribute('href', '/plan?step=schedule&returned=1');
        expect(screen.queryByRole('dialog', { name: 'Filters' })).not.toBeInTheDocument();
        await waitFor(() => expect(screen.getByTestId('location-search')).toHaveTextContent(
            '?planningIssue=unassigned&iterationId=1&fromPlanStep=schedule',
        ));
        expect(screen.queryByText('Modified view')).not.toBeInTheDocument();
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

    it('opens the board layout from the URL with one header and one New task action', async () => {
        renderWithProviders(<TasksPage />, {
            initialEntries: ['/tasks?layout=board'],
        });

        const layout = await screen.findByRole('group', { name: 'Task layout' });
        expect(within(layout).getByRole('button', { name: 'Board' }))
            .toHaveAttribute('aria-pressed', 'true');
        expect(within(layout).getByRole('button', { name: 'List' })).toHaveAttribute('aria-pressed', 'false');
        expect(within(layout).getByRole('button', { name: 'Pipeline' })).toBeVisible();
        expect(screen.getAllByText('Board').some(element => element.tagName === 'DIV')).toBe(true);
        const newTaskAction = screen.getByRole('button', { name: 'New task' });
        expect(newTaskAction.closest('.wc-page-primary')).not.toBeNull();
        expect(screen.getAllByRole('button', { name: 'New task' })).toHaveLength(1);
        expect(screen.queryByRole('button', { name: 'View options' })).not.toBeInTheDocument();
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
        // The drawer opens read-first; editing is one click away.
        expect(within(drawer).getByText('Reading Resolve launch blocker')).toBeVisible();
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
        taskServiceMock.getDetail.mockRejectedValue(new Error('task unavailable'));

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

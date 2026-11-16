import { beforeEach, describe, expect, it, vi } from 'vitest';
import { screen, waitFor, within } from '@testing-library/react';
import { useLocation } from 'react-router-dom';
import { renderWithProviders } from '../test/renderWithProviders';
import type { Task } from '../types/task';
import TasksPage from './TasksPage';

const workScopeMock = vi.hoisted(() => ({ iteration: 1 as number | 'backlog', setIteration: vi.fn() }));
const iterationServiceMock = vi.hoisted(() => ({ getAll: vi.fn(), getById: vi.fn() }));
const taskServiceMock = vi.hoisted(() => ({ getByIteration: vi.fn(), getById: vi.fn(), getDetail: vi.fn() }));

vi.mock('../features/scope/useWorkScope', () => ({
    useWorkScope: () => workScopeMock,
    useSetWorkScope: () => ({ setProject: vi.fn(), setIteration: vi.fn(), setScope: vi.fn() }),
}));
vi.mock('../services/iterationService', () => ({ iterationService: iterationServiceMock }));
vi.mock('../services/taskService', () => ({ taskService: taskServiceMock }));
vi.mock('../services/savedViewService', () => ({ savedViewService: { getAll: vi.fn().mockResolvedValue([]), update: vi.fn(), delete: vi.fn() } }));
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

// Task 2 waits for task 1, so its row and its card both show the "Waits for 1" chip.
const TASKS = [
    task(1, 'Write launch notes'),
    task(2, 'Fix login bug', { assignee: ana, status: 'active', effort_days: 2.5, dependencies: [1] }),
    task(3, 'Ship release build', { assignee: ana }),
];

const LocationProbe = () => <output data-testid="location-search">{useLocation().search}</output>;

const cardIds = (container: HTMLElement) => Array.from(container.querySelectorAll<HTMLElement>('[data-task-card]'))
    .map(card => Number(card.dataset.taskCard));

describe('Tasks board under the shared toolbar', () => {
    beforeEach(() => {
        workScopeMock.iteration = 1;
        iterationServiceMock.getAll.mockResolvedValue([{ id: 1, name: 'Iteration one', start_date: '2026-11-01', end_date: '2026-11-30' }]);
        taskServiceMock.getByIteration.mockResolvedValue(TASKS);
    });

    it('keeps a filter set in the list after switching to the board and back', async () => {
        const { user, container } = renderWithProviders(<><TasksPage /><LocationProbe /></>, { initialEntries: ['/tasks'] });
        expect(await screen.findByRole('button', { name: 'Write launch notes' })).toBeInTheDocument();

        await user.selectOptions(screen.getByRole('combobox', { name: 'Assignee' }), '7');
        const chips = await screen.findByRole('list', { name: 'Active filters' });
        expect(within(chips).getByText('Assignee: Ana')).toBeInTheDocument();
        await waitFor(() => expect(screen.queryByRole('button', { name: 'Write launch notes' })).not.toBeInTheDocument());

        await user.click(screen.getByRole('button', { name: 'Board' }));
        await waitFor(() => expect(cardIds(container).sort()).toEqual([2, 3]));
        expect(within(screen.getByRole('list', { name: 'Active filters' })).getByText('Assignee: Ana')).toBeInTheDocument();

        await user.click(screen.getByRole('button', { name: 'List' }));
        expect(await screen.findByRole('button', { name: 'Fix login bug' })).toBeInTheDocument();
        expect(screen.queryByRole('button', { name: 'Write launch notes' })).not.toBeInTheDocument();
        expect(within(screen.getByRole('list', { name: 'Active filters' })).getByText('Assignee: Ana')).toBeInTheDocument();
    });

    it('applies the toolbar search on the board as it does in the list', async () => {
        const { container } = renderWithProviders(<TasksPage />, { initialEntries: ['/tasks?layout=board&q=login'] });
        await waitFor(() => expect(cardIds(container)).toEqual([2]));
    });

    it('shows the same title, state chip, assignee and effort on a card and on its row', async () => {
        const expected = { title: 'Fix login bug', chip: 'Waits for 1', assignee: 'Ana', effort: '2.5d' };

        const board = renderWithProviders(<TasksPage />, { initialEntries: ['/tasks?layout=board'] });
        const card = await waitFor(() => {
            const found = board.container.querySelector<HTMLElement>('[data-task-card="2"]');
            expect(found).not.toBeNull();
            return found as HTMLElement;
        });
        expect(within(card).getByText(expected.title)).toBeInTheDocument();
        expect(within(card).getByText(expected.chip)).toBeInTheDocument();
        expect(within(card).getByText(expected.assignee)).toBeInTheDocument();
        expect(within(card).getByText(expected.effort)).toBeInTheDocument();
        board.unmount();

        const list = renderWithProviders(<TasksPage />, { initialEntries: ['/tasks'] });
        const row = await waitFor(() => {
            const found = list.container.querySelector<HTMLElement>('[data-task-row="2"]');
            expect(found).not.toBeNull();
            return found as HTMLElement;
        });
        expect(within(row).getByRole('button', { name: expected.title })).toBeInTheDocument();
        expect(within(row).getByText(expected.chip)).toBeInTheDocument();
        expect(within(row).getByRole('combobox', { name: `Assignee: ${expected.title}` })).toHaveDisplayValue(expected.assignee);
        expect(within(row).getByText(expected.effort)).toBeInTheDocument();
    });

    it.each([
        [4, { title: 'Draft onboarding guide', chip: 'Ready to start', effort: '0.625d', reviewer: null }],
        [5, { title: 'Review pricing copy', chip: 'In review', effort: '1d', reviewer: 'Reviewer: Morgan' }],
    ] as const)('shows the same title, state chip, assignee, effort and reviewer on card and row for task %i', async (id, expected) => {
        taskServiceMock.getByIteration.mockResolvedValue([
            task(4, 'Draft onboarding guide', { assignee: ana, effort_days: 0.625 }),
            task(5, 'Review pricing copy', { assignee: ana, status: 'resolved', effort_days: 1 }),
        ]);
        taskServiceMock.getDetail.mockResolvedValue({ reviewer_name: 'Morgan' });

        const board = renderWithProviders(<TasksPage />, { initialEntries: ['/tasks?layout=board'] });
        const card = await waitFor(() => {
            const found = board.container.querySelector<HTMLElement>(`[data-task-card="${id}"]`);
            expect(found).not.toBeNull();
            return found as HTMLElement;
        });
        expect(within(card).getByText(expected.title)).toBeInTheDocument();
        expect(within(card).getByText(expected.chip)).toBeInTheDocument();
        expect(within(card).getByText('Ana')).toBeInTheDocument();
        expect(within(card).getByText(expected.effort)).toBeInTheDocument();
        if (expected.reviewer) await waitFor(() => expect(within(card).getByText(expected.reviewer)).toBeInTheDocument());
        board.unmount();

        const list = renderWithProviders(<TasksPage />, { initialEntries: ['/tasks'] });
        const row = await waitFor(() => {
            const found = list.container.querySelector<HTMLElement>(`[data-task-row="${id}"]`);
            expect(found).not.toBeNull();
            return found as HTMLElement;
        });
        expect(within(row).getByRole('button', { name: expected.title })).toBeInTheDocument();
        expect(within(row).getByText(expected.chip)).toBeInTheDocument();
        expect(within(row).getByRole('combobox', { name: `Assignee: ${expected.title}` })).toHaveDisplayValue('Ana');
        expect(within(row).getByText(expected.effort)).toBeInTheDocument();
        if (expected.reviewer) await waitFor(() => expect(within(row).getByText(expected.reviewer)).toBeInTheDocument());
    });
});

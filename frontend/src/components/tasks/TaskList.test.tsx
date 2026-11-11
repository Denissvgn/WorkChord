import { beforeEach, describe, expect, it, vi } from 'vitest';
import { act, screen, waitFor } from '@testing-library/react';
import type { Task } from '../../types/task';
import { renderWithProviders } from '../../test/renderWithProviders';
import { TaskList } from './TaskList';

const taskServiceMock = vi.hoisted(() => ({
    getByIteration: vi.fn(),
    delete: vi.fn(),
    reorder: vi.fn(),
    mergeTasks: vi.fn(),
    unmergeTask: vi.fn(),
}));

const labelServiceMock = vi.hoisted(() => ({
    getGroups: vi.fn(),
}));

vi.mock('../../services/taskService', () => ({
    taskService: taskServiceMock,
}));

vi.mock('../../services/labelService', () => ({
    labelService: labelServiceMock,
}));

vi.mock('../../services/teamService', () => ({
    teamService: { getByIteration: vi.fn().mockResolvedValue([{ id: 5, name: 'Ada' }]) },
}));

vi.mock('../../services/projectService', () => ({
    projectService: { getAll: vi.fn().mockResolvedValue([]) },
}));

vi.mock('../../services/iterationService', () => ({
    iterationService: { getById: vi.fn().mockResolvedValue({ id: 1, name: 'Iteration', project_id: null }) },
}));

vi.mock('./TaskAgentReadinessBadge', () => ({
    TaskAgentReadinessBadge: () => null,
}));

const task = (id: number): Task => ({
    id,
    iteration_id: 1,
    project_id: null,
    milestone_id: null,
    parent_id: null,
    title: `Task ${id}`,
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
    agent_readiness: {
        is_ready: true,
        blockers: [],
        warnings: [],
        criteria: [],
    },
    version: 1,
    children: [],
    dependencies: [],
});

describe('TaskList accessibility', () => {
    beforeEach(() => {
        Object.values(taskServiceMock).forEach(mock => mock.mockReset());
        labelServiceMock.getGroups.mockReset();
        labelServiceMock.getGroups.mockResolvedValue([]);
    });

    it('announces the inner task loading state', () => {
        taskServiceMock.getByIteration.mockReturnValue(new Promise(() => undefined));

        renderWithProviders(
            <TaskList
                iterationId={1}
                sortKey="priority"
                onSortKeyChange={() => undefined}
            />,
        );

        expect(screen.getByRole('status')).toHaveTextContent('Loading tasks');
        expect(screen.getByRole('status')).toHaveAttribute('aria-busy', 'true');
    });

    it('associates the merge parent title label with its input', async () => {
        taskServiceMock.getByIteration.mockResolvedValue([task(1), task(2)]);
        const { user } = renderWithProviders(
            <TaskList
                iterationId={1}
                sortKey="priority"
                onSortKeyChange={() => undefined}
                requestedMode="merge"
            />,
        );

        const selections = await screen.findAllByRole('checkbox', {
            name: 'Select for merge',
        });
        await user.click(selections[0]!);
        await user.click(selections[1]!);
        await user.click(screen.getByRole('button', { name: 'Merge (2)' }));

        expect(screen.getByRole('textbox', {
            name: 'New parent task title',
        })).toHaveFocus();
    });
});


it('retains the merge opening revision while a live list refreshes', async () => {
    const original = [task(1), task(2)].map(value => ({ ...value, iteration_revision: 1 }));
    taskServiceMock.getByIteration.mockResolvedValue(original);
    taskServiceMock.mergeTasks.mockRejectedValue({ response: { status: 409, data: { detail: { message: 'Observed plan changed' } } } });
    const { user, queryClient } = renderWithProviders(<TaskList iterationId={1} sortKey="priority" onSortKeyChange={() => undefined} requestedMode="merge" />);
    const selections = await screen.findAllByRole('checkbox', { name: 'Select for merge' });
    await user.click(selections[0]); await user.click(selections[1]);
    await user.click(screen.getByRole('button', { name: 'Merge (2)' }));
    const title = screen.getByRole('textbox', { name: 'New parent task title' });
    await user.type(title, 'Retained merged intent');
    await act(async () => queryClient.setQueryData(['tasks', 1], original.map(value => ({ ...value, iteration_revision: 9 }))));
    await user.click(screen.getByRole('button', { name: 'Merge tasks' }));
    await waitFor(() => expect(taskServiceMock.mergeTasks.mock.lastCall?.[1].expected_revision).toBe(1));
    expect(title).toHaveValue('Retained merged intent');
    taskServiceMock.getByIteration.mockResolvedValue(original.map(value => ({ ...value, iteration_revision: 9 })));
    await user.click(await screen.findByRole('button', { name: 'Review current inputs' }));
    await waitFor(() => expect(title).toHaveValue('Retained merged intent'));
    await user.click(screen.getByRole('button', { name: 'Merge tasks' }));
    await waitFor(() => expect(taskServiceMock.mergeTasks.mock.lastCall?.[1].expected_revision).toBe(9));
});

it('selects every matching task and focuses the assignee picker when a hand-off opens bulk mode', async () => {
    taskServiceMock.getByIteration.mockResolvedValue([task(1), task(2), task(3)]);
    renderWithProviders(
        <TaskList
            iterationId={1}
            sortKey="priority"
            onSortKeyChange={() => undefined}
            requestedMode="bulk"
            preselectAllInBulk
        />,
    );

    expect(await screen.findByText('Selected tasks: 3')).toBeInTheDocument();
    const assignee = await screen.findByRole('combobox', { name: 'Choose assignee' });
    await waitFor(() => expect(assignee).toHaveFocus());
});

it('offers selection as a visible action instead of a menu', async () => {
    taskServiceMock.getByIteration.mockResolvedValue([task(1)]);
    renderWithProviders(<TaskList iterationId={1} sortKey="priority" onSortKeyChange={() => undefined} />);

    expect(await screen.findByRole('button', { name: 'Select' })).toBeVisible();
    expect(screen.getByRole('button', { name: 'Merge tasks' })).toBeVisible();
});

describe('TaskList rows and groups', () => {
    beforeEach(() => {
        Object.values(taskServiceMock).forEach(mock => mock.mockReset());
        labelServiceMock.getGroups.mockReset();
        labelServiceMock.getGroups.mockResolvedValue([]);
    });

    it('groups by status with counts, work in hand first and finished work collapsed', async () => {
        taskServiceMock.getByIteration.mockResolvedValue([
            { ...task(1), status: 'planned' }, { ...task(2), status: 'active' }, { ...task(3), status: 'planned' }, { ...task(4), status: 'closed' },
        ]);
        const { user } = renderWithProviders(<TaskList iterationId={1} sortKey="priority" onSortKeyChange={() => undefined} />);
        const groups = await screen.findAllByRole('heading', { level: 2 });
        expect(groups.map(group => group.textContent)).toEqual(['Active1 task', 'Planned2 tasks', 'Closed1 task']);
        expect(screen.getByRole('button', { name: /Closed/ })).toHaveAttribute('aria-expanded', 'false');
        expect(screen.queryByRole('button', { name: 'Task 4' })).toBeNull();
        await user.click(screen.getByRole('button', { name: /Closed/ }));
        expect(screen.getByRole('button', { name: 'Task 4' })).toBeInTheDocument();
        await user.click(screen.getByRole('button', { name: 'Group by status' }));
        expect(screen.queryByRole('heading', { level: 2 })).toBeNull();
        expect(screen.getByRole('button', { name: 'Group by status' })).toHaveAttribute('aria-pressed', 'false');
    });

    it('keeps secondary facts behind Details and one manual-order list without groups', async () => {
        taskServiceMock.getByIteration.mockResolvedValue([{ ...task(1), tags: ['backend'] }]);
        const { user } = renderWithProviders(<TaskList iterationId={1} sortKey="sort_order" onSortKeyChange={() => undefined} />);
        expect(await screen.findByRole('button', { name: 'Task 1' })).toBeInTheDocument();
        expect(screen.queryByRole('heading', { level: 2 })).toBeNull();
        expect(screen.getByRole('button', { name: 'Group by status' })).toBeDisabled();
        expect(screen.queryByText('backend')).toBeNull();
        await user.click(screen.getByRole('button', { name: 'Details (2): Task 1' }));
        expect(screen.getByText('backend')).toBeInTheDocument();
    });

    it('renders only the rows near the viewport for a long list', async () => {
        taskServiceMock.getByIteration.mockResolvedValue(Array.from({ length: 120 }, (_, index) => task(index + 1)));
        // jsdom has no layout: give the workspace scroller a viewport-sized box.
        vi.spyOn(HTMLElement.prototype, 'offsetHeight', 'get').mockReturnValue(900);
        vi.spyOn(HTMLElement.prototype, 'offsetWidth', 'get').mockReturnValue(1200);
        renderWithProviders(<main id="workspace-main"><TaskList iterationId={1} sortKey="priority" onSortKeyChange={() => undefined} /></main>);
        expect(await screen.findByRole('heading', { name: /Planned/ })).toBeInTheDocument();
        const rendered = screen.getAllByRole('button', { name: /^Task \d+$/ }).length;
        expect(rendered).toBeGreaterThan(0);
        expect(rendered).toBeLessThan(120);
    });
});

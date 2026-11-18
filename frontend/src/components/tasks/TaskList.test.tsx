import { beforeEach, describe, expect, it, vi } from 'vitest';
import { defaultFilters } from '../../utils/taskFilterDefaults';
import { act, fireEvent, screen, waitFor, within } from '@testing-library/react';
import type { Task } from '../../types/task';
import { createTestQueryClient, renderWithProviders } from '../../test/renderWithProviders';
import { REVIEWER_PAGE_SIZE } from './useAgentRowFacts';
import { TaskList } from './TaskList';
import { taskDetailResponse } from '../../test/fixtures/taskDetail';
import type { TaskFilters } from './TaskFiltersBar';
import { changeAppLanguage } from '../../i18n/i18n';

const taskServiceMock = vi.hoisted(() => ({
    getByIteration: vi.fn(),
    delete: vi.fn(),
    reorder: vi.fn(),
    mergeTasks: vi.fn(),
    unmergeTask: vi.fn(),
    update: vi.fn(),
    changeStatus: vi.fn(),
    runBulkOperation: vi.fn(),
    getDetail: vi.fn(),
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

const teamMock = vi.hoisted(() => ({ getByIteration: vi.fn() }));

vi.mock('../../services/teamService', () => ({
    teamService: teamMock,
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

beforeEach(() => {
    teamMock.getByIteration.mockResolvedValue([{ id: 5, name: 'Ada' }]);
    taskServiceMock.getDetail.mockImplementation(async (id: number) => taskDetailResponse({ ...task(id), status: 'resolved' }, null));
});

const rowOf = (title: string) => screen.getByRole('button', { name: title }).closest<HTMLElement>('[data-task-row]')!;
// user-event reports a move onto a child as the pointer leaving the row, so hover is raised directly.
const hover = (row: HTMLElement) => fireEvent.mouseOver(row);
const unhover = (row: HTMLElement) => fireEvent.mouseOut(row);
const INTERACTIVE = 'button, a[href], input, select, textarea, [tabindex]:not([tabindex="-1"])';

describe('TaskList accessibility', () => {
    beforeEach(() => {
        Object.values(taskServiceMock).forEach(mock => mock.mockReset());
        teamMock.getByIteration.mockResolvedValue([{ id: 5, name: 'Ada' }]);
        taskServiceMock.getDetail.mockImplementation(async (id: number) => taskDetailResponse({ ...task(id), status: 'resolved' }, null));
        labelServiceMock.getGroups.mockReset();
        labelServiceMock.getGroups.mockResolvedValue([]);
    });

    it('announces the inner task loading state', () => {
        taskServiceMock.getByIteration.mockReturnValue(new Promise(() => undefined));

        renderWithProviders(
            <TaskList
                iterationId={1}
                sortKey="priority"
               
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
               
            />,
        );

        await screen.findByRole('button', { name: 'Task 1' });
        hover(rowOf('Task 1'));
        await user.click(screen.getByRole('checkbox', { name: 'Select: Task 1' }));
        await user.click(screen.getByRole('checkbox', { name: 'Select: Task 2' }));
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
    const { user, queryClient } = renderWithProviders(<TaskList iterationId={1} sortKey="priority" />);
    await screen.findByRole('button', { name: 'Task 1' });
    hover(rowOf('Task 1'));
    await user.click(screen.getByRole('checkbox', { name: 'Select: Task 1' }));
    await user.click(screen.getByRole('checkbox', { name: 'Select: Task 2' }));
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
           
            requestedMode="bulk"
            preselectAllInBulk
        />,
    );

    expect(await screen.findByText('Selected tasks: 3')).toBeInTheDocument();
    const assignee = await screen.findByRole('combobox', { name: 'Choose assignee' });
    await waitFor(() => expect(assignee).toHaveFocus());
    expect(screen.queryByRole('button', { name: /Select all/ })).not.toBeInTheDocument();
});

it('leaves sorting, grouping, selection and merging to the page and shows a leading row inside the list', async () => {
    taskServiceMock.getByIteration.mockResolvedValue([task(1)]);
    renderWithProviders(<TaskList iterationId={1} sortKey="priority" leadingRow={<p>Quick add row</p>} />);

    expect(await screen.findByRole('button', { name: 'Task 1' })).toBeInTheDocument();
    expect(screen.getByText('Quick add row')).toBeInTheDocument();
    for (const name of ['Select', 'Merge tasks', 'Group by status', 'Merge (2)']) {
        expect(screen.queryByRole('button', { name })).not.toBeInTheDocument();
    }
    expect(screen.queryByRole('combobox', { name: 'Sort tasks' })).not.toBeInTheDocument();
});

describe('TaskList rows and groups', () => {
    beforeEach(() => {
        Object.values(taskServiceMock).forEach(mock => mock.mockReset());
        teamMock.getByIteration.mockResolvedValue([{ id: 5, name: 'Ada' }]);
        taskServiceMock.getDetail.mockImplementation(async (id: number) => taskDetailResponse({ ...task(id), status: 'resolved' }, null));
        labelServiceMock.getGroups.mockReset();
        labelServiceMock.getGroups.mockResolvedValue([]);
    });

    it('groups by status with counts, work in hand first and finished work collapsed', async () => {
        taskServiceMock.getByIteration.mockResolvedValue([
            { ...task(1), status: 'planned' }, { ...task(2), status: 'active' }, { ...task(3), status: 'planned' },
            { ...task(4), status: 'closed' }, { ...task(5), status: 'resolved' },
        ]);
        const { user, rerender } = renderWithProviders(<TaskList iterationId={1} sortKey="priority" />);
        const groups = await screen.findAllByRole('heading', { level: 2 });
        expect(groups.map(group => group.textContent)).toEqual(['Active1 task', 'Planned2 tasks', 'Resolved1 task', 'Closed1 task']);
        expect(screen.getByRole('button', { name: /Closed/ })).toHaveAttribute('aria-expanded', 'false');
        expect(screen.queryByRole('button', { name: 'Task 4' })).toBeNull();
        await user.click(screen.getByRole('button', { name: /Closed/ }));
        expect(screen.getByRole('button', { name: 'Task 4' })).toBeInTheDocument();
        rerender(<TaskList iterationId={1} sortKey="priority" groupByStatus={false} />);
        expect(screen.queryByRole('heading', { level: 2 })).toBeNull();
    });

    it('shows translated status names for legacy in-progress groups in English and Russian', async () => {
        taskServiceMock.getByIteration.mockResolvedValue([{ ...task(1), status: 'in_progress' }]);
        const { unmount } = renderWithProviders(<TaskList iterationId={1} sortKey="priority" />);
        expect((await screen.findByRole('heading', { level: 2 })).textContent).toBe('Active1 task');
        unmount();

        await changeAppLanguage('ru');
        try {
            renderWithProviders(<TaskList iterationId={1} sortKey="priority" />);
            expect((await screen.findByRole('heading', { level: 2 })).textContent).toBe('Активно1 задача');
        } finally {
            await changeAppLanguage('en');
        }
    });

    it('combines legacy and active tasks into one active group', async () => {
        taskServiceMock.getByIteration.mockResolvedValue([
            { ...task(1), status: 'in_progress' }, { ...task(2), status: 'active' }, { ...task(3), status: 'closed' },
        ]);
        const { user } = renderWithProviders(<TaskList iterationId={1} sortKey="priority" />);
        const groups = await screen.findAllByRole('heading', { level: 2 });
        expect(groups.map(group => group.textContent)).toEqual(['Active2 tasks', 'Closed1 task']);
        expect(screen.getByRole('button', { name: 'Task 1' })).toBeInTheDocument();
        expect(screen.getByRole('button', { name: 'Task 2' })).toBeInTheDocument();
        await user.click(within(groups[0]).getByRole('button'));
        expect(screen.queryByRole('button', { name: 'Task 1' })).not.toBeInTheDocument();
        expect(screen.queryByRole('button', { name: 'Task 2' })).not.toBeInTheDocument();
    });

    it('keeps secondary facts behind Details and one manual-order list without groups', async () => {
        taskServiceMock.getByIteration.mockResolvedValue([{ ...task(1), tags: ['backend'] }]);
        const { user } = renderWithProviders(<TaskList iterationId={1} sortKey="sort_order" />);
        expect(await screen.findByRole('button', { name: 'Task 1' })).toBeInTheDocument();
        expect(screen.queryByRole('heading', { level: 2 })).toBeNull();
        expect(screen.queryByText('backend')).toBeNull();
        hover(rowOf('Task 1'));
        await user.click(screen.getByRole('button', { name: 'Actions for Task 1' }));
        await user.click(screen.getByRole('menuitem', { name: 'Details (2)' }));
        expect(screen.getByText('backend')).toBeInTheDocument();
    });

    it('renders only the rows near the viewport for a long list', async () => {
        taskServiceMock.getByIteration.mockResolvedValue(Array.from({ length: 120 }, (_, index) => task(index + 1)));
        // jsdom has no layout: give the workspace scroller a viewport-sized box.
        vi.spyOn(HTMLElement.prototype, 'offsetHeight', 'get').mockReturnValue(900);
        vi.spyOn(HTMLElement.prototype, 'offsetWidth', 'get').mockReturnValue(1200);
        vi.spyOn(HTMLElement.prototype, 'clientHeight', 'get').mockReturnValue(900);
        vi.spyOn(HTMLElement.prototype, 'clientWidth', 'get').mockReturnValue(1200);
        renderWithProviders(<main id="workspace-main"><TaskList iterationId={1} sortKey="priority" /></main>);
        expect(await screen.findByRole('heading', { name: /Planned/ })).toBeInTheDocument();
        const rendered = screen.getAllByRole('button', { name: /^Task \d+$/ }).length;
        expect(rendered).toBeGreaterThan(0);
        expect(rendered).toBeLessThan(120);
    });
});

describe('TaskList rows', () => {
    beforeEach(() => {
        Object.values(taskServiceMock).forEach(mock => mock.mockReset());
        teamMock.getByIteration.mockResolvedValue([{ id: 5, name: 'Ada' }]);
        taskServiceMock.getDetail.mockImplementation(async (id: number) => taskDetailResponse({ ...task(id), status: 'resolved' }, null));
        labelServiceMock.getGroups.mockReset();
        labelServiceMock.getGroups.mockResolvedValue([]);
    });

    it('shows at most four interactive parts at rest, the checkbox always, and the menu on hover and focus', async () => {
        taskServiceMock.getByIteration.mockResolvedValue([task(1), task(2)]);
        const { user } = renderWithProviders(<TaskList iterationId={1} sortKey="priority" />);
        await screen.findByRole('button', { name: 'Task 1' });

        const row = rowOf('Task 1');
        expect(row).toHaveClass('h-11');
        const atRest = Array.from(row.querySelectorAll(INTERACTIVE));
        expect(atRest.length).toBeLessThanOrEqual(4);
        expect(within(row).getByRole('button', { name: /Status: Planned/ })).toBeInTheDocument();
        expect(within(row).getByRole('button', { name: 'Task 1' })).toBeInTheDocument();
        expect(within(row).getByRole('combobox', { name: 'Assignee: Task 1' })).toBeInTheDocument();
        expect(within(row).getByRole('checkbox', { name: 'Select: Task 1' })).toBeInTheDocument();
        expect(within(row).queryByRole('button', { name: 'Actions for Task 1' })).toBeNull();

        hover(row);
        expect(within(row).getByRole('checkbox', { name: 'Select: Task 1' })).toBeInTheDocument();
        expect(within(row).getByRole('button', { name: 'Actions for Task 1' })).toBeInTheDocument();
        unhover(row);
        expect(within(row).getByRole('checkbox', { name: 'Select: Task 1' })).toBeInTheDocument();
        expect(within(row).queryByRole('button', { name: 'Actions for Task 1' })).toBeNull();

        await user.click(within(row).getByRole('button', { name: 'Task 1' }));
        within(row).getByRole('button', { name: 'Task 1' }).focus();
        expect(await within(row).findByRole('checkbox', { name: 'Select: Task 1' })).toBeInTheDocument();
        expect(within(row).getByRole('button', { name: 'Actions for Task 1' })).toBeInTheDocument();

        // With a selection active, every row shows its checkbox, but an untouched row keeps its menu hidden.
        hover(row);
        fireEvent.click(within(row).getByRole('checkbox', { name: 'Select: Task 1' }));
        expect(within(row).getByRole('checkbox', { name: 'Select: Task 1' })).toBeChecked();
        (document.activeElement as HTMLElement | null)?.blur();
        unhover(row);
        for (const title of ['Task 1', 'Task 2']) {
            const untouched = rowOf(title);
            expect(within(untouched).getByRole('checkbox', { name: `Select: ${title}` })).toBeInTheDocument();
            expect(within(untouched).queryByRole('button', { name: `Actions for ${title}` })).toBeNull();
            expect(untouched.querySelectorAll(INTERACTIVE).length).toBeLessThanOrEqual(4);
        }
        hover(rowOf('Task 2'));
        expect(within(rowOf('Task 2')).getByRole('button', { name: 'Actions for Task 2' })).toBeInTheDocument();
    });

    it('shows a selection control on every row at rest, off with its reason on parent and composite rows', async () => {
        const parent = { ...task(3), children: [{ ...task(4), parent_id: 3 }] };
        const composite = { ...task(5), is_composite: true };
        taskServiceMock.getByIteration.mockResolvedValue([task(1), task(2), parent, composite]);
        const host = document.createElement('div');
        document.body.appendChild(host);
        renderWithProviders(<TaskList iterationId={1} sortKey="priority" selectionBarHost={host} />);
        await screen.findByRole('button', { name: 'Task 1' });

        const reason = 'This task is made of subtasks and changes through them. Select its subtasks instead.';
        for (const title of ['Task 1', 'Task 2', 'Task 3', 'Task 4', 'Task 5']) {
            const box = within(rowOf(title)).getByRole('checkbox', { name: `Select: ${title}` });
            expect(box).toBeVisible();
            if (title === 'Task 3' || title === 'Task 5') {
                expect(box).toBeDisabled();
                expect(box).toHaveAccessibleDescription(reason);
                expect(box).toHaveAttribute('title', reason);
            } else {
                expect(box).toBeEnabled();
                expect(box).not.toHaveAttribute('aria-describedby');
            }
        }

        // A parent row's checkbox cannot be ticked; its subtask's can, and the bar shows in the toolbar's place.
        fireEvent.click(within(rowOf('Task 3')).getByRole('checkbox', { name: 'Select: Task 3' }));
        expect(within(host).queryByTestId('task-bulk-operations')).toBeNull();
        fireEvent.click(within(rowOf('Task 4')).getByRole('checkbox', { name: 'Select: Task 4' }));
        expect(await within(host).findByText('Selected tasks: 1')).toBeInTheDocument();
        expect(within(rowOf('Task 4')).getByRole('checkbox', { name: 'Select: Task 4' })).toBeChecked();
        expect(within(rowOf('Task 3')).getByRole('checkbox', { name: 'Select: Task 3' })).not.toBeChecked();
        host.remove();
    });

    it('keeps rows in manual order to four interactive parts, with the drag handle on hover and focus only', async () => {
        const parent = { ...task(3), children: [{ ...task(4), parent_id: 3 }] };
        taskServiceMock.getByIteration.mockResolvedValue([task(1), task(2), parent]);
        renderWithProviders(<TaskList iterationId={1} sortKey="sort_order" />);
        await screen.findByRole('button', { name: 'Task 1' });

        const titles = ['Task 1', 'Task 2', 'Task 3', 'Task 4'];
        for (const title of titles) {
            expect(within(rowOf(title)).queryByRole('button', { name: `Drag: ${title}` })).toBeNull();
            expect(rowOf(title).querySelectorAll(INTERACTIVE).length).toBeLessThanOrEqual(4);
        }

        // Hover and keyboard focus reveal the handle, so dragging stays reachable.
        hover(rowOf('Task 1'));
        expect(within(rowOf('Task 1')).getByRole('button', { name: 'Drag: Task 1' })).toBeInTheDocument();
        unhover(rowOf('Task 1'));
        expect(within(rowOf('Task 1')).queryByRole('button', { name: 'Drag: Task 1' })).toBeNull();
        within(rowOf('Task 2')).getByRole('button', { name: 'Task 2' }).focus();
        expect(await within(rowOf('Task 2')).findByRole('button', { name: 'Drag: Task 2' })).toBeInTheDocument();
        (document.activeElement as HTMLElement | null)?.blur();

        // With a selection active, every selectable row shows its checkbox and still stays within four parts.
        hover(rowOf('Task 1'));
        fireEvent.click(within(rowOf('Task 1')).getByRole('checkbox', { name: 'Select: Task 1' }));
        unhover(rowOf('Task 1'));
        await waitFor(() => expect(within(rowOf('Task 2')).queryByRole('button', { name: 'Drag: Task 2' })).toBeNull());
        for (const title of titles) {
            const row = rowOf(title);
            // A parent is not selected itself; its leaf tasks are, so its checkbox shows but is off.
            if (title === 'Task 3') {
                expect(within(row).getByRole('button', { name: 'Collapse all: Task 3' })).toBeInTheDocument();
                expect(within(row).getByRole('checkbox', { name: 'Select: Task 3' })).toBeDisabled();
            } else expect(within(row).getByRole('checkbox', { name: `Select: ${title}` })).toBeEnabled();
            expect(within(row).queryByRole('button', { name: `Drag: ${title}` })).toBeNull();
            expect(within(row).queryByRole('button', { name: `Actions for ${title}` })).toBeNull();
            expect(row.querySelectorAll(INTERACTIVE).length).toBeLessThanOrEqual(4);
        }
    });

    it('assigns ten tasks in five interactions: tick one, shift-click the tenth, Assign, choose, apply', async () => {
        const tasks = Array.from({ length: 12 }, (_, index) => task(index + 1));
        taskServiceMock.getByIteration.mockResolvedValue(tasks);
        const versions = Object.fromEntries(tasks.map(item => [item.id, 1]));
        taskServiceMock.runBulkOperation.mockImplementation(async (request: { dry_run: boolean; task_ids: number[] }) => ({
            dry_run: request.dry_run, requested_count: request.task_ids.length, succeeded_count: request.task_ids.length, failed_count: 0,
            task_versions: versions, input_revisions: { 1: 3 },
            results: request.task_ids.map(id => ({ task_id: id, outcome: request.dry_run ? 'would_update' : 'updated', changes: {}, warnings: [] })),
        }));
        const { user } = renderWithProviders(<TaskList iterationId={1} sortKey="priority" />);
        await screen.findByRole('button', { name: 'Task 1' });

        // Pointing at the row reveals its checkbox; the five interactions are the clicks and the choice.
        hover(rowOf('Task 1'));
        await user.click(screen.getByRole('checkbox', { name: 'Select: Task 1' }));                       // 1
        await user.keyboard('{Shift>}');
        await user.click(screen.getByRole('checkbox', { name: 'Select: Task 10' }));                      // 2
        await user.keyboard('{/Shift}');
        expect(screen.getByText('Selected tasks: 10')).toBeInTheDocument();
        await user.click(screen.getByRole('button', { name: 'Assign' }));                                 // 3
        await user.selectOptions(screen.getByRole('combobox', { name: 'Choose assignee' }), 'Ada');       // 4
        await user.click(screen.getByRole('button', { name: 'Apply' }));                                  // 5

        await waitFor(() => expect(taskServiceMock.runBulkOperation).toHaveBeenCalledTimes(2));
        const applied = taskServiceMock.runBulkOperation.mock.calls.at(-1)![0];
        expect(applied).toMatchObject({ action: 'set_assignee', payload: { assignee_id: 5 }, dry_run: false });
        expect(applied.task_ids).toEqual([1, 2, 3, 4, 5, 6, 7, 8, 9, 10]);
        await waitFor(() => expect(screen.queryByTestId('task-bulk-operations')).toBeNull());
    });

    it('offers Status, Priority, Iteration, Merge for two or more, and Select all n matching in the bar', async () => {
        taskServiceMock.getByIteration.mockResolvedValue([task(1), task(2), task(3)]);
        const { user } = renderWithProviders(<TaskList iterationId={1} sortKey="priority" />);
        await screen.findByRole('button', { name: 'Task 1' });
        hover(rowOf('Task 1'));
        await user.click(screen.getByRole('checkbox', { name: 'Select: Task 1' }));

        const bar = screen.getByTestId('task-bulk-operations');
        for (const name of ['Assign', 'Status', 'Priority', 'Iteration', 'Select all 3 matching tasks']) {
            expect(within(bar).getByRole('button', { name })).toBeInTheDocument();
        }
        expect(within(bar).queryByRole('button', { name: /^Merge/ })).toBeNull();
        await user.click(within(bar).getByRole('button', { name: 'Select all 3 matching tasks' }));
        expect(screen.getByText('Selected tasks: 3')).toBeInTheDocument();
        expect(within(bar).getByRole('button', { name: 'Merge (3)' })).toBeInTheDocument();
        await user.click(within(bar).getByRole('button', { name: 'Clear selection' }));
        expect(screen.queryByTestId('task-bulk-operations')).toBeNull();
    });

    it('reaches every part of a row by keyboard and lists the actions the icons used to hold in the row menu', async () => {
        taskServiceMock.getByIteration.mockResolvedValue([{ ...task(1), tags: ['backend'] }]);
        const onOpenTask = vi.fn();
        const { user } = renderWithProviders(<TaskList iterationId={1} sortKey="priority" onOpenTask={onOpenTask} />);
        await screen.findByRole('button', { name: 'Task 1' });
        const row = rowOf('Task 1');

        within(row).getByRole('button', { name: /Status: Planned/ }).focus();
        const checkbox = await within(row).findByRole('checkbox', { name: 'Select: Task 1' });
        await user.tab({ shift: true });
        expect(checkbox).toHaveFocus();
        await user.tab();
        expect(within(row).getByRole('button', { name: /Status: Planned/ })).toHaveFocus();
        await user.tab();
        expect(within(row).getByRole('button', { name: 'Task 1' })).toHaveFocus();
        await user.tab();
        expect(within(row).getByRole('combobox', { name: 'Assignee: Task 1' })).toHaveFocus();
        await user.tab();
        const menu = within(row).getByRole('button', { name: 'Actions for Task 1' });
        expect(menu).toHaveFocus();

        await user.keyboard('{Enter}');
        const items = screen.getAllByRole('menuitem').map(item => item.textContent);
        expect(items).toEqual(['Details (2)', 'Edit task', 'Add subtask', 'Delete']);
        await user.keyboard('{ArrowDown}{Enter}');
        expect(onOpenTask).toHaveBeenCalledWith(expect.objectContaining({ id: 1 }));

        // The checkbox is the part before the status: Space ticks it.
        checkbox.focus();
        await user.keyboard(' ');
        expect(screen.getByText('Selected tasks: 1')).toBeInTheDocument();
    });

    it('changes the status and the assignee from the row', async () => {
        taskServiceMock.getByIteration.mockResolvedValue([task(1)]);
        taskServiceMock.update.mockResolvedValue({ ...task(1), assignee: { id: 5, name: 'Ada' } });
        taskServiceMock.changeStatus.mockResolvedValue({ task: { ...task(1), status: 'active' }, cascade_updates: [] });
        const { user } = renderWithProviders(<TaskList iterationId={1} sortKey="priority" />);
        await screen.findByRole('button', { name: 'Task 1' });
        const row = rowOf('Task 1');

        await user.selectOptions(await within(row).findByRole('option', { name: 'Ada' }).then(option => option.closest('select')!), 'Ada');
        await waitFor(() => expect(taskServiceMock.update).toHaveBeenCalledWith(1, { assignee_id: 5, expected_version: 1 }));

        await user.click(within(row).getByRole('button', { name: /Status: Planned/ }));
        await user.click(screen.getByRole('menuitem', { name: 'Active' }));
        await waitFor(() => expect(taskServiceMock.changeStatus).toHaveBeenCalledWith(1, 'active', undefined, 1));
    });

    it('shows the agent status under the name of an agent assignee and the Reviewer beside it', async () => {
        const agent = { id: 6, name: 'Build agent' };
        teamMock.getByIteration.mockResolvedValue([
            { id: 5, name: 'Ada', profile_id: 50, profile: { id: 50, profile_kind: 'human' } },
            { id: 6, name: 'Build agent', profile_id: 60, profile: { id: 60, profile_kind: 'agent' } },
        ]);
        taskServiceMock.getDetail.mockImplementation(async (id: number) => taskDetailResponse({ ...task(id), status: 'resolved' }, id === 3 ? 'Review bot' : null));
        taskServiceMock.getByIteration.mockResolvedValue([
            { ...task(1), assignee: agent, agent_working: true },
            { ...task(2), assignee: agent, agent_working: true, claimed_by: { id: 3, name: 'builder', display_name: 'Builder' }, status: 'active' },
            { ...task(3), assignee: agent, agent_working: false, status: 'resolved' },
            { ...task(4), assignee: { id: 5, name: 'Ada' }, agent_working: false },
        ]);
        renderWithProviders(<TaskList iterationId={1} sortKey="priority" groupByStatus={false} />);
        await screen.findByRole('button', { name: 'Task 1' });
        const lineOf = (title: string) => rowOf(title).querySelector('[data-agent-dispatch]')?.textContent;
        await waitFor(() => expect(lineOf('Task 1')).toBe('Agent status: Queued'));
        expect(lineOf('Task 2')).toBe('Agent status: Working');
        expect(lineOf('Task 3')).toBe('Agent status: Waiting for review');
        expect(lineOf('Task 4')).toBeUndefined();
        await waitFor(() => expect(rowOf('Task 3')).toHaveTextContent('Reviewer: Review bot'));
        // The Reviewer is read from the task detail, for the submitted task only.
        expect(taskServiceMock.getDetail.mock.calls.map(([id, params]) => [id, params])).toEqual([[3, { limit: 1 }]]);
        // Neither line is something to reach: the row keeps status, title and assignee at rest.
        expect(rowOf('Task 3').querySelectorAll(INTERACTIVE).length).toBeLessThanOrEqual(4);
    });

    it('names the Reviewer of every submitted task shown, reading them in bounded pages', async () => {
        const submitted = Array.from({ length: 45 }, (_, index) => ({ ...task(index + 1), status: 'resolved' as const }));
        taskServiceMock.getByIteration.mockResolvedValue([...submitted, task(46)]);
        taskServiceMock.getDetail.mockImplementation(async (id: number) => taskDetailResponse(submitted[id - 1], `Reviewer bot ${id}`));
        const queryClient = createTestQueryClient();
        renderWithProviders(<TaskList iterationId={1} sortKey="priority" groupByStatus={false} />, { queryClient });
        await screen.findByRole('button', { name: 'Task 45' });
        // Tasks past the first page keep their Reviewer too.
        await waitFor(() => expect(rowOf('Task 45')).toHaveTextContent('Reviewer: Reviewer bot 45'));
        submitted.forEach(item => expect(rowOf(item.title)).toHaveTextContent(`Reviewer: Reviewer bot ${item.id}`));
        // One read per submitted task shown, never for the open one, each asking for the smallest context page.
        const readIds = taskServiceMock.getDetail.mock.calls.map(([id]) => id as number).sort((a, b) => a - b);
        expect(readIds).toEqual(submitted.map(item => item.id));
        taskServiceMock.getDetail.mock.calls.forEach(([, params]) => expect(params).toEqual({ limit: 1 }));
        expect(rowOf('Task 46').querySelector('[data-reviewer-cell]')).toBeEmptyDOMElement();
        // The reads come in pages of at most REVIEWER_PAGE_SIZE tasks.
        const pages = queryClient.getQueryCache().findAll({ queryKey: ['tasks', 'reviewers'] }).map(query => String(query.queryKey[2]).split(',').length);
        expect(pages).toEqual([REVIEWER_PAGE_SIZE, REVIEWER_PAGE_SIZE, 45 - 2 * REVIEWER_PAGE_SIZE]);
    });

    it('names one state chip, chosen by priority', async () => {
        const waiting = { ...task(3), dependencies: [1] };
        taskServiceMock.getByIteration.mockResolvedValue([
            { ...task(1), blocked_reason: 'Waiting on legal', agent_readiness: { ...task(1).agent_readiness, definition_ready: false, start_ready: false } },
            { ...task(2), agent_readiness: { ...task(2).agent_readiness, definition_ready: false, start_ready: false } },
            { ...waiting, agent_readiness: { ...waiting.agent_readiness, definition_ready: true, start_ready: false } },
            { ...task(4), agent_readiness: { ...task(4).agent_readiness, definition_ready: true, start_ready: true } },
            { ...task(5), status: 'resolved' },
        ]);
        renderWithProviders(<TaskList iterationId={1} sortKey="priority" groupByStatus={false} />);
        await screen.findByRole('button', { name: 'Task 1' });
        const chipText = (title: string) => rowOf(title).querySelector('span.rounded-full')?.textContent;
        expect(chipText('Task 1')).toBe('Blocked');
        expect(chipText('Task 2')).toBe('Needs definition');
        expect(chipText('Task 3')).toBe('Waits for 1');
        expect(chipText('Task 4')).toBe('Ready to start');
        expect(chipText('Task 5')).toBe('In review');
        expect(rowOf('Task 1').querySelectorAll('span.rounded-full')).toHaveLength(1);
    });
});

describe('TaskList empty states', () => {
    const noFilters = {
        planningIssue: null, assigneeId: null, projectId: null, milestoneId: null, needsAttention: null, priority: null,
        status: null, hasDependency: null, isOverdue: null, agentReady: null, startDateFrom: '', startDateTo: '',
    } as unknown as TaskFilters;

    it('offers Clear filters, not a create action, when the filters hide every task (AC2)', async () => {
        taskServiceMock.getByIteration.mockResolvedValue([task(1), task(2)].map(value => ({ ...value, iteration_revision: 1 })));
        const onCreateTask = vi.fn();
        const onClearFilters = vi.fn();
        const { user } = renderWithProviders(
            <TaskList iterationId={1} sortKey="priority" filters={{ ...noFilters, status: 'no-such-status' }}
                hasActiveFilters onClearFilters={onClearFilters} onCreateTask={onCreateTask} />,
        );
        await user.click(await screen.findByRole('button', { name: 'Clear filters' }));
        expect(onClearFilters).toHaveBeenCalledTimes(1);
        expect(screen.queryByRole('button', { name: /new task/i })).not.toBeInTheDocument();
        expect(onCreateTask).not.toHaveBeenCalled();
    });

    it('shows why each task is at risk when opened from the at-risk signals', async () => {
        taskServiceMock.getByIteration.mockResolvedValue([
            { ...task(1), is_delayed: true, iteration_revision: 1 },
            { ...task(2), is_overdue: true, iteration_revision: 1 },
        ]);
        renderWithProviders(<TaskList iterationId={1} sortKey="priority" filters={{ ...defaultFilters, planningIssue: 'at-risk' }} />);
        expect(await screen.findByText('Not started by its planned start')).toBeInTheDocument();
        expect(screen.getByText('Past its end date')).toBeInTheDocument();
    });

    it('names the missed planned start, not a past start, when the baseline start has passed but the current start is ahead', async () => {
        const day = (offset: number) => new Date(Date.now() + offset * 86_400_000).toISOString().slice(0, 10);
        taskServiceMock.getByIteration.mockResolvedValue([
            { ...task(1), is_delayed: true, status: 'planned', baseline_start_date: day(-5), start_date: day(5), end_date: day(9),
                actual_start_date: null, iteration_revision: 1 },
        ]);
        renderWithProviders(<TaskList iterationId={1} sortKey="priority" filters={{ ...defaultFilters, planningIssue: 'at-risk' }} />);
        expect(await screen.findByText('Not started by its planned start')).toBeInTheDocument();
        expect(screen.queryByText(/before today/i)).not.toBeInTheDocument();
        expect(screen.queryByText('Started after its planned start')).not.toBeInTheDocument();
    });

    it('lists a task whose only risk is outside its date limits, using the dates the Tasks list receives', async () => {
        taskServiceMock.getByIteration.mockResolvedValue([
            { ...task(1), start_date: '2026-08-03', min_start_date: '2026-08-05', iteration_revision: 1 },
            { ...task(2), iteration_revision: 1 },
        ]);
        renderWithProviders(<TaskList iterationId={1} sortKey="priority" filters={{ ...defaultFilters, planningIssue: 'at-risk' }} />);
        expect(await screen.findByText('Outside its date limits')).toBeInTheDocument();
        expect(screen.getByText('Task 1')).toBeInTheDocument();
        expect(screen.queryByText('Task 2')).not.toBeInTheDocument();
    });

    it('says a task started late when it began after its planned start, not that it has not started', async () => {
        taskServiceMock.getByIteration.mockResolvedValue([
            { ...task(1), is_delayed: true, status: 'active', baseline_start_date: '2026-08-03', actual_start_date: '2026-08-06', iteration_revision: 1 },
        ]);
        renderWithProviders(<TaskList iterationId={1} sortKey="priority" filters={{ ...defaultFilters, planningIssue: 'at-risk' }} />);
        expect(await screen.findByText('Started after its planned start')).toBeInTheDocument();
        expect(screen.queryByText('Not started by its planned start')).not.toBeInTheDocument();
    });

    it('offers the one next step when the iteration has no tasks yet', async () => {
        taskServiceMock.getByIteration.mockResolvedValue([]);
        const onCreateTask = vi.fn();
        const { user } = renderWithProviders(
            <TaskList iterationId={1} sortKey="priority" filters={noFilters} onCreateTask={onCreateTask} />,
        );
        expect(await screen.findByText('No tasks yet')).toBeInTheDocument();
        expect(screen.queryByRole('button', { name: 'Clear filters' })).not.toBeInTheDocument();
        await user.click(screen.getByRole('button', { name: 'New task' }));
        expect(onCreateTask).toHaveBeenCalledTimes(1);
    });
});

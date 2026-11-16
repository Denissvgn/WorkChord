import { beforeEach, describe, expect, it, vi } from 'vitest';
import { act, fireEvent, screen, waitFor, within } from '@testing-library/react';
import type { Task } from '../../types/task';
import { createTestQueryClient, renderWithProviders } from '../../test/renderWithProviders';
import { REVIEWER_PAGE_SIZE } from './useAgentRowFacts';
import { TaskList } from './TaskList';
import { taskDetailResponse } from '../../test/fixtures/taskDetail';

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
            { ...task(1), status: 'planned' }, { ...task(2), status: 'active' }, { ...task(3), status: 'planned' }, { ...task(4), status: 'closed' },
        ]);
        const { user, rerender } = renderWithProviders(<TaskList iterationId={1} sortKey="priority" />);
        const groups = await screen.findAllByRole('heading', { level: 2 });
        expect(groups.map(group => group.textContent)).toEqual(['Active1 task', 'Planned2 tasks', 'Closed1 task']);
        expect(screen.getByRole('button', { name: /Closed/ })).toHaveAttribute('aria-expanded', 'false');
        expect(screen.queryByRole('button', { name: 'Task 4' })).toBeNull();
        await user.click(screen.getByRole('button', { name: /Closed/ }));
        expect(screen.getByRole('button', { name: 'Task 4' })).toBeInTheDocument();
        rerender(<TaskList iterationId={1} sortKey="priority" groupByStatus={false} />);
        expect(screen.queryByRole('heading', { level: 2 })).toBeNull();
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

    it('shows at most four interactive parts at rest and the checkbox and menu on hover and focus', async () => {
        taskServiceMock.getByIteration.mockResolvedValue([task(1), task(2)]);
        const { user } = renderWithProviders(<TaskList iterationId={1} sortKey="priority" />);
        await screen.findByRole('button', { name: 'Task 1' });

        const row = rowOf('Task 1');
        expect(row.className).toContain('min-h-11');
        const atRest = Array.from(row.querySelectorAll(INTERACTIVE));
        expect(atRest.length).toBeLessThanOrEqual(4);
        expect(within(row).getByRole('button', { name: /Status: Planned/ })).toBeInTheDocument();
        expect(within(row).getByRole('button', { name: 'Task 1' })).toBeInTheDocument();
        expect(within(row).getByRole('combobox', { name: 'Assignee: Task 1' })).toBeInTheDocument();
        expect(within(row).queryByRole('checkbox')).toBeNull();
        expect(within(row).queryByRole('button', { name: 'Actions for Task 1' })).toBeNull();

        hover(row);
        expect(within(row).getByRole('checkbox', { name: 'Select: Task 1' })).toBeInTheDocument();
        expect(within(row).getByRole('button', { name: 'Actions for Task 1' })).toBeInTheDocument();
        unhover(row);
        expect(within(row).queryByRole('checkbox')).toBeNull();

        await user.click(within(row).getByRole('button', { name: 'Task 1' }));
        within(row).getByRole('button', { name: 'Task 1' }).focus();
        expect(await within(row).findByRole('checkbox', { name: 'Select: Task 1' })).toBeInTheDocument();
        expect(within(row).getByRole('button', { name: 'Actions for Task 1' })).toBeInTheDocument();
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

    it('shows the agent status line under an agent assignee and the Reviewer beside it', async () => {
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

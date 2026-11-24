import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { act, screen, waitFor, within } from '@testing-library/react';
import { Route, Routes, useLocation } from 'react-router-dom';
import { renderWithProviders } from '../test/renderWithProviders';
import { expectPageChrome } from '../test/pageChrome';
import { useScopeStore } from '../features/scope/scopeStore';
import { useGetStartedVisibility } from '../features/firstRun/getStartedVisibility';
import type { AgentPipeline } from '../types/agent';
import type { Iteration, PlanCheckpoint } from '../types/iteration';
import type { Task, TaskReference } from '../types/task';
import i18n from '../i18n/i18n';
import OverviewPage from './OverviewPage';
import TasksPage from './TasksPage';
import { CommandMenu } from '../components/layout/CommandMenu';

const api = vi.hoisted(() => ({
    iterations: vi.fn(),
    readiness: vi.fn(),
    tasks: vi.fn(),
    pipeline: vi.fn(),
    task: vi.fn(),
    lookup: vi.fn(),
    iteration: vi.fn(),
    create: vi.fn(),
    projects: vi.fn(),
}));
const access = vi.hoisted(() => ({ hasAdminKey: true }));

vi.mock('../hooks/useAdminAccess', () => ({ useAdminAccess: () => access, useKeylessReader: () => ({ workViews: access.hasAdminKey }) }));
vi.mock('../hooks/useAgentAccess', () => ({ useAgentAccess: () => ({ hasAgentKey: false }) }));
vi.mock('../services/agentService', () => ({ agentService: { getPipeline: api.pipeline, getTaskTimeline: vi.fn().mockResolvedValue({ items: [] }) } }));
vi.mock('../services/iterationService', () => ({
    iterationService: {
        getAll: api.iterations,
        getPlanningReadiness: api.readiness,
        getById: api.iteration,
    },
}));
vi.mock('../services/taskService', () => ({
    taskService: {
        getByIteration: api.tasks,
        getById: api.task,
        lookup: api.lookup,
        create: api.create,
        ownerOptions: vi.fn().mockResolvedValue({ items: [], has_more: false }),
    },
}));
vi.mock('../services/savedViewService', () => ({ savedViewService: { getAll: vi.fn().mockResolvedValue([]) } }));
vi.mock('../services/labelService', () => ({ labelService: { getGroups: vi.fn().mockResolvedValue([]) } }));
vi.mock('../services/sessionService', () => ({ sessionService: { getWhoAmI: vi.fn().mockResolvedValue({ id: 3 }) } }));
vi.mock('../services/projectService', () => ({ projectService: { getAll: api.projects, getMilestones: vi.fn().mockResolvedValue([]) } }));
vi.mock('../services/teamService', () => ({ teamService: { getByIteration: vi.fn().mockResolvedValue([]) } }));
vi.mock('../services/triageService', () => ({ triageService: { getAll: vi.fn().mockResolvedValue([]) } }));
vi.mock('../components/tasks/TaskAgentReadinessBadge', () => ({ TaskAgentReadinessBadge: () => null }));

const TODAY = '2026-11-16';

const iteration = (id: number, projectId: number, projectName: string, start: string, end: string): Iteration => ({
    id,
    name: `Iteration ${id}`,
    calendar_id: 1,
    project_id: projectId,
    project: { id: projectId, name: projectName, status: 'active', health: 'green' },
    start_date: start,
    end_date: end,
    working_days: 20,
});

// Iteration 12 of Alpha and iteration 21 of Beta are open today; iteration 11 has ended.
const ITERATIONS = [
    iteration(11, 1, 'Alpha', '2026-10-01', '2026-10-31'),
    iteration(12, 1, 'Alpha', '2026-11-02', '2026-11-27'),
    iteration(21, 2, 'Beta', '2026-11-09', '2026-12-04'),
];

const task = (id: number, overrides: Partial<Task> = {}): Task => ({
    id,
    iteration_id: 12,
    project_id: 1,
    milestone_id: null,
    parent_id: null,
    title: `Task ${id}`,
    description: '',
    priority: 3,
    effort_days: 1,
    effort_hours: 8,
    project: { id: 1, name: 'Alpha' },
    milestone: null,
    assignee: { id: 5, name: 'Ada Byron' },
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
    agent_readiness: { is_ready: false, blockers: [], warnings: [], criteria: [] },
    version: 1,
    children: [],
    dependencies: [],
    ...overrides,
} as Task);

/**
 * Iteration 12: 2 closed, 1 resolved, 2 at risk, 1 blocked, 2 unassigned, 9 tasks in all.
 * Task 101 is closed but still flagged as a late start; finished work is never at risk.
 */
const ALPHA_TASKS = [
    task(101, { status: 'closed', is_delayed: true }),
    task(102, { status: 'closed' }),
    task(103, { status: 'resolved' }),
    task(104, { status: 'active', is_overdue: true }),
    task(105, { is_delayed: true }),
    task(106, { status: 'active', blocked_reason: 'Waiting for the vendor key' }),
    task(107, { assignee: null }),
    task(108, { assignee: null }),
    task(109),
];

/** Iteration 21: 1 closed, 1 at risk, 4 tasks in all. */
const BETA_TASKS = [
    task(201, { iteration_id: 21, project_id: 2, project: { id: 2, name: 'Beta' } as Task['project'], status: 'closed' }),
    task(202, { iteration_id: 21, project_id: 2, project: { id: 2, name: 'Beta' } as Task['project'], is_overdue: true }),
    task(203, { iteration_id: 21, project_id: 2, project: { id: 2, name: 'Beta' } as Task['project'] }),
    task(204, { iteration_id: 21, project_id: 2, project: { id: 2, name: 'Beta' } as Task['project'] }),
];

/** Iteration 11 has ended; with All projects its tasks are not counted. */
const PAST_TASKS = [task(301, { iteration_id: 11, status: 'closed' }), task(302, { iteration_id: 11 })];

const TASKS_BY_ITERATION: Record<number, Task[]> = { 11: PAST_TASKS, 12: ALPHA_TASKS, 21: BETA_TASKS };

const STAGES: (keyof AgentPipeline)[] = [
    'needs_definition', 'ready_to_assign', 'assigned_waiting', 'start_ready', 'executing', 'verification_required', 'recovery_required',
];

/** Stage sizes for iteration 12, plus tasks of other scopes that the counts must leave out. */
const pipelineResponse = (): AgentPipeline => ({
    needs_definition: [task(107, { assignee: null }), task(108, { assignee: null })],
    ready_to_assign: [task(109)],
    assigned_waiting: [task(105)],
    start_ready: [],
    executing: [task(104, { status: 'active' }), task(106, { status: 'active' }), task(203, { iteration_id: 21, project_id: 2 })],
    verification_required: [task(103, { status: 'resolved' }), task(204, { iteration_id: 21, project_id: 2, status: 'resolved' })],
    recovery_required: [task(401, { iteration_id: 11 })],
});

const checkpoints = (done: number): PlanCheckpoint[] => (
    ['iteration', 'team', 'work', 'blockers', 'schedule', 'review'] as PlanCheckpoint['id'][]
).map((id, index) => ({ id, state: index < done ? 'done' : 'todo', reason_codes: [], counts: {} }));

const readinessResponse = (done = 6) => ({
    iteration_id: 12,
    team_member_count: 2,
    team_capacity_hours: 80,
    team_members_no_capacity: 0,
    task_count: 9,
    tasks_without_assignee: 0,
    tasks_without_effort: 0,
    has_schedule: true,
    risk_count: 0,
    checkpoints: checkpoints(done),
    checkpoints_done: done,
    checkpoints_total: 6,
});

const LocationProbe = () => {
    const location = useLocation();
    return <output data-testid="location">{`${location.pathname}${location.search}`}</output>;
};

const renderOverview = (url = '/?project=1&iteration=12') => renderWithProviders(
    <>
        <Routes>
            <Route path="/" element={<OverviewPage />} />
            <Route path="/tasks" element={<TasksPage />} />
            <Route path="*" element={<p>Other page</p>} />
        </Routes>
        <LocationProbe />
    </>,
    { initialEntries: [url] },
);

const figure = (testId: string) => screen.findByTestId(testId);
const searchOf = () => new URLSearchParams(screen.getByTestId('location').textContent?.split('?')[1] ?? '');

/** The status groups of the Tasks list; each header names its status and its count. */
const listGroups = () => screen.findAllByRole('button', { name: new RegExp(`${i18n.t('taskList.groupCount', { count: 2 }).replace('2', '\\d+').replace(/s$/, 's?')}$`) });

/** Opens every status group of the Tasks list, then counts the task rows it renders. */
const countListRows = async (user: ReturnType<typeof renderOverview>['user']) => {
    for (const group of await listGroups()) {
        if (group.getAttribute('aria-expanded') === 'false') await user.click(group);
    }
    return screen.getAllByRole('button', { name: /^Task \d+$/ }).length;
};

/** Overview's own list, opened from a count: the rows it holds, or none when it is empty. */
const ownListRows = async () => {
    const drawer = await screen.findByRole('dialog');
    await waitFor(() => expect(within(drawer).queryByRole('status')).not.toBeInTheDocument());
    const list = within(drawer).queryByTestId('overview-count-list');
    if (!list) {
        expect(within(drawer).getByText(i18n.t('overview.list.empty'))).toBeInTheDocument();
        return [];
    }
    return within(list).getAllByRole('link').map(link => link.getAttribute('aria-label'));
};

const unavailable = () => Object.assign(new Error('Service unavailable'), { response: { status: 503 } });

const reference = (id: number, overrides: Partial<TaskReference> = {}): TaskReference => ({
    id,
    title: `Backlog ${id}`,
    version: 1,
    status: 'planned',
    project_id: 1,
    project_name: 'Alpha',
    iteration_id: null,
    parent_id: null,
    owner_profile_id: null,
    blocked_reason: null,
    ...overrides,
});

/** Alpha's backlog: 1 closed, 1 blocked and open, 1 closed with a blocker left in place, 5 tasks in all. */
const BACKLOG = [
    reference(501, { status: 'closed' }),
    reference(502, { blocked_reason: 'Needs a decision' }),
    reference(503, { status: 'closed', blocked_reason: 'Left over' }),
    reference(504),
    reference(505, { status: 'active' }),
];

describe('Overview', () => {
    beforeEach(() => {
        vi.useFakeTimers({ toFake: ['Date'] });
        vi.setSystemTime(new Date(`${TODAY}T10:00:00`));
        vi.clearAllMocks();
        access.hasAdminKey = true;
        useScopeStore.setState({ project: null, iteration: null });
        api.iterations.mockResolvedValue(ITERATIONS);
        api.readiness.mockResolvedValue(readinessResponse());
        api.tasks.mockImplementation(async (id: number) => TASKS_BY_ITERATION[id] ?? []);
        api.pipeline.mockResolvedValue(pipelineResponse());
        api.task.mockImplementation(async (id: number) => task(id));
        api.iteration.mockImplementation(async (id: number) => ITERATIONS.find(item => item.id === id));
        api.projects.mockResolvedValue([]);
        api.create.mockImplementation(async (iterationId: number | null, data: Partial<Task>) => task(900, { ...data, iteration_id: iterationId }));
        api.lookup.mockImplementation(async (params: { backlog_only?: boolean; project_id?: number }) => ({
            items: params.backlog_only && params.project_id === 1 ? BACKLOG : [],
            has_more: false,
            next_after_id: null,
            limit: 100,
        }));
        Element.prototype.scrollIntoView = vi.fn();
    });

    afterEach(() => {
        vi.useRealTimers();
    });

    it('shows one attention item, Work now, Agents now and three figures, and passes the page chrome check', async () => {
        api.projects.mockResolvedValue([{ id: 1, name: 'Alpha' }]);
        const { container } = renderOverview();

        const attention = await screen.findByRole('region', { name: i18n.t('overview.attentionItem.blocked', { count: 1 }) });
        expect(container.querySelectorAll('.overview-attention')).toHaveLength(1);
        expect(within(attention).getAllByRole('link')).toHaveLength(1);
        expect(screen.getByRole('heading', { level: 2, name: i18n.t('overview.workNow') })).toBeInTheDocument();
        expect(screen.getByRole('heading', { level: 2, name: i18n.t('overview.agentsNow') })).toBeInTheDocument();
        const onTrack = screen.getByRole('region', { name: i18n.t('overview.onTrack') });
        const figures = within(onTrack).getAllByRole('term').map(term => term.textContent);
        expect(figures).toEqual([
            i18n.t('overview.figures.done'),
            i18n.t('overview.figures.daysLeft'),
            i18n.t('overview.figures.atRisk'),
        ]);
        expect(await figure('overview-figure-done')).toHaveTextContent('2');
        expect(await figure('overview-figure-total')).toHaveTextContent('9');
        expect(await figure('overview-figure-at-risk')).toHaveTextContent('2');
        // Calendar days from Nov 16 to the end of iteration 12 on Nov 27.
        expect(screen.getByTestId('overview-figure-days-left')).toHaveTextContent('11');

        // The header names the scope's project and dates and leads with New task.
        const header = screen.getByTestId('page-header');
        expect(header).toHaveTextContent('Alpha · Iteration 12');
        expect(await within(header).findByRole('link', { name: i18n.t('tasks.newTask') })).toHaveAttribute('href', '/tasks?create=1&project=1&iteration=12');
        expect(within(header).getByRole('link', { name: i18n.t('tasks.newTask') })).toHaveClass('btn', 'primary');
        expect(container.querySelectorAll('.btn.primary')).toHaveLength(1);

        // The first-run slot comes before the attention item.
        const slot = screen.getByTestId('overview-first-run-slot');
        expect(slot.compareDocumentPosition(attention) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();

        // The five-figure strip and the iteration details are gone.
        for (const label of ['implemented', 'accepted', 'overdueDelivery', 'lateStart', 'iterationOverflow']) {
            expect(screen.queryByText(i18n.t(`workStatus.${label}`))).not.toBeInTheDocument();
        }
        expect(screen.queryByText(i18n.t('overview.focus.detailsSummary'))).not.toBeInTheDocument();
        expect(container.querySelector('details.overview-details')).toBeNull();

        // Work now lists open work by delivery risk: overdue, then not started on time, then blocked.
        const workNow = screen.getByRole('region', { name: i18n.t('overview.workNow') });
        const rows = within(workNow).getAllByRole('link', { name: /^Open “Task/ });
        expect(rows.map(row => row.getAttribute('aria-label'))).toEqual([
            'Open “Task 104” in the task drawer',
            'Open “Task 105” in the task drawer',
            'Open “Task 106” in the task drawer',
            'Open “Task 107” in the task drawer',
            'Open “Task 108” in the task drawer',
        ]);
        expect(within(rows[0]).getByText(i18n.t('overview.deliveryRisk.overdue'))).toBeInTheDocument();

        await waitFor(() => expect(screen.getByTestId('overview-stage-executing')).toHaveTextContent('2'));
        expectPageChrome(container);
    });

    it.each([
        {
            name: 'blocked tasks first',
            setup: () => undefined,
            title: () => i18n.t('overview.attentionItem.blocked', { count: 1 }),
            action: () => i18n.t('overview.attentionItem.blockedAction'),
            href: '/tasks?blocked=yes&project=1&iteration=12',
        },
        {
            name: 'reviews waiting for a person when nothing is blocked',
            setup: () => { TASKS_BY_ITERATION[12] = ALPHA_TASKS.map(item => ({ ...item, blocked_reason: null })); },
            title: () => i18n.t('overview.attentionItem.reviews', { count: 1 }),
            action: () => i18n.t('overview.attentionItem.reviewsAction'),
            href: '/tasks?layout=pipeline&stage=verification_required&project=1&iteration=12',
        },
        {
            name: 'tasks to assign when no review waits',
            setup: () => {
                TASKS_BY_ITERATION[12] = ALPHA_TASKS.map(item => ({ ...item, blocked_reason: null }));
                api.pipeline.mockResolvedValue({ ...pipelineResponse(), verification_required: [] });
            },
            title: () => i18n.t('overview.attentionItem.toAssign', { count: 2 }),
            action: () => i18n.t('overview.attentionItem.toAssignAction', { count: 2 }),
            href: '/tasks?planningIssue=unassigned&mode=bulk&project=1&iteration=12',
        },
        {
            name: 'the plan below 6 of 6 when the work is in order',
            setup: () => {
                TASKS_BY_ITERATION[12] = ALPHA_TASKS.map(item => ({ ...item, blocked_reason: null, assignee: { id: 5, name: 'Ada Byron' } }));
                api.pipeline.mockResolvedValue({ ...pipelineResponse(), verification_required: [] });
                api.readiness.mockResolvedValue(readinessResponse(4));
            },
            title: () => i18n.t('overview.attentionItem.plan', { done: 4, total: 6 }),
            action: () => i18n.t('overview.attentionItem.planAction'),
            href: '/plan?project=1&iteration=12',
        },
    ])('leads with the most severe item: $name', async ({ setup, title, action, href }) => {
        setup();
        try {
            const { container } = renderOverview();
            const attention = await screen.findByRole('region', { name: title() });
            expect(within(attention).getByRole('link', { name: action() })).toHaveAttribute('href', href);
            expect(container.querySelectorAll('.overview-attention')).toHaveLength(1);
        } finally {
            TASKS_BY_ITERATION[12] = ALPHA_TASKS;
        }
    });

    it('says nothing needs you when no exception is open and the plan is complete', async () => {
        TASKS_BY_ITERATION[12] = [task(101, { status: 'closed' }), task(109)];
        api.pipeline.mockResolvedValue({ ...pipelineResponse(), verification_required: [] });
        try {
            renderOverview();
            const attention = await screen.findByRole('region', { name: i18n.t('overview.attentionItem.clearTitle') });
            expect(within(attention).queryByRole('link')).not.toBeInTheDocument();
        } finally {
            TASKS_BY_ITERATION[12] = ALPHA_TASKS;
        }
    });

    it.each([
        { testId: 'overview-figure-done', expected: 2, params: { status: 'closed' } },
        { testId: 'overview-figure-total', expected: 9, params: {} },
        { testId: 'overview-figure-at-risk', expected: 2, params: { planningIssue: 'at-risk' } },
    ])('links the $testId figure to the task list it counts, and the list holds that many tasks', async ({ testId, expected, params }) => {
        const { user } = renderOverview();
        const link = await figure(testId);
        expect(link.tagName).toBe('A');
        expect(link).toHaveTextContent(String(expected));

        await user.click(link);
        await waitFor(() => expect(screen.getByTestId('location').textContent).toMatch(/^\/tasks/));
        const search = searchOf();
        expect(search.get('project')).toBe('1');
        expect(search.get('iteration')).toBe('12');
        for (const [key, value] of Object.entries(params)) expect(search.get(key)).toBe(value);

        expect(await countListRows(user)).toBe(expected);
    });

    it('shows Days left as plain text, because a number of days has no task list', async () => {
        renderOverview();
        const daysLeft = await figure('overview-figure-days-left');
        expect(daysLeft).toHaveTextContent('11');
        expect(daysLeft.tagName).toBe('SPAN');
        expect(daysLeft.closest('a')).toBeNull();
    });

    it.each(STAGES.map(stage => ({ stage })))('links the $stage stage count to that stage of the pipeline view, which holds that many tasks', async ({ stage }) => {
        const expected = { needs_definition: 2, ready_to_assign: 1, assigned_waiting: 1, start_ready: 0, executing: 2, active_outside_run: 0, verification_required: 1, recovery_required: 0 }[stage];
        const { user } = renderOverview();
        const count = await screen.findByTestId(`overview-stage-${stage}`);
        await waitFor(() => expect(count).toHaveTextContent(String(expected)));
        expect(count.tagName).toBe('A');

        await user.click(count);
        await waitFor(() => expect(screen.getByTestId('location').textContent).toMatch(/^\/tasks/));
        const search = searchOf();
        expect(search.get('layout')).toBe('pipeline');
        expect(search.get('stage')).toBe(stage);
        expect(search.get('iteration')).toBe('12');

        const heading = await screen.findByRole('heading', { name: i18n.t('agentPipeline.stageHeading', { stage: i18n.t(`agentPipeline.columns.${stage}.title`), count: expected }) });
        const section = heading.closest('section') as HTMLElement;
        expect(section.querySelectorAll('[data-testid^="task-card-"]')).toHaveLength(expected);
    });

    it('renders with All projects and one iteration: every section shows only that iteration\'s work', async () => {
        const { container } = renderOverview('/?project=all&iteration=12');

        await waitFor(() => expect(screen.getByTestId('page-header')).toHaveTextContent(
            i18n.t('overview.purpose.iteration', { project: 'Alpha', iteration: 'Iteration 12', start: 'Nov 2, 2026', end: 'Nov 27, 2026' }),
        ));
        // Iteration 12 alone: 2 closed of 9, 2 at risk. Iteration 21 and the ended iteration 11 are left out.
        expect(await figure('overview-figure-done')).toHaveTextContent('2');
        expect(screen.getByTestId('overview-figure-total')).toHaveTextContent('9');
        expect(screen.getByTestId('overview-figure-at-risk')).toHaveTextContent('2');
        expect(api.tasks).toHaveBeenCalledWith(12);
        expect(api.tasks).not.toHaveBeenCalledWith(11);
        expect(api.tasks).not.toHaveBeenCalledWith(21);
        expect(api.readiness).not.toHaveBeenCalledWith(21);
        expect(api.lookup).not.toHaveBeenCalled();
        // Calendar days from Nov 16 to Nov 27, the end of iteration 12.
        expect(screen.getByTestId('overview-figure-days-left')).toHaveTextContent('11');

        const workNow = screen.getByRole('region', { name: i18n.t('overview.workNow') });
        expect(within(workNow).queryByRole('link', { name: 'Open “Task 202” in the task drawer' })).not.toBeInTheDocument();
        expect(within(workNow).getByRole('link', { name: 'Open “Task 104” in the task drawer' })).toBeInTheDocument();
        expect(await screen.findByRole('region', { name: i18n.t('overview.attentionItem.blocked', { count: 1 }) }))
            .toHaveTextContent('Iteration 12 · Alpha:');

        await waitFor(() => expect(screen.getByTestId('overview-stage-executing')).toHaveTextContent('2'));
        expect(screen.getByTestId('overview-stage-executing')).toHaveAttribute('href', '/tasks?layout=pipeline&stage=executing&project=all&iteration=12');
        expect(screen.getByRole('region', { name: i18n.t('overview.agentsNow') }))
            .toHaveTextContent(i18n.t('overview.agentsNowScopeDescription', { scope: 'Iteration 12 · Alpha' }));
        expectPageChrome(container);
    });

    it('counts Days left in calendar days to the iteration end, whatever the working-day budget', async () => {
        api.iterations.mockResolvedValue(ITERATIONS.map(item => (item.id === 21 ? { ...item, working_days: 3 } : item)));
        renderOverview('/?project=all&iteration=21');
        expect(await figure('overview-figure-days-left')).toHaveTextContent('18');
    });

    it.each([
        { testId: 'overview-figure-done', expected: 2 },
        { testId: 'overview-figure-total', expected: 9 },
        { testId: 'overview-figure-at-risk', expected: 2 },
    ])('with All projects and one iteration links $testId to that iteration\'s task list, which holds exactly its count', async ({ testId, expected }) => {
        const { user } = renderOverview('/?project=all&iteration=12');
        const count = await figure(testId);
        await waitFor(() => expect(count).toHaveTextContent(String(expected)));
        expect(count.tagName).toBe('A');

        await user.click(count);
        await waitFor(() => expect(screen.getByTestId('location').textContent).toMatch(/^\/tasks/));
        expect(searchOf().get('project')).toBe('all');
        expect(searchOf().get('iteration')).toBe('12');
        expect(await countListRows(user)).toBe(expected);
    });

    it.each([
        ...STAGES.map(stage => ({
            iteration: 21,
            stage,
            expected: { executing: 1, verification_required: 1 }[stage as string] ?? 0,
        })),
        { iteration: 12, stage: 'executing' as const, expected: 2 },
        { iteration: 12, stage: 'needs_definition' as const, expected: 2 },
        // Task 401 is in iteration 11, which has ended; the scope bar can still name it.
        { iteration: 11, stage: 'recovery_required' as const, expected: 1 },
    ])('with All projects links the $stage count in iteration $iteration to the pipeline view, which holds that many tasks', async ({ iteration: scopeIteration, stage, expected }) => {
        const { user } = renderOverview(`/?project=all&iteration=${scopeIteration}`);
        const count = await screen.findByTestId(`overview-stage-${stage}`);
        await waitFor(() => expect(count).toHaveTextContent(String(expected)));
        expect(count.tagName).toBe('A');

        await user.click(count);
        await waitFor(() => expect(screen.getByTestId('location').textContent).toMatch(/^\/tasks/));
        const search = searchOf();
        expect(search.get('layout')).toBe('pipeline');
        expect(search.get('stage')).toBe(stage);
        expect(search.get('project')).toBe('all');
        expect(search.get('iteration')).toBe(String(scopeIteration));

        const heading = await screen.findByRole('heading', { name: i18n.t('agentPipeline.stageHeading', { stage: i18n.t(`agentPipeline.columns.${stage}.title`), count: expected }) });
        expect((heading.closest('section') as HTMLElement).querySelectorAll('[data-testid^="task-card-"]')).toHaveLength(expected);
    });

    it('closes its own list and keeps the scope', async () => {
        const { user } = renderOverview('/?project=1&iteration=backlog');
        await user.click(await figure('overview-figure-done'));
        const drawer = await screen.findByRole('dialog');
        await user.click(within(drawer).getByRole('button', { name: i18n.t('surfaces.slideOver.close') }));
        await waitFor(() => expect(screen.queryByRole('dialog')).not.toBeInTheDocument());
        expect(searchOf().get('list')).toBeNull();
        expect(searchOf().get('project')).toBe('1');
    });

    it('weighs only the plan of the iteration in scope with All projects', async () => {
        api.pipeline.mockResolvedValue({ ...pipelineResponse(), verification_required: [] });
        api.readiness.mockImplementation(async (id: number) => ({ ...readinessResponse(id === 21 ? 4 : 6), iteration_id: id }));
        renderOverview('/?project=all&iteration=21');
        const attention = await screen.findByRole('region', { name: i18n.t('overview.attentionItem.plan', { done: 4, total: 6 }) });
        expect(attention).toHaveTextContent('Iteration 21 · Beta:');
        expect(within(attention).getByRole('link', { name: i18n.t('overview.attentionItem.planAction') }))
            .toHaveAttribute('href', '/plan?project=all&iteration=21');
        expect(api.readiness).toHaveBeenCalledWith(21);
        // Get started reads the workspace default iteration as well as Overview's scoped plans.
        expect(api.readiness).toHaveBeenCalledWith(12);
        expect(api.readiness).not.toHaveBeenCalledWith(11);
    });

    it('shows only work with no iteration with All projects and Backlog', async () => {
        const betaBacklog = reference(601, { project_id: 2, project_name: 'Beta', title: 'Backlog 601' });
        api.lookup.mockImplementation(async (params: { backlog_only?: boolean; project_id?: number }) => ({
            items: params.backlog_only ? [...BACKLOG, betaBacklog] : [],
            has_more: false,
            next_after_id: null,
            limit: 100,
        }));
        api.pipeline.mockResolvedValue({
            ...pipelineResponse(),
            executing: [...pipelineResponse().executing, task(505, { iteration_id: null, status: 'active' })],
        });
        const { user } = renderOverview('/?project=all&iteration=backlog');

        await waitFor(() => expect(screen.getByTestId('page-header')).toHaveTextContent(i18n.t('overview.purpose.allProjectsBacklog')));
        expect(await figure('overview-figure-done')).toHaveTextContent('2');
        expect(screen.getByTestId('overview-figure-total')).toHaveTextContent('6');
        // The backlog of every project is read, and no iteration's tasks or plan are.
        expect(api.lookup).toHaveBeenCalledWith(expect.objectContaining({ backlog_only: true }));
        expect(api.lookup.mock.calls.every(([params]) => params.project_id === undefined)).toBe(true);
        expect(api.tasks).not.toHaveBeenCalled();
        // Backlog still reads the workspace's default iteration for Get started.
        expect(api.readiness).toHaveBeenCalledWith(12);
        expect(screen.queryByText(i18n.t('overview.noOpenIterations'))).not.toBeInTheDocument();

        const workNow = screen.getByRole('region', { name: i18n.t('overview.workNow') });
        expect(within(workNow).getAllByRole('link', { name: /^Open “Backlog/ }).map(row => row.getAttribute('aria-label'))).toEqual([
            'Open “Backlog 502” in the task drawer',
            'Open “Backlog 505” in the task drawer',
            'Open “Backlog 504” in the task drawer',
            'Open “Backlog 601” in the task drawer',
        ]);
        expect(within(workNow).queryByRole('link', { name: /Task \d+/ })).not.toBeInTheDocument();
        await waitFor(() => expect(screen.getByTestId('overview-stage-executing')).toHaveTextContent('1'));

        await user.click(screen.getByTestId('overview-figure-total'));
        expect(await ownListRows()).toHaveLength(6);
    });

    it('keeps attention, Work now, Agents now and the figures for the Backlog', async () => {
        api.pipeline.mockResolvedValue({
            ...pipelineResponse(),
            executing: [...pipelineResponse().executing, task(505, { iteration_id: null, status: 'active' })],
        });
        const { container, user } = renderOverview('/?project=1&iteration=backlog');

        // Task 503 is closed, so its leftover blocker does not count.
        const attention = await screen.findByRole('region', { name: i18n.t('overview.attentionItem.blocked', { count: 1 }) });
        expect(within(attention).getByRole('link', { name: i18n.t('overview.attentionItem.blockedAction') }))
            .toHaveAttribute('href', '/?list=blocked&project=1&iteration=backlog');
        // Blocked first, then work in progress, then planned work.
        const workNow = screen.getByRole('region', { name: i18n.t('overview.workNow') });
        expect(within(workNow).getAllByRole('link', { name: /^Open “Backlog/ }).map(row => row.getAttribute('aria-label'))).toEqual([
            'Open “Backlog 502” in the task drawer',
            'Open “Backlog 505” in the task drawer',
            'Open “Backlog 504” in the task drawer',
        ]);
        expect(screen.getByRole('heading', { level: 2, name: i18n.t('overview.agentsNow') })).toBeInTheDocument();
        expect(await figure('overview-figure-done')).toHaveTextContent('2');
        expect(screen.getByTestId('overview-figure-total')).toHaveTextContent('5');
        // Backlog has no end date and its references carry no schedule signals.
        expect(screen.getByTestId('overview-figure-days-left')).toHaveTextContent('—');
        expect(screen.getByTestId('overview-figure-at-risk')).toHaveTextContent('—');
        expect(screen.getByText(i18n.t('overview.figures.backlogNote'))).toBeInTheDocument();
        expectPageChrome(container);

        await user.click(screen.getByTestId('overview-figure-done'));
        expect(await ownListRows()).toEqual(['Backlog 501', 'Backlog 503'].map(title => i18n.t('overview.list.openTask', { title })));
    });

    it('links a Backlog stage count to the pipeline view on the Backlog, which holds that many tasks', async () => {
        api.pipeline.mockResolvedValue({
            ...pipelineResponse(),
            executing: [...pipelineResponse().executing, task(505, { iteration_id: null, status: 'active' })],
        });
        const { user } = renderOverview('/?project=1&iteration=backlog');
        const count = await screen.findByTestId('overview-stage-executing');
        await waitFor(() => expect(count).toHaveTextContent('1'));
        expect(count).toHaveAttribute('href', '/tasks?layout=pipeline&stage=executing&project=1&iteration=backlog');

        await user.click(count);
        const heading = await screen.findByRole('heading', { name: i18n.t('agentPipeline.stageHeading', { stage: i18n.t('agentPipeline.columns.executing.title'), count: 1 }) });
        expect((heading.closest('section') as HTMLElement).querySelectorAll('[data-testid^="task-card-"]')).toHaveLength(1);
    });

    it('keeps New task and offers Retry when projects fail to load', async () => {
        api.projects.mockRejectedValue(unavailable());
        renderOverview('/?project=1&iteration=12');
        expect(await screen.findByRole('alert')).toHaveTextContent(i18n.t('overview.dataStatus.projectsUnavailable'));
        expect(within(screen.getByRole('alert')).getByRole('button', { name: i18n.t('queryFeedback.retry') })).toBeInTheDocument();
        expect(await screen.findByRole('heading', { level: 2, name: i18n.t('overview.workNow') })).toBeInTheDocument();
        const header = screen.getByTestId('page-header');
        expect(within(header).getByRole('link', { name: i18n.t('tasks.newTask') })).toBeVisible();
    });

    it('opens New task on the Backlog as a backlog task of the scope project, with no iteration', async () => {
        api.projects.mockResolvedValue([{ id: 1, name: 'Alpha' }, { id: 2, name: 'Beta' }]);
        const { user } = renderOverview('/?project=1&iteration=backlog');
        const newTask = await within(screen.getByTestId('page-header')).findByRole('link', { name: i18n.t('tasks.newTask') });
        expect(newTask).toHaveAttribute('href', '/tasks?create=1&project=1&iteration=backlog');

        await user.click(newTask);
        const drawer = await screen.findByRole('dialog', { name: i18n.t('tasks.createNewTask') });
        expect(within(drawer).getByText(i18n.t('teamwork.inBacklog'))).toBeInTheDocument();
        await user.click(within(drawer).getByRole('button', { name: i18n.t('assigneePicker.more') }));
        await waitFor(() => expect(within(drawer).getByLabelText(i18n.t('surfaces.taskForm.project'))).toHaveValue('1'));
        await user.type(within(drawer).getByLabelText(i18n.t('surfaces.taskForm.taskTitle')), 'Write the release notes');
        await user.click(within(drawer).getByRole('button', { name: i18n.t('taskEditor.createTask') }));

        await waitFor(() => expect(api.create).toHaveBeenCalledTimes(1));
        expect(api.create).toHaveBeenCalledWith(null, expect.objectContaining({ title: 'Write the release notes', project_id: 1 }));
        await waitFor(() => expect(screen.queryByRole('dialog', { name: i18n.t('tasks.createNewTask') })).not.toBeInTheDocument());
        expect(searchOf().get('create')).toBeNull();
        expect(searchOf().get('iteration')).toBe('backlog');
    });

    it('opens New task with All projects in the iteration in scope', async () => {
        api.projects.mockResolvedValue([{ id: 1, name: 'Alpha' }, { id: 2, name: 'Beta' }]);
        const { user } = renderOverview('/?project=all&iteration=21');
        const newTask = await within(screen.getByTestId('page-header')).findByRole('link', { name: i18n.t('tasks.newTask') });
        expect(newTask).toHaveAttribute('href', '/tasks?create=1&project=all&iteration=21');

        await user.click(newTask);
        const drawer = await screen.findByRole('dialog', { name: i18n.t('tasks.createNewTask') });
        expect(within(drawer).getByText(i18n.t('teamwork.inIteration'))).toBeInTheDocument();
        await user.click(within(drawer).getByRole('button', { name: i18n.t('assigneePicker.more') }));
        await waitFor(() => expect(within(drawer).getByLabelText(i18n.t('surfaces.taskForm.project'))).toHaveValue('Beta'));
    });

    it('asks for a project before New task can create a backlog task with All projects', async () => {
        api.projects.mockResolvedValue([{ id: 1, name: 'Alpha' }, { id: 2, name: 'Beta' }]);
        const { user } = renderOverview('/?project=all&iteration=backlog');
        await user.click(await within(screen.getByTestId('page-header')).findByRole('link', { name: i18n.t('tasks.newTask') }));

        // A backlog task needs a project, and All projects names none.
        expect(await screen.findByText(i18n.t('teamwork.chooseProject'))).toBeInTheDocument();
        expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
        expect(searchOf().get('create')).toBe('1');
    });

    it('opens New task from the Tasks header on the Backlog in the pipeline view', async () => {
        const { user } = renderOverview('/tasks?layout=pipeline&project=1&iteration=backlog');
        await screen.findByRole('heading', { level: 1, name: i18n.t('tasks.allTasks') });
        const newTask = screen.getByRole('button', { name: i18n.t('tasks.newTask') });
        expect(newTask).toBeEnabled();

        await user.click(newTask);
        const drawer = await screen.findByRole('dialog', { name: i18n.t('tasks.createNewTask') });
        expect(within(drawer).getByText(i18n.t('teamwork.inBacklog'))).toBeInTheDocument();
    });

    it.each([
        ['Overview', '/?project=1&iteration=backlog'],
        ['the pipeline view', '/tasks?layout=pipeline&project=1&iteration=backlog'],
    ])('opens New task from the command menu on the Backlog from %s', async (_page, url) => {
        const { user } = renderWithProviders(
            <>
                <CommandMenu />
                <Routes>
                    <Route path="/" element={<OverviewPage />} />
                    <Route path="/tasks" element={<TasksPage />} />
                </Routes>
                <LocationProbe />
            </>,
            { initialEntries: [url] },
        );
        await user.keyboard('{Control>}k{/Control}');
        await user.type(screen.getByRole('combobox', { name: 'Search commands' }), i18n.t('commandMenu.commands.newTask.label'));
        await user.click(screen.getByRole('option', { name: new RegExp(i18n.t('commandMenu.commands.newTask.label')) }));

        expect(searchOf().get('create')).toBe('1');
        expect(searchOf().get('iteration')).toBe('backlog');
        const drawer = await screen.findByRole('dialog', { name: i18n.t('tasks.createNewTask') });
        expect(within(drawer).getByText(i18n.t('teamwork.inBacklog'))).toBeInTheDocument();
    });

    it('shows the backlog of every project when the workspace has no iterations', async () => {
        api.iterations.mockResolvedValue([]);
        api.lookup.mockImplementation(async (params: { backlog_only?: boolean }) => ({
            items: params.backlog_only ? BACKLOG : [],
            has_more: false,
            next_after_id: null,
            limit: 100,
        }));
        renderOverview('/?project=all&iteration=backlog');
        expect(await figure('overview-figure-done')).toHaveTextContent('2');
        expect(screen.getByTestId('overview-figure-total')).toHaveTextContent('5');
        expect(screen.queryByRole('heading', { name: i18n.t('emptyStates.overview.iterationTitle') })).not.toBeInTheDocument();
        expect(api.lookup).toHaveBeenCalledWith(expect.objectContaining({ backlog_only: true }));
    });

    describe.each([
        { scope: 'All projects', url: '/?project=all&iteration=backlog', projectId: undefined },
        { scope: 'one project', url: '/?project=1&iteration=backlog', projectId: 1 },
    ])('with no iterations and $scope with Backlog', ({ url, projectId }) => {
        const backlogPage = (items: TaskReference[]) => ({ items, has_more: false, next_after_id: null, limit: 100 });
        const emptyStateTitle = () => screen.queryByRole('heading', { name: i18n.t('emptyStates.overview.iterationTitle') });
        const workNow = () => screen.findByRole('region', { name: i18n.t('overview.workNow') });

        beforeEach(() => {
            api.iterations.mockResolvedValue([]);
            // Get started would name the next step itself; with it dismissed the page's own empty state is in view.
            useGetStartedVisibility.setState({ dismissed: true, requested: false });
        });

        afterEach(() => {
            useGetStartedVisibility.setState({ dismissed: false, requested: false });
        });

        it('shows loading, not the empty state, while the backlog is read', async () => {
            api.lookup.mockReturnValue(new Promise(() => undefined));
            renderOverview(url);
            expect(await within(await workNow()).findByText(i18n.t('overview.dataStatus.sectionLoading'))).toBeInTheDocument();
            expect(api.lookup).toHaveBeenCalledWith(expect.objectContaining({ backlog_only: true }));
            expect(emptyStateTitle()).not.toBeInTheDocument();
        });

        it('shows the error with Retry, not the empty state, when the backlog cannot be read', async () => {
            api.lookup.mockRejectedValue(new Error('offline'));
            const { user } = renderOverview(url);
            const section = await workNow();
            expect(await within(section).findByText(i18n.t('overview.dataStatus.sectionUnavailable'))).toBeInTheDocument();
            expect(emptyStateTitle()).not.toBeInTheDocument();

            // Once the backlog loads, Retry shows its work.
            api.lookup.mockResolvedValue(backlogPage(BACKLOG));
            await user.click(within(section).getByRole('button', { name: i18n.t('queryFeedback.retry') }));
            expect(await figure('overview-figure-done')).toHaveTextContent('2');
            expect(screen.getByTestId('overview-figure-total')).toHaveTextContent('5');
            expect(emptyStateTitle()).not.toBeInTheDocument();
        });

        it('shows the backlog work when there is some', async () => {
            api.lookup.mockResolvedValue(backlogPage(BACKLOG));
            renderOverview(url);
            expect(await figure('overview-figure-done')).toHaveTextContent('2');
            expect(screen.getByTestId('overview-figure-total')).toHaveTextContent('5');
            expect(emptyStateTitle()).not.toBeInTheDocument();
            expect(api.lookup.mock.calls.every(([params]) => params.project_id === projectId)).toBe(true);
        });

        it('shows the empty state once the backlog is read and holds no work', async () => {
            api.lookup.mockResolvedValue(backlogPage([]));
            renderOverview(url);
            expect(await screen.findByRole('heading', { name: i18n.t('emptyStates.overview.iterationTitle') })).toBeInTheDocument();
            expect(screen.queryByRole('region', { name: i18n.t('overview.workNow') })).not.toBeInTheDocument();
        });
    });

    it('says what is needed when the pipeline cannot be read', async () => {
        access.hasAdminKey = false;
        renderOverview();
        expect(await screen.findByText(i18n.t('overview.agentsNowLocked'))).toBeInTheDocument();
        expect(await figure('overview-figure-done')).toHaveTextContent('2');
    });

    it('never counts finished work as blocked', async () => {
        TASKS_BY_ITERATION[12] = ALPHA_TASKS.map(item => (
            item.id === 106 ? { ...item, blocked_reason: null } : item.id === 102 ? { ...item, blocked_reason: 'Left over' } : item
        ));
        try {
            renderOverview();
            expect(await screen.findByRole('region', { name: i18n.t('overview.attentionItem.reviews', { count: 1 }) })).toBeInTheDocument();
            expect(screen.queryByRole('region', { name: /blocked/i })).not.toBeInTheDocument();
        } finally {
            TASKS_BY_ITERATION[12] = ALPHA_TASKS;
        }
    });

    it.each([
        { name: 'the tasks fail', setup: () => { api.tasks.mockRejectedValue(new Error('offline')); }, source: 'tasks' },
        { name: 'the pipeline fails', setup: () => { api.pipeline.mockRejectedValue(unavailable()); }, source: 'pipeline' },
        { name: 'the plan progress fails', setup: () => { api.readiness.mockRejectedValue(new Error('offline')); }, source: 'plan' },
    ])('says it cannot tell what needs you, with a retry, when $name', async ({ setup, source }) => {
        TASKS_BY_ITERATION[12] = [task(101, { status: 'closed' }), task(109)];
        api.pipeline.mockResolvedValue({ ...pipelineResponse(), verification_required: [] });
        setup();
        try {
            const { user } = renderOverview();
            const attention = await screen.findByRole('region', { name: i18n.t('overview.attentionItem.unknownTitle') });
            expect(attention).toHaveTextContent(i18n.t(`overview.attentionItem.sources.${source}`));
            expect(screen.queryByText(i18n.t('overview.attentionItem.clearTitle'))).not.toBeInTheDocument();

            // Once the source loads, the retry settles the item.
            api.tasks.mockImplementation(async (id: number) => TASKS_BY_ITERATION[id] ?? []);
            api.pipeline.mockResolvedValue({ ...pipelineResponse(), verification_required: [] });
            api.readiness.mockResolvedValue(readinessResponse());
            await user.click(within(attention).getByRole('button', { name: i18n.t('overview.attentionItem.retry') }));
            expect(await screen.findByRole('region', { name: i18n.t('overview.attentionItem.clearTitle') })).toBeInTheDocument();
        } finally {
            TASKS_BY_ITERATION[12] = ALPHA_TASKS;
        }
    });

    it('keeps the attention item loading while the plan progress is pending', async () => {
        TASKS_BY_ITERATION[12] = [task(101, { status: 'closed' }), task(109)];
        api.pipeline.mockResolvedValue({ ...pipelineResponse(), verification_required: [] });
        api.readiness.mockReturnValue(new Promise(() => undefined));
        try {
            renderOverview();
            expect(await figure('overview-figure-done')).toHaveTextContent('1');
            expect(screen.getByRole('region', { name: i18n.t('overview.dataStatus.loadingSignals') })).toBeInTheDocument();
            expect(screen.queryByText(i18n.t('overview.attentionItem.clearTitle'))).not.toBeInTheDocument();
        } finally {
            TASKS_BY_ITERATION[12] = ALPHA_TASKS;
        }
    });

    it.each([
        { name: 'the tasks', fail: () => { api.tasks.mockRejectedValue(unavailable()); }, source: 'tasks', section: 'overview.workNow' },
        { name: 'the pipeline', fail: () => { api.pipeline.mockRejectedValue(unavailable()); }, source: 'pipeline', section: 'overview.agentsNow' },
        { name: 'the plan progress', fail: () => { api.readiness.mockRejectedValue(unavailable()); }, source: 'plan', section: null },
    ])('marks the last result as stale, with a retry, when a refresh of $name fails', async ({ fail, source, section }) => {
        TASKS_BY_ITERATION[12] = [task(101, { status: 'closed' }), task(109)];
        api.pipeline.mockResolvedValue({ ...pipelineResponse(), verification_required: [] });
        try {
            const { queryClient, user } = renderOverview();
            expect(await screen.findByRole('region', { name: i18n.t('overview.attentionItem.clearTitle') })).toBeInTheDocument();
            await waitFor(() => expect(screen.getByTestId('overview-stage-executing')).toHaveTextContent('2'));

            fail();
            await act(() => queryClient.refetchQueries());

            // The cached result stays, but never as an unqualified all-clear.
            const attention = await screen.findByRole('region', { name: i18n.t('overview.attentionItem.staleClearTitle') });
            expect(screen.queryByText(i18n.t('overview.attentionItem.clearTitle'))).not.toBeInTheDocument();
            expect(within(attention).getByTestId('overview-attention-stale'))
                .toHaveTextContent(i18n.t('overview.attentionItem.staleMeta', { sources: i18n.t(`overview.attentionItem.sources.${source}`) }));
            expect(screen.getByTestId('overview-figure-done')).toHaveTextContent('1');
            expect(screen.getByTestId('overview-stage-executing')).toHaveTextContent('2');
            if (section) {
                expect(within(screen.getByRole('region', { name: i18n.t(section) })).getByText(i18n.t('overview.dataStatus.sectionStale')))
                    .toBeInTheDocument();
            }

            // Once the source loads again, the retry settles the item.
            api.tasks.mockImplementation(async (id: number) => TASKS_BY_ITERATION[id] ?? []);
            api.pipeline.mockResolvedValue({ ...pipelineResponse(), verification_required: [] });
            api.readiness.mockResolvedValue(readinessResponse());
            await user.click(within(attention).getByRole('button', { name: i18n.t('overview.attentionItem.retry') }));
            expect(await screen.findByRole('region', { name: i18n.t('overview.attentionItem.clearTitle') })).toBeInTheDocument();
            expect(screen.queryByTestId('overview-attention-stale')).not.toBeInTheDocument();
            expect(screen.queryByText(i18n.t('overview.dataStatus.sectionStale'))).not.toBeInTheDocument();
        } finally {
            TASKS_BY_ITERATION[12] = ALPHA_TASKS;
        }
    });

    it('keeps the last attention item, marked as stale, when a refresh fails', async () => {
        const { queryClient } = renderOverview();
        const blocked = i18n.t('overview.attentionItem.blocked', { count: 1 });
        expect(await screen.findByRole('region', { name: blocked })).toBeInTheDocument();

        api.tasks.mockRejectedValue(unavailable());
        await act(() => queryClient.refetchQueries());

        const attention = await screen.findByRole('region', { name: blocked });
        await waitFor(() => expect(within(attention).getByTestId('overview-attention-stale'))
            .toHaveTextContent(i18n.t('overview.attentionItem.sources.tasks')));
        expect(within(attention).getAllByRole('link')).toHaveLength(1);
        expect(within(attention).getByRole('button', { name: i18n.t('overview.attentionItem.retry') })).toBeInTheDocument();
    });

    it('offers a retry when the tasks cannot be loaded', async () => {
        api.tasks.mockRejectedValueOnce(new Error('offline'));
        const { user } = renderOverview();
        const retries = await screen.findAllByRole('button', { name: /retry/i });
        expect(retries.length).toBeGreaterThan(0);
        await user.click(retries[0]);
        expect(await figure('overview-figure-done')).toHaveTextContent('2');
    });
});

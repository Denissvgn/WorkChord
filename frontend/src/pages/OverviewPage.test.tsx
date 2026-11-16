import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { screen, waitFor, within } from '@testing-library/react';
import { Route, Routes, useLocation } from 'react-router-dom';
import { renderWithProviders } from '../test/renderWithProviders';
import { expectPageChrome } from '../test/pageChrome';
import { useScopeStore } from '../features/scope/scopeStore';
import type { AgentPipeline } from '../types/agent';
import type { Iteration, PlanCheckpoint } from '../types/iteration';
import type { Task, TaskReference } from '../types/task';
import i18n from '../i18n/i18n';
import OverviewPage from './OverviewPage';
import TasksPage from './TasksPage';

const api = vi.hoisted(() => ({
    iterations: vi.fn(),
    readiness: vi.fn(),
    tasks: vi.fn(),
    pipeline: vi.fn(),
    task: vi.fn(),
    lookup: vi.fn(),
}));
const access = vi.hoisted(() => ({ hasAdminKey: true }));

vi.mock('../hooks/useAdminAccess', () => ({ useAdminAccess: () => access, useKeylessReader: () => ({ workViews: access.hasAdminKey }) }));
vi.mock('../hooks/useAgentAccess', () => ({ useAgentAccess: () => ({ hasAgentKey: false }) }));
vi.mock('../services/agentService', () => ({ agentService: { getPipeline: api.pipeline, getTaskTimeline: vi.fn().mockResolvedValue({ items: [] }) } }));
vi.mock('../services/iterationService', () => ({
    iterationService: {
        getAll: api.iterations,
        getPlanningReadiness: api.readiness,
        getById: vi.fn().mockResolvedValue({ id: 12, name: 'Iteration 12', project_id: 1 }),
    },
}));
vi.mock('../services/taskService', () => ({
    taskService: {
        getByIteration: api.tasks,
        getById: api.task,
        lookup: api.lookup,
    },
}));
vi.mock('../services/savedViewService', () => ({ savedViewService: { getAll: vi.fn().mockResolvedValue([]) } }));
vi.mock('../services/labelService', () => ({ labelService: { getGroups: vi.fn().mockResolvedValue([]) } }));
vi.mock('../services/sessionService', () => ({ sessionService: { getWhoAmI: vi.fn().mockResolvedValue({ id: 3 }) } }));
vi.mock('../services/projectService', () => ({ projectService: { getAll: vi.fn().mockResolvedValue([]) } }));
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
        expect(screen.getByTestId('overview-figure-days-left')).toHaveTextContent('8');

        // The header names the scope's project and dates and leads with New task.
        const header = screen.getByTestId('page-header');
        expect(header).toHaveTextContent('Alpha · Iteration 12');
        expect(within(header).getByRole('link', { name: i18n.t('tasks.newTask') })).toHaveAttribute('href', '/tasks?create=1&project=1&iteration=12');
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
        expect(daysLeft).toHaveTextContent('8');
        expect(daysLeft.tagName).toBe('SPAN');
        expect(daysLeft.closest('a')).toBeNull();
    });

    it.each(STAGES.map(stage => ({ stage })))('links the $stage stage count to that stage of the pipeline view, which holds that many tasks', async ({ stage }) => {
        const expected = { needs_definition: 2, ready_to_assign: 1, assigned_waiting: 1, start_ready: 0, executing: 2, verification_required: 1, recovery_required: 0 }[stage];
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

    it('renders with All projects: Done and At risk sum over the open iterations, and Days left counts to the latest end', async () => {
        const { container } = renderOverview('/?project=all&iteration=12');

        await waitFor(() => expect(screen.getByTestId('page-header')).toHaveTextContent(
            i18n.t('overview.purpose.allProjects', { count: 2, start: 'Nov 2, 2026', end: 'Dec 4, 2026' }).split(',')[0],
        ));
        // Done 2 + 1 of 9 + 4, at risk 2 + 1; the ended iteration 11 is left out.
        expect(await figure('overview-figure-done')).toHaveTextContent('3');
        expect(screen.getByTestId('overview-figure-total')).toHaveTextContent('13');
        expect(screen.getByTestId('overview-figure-at-risk')).toHaveTextContent('3');
        expect(api.tasks).not.toHaveBeenCalledWith(11);
        // Iteration 12 has 8 working days left and iteration 21, which ends last on Dec 4, has 13.
        expect(screen.getByTestId('overview-figure-days-left')).toHaveTextContent('13');

        // Work now draws from both open iterations, and the attention item names its iteration.
        const workNow = screen.getByRole('region', { name: i18n.t('overview.workNow') });
        expect(within(workNow).getByRole('link', { name: 'Open “Task 202” in the task drawer' })).toBeInTheDocument();
        expect(await screen.findByRole('region', { name: i18n.t('overview.attentionItem.blocked', { count: 1 }) }))
            .toHaveTextContent('Iteration 12 · Alpha:');

        await waitFor(() => expect(screen.getByTestId('overview-stage-executing')).toHaveTextContent('3'));
        expectPageChrome(container);
    });

    it.each([
        { testId: 'overview-figure-done', expected: ['Task 101', 'Task 102', 'Task 201'] },
        { testId: 'overview-figure-total', expected: [101, 102, 103, 104, 105, 106, 107, 108, 109, 201, 202, 203, 204].map(id => `Task ${id}`) },
        { testId: 'overview-figure-at-risk', expected: ['Task 104', 'Task 105', 'Task 202'] },
        { testId: 'overview-stage-executing', expected: ['Task 104', 'Task 106', 'Task 203'] },
        { testId: 'overview-stage-verification_required', expected: ['Task 103', 'Task 204'] },
        { testId: 'overview-stage-needs_definition', expected: ['Task 107', 'Task 108'] },
        // Zero counts link too: the list they open is empty. Task 401 is in the ended iteration 11.
        { testId: 'overview-stage-start_ready', expected: [] },
        { testId: 'overview-stage-recovery_required', expected: [] },
    ])('with All projects links $testId to a list that holds exactly its count', async ({ testId, expected }) => {
        const { user } = renderOverview('/?project=all&iteration=12');
        const count = await figure(testId);
        await waitFor(() => expect(count).toHaveTextContent(String(expected.length)));
        expect(count.tagName).toBe('A');

        await user.click(count);
        await waitFor(() => expect(searchOf().get('list')).not.toBeNull());
        expect(searchOf().get('project')).toBe('all');
        const rows = await ownListRows();
        expect(rows).toHaveLength(expected.length);
        expect(rows).toEqual(expected.map(title => i18n.t('overview.list.openTask', { title })));
    });

    it('closes its own list and keeps the scope', async () => {
        const { user } = renderOverview('/?project=all&iteration=12');
        await user.click(await figure('overview-figure-done'));
        const drawer = await screen.findByRole('dialog');
        await user.click(within(drawer).getByRole('button', { name: i18n.t('surfaces.slideOver.close') }));
        await waitFor(() => expect(screen.queryByRole('dialog')).not.toBeInTheDocument());
        expect(searchOf().get('list')).toBeNull();
        expect(searchOf().get('project')).toBe('all');
    });

    it('links zero counts with All projects and no open iteration to an empty list', async () => {
        api.iterations.mockResolvedValue([ITERATIONS[0]]);
        const { user } = renderOverview('/?project=all&iteration=11');
        expect(await screen.findByText(i18n.t('overview.noOpenIterations'))).toBeInTheDocument();
        const done = await figure('overview-figure-done');
        expect(done).toHaveTextContent('0');
        expect(screen.getByTestId('overview-figure-days-left')).toHaveTextContent('—');
        await user.click(done);
        expect(await ownListRows()).toEqual([]);
    });

    it('weighs the plan of every open iteration with All projects', async () => {
        TASKS_BY_ITERATION[12] = [task(101, { status: 'closed' }), task(109)];
        api.pipeline.mockResolvedValue({ ...pipelineResponse(), verification_required: [] });
        api.readiness.mockImplementation(async (id: number) => ({ ...readinessResponse(id === 21 ? 4 : 6), iteration_id: id }));
        try {
            renderOverview('/?project=all&iteration=12');
            const attention = await screen.findByRole('region', { name: i18n.t('overview.attentionItem.plan', { done: 4, total: 6 }) });
            expect(attention).toHaveTextContent('Iteration 21 · Beta:');
            expect(within(attention).getByRole('link', { name: i18n.t('overview.attentionItem.planAction') }))
                .toHaveAttribute('href', '/plan?project=all&iteration=21');
            expect(api.readiness).toHaveBeenCalledWith(12);
            expect(api.readiness).toHaveBeenCalledWith(21);
            expect(api.readiness).not.toHaveBeenCalledWith(11);
        } finally {
            TASKS_BY_ITERATION[12] = ALPHA_TASKS;
        }
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

    it('offers to create an iteration when there is none', async () => {
        api.iterations.mockResolvedValue([]);
        renderOverview('/');
        expect(await screen.findByRole('heading', { name: i18n.t('overview.noIterationTitle') })).toBeInTheDocument();
        expect(screen.getByRole('link', { name: i18n.t('overview.setUpPlanningPeriod') })).toHaveAttribute('href', expect.stringMatching(/^\/plan/));
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

    it('offers a retry when the tasks cannot be loaded', async () => {
        api.tasks.mockRejectedValueOnce(new Error('offline'));
        const { user } = renderOverview();
        const retries = await screen.findAllByRole('button', { name: /retry/i });
        expect(retries.length).toBeGreaterThan(0);
        await user.click(retries[0]);
        expect(await figure('overview-figure-done')).toHaveTextContent('2');
    });
});

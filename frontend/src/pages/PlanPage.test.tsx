import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { screen, waitFor, within } from '@testing-library/react';
import { Route, Routes, useLocation, useNavigate } from 'react-router-dom';
import { changeAppLanguage } from '../i18n/i18n';
import { LegacyRedirect } from '../navigation/LegacyRedirect';
import { expectPageChrome } from '../test/pageChrome';
import { renderWithProviders } from '../test/renderWithProviders';
import { useScopeStore } from '../features/scope/scopeStore';
import { useSetWorkScope } from '../features/scope/useWorkScope';
import type { TeamMember, TeamMemberCreate, TeamMemberProfile } from '../types/team';
import type { IterationPlanningReadinessSummary, PlanCheckpoint } from '../types/iteration';
import PlanPage from './PlanPage';
import type { Task, TaskBulkOperationRequest } from '../types/task';
import type { GanttTask, SchedulePreviewResponse } from '../types/gantt';
import planPageSource from './PlanPage.tsx?raw';

const services = vi.hoisted(() => ({
    iterations: { getAll: vi.fn(), getPlanningReadiness: vi.fn(), getById: vi.fn() },
    team: { getByIteration: vi.fn(), getProfiles: vi.fn(), create: vi.fn(), getWorkload: vi.fn(), addVacation: vi.fn() },
    tasks: { getByIteration: vi.fn(), getAssigneeRecommendations: vi.fn(), runBulkOperation: vi.fn(), update: vi.fn(), lookup: vi.fn(), move: vi.fn(), importFromText: vi.fn() },
    labels: { getLabels: vi.fn() },
    gantt: { getChart: vi.fn(), previewSchedule: vi.fn(), schedule: vi.fn() },
    triage: { getAll: vi.fn() },
    share: { getCurrent: vi.fn(), create: vi.fn(), revoke: vi.fn() },
}));

vi.mock('../services/iterationService', () => ({ iterationService: services.iterations }));
vi.mock('../services/teamService', () => ({ teamService: services.team }));
vi.mock('../services/taskService', () => ({ taskService: services.tasks }));
vi.mock('../services/labelService', () => ({ labelService: services.labels }));
vi.mock('../services/ganttService', () => ({ ganttService: services.gantt }));
vi.mock('../services/triageService', () => ({ triageService: services.triage }));
vi.mock('../services/planShareService', () => ({ planShareService: services.share }));
const planning = vi.hoisted(() => ({ readInitial: vi.fn() }));
vi.mock('../services/planningInputService', () => ({ planningInputService: planning }));

const ITERATION = {
    id: 1, name: 'August plan', calendar_id: 1, project: null, project_id: 1,
    start_date: '2026-08-03', end_date: '2026-08-14', working_days: 10,
};
const PLAN_ENTRY = '/plan?project=1&iteration=1';

const checkpoint = (
    id: PlanCheckpoint['id'],
    state: PlanCheckpoint['state'],
    reason_codes: string[] = [],
    counts: Record<string, number> = {},
): PlanCheckpoint => ({ id, state, reason_codes, counts });

const summary = (
    checkpoints: PlanCheckpoint[],
    overrides: Partial<IterationPlanningReadinessSummary> = {},
): IterationPlanningReadinessSummary => ({
    iteration_id: 1, team_member_count: 0, team_capacity_hours: 0, team_members_no_capacity: 0,
    task_count: 0, tasks_without_assignee: 0, tasks_without_effort: 0, has_schedule: false, risk_count: 0,
    checkpoints, checkpoints_done: checkpoints.filter(item => item.state === 'done').length, checkpoints_total: 6,
    ...overrides,
});

// The server's response for each fixture, as app/services/plan_checkpoints.py derives it.
const FIXTURES = {
    empty: summary([
        checkpoint('iteration', 'done'),
        checkpoint('team', 'todo', ['no_people']),
        checkpoint('work', 'todo', ['no_tasks']),
        checkpoint('blockers', 'blocked', ['add_work_first']),
        checkpoint('schedule', 'blocked', ['complete_earlier_checkpoints']),
        checkpoint('review', 'blocked', ['build_schedule_first']),
    ]),
    twoOfSix: summary([
        checkpoint('iteration', 'done'),
        checkpoint('team', 'warn', ['people_without_capacity'], { people_without_capacity: 1 }),
        checkpoint('work', 'done', [], { tasks: 4 }),
        checkpoint('blockers', 'warn', ['unassigned_tasks'], { unassigned_tasks: 2 }),
        checkpoint('schedule', 'blocked', ['complete_earlier_checkpoints']),
        checkpoint('review', 'blocked', ['build_schedule_first']),
    ], { team_member_count: 2, team_members_no_capacity: 1, task_count: 4, tasks_without_assignee: 2 }),
    sixOfSix: summary([
        checkpoint('iteration', 'done'),
        checkpoint('team', 'done', [], { people: 2 }),
        checkpoint('work', 'done', [], { tasks: 4 }),
        checkpoint('blockers', 'done'),
        checkpoint('schedule', 'done'),
        checkpoint('review', 'done'),
    ], { team_member_count: 2, team_capacity_hours: 128, task_count: 4, has_schedule: true }),
};

const TITLES = ['Iteration', 'Capacity', 'Work', 'Blockers', 'Schedule', 'Review'] as const;
const IDS = ['iteration', 'team', 'work', 'blockers', 'schedule', 'review'] as const;

const LocationProbe = () => {
    const location = useLocation();
    return <output data-testid="location">{`${location.pathname}${location.search}`}</output>;
};

const section = (id: typeof IDS[number]) => screen.getByTestId(`plan-section-${id}`);
const toggle = (title: string) => screen.getByRole('button', { name: new RegExp(`${title}$`) });
const stateText = (id: typeof IDS[number]) => within(section(id)).getByText((_, element) => (
    element?.classList.contains('pill') ?? false
)).textContent;

const renderPlan = (entry = PLAN_ENTRY) => renderWithProviders(<><PlanPage /><LocationProbe /></>, { initialEntries: [entry] });

beforeEach(() => {
    vi.resetAllMocks();
    useScopeStore.setState({ project: 1, iteration: 1 });
    services.iterations.getAll.mockResolvedValue([ITERATION]);
    services.iterations.getPlanningReadiness.mockResolvedValue(FIXTURES.empty);
    // The browser's own inputs disagree with the server on purpose: the page must show the server's states.
    services.team.getByIteration.mockResolvedValue([]);
    services.team.getProfiles.mockResolvedValue([]);
    services.tasks.getByIteration.mockResolvedValue([]);
    services.gantt.getChart.mockResolvedValue({ iteration: ITERATION, tasks: [], holidays: [], weekends: [] });
    services.triage.getAll.mockResolvedValue([]);
    services.share.getCurrent.mockResolvedValue(null);
});

afterEach(() => {
    useScopeStore.setState({ project: null, iteration: null });
});

describe('Plan is one page of six checkpoints', () => {
    it('lists the six checkpoints once, in order, with the first incomplete one open and no launcher content', async () => {
        services.iterations.getPlanningReadiness.mockResolvedValue(FIXTURES.twoOfSix);
        const { container } = renderPlan();

        const list = await screen.findByRole('list', { name: 'Checkpoints' });
        expect(within(list).getAllByRole('heading', { level: 2 }).map(heading => heading.textContent?.replace(/^Checkpoint \d+: /, '')))
            .toEqual([...TITLES]);
        expect(screen.getByRole('heading', { level: 1, name: 'Plan' })).toBeVisible();
        expect(screen.getByText('August plan')).toBeVisible();
        expect(screen.getByText('2 of 6')).toBeVisible();

        // Capacity is the first checkpoint that is not done.
        expect(toggle('Capacity')).toHaveAttribute('aria-expanded', 'true');
        for (const title of TITLES.filter(item => item !== 'Capacity')) {
            expect(toggle(title)).toHaveAttribute('aria-expanded', 'false');
        }
        expect(section('team').querySelector('.plan-section-body')).toBeVisible();

        for (const gone of ['Planning checkpoints', 'Direct planning tools', 'Recommended', 'Plan readiness']) {
            expect(screen.queryByText(new RegExp(gone))).not.toBeInTheDocument();
        }
        expect(screen.queryByRole('heading', { name: 'Needs attention' })).not.toBeInTheDocument();
        expect(planPageSource).not.toMatch(/plan-hub|STEP_DEFS|directTools|attentionJobs/);
        expectPageChrome(container, { status: 'migrated' });
    });

    it('names the checkpoint a waiting one waits for, offers no action there, and uses no red or amber', async () => {
        const { user } = renderPlan();
        await screen.findByRole('list', { name: 'Checkpoints' });

        // Blockers waits for Work, Schedule for the first earlier incomplete one, Review for Schedule.
        expect(stateText('blockers')).toBe('Waiting on checkpoint 3');
        expect(stateText('schedule')).toBe('Waiting on checkpoint 2');
        expect(stateText('review')).toBe('Waiting on checkpoint 5');
        expect(within(section('blockers')).getByText('Starts when Work is done.')).toBeVisible();

        await user.click(toggle('Blockers'));
        const blockers = section('blockers');
        const body = blockers.querySelector<HTMLElement>('.plan-section-body')!;
        expect(body).toHaveTextContent('This checkpoint waits for checkpoint 3, Work.');
        expect(within(body).queryAllByRole('link')).toEqual([]);
        expect(within(body).queryAllByRole('button')).toEqual([]);
        // The only control in a waiting section is its own expand toggle.
        expect(within(blockers).getAllByRole('button')).toEqual([toggle('Blockers')]);

        for (const id of ['blockers', 'schedule', 'review'] as const) {
            const waiting = section(id);
            const marked = [waiting, ...Array.from(waiting.querySelectorAll('*'))];
            expect(marked.filter(element => /\b(warn|blocked|danger|exception|error)\b/.test(element.getAttribute('class') ?? '')))
                .toEqual([]);
            expect(waiting.querySelector('.pill')).toHaveClass('opt');
        }
    });

    it('opens /plan/master?step=team as /plan with the Capacity section open', async () => {
        services.iterations.getPlanningReadiness.mockResolvedValue(FIXTURES.sixOfSix);
        renderWithProviders(<>
            <Routes>
                <Route path="/plan" element={<PlanPage />} />
                <Route path="/plan/master" element={<LegacyRedirect><p>Old checkpoint page</p></LegacyRedirect>} />
            </Routes>
            <LocationProbe />
        </>, { initialEntries: ['/plan/master?step=team&project=1&iteration=1'] });

        await screen.findByRole('list', { name: 'Checkpoints' });
        expect(screen.queryByText('Old checkpoint page')).not.toBeInTheDocument();
        expect(screen.getByTestId('location')).toHaveTextContent(/^\/plan\?step=team&project=1&iteration=1$/);
        expect(toggle('Capacity')).toHaveAttribute('aria-expanded', 'true');
        expect(TITLES.filter(title => toggle(title).getAttribute('aria-expanded') === 'true')).toEqual(['Capacity']);
    });

    it.each([
        ['an empty iteration', FIXTURES.empty, '1 of 6',
            ['Done', 'Next', 'Next', 'Waiting on checkpoint 3', 'Waiting on checkpoint 2', 'Waiting on checkpoint 5'], 'Capacity'],
        ['2 of 6', FIXTURES.twoOfSix, '2 of 6',
            ['Done', 'Needs attention', 'Done', 'Needs attention', 'Waiting on checkpoint 2', 'Waiting on checkpoint 5'], 'Capacity'],
        ['6 of 6', FIXTURES.sixOfSix, '6 of 6',
            ['Done', 'Done', 'Done', 'Done', 'Done', 'Done'], 'Review'],
    ])('shows the states of the planning-readiness response for %s', async (_name, response, progress, labels, openTitle) => {
        services.iterations.getPlanningReadiness.mockResolvedValue(response);
        renderPlan();
        await screen.findByRole('list', { name: 'Checkpoints' });

        expect(services.iterations.getPlanningReadiness).toHaveBeenCalledWith(1);
        expect(IDS.map(id => section(id).getAttribute('data-state'))).toEqual(response.checkpoints!.map(item => item.state));
        expect(IDS.map(stateText)).toEqual(labels);
        expect(screen.getByText(progress)).toBeVisible();
        expect(TITLES.filter(title => toggle(title).getAttribute('aria-expanded') === 'true')).toEqual([openTitle]);
    });

    it('keeps the at-risk signals in the Review section with a link to the filtered tasks', async () => {
        services.gantt.getChart.mockResolvedValue({ iteration: ITERATION, tasks: [scheduledTask({ is_delayed: true })], holidays: [], weekends: [] });
        services.iterations.getPlanningReadiness.mockResolvedValue(summary(
            FIXTURES.sixOfSix.checkpoints!.map(item => (item.id === 'review'
                ? checkpoint('review', 'warn', ['risks_to_acknowledge'], { risks: 1 })
                : item)),
            { team_member_count: 2, task_count: 4, has_schedule: true, risk_count: 1 },
        ));
        renderPlan();
        await screen.findByRole('list', { name: 'Checkpoints' });

        const review = section('review');
        expect(within(review).getByText('Needs attention')).toBeVisible();
        expect(within(review).getAllByText('1 planning exception to review')[0]).toBeVisible();
        expect(within(review).getByText('At-risk signals')).toBeVisible();
        expect(await within(review).findByRole('link', { name: 'At-risk signals: 1' }))
            .toHaveAttribute('href', '/tasks?planningIssue=at-risk&fromPlanStep=review&project=1&iteration=1');
    });

    it('names the reason beside each at-risk task in Review', async () => {
        services.gantt.getChart.mockResolvedValue({ iteration: ITERATION, tasks: [
            scheduledTask({ is_delayed: true }),
            scheduledTask({ id: 12, title: 'Ship notes', is_overdue: true, is_outside_constraints: true }),
        ], holidays: [], weekends: [] });
        services.iterations.getPlanningReadiness.mockResolvedValue(summary(
            FIXTURES.sixOfSix.checkpoints!.map(item => (item.id === 'review'
                ? checkpoint('review', 'warn', ['risks_to_acknowledge'], { risks: 2 })
                : item)),
            { team_member_count: 2, task_count: 4, has_schedule: true, risk_count: 2 },
        ));
        renderPlan();
        await screen.findByRole('list', { name: 'Checkpoints' });

        const list = await within(section('review')).findByRole('region', { name: 'Tasks at risk' });
        const first = within(list).getByRole('link', { name: 'Prepare release' }).closest('li')!;
        expect(first).toHaveTextContent('Not started by its planned start');
        const second = within(list).getByRole('link', { name: 'Ship notes' }).closest('li')!;
        expect(second).toHaveTextContent('Past its end date; Outside its date limits');
        // A task link opens the Tasks list filtered to at-risk work, where the same reasons are shown.
        const href = new URL(within(second).getByRole('link', { name: 'Ship notes' }).getAttribute('href')!, 'http://localhost');
        expect(href.pathname).toBe('/tasks');
        expect(href.searchParams.get('planningIssue')).toBe('at-risk');
        expect(href.searchParams.get('task')).toBe('12');
        expect(href.searchParams.get('fromPlanStep')).toBe('review');
    });

    it('names a missed planned start in Review when the server flags a task whose current start is still ahead', async () => {
        const ahead = new Date(Date.now() + 7 * 86_400_000).toISOString().slice(0, 10);
        services.gantt.getChart.mockResolvedValue({ iteration: ITERATION, tasks: [
            scheduledTask({ is_delayed: true, start_date: ahead, end_date: ahead }),
        ], holidays: [], weekends: [] });
        services.iterations.getPlanningReadiness.mockResolvedValue(summary(
            FIXTURES.sixOfSix.checkpoints!.map(item => (item.id === 'review'
                ? checkpoint('review', 'warn', ['risks_to_acknowledge'], { risks: 1 })
                : item)),
            { team_member_count: 2, task_count: 4, has_schedule: true, risk_count: 1 },
        ));
        renderPlan();
        await screen.findByRole('list', { name: 'Checkpoints' });

        const list = await within(section('review')).findByRole('region', { name: 'Tasks at risk' });
        const row = within(list).getByRole('link', { name: 'Prepare release' }).closest('li')!;
        expect(row).toHaveTextContent('Not started by its planned start');
        expect(row).not.toHaveTextContent(/before today/i);
    });

    it('re-reads readiness on return and opens the next checkpoint once the returned one is done', async () => {
        services.iterations.getPlanningReadiness.mockResolvedValueOnce(FIXTURES.empty).mockResolvedValue(FIXTURES.twoOfSix);
        renderPlan('/plan?step=work&returned=1&project=1&iteration=1');

        await waitFor(() => expect(services.iterations.getPlanningReadiness).toHaveBeenCalledTimes(2));
        await waitFor(() => expect(screen.getByTestId('location')).toHaveTextContent(/^\/plan\?project=1&iteration=1$/));
        expect(stateText('work')).toBe('Done');
        expect(toggle('Capacity')).toHaveAttribute('aria-expanded', 'true');
        expect(toggle('Work')).toHaveAttribute('aria-expanded', 'false');
    });

    it('opens one section at a time and keeps it in the link', async () => {
        const { user } = renderPlan();
        await screen.findByRole('list', { name: 'Checkpoints' });

        await user.click(toggle('Iteration'));
        expect(toggle('Iteration')).toHaveAttribute('aria-expanded', 'true');
        expect(toggle('Capacity')).toHaveAttribute('aria-expanded', 'false');
        expect(screen.getByTestId('location')).toHaveTextContent('step=iteration');
        // Iterations are managed in place: no link leaves the page for them.
        expect(within(section('iteration')).queryByRole('link', { name: /Open iterations/ })).not.toBeInTheDocument();
        expect(within(section('iteration')).getByRole('button', { name: 'Edit' })).toBeVisible();
        expect(within(section('iteration')).getByRole('button', { name: 'New iteration' })).toBeVisible();
        expect(within(section('iteration')).getByRole('button', { name: 'All iterations' })).toBeVisible();
    });

    it('starts another iteration from its first incomplete checkpoint after a section was opened by hand', async () => {
        const next = { ...ITERATION, id: 2, name: 'September plan', start_date: '2026-09-07', end_date: '2026-09-18' };
        services.iterations.getAll.mockResolvedValue([ITERATION, next]);
        services.iterations.getPlanningReadiness.mockImplementation(async (id: number) => (id === 2 ? FIXTURES.empty : FIXTURES.sixOfSix));
        // The scope bar's own command, so the section opened by hand stays in the link while the iteration changes.
        const ScopeNext = () => {
            const { setIteration } = useSetWorkScope();
            return <button type="button" onClick={() => setIteration(2)}>Scope the next iteration</button>;
        };
        const { user } = renderWithProviders(<><PlanPage /><ScopeNext /><LocationProbe /></>, { initialEntries: [PLAN_ENTRY] });
        await screen.findByRole('list', { name: 'Checkpoints' });
        await waitFor(() => expect(stateText('review')).toBe('Done'));

        await user.click(toggle('Iteration'));
        expect(toggle('Iteration')).toHaveAttribute('aria-expanded', 'true');
        expect(screen.getByTestId('location')).toHaveTextContent('step=iteration');
        // A new iteration comes into scope: its own first incomplete checkpoint opens, and the
        // section chosen for the previous iteration leaves the link.
        await user.click(screen.getByRole('button', { name: 'Scope the next iteration' }));
        await waitFor(() => expect(screen.getByTestId('location')).toHaveTextContent(/^\/plan\?project=1&iteration=2$/));
        await waitFor(() => expect(toggle('Capacity')).toHaveAttribute('aria-expanded', 'true'));
        expect(toggle('Iteration')).toHaveAttribute('aria-expanded', 'false');
    });

    it('keeps the section a link names together with another iteration', async () => {
        const next = { ...ITERATION, id: 2, name: 'September plan', start_date: '2026-09-07', end_date: '2026-09-18' };
        services.iterations.getAll.mockResolvedValue([ITERATION, next]);
        services.iterations.getPlanningReadiness.mockImplementation(async (id: number) => (id === 2 ? FIXTURES.empty : FIXTURES.sixOfSix));
        const OpenNext = () => {
            const navigate = useNavigate();
            return <button type="button" onClick={() => navigate('/plan?step=work&project=1&iteration=2')}>Open the next work</button>;
        };
        const { user } = renderWithProviders(<><PlanPage /><OpenNext /><LocationProbe /></>, { initialEntries: [PLAN_ENTRY] });
        await screen.findByRole('list', { name: 'Checkpoints' });
        await user.click(toggle('Iteration'));

        await user.click(screen.getByRole('button', { name: 'Open the next work' }));
        await waitFor(() => expect(toggle('Work')).toHaveAttribute('aria-expanded', 'true'));
        expect(screen.getByTestId('location')).toHaveTextContent('step=work');
    });

    it('opens the All iterations drawer over the checkpoints when the link asks for it', async () => {
        renderPlan('/plan?panel=iterations&project=1&iteration=1');
        expect(await screen.findByRole('dialog', { name: 'All iterations' })).toBeVisible();
        expect(await screen.findByRole('list', { name: 'Checkpoints' })).toBeInTheDocument();
    });

    it('says the checkpoints are unavailable when the readiness response fails, and retries', async () => {
        services.iterations.getPlanningReadiness.mockRejectedValueOnce(new Error('offline')).mockResolvedValue(FIXTURES.empty);
        const { user } = renderPlan();

        expect(await screen.findByRole('heading', { name: 'Checkpoint states are unavailable' })).toBeVisible();
        await user.click(screen.getByRole('button', { name: /Retry/ }));
        expect(await screen.findByRole('list', { name: 'Checkpoints' })).toBeVisible();
    });

    it('has English and Russian copy for the page', async () => {
        await changeAppLanguage('ru');
        try {
            renderPlan();
            expect(await screen.findByRole('list', { name: 'Контрольные точки' })).toBeVisible();
            expect(screen.getByText('1 из 6')).toBeVisible();
            expect(stateText('blockers')).toBe('Ждёт контрольную точку 3');
        } finally {
            await changeAppLanguage('en');
        }
    });
});

const profile = (id: number, kind: 'human' | 'agent'): TeamMemberProfile => ({
    id, display_name: kind === 'human' ? `Person ${id}` : `Agent ${id}`, profile_kind: kind,
    automation_enabled: false, assignment_modes: [], skills: [], created_at: '', updated_at: '',
});
const capacityRow = (id: number, kind: 'human' | 'agent'): TeamMember => ({
    id, iteration_id: 1, profile_id: id, name: profile(id, kind).display_name, position: 'Developer',
    availability_percent: 100, professionalism_coefficient: 1, operational_utilization: kind === 'agent' ? 0 : 20,
    profile: profile(id, kind), vacations: [],
});
const capacityReady = (rows: TeamMember[], hours: number) => summary([
    checkpoint('iteration', 'done'), checkpoint('team', 'done', [], { people: rows.length }),
    ...FIXTURES.empty.checkpoints!.slice(2),
], { team_member_count: rows.length, team_agent_count: rows.filter(row => row.profile?.profile_kind === 'agent').length, team_capacity_hours: hours });

// Stateful service doubles return new server responses after writes; checkpoint states are never derived by the page.
const capacityWorkspace = (initial: TeamMember[] = []) => {
    const rows = [...initial];
    const profiles = [profile(1, 'human'), profile(2, 'agent'), profile(3, 'human')];
    let revision = 1;
    services.team.getProfiles.mockResolvedValue(profiles);
    services.team.getByIteration.mockImplementation(async () => [...rows]);
    services.team.getWorkload.mockImplementation(async (id: number) => ({
        team_member_id: id, capacity_hours: rows.find(row => row.id === id)?.vacations.length ? 57.6 : 64,
    }));
    services.iterations.getPlanningReadiness.mockImplementation(async () => rows.length
        ? capacityReady(rows, rows.reduce((hours, row) => hours + (row.vacations.length ? 57.6 : 64), 0))
        : FIXTURES.empty);
    planning.readInitial.mockImplementation(async (_kind: string, id: number, creating: boolean) => ({
        resource: creating ? { id } : rows.find(row => row.id === id), expected_revisions: { 1: revision++ },
    }));
    services.team.create.mockImplementation(async (_id: number, data: TeamMemberCreate) => {
        const row: TeamMember = { ...data, id: rows.length + 1, iteration_id: 1, vacations: [], profile: profiles.find(profile => profile.id === data.profile_id) };
        rows.push(row);
        return row;
    });
    services.team.addVacation.mockImplementation(async (id: number, dates: { start_date: string; end_date: string }) => {
        const vacation = { id: 8, ...dates };
        const index = rows.findIndex(row => row.id === id);
        rows[index] = { ...rows[index], vacations: [...rows[index].vacations, vacation] };
        return vacation;
    });
    return rows;
};

describe('capacity inside Plan', () => {
    it('adds three people and agents to an empty iteration in one action and shows the server Done checkpoint', async () => {
        capacityWorkspace();
        const { user } = renderPlan();
        await user.click(await screen.findByRole('button', { name: 'Add capacity' }));
        await user.click(await screen.findByRole('checkbox', { name: /Person 1/ }));
        await user.click(screen.getByRole('checkbox', { name: /Agent 2/ }));
        await user.click(screen.getByRole('checkbox', { name: /Person 3/ }));
        await user.click(screen.getByRole('button', { name: 'Add selected' }));
        await waitFor(() => expect(stateText('team')).toBe('Done'));
        expect(services.team.create).toHaveBeenCalledTimes(3);
        expect(services.team.create.mock.calls.map(call => call[1].operational_utilization)).toEqual([20, 0, 20]);
        expect(services.team.create.mock.calls.map(call => call[2])).toEqual([{ 1: 1 }, { 1: 2 }, { 1: 3 }]);
        expect(toggle('Work')).toHaveAttribute('aria-expanded', 'true');
        await user.click(toggle('Capacity'));
        expect(within(await screen.findByRole('table')).getAllByRole('row')).toHaveLength(4);
        expect(screen.getByTestId('location')).toHaveTextContent('/plan?project=1&iteration=1');
        expect(within(section('team')).queryByRole('link')).not.toBeInTheDocument();
    });

    it('copies every previous iteration row with its availability and skips existing members on repeat', async () => {
        const rows = capacityWorkspace();
        const previous = { ...ITERATION, id: 2, start_date: '2026-07-20', end_date: '2026-07-31' };
        services.iterations.getAll.mockResolvedValue([ITERATION, previous,
            { ...previous, id: 99, project_id: 8, end_date: '2026-08-01' },
            { ...previous, id: 98, end_date: '2026-09-01' }]);
        const source = [capacityRow(1, 'human'), capacityRow(2, 'agent'), { ...capacityRow(3, 'human'), profile_id: null, profile: null }]
            .map((row, index) => ({ ...row, availability_percent: [75, 50, 90][index], operational_utilization: index === 1 ? 5 : 20, professionalism_coefficient: 1.2 }));
        services.team.getByIteration.mockImplementation(async (id: number) => id === 2 ? source : [...rows]);
        const { user } = renderPlan('/plan?step=team&project=1&iteration=1');
        await user.click(await screen.findByRole('button', { name: 'Copy from previous iteration' }));
        await waitFor(() => expect(services.team.create).toHaveBeenCalledTimes(3));
        await screen.findByText('Previous capacity copied. Existing members were kept.');
        for (const [index, row] of source.entries()) {
            expect(services.team.create.mock.calls[index][1]).toEqual(expect.objectContaining({
                availability_percent: row.availability_percent, operational_utilization: row.operational_utilization,
                professionalism_coefficient: row.professionalism_coefficient, profile_id: row.profile_id,
            }));
        }
        await user.click(screen.getByRole('button', { name: 'Copy from previous iteration' }));
        await waitFor(() => expect(screen.getByRole('button', { name: 'Copy from previous iteration' })).toBeEnabled());
        expect(services.team.create).toHaveBeenCalledTimes(3);
        expect(services.team.getByIteration).not.toHaveBeenCalledWith(99);
        expect(services.team.getByIteration).not.toHaveBeenCalledWith(98);
        expect(stateText('team')).toBe('Done');
    });

    it('adds time off in Plan and refreshes the member row and its hours', async () => {
        capacityWorkspace([capacityRow(1, 'human')]);
        const { user } = renderPlan('/plan?step=team&project=1&iteration=1');
        const table = await screen.findByRole('table');
        expect(await within(table).findByText('64 h')).toBeVisible();
        await user.click(screen.getByRole('button', { name: 'Actions for Person 1' }));
        await user.click(screen.getByRole('menuitem', { name: 'Time off' }));
        const dialog = await screen.findByRole('dialog');
        await user.type(await within(dialog).findByLabelText('Start date'), '2026-08-05');
        await user.type(within(dialog).getByLabelText('End date'), '2026-08-05');
        await user.click(within(dialog).getByRole('button', { name: 'Add vacation' }));
        expect(await within(table).findByText('57.6 h')).toBeInTheDocument();
        expect(within(table).getByText('Aug 5, 2026 – Aug 5, 2026')).toBeInTheDocument();
        expect(services.team.addVacation).toHaveBeenCalledWith(1, { start_date: '2026-08-05', end_date: '2026-08-05' }, { 1: 1 });
        expect(await screen.findByText('1 person, 0 agents, 57.6 h')).toBeInTheDocument();
    });

    it('reports people and agents separately with the total hours from the server', async () => {
        capacityWorkspace([capacityRow(1, 'human'), capacityRow(2, 'human'), capacityRow(3, 'agent'), capacityRow(4, 'agent'), capacityRow(5, 'agent')]);
        services.iterations.getPlanningReadiness.mockResolvedValue(capacityReady([
            capacityRow(1, 'human'), capacityRow(2, 'human'), capacityRow(3, 'agent'), capacityRow(4, 'agent'), capacityRow(5, 'agent'),
        ], 412));
        renderPlan();
        expect(await screen.findByText('2 people, 3 agents, 412 h')).toBeVisible();
    });
});

const plannedTask = (id: number, overrides: Partial<Task> = {}): Task => ({
    id, title: `Work item ${id}`, iteration_id: 1, project_id: 1, status: 'planned', version: 1,
    effort_hours: 2, effort_days: 0.25, nominal_day_hours: 8, tags: ['cap:code'], assignee: null,
    is_composite: false, is_deferred: false, children: [], ...overrides,
} as Task);

const workWorkspace = (initial: Task[]) => {
    const tasks = [...initial];
    let revision = 7;
    const rows = [capacityRow(1, 'human'), capacityRow(2, 'agent')];
    services.iterations.getById.mockImplementation(async () => ({ ...ITERATION, revision }));
    services.team.getByIteration.mockResolvedValue(rows);
    services.labels.getLabels.mockResolvedValue([{ slug: 'cap:code', name: 'Code' }, { slug: 'cap:test', name: 'Test' }]);
    services.tasks.getByIteration.mockImplementation(async () => [...tasks]);
    services.tasks.getAssigneeRecommendations.mockImplementation(async (id: number) => [{ team_member_id: tasks.find(task => task.id === id)?.tags.includes('cap:test') ? 2 : 1, score: 90 }]);
    services.team.getWorkload.mockImplementation(async (id: number) => ({ team_member_id: id, allocated_hours: id === 1 ? 20 : 8, capacity_hours: 60 }));
    services.iterations.getPlanningReadiness.mockImplementation(async () => {
        const eligible = tasks.filter(task => task.status === 'planned' && !task.is_composite && !task.is_deferred && !task.children?.length);
        const unassigned = eligible.filter(task => !task.assignee && !task.agent_working).length;
        const effort = eligible.filter(task => !task.effort_days).length;
        return summary([
            checkpoint('iteration', 'done'), checkpoint('team', 'done'), checkpoint('work', 'done', [], { tasks: tasks.length }),
            checkpoint('blockers', unassigned || effort ? 'warn' : 'done', [], { unassigned_tasks: unassigned, tasks_without_effort: effort }),
            checkpoint('schedule', 'todo'), checkpoint('review', 'blocked'),
        ], { task_count: tasks.length, tasks_without_assignee: unassigned, tasks_without_effort: effort });
    });
    services.tasks.runBulkOperation.mockImplementation(async (request: TaskBulkOperationRequest) => {
        expect(request.expected_revisions).toEqual({ 1: revision });
        const before = revision;
        if (!request.dry_run) revision++;
        const results = request.task_ids.map(id => {
            const index = tasks.findIndex(task => task.id === id);
            expect(request.expected_versions?.[id]).toBe(tasks[index].version);
            if (!request.dry_run) tasks[index] = { ...tasks[index], assignee: rows.find(row => row.id === request.payload?.assignee_id), version: tasks[index].version + 1, iteration_revision: revision };
            return { task_id: id, outcome: request.dry_run ? 'would_update' : 'updated', warnings: [], changes: {}, task: request.dry_run ? null : tasks[index] };
        });
        return { requested_count: request.task_ids.length, succeeded_count: request.task_ids.length, failed_count: 0, dry_run: request.dry_run,
            task_versions: request.expected_versions, input_revisions: { 1: before }, results };
    });
    services.tasks.update.mockImplementation(async (id: number, update: Partial<Task>) => {
        const index = tasks.findIndex(task => task.id === id);
        tasks[index] = { ...tasks[index], effort_hours: update.effort_hours!, effort_days: update.effort_hours! / 8, version: tasks[index].version + 1 };
        revision++;
        return tasks[index];
    });
    return tasks;
};
const BLOCKERS_ENTRY = '/plan?step=blockers&project=1&iteration=1';

describe('work and blockers inside Plan', () => {
    it('assigns all 48 unassigned tasks from Plan in one preview and apply', async () => {
        const tasks = workWorkspace(Array.from({ length: 48 }, (_, index) => plannedTask(index + 1, { tags: [index < 24 ? 'cap:code' : 'cap:test'] })));
        const { user } = renderPlan(BLOCKERS_ENTRY);
        const preview = await screen.findByRole('button', { name: 'Preview assignments' });
        await waitFor(() => expect(preview).toBeEnabled());
        expect(screen.getByLabelText('Assignee for Code')).toHaveValue('1');
        expect(screen.getByLabelText('Assignee for Test')).toHaveValue('2');
        await user.click(preview);
        await user.click(await screen.findByRole('button', { name: 'Assign 48 tasks' }));
        await screen.findByText('48 tasks assigned.');
        expect(tasks.every(task => task.assignee)).toBe(true);
        expect(new Set(services.tasks.getAssigneeRecommendations.mock.calls.map(call => call[0])).size).toBe(48);
        const requests = services.tasks.runBulkOperation.mock.calls.map(call => call[0] as TaskBulkOperationRequest);
        expect(requests.filter(request => request.dry_run).flatMap(request => request.task_ids)).toHaveLength(48);
        expect(requests.filter(request => !request.dry_run).flatMap(request => request.task_ids)).toEqual(Array.from({ length: 48 }, (_, i) => i + 1));
        expect(requests.filter(request => !request.dry_run).map(request => request.expected_revisions)).toEqual([{ 1: 7 }, { 1: 8 }]);
        await waitFor(() => expect(stateText('blockers')).toBe('Done'));
        expect(screen.getByTestId('location')).toHaveTextContent('/plan?step=blockers&project=1&iteration=1');
    });

    it('uses planning-readiness counts and lists no finished, active, deferred or composite task', async () => {
        workWorkspace([plannedTask(1, { effort_days: null, effort_hours: null }),
            plannedTask(2, { title: 'Finished work', status: 'resolved', effort_days: null }),
            plannedTask(3, { title: 'Closed work', status: 'closed' }),
            plannedTask(4, { title: 'Active work', status: 'active' }),
            plannedTask(5, { title: 'Deferred work', is_deferred: true }),
            plannedTask(6, { title: 'Composite work', is_composite: true }),
            plannedTask(7, { title: 'Agent held work', agent_working: true }),
        ]);
        services.iterations.getPlanningReadiness.mockResolvedValue(summary([
            checkpoint('iteration', 'done'), checkpoint('team', 'done'), checkpoint('work', 'done', [], { tasks: 99 }),
            checkpoint('blockers', 'warn', [], { unassigned_tasks: 48, tasks_without_effort: 12 }),
            checkpoint('schedule', 'blocked'), checkpoint('review', 'blocked'),
        ], { task_count: 99, tasks_without_assignee: 48, tasks_without_effort: 12 }));
        const { user } = renderPlan(BLOCKERS_ENTRY);
        expect(await screen.findByRole('heading', { name: 'Needs an assignee · 48' })).toBeVisible();
        expect(screen.getByRole('heading', { name: 'Needs effort · 12' })).toBeVisible();
        await screen.findByLabelText('Assignee for Code');
        for (const title of ['Finished work', 'Closed work', 'Active work', 'Deferred work', 'Composite work', 'Agent held work']) expect(screen.queryByText(title)).not.toBeInTheDocument();
        expect(screen.getAllByRole('link', { name: 'Open in Tasks selection mode' }).every(link => link.getAttribute('href')?.includes('mode=bulk'))).toBe(true);
        await user.click(toggle('Work'));
        expect(await screen.findByText(/99 tasks · .* h total effort/)).toBeVisible();
    });

    it('previews hours per row and marks the row that exceeds capacity before applying', async () => {
        workWorkspace(Array.from({ length: 48 }, (_, i) => plannedTask(i + 1, { tags: [i < 24 ? 'cap:code' : 'cap:test'] })));
        const { user } = renderPlan(BLOCKERS_ENTRY);
        const preview = await screen.findByRole('button', { name: 'Preview assignments' });
        await waitFor(() => expect(preview).toBeEnabled());
        await user.click(preview);
        const region = await screen.findByRole('region', { name: 'Preview assignments' });
        const rows = within(region).getAllByRole('row');
        expect(rows[1]).toHaveTextContent('Person 120 h48 h68 hExceeds capacity60 h');
        expect(rows[2]).toHaveTextContent('Agent 28 h48 h56 h60 h');
        expect(within(rows[2]).queryByText('Exceeds capacity')).not.toBeInTheDocument();
        expect(services.tasks.runBulkOperation.mock.calls.every(call => call[0].dry_run)).toBe(true);
        await user.selectOptions(screen.getByLabelText('Assignee for Code'), '2');
        expect(screen.queryByRole('region', { name: 'Preview assignments' })).not.toBeInTheDocument();
        expect(screen.queryByRole('button', { name: 'Assign 48 tasks' })).not.toBeInTheDocument();
    });

    it('saves effort as hours with a day hint and refreshes the server count', async () => {
        workWorkspace([plannedTask(1, { effort_days: null, effort_hours: null })]);
        const { user } = renderPlan(BLOCKERS_ENTRY);
        await user.type(await screen.findByRole('spinbutton', { name: /Work item 1.*Effort \(hours\)/ }), '12');
        expect(screen.getByText('1.5 days at 8 h/day')).toBeVisible();
        await user.click(screen.getByRole('button', { name: 'Save' }));
        await waitFor(() => expect(services.tasks.update).toHaveBeenCalledWith(1, { effort_hours: 12, expected_version: 1, expected_revision: 7 }));
        expect(await screen.findByRole('heading', { name: 'Needs effort · 0' })).toBeVisible();
    });

    it.each([
        { language: 'en', hints: ['1 day at 8 h/day', '2 days at 8 h/day', '5 days at 8 h/day'] },
        { language: 'ru', hints: ['1 день при 8 ч/день', '2 дня при 8 ч/день', '5 дней при 8 ч/день'] },
    ])('pluralizes the inline effort hint for 1, 2 and 5 days in $language', async ({ language, hints }) => {
        await changeAppLanguage(language);
        try {
            workWorkspace([plannedTask(1, { effort_days: null, effort_hours: null })]);
            const { user } = renderPlan(BLOCKERS_ENTRY);
            const input = await screen.findByRole('spinbutton', { name: /Work item 1/ });
            for (const [index, hours] of [8, 16, 40].entries()) {
                await user.clear(input);
                await user.type(input, String(hours));
                expect(screen.getByText(hints[index])).toBeVisible();
            }
        } finally {
            await changeAppLanguage('en');
        }
    });

    it('stops after a partial assignment and reports the applied count without retrying stale batches', async () => {
        workWorkspace([plannedTask(1), plannedTask(2, { tags: ['cap:test'] })]);
        const original = services.tasks.runBulkOperation.getMockImplementation()!;
        services.tasks.runBulkOperation.mockImplementation(async request => {
            if (!request.dry_run && request.payload.assignee_id === 2) throw new Error('The iteration changed.');
            return original(request);
        });
        const { user } = renderPlan(BLOCKERS_ENTRY);
        const preview = await screen.findByRole('button', { name: 'Preview assignments' });
        await waitFor(() => expect(preview).toBeEnabled());
        await user.click(preview);
        await user.click(await screen.findByRole('button', { name: 'Assign 2 tasks' }));
        expect(await screen.findByRole('alert')).toHaveTextContent('1 task assigned. Assignment stopped');
        expect(services.tasks.runBulkOperation).toHaveBeenCalledTimes(4);
        expect(screen.queryByRole('button', { name: 'Assign 2 tasks' })).not.toBeInTheDocument();
        await screen.findByRole('heading', { name: 'Needs an assignee · 1' });
    });

    it('adds project backlog selections across pages with observed versions', async () => {
        const tasks = workWorkspace([]);
        services.tasks.lookup.mockImplementation(async ({ after_id }) => ({ items: after_id ? [plannedTask(12)] : [plannedTask(11)], has_more: !after_id, next_after_id: after_id ? null : 11 }));
        services.tasks.move.mockImplementation(async (id: number) => { tasks.push(plannedTask(id)); return { iteration_revision: id === 11 ? 8 : 9 }; });
        const { user } = renderPlan('/plan?step=work&project=1&iteration=1');
        await user.click(await screen.findByRole('button', { name: 'Add from backlog' }));
        await user.click(await screen.findByRole('checkbox', { name: 'Work item 11' }));
        await user.click(screen.getByRole('checkbox', { name: 'Work item 12' }));
        await user.click(screen.getByRole('button', { name: 'Add 2 tasks' }));
        await waitFor(() => expect(services.tasks.move).toHaveBeenCalledTimes(2));
        expect(services.tasks.lookup).toHaveBeenCalledWith(expect.objectContaining({ project_id: 1, backlog_only: true, after_id: 11 }));
        expect(services.tasks.move.mock.calls).toEqual([
            [11, { iteration_id: 1, expected_version: 1, expected_revisions: { 1: 7 } }],
            [12, { iteration_id: 1, expected_version: 1, expected_revisions: { 1: 8 } }],
        ]);
        expect(await screen.findByText('2 tasks · 4 h total effort')).toBeVisible();
    });

    it('creates a new task inside Plan for the iteration in scope', async () => {
        workWorkspace([]);
        const { user } = renderPlan('/plan?step=work&project=1&iteration=1');
        await user.click(await screen.findByRole('button', { name: 'New task' }));
        const drawer = await screen.findByRole('dialog', { name: 'Create new task' });
        expect(within(drawer).getByRole('textbox', { name: /Task title/ })).toBeVisible();
        // The work is created here; the page still offers the full Tasks page only as a link.
        expect(screen.getByTestId('location')).toHaveTextContent(/^\/plan\?/);
    });

    it('imports tasks inside Plan using the existing version-bound import dialog', async () => {
        workWorkspace([]);
        services.tasks.importFromText.mockResolvedValue({ task_count: 1, triage_count: 0 });
        const { user } = renderPlan('/plan?step=work&project=1&iteration=1');
        await user.click(await screen.findByRole('button', { name: 'Import tasks' }));
        const dialog = await screen.findByRole('dialog');
        const editor = within(dialog).getByPlaceholderText('Or paste text here…');
        await waitFor(() => expect(editor).not.toHaveAttribute('readonly'));
        await user.type(editor, '- New work');
        await user.click(within(dialog).getByRole('button', { name: 'Import tasks' }));
        await waitFor(() => expect(services.tasks.importFromText).toHaveBeenCalledWith(1, '- New work', { destination: 'tasks', expectedRevision: 7 }));
    });
});

const scheduledTask = (overrides: Partial<GanttTask> = {}): GanttTask => ({
    id: 11, title: 'Prepare release', start_date: '2026-08-03', end_date: '2026-08-10',
    effort_hours: 40, effort_days: 5, calculated_effort_days: 5, progress: 0, priority: 2, status: 'planned',
    is_composite: false, is_overdue: false, is_delayed: false, is_optional: false,
    is_outside_constraints: false, tags: [], assignee: { id: 1, name: 'Person 1' },
    assignees: [{ id: 1, name: 'Person 1' }], children: [], dependencies: [], ...overrides,
});
/** A task as the iteration task list returns it (deferred tasks included, unlike the Gantt response). */
const listedTask = (overrides: Partial<Task> = {}): Task => plannedTask(11, {
    title: 'Prepare release', start_date: '2026-08-03', end_date: '2026-08-10', effort_hours: 40, effort_days: 5,
    assignee: { id: 1, name: 'Person 1' }, effective_is_deferred: false, ...overrides,
} as Partial<Task>);
const scheduleReady = summary([
    ...FIXTURES.sixOfSix.checkpoints!.slice(0, 4), checkpoint('schedule', 'todo', ['schedule_not_built']),
    checkpoint('review', 'blocked', ['build_schedule_first']),
], { team_member_count: 1, team_capacity_hours: 64, task_count: 1 });
const scheduleWorkspace = (end = '2026-08-10') => {
    let applied = false;
    const task = scheduledTask({ end_date: end });
    const result = { success: true, decisions: [], workload_balanced: true, workload_issues: [], unscheduled: [] };
    const preview: SchedulePreviewResponse = { input_revision: 7, input_planning_revision: 19, tasks: [task], overdue_task_ids: [], schedule_result: result };
    services.team.getByIteration.mockResolvedValue([capacityRow(1, 'human')]);
    services.team.getWorkload.mockResolvedValue({ team_member_id: 1, name: 'Person 1', allocated_hours: 40, capacity_hours: 64 });
    services.iterations.getAll.mockResolvedValue([{ ...ITERATION, revision: 7 }]);
    services.gantt.getChart.mockImplementation(async () => ({ iteration: { ...ITERATION, revision: 7 }, tasks: applied ? [task] : [], schedule_result: applied ? result : null }));
    services.gantt.previewSchedule.mockResolvedValue(preview);
    services.gantt.schedule.mockImplementation(async () => { applied = true; return result; });
    services.tasks.getByIteration.mockImplementation(async () => [listedTask(applied ? { end_date: end } : { start_date: null, end_date: null })]);
    services.iterations.getPlanningReadiness.mockImplementation(async () => !applied ? scheduleReady : summary([
        ...scheduleReady.checkpoints!.slice(0, 4), checkpoint('schedule', 'done'),
        end > ITERATION.end_date ? checkpoint('review', 'warn', ['risks_to_acknowledge'], { risks: 1 }) : checkpoint('review', 'done'),
    ], { team_member_count: 1, team_capacity_hours: 64, task_count: 1,
        has_schedule: true, risk_count: end > ITERATION.end_date ? 1 : 0,
    }));
    return { preview, result };
};

describe('schedule and review inside Plan', () => {
    it('calculates and applies assigned work without leaving Plan and reads Schedule Done from the server', async () => {
        scheduleWorkspace();
        const { user } = renderPlan();
        await user.click(await screen.findByRole('button', { name: 'Calculate schedule' }));
        expect(services.gantt.previewSchedule).toHaveBeenCalledWith(1, [], 7);
        expect(stateText('schedule')).toBe('Next');
        expect(screen.getByText('Calculated schedule · not saved')).toBeVisible();
        const table = await screen.findByRole('table', { name: 'Hours against capacity per assignee' });
        expect(within(table).getByText('40 h')).toBeVisible();
        expect(within(table).getByText('64 h')).toBeVisible();
        expect(screen.getByText('Calculated end')).toBeVisible();
        expect(screen.getByText('Iteration end')).toBeVisible();
        expect(screen.getAllByText('Dates are calculated. To move a task, change who does it, its effort, what it waits for, or its earliest start.')).toHaveLength(1);
        expect(screen.getByRole('link', { name: 'Open in Gantt' })).toHaveAttribute('href', '/gantt?fromPlanStep=schedule&project=1&iteration=1');
        await user.click(screen.getByRole('button', { name: 'Apply schedule' }));
        expect(services.gantt.schedule).toHaveBeenCalledWith(1, 7, 19);
        await waitFor(() => expect(stateText('schedule')).toBe('Done'));
        expect(screen.getByText('6 of 6')).toBeVisible();
        expect(screen.getByTestId('location')).toHaveTextContent(PLAN_ENTRY);
    });

    it('lists a task without dates with the exact reason text returned by the server', async () => {
        const { preview } = scheduleWorkspace();
        const message = 'Waiting for prerequisite “Review access” to finish before this task can be placed.';
        services.gantt.previewSchedule.mockResolvedValue({ ...preview, tasks: [scheduledTask({ start_date: null, end_date: null })], schedule_result: {
            ...preview.schedule_result, unscheduled: [{ task_id: 11, task_title: 'Prepare release', reason: 'prerequisites_pending', message }],
        } });
        const { user } = renderPlan();
        await user.click(await screen.findByRole('button', { name: 'Calculate schedule' }));
        expect(await screen.findByText(message)).toBeVisible();
        expect(screen.getByRole('link', { name: 'Prepare release' })).toHaveAttribute('href', '/tasks?task=11&fromPlanStep=schedule&project=1&iteration=1');
        expect(screen.queryByText('Every task has dates.')).not.toBeInTheDocument();
    });

    it('says every task has dates after Apply schedule when the saved result lists no unscheduled tasks', async () => {
        const { result } = scheduleWorkspace();
        const saved = { success: result.success, decisions: [], workload_balanced: true, workload_issues: [] };
        let applied = false;
        services.gantt.schedule.mockImplementation(async () => { applied = true; return result; });
        services.gantt.getChart.mockImplementation(async () => ({ iteration: { ...ITERATION, revision: 7 }, tasks: applied ? [scheduledTask()] : [], schedule_result: applied ? saved : null }));
        services.tasks.getByIteration.mockImplementation(async () => [listedTask(applied ? {} : { start_date: null, end_date: null })]);
        const { user } = renderPlan();
        await user.click(await screen.findByRole('button', { name: 'Calculate schedule' }));
        await user.click(await screen.findByRole('button', { name: 'Apply schedule' }));
        expect(await screen.findByText('Schedule applied.')).toBeVisible();
        expect(await screen.findByText('Every task has dates.')).toBeVisible();
        expect(screen.queryByText('Calculate the schedule to see why tasks have no dates.')).not.toBeInTheDocument();
    });

    it('does not claim every task has dates while an active task in the task list is undated', async () => {
        const { result } = scheduleWorkspace();
        const saved = { success: result.success, decisions: [], workload_balanced: true, workload_issues: [], unscheduled: [] };
        services.gantt.getChart.mockResolvedValue({ iteration: ITERATION, tasks: [scheduledTask()], schedule_result: saved, holidays: [], weekends: [] });
        services.tasks.getByIteration.mockResolvedValue([listedTask(), listedTask({ id: 12, title: 'Running work', status: 'active', start_date: null, end_date: null })]);
        renderPlan();
        expect(await screen.findByText('Calculate the schedule to see why tasks have no dates.')).toBeVisible();
        expect(screen.queryByText('Every task has dates.')).not.toBeInTheDocument();
    });

    it('does not claim every task has dates while the task list cannot be read', async () => {
        const { result } = scheduleWorkspace();
        const saved = { success: result.success, decisions: [], workload_balanced: true, workload_issues: [], unscheduled: [] };
        services.gantt.getChart.mockResolvedValue({ iteration: ITERATION, tasks: [scheduledTask()], schedule_result: saved, holidays: [], weekends: [] });
        services.tasks.getByIteration.mockRejectedValue(new Error('Task list unavailable'));
        renderPlan();
        expect(await screen.findByText('Calculate the schedule to see why tasks have no dates.')).toBeVisible();
        expect(screen.queryByText('Every task has dates.')).not.toBeInTheDocument();
    });

    it('does not claim every task has dates while a finished task in the task list is undated', async () => {
        const { result } = scheduleWorkspace();
        const saved = { success: result.success, decisions: [], workload_balanced: true, workload_issues: [], unscheduled: [] };
        services.gantt.getChart.mockResolvedValue({ iteration: ITERATION, tasks: [scheduledTask()], schedule_result: saved, holidays: [], weekends: [] });
        services.tasks.getByIteration.mockResolvedValue([listedTask(), listedTask({ id: 12, title: 'Old work', status: 'resolved', start_date: null, end_date: null })]);
        renderPlan();
        expect(await screen.findByText('Calculate the schedule to see why tasks have no dates.')).toBeVisible();
        expect(screen.queryByText('Every task has dates.')).not.toBeInTheDocument();
    });

    it('says every task has dates when every task is finished and dated', async () => {
        const { result } = scheduleWorkspace();
        const saved = { success: result.success, decisions: [], workload_balanced: true, workload_issues: [], unscheduled: [] };
        services.gantt.getChart.mockResolvedValue({ iteration: ITERATION, tasks: [
            scheduledTask({ status: 'resolved' }), scheduledTask({ id: 12, title: 'Old work', status: 'closed' }),
        ], schedule_result: saved, holidays: [], weekends: [] });
        services.tasks.getByIteration.mockResolvedValue([
            listedTask({ status: 'resolved' }), listedTask({ id: 12, title: 'Old work', status: 'closed' }),
        ]);
        renderPlan();
        expect(await screen.findByText('Every task has dates.')).toBeVisible();
        expect(screen.queryByText('Calculate the schedule to see why tasks have no dates.')).not.toBeInTheDocument();
    });

    it('does not claim every task has dates while a deferred task the Gantt response leaves out is undated', async () => {
        const { result } = scheduleWorkspace();
        const saved = { success: result.success, decisions: [], workload_balanced: true, workload_issues: [], unscheduled: [] };
        // The Gantt response omits deferred tasks; only the task list shows the undated deferred one.
        services.gantt.getChart.mockResolvedValue({ iteration: ITERATION, tasks: [scheduledTask()], schedule_result: saved, holidays: [], weekends: [] });
        services.tasks.getByIteration.mockResolvedValue([
            listedTask(),
            listedTask({ id: 12, title: 'Later work', is_deferred: true, effective_is_deferred: true, start_date: null, end_date: null }),
        ]);
        renderPlan();
        expect(await screen.findByText('Calculate the schedule to see why tasks have no dates.')).toBeVisible();
        expect(screen.queryByText('Every task has dates.')).not.toBeInTheDocument();
    });

    it('lists an undated deferred task with the server reason instead of claiming every task has dates', async () => {
        const { result } = scheduleWorkspace();
        const message = 'Deferred work is left out of scheduling. Undefer it to schedule it.';
        const saved = { ...result, unscheduled: [{ task_id: 12, task_title: 'Later work', reason: 'deferred', message }] };
        services.gantt.getChart.mockResolvedValue({ iteration: ITERATION, tasks: [scheduledTask()], schedule_result: saved, holidays: [], weekends: [] });
        services.tasks.getByIteration.mockResolvedValue([
            listedTask(),
            listedTask({ id: 12, title: 'Later work', is_deferred: true, effective_is_deferred: true, start_date: null, end_date: null }),
        ]);
        renderPlan();
        expect(await screen.findByText(message)).toBeVisible();
        expect(screen.getByRole('link', { name: 'Later work' })).toHaveAttribute('href', '/tasks?task=12&fromPlanStep=schedule&project=1&iteration=1');
        expect(screen.queryByText('Every task has dates.')).not.toBeInTheDocument();
    });

    it('says every task has dates when the task list is all dated, even if an older saved result lists unscheduled tasks', async () => {
        const { result } = scheduleWorkspace();
        const saved = { ...result, unscheduled: [{ task_id: 11, task_title: 'Prepare release', reason: 'prerequisites_pending', message: 'Waiting for a prerequisite.' }] };
        services.gantt.getChart.mockResolvedValue({ iteration: ITERATION, tasks: [scheduledTask()], schedule_result: saved, holidays: [], weekends: [] });
        services.tasks.getByIteration.mockResolvedValue([listedTask()]);
        renderPlan();
        expect(await screen.findByText('Every task has dates.')).toBeVisible();
        expect(screen.queryByText('Waiting for a prerequisite.')).not.toBeInTheDocument();
    });

    describe('judges "Every task has dates" for every kind of task', () => {
        const undated = { start_date: null, end_date: null };
        const subtask = (id: number, overrides: Partial<Task> = {}) => listedTask({ id, title: `Step ${id}`, parent_id: 20, ...overrides });
        const parent = (overrides: Partial<Task> = {}) => listedTask({ id: 20, title: 'Parent work', is_composite: true, ...overrides });
        const cases: Array<[string, Task[], boolean]> = [
            ['a dated task', [listedTask()], true],
            ['an undated task', [listedTask(undated)], false],
            ['a dated parent task whose subtasks are all dated',
                [parent({ children: [subtask(21), subtask(22)] })], true],
            ['a parent task without dates of its own, though all its subtasks are dated',
                [parent({ ...undated, children: [subtask(21), subtask(22)] })], false],
            ['a parent task with an undated subtask, though it has dates of its own',
                [parent({ children: [subtask(21), subtask(22, undated)] })], false],
            ['a dated parent task without subtasks', [parent()], true],
            ['an undated parent task without subtasks beside a dated task', [listedTask(), parent(undated)], false],
            ['a dated finished task', [listedTask({ status: 'closed' })], true],
            ['an undated finished task beside a dated task', [listedTask(), listedTask({ id: 12, status: 'resolved', ...undated })], false],
            ['a dated deferred task beside a dated task',
                [listedTask(), listedTask({ id: 12, is_deferred: true, effective_is_deferred: true } as Partial<Task>)], true],
            ['an undated deferred subtask of a dated parent task',
                [parent({ children: [subtask(21), subtask(22, { ...undated, is_deferred: true, effective_is_deferred: true } as Partial<Task>)] })], false],
        ];
        it.each(cases)('with %s', async (_label, tasks, claimed) => {
            const { result } = scheduleWorkspace();
            const saved = { success: result.success, decisions: [], workload_balanced: true, workload_issues: [], unscheduled: [] };
            services.gantt.getChart.mockResolvedValue({ iteration: ITERATION, tasks: [scheduledTask()], schedule_result: saved, holidays: [], weekends: [] });
            services.tasks.getByIteration.mockResolvedValue(tasks);
            renderPlan();
            if (claimed) {
                expect(await screen.findByText('Every task has dates.')).toBeVisible();
                expect(screen.queryByText('Calculate the schedule to see why tasks have no dates.')).not.toBeInTheDocument();
            } else {
                expect(await screen.findByText('Calculate the schedule to see why tasks have no dates.')).toBeVisible();
                expect(screen.queryByText('Every task has dates.')).not.toBeInTheDocument();
            }
        });

        it('says every task has dates after Apply schedule dates the only task, a parent task without subtasks', async () => {
            const { result } = scheduleWorkspace();
            let applied = false;
            const empty = scheduledTask({ id: 20, title: 'Parent work', is_composite: true });
            services.gantt.previewSchedule.mockResolvedValue({ input_revision: 7, input_planning_revision: 19, tasks: [empty], overdue_task_ids: [], schedule_result: result });
            services.gantt.schedule.mockImplementation(async () => { applied = true; return result; });
            services.gantt.getChart.mockImplementation(async () => ({ iteration: { ...ITERATION, revision: 7 }, tasks: applied ? [empty] : [], schedule_result: applied ? result : null }));
            services.tasks.getByIteration.mockImplementation(async () => [parent(applied ? {} : undated)]);
            const { user } = renderPlan();
            await user.click(await screen.findByRole('button', { name: 'Calculate schedule' }));
            await user.click(await screen.findByRole('button', { name: 'Apply schedule' }));
            expect(await screen.findByText('Schedule applied.')).toBeVisible();
            expect(await screen.findByText('Every task has dates.')).toBeVisible();
        });
    });

    it('does not mark Schedule Done from a successful apply when readiness still says it is incomplete', async () => {
        scheduleWorkspace();
        services.iterations.getPlanningReadiness.mockResolvedValue(scheduleReady);
        const { user } = renderPlan();
        await user.click(await screen.findByRole('button', { name: 'Calculate schedule' }));
        await user.click(await screen.findByRole('button', { name: 'Apply schedule' }));
        expect(await screen.findByText('Schedule applied.')).toBeVisible();
        await waitFor(() => expect(services.iterations.getPlanningReadiness).toHaveBeenCalledTimes(2));
        expect(stateText('schedule')).toBe('Next');
        expect(stateText('review')).toBe('Waiting on checkpoint 5');
        expect(screen.getByText('4 of 6')).toBeVisible();
    });

    it('lists an end after the iteration as a Review risk and shows the server’s 5 of 6 after applying', async () => {
        scheduleWorkspace('2026-08-20');
        const { user } = renderPlan();
        await user.click(await screen.findByRole('button', { name: 'Calculate schedule' }));
        await user.click(await screen.findByRole('button', { name: 'Apply schedule' }));
        await waitFor(() => expect(stateText('schedule')).toBe('Done'));
        expect(screen.getByText('5 of 6')).toBeVisible();
        expect(stateText('review')).toBe('Needs attention');
        expect(toggle('Review')).toHaveAttribute('aria-expanded', 'true');
        expect(within(section('review')).getByRole('link', { name: /End after the iteration.*: 1/ }))
            .toHaveAttribute('href', '/tasks?overflow=true&fromPlanStep=review&project=1&iteration=1');
        expect(await screen.findByRole('button', { name: 'Create share link' })).toBeVisible();
    });

    it('keeps Apply unavailable after a failed preview and allows calculation to be retried', async () => {
        scheduleWorkspace();
        services.gantt.previewSchedule.mockRejectedValueOnce(new Error('Scheduler unavailable'));
        const { user } = renderPlan();
        await user.click(await screen.findByRole('button', { name: 'Calculate schedule' }));
        expect(await screen.findByRole('alert')).toHaveTextContent('The schedule could not be calculated. Try calculating again.');
        expect(screen.queryByRole('button', { name: 'Apply schedule' })).not.toBeInTheDocument();
        await user.click(screen.getByRole('button', { name: 'Calculate schedule' }));
        expect(await screen.findByRole('button', { name: 'Apply schedule' })).toBeEnabled();
    });

    it('discards a conflicting preview and requires calculation again instead of replaying Apply', async () => {
        const { preview } = scheduleWorkspace();
        services.gantt.schedule.mockRejectedValueOnce({ response: { status: 409, data: { detail: { code: 'stale_planning_revision', message: 'Planning inputs changed' } } } });
        const { user } = renderPlan();
        await user.click(await screen.findByRole('button', { name: 'Calculate schedule' }));
        await user.click(await screen.findByRole('button', { name: 'Apply schedule' }));
        expect(await screen.findByRole('alert')).toHaveTextContent('Planning inputs changed');
        await waitFor(() => expect(screen.getByRole('button', { name: 'Calculate schedule' })).toBeEnabled());
        expect(screen.queryByRole('button', { name: 'Apply schedule' })).not.toBeInTheDocument();
        expect(stateText('schedule')).toBe('Next');
        expect(services.gantt.schedule).toHaveBeenCalledTimes(1);
        services.gantt.previewSchedule.mockResolvedValue({ ...preview, input_planning_revision: 20 });
        await user.click(screen.getByRole('button', { name: 'Calculate schedule' }));
        await user.click(await screen.findByRole('button', { name: 'Apply schedule' }));
        expect(services.gantt.schedule).toHaveBeenLastCalledWith(1, 7, 20);
        await waitFor(() => expect(stateText('schedule')).toBe('Done'));
    });

    it('refreshes an outdated revision after a preview conflict so Calculate can be retried', async () => {
        scheduleWorkspace();
        const { user } = renderPlan();
        const calculate = await screen.findByRole('button', { name: 'Calculate schedule' });
        services.gantt.getChart.mockResolvedValue({ iteration: { ...ITERATION, revision: 8 }, tasks: [] });
        services.gantt.previewSchedule.mockRejectedValueOnce({ response: { status: 409, data: { detail: 'Iteration changed. Calculate again.' } } });
        await user.click(calculate);
        expect(await screen.findByRole('alert')).toHaveTextContent('Iteration changed. Calculate again.');
        await waitFor(() => expect(calculate).toBeEnabled());
        await user.click(calculate);
        expect(services.gantt.previewSchedule).toHaveBeenNthCalledWith(1, 1, [], 7);
        expect(services.gantt.previewSchedule).toHaveBeenNthCalledWith(2, 1, [], 8);
        expect(await screen.findByRole('button', { name: 'Apply schedule' })).toBeEnabled();
    });

    it('links over-capacity rows and undated work to their filtered task lists even while Review waits for dates', async () => {
        const { result } = scheduleWorkspace();
        services.gantt.getChart.mockResolvedValue({ iteration: ITERATION, tasks: [scheduledTask({ start_date: null, end_date: null })], schedule_result: result });
        services.team.getWorkload.mockResolvedValue({ team_member_id: 1, name: 'Person 1', allocated_hours: 80, capacity_hours: 64 });
        const { user } = renderPlan();
        await screen.findByRole('list', { name: 'Checkpoints' });
        await user.click(toggle('Review'));
        expect(await screen.findByRole('link', { name: 'Person 1' })).toHaveAttribute('href', '/tasks?assignee=1&fromPlanStep=review&project=1&iteration=1');
        expect(screen.getByRole('link', { name: 'Tasks without dates: 1' })).toHaveAttribute('href', '/tasks?planningIssue=unscheduled&fromPlanStep=review&project=1&iteration=1');
        expect(stateText('review')).toBe('Waiting on checkpoint 5');
        expect(screen.getByText('4 of 6')).toBeVisible();
    });
});

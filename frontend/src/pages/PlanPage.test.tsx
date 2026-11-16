import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { screen, waitFor, within } from '@testing-library/react';
import { Route, Routes, useLocation } from 'react-router-dom';
import { changeAppLanguage } from '../i18n/i18n';
import { LegacyRedirect } from '../navigation/LegacyRedirect';
import { expectPageChrome } from '../test/pageChrome';
import { renderWithProviders } from '../test/renderWithProviders';
import { useScopeStore } from '../features/scope/scopeStore';
import type { TeamMember, TeamMemberCreate, TeamMemberProfile } from '../types/team';
import type { IterationPlanningReadinessSummary, PlanCheckpoint } from '../types/iteration';
import PlanPage from './PlanPage';
import planPageSource from './PlanPage.tsx?raw';

const services = vi.hoisted(() => ({
    iterations: { getAll: vi.fn(), getPlanningReadiness: vi.fn() },
    team: { getByIteration: vi.fn(), getProfiles: vi.fn(), create: vi.fn(), getWorkload: vi.fn(), addVacation: vi.fn() },
    tasks: { getByIteration: vi.fn() },
    gantt: { getChart: vi.fn() },
    triage: { getAll: vi.fn() },
    share: { getCurrent: vi.fn(), create: vi.fn(), revoke: vi.fn() },
}));

vi.mock('../services/iterationService', () => ({ iterationService: services.iterations }));
vi.mock('../services/teamService', () => ({ teamService: services.team }));
vi.mock('../services/taskService', () => ({ taskService: services.tasks }));
vi.mock('../services/ganttService', () => ({ ganttService: services.gantt }));
vi.mock('../services/triageService', () => ({ triageService: services.triage }));
vi.mock('../services/planShareService', () => ({ planShareService: services.share }));
const planning = vi.hoisted(() => ({ readInitial: vi.fn() }));
vi.mock('../services/planningInputService', () => ({ planningInputService: planning }));
vi.mock('./IterationsPage', () => ({ default: () => <p>Iterations of the project</p> }));

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
    services.gantt.getChart.mockResolvedValue({ tasks: [], holidays: [], weekends: [] });
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

    it('keeps the at-risk signals in the Review section with a link to Gantt', async () => {
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
        expect(within(review).getByText('1 planning exception to review')).toBeVisible();
        expect(within(review).getByText('At-risk signals')).toBeVisible();
        expect(await within(review).findByRole('link', { name: 'Open 1 at-risk signal in Gantt' }))
            .toHaveAttribute('href', '/gantt?fromPlanStep=review&project=1&iteration=1');
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
        expect(within(section('iteration')).getByRole('link', { name: /Open iterations/ }))
            .toHaveAttribute('href', '/iterations?fromPlanStep=iteration');
    });

    it('shows the iterations when the scope bar opens Plan on them', () => {
        renderPlan('/plan?panel=iterations&project=1&iteration=1');
        expect(screen.getByText('Iterations of the project')).toBeVisible();
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

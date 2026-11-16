import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { screen, waitFor, within } from '@testing-library/react';
import { Route, Routes, useLocation } from 'react-router-dom';
import { changeAppLanguage } from '../i18n/i18n';
import { LegacyRedirect } from '../navigation/LegacyRedirect';
import { expectPageChrome } from '../test/pageChrome';
import { renderWithProviders } from '../test/renderWithProviders';
import { useScopeStore } from '../features/scope/scopeStore';
import type { IterationPlanningReadinessSummary, PlanCheckpoint } from '../types/iteration';
import PlanPage from './PlanPage';
import planPageSource from './PlanPage.tsx?raw';

const services = vi.hoisted(() => ({
    iterations: { getAll: vi.fn(), getPlanningReadiness: vi.fn() },
    team: { getByIteration: vi.fn(), getProfiles: vi.fn(), create: vi.fn() },
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
    vi.clearAllMocks();
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
        // Iterations are managed in place: no link leaves the page for them.
        expect(within(section('iteration')).queryByRole('link', { name: /Open iterations/ })).not.toBeInTheDocument();
        expect(within(section('iteration')).getByRole('button', { name: 'Edit' })).toBeVisible();
        expect(within(section('iteration')).getByRole('button', { name: 'New iteration' })).toBeVisible();
        expect(within(section('iteration')).getByRole('button', { name: 'All iterations' })).toBeVisible();
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

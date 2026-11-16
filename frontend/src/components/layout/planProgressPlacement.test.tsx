import { beforeEach, describe, expect, it, vi } from 'vitest';
import { screen, within } from '@testing-library/react';
import type { ReactNode } from 'react';
import { renderWithProviders } from '../../test/renderWithProviders';
import OverviewPage from '../../pages/OverviewPage';
import PlanPage from '../../pages/PlanPage';
import PlanMasterPage from '../../pages/PlanMasterPage';
import { deriveStatus, EMPTY_READINESS, nextStep, readiness } from '../../features/planningMasters/masters';
import type { Iteration, IterationSummary } from '../../types/iteration';
import { AppSidebar } from './AppSidebar';

const mocks = vi.hoisted(() => ({
    usePlanningReadiness: vi.fn(),
    usePlanningNavigationSummary: vi.fn(),
    getTriage: vi.fn(),
    getIterationSummary: vi.fn(),
    getProjectSummary: vi.fn(),
}));

vi.mock('../../features/planningMasters/usePlanningReadiness', () => ({
    usePlanningReadiness: mocks.usePlanningReadiness,
}));
vi.mock('../../features/planningMasters/usePlanningNavigationSummary', () => ({
    usePlanningNavigationSummary: mocks.usePlanningNavigationSummary,
}));
vi.mock('../../services/triageService', () => ({ triageService: { getAll: mocks.getTriage } }));
vi.mock('../../services/iterationService', () => ({
    iterationService: { getSummary: mocks.getIterationSummary },
}));
vi.mock('../../services/projectService', () => ({
    projectService: { getSummary: mocks.getProjectSummary },
}));

const iteration: Iteration = {
    id: 1,
    name: 'August plan',
    calendar_id: 1,
    project_id: null,
    project: null,
    start_date: '2026-08-01',
    end_date: '2026-08-14',
    working_days: 10,
};

const iterationSummary: IterationSummary = {
    id: 1,
    name: 'August plan',
    project_id: null,
    project: null,
    start_date: '2026-08-01',
    end_date: '2026-08-14',
    working_days: 10,
    total_tasks: 1,
    completed_tasks: 0,
    total_effort_days: 2,
    team_capacity_days: 0,
    overdue_tasks_count: 0,
};

const queryState = () => ({
    enabled: true,
    hasData: true,
    dataUpdatedAt: Date.parse('2026-08-03T12:00:00Z'),
    isLoading: false,
    isFetching: false,
    isError: false,
    isBlockingError: false,
    isRefetchError: false,
    error: null,
    refetch: vi.fn().mockResolvedValue({ isError: false }),
});

// An iteration with a team and tasks but no schedule yet: below 6 of 6.
const planningState = (overrides: Record<string, unknown> = {}) => {
    const readinessData = {
        ...EMPTY_READINESS,
        iterationCount: 1,
        hasCurrentIteration: true,
        currentIterationName: iteration.name,
        currentIterationStart: iteration.start_date,
        currentIterationEnd: iteration.end_date,
        currentIterationDays: iteration.working_days,
        teamMemberCount: 2,
        teamCapacity: 80,
        taskCount: 3,
        hasGanttSchedule: false,
        inboxCount: 0,
        ...overrides,
    };
    const status = deriveStatus(readinessData);
    return {
        selectedIterationId: iteration.id,
        iterations: [iteration],
        currentIteration: iteration,
        teamMembers: [],
        allTasks: [],
        readinessData,
        status,
        ready: readiness(status),
        nextId: nextStep(status),
        isFetching: false,
        queryStates: {
            iterations: queryState(),
            team: queryState(),
            tasks: queryState(),
            gantt: queryState(),
            inbox: queryState(),
        },
        refetch: vi.fn().mockResolvedValue([]),
    };
};

const useState = (state: ReturnType<typeof planningState>) => {
    mocks.usePlanningReadiness.mockReturnValue(state);
    mocks.usePlanningNavigationSummary.mockReturnValue({
        iterations: state.iterations,
        ready: state.ready,
        isIterationsLoading: false,
        isIterationsError: false,
        isReadinessLoading: false,
        isReadinessError: false,
        isPlanProgressKnown: true,
    });
};

const Shell = ({ children }: { children: ReactNode }) => (
    <>
        <AppSidebar />
        <main>{children}</main>
    </>
);

// Any rendering of the plan's step count: "4/6", "4 of 6 ...".
const PROGRESS_TEXT = /\b\d+\s*(?:\/|of)\s*6\b/;
const progressTexts = () => Array.from(document.body.querySelectorAll('*'))
    .filter(el => Array.from(el.childNodes).some(
        node => node.nodeType === Node.TEXT_NODE && PROGRESS_TEXT.test(node.textContent ?? ''),
    ));

describe('plan progress placement', () => {
    beforeEach(() => {
        vi.clearAllMocks();
        mocks.getTriage.mockResolvedValue([]);
        mocks.getIterationSummary.mockResolvedValue(iterationSummary);
        mocks.getProjectSummary.mockResolvedValue(undefined);
    });

    it('shows plan progress on the Overview page only as the counter on the Plan item', async () => {
        const state = planningState();
        expect(state.ready.done).toBeLessThan(6);
        useState(state);
        renderWithProviders(<Shell><OverviewPage /></Shell>, { initialEntries: ['/'] });

        await screen.findByRole('heading', { level: 1 });
        const nav = screen.getByRole('navigation', { name: 'Primary navigation' });
        expect(within(nav).getByRole('link', { name: 'Plan' }))
            .toHaveTextContent(`${state.ready.done}/6`);
        // The counter and its screen-reader description, both on the Plan item.
        const planItem = within(nav).getByRole('link', { name: 'Plan' });
        expect(progressTexts().filter(el => !planItem.contains(el))).toEqual([]);
    });

    it('shows plan progress on the Plan page as the counter and once as "n of 6", and nowhere else', () => {
        const state = planningState();
        useState(state);
        renderWithProviders(<Shell><PlanPage /></Shell>, { initialEntries: ['/plan'] });

        const nav = screen.getByRole('navigation', { name: 'Primary navigation' });
        expect(within(nav).getByRole('link', { name: 'Plan' }))
            .toHaveTextContent(`${state.ready.done}/6`);
        const outsideNav = progressTexts().filter(el => !el.closest('nav'));
        expect(outsideNav).toHaveLength(1);
        expect(outsideNav[0]).toHaveTextContent(`${state.ready.done} of 6`);
        expect(screen.queryByRole('progressbar')).not.toBeInTheDocument();
    });

    it('shows no counter at 6 of 6, leaving the single "6 of 6" on the Plan page', () => {
        const state = planningState({ hasGanttSchedule: true, riskCount: 0 });
        expect(state.ready.done).toBe(6);
        useState(state);
        renderWithProviders(<Shell><PlanPage /></Shell>, { initialEntries: ['/plan'] });

        const nav = screen.getByRole('navigation', { name: 'Primary navigation' });
        expect(within(nav).getByRole('link', { name: 'Plan' })).toHaveTextContent(/^Plan$/);
        expect(progressTexts()).toHaveLength(1);
        expect(progressTexts()[0]).toHaveTextContent('6 of 6');
    });

    it('shows plan progress on the checkpoint view as the counter and once as "n of 6", with no bar', () => {
        const state = planningState();
        useState(state);
        renderWithProviders(<Shell><PlanMasterPage /></Shell>, { initialEntries: ['/plan/master'] });

        const nav = screen.getByRole('navigation', { name: 'Primary navigation' });
        expect(within(nav).getByRole('link', { name: 'Plan' }))
            .toHaveTextContent(`${state.ready.done}/6`);
        const outsideNav = progressTexts().filter(el => !el.closest('nav'));
        expect(outsideNav).toHaveLength(1);
        expect(outsideNav[0]).toHaveTextContent(`${state.ready.done} of 6`);
        expect(screen.queryByRole('progressbar')).not.toBeInTheDocument();
    });

    it('shows no counter at 6 of 6 on the checkpoint view, leaving the single "6 of 6"', () => {
        const state = planningState({ hasGanttSchedule: true, riskCount: 0 });
        expect(state.ready.done).toBe(6);
        useState(state);
        renderWithProviders(<Shell><PlanMasterPage /></Shell>, { initialEntries: ['/plan/master'] });

        const nav = screen.getByRole('navigation', { name: 'Primary navigation' });
        expect(within(nav).getByRole('link', { name: 'Plan' })).toHaveTextContent(/^Plan$/);
        expect(progressTexts()).toHaveLength(1);
        expect(progressTexts()[0]).toHaveTextContent('6 of 6');
        expect(screen.queryByRole('progressbar')).not.toBeInTheDocument();
    });
});

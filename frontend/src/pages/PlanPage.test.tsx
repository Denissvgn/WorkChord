import { beforeEach, describe, expect, it, vi } from 'vitest';
import { screen, within } from '@testing-library/react';
import {
    deriveStatus,
    EMPTY_READINESS,
    nextStep,
    readiness,
} from '../features/planningMasters/masters';
import { renderWithProviders } from '../test/renderWithProviders';
import PlanPage from './PlanPage';
import planPageSource from './PlanPage.tsx?raw';

const planningReadinessMock = vi.hoisted(() => ({
    usePlanningReadiness: vi.fn(),
}));

vi.mock('../features/planningMasters/usePlanningReadiness', () => planningReadinessMock);

const queryState = (overrides: Record<string, unknown> = {}) => ({
    enabled: true,
    hasData: true,
    isLoading: false,
    isFetching: false,
    isError: false,
    isBlockingError: false,
    isRefetchError: false,
    error: null,
    refetch: vi.fn().mockResolvedValue(undefined),
    ...overrides,
});

const planningState = ({
    readinessOverrides = {},
    queryOverrides = {},
    isFetching = false,
    refetch = vi.fn().mockResolvedValue([]),
}: {
    readinessOverrides?: Record<string, unknown>;
    queryOverrides?: Record<string, Record<string, unknown>>;
    isFetching?: boolean;
    refetch?: ReturnType<typeof vi.fn>;
} = {}) => {
    const readinessData = {
        ...EMPTY_READINESS,
        iterationCount: 1,
        hasCurrentIteration: true,
        currentIterationName: 'August plan',
        currentIterationStart: '2026-08-01',
        currentIterationEnd: '2026-08-14',
        currentIterationDays: 10,
        teamMemberCount: 2,
        teamCapacity: 80,
        taskCount: 3,
        hasGanttSchedule: false,
        inboxCount: 3,
        ...readinessOverrides,
    };
    const status = deriveStatus(readinessData);
    return {
        currentIteration: {
            id: 1,
            name: 'August plan',
            start_date: '2026-08-01',
            end_date: '2026-08-14',
        },
        readinessData,
        status,
        ready: readiness(status),
        nextId: nextStep(status),
        isFetching,
        queryStates: {
            iterations: queryState(queryOverrides.iterations),
            team: queryState(queryOverrides.team),
            tasks: queryState(queryOverrides.tasks),
            gantt: queryState(queryOverrides.gantt),
            inbox: queryState(queryOverrides.inbox),
        },
        refetch,
    };
};

describe('PlanPage mixed planning launcher', () => {
    beforeEach(() => {
        planningReadinessMock.usePlanningReadiness.mockReset();
    });

    it('keeps readiness in one accessible, progressively disclosed launch surface', async () => {
        const state = planningState();
        planningReadinessMock.usePlanningReadiness.mockReturnValue(state);
        const { user } = renderWithProviders(<PlanPage />, { initialEntries: ['/plan'] });

        const progress = screen.getByRole('progressbar', {
            name: `Plan readiness: ${state.ready.pct}%`,
        });
        expect(progress).toHaveAttribute('aria-valuemin', '0');
        expect(progress).toHaveAttribute('aria-valuemax', '100');
        expect(progress).toHaveAttribute('aria-valuenow', String(state.ready.pct));
        expect(screen.getAllByRole('progressbar')).toHaveLength(1);

        const primaryAction = screen.getByRole('link', { name: 'Resume plan' });
        expect(primaryAction).toHaveAttribute('href', '/plan/master');

        await user.click(screen.getByText(`${state.ready.done} of ${state.ready.total} checkpoints complete`));

        const checkpointList = screen.getByRole('list', { name: 'Planning checkpoints' });
        expect(within(checkpointList).getAllByRole('listitem')).toHaveLength(6);
        expect(within(checkpointList).getByText('Build schedule').closest('li'))
            .toHaveAttribute('aria-current', 'step');
    });

    it('names review and sharing as the completed plan action', () => {
        planningReadinessMock.usePlanningReadiness.mockReturnValue(planningState({
            readinessOverrides: {
                hasGanttSchedule: true,
                riskCount: 0,
            },
        }));
        renderWithProviders(<PlanPage />, { initialEntries: ['/plan'] });

        expect(screen.getByText('Plan is ready - share with the team')).toBeVisible();
        expect(screen.getByRole('link', { name: 'Review & share' }))
            .toHaveAttribute('href', '/plan/master');
    });

    it('explains readiness and sharing on demand without adding another primary action', async () => {
        planningReadinessMock.usePlanningReadiness.mockReturnValue(planningState());
        const { user } = renderWithProviders(<PlanPage />, { initialEntries: ['/plan'] });

        await user.click(screen.getByRole('button', { name: 'Planning help' }));

        const guide = screen.getByRole('dialog', { name: 'How Plan Work fits together' });
        expect(within(guide).getByText('Read readiness as a sequence')).toBeVisible();
        expect(within(guide).getByText('Resolve the first blocked checkpoint')).toBeVisible();
        expect(within(guide).getByRole('link', { name: 'Continue Plan Work' }))
            .toHaveAttribute('href', '/plan/master');
        expect(within(guide).queryByRole('link', { name: 'Continue Plan Work' }))
            .not.toHaveClass('primary');
    });

    it('moves inactive and beta planning jobs into direct tools', async () => {
        planningReadinessMock.usePlanningReadiness.mockReturnValue(planningState({
            readinessOverrides: { inboxCount: 0, riskCount: 0 },
        }));
        const { user } = renderWithProviders(<PlanPage />, { initialEntries: ['/plan'] });

        expect(screen.queryByRole('heading', { name: 'Needs attention' })).not.toBeInTheDocument();
        await user.click(screen.getByText('Direct planning tools'));
        const directTools = screen.getByRole('navigation', { name: 'Direct planning tools' });
        expect(within(directTools).getByRole('heading', { name: 'Shape work' })).toBeVisible();
        expect(within(directTools).getByRole('heading', { name: 'Schedule & capacity' })).toBeVisible();
        expect(within(directTools).getByRole('heading', { name: 'Automation' })).toBeVisible();
        expect(within(directTools).getByRole('link', { name: 'Plan a project or release' }))
            .toHaveAttribute('href', '/projects');
        expect(within(directTools).getByRole('link', { name: 'Triage' }))
            .toHaveAttribute('href', '/triage');
        expect(within(directTools).getByRole('link', { name: 'Prepare agent-ready work' }))
            .toHaveAttribute('href', '/agent-pipeline');
    });

    it('promotes only planning jobs with live signals', () => {
        planningReadinessMock.usePlanningReadiness.mockReturnValue(planningState({
            readinessOverrides: { inboxCount: 2, riskCount: 3 },
        }));
        renderWithProviders(<PlanPage />, { initialEntries: ['/plan'] });

        expect(screen.getByRole('heading', { name: 'Needs attention' })).toBeVisible();
        expect(screen.getByRole('link', { name: 'Process intake' }))
            .toHaveAccessibleDescription(/2 in queue/);
        expect(screen.getByRole('link', { name: 'Replan at-risk work' }))
            .toHaveAccessibleDescription(/3 active signals/);
        expect(screen.getByRole('link', { name: 'Plan a project or release' }))
            .not.toBeVisible();
        expect(screen.getByRole('link', { name: 'Prepare agent-ready work' }))
            .not.toBeVisible();
    });

    it('keeps the launcher usable when auxiliary intake status is unavailable', () => {
        planningReadinessMock.usePlanningReadiness.mockReturnValue(planningState({
            queryOverrides: {
                inbox: {
                    hasData: false,
                    isError: true,
                    isBlockingError: true,
                    error: new Error('Intake unavailable'),
                },
            },
        }));
        renderWithProviders(<PlanPage />, { initialEntries: ['/plan'] });

        expect(screen.getByRole('heading', { name: 'Plan an iteration' })).toBeVisible();
        expect(screen.getByText('Intake status unavailable')).toBeVisible();
        expect(screen.getByRole('link', { name: 'Process intake' })).toBeVisible();
    });

    it('uses a blocking recovery state when core planning data has no usable value', () => {
        const retry = vi.fn().mockResolvedValue([]);
        planningReadinessMock.usePlanningReadiness.mockReturnValue(planningState({
            queryOverrides: {
                tasks: {
                    hasData: false,
                    isError: true,
                    isBlockingError: true,
                    error: new Error('Tasks unavailable'),
                },
            },
            refetch: retry,
        }));
        renderWithProviders(<PlanPage />, { initialEntries: ['/plan'] });

        expect(screen.getByText('Planning data is unavailable')).toBeVisible();
        expect(screen.queryByRole('heading', { name: 'Plan an iteration' })).not.toBeInTheDocument();
    });

    it('preserves content and exposes a busy refresh contract during background fetching', () => {
        planningReadinessMock.usePlanningReadiness.mockReturnValue(planningState({
            isFetching: true,
        }));
        renderWithProviders(<PlanPage />, { initialEntries: ['/plan'] });

        expect(screen.getByRole('heading', { name: 'Plan an iteration' })).toBeVisible();
        const refresh = screen.getByRole('button', { name: 'Refreshing...' });
        expect(refresh).toBeDisabled();
        expect(refresh).toHaveAttribute('aria-busy', 'true');
    });

    it('announces the result of an explicit refresh', async () => {
        const refetch = vi.fn().mockResolvedValue([
            { status: 'fulfilled', value: { isError: false } },
        ]);
        planningReadinessMock.usePlanningReadiness.mockReturnValue(planningState({ refetch }));
        const { user } = renderWithProviders(<PlanPage />, { initialEntries: ['/plan'] });

        await user.click(screen.getByRole('button', { name: 'Refresh' }));

        expect(refetch).toHaveBeenCalledTimes(1);
        expect(await screen.findByRole('status')).toHaveTextContent('Planning data updated.');
    });

    it('keeps current content and names the recovery when refresh fails', async () => {
        const refetch = vi.fn().mockResolvedValue([
            { status: 'fulfilled', value: { isError: true } },
        ]);
        planningReadinessMock.usePlanningReadiness.mockReturnValue(planningState({ refetch }));
        const { user } = renderWithProviders(<PlanPage />, { initialEntries: ['/plan'] });

        await user.click(screen.getByRole('button', { name: 'Refresh' }));

        expect(screen.getByRole('heading', { name: 'Plan an iteration' })).toBeVisible();
        expect(await screen.findByRole('alert'))
            .toHaveTextContent('Some planning data could not be refreshed. Try again.');
    });

    it('keeps responsive checkpoint layout in CSS instead of an inline six-column grid', () => {
        expect(planPageSource).not.toContain('repeat(${STEP_DEFS.length}, 1fr)');
        expect(planPageSource).toContain('className="plan-hub-checkpoint-grid"');
    });
});

import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { act, render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { QueryClientProvider } from '@tanstack/react-query';
import { createMemoryRouter, Outlet, Route, RouterProvider, Routes, useLocation } from 'react-router-dom';
import i18n from '../../i18n/i18n';
import { createTestQueryClient, renderWithProviders } from '../../test/renderWithProviders';
import { OnTrackSummary } from '../../components/analytics/OnTrackSummary';
import { IterationList } from '../../components/iteration/IterationList';
import { PlanReturnBar } from '../../components/planning/PlanReturnBar';
import { PlanningWorkflowHelpContent } from '../../components/planning/PlanningWorkflowGuide';
import { TaskWorkflowHelpContent } from '../../components/tasks/TaskWorkflowGuide';
import PlanSharePage from '../../pages/PlanSharePage';
import type { IterationSummary } from '../../types/iteration';
import { useScopeStore } from './scopeStore';
import { useWorkScope } from './useWorkScope';

const iterationServiceMock = vi.hoisted(() => ({ getAll: vi.fn(), getPlanningReadiness: vi.fn(), delete: vi.fn() }));
const planShareServiceMock = vi.hoisted(() => ({ getByPublicId: vi.fn() }));

vi.mock('../../services/iterationService', () => ({ iterationService: iterationServiceMock }));
vi.mock('../../services/planShareService', () => ({ planShareService: planShareServiceMock }));
vi.mock('../../services/taskService', () => ({ taskService: { metricMatches: vi.fn() } }));

const iteration = (id: number, project_id: number, start_date: string, end_date: string) => ({
    id, name: `Iteration ${id}`, calendar_id: 1, project: null, project_id, start_date, end_date, working_days: 10,
});

// Today is 2026-11-16: iteration 12 of project 1 contains it, so it is the default scope.
const ITERATIONS = [
    iteration(12, 1, '2026-11-01', '2026-11-30'),
    iteration(22, 2, '2027-01-01', '2027-01-31'),
];

const LocationProbe = () => {
    const location = useLocation();
    return <output data-testid="location">{`${location.pathname}${location.search}`}</output>;
};

/** Stands in for the app shell: it holds the scope for every page, as AppShell does. */
const Shell = () => {
    const { isReadOnly } = useWorkScope();
    return (
        <>
            <LocationProbe />
            <output data-testid="read-only">{String(isReadOnly)}</output>
            <Outlet />
        </>
    );
};

const locationText = () => screen.getByTestId('location').textContent;
const settle = () => act(() => new Promise(resolve => setTimeout(resolve, 50)));

beforeEach(() => {
    vi.useFakeTimers({ toFake: ['Date'] });
    vi.setSystemTime(new Date('2026-11-16T12:00:00Z'));
    iterationServiceMock.getAll.mockReset();
    iterationServiceMock.getAll.mockResolvedValue(ITERATIONS);
    iterationServiceMock.getPlanningReadiness.mockResolvedValue({
        iteration_id: 12, team_member_count: 0, team_capacity_hours: 0, planned_hours: 0, assigned_hours: 0,
        team_members_no_capacity: 0, task_count: 0, tasks_without_assignee: 0, tasks_without_effort: 0,
        has_schedule: false, risk_count: 0,
    });
    useScopeStore.setState({ project: null, iteration: null });
});

afterEach(() => {
    vi.useRealTimers();
    useScopeStore.setState({ project: null, iteration: null });
});

describe('the planning page is a scoped page', () => {
    const renderPlanning = (entry: string) => {
        const router = createMemoryRouter([{
            element: <Shell />,
            children: [{ path: '/plan/master', element: <p>Planning page</p> }],
        }], { initialEntries: [entry] });
        render(
            <QueryClientProvider client={createTestQueryClient()}>
                <RouterProvider router={router} />
            </QueryClientProvider>,
        );
    };

    it('writes the default scope into the URL on arrival and lets the scope be set there', async () => {
        renderPlanning('/plan/master?step=team');
        await waitFor(() => expect(locationText()).toBe('/plan/master?step=team&project=1&iteration=12'));
        expect(screen.getByTestId('read-only')).toHaveTextContent('false');
    });

    it('shows the scope of a copied link over the scope this browser remembers', async () => {
        useScopeStore.setState({ project: 1, iteration: 12 });
        renderPlanning('/plan/master?step=team&project=2&iteration=22');
        await settle();
        expect(locationText()).toBe('/plan/master?step=team&project=2&iteration=22');
        expect(useScopeStore.getState()).toMatchObject({ project: 2, iteration: 22 });
    });
});

describe('links the app builds to the planning page carry the scope', () => {
    const SCOPE_ENTRY = '/analytics?project=2&iteration=22';

    it('carries it from the return bar back to the checkpoint', () => {
        renderWithProviders(<PlanReturnBar />, { initialEntries: ['/tasks?fromPlanStep=schedule&project=2&iteration=22'] });
        expect(screen.getByRole('link', { name: i18n.t('plan.master.returnToCheckpoint') }))
            .toHaveAttribute('href', '/plan/master?step=schedule&returned=1&project=2&iteration=22');
    });

    it('carries it from the outlook on Analytics to the schedule step', () => {
        const summary = {
            id: 22, name: 'Iteration 22', start_date: '2027-01-01', end_date: '2027-01-31', working_days: 20,
            total_tasks: 4, completed_tasks: 0, total_effort_days: 8, team_capacity_days: 20, overdue_tasks_count: 0,
            metric_contract_version: 2, accepted_tasks: 0, implemented_tasks: 0, unknown_estimate_tasks: 0,
            status_counts: { planned: 4 }, blocked_tasks: 0, remaining_effort_days: 8, scheduled_finish: null,
            remaining_working_days: 20,
        } as IterationSummary;
        renderWithProviders(<OnTrackSummary summary={summary} />, { initialEntries: [SCOPE_ENTRY] });
        expect(screen.getByRole('link', { name: i18n.t('analytics.onTrack.planIt') }))
            .toHaveAttribute('href', '/plan/master?step=schedule&project=2&iteration=22');
    });

    it('carries it from the Tasks and Plan guides', () => {
        renderWithProviders(<>
            <TaskWorkflowHelpContent />
            <PlanningWorkflowHelpContent surface="plan" />
        </>, { initialEntries: [SCOPE_ENTRY] });
        expect(screen.getByRole('link', { name: i18n.t('tasks.guide.openPlanWork') }))
            .toHaveAttribute('href', '/plan/master?project=2&iteration=22');
        expect(screen.getByRole('link', { name: i18n.t('plan.help.action') }))
            .toHaveAttribute('href', '/plan/master?project=2&iteration=22');
    });

    it('carries the remembered scope from a shared plan', async () => {
        useScopeStore.setState({ project: 2, iteration: 22 });
        planShareServiceMock.getByPublicId.mockResolvedValue({
            id: 4, public_id: 'shared-token', iteration_id: 22, iteration_name: 'Iteration 22',
            created_by_display: 'Guest', created_at: '2026-11-02T10:00:00Z', revoked_at: null,
            snapshot_data: {
                iteration: { id: 22, name: 'Iteration 22', start_date: '2027-01-01', end_date: '2027-01-31' },
                team_members: [], tasks: [],
                snapshot_info: { created_at: '2026-11-02T10:00:00Z', reason: 'plan_share' },
            },
        });
        renderWithProviders(
            <Routes><Route path="/plan/share/:publicId" element={<PlanSharePage />} /></Routes>,
            { initialEntries: ['/plan/share/shared-token'] },
        );
        expect(await screen.findByRole('link', { name: i18n.t('plan.master.openPlanMaster') }))
            .toHaveAttribute('href', '/plan/master?project=2&iteration=22');
    });

    it('opens the plan of an iteration in the list with that iteration and its project in scope', async () => {
        useScopeStore.setState({ project: 1, iteration: 12 });
        renderWithProviders(<><IterationList /><LocationProbe /></>, { initialEntries: ['/plan?panel=iterations&project=1&iteration=12'] });

        expect(await screen.findByRole('link', { name: i18n.t('iterations.openPlan') }))
            .toHaveAttribute('href', '/plan/master?project=1&iteration=12');

        await userEvent.click(screen.getByRole('button', { name: i18n.t('iterations.planThisIteration') }));
        expect(locationText()).toBe('/plan/master?project=2&iteration=22');
    });

    it('keeps All projects when the plan of an iteration is opened from the list', async () => {
        useScopeStore.setState({ project: 'all', iteration: 12 });
        renderWithProviders(<><IterationList /><LocationProbe /></>, { initialEntries: ['/plan?panel=iterations&project=all&iteration=12'] });

        await userEvent.click(await screen.findByRole('button', { name: i18n.t('iterations.planThisIteration') }));
        expect(locationText()).toBe('/plan/master?project=all&iteration=22');
    });
});

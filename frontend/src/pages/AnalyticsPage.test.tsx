import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { act, screen, waitFor, within } from '@testing-library/react';
import { renderWithProviders } from '../test/renderWithProviders';
import { useScopeStore } from '../features/scope/scopeStore';
import { ScopeBar } from '../components/layout/ScopeBar';
import AnalyticsPage from './AnalyticsPage';

const metrics = vi.hoisted(() => ({ get: vi.fn() }));
const iterationServiceMock = vi.hoisted(() => ({ getAll: vi.fn(), getSummary: vi.fn() }));
const projectServiceMock = vi.hoisted(() => ({ getAll: vi.fn() }));
const taskServiceMock = vi.hoisted(() => ({ getIterationHistory: vi.fn() }));

vi.mock('../services/deliveryMetricsService', () => ({ deliveryMetricsService: metrics }));
vi.mock('../services/iterationService', () => ({ iterationService: iterationServiceMock }));
vi.mock('../services/projectService', () => ({ projectService: projectServiceMock }));
vi.mock('../services/taskService', () => ({ taskService: taskServiceMock }));
vi.mock('../components/analytics/ExecutionUsagePanel', () => ({ ExecutionUsagePanel: ({ scope }: { scope: { iteration_id: number } }) => <div>Usage scope {scope.iteration_id}</div> }));
vi.mock('../components/analytics/OnTrackSummary', () => ({ OnTrackSummary: ({ summary }: { summary: { id: number } }) => <div>On track scope {summary.id}</div> }));
vi.mock('../components/analytics/StatusDistribution', () => ({ StatusDistribution: ({ summary }: { summary: { id: number } }) => <div>Status scope {summary.id}</div> }));
vi.mock('../components/tasks/WorkMetricsLine', () => ({ WorkMetricsLine: () => null }));
vi.mock('../components/dashboard/SavedViewDashboardCards', () => ({ SavedViewDashboardCards: () => null }));

const iteration = (id: number, project_id: number) => ({
    id, name: `Iteration ${id}`, calendar_id: 1, project_id, start_date: '2026-11-01', end_date: '2026-11-30', working_days: 10,
});
const sample = { unit: 'elapsed_seconds' as const, sample_count: 0, mean: null, median: null, censored_count: 0, unknown_count: 0 };
const report = {
    contract_version: 1, window_start: '2026-10-01T00:00:00Z', window_end: '2026-11-01T00:00:00Z', scope_basis: 'scope_at_observation',
    accepted_leaf_tasks: 0, acceptance_events: 0, rejection_events: 0, canceled_leaf_tasks: 0, reopened_events: 0,
    lead_time: sample, cycle_time: sample, review_delay: sample,
    coverage: { observation_count: 0, current_leaves_without_capture: 0, legacy_closed_acceptance_unknown: 0 },
    review_queue: [], recovery_queue: [], queues_truncated: false,
};
const settle = () => act(() => new Promise(resolve => setTimeout(resolve, 30)));

describe('Analytics page reads the scope bar', () => {
    beforeEach(() => {
        vi.clearAllMocks();
        useScopeStore.setState({ project: null, iteration: null });
        metrics.get.mockResolvedValue(report);
        iterationServiceMock.getAll.mockResolvedValue([iteration(9, 1), iteration(30, 2)]);
        iterationServiceMock.getSummary.mockImplementation(async (id: number) => ({ id, name: `Iteration ${id}`, start_date: '2026-11-01', end_date: '2026-11-30' }));
        projectServiceMock.getAll.mockResolvedValue([{ id: 1, name: 'Orchard', sort_order: 1, initiative: null }, { id: 2, name: 'Grove', sort_order: 2, initiative: null }]);
        taskServiceMock.getIterationHistory.mockResolvedValue([]);
    });
    afterEach(() => { useScopeStore.setState({ project: null, iteration: null }); });

    const renderPage = async (entry: string) => {
        const view = renderWithProviders(<><ScopeBar /><AnalyticsPage /></>, { initialEntries: [entry] });
        await waitFor(() => expect(screen.getByTestId('scope-bar')).not.toHaveTextContent('Loading'));
        await settle();
        return view;
    };

    it('reports the iteration of the scope bar and offers only the window as its own control', async () => {
        await renderPage('/analytics?project=1&iteration=9');
        await waitFor(() => expect(metrics.get).toHaveBeenCalledWith({ iteration_id: 9, lookback_days: 30 }));
        const toolbar = screen.getByTestId('page-toolbar');
        expect(within(toolbar).getAllByRole('combobox')).toHaveLength(1);
        expect(within(toolbar).getByRole('combobox')).toHaveAccessibleName('Window');
    });

    it('updates every section when the scope bar changes', async () => {
        const { user } = await renderPage('/analytics?project=1&iteration=9');
        expect(await screen.findByText('On track scope 9')).toBeVisible();
        expect(screen.getByText('Status scope 9')).toBeVisible();
        expect(screen.getByText('Usage scope 9')).toBeVisible();
        await user.click(screen.getByRole('combobox', { name: 'Project' }));
        await user.click(await screen.findByRole('option', { name: /Grove/ }));
        expect(await screen.findByText('On track scope 30')).toBeVisible();
        expect(screen.getByText('Status scope 30')).toBeVisible();
        expect(screen.getByText('Usage scope 30')).toBeVisible();
        await waitFor(() => expect(metrics.get).toHaveBeenLastCalledWith({ iteration_id: 30, lookback_days: 30 }));
        expect(taskServiceMock.getIterationHistory).toHaveBeenLastCalledWith(30);
        expect(within(screen.getByTestId('page-toolbar')).getAllByRole('combobox')).toHaveLength(1);
    });

    it('requests no delivery or execution-usage data when the scope bar is on Backlog', async () => {
        const { user } = await renderPage('/analytics?project=1&iteration=9');
        await waitFor(() => expect(metrics.get).toHaveBeenCalledWith({ iteration_id: 9, lookback_days: 30 }));
        metrics.get.mockClear();
        await user.click(screen.getByRole('combobox', { name: 'Iteration' }));
        await user.click(await screen.findByRole('option', { name: /^Backlog/ }));
        expect((await screen.findAllByText('Delivery metrics are available for one iteration or one project. Choose an iteration in the scope bar.'))[0]).toBeVisible();
        expect(metrics.get).not.toHaveBeenCalled();
        expect(screen.queryByText('Choose project')).not.toBeInTheDocument();
    });
});

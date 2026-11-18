import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { act, fireEvent, screen, waitFor, within } from '@testing-library/react';
import { renderWithProviders } from '../test/renderWithProviders';
import { useScopeStore } from '../features/scope/scopeStore';
import { ScopeBar } from '../components/layout/ScopeBar';
import AnalyticsPage from './AnalyticsPage';

const metrics = vi.hoisted(() => ({ get: vi.fn() }));
const usage = vi.hoisted(() => ({ get: vi.fn() }));
const iterationServiceMock = vi.hoisted(() => ({ getAll: vi.fn(), getSummary: vi.fn() }));
const projectServiceMock = vi.hoisted(() => ({ getAll: vi.fn() }));

vi.mock('../services/deliveryMetricsService', () => ({ deliveryMetricsService: metrics }));
vi.mock('../services/iterationService', () => ({ iterationService: iterationServiceMock }));
vi.mock('../services/projectService', () => ({ projectService: projectServiceMock }));
vi.mock('../services/executionUsageService', () => ({ executionUsageService: usage }));
vi.mock('../components/analytics/OnTrackSummary', () => ({ OnTrackSummary: ({ summary }: { summary: { id: number } }) => <div>On track scope {summary.id}</div> }));
vi.mock('../components/analytics/StatusDistribution', () => ({ StatusDistribution: ({ summary }: { summary: { id: number } }) => <div>Status scope {summary.id}</div> }));
vi.mock('../components/tasks/WorkMetricsLine', () => ({ WorkMetricsLine: () => null }));

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
        usage.get.mockResolvedValue({ window_start: report.window_start, window_end: report.window_end,
            expected_runs: 2, reported_runs: 1, unreported_runs: 1, partial_reports: 0, unavailable_reports: 0,
            measured_report_count: 1, simulated_reports: 0, provider_reported_cost: { USD: '12.50' }, estimated_cost: {},
            known_cost_reports: { USD: 1 }, unknown_cost_reports: 0, accepted_task_identities: 1,
            reports_linked_to_accepted_tasks: 1, reported_units: {}, unit_report_counts: {},
            reported_human_effort_minutes: null, human_effort_reports: 0, advisory_budget: null });
        iterationServiceMock.getAll.mockResolvedValue([iteration(9, 1), iteration(30, 2)]);
        iterationServiceMock.getSummary.mockImplementation(async (id: number) => ({ id, name: `Iteration ${id}`, start_date: '2026-11-01', end_date: '2026-11-30' }));
        projectServiceMock.getAll.mockResolvedValue([{ id: 1, name: 'Orchard', sort_order: 1, initiative: null }, { id: 2, name: 'Grove', sort_order: 2, initiative: null }]);
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
        expect(screen.queryByRole('heading', { name: 'Saved view dashboard' })).not.toBeInTheDocument();
        expect(screen.queryByRole('heading', { name: 'Task lifecycle' })).not.toBeInTheDocument();
    });

    it('updates every section when the scope bar changes', async () => {
        const { user } = await renderPage('/analytics?project=1&iteration=9');
        expect(await screen.findByText('On track scope 9')).toBeVisible();
        expect(screen.getByText('Status scope 9')).toBeVisible();
        await waitFor(() => expect(usage.get).toHaveBeenLastCalledWith({ iteration_id: 9, lookback_days: 30 }));
        await user.click(screen.getByRole('combobox', { name: 'Project' }));
        await user.click(await screen.findByRole('option', { name: /Grove/ }));
        expect(await screen.findByText('On track scope 30')).toBeVisible();
        expect(screen.getByText('Status scope 30')).toBeVisible();
        await waitFor(() => expect(usage.get).toHaveBeenLastCalledWith({ iteration_id: 30, lookback_days: 30 }));
        await waitFor(() => expect(metrics.get).toHaveBeenLastCalledWith({ iteration_id: 30, lookback_days: 30 }));
        expect(within(screen.getByTestId('page-toolbar')).getAllByRole('combobox')).toHaveLength(1);
    });

    it('requests both reports when the scope bar changes to Backlog and All projects', async () => {
        const { user } = await renderPage('/analytics?project=1&iteration=9');
        await user.click(screen.getByRole('combobox', { name: 'Iteration' }));
        await user.click(await screen.findByRole('option', { name: /^Backlog/ }));
        await waitFor(() => {
            expect(metrics.get).toHaveBeenLastCalledWith({ project_id: 1, backlog: true, lookback_days: 30 });
            expect(usage.get).toHaveBeenLastCalledWith({ project_id: 1, backlog: true, lookback_days: 30 });
        });
        expect(await screen.findByText('12.50')).toBeVisible();
        await user.click(screen.getByRole('combobox', { name: 'Project' }));
        await user.click(await screen.findByRole('option', { name: /All projects/ }));
        await waitFor(() => {
            expect(metrics.get).toHaveBeenLastCalledWith({ all_projects: true, all_projects_backlog: true, lookback_days: 30 });
            expect(usage.get).toHaveBeenLastCalledWith({ all_projects: true, all_projects_backlog: true, lookback_days: 30 });
        });
        expect(screen.queryByText(/Delivery metrics are available for one iteration/)).not.toBeInTheDocument();
        expect(screen.queryByText(/On track scope/)).not.toBeInTheDocument();
    });

    it('counts a task accepted by the chosen local person as one accepted deliverable', async () => {
        metrics.get.mockResolvedValue({ ...report, accepted_leaf_tasks: 1, acceptance_events: 1,
            coverage: { ...report.coverage, observation_count: 3 } });
        await renderPage('/analytics?project=1&iteration=9');
        const accepted = await screen.findByText('Accepted deliverables');
        expect(accepted.closest('div')).toHaveTextContent(/^Accepted deliverables1$/);
        expect(screen.getByText(/0 closed deliverables have unknown acceptance/)).toBeVisible();
    });

    it.each([
        ['/analytics?project=1&iteration=backlog', { project_id: 1, backlog: true }],
        ['/analytics?project=all&iteration=backlog', { all_projects: true, all_projects_backlog: true }],
        ['/analytics?project=all&iteration=9', { all_projects: true, all_projects_backlog: true }],
    ])('renders both report results and changes the window for %s', async (entry, scope) => {
        await renderPage(entry);
        await waitFor(() => {
            expect(metrics.get).toHaveBeenLastCalledWith({ ...scope, lookback_days: 30 });
            expect(usage.get).toHaveBeenLastCalledWith({ ...scope, lookback_days: 30 });
        });
        expect(screen.getByRole('heading', { name: 'Delivery and review' })).toBeVisible();
        expect(screen.getByRole('heading', { name: 'Execution usage' })).toBeVisible();
        expect(await screen.findByText('12.50')).toBeVisible();
        expect(screen.getByText('Reports: 1 of 2 observed attempts. Unreported: 1; partial: 0; unavailable: 0.')).toBeVisible();
        expect(screen.queryByText(/Delivery metrics are available for one iteration/)).not.toBeInTheDocument();
        expect(iterationServiceMock.getSummary).not.toHaveBeenCalled();
        fireEvent.change(screen.getByRole('combobox', { name: 'Window' }), { target: { value: '90' } });
        await waitFor(() => {
            expect(metrics.get).toHaveBeenLastCalledWith({ ...scope, lookback_days: 90 });
            expect(usage.get).toHaveBeenLastCalledWith({ ...scope, lookback_days: 90 });
        });
    });
});

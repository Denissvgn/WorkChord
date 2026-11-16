import { act, screen, waitFor, within } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { createTestQueryClient, renderWithProviders } from '../../test/renderWithProviders';
import { DeliveryAnalytics } from './DeliveryAnalytics';
import { ScopeBar } from '../layout/ScopeBar';
import { changeAppLanguage } from '../../i18n/i18n';
import { useScopeStore } from '../../features/scope/scopeStore';
import type { DeliveryMetrics } from '../../types/deliveryMetrics';

const metrics = vi.hoisted(() => ({ get: vi.fn() }));
const iterationsMock = vi.hoisted(() => ({ getAll: vi.fn() }));
const projects = vi.hoisted(() => ({ getAll: vi.fn() }));
vi.mock('../../services/deliveryMetricsService', () => ({ deliveryMetricsService: metrics }));
vi.mock('../../services/iterationService', () => ({ iterationService: iterationsMock }));
vi.mock('../../services/projectService', () => ({ projectService: projects }));
vi.mock('./ExecutionUsagePanel', () => ({ ExecutionUsagePanel: () => null }));

const iteration = (id: number, project_id: number) => ({
    id, name: `Iteration ${id}`, calendar_id: 1, project_id, start_date: '2026-11-01', end_date: '2026-11-30', working_days: 10,
});

const sample = (mean: number | null) => ({ unit: 'elapsed_seconds' as const, sample_count: mean === null ? 0 : 1,
    mean, median: mean, censored_count: 0, unknown_count: mean === null ? 1 : 0 });
const report: DeliveryMetrics = { contract_version: 1, window_start: '2026-09-01T00:00:00Z', window_end: '2026-10-01T00:00:00Z',
    scope_basis: 'scope_at_observation', accepted_leaf_tasks: 1, acceptance_events: 1, rejection_events: 0,
    canceled_leaf_tasks: 0, reopened_events: 0, lead_time: sample(null), cycle_time: sample(0), review_delay: sample(3),
    coverage: { observation_count: 3, current_leaves_without_capture: 2, legacy_closed_acceptance_unknown: 1 },
    review_queue: [{ task_id: 7, title: 'Ready artifact', reason: 'awaiting_review', age_seconds: null }],
    recovery_queue: [], queues_truncated: false };

const unavailable = 'Delivery metrics are available for one iteration or one project. Choose an iteration in the scope bar.';
const renderReport = (entry: string) => renderWithProviders(<><ScopeBar /><DeliveryAnalytics /></>, { initialEntries: [entry] });
const settle = () => act(() => new Promise(resolve => setTimeout(resolve, 30)));

describe('Delivery evidence', () => {
    beforeEach(() => {
        vi.clearAllMocks();
        useScopeStore.setState({ project: null, iteration: null });
        metrics.get.mockResolvedValue(report);
        iterationsMock.getAll.mockResolvedValue([iteration(9, 1), iteration(10, 1), iteration(30, 2)]);
        projects.getAll.mockResolvedValue([{ id: 1, name: 'Orchard', sort_order: 1, initiative: null }, { id: 2, name: 'Grove', sort_order: 2, initiative: null }]);
    });
    afterEach(() => { useScopeStore.setState({ project: null, iteration: null }); });

    it('separates unknown durations from zero and links actionable review items', async () => {
        renderReport('/analytics?project=1&iteration=9');
        const link = await screen.findByRole('link', { name: 'Ready artifact' });
        expect(link.getAttribute('href')).toMatch(/^\/tasks\?task=7/);
        expect(screen.getAllByText('Unknown').length).toBeGreaterThan(0);
        expect(screen.getAllByText('<0.01').length).toBeGreaterThan(0);
        expect(screen.getByText('3 recorded events. 2 current deliverables have no capture event; 1 closed deliverables have unknown acceptance.')).toBeVisible();
        expect(metrics.get).toHaveBeenCalledWith({ iteration_id: 9, lookback_days: 30 });
    });

    it('has no scope or project controls of its own, only the window', async () => {
        renderReport('/analytics?project=1&iteration=9');
        await screen.findByRole('link', { name: 'Ready artifact' });
        const section = screen.getByRole('region', { name: 'Delivery and review' });
        const selects = within(section).getAllByRole('combobox');
        expect(selects).toHaveLength(1);
        expect(selects[0]).toHaveAccessibleName('Window');
        expect(within(section).queryByText('Choose project')).not.toBeInTheDocument();
    });

    it('follows the scope bar: another iteration, then Backlog, then another project', async () => {
        const { user } = renderReport('/analytics?project=1&iteration=9');
        await screen.findByRole('link', { name: 'Ready artifact' });
        expect(metrics.get).toHaveBeenLastCalledWith({ iteration_id: 9, lookback_days: 30 });

        await user.click(screen.getByRole('combobox', { name: 'Iteration' }));
        await user.click(await screen.findByRole('option', { name: /Iteration 10/ }));
        await waitFor(() => expect(metrics.get).toHaveBeenLastCalledWith({ iteration_id: 10, lookback_days: 30 }));

        await user.click(screen.getByRole('combobox', { name: 'Iteration' }));
        await user.click(await screen.findByRole('option', { name: /^Backlog/ }));
        expect(await screen.findByText(unavailable)).toBeVisible();
        expect(screen.queryByRole('link', { name: 'Ready artifact' })).not.toBeInTheDocument();
        expect(metrics.get).toHaveBeenCalledTimes(2);
        expect(metrics.get).not.toHaveBeenCalledWith(expect.objectContaining({ project_id: expect.anything() }));

        await user.click(screen.getByRole('combobox', { name: 'Project' }));
        await user.click(await screen.findByRole('option', { name: /Grove/ }));
        await waitFor(() => expect(metrics.get).toHaveBeenLastCalledWith({ iteration_id: 30, lookback_days: 30 }));
    });

    it('requests nothing and says so when the scope is the Backlog of a project', async () => {
        renderReport('/analytics?project=2&iteration=backlog');
        expect(await screen.findByText(unavailable)).toBeVisible();
        await settle();
        expect(metrics.get).not.toHaveBeenCalled();
        expect(screen.queryByRole('link', { name: 'Ready artifact' })).not.toBeInTheDocument();
    });

    it('requests nothing and says so when the scope is All projects', async () => {
        renderReport('/analytics?project=all&iteration=backlog');
        expect(await screen.findByText(unavailable)).toBeVisible();
        await settle();
        expect(metrics.get).not.toHaveBeenCalled();
    });

    it('says so in Russian', async () => {
        await changeAppLanguage('ru');
        try {
            renderReport('/analytics?project=2&iteration=backlog');
            expect(await screen.findByText('Показатели доставки доступны для одной итерации или одного проекта. Выберите итерацию в панели области.')).toBeVisible();
            await settle();
            expect(metrics.get).not.toHaveBeenCalled();
        } finally { await changeAppLanguage('en'); }
    });

    it('uses the window with the scope from the bar', async () => {
        const { user } = renderReport('/analytics?project=1&iteration=9');
        await screen.findByRole('link', { name: 'Ready artifact' });
        await user.selectOptions(screen.getByRole('combobox', { name: 'Window' }), '90');
        await waitFor(() => expect(metrics.get).toHaveBeenLastCalledWith({ iteration_id: 9, lookback_days: 90 }));
    });

    it('hides cached private queues after a failed read and offers retry', async () => {
        const queryClient = createTestQueryClient();
        renderWithProviders(<><ScopeBar /><DeliveryAnalytics /></>, { queryClient, initialEntries: ['/analytics?project=1&iteration=9'] });
        await screen.findByRole('link', { name: 'Ready artifact' });
        metrics.get.mockRejectedValueOnce({ response: { status: 403, data: { detail: 'Access was revoked' } } });
        await queryClient.invalidateQueries({ queryKey: ['deliveryMetrics'] });
        await waitFor(() => expect(screen.queryByRole('link', { name: 'Ready artifact' })).not.toBeInTheDocument());
        expect(screen.getByRole('button', { name: /retry/i })).toBeVisible();
    });
});

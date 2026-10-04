import { fireEvent, screen, waitFor } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { createTestQueryClient, renderWithProviders } from '../../test/renderWithProviders';
import { DeliveryAnalytics } from './DeliveryAnalytics';
import type { DeliveryMetrics } from '../../types/deliveryMetrics';

const metrics = vi.hoisted(() => ({ get: vi.fn() }));
const projects = vi.hoisted(() => ({ getAll: vi.fn() }));
vi.mock('../../services/deliveryMetricsService', () => ({ deliveryMetricsService: metrics }));
vi.mock('../../services/projectService', () => ({ projectService: projects }));

const sample = (mean: number | null) => ({ unit: 'elapsed_seconds' as const, sample_count: mean === null ? 0 : 1,
    mean, median: mean, censored_count: 0, unknown_count: mean === null ? 1 : 0 });
const report: DeliveryMetrics = { contract_version: 1, window_start: '2026-09-01T00:00:00Z', window_end: '2026-10-01T00:00:00Z',
    scope_basis: 'scope_at_observation', accepted_leaf_tasks: 1, acceptance_events: 1, rejection_events: 0,
    canceled_leaf_tasks: 0, reopened_events: 0, lead_time: sample(null), cycle_time: sample(0), review_delay: sample(86400),
    coverage: { observation_count: 3, current_leaves_without_capture: 2, legacy_closed_acceptance_unknown: 1 },
    review_queue: [{ task_id: 7, title: 'Ready artifact', reason: 'awaiting_review', age_seconds: null }],
    recovery_queue: [], queues_truncated: false };

describe('Delivery evidence', () => {
    beforeEach(() => { vi.clearAllMocks(); metrics.get.mockResolvedValue(report); projects.getAll.mockResolvedValue([{ id: 1, name: 'Orchard' }]); });

    it('separates unknown durations from zero and links actionable review items', async () => {
        renderWithProviders(<DeliveryAnalytics iterationId={9} />);
        expect(await screen.findByRole('link', { name: 'Ready artifact' })).toHaveAttribute('href', '/tasks?task=7');
        expect(screen.getAllByText('Unknown').length).toBeGreaterThan(0);
        expect(screen.getByText('3 recorded events. 2 current deliverables have no capture event; 1 closed deliverables have unknown acceptance.')).toBeVisible();
        expect(metrics.get).toHaveBeenCalledWith({ iteration_id: 9, lookback_days: 30 });
        expect(projects.getAll).not.toHaveBeenCalled();
    });

    it('supports authorized project history without an agent credential or selected iteration', async () => {
        renderWithProviders(<DeliveryAnalytics />);
        await screen.findByRole('option', { name: 'Orchard' });
        expect(metrics.get).not.toHaveBeenCalled();
        fireEvent.change(screen.getByLabelText('Project', { selector: 'select' }), { target: { value: '1' } });
        await screen.findByRole('link', { name: 'Ready artifact' });
        expect(metrics.get).toHaveBeenCalledWith({ project_id: 1, lookback_days: 30 });
    });

    it('hides cached private queues after a failed read and offers retry', async () => {
        const queryClient = createTestQueryClient();
        renderWithProviders(<DeliveryAnalytics iterationId={9} />, { queryClient });
        await screen.findByRole('link', { name: 'Ready artifact' });
        metrics.get.mockRejectedValueOnce({ response: { status: 403, data: { detail: 'Access was revoked' } } });
        await queryClient.invalidateQueries({ queryKey: ['deliveryMetrics'] });
        await waitFor(() => expect(screen.queryByRole('link', { name: 'Ready artifact' })).not.toBeInTheDocument());
        expect(screen.getByRole('button', { name: /retry/i })).toBeVisible();
    });
});

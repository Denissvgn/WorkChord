import { fireEvent, screen, waitFor } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { renderWithProviders } from '../../test/renderWithProviders';
import { ExecutionUsagePanel } from './ExecutionUsagePanel';
import type { ExecutionUsageSummary } from '../../types/executionUsage';

const service = vi.hoisted(() => ({ get: vi.fn() }));
vi.mock('../../services/executionUsageService', () => ({ executionUsageService: service }));
const report: ExecutionUsageSummary = { window_start: '2026-09-01T00:00:00Z', window_end: '2026-10-01T00:00:00Z', window_basis: 'run_start_or_report_receipt',
    expected_runs: 2, reported_runs: 1, unreported_runs: 1, partial_reports: 1, unavailable_reports: 0, simulated_reports: 1,
    measured_report_count: 1, provider_reported_cost: { EUR: '0', USD: '0.000000000123' }, estimated_cost: { USD: '2.000000000000' },
    known_cost_reports: { EUR: 1, USD: 1 }, unknown_cost_reports: 1, accepted_task_identities: 1, reports_linked_to_accepted_tasks: 1,
    reported_human_effort_minutes: null, human_effort_reports: 0, reported_units: { input_tokens: '10', runtime_seconds: null },
    unit_report_counts: { input_tokens: 1, runtime_seconds: 0 }, simulated_reported_cost: { EUR: '99' }, simulated_estimated_cost: {}, simulated_units: {},
    independently_reconciled: false, advisory_budget: null };

describe('Reported execution usage', () => {
    beforeEach(() => { vi.clearAllMocks(); service.get.mockResolvedValue(report); });

    it('retains tiny decimal costs and keeps simulations, currencies and unknown effort visible', async () => {
        renderWithProviders(<ExecutionUsagePanel scope={{ project_id: 1, lookback_days: 30 }} />);
        expect(await screen.findByText('0.000000000123')).toBeVisible();
        expect(screen.getByText('EUR')).toBeVisible();
        expect(screen.getByText('USD')).toBeVisible();
        expect(screen.getByText(/Explicitly reported human effort: Unknown minutes/)).toBeVisible();
        expect(screen.getByText('1 simulated reports')).toBeVisible();
        expect(screen.getByText('Reports: 1 of 2 observed attempts. Unreported: 1; partial: 1; unavailable: 0.')).toBeVisible();
    });

    it('keeps an advisory budget editable after a failed read and never supplies a default currency', async () => {
        renderWithProviders(<ExecutionUsagePanel scope={{ iteration_id: 9, lookback_days: 30 }} />);
        await screen.findByText('0.000000000123');
        expect(screen.getByLabelText('Currency')).toHaveValue('');
        fireEvent.change(screen.getByLabelText('Advisory budget'), { target: { value: '100,25' } });
        fireEvent.change(screen.getByLabelText('Currency'), { target: { value: 'eur' } });
        service.get.mockRejectedValueOnce({ response: { status: 503, data: { detail: 'Temporarily unavailable' } } });
        fireEvent.click(screen.getByRole('button', { name: 'Compare covered reports' }));
        await waitFor(() => expect(service.get).toHaveBeenLastCalledWith({ iteration_id: 9, lookback_days: 30, budget_amount: '100.25', budget_currency: 'EUR' }));
        await screen.findByText('Temporarily unavailable');
        expect(screen.getByLabelText('Advisory budget')).toHaveValue('100,25');
        expect(screen.getByRole('button', { name: 'Compare covered reports' })).toBeEnabled();
    });
});

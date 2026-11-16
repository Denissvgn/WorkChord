import { describe, expect, it, vi } from 'vitest';
import { screen, within } from '@testing-library/react';
import { taskService } from '../../services/taskService';
import { renderWithProviders } from '../../test/renderWithProviders';
import { OnTrackSummary } from './OnTrackSummary';
import { StatusDistribution } from './StatusDistribution';
import type { IterationSummary } from '../../types/iteration';

vi.mock('../../services/taskService', () => ({ taskService: { metricMatches: vi.fn() } }));

const summary = (overrides: Partial<IterationSummary> = {}): IterationSummary => ({
    id: 7, name: 'Sprint 14', start_date: '2026-11-02', end_date: '2026-11-27', working_days: 20,
    total_tasks: 10, completed_tasks: 4, total_effort_days: 30, team_capacity_days: 40, overdue_tasks_count: 1,
    metric_contract_version: 2, accepted_tasks: 2, implemented_tasks: 4, unknown_estimate_tasks: 3,
    status_counts: { planned: 4, active: 2, resolved: 1, closed: 3 }, blocked_tasks: 2,
    remaining_effort_days: 12, scheduled_finish: '2026-11-20', remaining_working_days: 10, ...overrides,
});

describe('iteration outlook on Analytics', () => {
    it('answers on track from the schedule and the capacity left, and prints unknown estimates', () => {
        renderWithProviders(<OnTrackSummary summary={summary()} />);
        expect(screen.getByText('On track:')).toBeInTheDocument();
        expect(screen.getByText(/12d of work left against 20d of capacity in 10 working days/)).toBeInTheDocument();
        expect(screen.getByRole('button', { name: 'estimate unknown for 3 tasks, not counted' })).toBeInTheDocument();
        expect(screen.getByRole('button', { name: '2 blocked or waiting' })).toBeInTheDocument();
    });

    it('says behind when the schedule ends after the iteration, and at risk when work exceeds capacity', () => {
        const { unmount } = renderWithProviders(<OnTrackSummary summary={summary({ scheduled_finish: '2026-12-02' })} />);
        expect(screen.getByText('Behind:')).toBeInTheDocument();
        unmount();
        const second = renderWithProviders(<OnTrackSummary summary={summary({ remaining_effort_days: 30 })} />);
        expect(screen.getByText('At risk:')).toBeInTheDocument();
        second.unmount();
        renderWithProviders(<OnTrackSummary summary={summary({ scheduled_finish: null })} />);
        expect(screen.getByText('Not scheduled yet:')).toBeInTheDocument();
        expect(screen.getByRole('link', { name: 'Schedule the iteration' })).toBeInTheDocument();
    });

    it('shows schedule exception definitions and lists the matching tasks', async () => {
        vi.mocked(taskService.metricMatches).mockImplementation(async ({ metric }) => ({ metric, has_more: false, items: (metric === 'late_start' ? [1, 2] : [3]).map(id => ({ id, title: "Task " + id, status: 'planned', project_name: 'Orchard', iteration_name: 'Iteration 7' })) }));
        const { user } = renderWithProviders(<OnTrackSummary summary={summary({ late_start_tasks: 2, iteration_overflow_tasks: 1 })} />);
        expect(screen.getByText('Tasks that started after their planned start or have not started by that date.')).toBeVisible();
        expect(screen.getByText('Tasks scheduled to finish after the iteration ends.')).toBeVisible();
        await user.click(screen.getByRole('button', { name: '2 tasks' }));
        let dialog = await screen.findByRole('dialog', { name: 'Late start' });
        expect(await within(dialog).findAllByRole('link')).toHaveLength(2);
        expect(taskService.metricMatches).toHaveBeenCalledWith({ iteration_id: 7, metric: 'late_start' }, expect.anything());
        await user.click(within(dialog).getByRole('button', { name: 'Close' }));
        await user.click(screen.getByRole('button', { name: '1 task' }));
        dialog = await screen.findByRole('dialog', { name: 'Iteration overflow' });
        expect(await within(dialog).findAllByRole('link')).toHaveLength(1);
        expect(taskService.metricMatches).toHaveBeenCalledWith({ iteration_id: 7, metric: 'iteration_overflow' }, expect.anything());
    });

    it('shows schedule exceptions with unknown values when counts are missing on older summaries', () => {
        renderWithProviders(<OnTrackSummary summary={summary({ metric_contract_version: 1, late_start_tasks: undefined, iteration_overflow_tasks: undefined })} />);
        for (const [label, definition] of [
            ['Late start', 'Tasks that started after their planned start or have not started by that date.'],
            ['Iteration overflow', 'Tasks scheduled to finish after the iteration ends.'],
        ]) {
            const row = screen.getByText(label).parentElement!;
            expect(within(row).getByText(`${definition} Unknown`)).toBeVisible();
            expect(within(row).queryByRole('button')).not.toBeInTheDocument();
        }
    });

    it('discloses the total when a schedule exception list is truncated', async () => {
        vi.mocked(taskService.metricMatches).mockResolvedValue({ metric: 'late_start', has_more: true, items: Array.from({ length: 200 }, (_, index) => ({ id: index + 1, title: `Task ${index + 1}`, status: 'planned', project_name: 'Orchard', iteration_name: 'Iteration 7' })) });
        const { user } = renderWithProviders(<OnTrackSummary summary={summary({ late_start_tasks: 201 })} />);
        await user.click(screen.getByRole('button', { name: '201 tasks' }));
        const dialog = await screen.findByRole('dialog', { name: 'Late start' });
        expect(await within(dialog).findByText('Showing the first 200 of 201 tasks.')).toBeVisible();
        expect(within(dialog).getAllByRole('link')).toHaveLength(200);
    });

    it('splits tasks by status with counts and a table view, accepted shown separately', () => {
        renderWithProviders(<StatusDistribution summary={summary()} />);
        expect(screen.getByRole('img', { name: 'Planned 4, Active 2, Resolved 1, Closed 3' })).toBeInTheDocument();
        expect(screen.getByRole('button', { name: '2 accepted' })).toBeInTheDocument();
        expect(screen.getByRole('rowheader', { name: 'Accepted (of closed)' })).toBeInTheDocument();
    });

});

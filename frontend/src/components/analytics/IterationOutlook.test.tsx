import { describe, expect, it, vi } from 'vitest';
import { screen } from '@testing-library/react';
import { renderWithProviders } from '../../test/renderWithProviders';
import { OnTrackSummary } from './OnTrackSummary';
import { StatusDistribution } from './StatusDistribution';
import { TaskStatusFlow } from './TaskStatusFlow';
import type { IterationSummary } from '../../types/iteration';
import type { TaskStatusLog } from '../../types/task';

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

    it('splits tasks by status with counts and a table view, accepted shown separately', () => {
        renderWithProviders(<StatusDistribution summary={summary()} />);
        expect(screen.getByRole('img', { name: 'Planned 4, Active 2, Resolved 1, Closed 3' })).toBeInTheDocument();
        expect(screen.getByRole('button', { name: '2 accepted' })).toBeInTheDocument();
        expect(screen.getByRole('rowheader', { name: 'Accepted (of Closed)' })).toBeInTheDocument();
    });

    it('lists a task lifecycle in order with time in each state and the current state named', () => {
        const logs = [
            { id: 1, task_id: 5, from_status: 'planned', to_status: 'active', changed_at: '2026-11-03T09:00:00Z', triggered_by: 'user', affected_task_ids: [] },
            { id: 2, task_id: 5, from_status: 'active', to_status: 'resolved', changed_at: '2026-11-05T09:00:00Z', triggered_by: 'agent', affected_task_ids: [] },
        ] as TaskStatusLog[];
        renderWithProviders(<TaskStatusFlow taskId={5} title="Import holidays" logs={logs} nowMs={Date.parse('2026-11-06T09:00:00Z')} />);
        expect(screen.getByRole('link', { name: '#5 · Import holidays' })).toHaveAttribute('href', '/tasks?task=5');
        const items = screen.getAllByRole('listitem');
        expect(items).toHaveLength(3);
        expect(items[1]).toHaveTextContent(/Active.*for 2 days.*by a person/);
        expect(items[2]).toHaveTextContent(/Resolved.*Current.*for 1 day so far.*by an agent/);
    });
});

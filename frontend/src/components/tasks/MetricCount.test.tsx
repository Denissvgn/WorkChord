import { describe, expect, it, vi } from 'vitest';
import { screen, within } from '@testing-library/react';
import { renderWithProviders } from '../../test/renderWithProviders';
import { MetricCount } from './MetricCount';
import { WorkMetricsLine } from './WorkMetricsLine';
import type { WorkMetrics } from '../../types/workMetrics';

const service = vi.hoisted(() => ({ metricMatches: vi.fn() }));
vi.mock('../../services/taskService', () => ({ taskService: service }));

describe('counts that open their tasks', () => {
    it('opens a list with exactly the tasks the count names, each linking to the task', async () => {
        service.metricMatches.mockResolvedValue({ metric: 'blocked', has_more: false, items: [
            { id: 4, title: 'Wire the importer', status: 'active', project_name: 'Calendar', iteration_name: 'Sprint 14' },
            { id: 9, title: 'Write the preview', status: 'planned', project_name: 'Calendar', iteration_name: null },
        ] });
        const { user } = renderWithProviders(<MetricCount metric="blocked" scope={{ project_id: 3 }} title="Blocked or waiting tasks">2 blocked or waiting</MetricCount>);
        await user.click(screen.getByRole('button', { name: '2 blocked or waiting' }));
        const dialog = await screen.findByRole('dialog', { name: 'Blocked or waiting tasks' });
        expect(await within(dialog).findByText('2 tasks')).toBeInTheDocument();
        expect(within(dialog).getByRole('link', { name: '#4 · Wire the importer' })).toHaveAttribute('href', '/tasks?task=4');
        expect(within(dialog).getByText(/Planned · Calendar · Backlog/)).toBeInTheDocument();
        expect(service.metricMatches).toHaveBeenCalledWith({ project_id: 3, metric: 'blocked' }, expect.anything());
    });

    it('stays plain text without a scope, and the metrics line links non-zero counts only', () => {
        const metrics = { metric_contract_version: 2, implemented_tasks: 3, accepted_tasks: 0, overdue_tasks: 1, late_start_tasks: 0, iteration_overflow_tasks: 0 } as WorkMetrics;
        renderWithProviders(<WorkMetricsLine metrics={metrics} scope={{ iteration_id: 7 }} />);
        expect(screen.getByRole('button', { name: '3' })).toBeInTheDocument();
        expect(screen.getByRole('button', { name: '1' })).toBeInTheDocument();
        expect(screen.queryByRole('button', { name: '0' })).toBeNull();
        expect(service.metricMatches).not.toHaveBeenCalled();
    });
});

import { describe, expect, it, vi } from 'vitest';
import { screen } from '@testing-library/react';
import { AxiosError } from 'axios';
import { renderWithProviders } from '../../test/renderWithProviders';
import { IterationList } from './IterationList';

const iterations = vi.hoisted(() => ({ getAll: vi.fn(), getPlanningReadiness: vi.fn(), delete: vi.fn() }));
vi.mock('../../services/iterationService', () => ({ iterationService: iterations }));

describe('IterationList', () => {
    it('says the list could not be loaded, with the server detail and a retry', async () => {
        iterations.getAll.mockRejectedValue(new AxiosError('Service Unavailable', '503', undefined, undefined,
            { status: 503, data: { detail: 'Database is unavailable' } } as never));
        renderWithProviders(<IterationList />);
        const alert = await screen.findByRole('alert', {}, { timeout: 3000 });
        expect(alert).toHaveTextContent('The iteration list could not be loaded.');
        expect(alert).toHaveTextContent('Database is unavailable');
        expect(screen.getByRole('button', { name: 'Retry' })).toBeInTheDocument();
    });

    it('uses an upload icon to import and a download icon to export', async () => {
        iterations.getAll.mockResolvedValue([{ id: 1, name: 'Sprint 1', start_date: '2026-11-02', end_date: '2026-11-13', working_days: 10, project: null, project_id: null, calendar_id: 1 }]);
        iterations.getPlanningReadiness.mockResolvedValue({ iteration_id: 1, team_member_count: 0, team_capacity_hours: 0, planned_hours: 0, assigned_hours: 0,
            team_members_no_capacity: 0, task_count: 0, tasks_without_assignee: 0, tasks_without_effort: 0, has_schedule: false, risk_count: 0 });
        renderWithProviders(<IterationList />);
        const importButton = await screen.findByRole('button', { name: 'Import JSON' });
        expect(importButton.querySelector('svg')?.getAttribute('class')).toContain('lucide-upload');
        expect(screen.getByRole('button', { name: 'Export JSON' }).querySelector('svg')?.getAttribute('class')).toContain('lucide-download');
    });
});

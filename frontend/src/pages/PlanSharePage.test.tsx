import { screen } from '@testing-library/react';
import { Route, Routes } from 'react-router-dom';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import { renderWithProviders } from '../test/renderWithProviders';
import PlanSharePage from './PlanSharePage';

const planShareServiceMock = vi.hoisted(() => ({
    getByPublicId: vi.fn(),
}));

vi.mock('../services/planShareService', () => ({
    planShareService: planShareServiceMock,
}));

describe('PlanSharePage', () => {
    beforeEach(() => {
        planShareServiceMock.getByPublicId.mockReset();
        planShareServiceMock.getByPublicId.mockResolvedValue({
            id: 4,
            public_id: 'shared-token',
            iteration_id: 3,
            iteration_name: 'August launch',
            created_by_display: 'Guest ABC123',
            created_at: '2026-08-02T10:00:00Z',
            revoked_at: null,
            snapshot_data: {
                iteration: {
                    id: 3,
                    name: 'August launch',
                    start_date: '2026-08-03',
                    end_date: '2026-08-14',
                },
                team_members: [{
                    name: 'Ada Lovelace',
                    position: 'Engineer',
                    availability_percent: 80,
                }],
                tasks: [{
                    id: 9,
                    title: 'Prepare launch',
                    priority: 2,
                    effort_days: 2,
                    effort_hours: 16,
                    status: 'planned',
                    assignee_name: 'Ada Lovelace',
                    start_date: '2026-08-03',
                    end_date: '2026-08-04',
                    is_optional: false,
                    is_deferred: false,
                    tags: [],
                    dependencies: [],
                    children: [],
                }],
                snapshot_info: {
                    created_at: '2026-08-02T10:00:00Z',
                    reason: 'plan_share',
                },
            },
        });
    });

    it('renders a token-scoped snapshot as read-only plan content', async () => {
        renderWithProviders(
            <Routes>
                <Route path="/plan/share/:publicId" element={<PlanSharePage />} />
            </Routes>,
            {
            initialEntries: ['/plan/share/shared-token'],
            },
        );

        expect(await screen.findByRole('heading', {
            level: 1,
            name: 'August launch',
        })).toBeVisible();
        expect(planShareServiceMock.getByPublicId).toHaveBeenCalledWith('shared-token');
        expect(screen.getByText('Read-only snapshot')).toBeVisible();
        expect(screen.getByText('Prepare launch')).toBeVisible();
        expect(screen.getAllByText('Ada Lovelace')).not.toHaveLength(0);
        expect(screen.queryByRole('textbox')).not.toBeInTheDocument();
    });
});

import { beforeEach, describe, expect, it, vi } from 'vitest';
import { screen, within } from '@testing-library/react';
import { renderWithProviders } from '../../test/renderWithProviders';
import { useIterationStore } from '../../store/iterationStore';
import { AppSidebar } from './AppSidebar';

// These tests use the real planning summary hook; only the network services are replaced.
const services = vi.hoisted(() => ({
    getAll: vi.fn(),
    getPlanningReadiness: vi.fn(),
    getTriage: vi.fn(),
}));

vi.mock('../../services/iterationService', () => ({
    iterationService: { getAll: services.getAll, getPlanningReadiness: services.getPlanningReadiness },
}));
vi.mock('../../services/triageService', () => ({ triageService: { getAll: services.getTriage } }));

const iteration = {
    id: 4,
    name: 'August plan',
    calendar_id: 1,
    project_id: null,
    project: null,
    start_date: '2026-08-01',
    end_date: '2026-08-14',
    working_days: 10,
};

const readinessResponse = {
    team_member_count: 2,
    team_capacity_hours: 80,
    team_members_no_capacity: 0,
    task_count: 3,
    tasks_without_assignee: 0,
    tasks_without_effort: 0,
    tasks_agent_without_capacity: 0,
    team_agent_count: 0,
    has_schedule: false,
    risk_count: 0,
    checkpoints: ['iteration', 'team', 'work', 'blockers', 'schedule', 'review'].map((id, index) => ({
        id,
        state: index < 2 ? 'done' : 'todo',
        reason_codes: [],
        counts: {},
    })),
};

const planLink = () => within(screen.getByRole('navigation', { name: 'Primary navigation' }))
    .getByRole('link', { name: 'Plan' });

describe('Plan counter with the real planning summary', () => {
    beforeEach(() => {
        vi.clearAllMocks();
        useIterationStore.setState({ selectedIterationId: 0 });
        services.getTriage.mockResolvedValue([]);
        services.getAll.mockResolvedValue([iteration]);
        services.getPlanningReadiness.mockResolvedValue(readinessResponse);
    });

    it('shows no counter on direct entry to Settings with empty storage', async () => {
        renderWithProviders(<AppSidebar />, { initialEntries: ['/settings'] });

        await vi.waitFor(() => expect(services.getAll).toHaveBeenCalled());
        await screen.findByRole('link', { name: 'Settings' });
        await new Promise(resolve => setTimeout(resolve, 20));
        expect(services.getPlanningReadiness).not.toHaveBeenCalled();
        expect(planLink()).toHaveTextContent(/^Plan$/);
        expect(screen.queryByText(/\d\/6/)).not.toBeInTheDocument();
    });

    it('shows no counter while the readiness response is loading, then the real count', async () => {
        useIterationStore.setState({ selectedIterationId: iteration.id });
        let resolveReadiness: (value: typeof readinessResponse) => void = () => {};
        services.getPlanningReadiness.mockReturnValue(new Promise(resolve => { resolveReadiness = resolve; }));
        renderWithProviders(<AppSidebar />, { initialEntries: ['/settings'] });

        await vi.waitFor(() => expect(services.getPlanningReadiness).toHaveBeenCalledWith(iteration.id));
        expect(planLink()).toHaveTextContent(/^Plan$/);

        resolveReadiness(readinessResponse);
        await within(planLink()).findByText(/^\d\/6$/);
    });

    it('shows no counter for a partial readiness response, and 6/6 for a complete plan', async () => {
        useIterationStore.setState({ selectedIterationId: iteration.id });
        services.getPlanningReadiness.mockResolvedValue({
            ...readinessResponse,
            checkpoints: readinessResponse.checkpoints.slice(0, 3),
        });
        const { unmount } = renderWithProviders(<AppSidebar />, { initialEntries: ['/settings'] });
        await vi.waitFor(() => expect(services.getPlanningReadiness).toHaveBeenCalled());
        await new Promise(resolve => setTimeout(resolve, 20));
        expect(planLink()).toHaveTextContent(/^Plan$/);
        unmount();

        services.getPlanningReadiness.mockResolvedValue({
            ...readinessResponse,
            checkpoints: readinessResponse.checkpoints.map(item => ({ ...item, state: 'done' })),
        });
        renderWithProviders(<AppSidebar />, { initialEntries: ['/settings'] });
        await within(planLink()).findByText('6/6');
    });

    it('shows no counter when the readiness request fails', async () => {
        useIterationStore.setState({ selectedIterationId: iteration.id });
        services.getPlanningReadiness.mockRejectedValue(new Error('offline'));
        renderWithProviders(<AppSidebar />, { initialEntries: ['/settings'] });

        await vi.waitFor(() => expect(services.getPlanningReadiness).toHaveBeenCalled());
        await new Promise(resolve => setTimeout(resolve, 20));
        expect(planLink()).toHaveTextContent(/^Plan$/);
        expect(screen.queryByText(/\d\/6/)).not.toBeInTheDocument();
    });

    it('shows no counter when the iteration list fails to load', async () => {
        useIterationStore.setState({ selectedIterationId: iteration.id });
        services.getAll.mockRejectedValue(new Error('offline'));
        renderWithProviders(<AppSidebar />, { initialEntries: ['/settings'] });

        await vi.waitFor(() => expect(services.getAll).toHaveBeenCalled());
        await new Promise(resolve => setTimeout(resolve, 20));
        expect(planLink()).toHaveTextContent(/^Plan$/);
    });
});

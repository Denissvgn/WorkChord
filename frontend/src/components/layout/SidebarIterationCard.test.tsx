import { beforeEach, describe, expect, it, vi } from 'vitest';
import { screen, waitFor, within } from '@testing-library/react';
import { renderWithProviders } from '../../test/renderWithProviders';
import { SidebarIterationCard } from './SidebarIterationCard';

const planningReadinessMock = vi.hoisted(() => ({
    usePlanningReadiness: vi.fn(),
}));

vi.mock('../../features/planningMasters/usePlanningReadiness', () => planningReadinessMock);

const planningReadiness = (overrides: Record<string, unknown> = {}) => ({
    iterations: [],
    currentIteration: null,
    selectedIterationId: 0,
    selectIteration: vi.fn(),
    ready: { done: 0, total: 6, pct: 0 },
    isIterationsLoading: false,
    isIterationsError: false,
    isIterationsFetching: false,
    isReadinessLoading: false,
    isReadinessError: false,
    isReadinessFetching: false,
    refetch: vi.fn().mockResolvedValue(undefined),
    ...overrides,
});

describe('SidebarIterationCard', () => {
    beforeEach(() => {
        planningReadinessMock.usePlanningReadiness.mockReset();
    });

    it('does not present setup as an empty state while periods are loading', () => {
        planningReadinessMock.usePlanningReadiness.mockReturnValue(planningReadiness({
            isIterationsLoading: true,
        }));

        renderWithProviders(<SidebarIterationCard />);

        expect(screen.getByRole('status')).toHaveTextContent('Loading planning periods…');
        expect(screen.queryByRole('link', { name: 'Start Plan Work' })).not.toBeInTheDocument();
    });

    it('names the planning-period recovery and retries it', async () => {
        const refetch = vi.fn().mockResolvedValue(undefined);
        planningReadinessMock.usePlanningReadiness.mockReturnValue(planningReadiness({
            isIterationsError: true,
            refetch,
        }));
        const { user } = renderWithProviders(<SidebarIterationCard />);

        expect(screen.getByRole('status')).toHaveTextContent('Planning periods are unavailable.');
        await user.click(screen.getByRole('button', { name: 'Retry planning' }));

        expect(refetch).toHaveBeenCalledTimes(1);
    });

    it('keeps the planning destination available without inventing progress after a readiness failure', async () => {
        const refetch = vi.fn().mockResolvedValue(undefined);
        planningReadinessMock.usePlanningReadiness.mockReturnValue(planningReadiness({
            iterations: [{ id: 1, name: 'Current Sprint' }],
            currentIteration: { id: 1, name: 'Current Sprint' },
            selectedIterationId: 1,
            ready: { done: 6, total: 6, pct: 100 },
            isReadinessError: true,
            refetch,
        }));
        const { user } = renderWithProviders(<SidebarIterationCard />);

        expect(screen.getByRole('status')).toHaveTextContent('Planning progress is unavailable.');
        expect(screen.queryByText('6/6')).not.toBeInTheDocument();
        expect(screen.getByRole('link', { name: /Open Plan Work/ })).toBeInTheDocument();

        await user.click(screen.getByRole('button', { name: 'Retry planning' }));
        expect(refetch).toHaveBeenCalledTimes(1);
    });

    it('restores picker focus after Escape and after selecting a planning period', async () => {
        const selectIteration = vi.fn();
        planningReadinessMock.usePlanningReadiness.mockReturnValue(planningReadiness({
            iterations: [
                { id: 1, name: 'Current Sprint' },
                { id: 2, name: 'Next Sprint' },
            ],
            currentIteration: { id: 1, name: 'Current Sprint' },
            selectedIterationId: 1,
            selectIteration,
            ready: { done: 2, total: 6, pct: 33 },
        }));
        const { user } = renderWithProviders(<SidebarIterationCard />);

        const pickerTrigger = screen.getByRole('button', { name: 'Current Sprint' });
        await user.click(pickerTrigger);
        expect(pickerTrigger).toHaveAttribute('aria-expanded', 'true');
        expect(within(screen.getByRole('group', { name: 'Choose planning period' }))
            .getByRole('button', { name: 'Current Sprint' }))
            .toHaveAttribute('aria-pressed', 'true');

        await user.keyboard('{Escape}');
        expect(pickerTrigger).toHaveAttribute('aria-expanded', 'false');
        await waitFor(() => expect(pickerTrigger).toHaveFocus());

        await user.click(pickerTrigger);
        await user.click(within(screen.getByRole('group', { name: 'Choose planning period' }))
            .getByRole('button', { name: 'Next Sprint' }));

        expect(selectIteration).toHaveBeenCalledWith(2);
        await waitFor(() => expect(pickerTrigger).toHaveFocus());
    });
});

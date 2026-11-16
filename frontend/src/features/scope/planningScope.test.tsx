import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { useState, type ReactNode } from 'react';
import { act, render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { QueryClientProvider } from '@tanstack/react-query';
import { createMemoryRouter, Outlet, RouterProvider, useLocation } from 'react-router-dom';
import { createTestQueryClient } from '../../test/renderWithProviders';
import { usePlanningReadiness } from '../planningMasters/usePlanningReadiness';
import { useScopeStore } from './scopeStore';
import { useWorkScope } from './useWorkScope';

const serviceMocks = vi.hoisted(() => ({
    getIterations: vi.fn(),
    getTeam: vi.fn(),
    getTasks: vi.fn(),
    getGantt: vi.fn(),
    getInbox: vi.fn(),
}));

vi.mock('../../services/iterationService', () => ({ iterationService: { getAll: serviceMocks.getIterations } }));
vi.mock('../../services/teamService', () => ({ teamService: { getByIteration: serviceMocks.getTeam } }));
vi.mock('../../services/taskService', () => ({ taskService: { getByIteration: serviceMocks.getTasks } }));
vi.mock('../../services/ganttService', () => ({ ganttService: { getChart: serviceMocks.getGantt } }));
vi.mock('../../services/triageService', () => ({ triageService: { getAll: serviceMocks.getInbox } }));

const iteration = (id: number, project_id: number, start_date: string, end_date: string) => ({
    id, name: `Iteration ${id}`, calendar_id: 1, project_id, start_date, end_date, working_days: 10,
});

// Today is 2026-11-16. Project 1 opens on iteration 12, which contains today; project 2 has
// no iteration that contains today, so it opens on the next one, iteration 22.
const ITERATIONS = [
    iteration(11, 1, '2026-10-01', '2026-10-31'),
    iteration(12, 1, '2026-11-01', '2026-11-30'),
    iteration(21, 2, '2026-09-01', '2026-09-30'),
    iteration(22, 2, '2027-01-01', '2027-01-31'),
];

/** Stands in for the app shell: it holds the scope for every page, as AppShell does. */
const Shell = () => {
    const { isReady } = useWorkScope();
    const location = useLocation();
    return (
        <>
            <output data-testid="location">{`${location.pathname}${location.search}`}</output>
            <output data-testid="ready">{String(isReady)}</output>
            <Outlet />
        </>
    );
};

/** A planning page: it reads the iteration through the planning hook. */
const PlanningPage = () => {
    const { selectedIterationId } = usePlanningReadiness();
    return <output data-testid="planning-iteration">{selectedIterationId}</output>;
};

const Deferred = ({ children }: { children: ReactNode }) => {
    const [open, setOpen] = useState(false);
    return open ? children : <button type="button" onClick={() => setOpen(true)}>Open page</button>;
};

const renderPlan = (entry: string, deferred: boolean) => {
    const page = deferred ? <Deferred><PlanningPage /></Deferred> : <PlanningPage />;
    const router = createMemoryRouter([{
        element: <Shell />,
        children: [{ path: '/plan', element: page }],
    }], { initialEntries: [entry] });
    render(
        <QueryClientProvider client={createTestQueryClient()}>
            <RouterProvider router={router} />
        </QueryClientProvider>,
    );
};

const locationText = () => screen.getByTestId('location').textContent;
const settle = () => act(() => new Promise(resolve => setTimeout(resolve, 50)));

describe('an iteration in scope that no longer exists', () => {
    beforeEach(() => {
        vi.useFakeTimers({ toFake: ['Date'] });
        vi.setSystemTime(new Date('2026-11-16T12:00:00Z'));
        Object.values(serviceMocks).forEach(mock => mock.mockReset());
        serviceMocks.getIterations.mockResolvedValue(ITERATIONS);
        serviceMocks.getTeam.mockResolvedValue([]);
        serviceMocks.getTasks.mockResolvedValue([]);
        serviceMocks.getGantt.mockResolvedValue({ tasks: [], schedule_result: null });
        serviceMocks.getInbox.mockResolvedValue([]);
        useScopeStore.setState({ project: null, iteration: null });
    });

    afterEach(() => {
        vi.useRealTimers();
    });

    for (const deferred of [false, true]) {
        const when = deferred ? 'after the shell has set the scope' : 'with the shell';

        it(`keeps the chosen project and opens on its default iteration when the planning page opens ${when}`, async () => {
            useScopeStore.getState().remember({ project: 1, iteration: 12 });

            renderPlan('/plan?project=2&iteration=999', deferred);
            await waitFor(() => expect(screen.getByTestId('ready')).toHaveTextContent('true'));
            if (deferred) await userEvent.click(screen.getByRole('button', { name: 'Open page' }));
            await settle();

            await waitFor(() => expect(screen.getByTestId('planning-iteration')).toHaveTextContent('22'));
            await settle();
            expect(locationText()).toBe('/plan?project=2&iteration=22');
            expect(useScopeStore.getState()).toMatchObject({ project: 2, iteration: 22 });
        });
    }

    it('keeps the chosen project when the remembered iteration is gone and the URL has no scope', async () => {
        useScopeStore.getState().remember({ project: 2, iteration: 999 });

        renderPlan('/plan', false);
        await waitFor(() => expect(screen.getByTestId('planning-iteration')).toHaveTextContent('22'));
        await settle();

        expect(locationText()).toBe('/plan?project=2&iteration=22');
        expect(useScopeStore.getState()).toMatchObject({ project: 2, iteration: 22 });
    });
});

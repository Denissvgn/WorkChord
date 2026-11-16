import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { useEffect } from 'react';
import { act, render, screen, waitFor } from '@testing-library/react';
import { QueryClientProvider } from '@tanstack/react-query';
import { createMemoryRouter, RouterProvider, useLocation } from 'react-router-dom';
import { createTestQueryClient } from '../../test/renderWithProviders';
import { useIterationStore } from '../../store/iterationStore';
import { useScopeStore } from './scopeStore';
import { useWorkScope, type WorkScopeValue } from './useWorkScope';

const iterationServiceMock = vi.hoisted(() => ({ getAll: vi.fn() }));
vi.mock('../../services/iterationService', () => ({ iterationService: iterationServiceMock }));

const iteration = (id: number, project_id: number | null, start_date: string, end_date: string) => ({
    id, name: `Iteration ${id}`, calendar_id: 1, project_id, start_date, end_date, working_days: 10,
});

const ITERATIONS = [
    iteration(11, 1, '2026-10-01', '2026-10-31'),
    iteration(12, 1, '2026-11-01', '2026-11-30'),
    iteration(13, 1, '2026-12-01', '2026-12-31'),
    iteration(21, 2, '2026-09-01', '2026-09-30'),
    iteration(22, 2, '2027-01-01', '2027-01-31'),
    iteration(31, 3, '2026-06-01', '2026-06-30'),
];

let latest: WorkScopeValue | undefined;

const Probe = () => {
    const value = useWorkScope();
    const location = useLocation();
    useEffect(() => {
        latest = value;
    });
    return (
        <>
            <output data-testid="scope">{`${value.project ?? '-'}/${value.iteration ?? '-'}`}</output>
            <output data-testid="location">{`${location.pathname}${location.search}`}</output>
            <output data-testid="ready">{String(value.isReady)}</output>
        </>
    );
};

const renderAt = (...entries: string[]) => {
    const router = createMemoryRouter([{ path: '*', element: <Probe /> }], {
        initialEntries: entries,
        initialIndex: entries.length - 1,
    });
    render(
        <QueryClientProvider client={createTestQueryClient()}>
            <RouterProvider router={router} />
        </QueryClientProvider>,
    );
    return router;
};

const scopeText = () => screen.getByTestId('scope').textContent;
const locationText = () => screen.getByTestId('location').textContent;
const waitForReady = () => waitFor(() => expect(screen.getByTestId('ready')).toHaveTextContent('true'));

describe('useWorkScope', () => {
    beforeEach(() => {
        vi.useFakeTimers({ toFake: ['Date'] });
        vi.setSystemTime(new Date('2026-11-16T12:00:00Z'));
        iterationServiceMock.getAll.mockReset();
        iterationServiceMock.getAll.mockResolvedValue(ITERATIONS);
        useScopeStore.setState({ project: null, iteration: null });
        latest = undefined;
    });

    afterEach(() => {
        vi.useRealTimers();
    });

    it('shows the scope in the URL over the remembered scope', async () => {
        useScopeStore.getState().remember({ project: 2, iteration: 21 });

        renderAt('/tasks?project=1&iteration=13');

        expect(scopeText()).toBe('1/13');
        await waitForReady();
        expect(scopeText()).toBe('1/13');
        expect(locationText()).toBe('/tasks?project=1&iteration=13');
        expect(useScopeStore.getState()).toMatchObject({ project: 1, iteration: 13 });
    });

    it('accepts All projects and Backlog from the URL', async () => {
        useScopeStore.getState().remember({ project: 2, iteration: 21 });

        renderAt('/gantt?project=all&iteration=backlog');

        await waitForReady();
        expect(scopeText()).toBe('all/backlog');
        expect(locationText()).toBe('/gantt?project=all&iteration=backlog');
    });

    it('falls back to the remembered scope and writes it to the URL of a scoped page', async () => {
        useScopeStore.getState().remember({ project: 2, iteration: 21 });

        renderAt('/analytics?tab=flow');

        await waitFor(() => expect(locationText()).toBe('/analytics?tab=flow&project=2&iteration=21'));
        expect(scopeText()).toBe('2/21');
    });

    it('picks the iteration that contains today with no parameters and nothing remembered', async () => {
        renderAt('/tasks');

        await waitFor(() => expect(locationText()).toBe('/tasks?project=1&iteration=12'));
        expect(scopeText()).toBe('1/12');
        expect(useScopeStore.getState()).toMatchObject({ project: 1, iteration: 12 });
    });

    it('does not add scope parameters to a workspace-wide page', async () => {
        renderAt('/my-work');

        await waitForReady();
        expect(scopeText()).toBe('1/12');
        expect(latest?.isReadOnly).toBe(true);
        expect(locationText()).toBe('/my-work');
    });

    it('resets the iteration when the project changes and Back returns to the page before', async () => {
        const router = renderAt('/my-work');
        await waitForReady();

        await act(() => router.navigate('/tasks?project=1&iteration=13'));
        await waitFor(() => expect(scopeText()).toBe('1/13'));

        act(() => latest!.setProject(2));
        await waitFor(() => expect(locationText()).toBe('/tasks?project=2&iteration=22'));
        expect(scopeText()).toBe('2/22');

        act(() => latest!.setProject(3));
        await waitFor(() => expect(locationText()).toBe('/tasks?project=3&iteration=31'));

        act(() => latest!.setIteration('backlog'));
        await waitFor(() => expect(locationText()).toBe('/tasks?project=3&iteration=backlog'));

        act(() => latest!.setProject('all'));
        await waitFor(() => expect(locationText()).toBe('/tasks?project=all&iteration=12'));
        expect(useScopeStore.getState()).toMatchObject({ project: 'all', iteration: 12 });

        await act(() => router.navigate(-1));
        await waitFor(() => expect(locationText()).toBe('/my-work'));
    });

    it('treats a scoped page opened with a trailing slash as a scoped page', async () => {
        const router = renderAt('/my-work', '/tasks/');
        await waitForReady();

        expect(latest?.isReadOnly).toBe(false);
        expect(locationText()).toBe('/tasks/?project=1&iteration=12');

        act(() => latest!.setProject(2));
        await waitFor(() => expect(locationText()).toBe('/tasks/?project=2&iteration=22'));
        expect(latest!.linkTo('/gantt/')).toBe('/gantt/?project=2&iteration=22');

        await act(() => router.navigate(-1));
        await waitFor(() => expect(locationText()).toBe('/my-work'));
    });

    it('lets the project follow an iteration chosen in another project', async () => {
        renderAt('/plan?project=1&iteration=12');
        await waitForReady();

        act(() => latest!.setIteration(21));

        await waitFor(() => expect(locationText()).toBe('/plan?project=2&iteration=21'));
    });

    it('writes an iteration set through the old iteration store to the URL', async () => {
        const router = renderAt('/my-work', '/tasks?project=1&iteration=12');
        await waitForReady();

        act(() => useIterationStore.getState().setSelectedIterationId(21));

        await waitFor(() => expect(locationText()).toBe('/tasks?project=2&iteration=21'));
        expect(scopeText()).toBe('2/21');

        await act(() => router.navigate(-1));
        await waitFor(() => expect(locationText()).toBe('/my-work'));
    });

    it('builds scoped links with the current scope', async () => {
        renderAt('/triage?project=2&iteration=22');
        await waitForReady();

        expect(latest!.linkTo('/gantt')).toBe('/gantt?project=2&iteration=22');
        expect(latest!.linkTo('/settings')).toBe('/settings');
    });
});

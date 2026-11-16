import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { useState, type ReactNode } from 'react';
import { act, render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { QueryClientProvider } from '@tanstack/react-query';
import { createMemoryRouter, Outlet, RouterProvider, useLocation } from 'react-router-dom';
import { ToastProvider } from '../../components/feedback/ToastProvider';
import { createTestQueryClient } from '../../test/renderWithProviders';
import i18n from '../../i18n/i18n';
import GanttPage from '../../pages/GanttPage';
import TasksPage from '../../pages/TasksPage';
import { useScopeStore } from './scopeStore';
import { useWorkScope } from './useWorkScope';

const iterationServiceMock = vi.hoisted(() => ({ getAll: vi.fn() }));
const ganttServiceMock = vi.hoisted(() => ({ getChart: vi.fn(), previewSchedule: vi.fn(), explainSchedule: vi.fn() }));
const taskServiceMock = vi.hoisted(() => ({ batchUpdate: vi.fn(), getDetail: vi.fn(), getById: vi.fn() }));
const savedViewServiceMock = vi.hoisted(() => ({ getAll: vi.fn() }));

vi.mock('../../services/iterationService', () => ({ iterationService: iterationServiceMock }));
vi.mock('../../services/ganttService', () => ({ ganttService: ganttServiceMock }));
vi.mock('../../services/taskService', () => ({ taskService: taskServiceMock }));
vi.mock('../../services/savedViewService', () => ({ savedViewService: savedViewServiceMock }));
vi.mock('../../components/gantt/GanttChart', () => ({ GanttChart: () => <p>Gantt chart</p> }));
vi.mock('../../components/tasks/TaskList', () => ({ TaskList: () => <p>Iteration task list</p> }));
vi.mock('../../components/tasks/KanbanBoard/KanbanBoard', () => ({ KanbanBoard: () => <p>Board</p> }));
vi.mock('../../components/tasks/TaskFiltersBar', () => ({ TaskFiltersBar: () => <p>Filters</p> }));
vi.mock('../../components/tasks/SavedViewsControl', () => ({ SavedViewsControl: () => <p>Saved views</p> }));
vi.mock('../../components/tasks/BacklogPanel', () => ({ BacklogPanel: () => <p>Backlog task list</p> }));
vi.mock('../../components/tasks/TaskSearch', () => ({ TaskSearch: () => null }));
vi.mock('../../components/tasks/TaskEditorDrawer', () => ({ TaskEditorDrawer: () => null }));

const iteration = (id: number, project_id: number, start_date: string, end_date: string) => ({
    id, name: `Iteration ${id}`, calendar_id: 1, project_id, start_date, end_date, working_days: 10,
});

// Today is 2026-11-16: iteration 12 of project 1 contains it, so it is the default scope.
const ITERATIONS = [
    iteration(11, 1, '2026-10-01', '2026-10-31'),
    iteration(12, 1, '2026-11-01', '2026-11-30'),
    iteration(21, 2, '2026-09-01', '2026-09-30'),
    iteration(22, 2, '2027-01-01', '2027-01-31'),
];

const ganttChart = (id: number) => ({
    iteration: ITERATIONS.find(item => item.id === id),
    tasks: [], overdue_task_ids: [], holidays: [], weekends: [], member_vacations: {}, schedule_result: null,
});

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

/** Mounts the page only when asked, so it can open after the shell has settled the scope. */
const Deferred = ({ children }: { children: ReactNode }) => {
    const [open, setOpen] = useState(false);
    return open ? children : <button type="button" onClick={() => setOpen(true)}>Open page</button>;
};

const PAGES = {
    tasks: <TasksPage />,
    gantt: <GanttPage />,
} as const;

const renderApp = (entry: string, deferred: boolean) => {
    const page = (element: ReactNode) => (deferred ? <Deferred>{element}</Deferred> : element);
    const router = createMemoryRouter([{
        element: <Shell />,
        children: [
            { path: '/tasks', element: page(PAGES.tasks) },
            { path: '/gantt', element: page(PAGES.gantt) },
            { path: '*', element: <p>Workspace page</p> },
        ],
    }], { initialEntries: [entry] });
    render(
        <QueryClientProvider client={createTestQueryClient()}>
            <ToastProvider>
                <RouterProvider router={router} />
            </ToastProvider>
        </QueryClientProvider>,
    );
    return router;
};

const locationText = () => screen.getByTestId('location').textContent;
const waitForReady = () => waitFor(() => expect(screen.getByTestId('ready')).toHaveTextContent('true'));
/** Lets every pending effect, query and navigation run. */
const settle = () => act(() => new Promise(resolve => setTimeout(resolve, 50)));

const iterationSelect = () => screen.getByRole('combobox', { name: i18n.t('iterationIndicator.selectIteration') });

const expectPageShowsScope = async (path: 'tasks' | 'gantt', iterationParam: string) => {
    if (iterationParam === 'backlog' && path === 'tasks') {
        expect(await screen.findByText('Backlog task list')).toBeInTheDocument();
        expect(screen.queryByText('Iteration task list')).not.toBeInTheDocument();
        return;
    }
    await waitFor(() => expect(iterationSelect()).toHaveValue(iterationParam === 'backlog' ? '0' : iterationParam));
    if (iterationParam === 'backlog') {
        expect(iterationSelect()).toHaveDisplayValue(i18n.t('teamwork.backlog'));
        expect(ganttServiceMock.getChart).not.toHaveBeenCalled();
    } else {
        expect(await screen.findByText(path === 'gantt' ? 'Gantt chart' : 'Iteration task list')).toBeInTheDocument();
    }
};

const SCOPED_URLS = [
    { label: 'Backlog of project 2', search: '?project=2&iteration=backlog', project: 2, iteration: 'backlog' },
    { label: 'iteration 21 of project 2', search: '?project=2&iteration=21', project: 2, iteration: 21 },
] as const;

describe('a scope in the URL survives opening a page that still has its own iteration control', () => {
    beforeEach(() => {
        vi.useFakeTimers({ toFake: ['Date'] });
        vi.setSystemTime(new Date('2026-11-16T12:00:00Z'));
        iterationServiceMock.getAll.mockReset();
        iterationServiceMock.getAll.mockResolvedValue(ITERATIONS);
        ganttServiceMock.getChart.mockReset();
        ganttServiceMock.getChart.mockImplementation(async (id: number) => ganttChart(id));
        savedViewServiceMock.getAll.mockResolvedValue([]);
        useScopeStore.setState({ project: null, iteration: null });
    });

    afterEach(() => {
        vi.useRealTimers();
    });

    for (const path of ['tasks', 'gantt'] as const) {
        for (const url of SCOPED_URLS) {
            const entry = `/${path}${url.search}`;

            it(`keeps ${url.label} when ${path} opens with the shell`, async () => {
                useScopeStore.getState().remember({ project: 1, iteration: 12 });

                renderApp(entry, false);
                await waitForReady();
                await settle();

                expect(locationText()).toBe(entry);
                expect(useScopeStore.getState()).toMatchObject({ project: url.project, iteration: url.iteration });
                await expectPageShowsScope(path, String(url.iteration));
                expect(locationText()).toBe(entry);
            });

            it(`keeps ${url.label} when ${path} mounts after the shell has set the scope`, async () => {
                renderApp(entry, true);
                await waitForReady();
                await settle();
                expect(useScopeStore.getState()).toMatchObject({ project: url.project, iteration: url.iteration });

                await userEvent.click(screen.getByRole('button', { name: 'Open page' }));
                await settle();

                expect(locationText()).toBe(entry);
                expect(useScopeStore.getState()).toMatchObject({ project: url.project, iteration: url.iteration });
                await expectPageShowsScope(path, String(url.iteration));
                expect(locationText()).toBe(entry);
            });

            it(`keeps ${url.label} when ${path} is opened from another page`, async () => {
                const router = renderApp('/my-work', false);
                await waitForReady();
                await settle();
                expect(useScopeStore.getState()).toMatchObject({ project: 1, iteration: 12 });

                await act(() => router.navigate(entry));
                await settle();

                expect(locationText()).toBe(entry);
                expect(useScopeStore.getState()).toMatchObject({ project: url.project, iteration: url.iteration });
                await expectPageShowsScope(path, String(url.iteration));
            });
        }
    }

    for (const deferred of [false, true]) {
        const when = deferred ? 'after the shell has set the scope' : 'with the shell';

        it(`moves the scope to the iteration of a task opened from a link ${when}`, async () => {
            taskServiceMock.getById.mockResolvedValue({ id: 42, iteration_id: 21, title: 'Linked task' });

            renderApp('/tasks?task=42&project=1&iteration=12', deferred);
            await waitForReady();
            if (deferred) await userEvent.click(screen.getByRole('button', { name: 'Open page' }));

            await waitFor(() => expect(locationText()).toBe('/tasks?task=42&project=2&iteration=21'));
            await settle();
            expect(locationText()).toBe('/tasks?task=42&project=2&iteration=21');
            expect(useScopeStore.getState()).toMatchObject({ project: 2, iteration: 21 });
        });

        it(`moves the scope to the iteration a planning link names ${when}`, async () => {
            renderApp('/tasks?iterationId=11&project=1&iteration=12', deferred);
            await waitForReady();
            if (deferred) await userEvent.click(screen.getByRole('button', { name: 'Open page' }));

            await waitFor(() => expect(locationText()).toBe('/tasks?iterationId=11&project=1&iteration=11'));
            await settle();
            expect(locationText()).toBe('/tasks?iterationId=11&project=1&iteration=11');
            expect(useScopeStore.getState()).toMatchObject({ project: 1, iteration: 11 });
        });
    }

    it('opens the Tasks backlog from an older ?scope=backlog link and keeps it in the scope', async () => {
        useScopeStore.getState().remember({ project: 2, iteration: 21 });

        renderApp('/tasks?scope=backlog', false);
        await waitForReady();
        await settle();

        expect(await screen.findByText('Backlog task list')).toBeInTheDocument();
        expect(locationText()).toBe('/tasks?iteration=backlog&project=2');
        expect(useScopeStore.getState()).toMatchObject({ project: 2, iteration: 'backlog' });
    });

    it('leaves the Tasks backlog for the default iteration of the project', async () => {
        renderApp('/tasks?project=2&iteration=backlog', false);
        await waitForReady();

        const link = await screen.findByRole('link', { name: i18n.t('teamwork.iterationTasks') });
        expect(link).toHaveAttribute('href', '/tasks?project=2&iteration=22');
    });

    it('changes the iteration on Gantt without adding a history entry', async () => {
        const router = renderApp('/my-work', false);
        await waitForReady();
        await settle();
        await act(() => router.navigate('/gantt?project=1&iteration=12'));
        await settle();
        await waitFor(() => expect(iterationSelect()).toHaveValue('12'));

        await userEvent.selectOptions(iterationSelect(), '21');
        await settle();
        expect(locationText()).toBe('/gantt?project=2&iteration=21');
        expect(useScopeStore.getState()).toMatchObject({ project: 2, iteration: 21 });

        await act(() => router.navigate(-1));
        await settle();
        expect(router.state.location.pathname).toBe('/my-work');
    });
});

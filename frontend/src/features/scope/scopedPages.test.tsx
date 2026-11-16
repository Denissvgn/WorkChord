import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { useState, type ReactNode } from 'react';
import { act, cleanup, render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { QueryClientProvider } from '@tanstack/react-query';
import { createMemoryRouter, Outlet, RouterProvider, useLocation } from 'react-router-dom';
import { ToastProvider } from '../../components/feedback/ToastProvider';
import { createTestQueryClient } from '../../test/renderWithProviders';
import i18n from '../../i18n/i18n';
import GanttPage from '../../pages/GanttPage';
import AnalyticsPage from '../../pages/AnalyticsPage';
import { ScopeBar } from '../../components/layout/ScopeBar';
import TasksPage from '../../pages/TasksPage';
import { useScopeStore } from './scopeStore';
import { useWorkScope } from './useWorkScope';
import { scopedLink } from './workScope';
import { overviewTaskDrawerHref } from '../overview/overviewTaskThread';

const iterationServiceMock = vi.hoisted(() => ({ getAll: vi.fn(), getSummary: vi.fn() }));
const ganttServiceMock = vi.hoisted(() => ({ getChart: vi.fn(), previewSchedule: vi.fn(), explainSchedule: vi.fn() }));
const taskServiceMock = vi.hoisted(() => ({ batchUpdate: vi.fn(), getDetail: vi.fn(), getById: vi.fn(), getIterationHistory: vi.fn() }));
const savedViewServiceMock = vi.hoisted(() => ({ getAll: vi.fn() }));
const projectServiceMock = vi.hoisted(() => ({ getAll: vi.fn() }));

vi.mock('../../services/iterationService', () => ({ iterationService: iterationServiceMock }));
vi.mock('../../services/ganttService', () => ({ ganttService: ganttServiceMock }));
vi.mock('../../services/taskService', () => ({ taskService: taskServiceMock }));
vi.mock('../../services/savedViewService', () => ({ savedViewService: savedViewServiceMock }));
vi.mock('../../services/projectService', () => ({ projectService: projectServiceMock }));
vi.mock('../../components/analytics/DeliveryAnalytics', () => ({ DeliveryAnalytics: () => null }));
vi.mock('../../components/analytics/OnTrackSummary', () => ({ OnTrackSummary: () => null }));
vi.mock('../../components/analytics/StatusDistribution', () => ({ StatusDistribution: () => null }));
vi.mock('../../components/tasks/WorkMetricsLine', () => ({ WorkMetricsLine: () => null }));
vi.mock('../../components/dashboard/SavedViewDashboardCards', () => ({ SavedViewDashboardCards: () => null }));
vi.mock('../../components/gantt/GanttChart', () => ({ GanttChart: () => <p>Gantt chart</p> }));
vi.mock('../../components/tasks/TaskList', () => ({ TaskList: () => <p>Iteration task list</p> }));
vi.mock('../../components/tasks/KanbanBoard/KanbanBoard', () => ({ KanbanBoard: () => <p>Board</p> }));
vi.mock('../../components/tasks/TaskFiltersBar', () => ({ TaskFiltersBar: () => <p>Filters</p> }));
vi.mock('../../components/tasks/SavedViewsControl', () => ({ SavedViewsControl: () => <p>Saved views</p> }));
vi.mock('../../components/tasks/BacklogPanel', () => ({ BacklogPanel: () => <p>Backlog task list</p> }));
vi.mock('../../components/tasks/TaskSearch', () => ({ TaskSearch: () => null }));
vi.mock('../../components/tasks/TaskEditorDrawer', () => ({
    TaskEditorDrawer: ({ open, onClose }: { open: boolean; onClose: () => void }) => (
        open ? <button type="button" onClick={onClose}>Close task</button> : null
    ),
}));

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

const PROJECTS = [
    { id: 1, name: 'Alpha', sort_order: 1, initiative: { id: 7, name: 'Platform' } },
    { id: 2, name: 'Beta', sort_order: 2, initiative: null },
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
            <ScopeBar />
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
    analytics: <AnalyticsPage />,
} as const;

const renderApp = (entry: string, deferred: boolean) => {
    const page = (element: ReactNode) => (deferred ? <Deferred>{element}</Deferred> : element);
    const router = createMemoryRouter([{
        element: <Shell />,
        children: [
            { path: '/tasks', element: page(PAGES.tasks) },
            { path: '/gantt', element: page(PAGES.gantt) },
            { path: '/analytics', element: page(PAGES.analytics) },
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

const iterationPicker = () => screen.getByRole('combobox', { name: i18n.t('scopeBar.iteration') });
const projectPicker = () => screen.getByRole('combobox', { name: i18n.t('scopeBar.project') });

const expectPageShowsScope = async (path: 'tasks' | 'gantt', iterationParam: string) => {
    if (iterationParam === 'backlog' && path === 'tasks') {
        expect(await screen.findByText('Backlog task list')).toBeInTheDocument();
        expect(screen.queryByText('Iteration task list')).not.toBeInTheDocument();
        return;
    }
    await waitFor(() => expect(iterationPicker()).toHaveValue(
        iterationParam === 'backlog' ? i18n.t('scopeBar.backlog') : `Iteration ${iterationParam}`,
    ));
    if (iterationParam === 'backlog') {
        expect(ganttServiceMock.getChart).not.toHaveBeenCalled();
    } else {
        expect(await screen.findByText(path === 'gantt' ? 'Gantt chart' : 'Iteration task list')).toBeInTheDocument();
    }
};

const SCOPED_URLS = [
    { label: 'Backlog of project 2', search: '?project=2&iteration=backlog', project: 2, iteration: 'backlog' },
    { label: 'iteration 21 of project 2', search: '?project=2&iteration=21', project: 2, iteration: 21 },
] as const;

describe('a scope in the URL survives opening a scoped page', () => {
    beforeEach(() => {
        vi.useFakeTimers({ toFake: ['Date'] });
        vi.setSystemTime(new Date('2026-11-16T12:00:00Z'));
        iterationServiceMock.getAll.mockReset();
        iterationServiceMock.getAll.mockResolvedValue(ITERATIONS);
        ganttServiceMock.getChart.mockReset();
        ganttServiceMock.getChart.mockImplementation(async (id: number) => ganttChart(id));
        savedViewServiceMock.getAll.mockResolvedValue([]);
        projectServiceMock.getAll.mockResolvedValue(PROJECTS);
        taskServiceMock.getIterationHistory.mockResolvedValue([]);
        iterationServiceMock.getSummary.mockImplementation(async (id: number) => ({ id, name: `Iteration ${id}`, start_date: '2026-10-01', end_date: '2026-10-31' }));
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

        it(`moves the scope to the iteration of a task opened from a link that names no iteration ${when}`, async () => {
            taskServiceMock.getById.mockResolvedValue({ id: 42, iteration_id: 21, title: 'Linked task' });
            useScopeStore.getState().remember({ project: 1, iteration: 12 });

            renderApp('/tasks?task=42', deferred);
            await waitForReady();
            if (deferred) await userEvent.click(screen.getByRole('button', { name: 'Open page' }));

            await waitFor(() => expect(locationText()).toBe('/tasks?task=42&project=2&iteration=21'));
            await settle();
            expect(locationText()).toBe('/tasks?task=42&project=2&iteration=21');
            expect(useScopeStore.getState()).toMatchObject({ project: 2, iteration: 21 });
        });

        it(`keeps the iteration a task link names, not the task's own ${when}`, async () => {
            taskServiceMock.getById.mockResolvedValue({ id: 42, iteration_id: 21, title: 'Linked task' });

            renderApp('/tasks?task=42&project=1&iteration=12', deferred);
            await waitForReady();
            if (deferred) await userEvent.click(screen.getByRole('button', { name: 'Open page' }));

            await waitFor(() => expect(taskServiceMock.getById).toHaveBeenCalledWith(42));
            await settle();
            expect(locationText()).toBe('/tasks?task=42&project=1&iteration=12');
            expect(iterationPicker()).toHaveValue('Iteration 12');
            expect(useScopeStore.getState()).toMatchObject({ project: 1, iteration: 12 });
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

    describe('a task opened from Overview keeps the scope its link names, and the scope bar then decides', () => {
        /** Opens the task as Overview links to it, from a page whose scope is iteration 12 of Alpha, then closes its drawer. */
        const openTaskFromOverviewAndClose = async () => {
            taskServiceMock.getById.mockResolvedValue({ id: 42, iteration_id: 11, title: 'Overview task' });
            const router = renderApp('/?project=1&iteration=12', false);
            await waitForReady();
            await settle();

            await act(() => router.navigate(scopedLink(overviewTaskDrawerHref(42, 'attention'), { project: 1, iteration: 12 })));
            await waitFor(() => expect(taskServiceMock.getById).toHaveBeenCalledWith(42));
            await settle();
            expect(iterationPicker()).toHaveValue('Iteration 12');
            expect(useScopeStore.getState()).toMatchObject({ project: 1, iteration: 12 });

            await userEvent.click(screen.getByRole('button', { name: 'Close task' }));
            await settle();
            const params = new URLSearchParams(router.state.location.search);
            expect(params.get('task')).toBeNull();
            expect(params.get('thread')).toBeNull();
            expect(params.get('from')).toBe('overview');
            expect(params.get('returnTask')).toBe('42');
            return router;
        };

        const scopeParams = (router: ReturnType<typeof renderApp>) => {
            const params = new URLSearchParams(router.state.location.search);
            return { project: params.get('project'), iteration: params.get('iteration') };
        };

        const chooseBacklog = async () => {
            await userEvent.click(iterationPicker());
            await userEvent.click(screen.getByRole('option', { name: new RegExp(`^${i18n.t('scopeBar.backlog')}`) }));
            await settle();
        };

        it('keeps another iteration chosen after the drawer closes', async () => {
            const router = await openTaskFromOverviewAndClose();

            await userEvent.click(iterationPicker());
            await userEvent.click(screen.getByRole('option', { name: /Iteration 11/ }));
            await settle();

            expect(iterationPicker()).toHaveValue('Iteration 11');
            expect(scopeParams(router)).toEqual({ project: '1', iteration: '11' });
            expect(useScopeStore.getState()).toMatchObject({ project: 1, iteration: 11 });
        });

        it('keeps Backlog chosen after the drawer closes', async () => {
            const router = await openTaskFromOverviewAndClose();

            await chooseBacklog();

            expect(await screen.findByText('Backlog task list')).toBeInTheDocument();
            expect(iterationPicker()).toHaveValue(i18n.t('scopeBar.backlog'));
            expect(scopeParams(router)).toEqual({ project: '1', iteration: 'backlog' });
            expect(useScopeStore.getState()).toMatchObject({ project: 1, iteration: 'backlog' });
        });

        it('keeps another project chosen after the drawer closes', async () => {
            const router = await openTaskFromOverviewAndClose();

            await userEvent.click(projectPicker());
            await userEvent.click(screen.getByRole('option', { name: 'Beta' }));
            await settle();

            expect(projectPicker()).toHaveValue('Beta');
            expect(iterationPicker()).toHaveValue('Iteration 22');
            expect(scopeParams(router)).toEqual({ project: '2', iteration: '22' });
            expect(useScopeStore.getState()).toMatchObject({ project: 2, iteration: 22 });
        });

        it('keeps Backlog after a refresh of the page left by the drawer-close flow', async () => {
            const router = await openTaskFromOverviewAndClose();
            await chooseBacklog();
            const url = `${router.state.location.pathname}${router.state.location.search}`;
            expect(new URLSearchParams(router.state.location.search).get('returnTask')).toBe('42');
            cleanup();
            taskServiceMock.getById.mockClear();

            renderApp(url, false);
            await waitForReady();
            await waitFor(() => expect(taskServiceMock.getById).toHaveBeenCalledWith(42));
            await settle();

            expect(locationText()).toBe(url);
            expect(await screen.findByText('Backlog task list')).toBeInTheDocument();
            expect(iterationPicker()).toHaveValue(i18n.t('scopeBar.backlog'));
            expect(useScopeStore.getState()).toMatchObject({ project: 1, iteration: 'backlog' });
        });
    });

    describe('a copied link with Overview task context opens the scope it names in a browser that remembered another', () => {
        beforeEach(() => {
            taskServiceMock.getById.mockReset();
            taskServiceMock.getById.mockResolvedValue({ id: 42, iteration_id: 11, title: 'Overview task' });
            useScopeStore.getState().remember({ project: 2, iteration: 21 });
        });

        const COPIED = [
            { label: 'Backlog', search: '?layout=board&from=overview&returnTask=42&project=1&iteration=backlog', iteration: 'backlog' },
            { label: 'another iteration than the task\'s', search: '?layout=board&from=overview&returnTask=42&project=1&iteration=12', iteration: 12 },
            { label: 'Backlog with the task drawer open', search: '?layout=board&task=42&from=overview&returnTask=42&thread=attention&project=1&iteration=backlog', iteration: 'backlog' },
            { label: 'another iteration with the task drawer open', search: '?layout=board&task=42&from=overview&returnTask=42&thread=attention&project=1&iteration=12', iteration: 12 },
        ] as const;

        for (const copied of COPIED) {
            it(`keeps ${copied.label}`, async () => {
                const url = `/tasks${copied.search}`;
                renderApp(url, false);
                await waitForReady();
                await waitFor(() => expect(taskServiceMock.getById).toHaveBeenCalledWith(42));
                await settle();

                expect(locationText()).toBe(url);
                expect(iterationPicker()).toHaveValue(
                    copied.iteration === 'backlog' ? i18n.t('scopeBar.backlog') : `Iteration ${copied.iteration}`,
                );
                expect(useScopeStore.getState()).toMatchObject({ project: 1, iteration: copied.iteration });
            });
        }

        it('does not move the scope for Overview return context alone when the link names no iteration', async () => {
            useScopeStore.getState().remember({ project: 1, iteration: 12 });
            renderApp('/tasks?layout=board&from=overview&returnTask=42', false);
            await waitForReady();
            await waitFor(() => expect(taskServiceMock.getById).toHaveBeenCalledWith(42));
            await settle();

            expect(locationText()).toBe('/tasks?layout=board&from=overview&returnTask=42&project=1&iteration=12');
            expect(useScopeStore.getState()).toMatchObject({ project: 1, iteration: 12 });
        });
    });

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
        await waitFor(() => expect(iterationPicker()).toHaveValue('Iteration 12'));

        await userEvent.click(iterationPicker());
        await userEvent.click(screen.getByRole('option', { name: /Iteration 11/ }));
        await settle();
        expect(locationText()).toBe('/gantt?project=1&iteration=11');
        expect(useScopeStore.getState()).toMatchObject({ project: 1, iteration: 11 });

        await act(() => router.navigate(-1));
        await settle();
        expect(router.state.location.pathname).toBe('/my-work');
    });

    it('changes the project from the bar and opens that project on its default iteration', async () => {
        const router = renderApp('/my-work', false);
        await waitForReady();
        await settle();
        await act(() => router.navigate('/gantt?project=1&iteration=12'));
        await settle();
        await waitFor(() => expect(projectPicker()).toHaveValue('Alpha'));

        await userEvent.click(projectPicker());
        await userEvent.click(screen.getByRole('option', { name: 'Beta' }));
        await settle();
        expect(locationText()).toBe('/gantt?project=2&iteration=22');
        expect(iterationPicker()).toHaveValue('Iteration 22');
    });

    it('shows the iteration chosen on Tasks on Gantt and Analytics, and again on Tasks', async () => {
        const router = renderApp('/tasks?project=1&iteration=12', false);
        await waitForReady();
        await waitFor(() => expect(iterationPicker()).toHaveValue('Iteration 12'));

        await userEvent.click(iterationPicker());
        await userEvent.click(screen.getByRole('option', { name: /Iteration 11/ }));
        await settle();
        expect(locationText()).toBe('/tasks?project=1&iteration=11');

        await act(() => router.navigate('/gantt'));
        await settle();
        expect(locationText()).toBe('/gantt?project=1&iteration=11');
        expect(iterationPicker()).toHaveValue('Iteration 11');
        await waitFor(() => expect(ganttServiceMock.getChart).toHaveBeenLastCalledWith(11));

        await act(() => router.navigate('/analytics'));
        await settle();
        expect(locationText()).toBe('/analytics?project=1&iteration=11');
        expect(iterationPicker()).toHaveValue('Iteration 11');
        await waitFor(() => expect(taskServiceMock.getIterationHistory).toHaveBeenLastCalledWith(11));

        await act(() => router.navigate('/tasks'));
        await settle();
        expect(locationText()).toBe('/tasks?project=1&iteration=11');
        expect(await screen.findByText('Iteration task list')).toBeInTheDocument();
    });

    it('shows the scope as text on a workspace-wide page', async () => {
        renderApp('/my-work?project=1&iteration=11', false);
        await waitForReady();
        await settle();
        expect(screen.queryByRole('combobox')).not.toBeInTheDocument();
        expect(screen.getByTestId('scope-bar')).toHaveTextContent('ProjectAlpha·IterationIteration 11');
    });
});

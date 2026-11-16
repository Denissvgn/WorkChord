import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { act, render, screen, waitFor } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { QueryClientProvider } from '@tanstack/react-query';
import { createMemoryRouter, Outlet, RouterProvider, useLocation } from 'react-router-dom';
import { ToastProvider } from '../../components/feedback/ToastProvider';
import { createTestQueryClient } from '../../test/renderWithProviders';
import i18n from '../../i18n/i18n';
import TasksPage from '../../pages/TasksPage';
import { useScopeStore } from './scopeStore';
import { ScopeBar } from '../../components/layout/ScopeBar';
import { useWorkScope } from './useWorkScope';

const iterationServiceMock = vi.hoisted(() => ({ getAll: vi.fn() }));
const projectServiceMock = vi.hoisted(() => ({ getAll: vi.fn() }));
const taskServiceMock = vi.hoisted(() => ({ lookup: vi.fn(), batchUpdate: vi.fn(), getDetail: vi.fn(), getById: vi.fn() }));
const savedViewServiceMock = vi.hoisted(() => ({ getAll: vi.fn() }));

vi.mock('../../services/iterationService', () => ({ iterationService: iterationServiceMock }));
vi.mock('../../services/projectService', () => ({ projectService: projectServiceMock }));
vi.mock('../../services/taskService', () => ({ taskService: taskServiceMock }));
vi.mock('../../services/savedViewService', () => ({ savedViewService: savedViewServiceMock }));
vi.mock('../../components/tasks/TaskSearch', () => ({ TaskSearch: () => null }));
vi.mock('../../components/tasks/TaskList', () => ({ TaskList: () => <p>Iteration task list</p> }));
vi.mock('../../components/tasks/KanbanBoard/KanbanBoard', () => ({ KanbanBoard: () => <p>Iteration board</p> }));
vi.mock('../../components/tasks/TaskFiltersBar', () => ({ TaskFiltersBar: () => null }));
vi.mock('../../components/tasks/SavedViewsControl', () => ({ SavedViewsControl: () => null }));
vi.mock('../../components/tasks/TaskEditorDrawer', () => ({ TaskEditorDrawer: () => null }));

const iteration = (id: number, project_id: number, start_date: string, end_date: string) => ({
    id, name: `Iteration ${id}`, calendar_id: 1, project_id, start_date, end_date, working_days: 10,
});

// Today is 2026-11-16: iteration 12 of project 1 contains it, so it is the default of Alpha
// and of All projects. Gamma has no iterations, so it opens on its Backlog.
const ITERATIONS = [
    iteration(11, 1, '2026-10-01', '2026-10-31'),
    iteration(12, 1, '2026-11-01', '2026-11-30'),
    iteration(21, 2, '2026-09-01', '2026-09-30'),
];

const PROJECTS = [
    { id: 1, name: 'Alpha' },
    { id: 2, name: 'Beta' },
    { id: 3, name: 'Gamma' },
];

const backlogTask = (id: number, projectId: number) => ({
    id, title: `Backlog task ${id}`, project_id: projectId,
    project_name: PROJECTS.find(project => project.id === projectId)?.name, status: 'todo',
});

/** True when the shell also shows the scope bar. The Tasks backlog has its own project select, so most tests leave it out. */
let showScopeBar = false;

/** Stands in for the app shell: it holds the scope for every page, as AppShell does. */
const Shell = () => {
    const { isReady } = useWorkScope();
    const location = useLocation();
    return (
        <>
            <output data-testid="location">{`${location.pathname}${location.search}`}</output>
            <output data-testid="ready">{String(isReady)}</output>
            {showScopeBar && <ScopeBar />}
            <Outlet />
        </>
    );
};

const renderTasks = (entry: string) => {
    const router = createMemoryRouter([{
        element: <Shell />,
        children: [
            { path: '/tasks', element: <TasksPage /> },
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
const settle = () => act(() => new Promise(resolve => setTimeout(resolve, 50)));
const projectSelect = () => screen.getByRole('combobox', { name: i18n.t('teamwork.project') });
const lastLookup = () => taskServiceMock.lookup.mock.calls.at(-1)?.[0];

describe('the project selector of the Tasks backlog sets the work scope', () => {
    beforeEach(() => {
        showScopeBar = false;
        vi.useFakeTimers({ toFake: ['Date'] });
        vi.setSystemTime(new Date('2026-11-16T12:00:00Z'));
        iterationServiceMock.getAll.mockReset();
        iterationServiceMock.getAll.mockResolvedValue(ITERATIONS);
        projectServiceMock.getAll.mockReset();
        projectServiceMock.getAll.mockResolvedValue(PROJECTS);
        taskServiceMock.lookup.mockReset();
        taskServiceMock.lookup.mockImplementation(async (params: { project_id?: number }) => ({
            items: params.project_id ? [backlogTask(params.project_id * 100, params.project_id)] : [],
            has_more: false,
            next_after_id: null,
        }));
        savedViewServiceMock.getAll.mockResolvedValue([]);
        useScopeStore.setState({ project: 1, iteration: 12 });
    });

    afterEach(() => {
        vi.useRealTimers();
    });

    it('shows and requests the backlog of the project in the URL', async () => {
        renderTasks('/tasks?project=2&iteration=backlog');
        await waitFor(() => expect(screen.getByTestId('ready')).toHaveTextContent('true'));

        await waitFor(() => expect(projectSelect()).toHaveDisplayValue('Beta'));
        expect(await screen.findByRole('link', { name: /Backlog task 200/ })).toBeInTheDocument();
        expect(taskServiceMock.lookup).toHaveBeenCalled();
        for (const [params] of taskServiceMock.lookup.mock.calls) {
            expect(params).toMatchObject({ project_id: 2, backlog_only: true });
        }
        await settle();
        expect(locationText()).toBe('/tasks?project=2&iteration=backlog');
        expect(useScopeStore.getState()).toMatchObject({ project: 2, iteration: 'backlog' });
    });

    it('resets the iteration by the default rule when a project is chosen in the backlog', async () => {
        renderTasks('/tasks?project=2&iteration=backlog');
        await waitFor(() => expect(projectSelect()).toHaveDisplayValue('Beta'));

        await userEvent.selectOptions(projectSelect(), 'Alpha');
        await settle();

        expect(locationText()).toBe('/tasks?project=1&iteration=12');
        expect(useScopeStore.getState()).toMatchObject({ project: 1, iteration: 12 });
        expect(screen.getByText('Iteration task list')).toBeInTheDocument();
        expect(screen.queryByRole('combobox', { name: i18n.t('teamwork.project') })).not.toBeInTheDocument();
    });

    it('stays on the backlog when the chosen project has no iterations', async () => {
        renderTasks('/tasks?project=2&iteration=backlog');
        await waitFor(() => expect(projectSelect()).toHaveDisplayValue('Beta'));

        await userEvent.selectOptions(projectSelect(), 'Gamma');
        await settle();

        expect(locationText()).toBe('/tasks?project=3&iteration=backlog');
        expect(useScopeStore.getState()).toMatchObject({ project: 3, iteration: 'backlog' });
        expect(projectSelect()).toHaveDisplayValue('Gamma');
        expect(lastLookup()).toMatchObject({ project_id: 3, backlog_only: true });
        expect(await screen.findByRole('link', { name: /Backlog task 300/ })).toBeInTheDocument();
        expect(screen.queryByRole('link', { name: /Backlog task 200/ })).not.toBeInTheDocument();
    });

    it('opens All projects on the iteration the default rule picks across every project', async () => {
        renderTasks('/tasks?project=2&iteration=backlog');
        await waitFor(() => expect(projectSelect()).toHaveDisplayValue('Beta'));

        await userEvent.selectOptions(projectSelect(), i18n.t('teamwork.allProjects'));
        await settle();

        expect(locationText()).toBe('/tasks?project=all&iteration=12');
        expect(useScopeStore.getState()).toMatchObject({ project: 'all', iteration: 12 });
    });

    it('changes the project in the backlog without adding a history entry', async () => {
        const router = renderTasks('/my-work');
        await settle();
        await act(() => router.navigate('/tasks?project=2&iteration=backlog'));
        await waitFor(() => expect(projectSelect()).toHaveDisplayValue('Beta'));

        await userEvent.selectOptions(projectSelect(), 'Alpha');
        await settle();
        expect(locationText()).toBe('/tasks?project=1&iteration=12');

        await act(() => router.navigate(-1));
        await settle();
        expect(router.state.location.pathname).toBe('/my-work');
    });
});

describe('the Tasks links into and out of the Backlog change only the scope', () => {
    beforeEach(() => {
        showScopeBar = false;
        vi.useFakeTimers({ toFake: ['Date'] });
        vi.setSystemTime(new Date('2026-11-16T12:00:00Z'));
        iterationServiceMock.getAll.mockReset();
        iterationServiceMock.getAll.mockResolvedValue(ITERATIONS);
        projectServiceMock.getAll.mockReset();
        projectServiceMock.getAll.mockResolvedValue(PROJECTS);
        taskServiceMock.lookup.mockReset();
        taskServiceMock.lookup.mockResolvedValue({ items: [], has_more: false, next_after_id: null });
        savedViewServiceMock.getAll.mockResolvedValue([]);
        useScopeStore.setState({ project: null, iteration: null });
    });

    afterEach(() => {
        vi.useRealTimers();
    });

    const openTasksFromMyWork = async (entry: string) => {
        const router = renderTasks('/my-work');
        await settle();
        await act(() => router.navigate(entry));
        await settle();
        return router;
    };

    const goBack = async (router: ReturnType<typeof renderTasks>) => {
        await act(() => router.navigate(-1));
        await settle();
    };

    it('enters the Backlog, changes the project, and Back returns to the page before Tasks', async () => {
        const router = await openTasksFromMyWork('/tasks');
        expect(locationText()).toBe('/tasks?project=1&iteration=12');

        await userEvent.click(await screen.findByRole('link', { name: i18n.t('teamwork.projectBacklog') }));
        await settle();
        expect(locationText()).toBe('/tasks?project=1&iteration=backlog');
        expect(useScopeStore.getState()).toMatchObject({ project: 1, iteration: 'backlog' });

        await waitFor(() => expect(projectSelect()).toHaveDisplayValue('Alpha'));
        await userEvent.selectOptions(projectSelect(), 'Gamma');
        await settle();
        expect(locationText()).toBe('/tasks?project=3&iteration=backlog');

        await goBack(router);
        expect(router.state.location.pathname).toBe('/my-work');
    });

    it('leaves the Backlog for the iteration tasks, and Back returns to the page before Tasks', async () => {
        const router = await openTasksFromMyWork('/tasks?project=2&iteration=backlog');
        await waitFor(() => expect(projectSelect()).toHaveDisplayValue('Beta'));

        await userEvent.click(screen.getByRole('link', { name: i18n.t('teamwork.iterationTasks') }));
        await settle();
        expect(locationText()).toBe('/tasks?project=2&iteration=21');
        expect(screen.getByText('Iteration task list')).toBeInTheDocument();

        await goBack(router);
        expect(router.state.location.pathname).toBe('/my-work');
    });

    it('changes the iteration in the iteration view, and Back returns to the page before Tasks', async () => {
        showScopeBar = true;
        const router = await openTasksFromMyWork('/tasks');
        const picker = await screen.findByRole('combobox', { name: i18n.t('scopeBar.iteration') });

        await userEvent.click(picker);
        await userEvent.click(screen.getByRole('option', { name: /Iteration 11/ }));
        await settle();
        expect(locationText()).toBe('/tasks?project=1&iteration=11');

        await goBack(router);
        expect(router.state.location.pathname).toBe('/my-work');
    });

    it('opens Iterations as a new page when there are no iterations, so Back returns to Tasks', async () => {
        iterationServiceMock.getAll.mockResolvedValue([]);
        const router = await openTasksFromMyWork('/tasks');

        await userEvent.click(await screen.findByRole('link', { name: i18n.t('tasks.goToIterations') }));
        await settle();
        expect(router.state.location.pathname).toBe('/iterations');

        await goBack(router);
        expect(router.state.location.pathname).toBe('/tasks');
    });
});

import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { act, screen, waitFor, within } from '@testing-library/react';
import { Route, Routes, useLocation } from 'react-router-dom';
import { renderWithProviders } from '../test/renderWithProviders';
import { useScopeStore } from '../features/scope/scopeStore';
import { ScopeBar } from '../components/layout/ScopeBar';
import { LegacyRedirect } from '../navigation/LegacyRedirect';
import type { IterationPlanningReadinessSummary, PlanCheckpoint } from '../types/iteration';
import PlanPage from './PlanPage';

const services = vi.hoisted(() => ({
    iterations: { getAll: vi.fn(), getPlanningReadiness: vi.fn(), create: vi.fn(), update: vi.fn(), delete: vi.fn() },
    projects: { getAll: vi.fn() },
    calendars: { getAll: vi.fn() },
    team: { getByIteration: vi.fn(), getProfiles: vi.fn() },
    tasks: { getByIteration: vi.fn() },
    gantt: { getChart: vi.fn() },
    triage: { getAll: vi.fn() },
    share: { getCurrent: vi.fn() },
    planning: { readInitial: vi.fn() },
}));

vi.mock('../services/iterationService', () => ({ iterationService: services.iterations }));
vi.mock('../services/projectService', () => ({ projectService: services.projects }));
vi.mock('../services/calendarService', () => ({ calendarService: services.calendars }));
vi.mock('../services/teamService', () => ({ teamService: services.team }));
vi.mock('../services/taskService', () => ({ taskService: services.tasks }));
vi.mock('../services/ganttService', () => ({ ganttService: services.gantt }));
vi.mock('../services/triageService', () => ({ triageService: services.triage }));
vi.mock('../services/planShareService', () => ({ planShareService: services.share }));
vi.mock('../services/planningInputService', () => ({ planningInputService: services.planning }));

const iteration = (id: number, name: string, project_id: number) => ({
    id, name, calendar_id: 1, project_id, start_date: '2026-11-01', end_date: '2026-11-30', working_days: 10,
    project: { id: project_id, name: project_id === 1 ? 'Agdash' : 'Beacon', status: 'active', health: 'green' },
});

const ITERATIONS = [iteration(12, 'Sprint 2', 1), iteration(21, 'Launch', 2)];
const PROJECTS = [
    { id: 1, name: 'Agdash', sort_order: 1, initiative: null },
    { id: 2, name: 'Beacon', sort_order: 2, initiative: null },
    { id: 3, name: 'Cobalt', sort_order: 3, initiative: null },
];

const checkpoint = (id: PlanCheckpoint['id'], state: PlanCheckpoint['state'], reason_codes: string[] = []): PlanCheckpoint => (
    { id, state, reason_codes, counts: {} }
);
const summary = (iterationId: number): IterationPlanningReadinessSummary => {
    const checkpoints = [
        checkpoint('iteration', 'done'), checkpoint('team', 'todo', ['no_people']), checkpoint('work', 'todo', ['no_tasks']),
        checkpoint('blockers', 'blocked', ['add_work_first']), checkpoint('schedule', 'blocked', ['complete_earlier_checkpoints']),
        checkpoint('review', 'blocked', ['build_schedule_first']),
    ];
    return {
        iteration_id: iterationId, team_member_count: 0, team_capacity_hours: 0, planned_hours: 0, assigned_hours: 0,
        team_members_no_capacity: 0, task_count: 0, tasks_without_assignee: 0, tasks_without_effort: 0,
        has_schedule: false, risk_count: 0, checkpoints, checkpoints_done: 1, checkpoints_total: 6,
    };
};

const LocationProbe = () => {
    const location = useLocation();
    return <output data-testid="location">{`${location.pathname}${location.search}`}</output>;
};

const settle = () => act(() => new Promise(resolve => setTimeout(resolve, 30)));
const locationText = () => screen.getByTestId('location').textContent;
const formDialog = (name = 'Create new iteration') => screen.queryByRole('dialog', { name });
const listDialog = () => screen.queryByRole('dialog', { name: 'All iterations' });

describe('Plan manages iterations', () => {
    beforeEach(() => {
        vi.clearAllMocks();
        services.iterations.getAll.mockResolvedValue(ITERATIONS);
        services.iterations.getPlanningReadiness.mockImplementation(async (id: number) => summary(id));
        services.projects.getAll.mockResolvedValue(PROJECTS);
        services.calendars.getAll.mockResolvedValue([{ id: 1, name: 'Company calendar', year: 2026, holidays: [], weekend_days: [5, 6], short_days: [] }]);
        services.team.getByIteration.mockResolvedValue([]);
        services.team.getProfiles.mockResolvedValue([]);
        services.tasks.getByIteration.mockResolvedValue([]);
        services.gantt.getChart.mockResolvedValue({ tasks: [], holidays: [], weekends: [] });
        services.triage.getAll.mockResolvedValue([]);
        services.share.getCurrent.mockResolvedValue(null);
        services.planning.readInitial.mockImplementation(async (_kind: string, id: number) => ({
            resource: ITERATIONS.find(item => item.id === id), resource_id: id, expected_revisions: { [id]: 1 }, complete: true,
        }));
        useScopeStore.setState({ project: null, iteration: null });
    });

    afterEach(() => {
        useScopeStore.setState({ project: null, iteration: null });
    });

    const renderPlan = async (entry: string) => {
        const view = renderWithProviders(
            <><ScopeBar /><PlanPage /><LocationProbe /></>,
            { initialEntries: [entry] },
        );
        await waitFor(() => expect(screen.getByTestId('scope-bar')).not.toHaveTextContent('Loading'));
        await settle();
        return view;
    };

    const chooseAction = async (user: ReturnType<typeof renderWithProviders>['user'], name: string) => {
        await user.click(screen.getByRole('combobox', { name: 'Iteration' }));
        await user.click(await screen.findByRole('option', { name }));
        await settle();
    };

    describe('checkpoint 1', () => {
        it('shows the iteration in scope with its dates, working days, calendar and project, and Edit', async () => {
            const { user } = await renderPlan('/plan?project=2&iteration=21');
            const section = await screen.findByTestId('plan-section-iteration');
            await user.click(within(section).getByRole('button', { name: /Iteration$/ }));
            expect(within(section).getByText('Launch')).toBeVisible();
            expect(within(section).getByText('Dates').nextElementSibling).toHaveTextContent(/Nov 1, 2026.*Nov 30, 2026/);
            expect(within(section).getByText('10 days')).toBeVisible();
            expect(within(section).getByText('Company calendar')).toBeVisible();
            expect(within(section).getByRole('link', { name: 'Beacon' })).toHaveAttribute('href', '/projects/2');

            await user.click(within(section).getByRole('button', { name: 'Edit' }));
            const drawer = await screen.findByRole('dialog', { name: 'Edit iteration' });
            await waitFor(() => expect(within(drawer).getByLabelText('Iteration name')).toHaveValue('Launch'));
            expect(locationText()).toContain('edit=21');
            await user.click(within(drawer).getByRole('button', { name: 'Cancel' }));
            await waitFor(() => expect(formDialog('Edit iteration')).not.toBeInTheDocument());
            expect(locationText()).toBe('/plan?project=2&iteration=21&step=iteration');
        });

        it('offers New iteration when the project has none, and saving it sets the scope and marks the checkpoint done', async () => {
            services.iterations.getAll.mockResolvedValue([]);
            const created = { ...iteration(31, 'Kickoff', 3), start_date: '2026-12-01', end_date: '2026-12-14', working_days: 10 };
            services.iterations.create.mockImplementation(async () => {
                services.iterations.getAll.mockResolvedValue([created]);
                return created;
            });
            const { user } = await renderPlan('/plan?project=3&iteration=backlog');

            const section = screen.getByTestId('plan-section-iteration');
            expect(section).toHaveAttribute('data-state', 'todo');
            expect(section).toHaveTextContent('There is no iteration in scope.');
            await user.click(within(section).getByRole('button', { name: 'New iteration' }));

            const drawer = await screen.findByRole('dialog', { name: 'Create new iteration' });
            // The new iteration starts on the project in scope.
            await waitFor(() => expect(within(drawer).getByRole('combobox', { name: 'Project scope' })).toHaveDisplayValue('Cobalt'));
            await user.type(within(drawer).getByLabelText('Iteration name'), 'Kickoff');
            await user.type(within(drawer).getByLabelText('Start date'), '2026-12-01');
            await user.type(within(drawer).getByLabelText('End date'), '2026-12-14');
            await user.click(within(drawer).getByRole('button', { name: 'Save iteration' }));

            await waitFor(() => expect(services.iterations.create).toHaveBeenCalled());
            expect(services.iterations.create.mock.calls[0][0]).toMatchObject(
                { name: 'Kickoff', project_id: 3, start_date: '2026-12-01', end_date: '2026-12-14' },
            );
            await waitFor(() => expect(formDialog()).not.toBeInTheDocument(),);
            // The scope follows the new iteration, in the link and in the scope bar.
            await waitFor(() => expect(locationText()).toBe('/plan?project=3&iteration=31'));
            expect(useScopeStore.getState()).toMatchObject({ project: 3, iteration: 31 });
            await waitFor(() => expect(screen.getByRole('combobox', { name: 'Iteration' })).toHaveValue('Kickoff'));
            // The checkpoint's state is the server's answer for the new iteration.
            await waitFor(() => expect(services.iterations.getPlanningReadiness).toHaveBeenCalledWith(31));
            await waitFor(() => expect(screen.getByTestId('plan-section-iteration')).toHaveAttribute('data-state', 'done'));
            expect(screen.getByText('1 of 6')).toBeVisible();
        });
    });

    describe('New iteration and Manage iterations in the scope bar', () => {
        it('opens the form for New iteration and the list for Manage iterations', async () => {
            const { user } = await renderPlan('/plan?project=2&iteration=21');
            expect(formDialog()).not.toBeInTheDocument();
            expect(listDialog()).not.toBeInTheDocument();

            await chooseAction(user, 'New iteration');
            expect(locationText()).toContain('create=1');
            expect(formDialog()).toBeInTheDocument();
            expect(listDialog()).not.toBeInTheDocument();

            await chooseAction(user, 'Manage iterations');
            expect(locationText()).toContain('panel=iterations');
            expect(locationText()).not.toContain('create=1');
            expect(formDialog()).not.toBeInTheDocument();
            expect(listDialog()).toBeInTheDocument();
        });

        it('shows the new iteration form in the drawer with four fields first and the rest under More', async () => {
            const { user } = await renderPlan('/plan?project=2&iteration=21&create=1');
            const drawer = await screen.findByRole('dialog', { name: 'Create new iteration' });
            expect(drawer).toHaveAttribute('aria-modal', 'true');
            expect(within(drawer).getByLabelText('Iteration name')).toBeVisible();
            expect(within(drawer).getByRole('combobox', { name: 'Project scope' })).toBeVisible();
            expect(within(drawer).getByLabelText('Start date')).toBeVisible();
            expect(within(drawer).getByLabelText('End date')).toBeVisible();
            expect(within(drawer).getByRole('button', { name: 'More' })).toHaveAttribute('aria-expanded', 'false');
            expect(within(drawer).queryByRole('button', { name: 'Repeating series' })).not.toBeInTheDocument();
            expect(within(drawer).queryByLabelText('Calendar')).not.toBeInTheDocument();
            expect(within(drawer).queryByLabelText('Manager email (for notifications)')).not.toBeInTheDocument();
            await user.click(within(drawer).getByRole('button', { name: 'More' }));
            expect(within(drawer).getByRole('button', { name: 'Repeating series' })).toBeVisible();
            expect(await within(drawer).findByRole('option', { name: 'Company calendar' })).toBeInTheDocument();
            expect(within(drawer).getByLabelText('Manager email (for notifications)')).toBeVisible();
        });

        it('removes create=1 and keeps the scope when the form is closed, and asks before dropping changes', async () => {
            const { user } = await renderPlan('/plan?project=2&iteration=21&create=1');
            const drawer = await screen.findByRole('dialog', { name: 'Create new iteration' });
            await user.type(within(drawer).getByLabelText('Iteration name'), 'Draft');
            await user.click(within(drawer).getByRole('button', { name: 'Close' }));
            await user.click(await screen.findByRole('button', { name: 'Keep editing' }));
            expect(formDialog()).toBeInTheDocument();
            await user.click(within(formDialog()!).getByRole('button', { name: 'Close' }));
            await user.click(await screen.findByRole('button', { name: 'Discard changes' }));
            await settle();
            expect(formDialog()).not.toBeInTheDocument();
            expect(locationText()).toBe('/plan?project=2&iteration=21');
        });
    });

    describe('All iterations drawer', () => {
        it('lists only the iterations of the project in scope, and all of them for All projects', async () => {
            const { user } = await renderPlan('/plan?panel=iterations&project=2&iteration=21');
            let drawer = await screen.findByRole('dialog', { name: 'All iterations' });
            expect(await within(drawer).findByRole('heading', { name: 'Launch' })).toBeVisible();
            expect(within(drawer).queryByRole('heading', { name: 'Sprint 2' })).not.toBeInTheDocument();
            await user.click(within(drawer).getByRole('button', { name: 'Close' }));

            await user.click(screen.getByRole('combobox', { name: 'Project' }));
            await user.click(await screen.findByRole('option', { name: /^All projects/ }));
            await settle();
            await user.click(screen.getByRole('combobox', { name: 'Iteration' }));
            await user.click(await screen.findByRole('option', { name: 'Manage iterations' }));
            await settle();
            drawer = await screen.findByRole('dialog', { name: 'All iterations' });
            expect(within(drawer).getByRole('heading', { name: 'Sprint 2' })).toBeVisible();
            expect(within(drawer).getByRole('heading', { name: 'Launch' })).toBeVisible();
        });

        it('opens an iteration: it becomes the scope with its project, and the drawer closes', async () => {
            const { user } = await renderPlan('/plan?panel=iterations&project=2&iteration=21');
            await user.click(await screen.findByRole('button', { name: 'Open Launch' }));
            await settle();
            expect(locationText()).toBe('/plan?project=2&iteration=21');
            expect(listDialog()).not.toBeInTheDocument();

            // The same list opens again from the first checkpoint.
            await user.click(within(screen.getByTestId('plan-section-iteration')).getByRole('button', { name: /Iteration$/ }));
            await user.click(screen.getByRole('button', { name: 'All iterations' }));
            expect(await screen.findByRole('dialog', { name: 'All iterations' })).toBeInTheDocument();
            expect(locationText()).toContain('panel=iterations');
        });

        it('keeps All projects when an iteration is opened under it', async () => {
            const { user } = await renderPlan('/plan?panel=iterations&project=all&iteration=12');
            const drawer = await screen.findByRole('dialog', { name: 'All iterations' });
            await user.click(await within(drawer).findByRole('button', { name: 'Open Launch' }));
            await settle();
            expect(locationText()).toBe('/plan?project=all&iteration=21');
            expect(useScopeStore.getState()).toMatchObject({ project: 'all', iteration: 21 });
        });

        it('edits an iteration from a row and returns to the list', async () => {
            const { user } = await renderPlan('/plan?panel=iterations&project=2&iteration=21');
            await user.click(await screen.findByRole('button', { name: 'Edit Launch' }));
            const drawer = await screen.findByRole('dialog', { name: 'Edit iteration' });
            expect(listDialog()).not.toBeInTheDocument();
            await waitFor(() => expect(within(drawer).getByLabelText('Iteration name')).toHaveValue('Launch'));
            await user.click(within(drawer).getByRole('button', { name: 'Cancel' }));
            await waitFor(() => expect(formDialog('Edit iteration')).not.toBeInTheDocument());
            expect(listDialog()).toBeInTheDocument();
            expect(locationText()).toBe('/plan?panel=iterations&project=2&iteration=21');
        });
    });

    describe('the old iterations path', () => {
        it('opens Plan with the All iterations drawer open', async () => {
            useScopeStore.setState({ project: 2, iteration: 21 });
            renderWithProviders(
                <>
                    <Routes>
                        <Route path="/plan" element={<PlanPage />} />
                        <Route path="/iterations" element={<LegacyRedirect><PlanPage /></LegacyRedirect>} />
                    </Routes>
                    <LocationProbe />
                </>,
                { initialEntries: ['/iterations?project=2&iteration=21'] },
            );
            const drawer = await screen.findByRole('dialog', { name: 'All iterations' });
            expect(locationText()).toBe('/plan?project=2&iteration=21&panel=iterations');
            expect(await within(drawer).findByRole('heading', { name: 'Launch' })).toBeVisible();
        });
    });
});

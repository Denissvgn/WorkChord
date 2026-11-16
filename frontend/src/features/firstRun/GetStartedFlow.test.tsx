import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { screen, waitFor, within } from '@testing-library/react';
import { useState } from 'react';
import type { ReactNode } from 'react';
import { Route, Routes, useLocation } from 'react-router-dom';
import { renderWithProviders } from '../../test/renderWithProviders';
import i18n from '../../i18n/i18n';
import OverviewPage from '../../pages/OverviewPage';
import PlanPage from '../../pages/PlanPage';
import TasksPage from '../../pages/TasksPage';
import { ScopeBar } from '../../components/layout/ScopeBar';
import { PlanReturnBar } from '../../components/planning/PlanReturnBar';
import { useScopeStore } from '../scope/scopeStore';
import { IdentityContext } from '../identity/identityContext';
import type { WorkspaceIdentity } from '../identity/identityService';
import type { Iteration, PlanCheckpoint } from '../../types/iteration';
import type { Project } from '../../types/project';
import type { Task } from '../../types/task';
import type { TeamMember } from '../../types/team';
import { FirstRunLanding } from './FirstRunLanding';
import { useGetStartedVisibility } from './getStartedVisibility';
import { SETUP_RETURN_KEY, useSetupReturn } from './setupReturn';

/** A small in-memory workspace standing in for the server, behind the real pages. */
const server = vi.hoisted(() => ({
    identity: null as unknown as WorkspaceIdentity,
    profiles: [] as { id: number; display_name: string; profile_kind: 'human' | 'agent' }[],
    projects: [] as Project[],
    iterations: [] as Iteration[],
    members: [] as TeamMember[],
    tasks: [] as Task[],
    scheduleApplied: false,
    writes: [] as string[],
}));

vi.mock('../../hooks/useAdminAccess', () => ({ useAdminAccess: () => ({ hasAdminKey: true }), useKeylessReader: () => ({ workViews: true }) }));
vi.mock('../../hooks/useAgentAccess', () => ({ useAgentAccess: () => ({ hasAgentKey: false }) }));
vi.mock('../../services/agentService', () => ({
    agentService: {
        getPipeline: vi.fn(async () => ({
            needs_definition: [], ready_to_assign: [], assigned_waiting: [], start_ready: [],
            executing: [], verification_required: [], recovery_required: [],
        })),
        getTaskTimeline: vi.fn(async () => ({ items: [] })),
    },
}));
vi.mock('../../services/projectService', () => ({
    projectService: {
        getAll: vi.fn(async () => [...server.projects]),
        create: vi.fn(async (data: Partial<Project>) => {
            server.writes.push('project');
            const project = { id: 40 + server.projects.length, sort_order: 1, initiative: null, ...data } as Project;
            server.projects.push(project);
            return project;
        }),
    },
}));
vi.mock('../../services/calendarService', () => ({
    calendarService: {
        getAll: vi.fn(async () => [{ id: 1, name: 'Company calendar', year: 2026, holidays: [], weekend_days: [5, 6], short_days: [] }]),
    },
}));
vi.mock('../../services/iterationService', () => {
    const readiness = (id: number) => {
        const iteration = server.iterations.find(item => item.id === id);
        const people = iteration ? server.members.length : 0;
        const work = iteration ? server.tasks.filter(task => task.iteration_id === id).length : 0;
        const applied = Boolean(iteration) && server.scheduleApplied;
        const state = (id: PlanCheckpoint['id']): PlanCheckpoint['state'] => {
            if (id === 'iteration') return iteration ? 'done' : 'todo';
            if (id === 'team') return people > 0 ? 'done' : 'todo';
            if (id === 'work') return work > 0 ? 'done' : 'todo';
            if (id === 'blockers') return work > 0 ? 'done' : 'blocked';
            if (id === 'schedule') return applied ? 'done' : people > 0 && work > 0 ? 'todo' : 'blocked';
            return applied ? 'done' : 'blocked';
        };
        const checkpoints = (['iteration', 'team', 'work', 'blockers', 'schedule', 'review'] as const)
            .map(item => ({ id: item, state: state(item), reason_codes: [], counts: {} }));
        return {
            iteration_id: id,
            team_member_count: people,
            team_capacity_hours: people * 64,
            planned_hours: work * 8,
            assigned_hours: work * 8,
            team_members_no_capacity: 0,
            task_count: work,
            tasks_without_assignee: 0,
            tasks_without_effort: 0,
            has_schedule: applied,
            risk_count: 0,
            checkpoints,
            checkpoints_done: checkpoints.filter(item => item.state === 'done').length,
            checkpoints_total: 6,
        };
    };
    return {
        iterationService: {
            getAll: vi.fn(async () => [...server.iterations]),
            getById: vi.fn(async (id: number) => ({ ...server.iterations.find(item => item.id === id), revision: 1 })),
            getPlanningReadiness: vi.fn(async (id: number) => readiness(id)),
            create: vi.fn(async (data: Partial<Iteration>) => {
                server.writes.push('iteration');
                const project = server.projects.find(item => item.id === data.project_id);
                const iteration = {
                    id: 70 + server.iterations.length, calendar_id: 1, working_days: 10, revision: 1, ...data,
                    project: project && { id: project.id, name: project.name, status: 'planned', health: 'unknown' },
                } as Iteration;
                server.iterations.push(iteration);
                return iteration;
            }),
        },
    };
});
vi.mock('../../services/teamService', () => ({
    teamService: {
        getByIteration: vi.fn(async () => [...server.members]),
        getProfiles: vi.fn(async () => [...server.profiles]),
        createProfile: vi.fn(async (data: { display_name: string }) => {
            server.writes.push('profile');
            const profile = { id: 7, display_name: data.display_name, profile_kind: 'human' as const };
            server.profiles.push(profile);
            return profile;
        }),
        create: vi.fn(async (iterationId: number, data: Partial<TeamMember>) => {
            server.writes.push('capacity');
            const member = { id: 30 + server.members.length, iteration_id: iterationId, vacations: [], ...data } as TeamMember;
            server.members.push(member);
            return member;
        }),
        getWorkload: vi.fn(async (id: number) => ({
            team_member_id: id, name: 'Ada Lovelace', capacity_days: 8, allocated_days: 1, free_days: 7,
            workload_status: 'green', workload_percent: 12, capacity_hours: 64, allocated_hours: 8, free_hours: 56, nominal_day_hours: 8,
        })),
    },
}));
vi.mock('../../services/planningInputService', () => ({
    planningInputService: { readInitial: vi.fn(async (_kind: string, id: number) => ({ expected_revisions: { [id]: 1 }, complete: true })) },
}));
vi.mock('../../services/taskService', () => ({
    taskService: {
        getByIteration: vi.fn(async (id: number) => server.tasks.filter(task => task.iteration_id === id)),
        lookup: vi.fn(async () => ({ items: [], has_more: false, next_after_id: null, limit: 100 })),
    },
}));
vi.mock('../../services/ganttService', () => {
    const chart = (id: number) => ({
        iteration: { ...server.iterations.find(item => item.id === id), revision: 1 },
        tasks: [], overdue_task_ids: [], holidays: [], weekends: [], member_vacations: {},
        schedule_result: server.scheduleApplied ? { success: true, decisions: [], workload_balanced: true, workload_issues: [], unscheduled: [] } : null,
    });
    return {
        ganttService: {
            getChart: vi.fn(async (id: number) => chart(id)),
            previewSchedule: vi.fn(async () => ({
                input_revision: 1, input_planning_revision: 1, tasks: [], overdue_task_ids: [],
                schedule_result: { success: true, decisions: [], workload_balanced: true, workload_issues: [], unscheduled: [] },
            })),
            schedule: vi.fn(async () => {
                server.writes.push('schedule');
                server.scheduleApplied = true;
                return { success: true };
            }),
        },
    };
});
vi.mock('../identity/identityService', () => ({
    identityService: {
        chooseLocalProfile: vi.fn(async (id: number | null) => {
            server.writes.push('local-profile');
            const chosen = server.profiles.find(profile => profile.id === id) ?? null;
            server.identity = { ...server.identity, profile: chosen && { id: chosen.id, display_name: chosen.display_name } };
            return { profile: server.identity.profile };
        }),
    },
}));
vi.mock('../../services/savedViewService', () => ({ savedViewService: { getAll: vi.fn(async () => []) } }));
vi.mock('../../services/labelService', () => ({ labelService: { getGroups: vi.fn(async () => []) } }));
vi.mock('../../services/triageService', () => ({ triageService: { getAll: vi.fn(async () => []) } }));
vi.mock('../../services/planShareService', () => ({ planShareService: { getCurrent: vi.fn(async () => null) } }));
vi.mock('../../services/sessionService', () => ({ sessionService: { getWhoAmI: vi.fn(async () => ({ id: 1, principal_id: null })) } }));
// The task list and the task form are pages of their own; this test follows the Tasks page around them.
vi.mock('../../components/tasks/TaskList', () => ({ TaskList: () => <p>Task list</p> }));
vi.mock('../../components/tasks/TaskForm', () => ({
    TaskForm: ({ iterationId, onSuccess }: { iterationId: number | null; onSuccess: () => void }) => (
        <button type="button" onClick={() => {
            server.writes.push('task');
            server.tasks.push({ id: 90 + server.tasks.length, title: 'Write the brief', iteration_id: iterationId, effort_hours: 8 } as Task);
            onSuccess();
        }}>Save the new task</button>
    ),
}));

const localIdentity = (): WorkspaceIdentity => ({
    mode: 'trusted_local',
    authenticated: true,
    configured: true,
    principal: null,
    profile: null,
    workspace_role: 'owner',
    projects: {},
    csrf_token: null,
    access: 'full',
});

/** The identity the shell provides, read again from the server on refresh. */
const TestIdentity = ({ children }: { children: ReactNode }) => {
    const [identity, setIdentity] = useState(server.identity);
    return (
        <IdentityContext.Provider value={{ identity, refresh: () => setIdentity(server.identity), signOut: async () => {} }}>
            {children}
        </IdentityContext.Provider>
    );
};

const LocationProbe = () => {
    const location = useLocation();
    return <output data-testid="location">{`${location.pathname}${location.search}`}</output>;
};

/** Gantt is a page of its own; on the way there and back only its return to Plan matters here. */
const GanttWithReturn = () => <div><h1>Gantt</h1><PlanReturnBar /></div>;

const renderWorkspace = () => renderWithProviders(
    <TestIdentity>
        <FirstRunLanding />
        <ScopeBar />
        <Routes>
            <Route path="/" element={<OverviewPage />} />
            <Route path="/plan" element={<PlanPage />} />
            <Route path="/tasks" element={<TasksPage />} />
            <Route path="/gantt" element={<GanttWithReturn />} />
        </Routes>
        <LocationProbe />
    </TestIdentity>,
    { initialEntries: ['/'] },
);

type User = ReturnType<typeof renderWorkspace>['user'];

const panel = () => screen.findByTestId('get-started-panel');
const step = (id: string) => screen.getByTestId(`get-started-step-${id}`);
const toggleOf = (id: string) => within(step(id)).getByRole('button', { name: new RegExp(i18n.t(`firstRun.steps.${id}.title`)) });
const location = () => screen.getByTestId('location').textContent ?? '';
const newTask = () => within(screen.getByTestId('page-header')).getByRole('link', { name: i18n.t('tasks.newTask') });
const backToSetup = () => screen.findByRole('link', { name: i18n.t('firstRun.backToSetup') });
const planSection = (id: string) => screen.findByTestId(`plan-section-${id}`);

/** Opens the step's checkpoint on the real Plan page from the panel's own link. */
const openStep = async (user: User, id: string, checkpoint: string) => {
    await panel();
    await waitFor(() => expect(toggleOf(id)).toHaveAttribute('aria-expanded', 'true'));
    const open = within(step(id)).getByRole('link', { name: i18n.t('firstRun.openPlan') });
    expect(open.getAttribute('href')).toMatch(new RegExp(`^/plan\\?step=${checkpoint}&setup=1`));
    expect(open).toHaveClass('btn', 'primary');
    await user.click(open);
    const section = await planSection(checkpoint);
    await waitFor(() => expect(within(section).getByRole('region')).toBeInTheDocument());
    return section;
};

/** Comes back to Get started from Plan, where the step just taken is done and the next one is open. */
const comeBack = async (user: User, id: string, nextId: string | null) => {
    await user.click(await backToSetup());
    expect(location()).toMatch(/^\/(\?|$)/);
    if (nextId === null) return;
    await waitFor(() => expect(step(id)).toHaveAttribute('data-done', 'true'));
    await waitFor(() => expect(toggleOf(nextId)).toHaveAttribute('aria-expanded', 'true'));
};

beforeEach(() => {
    localStorage.clear();
    sessionStorage.clear();
    useGetStartedVisibility.setState({ dismissed: false, requested: false });
    useSetupReturn.setState({ active: false });
    useScopeStore.setState({ project: null, iteration: null });
    server.identity = localIdentity();
    server.profiles = [];
    server.projects = [];
    server.iterations = [];
    server.members = [];
    server.tasks = [];
    server.scheduleApplied = false;
    server.writes = [];
    Element.prototype.scrollIntoView = vi.fn();
});

afterEach(() => {
    localStorage.clear();
    sessionStorage.clear();
});

describe('Get started panel with the real Plan and Tasks pages', () => {
    it('takes an empty workspace through the six steps to an applied schedule, then hides itself', async () => {
        const { user } = renderWorkspace();
        await panel();

        // 1 Say who you are: the profile picker, in place.
        await user.type(within(step('profile')).getByLabelText(i18n.t('identity.yourName')), 'Ada Lovelace');
        await user.click(within(step('profile')).getByRole('button', { name: i18n.t('identity.addMe') }));
        await waitFor(() => expect(step('profile')).toHaveAttribute('data-done', 'true'));

        // 2 Create a project: name, start and target date in a short modal.
        await waitFor(() => expect(toggleOf('project')).toHaveAttribute('aria-expanded', 'true'));
        await user.click(within(step('project')).getByRole('button', { name: i18n.t('firstRun.steps.project.action') }));
        const dialog = await screen.findByRole('dialog', { name: i18n.t('firstRun.createProject.title') });
        await user.type(within(dialog).getByLabelText(i18n.t('surfaces.projectForm.projectName')), 'Launch');
        await user.type(within(dialog).getByLabelText(i18n.t('surfaces.projectForm.startDate')), '2026-11-16');
        await user.type(within(dialog).getByLabelText(i18n.t('surfaces.projectForm.targetDate')), '2026-12-18');
        await user.click(within(dialog).getByRole('button', { name: i18n.t('surfaces.projectForm.createProject') }));
        await waitFor(() => expect(step('project')).toHaveAttribute('data-done', 'true'));
        const projectId = server.projects[0].id;

        // 3 Create an iteration: Plan, checkpoint 1. Saving puts the iteration in scope, which
        // rewrites the link; the way back to Get started stays.
        let section = await openStep(user, 'iteration', 'iteration');
        await user.click(within(section).getByRole('button', { name: 'New iteration' }));
        const drawer = await screen.findByRole('dialog', { name: 'Create new iteration' });
        await user.type(within(drawer).getByLabelText('Iteration name'), 'Iteration 1');
        await user.type(within(drawer).getByLabelText('Start date'), '2026-11-16');
        await user.type(within(drawer).getByLabelText('End date'), '2026-11-27');
        await user.click(within(drawer).getByRole('button', { name: 'Save iteration' }));
        const iterationId = 70;
        await waitFor(() => expect(location()).toBe(`/plan?project=${projectId}&iteration=${iterationId}`));
        await waitFor(() => expect(screen.getByTestId('plan-section-iteration')).toHaveAttribute('data-state', 'done'));
        await comeBack(user, 'iteration', 'capacity');

        // 4 Add capacity: Plan, checkpoint 2, with Add me and Connect an agent in place.
        section = await openStep(user, 'capacity', 'team');
        await user.click(within(section).getByRole('button', { name: i18n.t('teamPage.connectAgent') }));
        const connect = await screen.findByRole('dialog', { name: i18n.t('teamPage.connectAgent') });
        await user.click(within(connect).getByRole('button', { name: i18n.t('actions.close') }));
        await waitFor(() => expect(screen.queryByRole('dialog', { name: i18n.t('teamPage.connectAgent') })).not.toBeInTheDocument());
        await user.click(within(screen.getByTestId('plan-section-team')).getByRole('button', { name: i18n.t('identity.addMe') }));
        await waitFor(() => expect(server.members).toHaveLength(1));
        expect(server.members[0]).toMatchObject({ iteration_id: iterationId, profile_id: 7, name: 'Ada Lovelace' });
        await waitFor(() => expect(screen.getByTestId('plan-section-team')).toHaveAttribute('data-state', 'done'));
        await comeBack(user, 'capacity', 'tasks');

        // 5 Add tasks: Plan, checkpoint 3, then Tasks and back to the checkpoint.
        section = await openStep(user, 'tasks', 'work');
        await user.click(within(section).getByRole('link', { name: i18n.t('planWork.openTasks') }));
        await waitFor(() => expect(location()).toMatch(/^\/tasks\?.*fromPlanStep=work/));
        // Tasks is a full page of its own; the way back to Get started belongs to Plan.
        expect(screen.queryByRole('link', { name: i18n.t('firstRun.backToSetup') })).not.toBeInTheDocument();
        await user.click(await screen.findByRole('button', { name: i18n.t('tasks.newTask') }));
        await user.click(await screen.findByRole('button', { name: 'Save the new task' }));
        expect(server.tasks).toMatchObject([{ iteration_id: iterationId }]);
        await user.click(screen.getByRole('link', { name: i18n.t('plan.master.returnToCheckpoint') }));
        await waitFor(() => expect(location()).toMatch(/^\/plan\?/));
        expect(location()).not.toContain('setup=1');
        await waitFor(() => expect(screen.getByTestId('plan-section-work')).toHaveAttribute('data-state', 'done'));
        await comeBack(user, 'tasks', 'schedule');

        // 6 Build the schedule: Plan, checkpoint 5. Gantt and back, then calculate and apply.
        section = await openStep(user, 'schedule', 'schedule');
        await user.click(within(section).getByRole('link', { name: i18n.t('planSchedule.openGantt') }));
        await screen.findByRole('heading', { name: 'Gantt' });
        await user.click(screen.getByRole('link', { name: i18n.t('plan.master.returnToCheckpoint') }));
        section = await planSection('schedule');
        await user.click(await within(section).findByRole('button', { name: i18n.t('planSchedule.calculate') }));
        await user.click(await within(screen.getByTestId('plan-section-schedule')).findByRole('button', { name: i18n.t('planSchedule.apply') }));
        await waitFor(() => expect(server.scheduleApplied).toBe(true));
        await waitFor(() => expect(screen.getByTestId('plan-section-schedule')).toHaveAttribute('data-state', 'done'));
        await comeBack(user, 'schedule', null);

        // All six are done: the panel hides itself and New task is the primary action again.
        await waitFor(() => expect(screen.queryByTestId('get-started-panel')).not.toBeInTheDocument());
        await waitFor(() => expect(newTask()).toHaveClass('btn', 'primary'));
        expect(server.writes).toEqual(['profile', 'local-profile', 'project', 'iteration', 'capacity', 'task', 'schedule']);
        // Back on Overview, the step opened from the panel is over.
        expect(sessionStorage.getItem(SETUP_RETURN_KEY)).toBeNull();
    });
});

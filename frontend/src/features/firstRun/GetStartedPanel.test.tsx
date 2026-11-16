import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { act, screen, waitFor, within } from '@testing-library/react';
import { useState } from 'react';
import type { ReactNode } from 'react';
import { Route, Routes, useLocation, useSearchParams } from 'react-router-dom';
import { useQueryClient } from '@tanstack/react-query';
import { renderWithProviders } from '../../test/renderWithProviders';
import i18n from '../../i18n/i18n';
import OverviewPage from '../../pages/OverviewPage';
import { ContextHelp } from '../../components/layout/ContextHelp';
import { useScopeStore } from '../scope/scopeStore';
import { IdentityContext } from '../identity/identityContext';
import type { WorkspaceIdentity } from '../identity/identityService';
import type { Iteration, PlanCheckpoint } from '../../types/iteration';
import type { Project } from '../../types/project';
import { FirstRunLanding } from './FirstRunLanding';
import { SetupReturnBar } from './SetupReturnBar';
import { GET_STARTED_DISMISSED_KEY, useGetStartedVisibility } from './getStartedVisibility';
import { firstRunSteps } from './firstRunSteps';

/** A small in-memory workspace standing in for the server. */
const server = vi.hoisted(() => ({
    identity: null as unknown as WorkspaceIdentity,
    profiles: [] as { id: number; display_name: string; profile_kind: 'human' | 'agent' }[],
    projects: [] as Project[],
    iterations: [] as Iteration[],
    capacityRows: 0,
    tasks: 0,
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
vi.mock('../../services/taskService', () => ({
    taskService: { getByIteration: vi.fn(async () => []), lookup: vi.fn(async () => ({ items: [], has_more: false, next_after_id: null, limit: 100 })) },
}));
vi.mock('../../services/projectService', () => ({
    projectService: {
        getAll: vi.fn(async () => [...server.projects]),
        create: vi.fn(async (data: Partial<Project>) => {
            server.writes.push('project');
            const project = { id: 40 + server.projects.length, ...data } as Project;
            server.projects.push(project);
            return project;
        }),
    },
}));
vi.mock('../../services/iterationService', () => ({
    iterationService: {
        getAll: vi.fn(async () => [...server.iterations]),
        getPlanningReadiness: vi.fn(async (id: number) => {
            const ids = ['iteration', 'team', 'work', 'blockers', 'schedule', 'review'] as const;
            const checkpoints: PlanCheckpoint[] = ids.map(item => ({
                id: item,
                state: item === 'iteration' || (item === 'team' && server.capacityRows > 0) || (item === 'work' && server.tasks > 0)
                    || (item === 'schedule' && server.scheduleApplied) ? 'done' : 'todo',
                reason_codes: [],
                counts: {},
            }));
            return {
                iteration_id: id,
                team_member_count: server.capacityRows,
                team_capacity_hours: server.capacityRows * 64,
                team_members_no_capacity: 0,
                task_count: server.tasks,
                tasks_without_assignee: 0,
                tasks_without_effort: 0,
                has_schedule: server.scheduleApplied,
                risk_count: 0,
                checkpoints,
            };
        }),
    },
}));
vi.mock('../../services/teamService', () => ({
    teamService: {
        getByIteration: vi.fn(async () => []),
        getProfiles: vi.fn(async () => [...server.profiles]),
        createProfile: vi.fn(async (data: { display_name: string }) => {
            server.writes.push('profile');
            const profile = { id: 7, display_name: data.display_name, profile_kind: 'human' as const };
            server.profiles.push(profile);
            return profile;
        }),
    },
}));
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

const localIdentity = (profile: WorkspaceIdentity['profile'] = null): WorkspaceIdentity => ({
    mode: 'trusted_local',
    authenticated: true,
    configured: true,
    principal: null,
    profile,
    workspace_role: 'owner',
    projects: {},
    csrf_token: null,
    access: 'full',
});

const iterationFor = (projectId: number): Iteration => ({
    id: 70,
    name: 'Iteration 1',
    calendar_id: 1,
    project_id: projectId,
    project: { id: projectId, name: 'Launch', status: 'planned', health: 'unknown' },
    start_date: '2026-11-16',
    end_date: '2026-11-27',
    working_days: 10,
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

/**
 * Plan as far as this test needs it: the checkpoint the link asked for, a control that makes the
 * change on the server the way the real checkpoint does, and the way back to Get started.
 */
const PlanStand = () => {
    const [params] = useSearchParams();
    const client = useQueryClient();
    const step = params.get('step');
    const complete = async () => {
        if (step === 'iteration') server.iterations.push(iterationFor(server.projects[0].id));
        if (step === 'team') server.capacityRows += 1;
        if (step === 'work') server.tasks += 1;
        if (step === 'schedule') server.scheduleApplied = true;
        server.writes.push(`plan:${step}`);
        await client.invalidateQueries();
    };
    return (
        <div>
            <h1>Plan stand</h1>
            <SetupReturnBar />
            <button type="button" onClick={() => { void complete(); }}>Complete {step}</button>
        </div>
    );
};

const LocationProbe = () => {
    const location = useLocation();
    return <output data-testid="location">{`${location.pathname}${location.search}`}</output>;
};

const renderWorkspace = (url = '/') => renderWithProviders(
    <TestIdentity>
        <FirstRunLanding />
        <ContextHelp />
        <Routes>
            <Route path="/" element={<OverviewPage />} />
            <Route path="/plan" element={<PlanStand />} />
            <Route path="*" element={<p>Other page</p>} />
        </Routes>
        <LocationProbe />
    </TestIdentity>,
    { initialEntries: [url] },
);

const panel = () => screen.findByTestId('get-started-panel');
const step = (id: string) => screen.getByTestId(`get-started-step-${id}`);
const toggleOf = (id: string) => within(step(id)).getByRole('button', { name: new RegExp(i18n.t(`firstRun.steps.${id}.title`)) });
const doneStates = () => ['profile', 'project', 'iteration', 'capacity', 'tasks', 'schedule']
    .map(id => step(id).getAttribute('data-done') === 'true');
const newTask = () => within(screen.getByTestId('page-header')).getByRole('link', { name: i18n.t('tasks.newTask') });

/** Opens the step's Plan checkpoint, completes it there, and comes back to Get started. */
const followPlanStep = async (user: ReturnType<typeof renderWorkspace>['user'], id: string, checkpoint: string) => {
    await waitFor(() => expect(toggleOf(id)).toHaveAttribute('aria-expanded', 'true'));
    const open = within(step(id)).getByRole('link', { name: i18n.t('firstRun.openPlan') });
    expect(open.getAttribute('href')).toMatch(new RegExp(`^/plan\\?step=${checkpoint}&setup=1`));
    expect(open).toHaveClass('btn', 'primary');
    await user.click(open);
    await user.click(await screen.findByRole('button', { name: `Complete ${checkpoint}` }));
    await waitFor(() => expect(server.writes).toContain(`plan:${checkpoint}`));
    await user.click(screen.getByRole('link', { name: i18n.t('firstRun.backToSetup') }));
    expect(screen.getByTestId('location').textContent).toMatch(/^\/(\?|$)/);
};

beforeEach(() => {
    localStorage.clear();
    useGetStartedVisibility.setState({ dismissed: false, requested: false });
    useScopeStore.setState({ project: null, iteration: null });
    server.identity = localIdentity();
    server.profiles = [];
    server.projects = [];
    server.iterations = [];
    server.capacityRows = 0;
    server.tasks = 0;
    server.scheduleApplied = false;
    server.writes = [];
    Element.prototype.scrollIntoView = vi.fn();
});

afterEach(() => {
    localStorage.clear();
});

describe('Get started steps', () => {
    it('marks each step done from its own data only', () => {
        const empty = { profileChosen: false, projectCount: 0, iterationCount: 0, capacityRows: 0, taskCount: 0, scheduleApplied: false };
        expect(firstRunSteps(empty).map(item => item.done)).toEqual([false, false, false, false, false, false]);
        // A later step's data does not mark an earlier step done.
        expect(firstRunSteps({ ...empty, taskCount: 3 }).map(item => item.done)).toEqual([false, false, false, false, true, false]);
        expect(firstRunSteps({ profileChosen: true, projectCount: 1, iterationCount: 1, capacityRows: 1, taskCount: 1, scheduleApplied: true })
            .every(item => item.done)).toBe(true);
    });
});

describe('Get started panel', () => {
    it('takes an empty workspace through the six steps to an applied schedule, then hides itself', async () => {
        const { user } = renderWorkspace();
        await panel();
        expect(doneStates()).toEqual([false, false, false, false, false, false]);
        // While the panel shows, its next step is the page's one primary action.
        expect(newTask()).toHaveClass('btn', 'secondary');
        // The empty Overview does not repeat the next step.
        expect(screen.queryByText(i18n.t('overview.noIterationTitle'))).not.toBeInTheDocument();

        // 1 Say who you are: the profile picker, in place.
        expect(toggleOf('profile')).toHaveAttribute('aria-expanded', 'true');
        await user.type(within(step('profile')).getByLabelText(i18n.t('identity.yourName')), 'Ada Lovelace');
        await user.click(within(step('profile')).getByRole('button', { name: i18n.t('identity.addMe') }));
        await waitFor(() => expect(step('profile')).toHaveAttribute('data-done', 'true'));
        expect(step('profile')).toHaveTextContent(i18n.t('firstRun.steps.profile.result', { name: 'Ada Lovelace' }));

        // 2 Create a project: name, start and target date in a short modal.
        await waitFor(() => expect(toggleOf('project')).toHaveAttribute('aria-expanded', 'true'));
        await user.click(within(step('project')).getByRole('button', { name: i18n.t('firstRun.steps.project.action') }));
        const dialog = await screen.findByRole('dialog', { name: i18n.t('firstRun.createProject.title') });
        await user.type(within(dialog).getByLabelText(i18n.t('surfaces.projectForm.projectName')), 'Launch');
        await user.type(within(dialog).getByLabelText(i18n.t('surfaces.projectForm.startDate')), '2026-11-16');
        await user.type(within(dialog).getByLabelText(i18n.t('surfaces.projectForm.targetDate')), '2026-12-18');
        await user.click(within(dialog).getByRole('button', { name: i18n.t('surfaces.projectForm.createProject') }));
        await waitFor(() => expect(step('project')).toHaveAttribute('data-done', 'true'));
        expect(server.projects[0]).toMatchObject({ name: 'Launch', start_date: '2026-11-16', target_date: '2026-12-18' });
        expect(screen.queryByRole('dialog')).not.toBeInTheDocument();
        // The new project becomes the scope, so its iteration is created in it.
        expect(useScopeStore.getState().project).toBe(server.projects[0].id);

        // 3 to 6 open Plan at their checkpoints; coming back opens the next step.
        await followPlanStep(user, 'iteration', 'iteration');
        await panel();
        await waitFor(() => expect(step('iteration')).toHaveAttribute('data-done', 'true'));
        await followPlanStep(user, 'capacity', 'team');
        await panel();
        await waitFor(() => expect(step('capacity')).toHaveAttribute('data-done', 'true'));
        await followPlanStep(user, 'tasks', 'work');
        await panel();
        await waitFor(() => expect(step('tasks')).toHaveAttribute('data-done', 'true'));
        await followPlanStep(user, 'schedule', 'schedule');

        // The schedule is applied: all six are done and the panel is gone.
        expect(server.scheduleApplied).toBe(true);
        await waitFor(() => expect(screen.queryByTestId('get-started-panel')).not.toBeInTheDocument());
        await waitFor(() => expect(newTask()).toHaveClass('btn', 'primary'));
        expect(server.writes).toEqual(['profile', 'local-profile', 'project', 'plan:iteration', 'plan:team', 'plan:work', 'plan:schedule']);
    });

    it('marks Create a project not done again when the only project is deleted', async () => {
        server.identity = localIdentity({ id: 7, display_name: 'Ada Lovelace' });
        server.projects = [{ id: 40, name: 'Launch' } as Project];
        const { queryClient } = renderWorkspace();
        await panel();
        expect(doneStates()).toEqual([true, true, false, false, false, false]);
        expect(toggleOf('iteration')).toHaveAttribute('aria-expanded', 'true');

        // The project is deleted; the project pages refresh the project list after a delete.
        server.projects = [];
        await act(() => queryClient.invalidateQueries({ queryKey: ['projects'] }));

        await waitFor(() => expect(step('project')).toHaveAttribute('data-done', 'false'));
        expect(doneStates()).toEqual([true, false, false, false, false, false]);
        expect(toggleOf('project')).toHaveAttribute('aria-expanded', 'true');
        expect(toggleOf('iteration')).toHaveAttribute('aria-expanded', 'false');
    });

    it('stays dismissed in this browser only, and Help, Setup guide shows it again', async () => {
        const first = renderWorkspace();
        await panel();
        await first.user.click(screen.getByRole('button', { name: i18n.t('firstRun.dismissLabel') }));
        expect(screen.queryByTestId('get-started-panel')).not.toBeInTheDocument();
        expect(localStorage.getItem(GET_STARTED_DISMISSED_KEY)).toBe('1');
        // Dismissing is a choice of this browser: nothing is written to the workspace.
        expect(server.writes).toEqual([]);
        first.unmount();

        // The same browser, later: the panel stays hidden although setup is incomplete.
        useGetStartedVisibility.setState({ dismissed: localStorage.getItem(GET_STARTED_DISMISSED_KEY) === '1', requested: false });
        const again = renderWorkspace();
        expect(await screen.findByText(i18n.t('overview.noIterationTitle'))).toBeInTheDocument();
        expect(screen.queryByTestId('get-started-panel')).not.toBeInTheDocument();
        again.unmount();

        // Another browser has nothing stored, so the same workspace shows the panel there.
        const stored = localStorage.getItem(GET_STARTED_DISMISSED_KEY);
        localStorage.clear();
        useGetStartedVisibility.setState({ dismissed: false, requested: false });
        const other = renderWorkspace();
        await panel();
        other.unmount();
        localStorage.setItem(GET_STARTED_DISMISSED_KEY, stored!);
        useGetStartedVisibility.setState({ dismissed: true, requested: false });

        // Back in this browser, Help, Setup guide reopens it, from any page.
        const { user } = renderWorkspace('/team');
        expect(await screen.findByText('Other page')).toBeInTheDocument();
        await user.click(screen.getByRole('button', { name: i18n.t('contextHelp.openForPage', { page: i18n.t('documentTitles.team') }) }));
        const help = screen.getByRole('dialog', { name: i18n.t('contextHelp.title') });
        await user.click(within(help).getByRole('button', { name: i18n.t('contextHelp.setupGuide.open') }));
        await panel();
        expect(screen.getByTestId('location').textContent).toMatch(/^\/(\?|$)/);
        expect(localStorage.getItem(GET_STARTED_DISMISSED_KEY)).toBeNull();
        expect(toggleOf('profile')).toHaveAttribute('aria-expanded', 'true');
    });

    it('reopens from Help with every step done, and closes again', async () => {
        server.identity = localIdentity({ id: 7, display_name: 'Ada Lovelace' });
        server.projects = [{ id: 40, name: 'Launch' } as Project];
        server.iterations = [iterationFor(40)];
        server.capacityRows = 1;
        server.tasks = 2;
        server.scheduleApplied = true;
        const { user } = renderWorkspace('/?project=40&iteration=70');
        await waitFor(() => expect(newTask()).toHaveClass('btn', 'primary'));
        expect(screen.queryByTestId('get-started-panel')).not.toBeInTheDocument();

        await user.click(screen.getByRole('button', { name: i18n.t('contextHelp.openForPage', { page: i18n.t('documentTitles.overview') }) }));
        await user.click(within(screen.getByRole('dialog', { name: i18n.t('contextHelp.title') }))
            .getByRole('button', { name: i18n.t('contextHelp.setupGuide.open') }));
        expect(await panel()).toHaveTextContent(i18n.t('firstRun.allDone'));
        expect(doneStates()).toEqual([true, true, true, true, true, true]);

        await user.click(screen.getByRole('button', { name: i18n.t('firstRun.dismissLabel') }));
        expect(screen.queryByTestId('get-started-panel')).not.toBeInTheDocument();
    });

    it('leaves an empty place for a second way in, such as a sample project', async () => {
        renderWorkspace();
        const slot = within(await panel()).getByTestId('get-started-secondary-slot');
        expect(slot).toBeEmptyDOMElement();
    });
});

describe('first page of a workspace with no project', () => {
    it('opens on Overview with the panel, whatever page was requested first', async () => {
        renderWorkspace('/tasks?view=board');
        await panel();
        expect(screen.getByTestId('location').textContent).toMatch(/^\/(\?|$)/);
    });

    it('keeps the requested page once a project exists', async () => {
        server.projects = [{ id: 40, name: 'Launch' } as Project];
        const { queryClient } = renderWorkspace('/tasks');
        expect(await screen.findByText('Other page')).toBeInTheDocument();
        await waitFor(() => expect(queryClient.getQueryData(['projects'])).toHaveLength(1));
        await act(async () => { await Promise.resolve(); });
        expect(screen.getByTestId('location')).toHaveTextContent(/^\/tasks$/);
    });
});

import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { act, screen, waitFor, within } from '@testing-library/react';
import { useState } from 'react';
import type { ReactNode } from 'react';
import { Route, Routes, useLocation } from 'react-router-dom';
import { renderWithProviders } from '../../test/renderWithProviders';
import i18n from '../../i18n/i18n';
import OverviewPage from '../../pages/OverviewPage';
import { ContextHelp } from '../../components/layout/ContextHelp';
import { useScopeStore } from '../scope/scopeStore';
import { IdentityContext } from '../identity/identityContext';
import type { WorkspaceIdentity } from '../identity/identityService';
import type { Iteration, PlanCheckpoint } from '../../types/iteration';
import { iterationService } from '../../services/iterationService';
import { planningNavigationSummaryKey } from '../planningMasters/usePlanningNavigationSummary';
import type { Project } from '../../types/project';
import { FirstRunLanding } from './FirstRunLanding';
import { GET_STARTED_DISMISSED_KEY, useGetStartedVisibility } from './getStartedVisibility';
import { useSampleProject } from './sampleProjectStore';
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

beforeEach(() => {
    localStorage.clear();
    useSampleProject.setState({ manifest: null, busy: false });
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
    vi.mocked(iterationService.getPlanningReadiness).mockClear();
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
        expect(await screen.findByText(i18n.t('emptyStates.overview.iterationTitle'))).toBeInTheDocument();
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

    it('keeps a completed sample removable after dismissing and reopening Help', async () => {
        server.identity = localIdentity({ id: 7, display_name: 'Ada Lovelace' });
        server.projects = [{ id: 40, name: 'Sample project' } as Project];
        server.iterations = [iterationFor(40)];
        server.capacityRows = 1;
        server.tasks = 8;
        server.scheduleApplied = true;
        useSampleProject.setState({ manifest: { owner: 'local', complete: true,
            records: [{ kind: 'project', id: 40, name: 'Sample project' }] } });
        const { user } = renderWorkspace('/?project=40&iteration=70');
        expect(await panel()).toHaveTextContent(i18n.t('firstRun.allDone'));
        expect(screen.getByRole('button', { name: 'Remove sample data' })).toBeVisible();
        await user.click(screen.getByRole('button', { name: i18n.t('firstRun.dismissLabel') }));
        expect(screen.queryByTestId('get-started-panel')).not.toBeInTheDocument();
        await user.click(screen.getByRole('button', { name: i18n.t('contextHelp.openForPage', { page: i18n.t('documentTitles.overview') }) }));
        await user.click(within(screen.getByRole('dialog', { name: i18n.t('contextHelp.title') }))
            .getByRole('button', { name: i18n.t('contextHelp.setupGuide.open') }));
        await panel();
        expect(screen.getByRole('button', { name: 'Remove sample data' })).toBeVisible();
    });

    it('hides itself when setup reopened from Help is then completed', async () => {
        server.identity = localIdentity({ id: 7, display_name: 'Ada Lovelace' });
        server.projects = [{ id: 40, name: 'Launch' } as Project];
        server.iterations = [iterationFor(40)];
        server.capacityRows = 1;
        server.tasks = 2;
        const { user, queryClient } = renderWorkspace('/?project=40&iteration=70');
        await panel();
        await user.click(screen.getByRole('button', { name: i18n.t('firstRun.dismissLabel') }));
        expect(screen.queryByTestId('get-started-panel')).not.toBeInTheDocument();

        // Reopened while the schedule is still to build.
        await user.click(screen.getByRole('button', { name: i18n.t('contextHelp.openForPage', { page: i18n.t('documentTitles.overview') }) }));
        await user.click(within(screen.getByRole('dialog', { name: i18n.t('contextHelp.title') }))
            .getByRole('button', { name: i18n.t('contextHelp.setupGuide.open') }));
        await panel();
        expect(toggleOf('schedule')).toHaveAttribute('aria-expanded', 'true');

        // The schedule is applied: all six are done and the panel hides itself as usual.
        server.scheduleApplied = true;
        await act(() => queryClient.invalidateQueries());
        await waitFor(() => expect(screen.queryByTestId('get-started-panel')).not.toBeInTheDocument());
        await waitFor(() => expect(newTask()).toHaveClass('btn', 'primary'));
        expect(useGetStartedVisibility.getState().requested).toBe(false);
        expect(localStorage.getItem(GET_STARTED_DISMISSED_KEY)).toBeNull();
    });

    it('counts capacity, tasks and the schedule only for the iteration Plan opens', async () => {
        server.identity = localIdentity({ id: 7, display_name: 'Ada Lovelace' });
        server.projects = [{ id: 40, name: 'Launch' } as Project, { id: 41, name: 'Harbor' } as Project];
        // Launch has a fully planned iteration; Harbor has none.
        server.iterations = [iterationFor(40)];
        server.capacityRows = 1;
        server.tasks = 2;
        server.scheduleApplied = true;

        // A project without iterations: Plan opens no iteration, so steps 4 to 6 are still to do.
        const harbor = renderWorkspace('/?project=41');
        await panel();
        expect(doneStates()).toEqual([true, true, true, false, false, false]);
        expect(toggleOf('capacity')).toHaveAttribute('aria-expanded', 'true');
        harbor.unmount();

        // The backlog of the planned project: again no iteration in scope.
        const backlog = renderWorkspace('/?project=40&iteration=backlog');
        await panel();
        expect(doneStates()).toEqual([true, true, true, false, false, false]);
        backlog.unmount();
        expect(iterationService.getPlanningReadiness).not.toHaveBeenCalledWith(70);

        // The planned iteration itself: all six are done and the panel stays hidden.
        const planned = renderWorkspace('/?project=40&iteration=70');
        await waitFor(() => expect(planned.queryClient.getQueryData(planningNavigationSummaryKey(70))).toBeDefined());
        await waitFor(() => expect(newTask()).toHaveClass('btn', 'primary'));
        expect(screen.queryByTestId('get-started-panel')).not.toBeInTheDocument();
    });

    it('offers a sample project as a second way in', async () => {
        renderWorkspace();
        const slot = within(await panel()).getByTestId('get-started-secondary-slot');
        expect(within(slot).getByRole('button', { name: 'Load a sample project' })).toBeInTheDocument();
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

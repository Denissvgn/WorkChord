import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { useEffect } from 'react';
import { createMemoryRouter, RouterProvider, useLocation } from 'react-router-dom';
import { QueryClientProvider } from '@tanstack/react-query';
import { render } from '@testing-library/react';
import { createTestQueryClient } from '../../test/renderWithProviders';
import { DraftDismissalDialog } from '../../components/tasks/DraftDismissalDialog';
import { useDraftDismissal } from '../../components/tasks/useDraftDismissal';
import userEvent from '@testing-library/user-event';
import { act, cleanup, screen, waitFor, within } from '@testing-library/react';
import { renderWithProviders as renderTestProviders } from '../../test/renderWithProviders';
import { IdentityContext } from '../identity/identityContext';
import type { WorkspaceIdentity } from '../identity/identityService';
import api from '../../services/api';
import { iterationService } from '../../services/iterationService';
import { loadSampleProject, removeSampleProject, type SampleManifest } from './sampleProject';
import { sampleProjectFixture } from './sampleProject.fixture';
import { SampleProjectAction } from './SampleProjectAction';
import { useSampleProject } from './sampleProjectStore';
import { changeAppLanguage } from '../../i18n/i18n';
import { RoadmapView } from '../../components/projects/RoadmapView';
import type { Project } from '../../types/project';
import { formatDate } from '../../utils/formatDate';
import { useScopeStore } from '../scope/scopeStore';
import { useWorkScope } from '../scope/useWorkScope';
import { useFirstRunProgress } from './useFirstRunProgress';
import { GetStartedPanel } from './GetStartedPanel';

vi.mock('../../services/api', () => ({ default: { get: vi.fn(), post: vi.fn(), put: vi.fn(), delete: vi.fn() } }));
vi.mock('../../hooks/useAdminAccess', () => ({ useAdminAccess: () => ({ hasAdminAccess: false }) }));
type Row = { id: number; name?: string; title?: string; [key: string]: unknown };
let rows: Map<string, Row>;
let nextId: number;
let revision: number;
let writes: string[];
let applied: boolean;
let failIteration: boolean;
const person = { id: 1, display_name: 'Robin' };
const identity: WorkspaceIdentity = { mode: 'trusted_local', principal: null, profile: person, access: 'full',
    authenticated: false, configured: true, workspace_role: null, projects: {}, csrf_token: null };
const record = (kind: string, data: Record<string, unknown>) => {
    const row = { id: nextId++, ...data };
    rows.set(`${kind}:${row.id}`, row);
    return row;
};
const list = (kind: string) => [...rows.entries()].filter(([key]) => key.startsWith(`${kind}:`)).map(([, row]) => row);
const read = (kind: string, id: number) => {
    const row = rows.get(`${kind}:${id}`);
    if (!row) throw { response: { status: 404 } };
    return row;
};
const readiness = (iterationId: number) => {
    const tasks = list('task').filter(row => row.iteration_id === iterationId);
    const members = list('member').filter(row => row.iteration_id === iterationId);
    const scheduled = Boolean(read('iteration', iterationId).scheduled) || applied;
    const states = [list('iteration').length > 0, members.length === 2, tasks.length === 8,
        tasks.length === 8 && tasks.every(task => task.assignee_id && Number(task.effort_hours) > 0), scheduled, scheduled];
    return { team_member_count: members.length, task_count: tasks.length, checkpoints_done: states.filter(Boolean).length,
        checkpoints: states.map((done, i) => ({ id: ['iteration', 'team', 'work', 'blockers', 'schedule', 'review'][i], state: done ? 'done' : 'todo' })) };
};
const fresh = (): SampleManifest => ({ owner: 'local', records: [], complete: false });
const queryClients = new Set<ReturnType<typeof renderTestProviders>['queryClient']>();
const renderWithProviders = (...args: Parameters<typeof renderTestProviders>) => {
    const result = renderTestProviders(...args);
    queryClients.add(result.queryClient);
    return result;
};
const Location = () => { const location = useLocation(); return <output data-testid="location">{location.pathname}{location.search}</output>; };
const renderAction = (value = identity) => renderWithProviders(<IdentityContext.Provider value={{ identity: value, refresh: vi.fn(), signOut: vi.fn() }}><SampleProjectAction /><Location /></IdentityContext.Provider>);
const WorkspaceSetup = () => {
    const progress = useFirstRunProgress();
    const { scope, setScope } = useWorkScope();
    return <><output data-testid="scope">{JSON.stringify(scope)}</output>
        <button onClick={() => setScope({ project: 'all', iteration: scope?.iteration })}>All projects</button>
        {progress.known && <GetStartedPanel progress={progress} />}<Location /></>;
};

beforeEach(async () => {
    vi.resetAllMocks();
    await changeAppLanguage('en');
    rows = new Map(); nextId = 10; revision = 1; writes = []; applied = false; failIteration = false;
    localStorage.clear();
    sessionStorage.clear();
    useSampleProject.setState({ manifest: null, busy: false });
    useScopeStore.setState({ project: null, iteration: null });
    rows.set('profile:1', person);
    vi.mocked(api.post).mockImplementation(async (url, body) => {
        const path = String(url); const data = (body ?? {}) as Record<string, unknown>;
        writes.push(path);
        if (path.endsWith('/context')) return { data: { kind: 'member', resource_id: Number(path.split('/')[4]), resource: { id: Number(path.split('/')[4]) }, complete: true, expected_revisions: { [list('iteration')[0].id]: revision } } };
        if (path === '/projects') return { data: record('project', data) };
        if (/^\/projects\/\d+\/milestones$/.test(path)) return { data: record('milestone', { ...data, project_id: Number(path.split('/')[2]) }) };
        if (path === '/iterations') {
            if (failIteration) throw new Error('offline');
            return { data: record('iteration', { ...data, revision }) };
        }
        if (path === '/team-member-profiles') return { data: record('profile', data) };
        if (path.endsWith('/team')) { revision++; return { data: record('member', { ...data, name: read('profile', Number(data.profile_id)).display_name ?? person.display_name, iteration_id: Number(path.split('/')[2]) }) }; }
        if (path.endsWith('/tasks')) {
            expect(data.expected_revision).toBe(revision);
            expect((data.depends_on as number[]).every(id => rows.has(`task:${id}`))).toBe(true);
            revision++;
            return { data: record('task', { ...data, iteration_id: Number(path.split('/')[2]), version: 1 }) };
        }
        if (path.endsWith('/schedule/preview')) return { data: { input_revision: revision, input_planning_revision: 5, tasks: [] } };
        if (path.endsWith('/schedule')) {
            expect(data).toEqual({ expected_revision: revision, expected_planning_revision: 5 });
            const iteration = read('iteration', Number(path.split('/')[2]));
            for (const member of list('member').filter(row => row.iteration_id === iteration.id)) {
                const overlapping = list('member').filter(row => row.profile_id === member.profile_id).filter(row => {
                    const other = read('iteration', Number(row.iteration_id));
                    return String(other.start_date) <= String(iteration.end_date) && String(other.end_date) >= String(iteration.start_date);
                });
                if (overlapping.reduce((sum, row) => sum + Number(row.availability_percent), 0) > 100) {
                    throw new Error('shared_capacity_overallocated');
                }
            }
            applied = true; revision++; return { data: { success: true } };
        }
        throw new Error(`Unexpected POST ${path}`);
    });
    vi.mocked(api.get).mockImplementation(async (url, config) => {
        const path = String(url); const parts = path.split('/'); const id = Number(parts[2]);
        if (path === '/projects/page' || path === '/iterations/page') return { data: {
            items: list(path === '/projects/page' ? 'project' : 'iteration'), has_more: false, next_after_id: null, upper_id: nextId,
        } };
        if (/^\/team-member-profiles\/\d+\/capacity$/.test(path)) {
            const days = [];
            const params = config?.params as { start: string; end: string };
            const start = new Date(`${params.start}T12:00:00Z`);
            const end = new Date(`${params.end}T12:00:00Z`);
            for (const day = new Date(start); day <= end; day.setUTCDate(day.getUTCDate() + 1)) {
                const date = day.toISOString().slice(0, 10);
                const allocated = list('member').filter(row => row.profile_id === id).some(row => {
                    const iteration = read('iteration', Number(row.iteration_id));
                    return String(iteration.start_date) <= date && String(iteration.end_date) >= date;
                });
                days.push({ date, allocated_hours: allocated ? 8 : 0, committed_effort_hours: 0 });
            }
            return { data: { calendar_year: null, days } };
        }
        if (path.includes('/planning-inputs/')) {
            const kind = parts[3]; const resourceId = Number(parts[4]);
            return { data: { kind, resource_id: resourceId, resource: read(kind, resourceId), complete: true,
                expected_revisions: kind === 'profile' ? {} : Object.fromEntries(list('iteration').map(row => [row.id, revision])) } };
        }
        if (path === '/roadmap/milestones') return { data: { items: list('milestone').map(row => ({ status: 'planned', sort_order: 0, ...row })), next_cursor: null } };
        if (path.endsWith('/planning-readiness')) return { data: readiness(id) };
        if (/^\/iterations\/\d+$/.test(path)) return { data: { ...read('iteration', id), revision, nominal_day_hours: 8 } };
        if (path.endsWith('/detail')) return { data: { task: read('task', id), children: { items: list('task').filter(row => row.parent_id === id), has_more: false } } };
        if (path.endsWith('/workload')) return { data: { allocated_days: 0 } };
        if (path.endsWith('/team')) return { data: list('member').filter(row => row.iteration_id === id) };
        if (path.endsWith('/tasks')) return { data: list('task').filter(row => parts[1] === 'projects' ? row.project_id === id : row.iteration_id === id).map(row => ({ ...row, assignee: row.assignee_id ? { id: row.assignee_id } : null })) };
        if (path.endsWith('/iterations')) return { data: list('iteration').filter(row => row.project_id === id) };
        if (path.endsWith('/milestones')) return { data: list('milestone').filter(row => row.project_id === id) };
        throw new Error(`Unexpected GET ${path}`);
    });
    vi.mocked(api.put).mockImplementation(async (url, data) => {
        const row = read('member', Number(String(url).split('/')[2])); Object.assign(row, data); revision++;
        return { data: row };
    });
    vi.mocked(api.delete).mockImplementation(async (url, config) => {
        const parts = String(url).split('/'); const id = Number(parts.at(-1));
        const kind = ({ tasks: 'task', 'team-members': 'member', 'team-member-profiles': 'profile', iterations: 'iteration', projects: parts.length > 3 ? 'milestone' : 'project' } as Record<string, string>)[parts[1]];
        read(kind, id);
        if (kind === 'task') expect(config?.params).toEqual({ expected_version: 1, expected_revision: revision });
        rows.delete(`${kind}:${id}`); revision++;
        if (kind === 'iteration') applied = false;
        return { data: { success: true } };
    });
});

afterEach(() => {
    cleanup();
    for (const client of queryClients) client.clear();
    queryClients.clear();
    useSampleProject.setState({ manifest: null, busy: false });
    useScopeStore.setState({ project: null, iteration: null });
    localStorage.clear();
    sessionStorage.clear();
});

const OpenDraft = ({ mode }: { mode: 'dirty' | 'pending' }) => {
    const guard = useDraftDismissal(() => undefined);
    useEffect(() => {
        if (mode === 'dirty') guard.setDirty(true); else guard.setPending(true);
    }, [guard, mode]);
    return <DraftDismissalDialog guard={guard} />;
};
/** The app's router, with a task draft open that would normally ask before leaving the page. */
const renderInDataRouter = (entry: string, mode: 'dirty' | 'pending') => {
    const queryClient = createTestQueryClient();
    queryClients.add(queryClient);
    const router = createMemoryRouter([{ path: '*', element: <IdentityContext.Provider value={{ identity, refresh: vi.fn(), signOut: vi.fn() }}>
        <SampleProjectAction /><OpenDraft mode={mode} /><Location /></IdentityContext.Provider> }], { initialEntries: [entry] });
    render(<QueryClientProvider client={queryClient}><RouterProvider router={router} /></QueryClientProvider>);
    return { router, queryClient };
};
/** Collects every uncaught error and console error until stop() is called. */
const watchForErrors = () => {
    const errors: string[] = [];
    const onError = (event: ErrorEvent) => { errors.push(String(event.error ?? event.message)); event.preventDefault(); };
    const onRejection = (event: PromiseRejectionEvent) => { errors.push(String(event.reason)); event.preventDefault(); };
    window.addEventListener('error', onError);
    window.addEventListener('unhandledrejection', onRejection);
    const consoleError = vi.spyOn(console, 'error').mockImplementation((...args) => { errors.push(args.map(String).join(' ')); });
    return { errors, stop: () => {
        window.removeEventListener('error', onError);
        window.removeEventListener('unhandledrejection', onRejection);
        consoleError.mockRestore();
    } };
};

describe('sample project lifecycle', () => {
    it.each(['dirty', 'pending'] as const)('logs no uncaught error and opens the plan without asking when the sample loads over a %s draft', async mode => {
        const watch = watchForErrors();
        try {
            renderInDataRouter('/overview', mode);
            await userEvent.setup().click(await screen.findByRole('button', { name: 'Load a sample project' }));
            await waitFor(() => expect(screen.getByTestId('location')).toHaveTextContent('/plan?project='));
            await act(() => new Promise(resolve => setTimeout(resolve, 50)));
            expect(screen.queryByRole('dialog')).toBeNull();
            expect(watch.errors).toEqual([]);
        } finally { watch.stop(); }
    });

    it('logs no uncaught error when a draft is discarded to leave the page', async () => {
        const watch = watchForErrors();
        try {
            const { router } = renderInDataRouter('/overview', 'dirty');
            const user = userEvent.setup();
            await act(async () => { void router.navigate('/elsewhere'); });
            await user.click(await screen.findByRole('button', { name: /discard/i }));
            await waitFor(() => expect(screen.getByTestId('location')).toHaveTextContent('/elsewhere'));
            await act(() => new Promise(resolve => setTimeout(resolve, 50)));
            expect(watch.errors).toEqual([]);
        } finally { watch.stop(); }
    });

    it('loads a dated Roadmap project, two milestones and an applied iteration at 6 of 6', async () => {
        const receipt = fresh();
        const result = await loadSampleProject(receipt, person, 'en', vi.fn());
        expect(writes.slice(0, 4)).toEqual(['/projects', '/projects/10/milestones', '/projects/10/milestones', '/iterations']);
        const project = read('project', result.projectId);
        expect(project.start_date).toMatch(/^\d{4}-\d{2}-\d{2}$/);
        expect(String(project.target_date) > String(project.start_date)).toBe(true);
        expect(list('milestone')).toHaveLength(2);
        expect(list('member').map(row => row.profile_id)).toEqual([1, list('profile').find(row => row.id !== 1)!.id]);
        expect(list('profile').find(row => row.display_name === 'Sample agent')).toMatchObject({ profile_kind: 'agent', automation_enabled: false });
        expect(list('task')).toHaveLength(8);
        for (const task of list('task')) expect(task).toMatchObject({ tags: ['sample'], effort_hours: 2, brief: { schema_version: 1 } });
        expect(list('task').every(task => task.assignee_id && task.milestone_id)).toBe(true);
        expect(list('task').filter(task => (task.depends_on as number[]).length)).toHaveLength(6);
        expect(receipt.records.every(row => row.name.includes('Sample'))).toBe(true);
        expect((await iterationService.getPlanningReadiness(result.iterationId)).checkpoints_done).toBe(6);
        expect(receipt.complete).toBe(true);
        renderWithProviders(<RoadmapView projects={[project as unknown as Project]} initiatives={[]}
            includeEmptyGroups window={{ from: '', to: '' }} onResetWindow={vi.fn()}
            onEditInitiative={vi.fn()} onDeleteInitiative={vi.fn()} />);
        expect(await screen.findByRole('link', { name: String(project.name) })).toBeVisible();
        expect(screen.getByText(`Scheduled from ${formatDate(String(project.start_date))} to ${formatDate(String(project.target_date))}`)).toBeVisible();
        for (const milestone of list('milestone')) {
            expect(await screen.findByRole('button', { name: new RegExp(`^${milestone.name},`) })).toBeVisible();
        }
    });

    it('opens the created plan after one load action', async () => {
        const { user } = renderAction();
        await user.click(screen.getByRole('button', { name: 'Load a sample project' }));
        await waitFor(() => expect(screen.getByTestId('location')).toHaveTextContent(`/plan?project=${list('project')[0]?.id}&iteration=${list('iteration')[0]?.id}`));
        expect(readiness(list('iteration')[0].id).checkpoints_done).toBe(6);
    });

    it.each(['complete', 'partial', 'missing prior scope', 'All projects with sample iteration', 'scope repair during restoration', 'navigation during restoration'] as const)(
        'restores workspace setup after sample removal with %s', async mode => {
            const project = record('project', { name: 'Workspace project' });
            const iteration = record('iteration', { name: 'Workspace iteration', project_id: project.id,
                start_date: '2026-01-01', end_date: '2026-01-30', scheduled: true });
            const member = record('member', { name: person.display_name, profile_id: person.id, iteration_id: iteration.id });
            record('task', { title: 'Workspace task', project_id: project.id, iteration_id: iteration.id,
                assignee_id: member.id, effort_hours: 2 });
            const { user, queryClient } = renderWithProviders(<IdentityContext.Provider value={{ identity, refresh: vi.fn(), signOut: vi.fn() }}>
                <WorkspaceSetup />
            </IdentityContext.Provider>, { initialEntries: [`/overview?project=${project.id}&iteration=${iteration.id}`] });
            await screen.findByTestId('get-started-panel');
            for (const step of ['profile', 'project', 'iteration', 'capacity', 'tasks', 'schedule']) {
                expect(screen.getByTestId(`get-started-step-${step}`)).toHaveAttribute('data-done', 'true');
            }
            await user.click(screen.getByRole('button', { name: 'Load a sample project' }));
            await waitFor(() => {
                expect(useSampleProject.getState().manifest?.complete).toBe(true);
                expect(useSampleProject.getState().busy).toBe(false);
            });
            const sampleProjectId = useSampleProject.getState().manifest!.records.find(row => row.kind === 'project')!.id;
            const sampleIteration = list('iteration').find(row => row.id !== iteration.id)!;
            await waitFor(() => {
                expect(screen.getByTestId('location')).toHaveTextContent(`/plan?project=${sampleProjectId}&iteration=${sampleIteration.id}`);
                expect(useScopeStore.getState()).toMatchObject({ project: sampleProjectId, iteration: sampleIteration.id });
            });
            expect(useSampleProject.getState().manifest?.previousScope).toEqual({ project: project.id, iteration: iteration.id });
            expect(JSON.parse(localStorage.getItem('workchord-sample-project')!).previousScope).toEqual({ project: project.id, iteration: iteration.id });
            if (mode === 'missing prior scope') {
                rows.delete(`project:${project.id}`);
                rows.delete(`iteration:${iteration.id}`);
            }
            if (mode === 'All projects with sample iteration') await user.click(screen.getByRole('button', { name: 'All projects' }));
            if (mode === 'partial') {
                const originalDelete = vi.mocked(api.delete).getMockImplementation()!;
                vi.mocked(api.delete).mockImplementation(async (...args) => {
                    if (String(args[0]).includes('/milestones/')) throw new Error('offline');
                    return originalDelete(...args);
                });
            }
            let releaseLookup: (() => void) | undefined;
            let lookupPending = false;
            if (mode === 'scope repair during restoration' || mode === 'navigation during restoration') {
                const gate = new Promise<void>(resolve => { releaseLookup = resolve; });
                const originalGet = vi.mocked(api.get).getMockImplementation()!;
                vi.mocked(api.get).mockImplementation(async (...args) => {
                    if (args[0] === '/projects/page' && !rows.has(`project:${sampleProjectId}`)) {
                        lookupPending = true;
                        await gate;
                    }
                    return originalGet(...args);
                });
            }
            await user.click(screen.getByRole('button', { name: 'Remove sample data' }));
            await user.click(within(screen.getByRole('dialog')).getByRole('button', { name: 'Remove sample data' }));
            if (releaseLookup) {
                await waitFor(() => expect(lookupPending).toBe(true));
                act(() => { queryClient.setQueryData(['iterations'], list('iteration')); });
                await waitFor(() => expect(useScopeStore.getState()).toMatchObject({ project: sampleProjectId, iteration: 'backlog' }));
                if (mode === 'navigation during restoration') await user.click(screen.getByRole('button', { name: 'All projects' }));
                await act(async () => { releaseLookup!(); });
            }
            const restored = mode === 'missing prior scope' || mode === 'navigation during restoration' ? { project: 'all', iteration: 'backlog' }
                : { project: project.id, iteration: iteration.id };
            await waitFor(() => {
                expect(useSampleProject.getState().busy).toBe(false);
                expect(screen.getByTestId('scope')).toHaveTextContent(JSON.stringify(restored));
                expect(screen.getByTestId('location')).toHaveTextContent(`project=${restored.project}&iteration=${restored.iteration}`);
                expect(useScopeStore.getState()).toMatchObject(restored);
            });
            expect(rows.has(`iteration:${sampleIteration.id}`)).toBe(false);
            if (mode !== 'missing prior scope' && mode !== 'navigation during restoration') {
                await waitFor(() => {
                    for (const step of ['profile', 'project', 'iteration', 'capacity', 'tasks', 'schedule']) {
                        expect(screen.getByTestId(`get-started-step-${step}`)).toHaveAttribute('data-done', 'true');
                    }
                });
            }
            if (mode === 'partial') {
                expect(await within(screen.getByRole('dialog')).findByText(/Removal stopped/)).toBeVisible();
                expect(rows.has(`project:${sampleProjectId}`)).toBe(true);
            } else expect(rows.has(`project:${sampleProjectId}`)).toBe(false);
        },
    );

    it('moves the scope off the deleted project before anything refetches or the result is shown', async () => {
        const project = record('project', { name: 'Workspace project' });
        const iteration = record('iteration', { name: 'Workspace iteration', project_id: project.id,
            start_date: '2026-01-01', end_date: '2026-01-30', scheduled: true });
        const { user, queryClient } = renderWithProviders(<IdentityContext.Provider value={{ identity, refresh: vi.fn(), signOut: vi.fn() }}>
            <WorkspaceSetup />
        </IdentityContext.Provider>, { initialEntries: [`/overview?project=${project.id}&iteration=${iteration.id}`] });
        await screen.findByTestId('get-started-panel');
        await user.click(screen.getByRole('button', { name: 'Load a sample project' }));
        await waitFor(() => expect(useSampleProject.getState().manifest?.complete).toBe(true));
        const sampleProjectId = useSampleProject.getState().manifest!.records.find(row => row.kind === 'project')!.id;
        const sampleIterationId = useSampleProject.getState().manifest!.records.find(row => row.kind === 'iteration')!.id;
        await waitFor(() => expect(screen.getByTestId('location')).toHaveTextContent(`project=${sampleProjectId}&iteration=${sampleIterationId}`));
        await waitFor(() => expect(useSampleProject.getState().busy).toBe(false));
        // Everything that refetches after a deletion must already find the scope off the deleted records.
        const namingDeleted: string[] = [];
        const original = queryClient.invalidateQueries.bind(queryClient);
        vi.spyOn(queryClient, 'invalidateQueries').mockImplementation((...args) => {
            if (!rows.has(`project:${sampleProjectId}`)) {
                const { project: p, iteration: i } = useScopeStore.getState();
                if (p === sampleProjectId || i === sampleIterationId) namingDeleted.push(`${p}/${i}`);
            }
            return original(...args);
        });
        await user.click(screen.getByRole('button', { name: 'Remove sample data' }));
        await user.click(within(screen.getByRole('dialog')).getByRole('button', { name: 'Remove sample data' }));
        await waitFor(() => expect(useSampleProject.getState().busy).toBe(false));
        expect(rows.has(`project:${sampleProjectId}`)).toBe(false);
        expect(namingDeleted).toEqual([]);
        expect(screen.getByTestId('scope')).toHaveTextContent(JSON.stringify({ project: project.id, iteration: iteration.id }));
        expect(screen.getByTestId('location')).toHaveTextContent(`project=${project.id}&iteration=${iteration.id}`);
    });

    it('applies a schedule at 6 of 6 when the person already has overlapping 100% capacity', async () => {
        const original = sampleProjectFixture('en');
        const existing = record('iteration', { name: 'Existing iteration', start_date: original.start, end_date: original.end });
        record('member', { name: person.display_name, profile_id: person.id, iteration_id: existing.id, availability_percent: 100 });
        const before = structuredClone(rows);
        const receipt = fresh();
        const result = await loadSampleProject(receipt, person, 'en', vi.fn());
        const iteration = read('iteration', result.iterationId);
        expect(String(iteration.start_date) > original.end).toBe(true);
        expect(read('project', result.projectId)).toMatchObject({ start_date: iteration.start_date, target_date: iteration.end_date });
        expect(list('milestone').every(row => String(row.target_date) >= String(iteration.start_date)
            && String(row.target_date) <= String(iteration.end_date))).toBe(true);
        expect(applied).toBe(true);
        expect((await iterationService.getPlanningReadiness(result.iterationId)).checkpoints_done).toBe(6);
        expect(receipt.complete).toBe(true);
        for (const [key, row] of before) expect(rows.get(key)).toEqual(row);
        await removeSampleProject(receipt, vi.fn());
        expect(rows).toEqual(before);
    });

    it('removes exactly the created records, preserving existing data and the current person', async () => {
        const existing = record('project', { name: 'Existing project' });
        const existingTask = record('task', { title: 'Existing task', project_id: existing.id, version: 1 });
        const existingProfile = record('profile', { display_name: 'Sample agent' });
        const before = new Map(rows);
        const receipt = fresh(); const save = vi.fn();
        await loadSampleProject(receipt, person, 'en', save);
        const createdIds = receipt.records.map(row => row.id).sort((a, b) => a - b);
        await removeSampleProject(receipt, save);
        expect(rows).toEqual(before);
        expect(rows.get(`task:${existingTask.id}`)).toEqual(existingTask);
        expect(rows.get(`profile:${existingProfile.id}`)).toEqual(existingProfile);
        expect(vi.mocked(api.delete).mock.calls.map(([url]) => Number(String(url).split('/').at(-1))).sort((a, b) => a - b)).toEqual(createdIds);
        expect(receipt.records).toEqual([]);
    });

    it('lists what exists after the third call and offers a working confirmed Remove', async () => {
        failIteration = true;
        const { user } = renderAction();
        await user.click(screen.getByRole('button', { name: 'Load a sample project' }));
        await screen.findByRole('alert');
        expect(writes).toEqual(['/projects', '/projects/10/milestones', '/projects/10/milestones', '/iterations']);
        expect(screen.getByText('Created records (3)')).toBeInTheDocument();
        expect(screen.getByText(/Project: Sample welcome guide/)).toBeVisible();
        expect(screen.getByText(/Milestone: Sample draft ready/)).toBeVisible();
        expect(screen.getByText(/Milestone: Sample guide published/)).toBeVisible();
        await user.click(screen.getByRole('button', { name: 'Remove sample data' }));
        const dialog = screen.getByRole('dialog');
        expect(within(dialog).getByText(/Project: Sample welcome guide/)).toBeVisible();
        expect(within(dialog).queryByText(/Removal stopped/)).not.toBeInTheDocument();
        expect(api.delete).not.toHaveBeenCalled();
        await user.click(within(dialog).getByRole('button', { name: 'Remove sample data' }));
        await waitFor(() => expect(list('project')).toHaveLength(0));
        expect(list('milestone')).toHaveLength(0);
        expect(rows.get('profile:1')).toEqual(person);
        expect(await screen.findByRole('button', { name: 'Load a sample project' })).toBeEnabled();
    });

    it('shows the removal failure warning only after removal fails and supports retry', async () => {
        failIteration = true;
        const { user } = renderAction();
        await user.click(screen.getByRole('button', { name: 'Load a sample project' }));
        await screen.findByRole('alert');
        await user.click(screen.getByRole('button', { name: 'Remove sample data' }));
        const dialog = screen.getByRole('dialog');
        expect(within(dialog).queryByText(/Removal stopped/)).not.toBeInTheDocument();
        vi.mocked(api.delete).mockRejectedValueOnce(new Error('offline'));
        await user.click(within(dialog).getByRole('button', { name: 'Remove sample data' }));
        expect(await within(dialog).findByText(/Removal stopped/)).toBeVisible();
        expect(list('project')).toHaveLength(1);
        expect(list('milestone')).toHaveLength(2);
        await user.click(within(dialog).getByRole('button', { name: 'Remove sample data' }));
        expect(await screen.findByRole('button', { name: 'Load a sample project' })).toBeEnabled();
        expect(rows.size).toBe(1);
    });

    it('keeps a deletion receipt and retries removal after a partial deletion failure', async () => {
        const receipt = fresh(); await loadSampleProject(receipt, person, 'en', vi.fn());
        vi.mocked(api.delete).mockRejectedValueOnce(new Error('offline'));
        const count = receipt.records.length;
        await expect(removeSampleProject(receipt, vi.fn())).rejects.toThrow('offline');
        expect(receipt.records).toHaveLength(count);
        await removeSampleProject(receipt, vi.fn());
        expect(rows.size).toBe(1);
    });

    it('refuses to cascade-delete added work in the sample iteration', async () => {
        const receipt = fresh(); const { iterationId, projectId } = await loadSampleProject(receipt, person, 'en', vi.fn());
        const added = record('task', { title: 'Keep this task', project_id: projectId, iteration_id: iterationId });
        await expect(removeSampleProject(receipt, vi.fn())).rejects.toThrow('additional work');
        expect(rows.get(`task:${added.id}`)).toEqual(added);
        expect(rows.has(`iteration:${iterationId}`)).toBe(true);
    });

    it('preserves an added child instead of cascading its sample parent deletion', async () => {
        const receipt = fresh(); const { iterationId, projectId } = await loadSampleProject(receipt, person, 'en', vi.fn());
        const parent = list('task').at(-1)!;
        const added = record('task', { title: 'Keep child', parent_id: parent.id, project_id: projectId, iteration_id: iterationId });
        await expect(removeSampleProject(receipt, vi.fn())).rejects.toThrow('additional work');
        expect(rows.has(`task:${parent.id}`)).toBe(true);
        expect(rows.get(`task:${added.id}`)).toEqual(added);
        expect(api.delete).not.toHaveBeenCalled();
    });

    it('preserves sample capacity used by added work even with zero allocated effort', async () => {
        const receipt = fresh(); const { iterationId, projectId } = await loadSampleProject(receipt, person, 'en', vi.fn());
        const member = list('member').at(-1)!;
        const added = record('task', { title: 'Keep assignment', assignee_id: member.id, project_id: projectId, iteration_id: iterationId });
        await expect(removeSampleProject(receipt, vi.fn())).rejects.toThrow('additional work');
        expect(rows.has(`member:${member.id}`)).toBe(true);
        expect(rows.get(`task:${added.id}`)).toEqual(added);
    });

    it('persists each returned create and completed deletion in browser storage', async () => {
        const receipt = fresh();
        const save = vi.fn((value: SampleManifest) => {
            useSampleProject.getState().save(value);
            expect(JSON.parse(localStorage.getItem('workchord-sample-project')!)).toEqual(value);
        });
        await loadSampleProject(receipt, person, 'en', save);
        const count = receipt.records.length;
        expect(save.mock.calls.length).toBeGreaterThanOrEqual(count);
        save.mockClear();
        await removeSampleProject(receipt, save);
        expect(save).toHaveBeenCalledTimes(count);
        expect(JSON.parse(localStorage.getItem('workchord-sample-project')!).records).toEqual([]);
    });

    it('hides sample writes from observers and managed members without workspace editing authority', () => {
        const { unmount } = renderAction({ ...identity, access: 'observe' });
        expect(screen.queryByRole('button', { name: 'Load a sample project' })).not.toBeInTheDocument();
        unmount();
        renderAction({ ...identity, mode: 'managed', authenticated: true, principal: { id: 2, kind: 'human', display_name: 'Robin' }, workspace_role: 'member' });
        expect(screen.queryByRole('button', { name: 'Load a sample project' })).not.toBeInTheDocument();
        expect(api.post).not.toHaveBeenCalled();
    });

    it('does not load until a person is chosen and refuses writes without receipt storage', async () => {
        const { user, unmount } = renderAction({ ...identity, profile: null });
        expect(screen.getByRole('button', { name: 'Load a sample project' })).toBeDisabled();
        unmount(); renderAction();
        const storage = vi.spyOn(Storage.prototype, 'setItem').mockImplementation(() => { throw new Error('blocked'); });
        await user.click(screen.getByRole('button', { name: 'Load a sample project' }));
        await screen.findByRole('alert');
        expect(api.post).not.toHaveBeenCalled(); storage.mockRestore();
    });

    it('provides the same complete fixture in Russian and retains Sample names', async () => {
        const fixture = sampleProjectFixture('ru');
        expect(fixture.tasks).toHaveLength(8);
        expect(fixture.tasks[0].brief.scope).toMatch(/Опишите/);
        expect(fixture.tasks.every(task => task.title.startsWith('Sample:'))).toBe(true);
        await changeAppLanguage('ru'); renderAction();
        expect(screen.getByRole('button', { name: 'Загрузить пример проекта' })).toBeEnabled();
    });
});

import { beforeEach, describe, expect, it, vi } from 'vitest';
import { useLocation } from 'react-router-dom';
import { screen, waitFor, within } from '@testing-library/react';
import { renderWithProviders } from '../../test/renderWithProviders';
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
    const states = [list('iteration').length > 0, members.length === 2, tasks.length === 8,
        tasks.length === 8 && tasks.every(task => task.assignee_id && Number(task.effort_hours) > 0), applied, applied];
    return { checkpoints_done: states.filter(Boolean).length, checkpoints: states.map((done, i) => ({ id: ['iteration', 'team', 'work', 'blockers', 'schedule', 'review'][i], state: done ? 'done' : 'todo' })) };
};
const fresh = (): SampleManifest => ({ owner: 'local', records: [], complete: false });
const Location = () => { const location = useLocation(); return <output data-testid="location">{location.pathname}{location.search}</output>; };
const renderAction = (value = identity) => renderWithProviders(<IdentityContext.Provider value={{ identity: value, refresh: vi.fn(), signOut: vi.fn() }}><SampleProjectAction /><Location /></IdentityContext.Provider>);

beforeEach(async () => {
    vi.resetAllMocks();
    await changeAppLanguage('en');
    rows = new Map(); nextId = 10; revision = 1; writes = []; applied = false; failIteration = false;
    localStorage.clear();
    useSampleProject.setState({ manifest: null, busy: false });
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
            applied = true; revision++; return { data: { success: true } };
        }
        throw new Error(`Unexpected POST ${path}`);
    });
    vi.mocked(api.get).mockImplementation(async url => {
        const path = String(url); const parts = path.split('/'); const id = Number(parts[2]);
        if (path.includes('/planning-inputs/')) {
            const kind = parts[3]; const resourceId = Number(parts[4]);
            return { data: { kind, resource_id: resourceId, resource: read(kind, resourceId), complete: true,
                expected_revisions: kind === 'profile' ? {} : list('iteration').length ? { [list('iteration')[0].id]: revision } : {} } };
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

describe('sample project lifecycle', () => {
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
        expect(api.delete).not.toHaveBeenCalled();
        await user.click(within(dialog).getByRole('button', { name: 'Remove sample data' }));
        await waitFor(() => expect(list('project')).toHaveLength(0));
        expect(list('milestone')).toHaveLength(0);
        expect(rows.get('profile:1')).toEqual(person);
        expect(await screen.findByRole('button', { name: 'Load a sample project' })).toBeEnabled();
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

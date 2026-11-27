import { beforeEach, describe, expect, it, vi } from 'vitest';
import { screen, waitFor, within } from '@testing-library/react';
import { renderWithProviders } from '../../test/renderWithProviders';
import { TaskForm } from './TaskForm';
import type { Task } from '../../types/task';

const api = vi.hoisted(() => ({ get: vi.fn(), post: vi.fn(), put: vi.fn() }));
vi.mock('../../services/api', () => ({ default: api }));
vi.mock('./TaskWorkPanel', () => ({ TaskWorkPanel: () => null }));
vi.mock('./DeliveryDependencies', () => ({ DeliveryDependencies: () => null }));
vi.mock('./GitHubReconciliationPanel', () => ({ GitHubReconciliationPanel: () => null }));
vi.mock('./TaskDiscussion', () => ({ TaskDiscussion: () => null }));
vi.mock('./TimeEntriesPanel', () => ({ TimeEntriesPanel: () => null }));
vi.mock('./TaskTimelinePanel', () => ({ TaskTimelinePanel: () => null }));
const iteration = { id: 2, name: 'November', revision: 3, nominal_day_hours: 8, project_id: 1, project: { id: 1, name: 'Calendar' } };
const profile = { id: 9, display_name: 'Builder', profile_kind: 'agent' };
const person = { id: 7, name: 'Sam', profile_id: 8, profile: { profile_kind: 'human' } };
const added = { id: 10, name: 'Builder', profile_id: 9, profile: { profile_kind: 'agent' } };
let members: typeof person[];
let revision: number;

beforeEach(() => {
    members = [person]; revision = 3;
    api.get.mockReset(); api.post.mockReset(); api.put.mockReset();
    api.put.mockResolvedValue({ data: { id: 101, title: 'Import holidays' } });
    api.get.mockImplementation(async (path: string) => {
        if (path === '/iterations/2') return { data: iteration };
        if (path === '/iterations/2/team') return { data: members };
        if (path === '/team-member-profiles') return { data: [profile] };
        if (path.endsWith('/workload')) return { data: { workload_percent: 40 } };
        if (path === '/tasks/planning-inputs/iteration/2/context') return { data: { kind: 'iteration', resource_id: 2, resource: iteration, complete: true, expected_revisions: { 2: revision } } };
        if (path === '/projects/page') return { data: { items: [iteration.project], has_more: false, upper_id: 1 } };
        if (path === '/tasks/owner-options' || path === '/tasks/lookup') return { data: { items: [], has_more: false } };
        return { data: [] };
    });
    api.post.mockImplementation(async (path: string) => {
        if (path === '/tasks/planning-inputs/member/2/context') return { data: { kind: 'member', resource_id: 2, resource: iteration, complete: true, expected_revisions: { 2: revision } } };
        if (path === '/iterations/2/team') { members = [...members, added]; revision++; return { data: added }; }
        return { data: { id: 101, title: 'Import holidays' } };
    });
});

const openForm = () => renderWithProviders(<TaskForm iterationId={2} initialTitle="Import holidays" onSuccess={vi.fn()} onCancel={vi.fn()} />);

describe('assigning iteration capacity from the task form', () => {
    it.each(['human', 'agent'])('groups People and Agents with load and adds an outside %s profile and assigns in one confirmed save', async kind => {
        const original = api.get.getMockImplementation()!;
        api.get.mockImplementation(async (path: string) => path === '/team-member-profiles' ? { data: [{ ...profile, profile_kind: kind }] } : original(path));
        const { user } = openForm();
        const select = await screen.findByRole('combobox', { name: 'Assignee' });
        expect(await within(select).findByRole('option', { name: 'Sam · 40% load' })).toBeInTheDocument();
        expect(within(select).getByRole('group', { name: 'People' })).toBeInTheDocument();
        expect(within(select).getByRole('group', { name: 'Agents' })).toBeInTheDocument();
        expect(within(select).getByRole('group', { name: 'Not in this iteration' })).toBeInTheDocument();
        await user.selectOptions(select, 'profile:9');
        expect(api.post).not.toHaveBeenCalled();
        await user.click(screen.getByRole('button', { name: 'Add to iteration and assign' }));
        await waitFor(() => expect(api.post).toHaveBeenCalledWith('/iterations/2/tasks', expect.objectContaining({ assignee_id: 10, expected_revision: 4 })));
        expect(api.post).toHaveBeenCalledWith('/iterations/2/team', expect.objectContaining({ profile_id: 9, position: kind === 'agent' ? 'Agent' : 'Team member', operational_utilization: kind === 'agent' ? 0 : 20 }), { headers: { 'X-Expected-Revisions': '{"2":3}' } });
        expect(api.post.mock.calls.filter(([path]) => path === '/iterations/2/team')).toHaveLength(1);
    });

    it('adds capacity and assigns an existing task with its observed version in one save', async () => {
        const task = { id: 101, version: 3, iteration_id: 2, project_id: 1, title: 'Import holidays', status: 'planned',
            priority: 3, effort_days: 1, tags: [], dependencies: [], children: [], agent_readiness: { is_ready: false, blockers: [], warnings: [], criteria: [] } } as unknown as Task;
        const { user } = renderWithProviders(<TaskForm iterationId={2} initialData={task} onSuccess={vi.fn()} onCancel={vi.fn()} />);
        await screen.findByRole('option', { name: 'Builder · Add to iteration and assign' });
        await user.selectOptions(screen.getByRole('combobox', { name: 'Assignee' }), 'profile:9');
        await user.click(screen.getByRole('button', { name: 'Add to iteration and assign' }));
        await waitFor(() => expect(api.put).toHaveBeenCalledWith('/tasks/101', expect.objectContaining({ assignee_id: 10, expected_version: 3 })));
        expect(api.post.mock.calls.filter(([path]) => path === '/iterations/2/team')).toHaveLength(1);
    });

    it('names a refused reviewer conflict and points to the Routing section when the form saves a new assignee', async () => {
        const task = { id: 101, version: 3, iteration_id: 2, project_id: 1, title: 'Import holidays', status: 'planned',
            priority: 3, effort_days: 1, tags: [], dependencies: [], children: [], agent_readiness: { is_ready: false, blockers: [], warnings: [], criteria: [] } } as unknown as Task;
        const check = { task_id: 101, assignee_id: 7, assignee_publishers: ['gamma'], assignee_catalog_keys: [], different_publisher_required: true, conflict_mode: 'refuse',
            structured: true, text_routing: false, consistent: false, applied: false, routing: null, suggestion: null,
            issues: [{ code: 'reviewer_shares_assignee_publisher', severity: 'conflict', field: 'reviewer', message: 'Same publisher.' }] };
        api.put.mockRejectedValueOnce({ response: { status: 409, data: { detail: { code: 'routing_inconsistent', message: 'The task\'s routing conflicts.', routing_check: check } } } });
        const { user } = renderWithProviders(<TaskForm iterationId={2} initialData={task} onSuccess={vi.fn()} onCancel={vi.fn()} />);
        const select = await screen.findByRole('combobox', { name: 'Assignee' });
        await within(select).findByRole('option', { name: 'Sam · 40% load' });
        await user.selectOptions(select, '7');
        await user.click(screen.getByRole('button', { name: 'Update task' }));
        const alert = await screen.findByRole('alert');
        expect(alert).toHaveTextContent(/same publisher as the new assignee/);
        expect(alert).toHaveTextContent(/Reassign to/);
        expect(alert).not.toHaveTextContent('The task\'s routing conflicts.');
        expect(await screen.findByRole('group', { name: 'Routing check' })).toBeVisible();
    });

    it('keeps Owner editable only under More', async () => {
        const { user } = openForm();
        expect(screen.queryByRole('combobox', { name: 'Owner' })).not.toBeInTheDocument();
        await user.click(screen.getByRole('button', { name: 'More' }));
        expect(screen.getByRole('combobox', { name: 'Owner' })).toBeInTheDocument();
    });

    it('reuses capacity after an uncertain capacity response instead of creating it twice', async () => {
        const original = api.post.getMockImplementation()!;
        let loseResponse = true;
        api.post.mockImplementation(async (...args: unknown[]) => {
            const result = await original(...args);
            if (args[0] === '/iterations/2/team' && loseResponse) { loseResponse = false; throw new TypeError('Lost response'); }
            return result;
        });
        const { user } = openForm();
        await screen.findByRole('option', { name: 'Builder · Add to iteration and assign' });
        await user.selectOptions(screen.getByRole('combobox', { name: 'Assignee' }), 'profile:9');
        await user.click(screen.getByRole('button', { name: 'Add to iteration and assign' }));
        await screen.findByText(/Could not add capacity/);
        expect(api.post.mock.calls.some(([path]) => path === '/iterations/2/tasks')).toBe(false);
        await user.click(screen.getByRole('button', { name: 'Add to iteration and assign' }));
        await waitFor(() => expect(api.post).toHaveBeenCalledWith('/iterations/2/tasks', expect.objectContaining({ assignee_id: 10 })));
        expect(api.post.mock.calls.filter(([path]) => path === '/iterations/2/team')).toHaveLength(1);
    });
});

import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { screen, waitFor } from '@testing-library/react';
import { renderWithProviders } from '../../test/renderWithProviders';
import { IdentityContext } from '../../features/identity/identityContext';
import type { WorkspaceIdentity } from '../../features/identity/identityService';
import { ADMIN_API_KEY_STORAGE_KEY } from '../../utils/adminAccess';
import type { Task } from '../../types/task';
import { emptyTaskBrief } from './taskEditorContract';
import { TaskReadView } from './TaskReadView';

const service = vi.hoisted(() => ({ writeBrief: vi.fn(), actions: vi.fn(), command: vi.fn() }));
vi.mock('../../services/taskService', () => ({ taskService: service }));
vi.mock('./TaskWorkPanel', () => ({ TaskWorkPanel: () => <p>Work panel</p> }));
vi.mock('./DeliveryDependencies', () => ({ DeliveryDependencies: () => null }));
vi.mock('./TaskDiscussion', () => ({ TaskDiscussion: () => <p>Discussion</p> }));
vi.mock('./TimeEntriesPanel', () => ({ TimeEntriesPanel: () => null }));
vi.mock('./TaskTimelinePanel', () => ({ TaskTimelinePanel: () => <p>History</p> }));

const task = {
    id: 5, title: 'Plan the launch', status: 'planned', version: 1, priority: 2, effort_days: 3, assignee: null, owner: null,
    project_id: 1, iteration_id: 2, dependencies: [], children: [], tags: [], is_overdue: false, is_delayed: false,
    is_composite: false, is_optional: false, is_deferred: false, sort_order: 0, external_links: [], request_count: 0,
    agent_readiness: { is_ready: false, blockers: [], warnings: [], criteria: [] }, effort_hours: null,
    brief: { ...emptyTaskBrief(), acceptance_criteria: [{ id: 'a', revision: 1, text: 'Done', verification: '' }] },
} as unknown as Task;

const identity: WorkspaceIdentity = { mode: 'trusted_local', authenticated: false, configured: false, principal: null,
    profile: { id: 3, display_name: 'Priya Nair' }, workspace_role: null, projects: {}, csrf_token: null };

const actions = { task_id: 5, version: 1, claim_generation: 0, running_run_ids: [], live_assignment_ids: [],
    actions: [{ action: 'start_manual', allowed: true, blockers: [] }] };

describe('task view while editing is unlocked with the admin key', () => {
    beforeEach(() => {
        vi.clearAllMocks();
        sessionStorage.setItem(ADMIN_API_KEY_STORAGE_KEY, 'key');
        service.actions.mockResolvedValue(actions);
        service.command.mockResolvedValue(task);
    });
    afterEach(() => sessionStorage.clear());

    it('offers no Start work, says why, and starts work after Lock editing', async () => {
        const { user } = renderWithProviders(<IdentityContext.Provider value={{ identity, refresh: vi.fn(), signOut: vi.fn() }}>
            <TaskReadView task={task} draftKey={null} onTaskUpdated={vi.fn()} onEditAll={vi.fn()} onDirty={vi.fn()} onPending={vi.fn()} onReload={vi.fn()} />
        </IdentityContext.Provider>, { initialEntries: ['/tasks?task=5'] });
        expect(screen.queryByRole('button', { name: 'Start work' })).not.toBeInTheDocument();
        expect(screen.getByText('Start work and Submit for review are taken as the chosen person. Lock editing to use them.')).toBeInTheDocument();
        await user.click(screen.getByRole('button', { name: 'Lock editing' }));
        expect(sessionStorage.getItem(ADMIN_API_KEY_STORAGE_KEY)).toBeNull();
        await user.click(await screen.findByRole('button', { name: 'Start work' }));
        await waitFor(() => expect(service.command).toHaveBeenCalledWith(5, expect.objectContaining({ action: 'start_manual' })));
        expect(screen.queryByRole('button', { name: 'Lock editing' })).not.toBeInTheDocument();
    });
});

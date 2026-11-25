import { beforeEach, describe, expect, it, vi } from 'vitest';
import { screen, waitFor } from '@testing-library/react';
import { renderWithProviders } from '../../test/renderWithProviders';
import { IdentityContext } from '../../features/identity/identityContext';
import type { WorkspaceIdentity } from '../../features/identity/identityService';
import type { DeliveryPrerequisite } from '../../types/github';
import type { Task } from '../../types/task';
import { useState } from 'react';
import { DeliveryDependencies } from './DeliveryDependencies';
import { useTaskViewSession } from './taskViewSession';

const mocks = vi.hoisted(() => ({ get: vi.fn(), post: vi.fn(), delete: vi.fn(), retarget: vi.fn(), getById: vi.fn(), lookup: vi.fn() }));
vi.mock('../../services/api', () => ({ default: { get: mocks.get, post: mocks.post, delete: mocks.delete } }));
vi.mock('../../services/githubService', () => ({ githubService: { retargetPrerequisite: mocks.retarget } }));
vi.mock('../../services/taskService', () => ({ taskService: { getById: mocks.getById, lookup: mocks.lookup } }));
vi.mock('../../services/projectService', () => ({ projectService: { getAll: vi.fn(), getMilestones: vi.fn() } }));

const task = { id: 7, version: 5, project_id: 5, title: 'Ship export' } as unknown as Task;
const edge = (overrides: Partial<DeliveryPrerequisite> = {}): DeliveryPrerequisite => ({
    id: 11, kind: 'task', target_id: 3, title: 'Build API', ready: false, reason: 'prerequisite_merge_not_observed',
    target_branch: 'main', merge: { state: 'not_observed', verified: false, target_branch: 'main' },
    hold: { case: 'not_observed', reason: 'prerequisite_merge_not_observed', next_owner: 'pm', next_action: 'No merge into main is observed for task 3; link its pull request if missing, then run GitHub catch-up.' },
    ...overrides,
});
const identity = (overrides: Partial<WorkspaceIdentity> = {}): WorkspaceIdentity => ({
    mode: 'managed', authenticated: true, configured: true, principal: { id: 1, kind: 'human', display_name: 'Pat' }, profile: null,
    workspace_role: 'member', projects: { '5': 'editor' }, csrf_token: null, features: ['delivery-prerequisite-retarget-v1'], ...overrides,
});
const renderEditor = async (value: WorkspaceIdentity = identity()) => {
    const result = renderWithProviders(<IdentityContext.Provider value={{ identity: value, refresh: vi.fn(), signOut: vi.fn() }}>
        <DeliveryDependencies task={task} disabled={false} onPending={vi.fn()} onUpdated={vi.fn()} /></IdentityContext.Provider>);
    await result.user.click(screen.getByText('Delivery prerequisites'));
    return result;
};
const conflict = { response: { status: 409, data: { detail: 'Task version is stale' } } };

beforeEach(() => {
    vi.clearAllMocks();
    sessionStorage.clear();
    mocks.get.mockResolvedValue({ data: [edge()] });
    mocks.getById.mockResolvedValue({ ...task, version: 6 });
    mocks.lookup.mockResolvedValue({ items: [{ id: 3, title: 'Build API' }] });
});

describe('prerequisite target branch', () => {
    it('shows the branch and why the prerequisite is held', async () => {
        await renderEditor();
        expect(await screen.findByText('main')).toBeInTheDocument();
        expect(screen.getByText('No merge observed')).toBeInTheDocument();
        expect(screen.getByText(/No merge into main is observed/)).toBeInTheDocument();
        expect(screen.getByText(/Next: project manager\./)).toBeInTheDocument();
    });

    it('explains a merge on another branch and an unconfirmed merge branch', async () => {
        mocks.get.mockResolvedValue({ data: [
            edge({ id: 1, title: 'Alpha', hold: { case: 'merged_on_other_branch', reason: 'prerequisite_merge_not_observed', next_owner: 'pm', next_action: 'It merged into another branch.' } }),
            edge({ id: 2, title: 'Beta', hold: { case: 'merge_branch_unknown', reason: 'prerequisite_merge_not_observed', next_owner: 'pm', next_action: 'Run GitHub catch-up.' } }),
        ] });
        await renderEditor();
        expect(await screen.findByText('Merged on another branch')).toBeInTheDocument();
        expect(screen.getByText('Merge branch not confirmed')).toBeInTheDocument();
    });

    it('says when only acceptance is required', async () => {
        mocks.get.mockResolvedValue({ data: [edge({ target_branch: null, merge: null, hold: null, reason: 'prerequisite_acceptance_required' })] });
        await renderEditor();
        expect(await screen.findByText('No target branch: acceptance alone releases this prerequisite.')).toBeInTheDocument();
    });

    it('creates a prerequisite with a target branch', async () => {
        mocks.post.mockResolvedValue({ data: {} });
        const { user } = await renderEditor();
        await user.type(screen.getByLabelText('Search tasks'), 'Build');
        await user.selectOptions(await screen.findByLabelText('Prerequisite'), '3');
        await user.type(screen.getByLabelText('Target branch (optional)'), ' release/1.9 ');
        await user.click(screen.getByRole('button', { name: 'Add prerequisite' }));
        await waitFor(() => expect(mocks.post).toHaveBeenCalledWith(`/tasks/${task.id}/delivery-dependencies`,
            { kind: 'task', target_id: 3, expected_version: 5, target_branch: 'release/1.9' }));
    });

    it('creates a prerequisite without a branch when the field is empty', async () => {
        mocks.post.mockResolvedValue({ data: {} });
        const { user } = await renderEditor();
        await user.type(screen.getByLabelText('Search tasks'), 'Build');
        await user.selectOptions(await screen.findByLabelText('Prerequisite'), '3');
        await user.click(screen.getByRole('button', { name: 'Add prerequisite' }));
        await waitFor(() => expect(mocks.post).toHaveBeenCalledWith(`/tasks/${task.id}/delivery-dependencies`, { kind: 'task', target_id: 3, expected_version: 5 }));
    });

    it('changes the branch and refreshes the hold reason', async () => {
        mocks.retarget.mockResolvedValue([]);
        const changed = edge({ target_branch: 'release/1.9', hold: { case: 'merge_branch_unknown', reason: 'prerequisite_merge_not_observed', next_owner: 'pm', next_action: 'Run GitHub catch-up for task 3.' } });
        const { user } = await renderEditor();
        await user.click(await screen.findByRole('button', { name: 'Change target branch for Build API' }));
        const input = screen.getByLabelText('Target branch');
        expect(input).toHaveValue('main');
        mocks.get.mockResolvedValue({ data: [changed] });
        await user.clear(input);
        await user.type(input, 'release/1.9');
        await user.click(screen.getByRole('button', { name: 'Save branch' }));
        await waitFor(() => expect(mocks.retarget).toHaveBeenCalledWith(task.id, 11, 5, 'release/1.9'));
        expect(await screen.findByText('Merge branch not confirmed')).toBeInTheDocument();
        expect(screen.queryByLabelText('Target branch')).not.toBeInTheDocument();
    });

    it('sets a branch on a prerequisite that has none', async () => {
        mocks.get.mockResolvedValue({ data: [edge({ target_branch: null, merge: null, hold: null })] });
        mocks.retarget.mockResolvedValue([]);
        const { user } = await renderEditor();
        await user.click(await screen.findByRole('button', { name: 'Set target branch for Build API' }));
        expect(screen.queryByRole('button', { name: 'Clear branch' })).not.toBeInTheDocument();
        await user.type(screen.getByLabelText('Target branch'), 'main');
        await user.click(screen.getByRole('button', { name: 'Save branch' }));
        await waitFor(() => expect(mocks.retarget).toHaveBeenCalledWith(task.id, 11, 5, 'main'));
    });

    it('clears the branch with null', async () => {
        mocks.retarget.mockResolvedValue([]);
        const { user } = await renderEditor();
        await user.click(await screen.findByRole('button', { name: 'Change target branch for Build API' }));
        await user.click(screen.getByRole('button', { name: 'Clear branch' }));
        await waitFor(() => expect(mocks.retarget).toHaveBeenCalledWith(task.id, 11, 5, null));
    });

    it('refreshes and says so on a stale version, keeping the draft', async () => {
        mocks.retarget.mockRejectedValue(conflict);
        const { user } = await renderEditor();
        await user.click(await screen.findByRole('button', { name: 'Change target branch for Build API' }));
        await user.clear(screen.getByLabelText('Target branch'));
        await user.type(screen.getByLabelText('Target branch'), 'develop');
        const reads = mocks.get.mock.calls.length;
        await user.click(screen.getByRole('button', { name: 'Save branch' }));
        expect(await screen.findByRole('alert')).toHaveTextContent('This task changed while you were editing.');
        await waitFor(() => expect(mocks.getById).toHaveBeenCalledWith(task.id));
        await waitFor(() => expect(mocks.get.mock.calls.length).toBeGreaterThan(reads));
        expect(screen.getByLabelText('Target branch')).toHaveValue('develop');
    });

    describe('across the task view remounting on a new version', () => {
        const onDirty = vi.fn();
        // Mirrors the drawer: the session lives above the remount boundary, the view is keyed by version.
        const Drawer = ({ person }: { person: string }) => {
            const draftKey = `workchord-draft:${person}:task:7`;
            const [session, onSession] = useTaskViewSession(draftKey);
            const [version, setVersion] = useState(5);
            return <IdentityContext.Provider value={{ identity: identity(), refresh: vi.fn(), signOut: vi.fn() }}>
                <DeliveryDependencies key={version} task={{ ...task, version } as Task} disabled={false} draftKey={draftKey}
                    session={session} onSession={onSession} onDirty={onDirty} onPending={vi.fn()} onUpdated={() => setVersion(6)} />
            </IdentityContext.Provider>;
        };
        const startEditing = async (user: ReturnType<typeof renderWithProviders>['user']) => {
            await user.click(screen.getByText('Delivery prerequisites'));
            await user.click(await screen.findByRole('button', { name: 'Change target branch for Build API' }));
            await user.clear(screen.getByLabelText('Target branch'));
            await user.type(screen.getByLabelText('Target branch'), 'develop');
        };

        it('keeps the list open, the draft and the notice after a stale version, and reports the draft as unsaved', async () => {
            mocks.retarget.mockRejectedValue(conflict);
            const { user } = renderWithProviders(<Drawer person="1" />);
            await startEditing(user);
            expect(onDirty).toHaveBeenLastCalledWith(true);
            await user.click(screen.getByRole('button', { name: 'Save branch' }));
            expect(await screen.findByRole('alert')).toHaveTextContent('This task changed while you were editing.');
            await waitFor(() => expect(mocks.getById).toHaveBeenCalled());
            await waitFor(() => expect(screen.getByLabelText('Target branch')).toHaveValue('develop'));
            expect(screen.getByRole('alert')).toHaveTextContent('This task changed while you were editing.');
            expect(onDirty).toHaveBeenLastCalledWith(true);
        });

        it('keeps the list open after a saved change and clears the draft', async () => {
            mocks.retarget.mockResolvedValue([]);
            const { user } = renderWithProviders(<Drawer person="1" />);
            await user.click(screen.getByText('Delivery prerequisites'));
            await user.click(await screen.findByRole('button', { name: 'Change target branch for Build API' }));
            await user.click(screen.getByRole('button', { name: 'Clear branch' }));
            await waitFor(() => expect(mocks.retarget).toHaveBeenCalled());
            expect(await screen.findByText('Build API', { exact: false })).toBeVisible();
            expect(screen.queryByLabelText('Target branch')).not.toBeInTheDocument();
            expect(sessionStorage.length).toBe(0);
            expect(onDirty).toHaveBeenLastCalledWith(false);
        });

        it('does not report an unchanged field as unsaved, and clears the draft on cancel', async () => {
            const { user } = renderWithProviders(<Drawer person="1" />);
            await user.click(screen.getByText('Delivery prerequisites'));
            await user.click(await screen.findByRole('button', { name: 'Change target branch for Build API' }));
            expect(onDirty).toHaveBeenLastCalledWith(false);
            await user.type(screen.getByLabelText('Target branch'), 'x');
            expect(sessionStorage.length).toBe(1);
            await user.click(screen.getByRole('button', { name: 'Cancel' }));
            expect(sessionStorage.length).toBe(0);
            expect(onDirty).toHaveBeenLastCalledWith(false);
        });

        it('offers the same person their draft in a new drawer but shows nobody else a draft or notice', async () => {
            const first = renderWithProviders(<Drawer person="1" />);
            await startEditing(first.user);
            first.unmount();
            const other = renderWithProviders(<Drawer person="2" />);
            expect(screen.queryByLabelText('Target branch')).not.toBeInTheDocument();
            other.unmount();
            renderWithProviders(<Drawer person="1" />);
            expect(await screen.findByLabelText('Target branch')).toHaveValue('develop');
        });

        it('survives a failing task refresh after a stale version', async () => {
            mocks.retarget.mockRejectedValue(conflict);
            mocks.getById.mockRejectedValue(new Error('offline'));
            const { user } = renderWithProviders(<Drawer person="1" />);
            await startEditing(user);
            await user.click(screen.getByRole('button', { name: 'Save branch' }));
            expect(await screen.findByRole('alert')).toHaveTextContent('This task changed while you were editing.');
            expect(screen.getByLabelText('Target branch')).toHaveValue('develop');
        });
    });

    it('shows the server message for an invalid branch and keeps the draft', async () => {
        mocks.retarget.mockRejectedValue({ response: { status: 422, data: { detail: 'Branch name is not valid' } } });
        const { user } = await renderEditor();
        await user.click(await screen.findByRole('button', { name: 'Change target branch for Build API' }));
        await user.clear(screen.getByLabelText('Target branch'));
        await user.type(screen.getByLabelText('Target branch'), 'bad..name');
        await user.click(screen.getByRole('button', { name: 'Save branch' }));
        expect(await screen.findByRole('alert')).toHaveTextContent('Branch name is not valid');
        expect(screen.getByLabelText('Target branch')).toHaveValue('bad..name');
        expect(screen.getByLabelText('Target branch')).toHaveAttribute('aria-invalid', 'true');
        expect(mocks.getById).not.toHaveBeenCalled();
    });

    it('cancels without saving', async () => {
        const { user } = await renderEditor();
        await user.click(await screen.findByRole('button', { name: 'Change target branch for Build API' }));
        await user.click(screen.getByRole('button', { name: 'Cancel' }));
        expect(screen.queryByLabelText('Target branch')).not.toBeInTheDocument();
        expect(mocks.retarget).not.toHaveBeenCalled();
    });

    it.each([
        ['a viewer', identity({ projects: { '5': 'viewer' }, workspace_role: null })],
        ['a server without retargeting', identity({ features: [] })],
        ['a paired reader', identity({ access: 'observe' })],
    ])('offers no branch editing to %s', async (_name, value) => {
        await renderEditor(value);
        expect(await screen.findByText('main')).toBeInTheDocument();
        expect(screen.queryByRole('button', { name: /target branch for/ })).not.toBeInTheDocument();
    });
});

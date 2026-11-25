import { beforeEach, describe, expect, it, vi } from 'vitest';
import { screen, waitFor } from '@testing-library/react';
import { renderWithProviders } from '../../test/renderWithProviders';
import { IdentityContext } from '../../features/identity/identityContext';
import type { WorkspaceIdentity } from '../../features/identity/identityService';
import type { GitHubPullReconciliation, GitHubReconciliation } from '../../types/github';
import type { Task } from '../../types/task';
import { GitHubReconciliationPanel } from './GitHubReconciliationPanel';
import { useTaskViewSession } from './taskViewSession';

const service = vi.hoisted(() => ({ getReconciliation: vi.fn(), catchUp: vi.fn() }));
const tasks = vi.hoisted(() => ({ getById: vi.fn() }));
vi.mock('../../services/githubService', () => ({ githubService: service }));
vi.mock('../../services/taskService', () => ({ taskService: tasks }));

const task = { id: 41, version: 3, project_id: 5, title: 'Add export' } as unknown as Task;

const pull = (overrides: Partial<GitHubPullReconciliation> = {}): GitHubPullReconciliation => ({
    link_id: 1, url: 'https://github.com/acme/app/pull/9', title: 'Add export', state: 'open',
    submitted_sha: 'aaaaaaa1111111', submissions: [], observed_head_sha: 'aaaaaaa1111111', target_branch: 'main',
    checks: { state: 'success', total: 4, sha: 'aaaaaaa1111111' }, merged: false, merge_commit_sha: null, merged_at: null, closed_at: null,
    observed_at: '2026-11-25T10:00:00Z', observation_source: 'catch_up', observation_error: null,
    review: { accepted: false, state: 'not_requested' }, differences: [], next_owner: 'reviewer', next_action: 'Review the submitted commit; the head matches it.',
    ...overrides,
});
const view = (...pulls: GitHubPullReconciliation[]): GitHubReconciliation => ({ task_id: 41, task_status: 'active', accepted: false, pull_requests: pulls });

const identity = (overrides: Partial<WorkspaceIdentity> = {}): WorkspaceIdentity => ({
    mode: 'managed', authenticated: true, configured: true, principal: { id: 1, kind: 'human', display_name: 'Pat' }, profile: null,
    workspace_role: 'member', projects: { '5': 'editor' }, csrf_token: null, ...overrides,
});
const onTaskUpdated = vi.fn();
const Harness = ({ value }: { value: WorkspaceIdentity }) => {
    const [session, onSession] = useTaskViewSession('draft');
    return <IdentityContext.Provider value={{ identity: value, refresh: vi.fn(), signOut: vi.fn() }}>
        <GitHubReconciliationPanel task={task} session={session} onSession={onSession} onTaskUpdated={onTaskUpdated} /></IdentityContext.Provider>;
};
const renderPanel = (value: WorkspaceIdentity = identity()) => renderWithProviders(<Harness value={value} />);

beforeEach(() => { vi.clearAllMocks(); tasks.getById.mockResolvedValue({ ...task, version: 4 }); });

describe('GitHub reconciliation panel', () => {
    it('says a pull request is unobserved and what to do next', async () => {
        service.getReconciliation.mockResolvedValue(view(pull({
            state: 'unobserved', observed_head_sha: null, target_branch: null, checks: { state: null }, observed_at: null, observation_source: null,
            submitted_sha: null, differences: ['never_observed'], next_owner: 'pm', next_action: 'Run catch-up to read the pull request from GitHub.',
        })));
        renderPanel();
        expect(await screen.findByText('This pull request has not been read from GitHub yet.')).toBeInTheDocument();
        expect(screen.getByText('Never observed')).toBeInTheDocument();
        expect(screen.getByText('Unknown until GitHub is read')).toBeInTheDocument();
        expect(screen.getByText('Next: project manager.')).toBeInTheDocument();
        expect(screen.getByText('Run catch-up to read the pull request from GitHub.')).toBeInTheDocument();
    });

    it('flags a head that differs from the submitted commit', async () => {
        service.getReconciliation.mockResolvedValue(view(pull({
            observed_head_sha: 'bbbbbbb2222222', differences: ['head_differs_from_submission', 'checks_not_observed_for_head'], checks: { state: 'not_observed' },
            next_owner: 'pm', next_action: 'The head differs from the submitted commit; have the worker submit the current head, then request review.',
        })));
        renderPanel();
        expect(await screen.findByText('Differs from the submitted commit')).toBeInTheDocument();
        expect(screen.getByText('aaaaaaa')).toBeInTheDocument();
        expect(screen.getByText('bbbbbbb')).toBeInTheDocument();
        expect(screen.getByText('The pull request head is not the submitted commit.')).toBeInTheDocument();
    });

    it('shows a merge with its branch and commit', async () => {
        service.getReconciliation.mockResolvedValue(view(pull({
            state: 'merged', merged: true, merge_commit_sha: 'ccccccc3333333', merged_at: '2026-11-25T11:00:00Z', target_branch: 'release/1.9',
            next_owner: 'reviewer', next_action: 'Merged outside WorkChord; the independent verdict on the submitted commit is still required.',
        })));
        renderPanel();
        expect(await screen.findByText('release/1.9')).toBeInTheDocument();
        expect(screen.getByText(/^Merged Nov/)).toBeInTheDocument();
        expect(screen.getByText('ccccccc')).toBeInTheDocument();
    });

    it('says a merged pull request has no recorded base branch', async () => {
        service.getReconciliation.mockResolvedValue(view(pull({ state: 'merged', merged: true, merged_at: null, target_branch: null, merge_commit_sha: null })));
        renderPanel();
        expect(await screen.findByText('Not recorded')).toBeInTheDocument();
        expect(screen.getByText(/at an unrecorded time/)).toBeInTheDocument();
    });

    it('shows a pull request closed without merging', async () => {
        service.getReconciliation.mockResolvedValue(view(pull({
            state: 'closed_unmerged', closed_at: '2026-11-25T12:00:00Z', differences: ['closed_without_merge'],
            next_owner: 'pm', next_action: 'Closed without merging; reopen the pull request or replace the task.',
        })));
        renderPanel();
        expect(await screen.findByText(/^Closed without merging /)).toBeInTheDocument();
        expect(screen.getByText('Closed, not merged')).toBeInTheDocument();
        expect(screen.getByText('Closed without merging; reopen the pull request or replace the task.')).toBeInTheDocument();
    });

    it('names review states and observation sources, and falls back to an unknown code', async () => {
        service.getReconciliation.mockResolvedValue(view(
            pull({ link_id: 1, review: { accepted: false, state: 'queued' }, observation_source: 'refresh' }),
            pull({ link_id: 2, review: { accepted: false, state: 'new_state' }, observation_source: 'other_source' })));
        renderPanel();
        expect(await screen.findByText('Review queued')).toBeInTheDocument();
        expect(screen.getByText(/Read from GitHub/)).toBeInTheDocument();
        expect(screen.getByText('new_state')).toBeInTheDocument();
        expect(screen.getByText(/other_source/)).toBeInTheDocument();
    });

    it('says when no pull request is linked', async () => {
        service.getReconciliation.mockResolvedValue(view());
        renderPanel();
        expect(await screen.findByText('No pull request is linked to this task.')).toBeInTheDocument();
    });

    it('offers a retry when the view cannot be loaded', async () => {
        service.getReconciliation.mockRejectedValueOnce(new Error('offline')).mockResolvedValue(view(pull()));
        const { user } = renderPanel();
        await user.click(await screen.findByRole('button', { name: /retry/i }));
        expect(await screen.findByText('Add export')).toBeInTheDocument();
    });

    describe('catch-up', () => {
        it('runs for people who can edit and shows the refreshed view', async () => {
            service.getReconciliation.mockResolvedValue(view(pull({ state: 'unobserved', differences: ['never_observed'], observed_at: null })));
            service.catchUp.mockResolvedValue(view(pull({ state: 'merged', merged: true, merged_at: '2026-11-25T11:00:00Z' })));
            const { user } = renderPanel();
            await user.click(await screen.findByRole('button', { name: 'Run catch-up' }));
            expect(service.catchUp).toHaveBeenCalledWith(41);
            expect(await screen.findByText('Catch-up finished. The view shows what GitHub reports now.')).toBeInTheDocument();
            expect(screen.queryByText('This pull request has not been read from GitHub yet.')).not.toBeInTheDocument();
        });

        it('hands the refreshed task to the page so its next versioned action is not stale', async () => {
            service.getReconciliation.mockResolvedValue(view(pull()));
            service.catchUp.mockResolvedValue(view(pull()));
            const { user } = renderPanel();
            await user.click(await screen.findByRole('button', { name: 'Run catch-up' }));
            await waitFor(() => expect(onTaskUpdated).toHaveBeenCalledWith({ ...task, version: 4 }));
            expect(tasks.getById).toHaveBeenCalledWith(41);
        });

        it('still finishes when the task refresh fails', async () => {
            service.getReconciliation.mockResolvedValue(view(pull()));
            service.catchUp.mockResolvedValue(view(pull()));
            tasks.getById.mockRejectedValue(new Error('offline'));
            const { user } = renderPanel();
            await user.click(await screen.findByRole('button', { name: 'Run catch-up' }));
            expect(await screen.findByText('Catch-up finished. The view shows what GitHub reports now.')).toBeInTheDocument();
            expect(onTaskUpdated).not.toHaveBeenCalled();
        });

        it('is disabled and busy while it runs', async () => {
            service.getReconciliation.mockResolvedValue(view(pull()));
            let finish: (value: GitHubReconciliation) => void = () => undefined;
            service.catchUp.mockReturnValue(new Promise<GitHubReconciliation>(resolve => { finish = resolve; }));
            const { user } = renderPanel();
            await user.click(await screen.findByRole('button', { name: 'Run catch-up' }));
            await waitFor(() => expect(screen.getByRole('button', { name: 'Run catch-up' })).toBeDisabled());
            finish(view(pull()));
            await waitFor(() => expect(screen.getByRole('button', { name: 'Run catch-up' })).toBeEnabled());
        });

        it('names a failure beside the action', async () => {
            service.getReconciliation.mockResolvedValue(view(pull()));
            service.catchUp.mockRejectedValue({ response: { status: 502, data: { detail: 'GitHub token missing' } } });
            const { user } = renderPanel();
            await user.click(await screen.findByRole('button', { name: 'Run catch-up' }));
            expect(await screen.findByRole('alert')).toHaveTextContent('GitHub token missing');
        });

        it.each([
            ['a viewer', identity({ projects: { '5': 'viewer' }, workspace_role: null })],
            ['a paired reader', identity({ access: 'observe', workspace_role: 'owner' })],
        ])('is hidden for %s, who still sees the panel', async (_name, value) => {
            service.getReconciliation.mockResolvedValue(view(pull()));
            renderPanel(value);
            expect(await screen.findByText('Add export')).toBeInTheDocument();
            expect(screen.queryByRole('button', { name: 'Run catch-up' })).not.toBeInTheDocument();
        });
    });
});

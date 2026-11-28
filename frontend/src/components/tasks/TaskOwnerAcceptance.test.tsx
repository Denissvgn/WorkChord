import { beforeEach, describe, expect, it, vi } from 'vitest';
import { screen, waitFor, within } from '@testing-library/react';
import { renderWithProviders } from '../../test/renderWithProviders';
import { MutationSuccessFeedback } from '../../features/MutationSuccessFeedback';
import { IdentityContext } from '../../features/identity/identityContext';
import type { WorkspaceIdentity } from '../../features/identity/identityService';
import i18n, { ensureLanguageResources } from '../../i18n/i18n';
import type { Task, TaskReviewRecord } from '../../types/task';
import { emptyTaskBrief } from './taskEditorContract';
import { TaskWorkPanel } from './TaskWorkPanel';

const service = vi.hoisted(() => ({ actions: vi.fn(), progress: vi.fn(), command: vi.fn(), review: vi.fn(), getDetail: vi.fn(), ownerAccept: vi.fn(), reviews: vi.fn() }));
vi.mock('../../services/taskService', () => ({ taskService: service }));
vi.mock('../../services/iterationService', () => ({ iterationService: { getAll: vi.fn().mockResolvedValue([]) } }));

const resolved = {
    id: 42, iteration_id: null, project_id: 2, title: 'Human work', priority: 5, effort_days: null, effort_hours: null,
    status: 'resolved', execution_mode: 'manual', is_overdue: false, is_delayed: false, is_composite: false,
    is_optional: false, is_deferred: false, tags: [], sort_order: 0, external_links: [], request_count: 0,
    agent_readiness: { is_ready: false, blockers: [], warnings: [], criteria: [] }, version: 3, children: [], dependencies: [],
    brief_revision: 2, artifact_revision: 1, assignee: { id: 7, name: 'Sam' },
    brief: { ...emptyTaskBrief(), acceptance_criteria: [{ id: 'criterion', revision: 1, text: 'Inspect the result', verification: '' }] },
} as Task;

const identity = (overrides: Partial<WorkspaceIdentity>): WorkspaceIdentity => ({ mode: 'managed', authenticated: true, configured: true,
    principal: { id: 9, kind: 'human', display_name: 'Olga' }, profile: null, workspace_role: 'owner', projects: {}, csrf_token: 'x', access: 'full', ...overrides });

const publisherBlocker = { code: 'verified_publisher_review_required', message: 'Use an assigned agent verifier for formal review.' };
const policyActions = { task_id: 42, version: 3, claim_generation: 0, running_run_ids: [], live_assignment_ids: [], actions: [
    { action: 'review', allowed: false, blockers: [publisherBlocker] }, { action: 'accept_review', allowed: false, blockers: [publisherBlocker] },
] };

const renderPanel = (who: WorkspaceIdentity, task: Task = resolved, onUpdated = vi.fn()) => ({ onUpdated, ...renderWithProviders(
    <IdentityContext.Provider value={{ identity: who, refresh: vi.fn(), signOut: vi.fn() }}>
        <MutationSuccessFeedback />
        <TaskWorkPanel task={task} disabled={false} draftKey={null} onDirty={vi.fn()} onPending={vi.fn()} onUpdated={onUpdated} onReload={vi.fn()} />
    </IdentityContext.Provider>) });

describe('owner acceptance under the different-publisher policy', () => {
    beforeEach(async () => {
        vi.clearAllMocks();
        await i18n.changeLanguage('en');
        service.actions.mockResolvedValue(policyActions);
        service.getDetail.mockResolvedValue({ task: resolved, reviewer_name: null });
        service.reviews.mockResolvedValue([]);
        service.ownerAccept.mockResolvedValue({ ...resolved, status: 'closed', version: 4 });
    });

    it('lets a signed-in owner accept with a reason, by keyboard, and announces the result', async () => {
        const { user, onUpdated } = renderPanel(identity({}));
        const button = await screen.findByRole('button', { name: 'Accept as owner' });
        expect(button).toBeDisabled();
        expect(button).toHaveAccessibleDescription('Add a reason to accept as owner.');
        const reason = screen.getByRole('textbox', { name: /Reason for accepting as owner/ });
        // Reach the reason field and the button with the keyboard alone.
        for (let step = 0; step < 40 && document.activeElement !== reason; step += 1) await user.tab();
        expect(reason).toHaveFocus();
        await user.keyboard('Verified the release by hand');
        expect(button).toBeEnabled();
        await user.tab();
        expect(button).toHaveFocus();
        await user.keyboard('{Enter}');
        await waitFor(() => expect(service.ownerAccept).toHaveBeenCalledWith(42, { expected_version: 3, brief_revision: 2, artifact_revision: 1, reason: 'Verified the release by hand' }));
        await waitFor(() => expect(onUpdated).toHaveBeenCalled());
        expect(await screen.findByText('Accepted “Human work” as an owner override.')).toBeInTheDocument();
        expect(service.review).not.toHaveBeenCalled();
    });

    it('does not accept with a blank reason', async () => {
        const { user } = renderPanel(identity({ workspace_role: 'operator' }));
        await user.type(await screen.findByRole('textbox', { name: /Reason for accepting as owner/ }), '   ');
        expect(screen.getByRole('button', { name: 'Accept as owner' })).toBeDisabled();
    });

    it('shows a refusal from the server and keeps the reason', async () => {
        service.ownerAccept.mockRejectedValue({ response: { status: 403, data: { detail: { message: 'Only a signed-in workspace owner or operator can accept work as an owner override.' } } } });
        const { user } = renderPanel(identity({}));
        await user.type(await screen.findByRole('textbox', { name: /Reason for accepting as owner/ }), 'Because');
        await user.click(screen.getByRole('button', { name: 'Accept as owner' }));
        expect(await screen.findByRole('alert')).toHaveTextContent('Only a signed-in workspace owner or operator can accept work as an owner override.');
        expect(screen.getByRole('textbox', { name: /Reason for accepting as owner/ })).toHaveValue('Because');
    });

    it('explains a trusted-local browser with no signed-in person and offers no action', async () => {
        renderPanel(identity({ mode: 'trusted_local', authenticated: false, principal: null, workspace_role: null }));
        expect(await screen.findByText(/This browser has no signed-in person/)).toBeInTheDocument();
        expect(screen.queryByRole('button', { name: 'Accept as owner' })).not.toBeInTheDocument();
        expect(screen.queryByRole('textbox', { name: /Reason for accepting as owner/ })).not.toBeInTheDocument();
    });

    it.each(['member', null] as const)(
        'tells a person without authority (%s) why and what to do', async role => {
            renderPanel(identity({ workspace_role: role }));
            expect(await screen.findByText(/Ask one of them to accept this task, or to assign an agent verifier/)).toBeInTheDocument();
            expect(screen.queryByRole('button', { name: 'Accept as owner' })).not.toBeInTheDocument();
        });

    it('tells a paired observer what to do, from the denial the server actually sends', async () => {
        const denied = { code: 'permission_denied', message: 'Project review permission is required.' };
        service.actions.mockResolvedValue({ ...policyActions, actions: [
            { action: 'review', allowed: false, blockers: [denied] }, { action: 'accept_review', allowed: false, blockers: [denied] },
        ] });
        renderPanel(identity({ access: 'observe' }));
        expect(await screen.findByText(/A paired observer cannot accept work/)).toBeInTheDocument();
        expect(screen.queryByRole('button', { name: 'Accept as owner' })).not.toBeInTheDocument();
    });

    it('names unsaved progress as a reason the button is disabled', async () => {
        sessionStorage.setItem('workchord-draft:person:42:progress', JSON.stringify({ version: 3, savedAt: Date.now(), criteria: [
            { criterion_id: 'criterion', criterion_revision: 1, state: 'completed', evidence: 'Unsaved evidence' },
        ] }));
        renderWithProviders(<IdentityContext.Provider value={{ identity: identity({}), refresh: vi.fn(), signOut: vi.fn() }}>
            <TaskWorkPanel task={resolved} disabled={false} draftKey="workchord-draft:person:42" onDirty={vi.fn()} onPending={vi.fn()} onUpdated={vi.fn()} onReload={vi.fn()} />
        </IdentityContext.Provider>);
        const button = await screen.findByRole('button', { name: 'Accept as owner' });
        expect(button).toBeDisabled();
        expect(button).toHaveAccessibleDescription(expect.stringContaining('Save or discard progress changes before accepting.'));
        expect(button).toHaveAccessibleDescription(expect.stringContaining('Add a reason to accept as owner.'));
        sessionStorage.clear();
    });

    it('is not offered when acceptance is not blocked by the publisher policy', async () => {
        service.actions.mockResolvedValue({ ...policyActions, actions: [
            { action: 'review', allowed: true, blockers: [] }, { action: 'accept_review', allowed: true, blockers: [] },
        ] });
        renderPanel(identity({}));
        await screen.findByRole('button', { name: 'Accept' });
        expect(screen.queryByRole('button', { name: 'Accept as owner' })).not.toBeInTheDocument();
    });

    it('is not offered on work that is not resolved', async () => {
        renderPanel(identity({}), { ...resolved, status: 'active' });
        await waitFor(() => expect(service.actions).toHaveBeenCalled());
        expect(screen.queryByRole('button', { name: 'Accept as owner' })).not.toBeInTheDocument();
    });

    it.each(['en', 'ru'])('labels an owner override in the review history with its reason in %s', async language => {
        await ensureLanguageResources(language);
        await i18n.changeLanguage(language);
        const records: TaskReviewRecord[] = [
            { id: 1, task_version: 2, brief_revision: 2, artifact_revision: 1, principal_id: 4, verdict: 'reject', kind: 'review', reason: 'Needs another pass', evidence: '', created_at: '2026-11-25T10:00:00Z' },
            { id: 2, task_version: 3, brief_revision: 2, artifact_revision: 1, principal_id: 9, verdict: 'accept', kind: 'owner_override', reason: 'Checked by hand', evidence: '', created_at: '2026-11-26T10:00:00Z' },
        ];
        service.reviews.mockResolvedValue(records);
        renderPanel(identity({}), { ...resolved, status: 'closed' });
        const items = await screen.findAllByRole('listitem');
        expect(items[0]).toHaveTextContent(i18n.t('domain.ownerOverrideLabel'));
        expect(items[0]).toHaveTextContent(i18n.t('domain.reviewAccepted'));
        expect(items[0]).toHaveTextContent('Checked by hand');
        expect(items[1]).not.toHaveTextContent(i18n.t('domain.ownerOverrideLabel'));
        expect(items[1]).toHaveTextContent('Needs another pass');
    });

    it('pages through every review so the newest are shown', async () => {
        const record = (id: number, over: Partial<TaskReviewRecord> = {}): TaskReviewRecord => ({ id, task_version: 3, brief_revision: 2, artifact_revision: 1, principal_id: 4,
            verdict: 'reject', kind: 'review', reason: `Reason ${id}`, evidence: '', created_at: '2026-11-25T10:00:00Z', ...over });
        const first = Array.from({ length: 100 }, (_, index) => record(index + 1));
        service.reviews.mockImplementation(async (_id: number, params: { after_id?: number }) => (params.after_id ?? 0) === 0 ? first
            : [record(101, { verdict: 'accept', kind: 'owner_override', reason: 'Newest decision' })]);
        renderPanel(identity({}), { ...resolved, status: 'closed' });
        const items = within(await screen.findByRole('region', { name: 'Review history' })).getAllByRole('listitem');
        expect(service.reviews).toHaveBeenCalledWith(42, { limit: 100, after_id: 0 });
        expect(service.reviews).toHaveBeenCalledWith(42, { limit: 100, after_id: 100 });
        expect(items).toHaveLength(101);
        expect(items[0]).toHaveTextContent('Newest decision');
        expect(items[0]).toHaveTextContent('Owner override');
    });
});

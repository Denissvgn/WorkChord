import { beforeEach, describe, expect, it, vi } from 'vitest';
import { screen, waitFor, within } from '@testing-library/react';
import { renderWithProviders } from '../../test/renderWithProviders';
import { MutationSuccessFeedback } from '../../features/MutationSuccessFeedback';
import { IdentityContext } from '../../features/identity/identityContext';
import type { WorkspaceIdentity } from '../../features/identity/identityService';
import i18n, { ensureLanguageResources } from '../../i18n/i18n';
import type { Task, TaskPostponementRecord } from '../../types/task';
import { TaskWorkPanel } from './TaskWorkPanel';

const service = vi.hoisted(() => ({
    actions: vi.fn(), progress: vi.fn(), command: vi.fn(), review: vi.fn(), getDetail: vi.fn(), ownerAccept: vi.fn(), reviews: vi.fn(),
    lookup: vi.fn(), postpone: vi.fn(), reactivate: vi.fn(), recordOwnerDecision: vi.fn(),
}));
vi.mock('../../services/taskService', () => ({ taskService: service }));
vi.mock('../../services/iterationService', () => ({ iterationService: { getAll: vi.fn().mockResolvedValue([]) } }));

const base = {
    id: 42, iteration_id: null, project_id: 2, title: 'Ship the importer', priority: 5, effort_days: null, effort_hours: null,
    status: 'active', execution_mode: 'manual', is_overdue: false, is_delayed: false, is_composite: false,
    is_optional: false, is_deferred: false, tags: [], sort_order: 0, external_links: [], request_count: 0,
    agent_readiness: { is_ready: false, blockers: [], warnings: [], criteria: [] }, version: 3, children: [], dependencies: [],
    brief_revision: 1, artifact_revision: 1, assignee: { id: 7, name: 'Sam' },
} as Task;
const postponed = { ...base, status: 'postponed', version: 4 } as Task;

const identity = (overrides: Partial<WorkspaceIdentity> = {}): WorkspaceIdentity => ({ mode: 'managed', authenticated: true, configured: true,
    principal: { id: 9, kind: 'human', display_name: 'Olga' }, profile: null, workspace_role: 'owner', projects: {}, csrf_token: 'x', access: 'full', ...overrides });

const allowed = (...names: string[]) => ({ task_id: 42, version: 3, claim_generation: 2, running_run_ids: [11], live_assignment_ids: [5, 6], actions: [
    { action: 'postpone', allowed: names.includes('postpone'), blockers: names.includes('postpone') ? [] : [{ code: 'permission_denied', message: 'Project manage permission is required.' }] },
    { action: 'reactivate', allowed: names.includes('reactivate'), blockers: names.includes('reactivate') ? [] : [{ code: 'not_postponed', message: 'Only postponed work can be reactivated.' }] },
] });

const record = (overrides: Partial<TaskPostponementRecord> = {}): TaskPostponementRecord => ({
    id: 1, task_id: 42, open: true, from_status: 'active', reason: 'Waiting on the vendor', postponed_at: '2026-11-20T10:00:00Z',
    released: { claim_actor_id: null, claim_generation: null, assignment_ids: [], run_ids: [] },
    requirements: [
        { id: 10, position: 0, kind: 'predecessor_accepted', task_id: 7, triage_item_id: null, on_date: null, description: null, met: true, met_at: '2026-11-21T09:00:00Z' },
        { id: 11, position: 1, kind: 'date', task_id: null, triage_item_id: null, on_date: '2026-12-15', description: null, met: false, met_at: null },
        { id: 12, position: 2, kind: 'owner_decision', task_id: null, triage_item_id: null, on_date: null, description: 'Pick the vendor', met: false, met_at: null },
    ],
    reactivated_at: null, reactivated_to_status: null, reactivation_reason: null, ...overrides,
});

const renderPanel = (task: Task, who: WorkspaceIdentity = identity(), onUpdated = vi.fn()) => ({ onUpdated, ...renderWithProviders(
    <IdentityContext.Provider value={{ identity: who, refresh: vi.fn(), signOut: vi.fn() }}>
        <MutationSuccessFeedback />
        <TaskWorkPanel task={task} disabled={false} draftKey={null} onDirty={vi.fn()} onPending={vi.fn()} onUpdated={onUpdated} onReload={vi.fn()} />
    </IdentityContext.Provider>) });

beforeEach(async () => {
    vi.clearAllMocks();
    await ensureLanguageResources('en');
    await i18n.changeLanguage('en');
    service.getDetail.mockResolvedValue({ task: base, reviewer_name: null });
    service.reviews.mockResolvedValue([]);
    service.lookup.mockResolvedValue({ items: [{ id: 7, title: 'Vendor contract' }, { id: 42, title: 'Ship the importer' }], has_more: false, next_after_id: null, limit: 20 });
});

describe('postponing a task', () => {
    beforeEach(() => { service.actions.mockResolvedValue(allowed('postpone')); });

    it('is offered only to a person who may postpone', async () => {
        service.actions.mockResolvedValue(allowed());
        renderPanel(base);
        await screen.findByText('No actions are currently available.');
        expect(screen.queryByRole('button', { name: 'Postpone…' })).not.toBeInTheDocument();
        expect(screen.queryByRole('heading', { name: 'Postpone this work' })).not.toBeInTheDocument();
    });

    it('is not offered for work that is already closed or postponed by the server verdict', async () => {
        service.actions.mockResolvedValue({ ...allowed(), actions: [{ action: 'postpone', allowed: false, blockers: [{ code: 'invalid_lifecycle', message: 'Only planned, active or resolved work can be postponed.' }] }] });
        renderPanel({ ...base, status: 'closed' });
        await screen.findByText('No actions are currently available.');
        expect(screen.queryByRole('button', { name: 'Postpone…' })).not.toBeInTheDocument();
    });

    it('names what is released, and the unmet needs, before it can be confirmed', async () => {
        const { user } = renderPanel(base);
        await user.click(await screen.findByRole('button', { name: 'Postpone…' }));
        const release = screen.getByRole('group', { name: 'What postponing releases' });
        expect(within(release).getByText('Stops 1 running run.')).toBeInTheDocument();
        expect(within(release).getByText('Ends 2 live assignments.')).toBeInTheDocument();
        expect(within(release).getByText('When it comes back, it returns to Planned.')).toBeInTheDocument();
        const confirm = screen.getByRole('button', { name: 'Postpone work' });
        expect(confirm).toBeDisabled();
        expect(confirm).toHaveAccessibleDescription('Add a reason. Complete every requirement, or remove the ones you do not need.');
    });

    it('says resolved work returns to resolved', async () => {
        const { user } = renderPanel({ ...base, status: 'resolved' });
        await user.click(await screen.findByRole('button', { name: 'Postpone…' }));
        expect(screen.getByText('When it comes back, it returns to Resolved for review.')).toBeInTheDocument();
    });

    it('postpones with a reason and every kind of requirement, by keyboard, and announces the result', async () => {
        service.postpone.mockResolvedValue({ task: postponed, postponement: record() });
        const { user, onUpdated } = renderPanel(base);
        const open = await screen.findByRole('button', { name: 'Postpone…' });
        open.focus();
        await user.keyboard('{Enter}');
        expect(screen.getByRole('textbox', { name: /Why is this work being postponed/ })).toHaveFocus();
        await user.keyboard('Waiting on the vendor');
        // First requirement: a predecessor task chosen from a search.
        await user.type(screen.getByRole('textbox', { name: 'Find the task' }), 'vendor');
        const picker = await screen.findByRole('combobox', { name: 'Task' });
        await waitFor(() => expect(within(picker).getByRole('option', { name: '#7 · Vendor contract' })).toBeInTheDocument());
        expect(within(picker).queryByRole('option', { name: /Ship the importer/ })).not.toBeInTheDocument();
        await user.selectOptions(picker, '7');
        // Second: a date. Third: an owner decision. Fourth: a triage item.
        await user.click(screen.getByRole('button', { name: 'Add a requirement' }));
        await user.selectOptions(screen.getAllByRole('combobox', { name: 'Requirement type' })[1], 'date');
        await user.type(screen.getByLabelText('Resume on or after'), '2099-12-15');
        await user.click(screen.getByRole('button', { name: 'Add a requirement' }));
        await user.selectOptions(screen.getAllByRole('combobox', { name: 'Requirement type' })[2], 'owner_decision');
        await user.type(screen.getByRole('textbox', { name: 'What the owner must decide' }), 'Pick the vendor');
        await user.click(screen.getByRole('button', { name: 'Add a requirement' }));
        await user.selectOptions(screen.getAllByRole('combobox', { name: 'Requirement type' })[3], 'linked_triage');
        await user.type(screen.getByRole('textbox', { name: 'Triage item number' }), '31');
        const confirm = screen.getByRole('button', { name: 'Postpone work' });
        expect(confirm).toBeEnabled();
        confirm.focus();
        await user.keyboard('{Enter}');
        await waitFor(() => expect(service.postpone).toHaveBeenCalledWith(42, {
            expected_version: 3, reason: 'Waiting on the vendor',
            requirements: [{ kind: 'predecessor_accepted', task_id: 7 }, { kind: 'date', on_date: '2099-12-15' },
                { kind: 'owner_decision', description: 'Pick the vendor' }, { kind: 'linked_resolved', triage_item_id: 31 }],
            expected_claim_generation: 2, expected_running_run_ids: [11], expected_live_assignment_ids: [5, 6],
        }));
        await waitFor(() => expect(onUpdated).toHaveBeenCalledWith(postponed));
        expect(await screen.findByText('Postponed “Ship the importer”.')).toBeInTheDocument();
    });

    it('keeps the form and shows the refusal when the server declines', async () => {
        service.postpone.mockRejectedValue({ response: { status: 409, data: { detail: { message: 'This task changed. Reload it.' } } } });
        const { user, onUpdated } = renderPanel(base);
        await user.click(await screen.findByRole('button', { name: 'Postpone…' }));
        await user.type(screen.getByRole('textbox', { name: /Why is this work being postponed/ }), 'Because');
        await user.selectOptions(screen.getByRole('combobox', { name: 'Requirement type' }), 'owner_decision');
        await user.type(screen.getByRole('textbox', { name: 'What the owner must decide' }), 'Decide');
        await user.click(screen.getByRole('button', { name: 'Postpone work' }));
        expect((await screen.findAllByRole('alert')).some(item => item.textContent === 'This task changed. Reload it.')).toBe(true);
        expect(screen.getByRole('textbox', { name: /Why is this work being postponed/ })).toHaveValue('Because');
        expect(onUpdated).not.toHaveBeenCalled();
    });

    it('removes a requirement but always keeps at least one', async () => {
        const { user } = renderPanel(base);
        await user.click(await screen.findByRole('button', { name: 'Postpone…' }));
        expect(screen.queryByRole('button', { name: /Remove requirement/ })).not.toBeInTheDocument();
        await user.click(screen.getByRole('button', { name: 'Add a requirement' }));
        await user.click(screen.getByRole('button', { name: 'Remove requirement 2' }));
        expect(screen.getAllByRole('combobox', { name: 'Requirement type' })).toHaveLength(1);
    });
});

describe('closing the postpone form', () => {
    it('returns focus to Postpone and clears the draft on discard', async () => {
        service.actions.mockResolvedValue(allowed('postpone'));
        const { user } = renderPanel(base);
        await user.click(await screen.findByRole('button', { name: 'Postpone…' }));
        await user.keyboard('Half written');
        await user.click(screen.getByRole('button', { name: 'Discard' }));
        const open = screen.getByRole('button', { name: 'Postpone…' });
        expect(open).toHaveFocus();
        await user.click(open);
        expect(screen.getByRole('textbox', { name: /Why is this work being postponed/ })).toHaveValue('');
    });
});

describe('a postponed task', () => {
    beforeEach(() => {
        service.actions.mockResolvedValue(allowed('reactivate'));
        service.getDetail.mockResolvedValue({ task: postponed, reviewer_name: null, postponement: record() });
    });

    it('shows the reason and each requirement as met or not met', async () => {
        renderPanel(postponed);
        const waiting = await screen.findByRole('list', { name: 'What it is waiting for' });
        expect(await screen.findByText('Waiting on the vendor')).toBeInTheDocument();
        const items = within(waiting).getAllByRole('listitem');
        expect(items[0]).toHaveTextContent('Met: Task #7 is accepted');
        expect(items[1]).toHaveTextContent('Not met yet: It is');
        expect(items[2]).toHaveTextContent('Not met yet: The owner decides: Pick the vendor');
    });

    it('reactivates with a reason, by keyboard, and announces the result', async () => {
        service.reactivate.mockResolvedValue({ task: { ...base, status: 'planned', version: 5 }, postponement: record({ open: false }) });
        const { user, onUpdated } = renderPanel(postponed);
        await screen.findByText('Waiting on the vendor');
        const button = screen.getByRole('button', { name: 'Reactivate' });
        expect(button).toBeDisabled();
        expect(button).toHaveAccessibleDescription('Add a reason to reactivate.');
        expect(screen.getByText(/returns this work to Planned now/)).toBeInTheDocument();
        const reason = screen.getByRole('textbox', { name: /Reason for reactivating/ });
        for (let step = 0; step < 40 && document.activeElement !== reason; step += 1) await user.tab();
        expect(reason).toHaveFocus();
        await user.keyboard('The vendor replied');
        await user.tab();
        expect(button).toHaveFocus();
        await user.keyboard('{Enter}');
        await waitFor(() => expect(service.reactivate).toHaveBeenCalledWith(42, { expected_version: 4, reason: 'The vendor replied' }));
        await waitFor(() => expect(onUpdated).toHaveBeenCalled());
        expect(await screen.findByText('Reactivated “Ship the importer”.')).toBeInTheDocument();
    });

    it('shows the panel but no Reactivate action to a person without authority', async () => {
        service.actions.mockResolvedValue(allowed());
        renderPanel(postponed, identity({ workspace_role: 'member' }));
        expect(await screen.findByText('Waiting on the vendor')).toBeInTheDocument();
        expect(screen.queryByRole('button', { name: 'Reactivate' })).not.toBeInTheDocument();
        expect(screen.queryByRole('textbox', { name: /Reason for reactivating/ })).not.toBeInTheDocument();
    });

    it('lets the workspace owner record an owner decision', async () => {
        service.recordOwnerDecision.mockResolvedValue({ task: postponed, postponement: record() });
        const { user, onUpdated } = renderPanel(postponed);
        const decision = await screen.findByRole('textbox', { name: /What the owner decided/ });
        const button = screen.getByRole('button', { name: 'Record decision' });
        expect(button).toBeDisabled();
        expect(button).toHaveAccessibleDescription('Write the decision to record it.');
        await user.type(decision, 'Vendor A');
        await user.click(button);
        await waitFor(() => expect(service.recordOwnerDecision).toHaveBeenCalledWith(42, 12, { expected_version: 4, decision: 'Vendor A' }));
        await waitFor(() => expect(onUpdated).toHaveBeenCalled());
        expect(await screen.findByText('Recorded the owner decision for “Ship the importer”.')).toBeInTheDocument();
    });

    it.each([
        ['a project manager who is not the workspace owner', identity({ workspace_role: 'member' })],
        ['a paired observer', identity({ access: 'observe' })],
        ['a trusted-local paired observer', identity({ principal: null, mode: 'trusted_local', access: 'observe' })],
    ])('does not offer the owner decision to %s', async (_name, who) => {
        renderPanel(postponed, who);
        await screen.findByText('Waiting on the vendor');
        expect(screen.queryByRole('button', { name: 'Record decision' })).not.toBeInTheDocument();
        expect(screen.getByText('Only the workspace owner can record this decision.')).toBeInTheDocument();
    });

    it('lets a trusted-local browser record the owner decision, and shows a met requirement at the same version', async () => {
        const met = record({ requirements: record().requirements.map(item => item.id === 12 ? { ...item, met: true, met_at: '2026-11-27T09:00:00Z' } : item) });
        service.recordOwnerDecision.mockImplementation(async () => { service.getDetail.mockResolvedValue({ task: postponed, reviewer_name: null, postponement: met }); return { task: postponed, postponement: met }; });
        const { user } = renderPanel(postponed, identity({ principal: null, mode: 'trusted_local', workspace_role: null }));
        await user.type(await screen.findByRole('textbox', { name: /What the owner decided/ }), 'Vendor A');
        await user.click(screen.getByRole('button', { name: 'Record decision' }));
        await waitFor(() => expect(service.recordOwnerDecision).toHaveBeenCalled());
        await waitFor(() => expect(screen.getByText(/The owner decides: Pick the vendor/).closest('li')).toHaveTextContent('Met:'));
        expect(screen.queryByRole('button', { name: 'Record decision' })).not.toBeInTheDocument();
    });

    it('still offers Reactivate when no postponement record exists', async () => {
        service.getDetail.mockResolvedValue({ task: postponed, reviewer_name: null, postponement: null });
        renderPanel(postponed);
        expect(await screen.findByText('No reason or requirements were recorded for this postponement.')).toBeInTheDocument();
        expect(screen.getByRole('button', { name: 'Reactivate' })).toBeInTheDocument();
    });

    it('names a deleted requirement target without breaking', async () => {
        service.getDetail.mockResolvedValue({ task: postponed, reviewer_name: null, postponement: record({ requirements: [
            { id: 10, position: 0, kind: 'predecessor_accepted', task_id: null, triage_item_id: null, on_date: null, description: null, met: false, met_at: null }] }) });
        renderPanel(postponed);
        expect(await screen.findByText(/A task or triage item that was deleted/)).toBeInTheDocument();
    });

    it('is written in Russian too', async () => {
        await ensureLanguageResources('ru');
        await i18n.changeLanguage('ru');
        renderPanel(postponed);
        expect((await screen.findAllByText('Выполнено:', { exact: false })).length).toBeGreaterThan(0);
        expect(screen.getByRole('button', { name: 'Возобновить' })).toBeInTheDocument();
        expect(screen.queryByText(/domain\./)).not.toBeInTheDocument();
        await i18n.changeLanguage('en');
    });
});

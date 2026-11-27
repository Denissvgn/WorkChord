import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { screen, waitFor } from '@testing-library/react';
import { renderWithProviders } from '../../test/renderWithProviders';
import type { Task } from '../../types/task';
import { emptyTaskBrief } from './taskEditorContract';
import i18n, { ensureLanguageResources } from '../../i18n/i18n';
import { TaskWorkPanel } from './TaskWorkPanel';

const service = vi.hoisted(() => ({ actions: vi.fn(), progress: vi.fn(), command: vi.fn(), review: vi.fn(), getDetail: vi.fn(), reviews: vi.fn().mockResolvedValue([]) }));
vi.mock('../../services/taskService', () => ({ taskService: service }));
vi.mock('../../services/iterationService', () => ({ iterationService: { getAll: vi.fn().mockResolvedValue([]) } }));

const task: Task = {
    id: 42, iteration_id: null, project_id: 2, title: 'Human work', priority: 5, effort_days: null, effort_hours: null,
    status: 'active', execution_mode: 'manual', is_overdue: false, is_delayed: false, is_composite: false,
    is_optional: false, is_deferred: false, tags: [], sort_order: 0, external_links: [], request_count: 0,
    agent_readiness: { is_ready: false, blockers: [], warnings: [], criteria: [] }, version: 3, children: [], dependencies: [],
    brief_revision: 1, artifact_revision: 0,
    brief: { ...emptyTaskBrief(), acceptance_criteria: [{ id: 'criterion', revision: 1, text: 'Inspect the result', verification: '' }] },
};

const renderPanel = () => renderWithProviders(<TaskWorkPanel task={task} disabled={false} draftKey="workchord-draft:person:42"
    onDirty={vi.fn()} onPending={vi.fn()} onUpdated={vi.fn()} onReload={vi.fn()} />);

describe('criterion progress saves', () => {
    beforeEach(() => {
        sessionStorage.clear();
        vi.clearAllMocks();
        service.actions.mockResolvedValue({ task_id: 42, version: 3, actions: [], claim_generation: 0, running_run_ids: [], live_assignment_ids: [] });
    });

    it('retains evidence after a save conflict and uses the displayed task version', async () => {
        service.progress.mockRejectedValue({ response: { status: 409, data: { detail: { message: 'Another editor changed this work' } } } });
        const { user } = renderPanel();
        await user.selectOptions(screen.getByLabelText('Inspect the result'), 'completed');
        await user.type(screen.getByRole('textbox', { name: 'Evidence' }), 'Observed the result directly');
        await user.click(screen.getByRole('button', { name: 'Save progress' }));
        await screen.findByText('Another editor changed this work');
        expect(screen.getByRole('textbox', { name: 'Evidence' })).toHaveValue('Observed the result directly');
        expect(service.progress).toHaveBeenCalledWith(42, expect.objectContaining({ expected_version: 3, criteria: [
            { criterion_id: 'criterion', criterion_revision: 1, state: 'completed', evidence: 'Observed the result directly' },
        ] }));
        expect(service.review).not.toHaveBeenCalled();
    });

    it('requires explicit review before reapplying a stale saved evidence draft', async () => {
        sessionStorage.setItem('workchord-draft:person:42:progress', JSON.stringify({ version: 2, savedAt: Date.now(), criteria: [
            { criterion_id: 'criterion', criterion_revision: 1, state: 'completed', evidence: 'Saved evidence draft' },
        ] }));
        service.progress.mockResolvedValue(task);
        const { user } = renderPanel();
        expect(screen.getByRole('textbox', { name: 'Evidence' })).toHaveValue('Saved evidence draft');
        expect(screen.getByRole('button', { name: 'Save progress' })).toBeDisabled();
        await user.click(screen.getByRole('button', { name: 'Keep draft with current version' }));
        await user.click(screen.getByRole('button', { name: 'Save progress' }));
        await waitFor(() => expect(service.progress).toHaveBeenCalledWith(42, expect.objectContaining({ expected_version: 3 })));
    });

    it('lists the current criteria with no stale-draft warning after a brief change', async () => {
        // A draft taken while the brief had no criteria, before a criterion was added.
        sessionStorage.setItem('workchord-draft:person:42:progress', JSON.stringify({ version: 2, savedAt: Date.now(), criteria: [], base: [],
            reason: 'Checked the output', action: '' }));
        renderPanel();
        expect(screen.queryByText(/This progress draft belongs to an older version/)).not.toBeInTheDocument();
        expect(screen.queryByText('No acceptance criteria yet.')).not.toBeInTheDocument();
        expect(screen.getByLabelText('Inspect the result')).toHaveValue('pending');
        expect(screen.getByRole('textbox', { name: /Reason for the action or review/ })).toHaveValue('Checked the output');
        await waitFor(() => expect(JSON.parse(sessionStorage.getItem('workchord-draft:person:42:progress')!).version).toBe(3));
    });

    it('keeps evidence for an unchanged criterion across a brief change and saves it with the current version', async () => {
        sessionStorage.setItem('workchord-draft:person:42:progress', JSON.stringify({ version: 2, savedAt: Date.now(),
            criteria: [
                { criterion_id: 'criterion', criterion_revision: 1, state: 'completed', evidence: 'Saw it work' },
                { criterion_id: 'removed', criterion_revision: 1, state: 'completed', evidence: 'No longer in the brief' },
            ],
            base: [
                { criterion_id: 'criterion', criterion_revision: 1, state: 'pending', evidence: '' },
                { criterion_id: 'removed', criterion_revision: 1, state: 'pending', evidence: '' },
            ] }));
        service.progress.mockResolvedValue(task);
        const { user } = renderPanel();
        expect(screen.queryByText(/This progress draft belongs to an older version/)).not.toBeInTheDocument();
        expect(screen.queryByText('Criterion removed from the current brief')).not.toBeInTheDocument();
        expect(screen.getByRole('textbox', { name: 'Evidence' })).toHaveValue('Saw it work');
        await user.click(screen.getByRole('button', { name: 'Save progress' }));
        await waitFor(() => expect(service.progress).toHaveBeenCalledWith(42, expect.objectContaining({ expected_version: 3, criteria: [
            { criterion_id: 'criterion', criterion_revision: 1, state: 'completed', evidence: 'Saw it work' },
        ] })));
    });

    it('shows the cleared server progress for an untouched criterion after a brief change, with no stale-draft warning', async () => {
        // Progress was saved, a review reason was begun, and then a brief edit cleared the saved progress on the server.
        const recorded = { criterion_id: 'criterion', criterion_revision: 1, state: 'completed' as const, evidence: 'Saw it work' };
        sessionStorage.setItem('workchord-draft:person:42:progress', JSON.stringify({ version: 2, savedAt: Date.now(),
            criteria: [recorded], base: [recorded], reason: 'Checked the output', action: '' }));
        renderPanel();
        expect(screen.queryByText(/This progress draft belongs to an older version/)).not.toBeInTheDocument();
        expect(screen.getByLabelText('Inspect the result')).toHaveValue('pending');
        expect(screen.getByRole('textbox', { name: 'Evidence' })).toHaveValue('');
        // Review controls stay usable: a stale draft would disable them.
        await waitFor(() => expect(screen.getByRole('textbox', { name: /Reason for the action or review/ })).toBeEnabled());
        expect(screen.getByRole('textbox', { name: /Reason for the action or review/ })).toHaveValue('Checked the output');
        await waitFor(() => expect(JSON.parse(sessionStorage.getItem('workchord-draft:person:42:progress')!).version).toBe(3));
    });

    it('keeps the server value for an untouched criterion that another person saved', () => {
        const recorded = { ...task, progress: { criteria: [{ criterion_id: 'criterion', criterion_revision: 1, state: 'in_progress' as const, evidence: 'Recorded elsewhere' }], artifacts: [], brief_revision: 1, artifact_revision: 0 } } as Task;
        const pending = { criterion_id: 'criterion', criterion_revision: 1, state: 'pending' as const, evidence: '' };
        sessionStorage.setItem('workchord-draft:person:42:progress', JSON.stringify({ version: 2, savedAt: Date.now(),
            criteria: [pending], base: [pending], reason: 'Checked the output', action: '' }));
        renderWithProviders(<TaskWorkPanel task={recorded} disabled={false} draftKey="workchord-draft:person:42"
            onDirty={vi.fn()} onPending={vi.fn()} onUpdated={vi.fn()} onReload={vi.fn()} />);
        expect(screen.queryByText(/This progress draft belongs to an older version/)).not.toBeInTheDocument();
        expect(screen.getByLabelText('Inspect the result')).toHaveValue('in_progress');
        expect(screen.getByRole('textbox', { name: 'Evidence' })).toHaveValue('Recorded elsewhere');
    });

    it('still warns when the saved progress of an edited criterion changed on the server', () => {
        const recorded = { ...task, progress: { criteria: [{ criterion_id: 'criterion', criterion_revision: 1, state: 'in_progress' as const, evidence: 'Recorded elsewhere' }], artifacts: [], brief_revision: 1, artifact_revision: 0 } } as Task;
        sessionStorage.setItem('workchord-draft:person:42:progress', JSON.stringify({ version: 2, savedAt: Date.now(),
            criteria: [{ criterion_id: 'criterion', criterion_revision: 1, state: 'completed', evidence: 'My evidence' }],
            base: [{ criterion_id: 'criterion', criterion_revision: 1, state: 'pending', evidence: '' }] }));
        renderWithProviders(<TaskWorkPanel task={recorded} disabled={false} draftKey="workchord-draft:person:42"
            onDirty={vi.fn()} onPending={vi.fn()} onUpdated={vi.fn()} onReload={vi.fn()} />);
        expect(screen.getByText(/This progress draft belongs to an older version/)).toBeInTheDocument();
        expect(screen.getByRole('button', { name: 'Save progress' })).toBeDisabled();
    });
});


it('keeps the initial aggregate map through a failed uncommit and explicit current comparison', async () => {
    sessionStorage.clear();
    const committed = { ...task, iteration_id: 1, iteration_revision: 4 };
    service.actions.mockResolvedValue({ task_id: 42, version: 3, actions: [{ action: 'uncommit', allowed: true, blockers: [] }], claim_generation: 0, running_run_ids: [], live_assignment_ids: [] });
    service.command.mockRejectedValue({ response: { status: 409, data: { detail: { message: 'Planning scope changed' } } } });
    const props = { disabled: false, draftKey: 'scoped-command', onDirty: vi.fn(), onPending: vi.fn(), onUpdated: vi.fn(), onReload: vi.fn() };
    const view = renderWithProviders(<TaskWorkPanel {...props} task={committed} />);
    await view.user.selectOptions(await screen.findByLabelText('Action'), 'uncommit');
    await view.user.type(screen.getByRole('textbox', { name: 'Reason for the action or review'  }), 'Keep this reason');
    view.rerender(<TaskWorkPanel {...props} task={{ ...committed, iteration_revision: 99 }} />);
    await view.user.click(screen.getByRole('button', { name: 'Apply action' }));
    await screen.findByText('Planning scope changed');
    expect(service.command.mock.lastCall?.[1].expected_revisions).toEqual({ 1: 4 });
    expect(screen.getByRole('textbox', { name: 'Reason for the action or review'  })).toHaveValue('Keep this reason');
    expect(JSON.parse(sessionStorage.getItem('scoped-command:progress')!).commandRevisions).toEqual({ 1: 4 });
    service.getDetail.mockResolvedValue({ task: { ...committed, iteration_revision: 99 } });
    await view.user.click(screen.getByRole('button', { name: 'Review current inputs' }));
    await waitFor(() => expect(JSON.parse(sessionStorage.getItem('scoped-command:progress')!).commandRevisions).toEqual({ 1: 99 }));
    expect(screen.getByRole('textbox', { name: 'Reason for the action or review'  })).toHaveValue('Keep this reason');
});

describe('unavailable actions', () => {
    afterEach(async () => { await i18n.changeLanguage('en'); });

    it.each([
        ['en', 'Postpone', 'Reactivate'],
        ['ru', 'Отложить', 'Возобновить'],
    ])('names postpone and reactivate in %s', async (language, postpone, reactivate) => {
        await ensureLanguageResources(language);
        await i18n.changeLanguage(language);
        service.actions.mockResolvedValue({ task_id: 42, version: 3, actions: [
            { action: 'postpone', allowed: false, blockers: [{ code: 'permission_denied', message: 'Project manage permission is required.' }] },
            { action: 'reactivate', allowed: false, blockers: [{ code: 'not_postponed', message: 'Only postponed work can be reactivated.' }] },
        ], claim_generation: 0, running_run_ids: [], live_assignment_ids: [] });
        renderPanel();
        expect(await screen.findByText(postpone)).toBeInTheDocument();
        expect(screen.getByText(reactivate)).toBeInTheDocument();
        expect(screen.queryByText(/domain\.action_/)).not.toBeInTheDocument();
    });
});

describe('review by a person', () => {
    const resolved: Task = { ...task, status: 'resolved', assignee: { id: 7, name: 'Sam' } };
    beforeEach(() => {
        sessionStorage.clear();
        vi.clearAllMocks();
        service.actions.mockResolvedValue({ task_id: 42, version: 3, actions: [
            { action: 'review', allowed: true, blockers: [] }, { action: 'accept_review', allowed: true, blockers: [] },
        ], claim_generation: 0, running_run_ids: [], live_assignment_ids: [] });
        service.getDetail.mockResolvedValue({ task: resolved, reviewer_name: 'Independent Verification Runtime' });
        service.review.mockResolvedValue({ ...resolved, status: 'active', version: 4 });
    });

    afterEach(async () => { await i18n.changeLanguage('en'); });

    it.each(['en', 'ru'])('names missing acceptance requirements beside Accept in %s', async language => {
        await ensureLanguageResources(language);
        await i18n.changeLanguage(language);
        const { user } = renderPanel2(resolved);
        const accept = screen.getByRole('button', { name: i18n.t('domain.accept') });
        await waitFor(() => expect(screen.getByLabelText(i18n.t('domain.resultFor', { criterion: 'Inspect the result' }))).toBeEnabled());
        expect(accept).toBeDisabled();
        expect(accept).toHaveAccessibleDescription(expect.stringContaining(i18n.t('domain.acceptNeedsReason')));
        expect(accept).toHaveAccessibleDescription(expect.stringContaining(i18n.t('domain.acceptNeedsResults')));
        const result = screen.getByLabelText(i18n.t('domain.resultFor', { criterion: 'Inspect the result' }));
        await user.selectOptions(result, 'pass');
        expect(accept).toHaveAccessibleDescription(i18n.t('domain.acceptNeedsReason'));
        const reason = screen.getByRole('textbox', { name: i18n.t('domain.reason') });
        expect(result.compareDocumentPosition(reason) & Node.DOCUMENT_POSITION_FOLLOWING).toBeTruthy();
        await user.type(reason, '   ');
        expect(accept).toBeDisabled();
        await user.type(reason, 'Checked the result');
        expect(accept).toBeEnabled();
        expect(accept).not.toHaveAttribute('aria-describedby');
    });

    it('shows server acceptance blockers beside Accept', async () => {
        service.actions.mockResolvedValue({ actions: [
            { action: 'review', allowed: true, blockers: [] },
            { action: 'accept_review', allowed: false, blockers: [{ message: 'Only the assigned reviewer can accept.' }] },
        ] });
        renderPanel2(resolved);
        const accept = screen.getByRole('button', { name: 'Accept' });
        await waitFor(() => expect(accept).toHaveAccessibleDescription(expect.stringContaining('Only the assigned reviewer can accept.')));
        expect(accept).toBeDisabled();
    });

    it.each(['en', 'ru'])('ends every server blocker beside Accept with its own full stop in %s', async language => {
        await ensureLanguageResources(language);
        await i18n.changeLanguage(language);
        service.actions.mockResolvedValue({ actions: [
            { action: 'review', allowed: true, blockers: [] },
            { action: 'accept_review', allowed: false, blockers: [
                { message: 'Only the assigned reviewer can accept' },
                { message: 'Attach the test run!' },
                { message: 'Is the evidence complete?' },
            ] },
        ] });
        renderPanel2(resolved);
        const accept = screen.getByRole('button', { name: i18n.t('domain.accept') });
        await waitFor(() => expect(accept).toHaveAccessibleDescription(expect.stringContaining('Only the assigned reviewer can accept.')));
        expect(accept).toHaveAccessibleDescription(expect.stringContaining('Only the assigned reviewer can accept. Attach the test run. Is the evidence complete.'));
        expect(accept).not.toHaveAccessibleDescription(expect.stringMatching(/[!?]|\.\./));
        expect(accept).toBeDisabled();
    });

    it('names the reviewer and the rework owner', async () => {
        renderPanel2(resolved);
        expect(await screen.findByText('Independent Verification Runtime')).toBeInTheDocument();
        expect(screen.getByText(/Rework goes to Sam/)).toBeInTheDocument();
    });

    it('sends a result per criterion and needs a failing criterion to request changes', async () => {
        const { user } = renderPanel2(resolved);
        await user.type(await screen.findByRole('textbox', { name: 'Reason for the action or review' }), 'The output is missing a section');
        const requestChanges = screen.getByRole('button', { name: 'Request changes' });
        expect(requestChanges).toBeDisabled();
        expect(screen.getByRole('button', { name: 'Accept' })).toBeDisabled();
        await user.selectOptions(await screen.findByLabelText('Result: Inspect the result'), 'fail');
        await user.type(screen.getByRole('textbox', { name: 'What you checked or what must change' }), 'Add the summary section');
        await user.click(requestChanges);
        await waitFor(() => expect(service.review).toHaveBeenCalled());
        const payload = service.review.mock.lastCall?.[1];
        expect(payload.verdict).toBe('reject');
        expect(JSON.parse(payload.evidence)).toEqual({ criteria: [
            { id: 'criterion', revision: 1, result: 'fail', note: 'Add the summary section' },
        ] });
    });
});

function renderPanel2(current: Task) {
    return renderWithProviders(<TaskWorkPanel task={current} disabled={false} draftKey={null}
        onDirty={vi.fn()} onPending={vi.fn()} onUpdated={vi.fn()} onReload={vi.fn()} />);
}

describe('acceptance requirements and who decides', () => {
    const actionsFor = (version: number) => ({ task_id: 42, version, claim_generation: 0, running_run_ids: [], live_assignment_ids: [],
        actions: [{ action: 'resolve_manual', allowed: true, blockers: [] }, { action: 'accept_review', allowed: true, blockers: [] }, { action: 'review', allowed: true, blockers: [] }] });
    const panel = (current: Task, onEditBrief = vi.fn()) => ({ onEditBrief, ...renderWithProviders(<TaskWorkPanel task={current} disabled={false} draftKey={null}
        onDirty={vi.fn()} onPending={vi.fn()} onUpdated={vi.fn()} onReload={vi.fn()} onEditBrief={onEditBrief} />) });

    beforeEach(() => { vi.clearAllMocks(); service.actions.mockResolvedValue(actionsFor(3)); });

    it('blocks submitting for review without an acceptance criterion and offers Edit brief', async () => {
        const noCriteria = { ...task, brief: { ...emptyTaskBrief(), acceptance_criteria: [] } };
        const { user, onEditBrief } = panel(noCriteria);
        expect(screen.getByRole('alert')).toHaveTextContent('Add at least one acceptance criterion before submitting for review.');
        await user.type(await screen.findByRole('textbox', { name: /Reason/ }), 'Done');
        await waitFor(() => expect(screen.getByRole('combobox', { name: 'Action' })).toBeEnabled());
        await user.selectOptions(screen.getByRole('combobox', { name: 'Action' }), 'resolve_manual');
        expect(screen.getByRole('button', { name: 'Apply action' })).toBeDisabled();
        await user.click(screen.getByRole('button', { name: 'Edit brief' }));
        expect(onEditBrief).toHaveBeenCalled();
        expect(service.command).not.toHaveBeenCalled();
    });

    it('does not show the block when a criterion exists', () => {
        panel(task);
        expect(screen.queryByText(/Add at least one acceptance criterion/)).not.toBeInTheDocument();
    });

    it('says anyone, including the assignee, can accept when no other reviewer is set', async () => {
        service.getDetail.mockResolvedValue({ task: task, reviewer_name: null });
        panel({ ...task, status: 'resolved', assignee: { id: 1, name: 'Sam Ortiz' } } as Task);
        expect(await screen.findByText(/Anyone, including the assignee, can accept\./)).toBeInTheDocument();
        expect(screen.queryByText(/A separate reviewer decides acceptance/)).not.toBeInTheDocument();
    });

    it('says a separate reviewer decides only when the reviewer differs from the assignee', async () => {
        service.getDetail.mockResolvedValue({ task: task, reviewer_name: 'Priya Nair' });
        panel({ ...task, status: 'resolved', assignee: { id: 1, name: 'Sam Ortiz' } } as Task);
        expect(await screen.findByText(/A separate reviewer decides acceptance\./)).toBeInTheDocument();
        expect(screen.queryByText(/Anyone, including the assignee/)).not.toBeInTheDocument();
    });
});

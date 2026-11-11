import { beforeEach, describe, expect, it, vi } from 'vitest';
import { screen, waitFor } from '@testing-library/react';
import { renderWithProviders } from '../../test/renderWithProviders';
import type { Task } from '../../types/task';
import { emptyTaskBrief } from './taskEditorContract';
import { TaskWorkPanel } from './TaskWorkPanel';

const service = vi.hoisted(() => ({ actions: vi.fn(), progress: vi.fn(), command: vi.fn(), review: vi.fn(), getDetail: vi.fn() }));
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

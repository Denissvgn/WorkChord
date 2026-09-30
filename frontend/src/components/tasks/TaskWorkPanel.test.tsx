import { beforeEach, describe, expect, it, vi } from 'vitest';
import { screen, waitFor } from '@testing-library/react';
import { renderWithProviders } from '../../test/renderWithProviders';
import type { Task } from '../../types/task';
import { emptyTaskBrief } from './taskEditorContract';
import { TaskWorkPanel } from './TaskWorkPanel';

const service = vi.hoisted(() => ({ actions: vi.fn(), progress: vi.fn(), command: vi.fn(), review: vi.fn() }));
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

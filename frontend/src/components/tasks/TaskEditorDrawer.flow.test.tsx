import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { screen, waitFor, within } from '@testing-library/react';
import { useLocation } from 'react-router-dom';
import { renderWithProviders } from '../../test/renderWithProviders';
import type { Task, TaskActions, TaskDetail } from '../../types/task';
import { emptyTaskBrief } from './taskEditorContract';
import { TaskEditorDrawer } from './TaskEditorDrawer';

const service = vi.hoisted(() => ({ getDetail: vi.fn(), getById: vi.fn(), actions: vi.fn(), command: vi.fn(), writeBrief: vi.fn(), progress: vi.fn(), review: vi.fn(), lookup: vi.fn(), reviews: vi.fn().mockResolvedValue([]) }));
vi.mock('../../services/taskService', () => ({ taskService: service }));
vi.mock('../../services/iterationService', () => ({ iterationService: { getAll: vi.fn().mockResolvedValue([]) } }));
vi.mock('../../features/identity/identityContext', () => ({ useIdentity: () => ({ identity: { mode: 'trusted_local', principal: null } }) }));
vi.mock('./TaskTimelinePanel', () => ({ TaskTimelinePanel: () => null }));
vi.mock('./TaskDiscussion', () => ({ TaskDiscussion: () => null }));

const criterion = { id: 'preview', revision: 1, text: 'A valid file shows a preview.', verification: '' };
const baseTask = {
    id: 1, title: 'Draft launch checklist', status: 'planned', execution_mode: 'manual', version: 2, priority: 5, effort_days: 1, effort_hours: 8,
    assignee: { id: 1, name: 'Dana Walker' }, owner: null, project_id: null, iteration_id: null, start_date: null, end_date: null,
    dependencies: [], children: [], tags: [], external_links: [], request_count: 0, sort_order: 0,
    is_overdue: false, is_delayed: false, is_composite: false, is_optional: false, is_deferred: false,
    agent_readiness: { is_ready: false, blockers: [], warnings: [], criteria: [] }, brief_revision: 1, artifact_revision: 0,
    brief: { ...emptyTaskBrief(), goal: 'List what launch needs.', acceptance_criteria: [criterion] }, progress: null,
} as unknown as Task;

const detail = (task: Task): TaskDetail => ({
    task, ancestors: [], ancestors_complete: true, execution_context_complete: false, reviewer_name: null,
    children: { items: [], has_more: false, next_after_id: null, limit: 50 },
    dependencies: { items: [], has_more: false, next_after_id: null, limit: 50 },
});
const actionsFor = (task: Task): TaskActions => ({
    task_id: task.id, version: task.version, claim_generation: 0, running_run_ids: [], live_assignment_ids: [],
    actions: [
        { action: 'start_manual', allowed: task.status === 'planned', blockers: [] },
        { action: 'resolve_manual', allowed: task.status === 'active', blockers: [] },
        { action: 'block', allowed: true, blockers: [] },
        { action: 'review', allowed: task.status === 'resolved', blockers: [] },
        { action: 'accept_review', allowed: task.status === 'resolved', blockers: [] },
        { action: 'record_progress', allowed: true, blockers: [] },
    ],
});

let current: Task;
const serve = (task: Task) => { current = task; return task; };
let consoleError: { mock: { calls: unknown[][] }; mockRestore: () => void };
const duplicateKeyWarnings = () => consoleError.mock.calls.filter(call => call.some(part => typeof part === 'string' && part.includes('same key')));

beforeEach(() => {
    sessionStorage.clear();
    vi.clearAllMocks();
    consoleError = vi.spyOn(console, 'error');
    service.getDetail.mockImplementation(async () => detail(current));
    service.getById.mockImplementation(async () => current);
    service.actions.mockImplementation(async () => actionsFor(current));
});
afterEach(() => consoleError.mockRestore());

const openDrawer = (task: Task) => {
    serve(task);
    return renderWithProviders(<TaskEditorDrawer taskId={task.id} open onClose={vi.fn()} />, { initialEntries: [`/my-work?task=${task.id}`] });
};
const drawer = () => screen.getByRole('dialog');
const enabledButton = async (name: string) => {
    const button = await within(drawer()).findByRole('button', { name });
    await waitFor(() => expect(button).toBeEnabled());
    return button;
};

describe('task drawer start, submit and review', () => {
    it('starts and submits from the header in one click each and logs no duplicate-key warning', async () => {
        service.command.mockImplementation(async (_id: number, command: { action: string; expected_version: number }) => serve({
            ...current, status: command.action === 'start_manual' ? 'active' : 'resolved', version: command.expected_version + 1,
        }));
        const { user } = openDrawer(baseTask);
        await user.click(await enabledButton('Start work'));
        await user.click(await enabledButton('Submit for review'));
        expect(await within(drawer()).findByText('Resolved')).toBeInTheDocument();
        expect(service.command.mock.calls.map(call => [call[1].action, call[1].reason])).toEqual([
            ['start_manual', 'Started from the task view.'],
            ['resolve_manual', 'Submitted for review from the task view.'],
        ]);
        expect(within(drawer()).queryByText('Save or discard your edits to change status.')).not.toBeInTheDocument();
        await user.click(await enabledButton('Review'));
        expect(await within(drawer()).findByLabelText('Result: A valid file shows a preview.')).toBeInTheDocument();
        expect(duplicateKeyWarnings()).toEqual([]);
    });

    it('lists the cleared progress in Review after a goal-only brief change, with no stale-draft warning', async () => {
        const progress = { criteria: [{ criterion_id: criterion.id, criterion_revision: 1, state: 'completed', evidence: 'Preview shown.' }], artifacts: [], brief_revision: 1, artifact_revision: 0 };
        const resolved = { ...baseTask, status: 'resolved', version: 3, progress } as Task;
        // Saving a brief clears saved progress on the server.
        service.writeBrief.mockImplementation(async (_id: number, version: number, brief: Task['brief']) => serve({ ...current, version: version + 1, brief, progress: null }));
        const { user } = openDrawer(resolved);
        await user.click(await enabledButton('Review'));
        expect(await within(drawer()).findByLabelText(criterion.text)).toHaveValue('completed');
        await user.type(within(drawer()).getByRole('textbox', { name: /Reason for the action or review/ }), 'Checked the checklist');
        await user.click(within(drawer()).getByRole('button', { name: 'Brief' }));
        await user.click(within(drawer()).getByRole('button', { name: 'Edit brief' }));
        const goal = within(drawer()).getByRole('textbox', { name: 'Goal' });
        await user.clear(goal);
        await user.type(goal, 'List every step launch needs.');
        await user.click(within(drawer()).getByRole('button', { name: 'Save brief' }));
        await waitFor(() => expect(service.writeBrief).toHaveBeenCalledWith(1, 3, expect.anything()));

        await user.click(await enabledButton('Review'));
        expect(await within(drawer()).findByLabelText(`Result: ${criterion.text}`)).toBeEnabled();
        expect(within(drawer()).getByLabelText(criterion.text)).toHaveValue('pending');
        expect(within(drawer()).queryByText(/This progress draft belongs to an older version/)).not.toBeInTheDocument();
        expect(within(drawer()).getByRole('textbox', { name: /Reason for the action or review/ })).toBeEnabled();
        expect(within(drawer()).getByRole('textbox', { name: /Reason for the action or review/ })).toHaveValue('Checked the checklist');
        expect(duplicateKeyWarnings()).toEqual([]);
    });

    it('lists the current criteria in Review after a brief change, with no stale-draft warning', async () => {
        const resolved = { ...baseTask, status: 'resolved', version: 3, brief: { ...baseTask.brief!, acceptance_criteria: [] } } as Task;
        service.writeBrief.mockImplementation(async (_id: number, version: number, brief: Task['brief']) => serve({ ...current, version: version + 1, brief }));
        const { user } = openDrawer(resolved);
        // Begin a review, which keeps a local draft of the reason, then fix the brief.
        await user.click(await enabledButton('Review'));
        await user.type(await within(drawer()).findByRole('textbox', { name: /Reason for the action or review/ }), 'Checked the checklist');
        await user.click(within(drawer()).getByRole('button', { name: 'Brief' }));
        await user.click(within(drawer()).getByRole('button', { name: 'Edit brief' }));
        await user.click(within(drawer()).getByRole('button', { name: 'Add criterion' }));
        await user.type(within(drawer()).getByRole('textbox', { name: 'Criterion 1' }), 'Every launch step has an owner.');
        await user.click(within(drawer()).getByRole('button', { name: 'Save brief' }));
        await waitFor(() => expect(service.writeBrief).toHaveBeenCalledWith(1, 3, expect.anything()));

        await user.click(await enabledButton('Review'));
        expect(await within(drawer()).findByLabelText('Result: Every launch step has an owner.')).toBeInTheDocument();
        expect(within(drawer()).getByLabelText('Every launch step has an owner.')).toBeInTheDocument();
        expect(within(drawer()).queryByText(/This progress draft belongs to an older version/)).not.toBeInTheDocument();
        expect(within(drawer()).queryByText('No acceptance criteria yet.')).not.toBeInTheDocument();
        expect(within(drawer()).getByRole('textbox', { name: /Reason for the action or review/ })).toHaveValue('Checked the checklist');
        expect(duplicateKeyWarnings()).toEqual([]);
    });
});

describe('task drawer for superseded work', () => {
    it('opens the successor from a page that is not Tasks: closes, then goes to the Tasks page with the successor', async () => {
        const onClose = vi.fn();
        const Where = () => <output data-testid="where">{useLocation().pathname + useLocation().search}</output>;
        serve({ ...baseTask, displayed_state: 'superseded', successor_task_id: 77, successor_kind: 'supersession' } as unknown as Task);
        const { user } = renderWithProviders(<><TaskEditorDrawer taskId={1} open onClose={onClose} /><Where /></>, { initialEntries: ['/gantt?iteration=3&task=1'] });
        await user.click(await within(drawer()).findByRole('button', { name: 'Superseded by #77' }));
        expect(onClose).toHaveBeenCalled();
        expect(screen.getByTestId('where')).toHaveTextContent('/tasks');
        expect(screen.getByTestId('where')).toHaveTextContent('task=77');
    });
});

import { beforeEach, describe, expect, it, vi } from 'vitest';
import { screen, waitFor } from '@testing-library/react';
import { useLocation } from 'react-router-dom';
import { renderWithProviders } from '../../test/renderWithProviders';
import type { Task } from '../../types/task';
import { emptyTaskBrief } from './taskEditorContract';
import { TaskReadView } from './TaskReadView';

const service = vi.hoisted(() => ({ writeBrief: vi.fn(), actions: vi.fn(), command: vi.fn(), reviews: vi.fn().mockResolvedValue([]) }));
vi.mock('../../services/taskService', () => ({ taskService: service }));
vi.mock('../../services/teamService', () => ({ teamService: { getByIteration: vi.fn().mockResolvedValue([]) } }));
vi.mock('./TaskWorkPanel', () => ({ TaskWorkPanel: () => <p>Work panel</p> }));
vi.mock('./DeliveryDependencies', () => ({ DeliveryDependencies: () => null }));
vi.mock('./GitHubReconciliationPanel', () => ({ GitHubReconciliationPanel: () => <p>Reconciliation panel</p> }));
vi.mock('./TaskDiscussion', () => ({ TaskDiscussion: () => <p>Discussion</p> }));
vi.mock('./TimeEntriesPanel', () => ({ TimeEntriesPanel: () => null }));
vi.mock('./TaskTimelinePanel', () => ({ TaskTimelinePanel: () => <p>History</p> }));

const task = {
    id: 312, title: 'Import holidays from a CSV file', status: 'active', version: 4, priority: 2, effort_days: 3,
    assignee: { id: 7, name: 'Sam Ortiz' }, owner: { id: 3, name: 'Priya Nair' }, end_date: '2026-11-21', start_date: '2026-11-17',
    project_id: 1, iteration_id: 2, dependencies: [298], children: [], tags: [], is_overdue: false, is_delayed: false,
    is_composite: false, is_optional: false, is_deferred: false, sort_order: 0, external_links: [], request_count: 0,
    agent_readiness: { is_ready: false, blockers: [], warnings: [], criteria: [] }, effort_hours: null,
    brief: { ...emptyTaskBrief(), goal: 'Load a year of holidays from a CSV file.', scope: 'One CSV with date and name columns.',
        acceptance_criteria: [
            { id: 'preview', revision: 1, text: 'A valid file shows a preview.', verification: '' },
            { id: 'errors', revision: 1, text: 'An invalid row names its line.', verification: '' },
        ] },
    progress: { criteria: [{ criterion_id: 'preview', criterion_revision: 1, state: 'completed', evidence: 'Screenshot' }], artifacts: [], brief_revision: 1, artifact_revision: 0 },
} as unknown as Task;

const Location = () => <p data-testid="location">{useLocation().search}</p>;

const renderView = (overrides: Partial<Parameters<typeof TaskReadView>[0]> = {}) => renderWithProviders(<>
    <TaskReadView task={task} draftKey={null} onTaskUpdated={vi.fn()} onEditAll={vi.fn()} onDirty={vi.fn()} onPending={vi.fn()} onReload={vi.fn()} {...overrides} />
    <Location />
</>, { initialEntries: ['/tasks?task=312'] });

const actionsAllowing = (...allowed: string[]) => ({ task_id: 312, version: 4, claim_generation: 0, running_run_ids: [], live_assignment_ids: [],
    actions: ['start_manual', 'resolve_manual', 'review'].map(action => ({ action, allowed: allowed.includes(action), blockers: [] })) });

beforeEach(() => {
    vi.clearAllMocks();
    service.actions.mockResolvedValue(actionsAllowing('resolve_manual'));
});

describe('read-first task view', () => {
    it('reads the brief without any input and links to the evidence', () => {
        renderView();
        expect(screen.getByText('Load a year of holidays from a CSV file.')).toBeInTheDocument();
        expect(screen.queryByRole('textbox')).not.toBeInTheDocument();
        expect(screen.getByRole('button', { name: 'Work & review · 1 of 2 criteria' })).toBeInTheDocument();
        expect(screen.getByText('Sam Ortiz')).toBeInTheDocument();
    });

    it('keeps the part in the URL', async () => {
        const { user } = renderView();
        await user.click(screen.getByRole('button', { name: 'Work & review · 1 of 2 criteria' }));
        expect(screen.getByText('Work panel')).toBeInTheDocument();
        expect(screen.getByText('Reconciliation panel')).toBeInTheDocument();
        expect(screen.getByTestId('location')).toHaveTextContent('task=312&part=work');
        await user.click(screen.getByRole('button', { name: 'Activity' }));
        expect(screen.getByText('Discussion')).toBeInTheDocument();
    });

    it('edits only the brief, pauses the status change, and saves with the task version', async () => {
        const onTaskUpdated = vi.fn();
        service.writeBrief.mockResolvedValue({ ...task, version: 5 });
        const { user } = renderView({ onTaskUpdated });
        await user.click(screen.getByRole('button', { name: 'Edit brief' }));
        expect(screen.getByText('Save or discard your edits to change status.')).toBeInTheDocument();
        expect(screen.getByRole('button', { name: 'Submit for review' })).toBeDisabled();
        await user.click(screen.getByRole('button', { name: 'Save brief' }));
        await waitFor(() => expect(service.writeBrief).toHaveBeenCalledWith(312, 4, expect.objectContaining({ goal: 'Load a year of holidays from a CSV file.' })));
        await waitFor(() => expect(onTaskUpdated).toHaveBeenCalledWith(expect.objectContaining({ version: 5 })));
    });
});

describe('header status change', () => {
    const planned = { ...task, status: 'planned' } as Task;

    it('starts a planned task in one click when no reason is required', async () => {
        const onTaskUpdated = vi.fn();
        service.actions.mockResolvedValue(actionsAllowing('start_manual'));
        service.command.mockResolvedValue({ ...planned, status: 'active', version: 5 });
        const { user } = renderView({ task: planned, onTaskUpdated });
        const start = screen.getByRole('button', { name: 'Start work' });
        await waitFor(() => expect(start).toBeEnabled());
        await user.click(start);
        await waitFor(() => expect(onTaskUpdated).toHaveBeenCalledWith(expect.objectContaining({ status: 'active', version: 5 })));
        expect(service.command).toHaveBeenCalledTimes(1);
        expect(service.command).toHaveBeenCalledWith(312, expect.objectContaining({ action: 'start_manual', expected_version: 4, reason: 'Started from the task view.' }));
        expect(screen.queryByRole('textbox')).not.toBeInTheDocument();
        expect(screen.queryByText('Save or discard your edits to change status.')).not.toBeInTheDocument();
        expect(screen.getByTestId('location')).toHaveTextContent('task=312');
        expect(screen.getByTestId('location')).not.toHaveTextContent('part=work');
    });

    it('asks for one inline reason only when the server requires one', async () => {
        const onTaskUpdated = vi.fn();
        service.actions.mockResolvedValue(actionsAllowing('start_manual'));
        service.command
            .mockRejectedValueOnce({ response: { status: 422, data: { detail: [{ type: 'value_error', loc: ['body', 'reason'], msg: 'A reason is required' }] } } })
            .mockResolvedValueOnce({ ...planned, status: 'active', version: 5 });
        const { user } = renderView({ task: planned, onTaskUpdated });
        await waitFor(() => expect(screen.getByRole('button', { name: 'Start work' })).toBeEnabled());
        await user.click(screen.getByRole('button', { name: 'Start work' }));
        const reason = await screen.findByRole('textbox', { name: /Reason for the action or review/ });
        expect(screen.getByText('This change needs a reason. Add one, then confirm.')).toBeInTheDocument();
        expect(screen.queryByText('Save or discard your edits to change status.')).not.toBeInTheDocument();
        expect(screen.queryByRole('alert')).not.toBeInTheDocument();
        await user.type(reason, 'The customer asked us to begin');
        const confirm = screen.getAllByRole('button', { name: 'Start work' }).find(button => button.getAttribute('type') === 'submit')!;
        await user.click(confirm);
        await waitFor(() => expect(onTaskUpdated).toHaveBeenCalledWith(expect.objectContaining({ status: 'active' })));
        expect(service.command).toHaveBeenCalledTimes(2);
        expect(service.command.mock.lastCall?.[1]).toEqual(expect.objectContaining({ action: 'start_manual', reason: 'The customer asked us to begin' }));
        expect(screen.queryByRole('textbox')).not.toBeInTheDocument();
    });

    it('shows a refusal that is not about the reason inline, without a reason field', async () => {
        service.actions.mockResolvedValue(actionsAllowing('start_manual'));
        service.command.mockRejectedValue({ response: { status: 409, data: { detail: { message: 'Another editor changed this task' } } } });
        const { user } = renderView({ task: planned });
        await waitFor(() => expect(screen.getByRole('button', { name: 'Start work' })).toBeEnabled());
        await user.click(screen.getByRole('button', { name: 'Start work' }));
        expect(await screen.findByRole('alert')).toHaveTextContent('Another editor changed this task');
        expect(screen.queryByRole('textbox')).not.toBeInTheDocument();
    });

    it('submits for review in one click when the task has criteria', async () => {
        const onTaskUpdated = vi.fn();
        service.command.mockResolvedValue({ ...task, status: 'resolved', version: 5 });
        const { user } = renderView({ onTaskUpdated });
        await waitFor(() => expect(screen.getByRole('button', { name: 'Submit for review' })).toBeEnabled());
        await user.click(screen.getByRole('button', { name: 'Submit for review' }));
        await waitFor(() => expect(onTaskUpdated).toHaveBeenCalledWith(expect.objectContaining({ status: 'resolved' })));
        expect(service.command).toHaveBeenCalledWith(312, expect.objectContaining({ action: 'resolve_manual', reason: 'Submitted for review from the task view.' }));
    });

    it('opens Work & review instead of submitting a task without criteria', async () => {
        const noCriteria = { ...task, brief: { ...task.brief!, acceptance_criteria: [] } } as Task;
        const { user } = renderView({ task: noCriteria });
        await waitFor(() => expect(screen.getByRole('button', { name: 'Submit for review' })).toBeEnabled());
        await user.click(screen.getByRole('button', { name: 'Submit for review' }));
        expect(screen.getByTestId('location')).toHaveTextContent('task=312&part=work');
        expect(service.command).not.toHaveBeenCalled();
    });

    it('opens Review without claiming unsaved edits', async () => {
        const resolved = { ...task, status: 'resolved' } as Task;
        const onDirty = vi.fn();
        const { user } = renderView({ task: resolved, onDirty });
        await user.click(screen.getByRole('button', { name: 'Review' }));
        expect(screen.getByText('Work panel')).toBeInTheDocument();
        expect(screen.getByTestId('location')).toHaveTextContent('task=312&part=work');
        expect(screen.queryByText('Save or discard your edits to change status.')).not.toBeInTheDocument();
        expect(screen.getByRole('button', { name: 'Review' })).toBeEnabled();
        expect(onDirty).not.toHaveBeenCalledWith(true);
        expect(service.command).not.toHaveBeenCalled();
    });
});

describe('task view for stopped work', () => {
    it.each([
        ['postponed', 'postponed', 'Postponed'], ['canceled', 'active', 'Canceled'], ['superseded', 'planned', 'Superseded'],
    ] as const)('shows %s as its own state and offers no work to start or submit', (state, stored, label) => {
        renderView({ task: { ...task, status: stored, displayed_state: state, successor_task_id: state === 'superseded' ? 77 : null } as Task });
        expect(screen.getByText(label, { selector: '[data-task-state]' })).toBeVisible();
        expect(screen.queryByRole('button', { name: /Start work|Submit for review|Review work/ })).not.toBeInTheDocument();
    });

    it('links a superseded task to its successor and keeps the keyboard path', async () => {
        const { user } = renderView({ task: { ...task, status: 'planned', displayed_state: 'superseded', successor_task_id: 77, successor_kind: 'supersession' } as Task });
        const link = screen.getByRole('button', { name: 'Superseded by #77' });
        link.focus();
        await user.keyboard('{Enter}');
        expect(screen.getByTestId('location')).toHaveTextContent('task=77');
    });
});

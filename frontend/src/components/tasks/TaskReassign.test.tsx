import { beforeEach, describe, expect, it, vi } from 'vitest';
import { screen, waitFor, within } from '@testing-library/react';
import { renderWithProviders } from '../../test/renderWithProviders';
import i18n, { changeAppLanguage } from '../../i18n/i18n';
import type { RoutingCheck, Task } from '../../types/task';
import { emptyTaskBrief } from './taskEditorContract';
import { TaskReassign } from './TaskReassign';
import { TaskReadView } from './TaskReadView';

const service = vi.hoisted(() => ({ routingCheck: vi.fn(), update: vi.fn(), actions: vi.fn(), writeBrief: vi.fn(), command: vi.fn() }));
vi.mock('../../services/taskService', () => ({ taskService: service }));
vi.mock('../../services/teamService', () => ({
    teamService: { getByIteration: vi.fn().mockResolvedValue([
        { id: 7, name: 'Sam Ortiz', iteration_id: 2, profile_id: 70, profile: { id: 70, profile_kind: 'agent' } },
        { id: 9, name: 'Vendor Agent', iteration_id: 2, profile_id: 90, profile: { id: 90, profile_kind: 'agent' } },
    ]) },
}));
vi.mock('./TaskWorkPanel', () => ({ TaskWorkPanel: () => null }));

const routing = {
    schema_version: 1 as const,
    first_rung: { catalog_key: 'alpha-large', effort: 'high', publisher_key: 'alpha' },
    escalation: [{ catalog_key: 'beta-large', effort: 'high', publisher_key: 'beta' }],
    escalate_after_failed_runs: 2,
    after_last_rung: 'Ask the owner.',
    reviewer: { catalog_key: 'gamma-review', effort: 'medium', publisher_key: 'gamma', instructions: 'Check each criterion.' },
    notes: '',
};

const task = {
    id: 312, title: 'Import holidays', status: 'planned', version: 4, priority: 2, effort_days: 3,
    assignee: { id: 7, name: 'Sam Ortiz' }, project_id: 1, iteration_id: 2, dependencies: [], children: [], tags: [],
    is_overdue: false, is_delayed: false, is_composite: false, is_optional: false, is_deferred: false, sort_order: 0,
    external_links: [], request_count: 0, agent_readiness: { is_ready: false, blockers: [], warnings: [], criteria: [] },
    brief: { ...emptyTaskBrief(), goal: 'Load holidays.', routing },
} as unknown as Task;

const conflictCheck = (mode: 'refuse' | 'warn'): RoutingCheck => ({
    task_id: 312, assignee_id: 9, assignee_publishers: ['gamma'], assignee_catalog_keys: ['gamma-large'],
    different_publisher_required: true, conflict_mode: mode, structured: true, text_routing: false, consistent: false,
    issues: [{ code: 'reviewer_shares_assignee_publisher', severity: 'conflict', field: 'reviewer', message: 'Reviewer shares the assignee publisher.', catalog_key: 'gamma-review', publisher_key: 'gamma' }],
    routing, suggestion: { ...routing, first_rung: { catalog_key: 'gamma-large', publisher_key: 'gamma' }, reviewer: { catalog_key: 'alpha-review', effort: 'medium', publisher_key: 'alpha' } },
    suggested_reviewer: { catalog_key: 'alpha-review', effort: 'medium', publisher_key: 'alpha' }, applied: false,
});
const noRoutingCheck: RoutingCheck = {
    task_id: 312, assignee_id: 9, assignee_publishers: [], assignee_catalog_keys: [], different_publisher_required: true,
    conflict_mode: 'refuse', structured: false, text_routing: false, consistent: true, issues: [], applied: false,
};

const renderReassign = (overrides: Partial<Task> = {}) => {
    const onTaskUpdated = vi.fn();
    const onPending = vi.fn();
    const view = renderWithProviders(<TaskReassign task={{ ...task, ...overrides } as Task} onTaskUpdated={onTaskUpdated} onPending={onPending} />);
    return { ...view, onTaskUpdated, onPending };
};

const choose = async (user: ReturnType<typeof renderReassign>['user'], name = 'Vendor Agent') => {
    const select = await screen.findByRole('combobox', { name: 'Reassign to' });
    await waitFor(() => expect(within(select).getByRole('option', { name })).toBeInTheDocument());
    await user.selectOptions(select, name);
};

beforeEach(async () => {
    vi.clearAllMocks();
    await changeAppLanguage('en');
    service.update.mockImplementation(async (_id: number, data: { assignee_id: number | null }) => ({ ...task, version: 5, assignee: { id: data.assignee_id, name: 'Vendor Agent' } }));
});

describe('reassigning a task with structured routing', () => {
    it('shows the conflict and the suggested reviewer before saving, and refuses a plain save in refuse mode', async () => {
        service.routingCheck.mockResolvedValue(conflictCheck('refuse'));
        const { user } = renderReassign();
        await choose(user);
        const notice = await screen.findByRole('group', { name: 'Routing check' });
        expect(service.routingCheck).toHaveBeenCalledWith(312, 9);
        expect(within(notice).getByText(/does not fit Vendor Agent/)).toBeVisible();
        expect(within(notice).getByText(/same publisher as the new assignee/)).toBeVisible();
        expect(within(notice).getByText('Suggested reviewer: alpha-review at medium effort (alpha).')).toBeVisible();
        expect(within(notice).getByText(/does not save a reassignment that leaves this conflict/)).toBeVisible();
        expect(service.update).not.toHaveBeenCalled();
        expect(screen.queryByRole('button', { name: 'Reassign' })).not.toBeInTheDocument();
        expect(screen.queryByRole('button', { name: 'Reassign and keep the reviewer' })).not.toBeInTheDocument();
        await user.click(screen.getByRole('button', { name: 'Reassign and use the suggested routing' }));
        await waitFor(() => expect(service.update).toHaveBeenCalledWith(312, { assignee_id: 9, expected_version: 4, routing_resolution: 'apply_suggestion' }));
    });

    it('in warn mode also offers to keep the reviewer, which saves with a plain check', async () => {
        service.routingCheck.mockResolvedValue(conflictCheck('warn'));
        const { user, onTaskUpdated } = renderReassign();
        await choose(user);
        const notice = await screen.findByRole('group', { name: 'Routing check' });
        expect(within(notice).getByText(/allows saving the reassignment with this conflict/)).toBeVisible();
        expect(screen.getByRole('button', { name: 'Reassign and use the suggested routing' })).toBeEnabled();
        await user.click(screen.getByRole('button', { name: 'Reassign and keep the reviewer' }));
        await waitFor(() => expect(service.update).toHaveBeenCalledWith(312, { assignee_id: 9, expected_version: 4, routing_resolution: 'check' }));
        await waitFor(() => expect(onTaskUpdated).toHaveBeenCalled());
    });

    it('reassigns a task without routing with no notice', async () => {
        service.routingCheck.mockResolvedValue(noRoutingCheck);
        const { user } = renderReassign({ brief: { ...emptyTaskBrief(), goal: 'Load holidays.' } } as Partial<Task>);
        await choose(user);
        await waitFor(() => expect(service.routingCheck).toHaveBeenCalled());
        expect(screen.queryByRole('group', { name: 'Routing check' })).not.toBeInTheDocument();
        await user.click(await screen.findByRole('button', { name: 'Reassign' }));
        await waitFor(() => expect(service.update).toHaveBeenCalledWith(312, { assignee_id: 9, expected_version: 4, routing_resolution: 'check' }));
    });

    it('shows the 409 routing_inconsistent body when the server refuses a change the preview allowed', async () => {
        service.routingCheck.mockResolvedValue(noRoutingCheck);
        service.update.mockRejectedValueOnce({ response: { status: 409, data: { detail: {
            code: 'routing_inconsistent', message: 'The task\'s routing conflicts with its assignee or the project\'s review policy.',
            routing_check: conflictCheck('refuse'),
        } } } });
        const { user } = renderReassign();
        await choose(user);
        await user.click(await screen.findByRole('button', { name: 'Reassign' }));
        const notice = await screen.findByRole('group', { name: 'Routing check' });
        expect(within(notice).getByText('Suggested reviewer: alpha-review at medium effort (alpha).')).toBeVisible();
        expect(screen.queryByRole('alert')).not.toBeInTheDocument();
        await user.click(screen.getByRole('button', { name: 'Reassign and use the suggested routing' }));
        await waitFor(() => expect(service.update).toHaveBeenLastCalledWith(312, { assignee_id: 9, expected_version: 4, routing_resolution: 'apply_suggestion' }));
    });

    it('lets the change be chosen, checked and saved with the keyboard alone', async () => {
        service.routingCheck.mockResolvedValue(conflictCheck('refuse'));
        const { user } = renderReassign();
        const select = await screen.findByRole('combobox', { name: 'Reassign to' });
        await waitFor(() => expect(within(select).getByRole('option', { name: 'Vendor Agent' })).toBeInTheDocument());
        await user.tab();
        expect(select).toHaveFocus();
        await user.selectOptions(select, 'Vendor Agent');
        await screen.findByRole('group', { name: 'Routing check' });
        await user.tab();
        expect(screen.getByRole('button', { name: 'Reassign and use the suggested routing' })).toHaveFocus();
        await user.keyboard('{Enter}');
        await waitFor(() => expect(service.update).toHaveBeenCalledWith(312, expect.objectContaining({ routing_resolution: 'apply_suggestion' })));
    });

    it('waits for the check and offers a retry when it fails', async () => {
        service.routingCheck.mockRejectedValueOnce(new Error('offline')).mockResolvedValueOnce(noRoutingCheck);
        const { user } = renderReassign();
        await choose(user);
        expect(await screen.findByRole('button', { name: /retry/i })).toBeVisible();
        expect(screen.queryByRole('button', { name: 'Reassign' })).not.toBeInTheDocument();
        await user.click(screen.getByRole('button', { name: /retry/i }));
        expect(await screen.findByRole('button', { name: 'Reassign' })).toBeEnabled();
    });

    it('shows the conflict in Russian', async () => {
        await changeAppLanguage('ru');
        service.routingCheck.mockResolvedValue(conflictCheck('refuse'));
        try {
            const { user } = renderReassign();
            const select = await screen.findByRole('combobox', { name: 'Переназначить на' });
            await waitFor(() => expect(within(select).getByRole('option', { name: 'Vendor Agent' })).toBeInTheDocument());
            await user.selectOptions(select, 'Vendor Agent');
            const notice = await screen.findByRole('group', { name: 'Проверка маршрутизации' });
            expect(within(notice).getByText(/Ревьюер от того же издателя/)).toBeVisible();
            expect(within(notice).getByText('Предлагаемый ревьюер: alpha-review, усилие medium (alpha).')).toBeVisible();
            expect(screen.getByRole('button', { name: 'Переназначить и взять предложенную маршрутизацию' })).toBeVisible();
        } finally {
            await changeAppLanguage('en');
        }
        expect(i18n.language).toBe('en');
    });
});

describe('routing on the task page', () => {
    it('shows the first rung, the escalation and the reviewer', async () => {
        service.actions.mockResolvedValue({ task_id: 312, version: 4, claim_generation: 0, running_run_ids: [], live_assignment_ids: [], actions: [] });
        renderWithProviders(<TaskReadView task={task} draftKey={null} onTaskUpdated={vi.fn()} onEditAll={vi.fn()} onDirty={vi.fn()} onPending={vi.fn()} onReload={vi.fn()} />);
        const section = await screen.findByRole('region', { name: 'Routing' });
        expect(within(section).getByText('First rung').nextSibling).toHaveTextContent('alpha-large at high effort (alpha)');
        expect(within(section).getByText('beta-large at high effort (beta)')).toBeVisible();
        expect(within(section).getByText('Moves to the next rung after 2 failed runs.')).toBeVisible();
        expect(within(section).getByText('gamma-review at medium effort (gamma)')).toBeVisible();
        expect(within(section).getByText('Check each criterion.')).toBeVisible();
        expect(within(section).getByRole('combobox', { name: 'Reassign to' })).toBeVisible();
    });

    it('says so when the task has no routing', async () => {
        service.actions.mockResolvedValue({ task_id: 312, version: 4, claim_generation: 0, running_run_ids: [], live_assignment_ids: [], actions: [] });
        renderWithProviders(<TaskReadView task={{ ...task, brief: { ...emptyTaskBrief(), goal: 'Load holidays.' } } as Task} draftKey={null}
            onTaskUpdated={vi.fn()} onEditAll={vi.fn()} onDirty={vi.fn()} onPending={vi.fn()} onReload={vi.fn()} />);
        expect(await screen.findByText('This task has no structured routing.')).toBeVisible();
    });
});

import { beforeEach, describe, expect, it, vi } from 'vitest';
import { screen, waitFor, within } from '@testing-library/react';
import { renderWithProviders } from '../../test/renderWithProviders';
import { changeAppLanguage } from '../../i18n/i18n';
import type { RoutingCheck, TaskBulkOperationRequest } from '../../types/task';
import { MutationSuccessFeedback } from '../../features/MutationSuccessFeedback';
import { TaskBulkOperationsPanel } from './TaskBulkOperationsPanel';

const services = vi.hoisted(() => ({ runBulkOperation: vi.fn() }));
vi.mock('../../services/taskService', () => ({ taskService: { runBulkOperation: services.runBulkOperation } }));
vi.mock('../../services/teamService', () => ({ teamService: { getByIteration: vi.fn().mockResolvedValue([{ id: 9, name: 'Vendor Agent' }]) } }));
vi.mock('../../services/projectService', () => ({ projectService: { getAll: vi.fn().mockResolvedValue([]), getMilestones: vi.fn().mockResolvedValue([]) } }));
vi.mock('../../services/iterationService', () => ({ iterationService: { getById: vi.fn().mockResolvedValue({ id: 1, name: 'Iteration', project_id: null }), getAll: vi.fn().mockResolvedValue([]) } }));

const selected = [{ id: 1, title: 'Task 1', version: 1 }, { id: 2, title: 'Task 2', version: 1 }, { id: 3, title: 'Task 3', version: 1 }];

const conflict = (mode: 'refuse' | 'warn', taskId: number): RoutingCheck => ({
    task_id: taskId, assignee_id: 9, assignee_publishers: ['gamma'], assignee_catalog_keys: [], different_publisher_required: true,
    conflict_mode: mode, structured: true, text_routing: false, consistent: false, applied: false,
    issues: [{ code: 'reviewer_shares_assignee_publisher', severity: 'conflict', field: 'reviewer', message: 'Reviewer shares the assignee publisher.' }],
    suggestion: { schema_version: 1, escalation: [], escalate_after_failed_runs: 2, reviewer: { catalog_key: 'alpha-review', publisher_key: 'alpha' } },
    suggested_reviewer: { catalog_key: 'alpha-review', publisher_key: 'alpha' },
});

/** Tasks 1 and 3 have a reviewer that no longer fits; task 2 has no routing. */
const server = (mode: 'refuse' | 'warn') => async (request: TaskBulkOperationRequest) => {
    const resolved = request.payload?.routing_resolution === 'apply_suggestion';
    const results = request.task_ids.map(id => {
        const conflicting = id !== 2;
        if (!conflicting) return { task_id: id, outcome: request.dry_run ? 'would_update' : 'updated', changes: {}, warnings: [] };
        if (resolved) return { task_id: id, outcome: request.dry_run ? 'would_update' : 'updated', changes: {}, warnings: [], routing_check: { ...conflict(mode, id), applied: true, consistent: true } };
        if (mode === 'refuse') return { task_id: id, outcome: 'failed', changes: {}, warnings: [], error: 'The routing conflicts', routing_check: conflict(mode, id) };
        return { task_id: id, outcome: request.dry_run ? 'would_update' : 'updated', changes: {}, warnings: [], routing_check: conflict(mode, id) };
    });
    return {
        dry_run: request.dry_run, requested_count: results.length, succeeded_count: results.filter(r => r.outcome !== 'failed').length,
        failed_count: results.filter(r => r.outcome === 'failed').length, task_versions: { 1: 1, 2: 1, 3: 1 }, input_revisions: { 1: 4 }, results,
    };
};

const renderPanel = () => renderWithProviders(<>
    <MutationSuccessFeedback />
    <TaskBulkOperationsPanel iterationId={1} selectedTasks={selected} matchingCount={3} onSelectAll={vi.fn()} onClearSelection={vi.fn()} openAssign />
</>);

const apply = async (user: ReturnType<typeof renderPanel>['user'], assignee = 'Vendor Agent') => {
    const select = screen.getByRole('combobox', { name: 'Choose assignee' });
    await waitFor(() => expect(within(select).getByRole('option', { name: assignee })).toBeInTheDocument());
    await user.selectOptions(select, assignee);
    await user.click(screen.getByRole('button', { name: 'Apply' }));
};

const writes = () => services.runBulkOperation.mock.calls.map(call => call[0] as TaskBulkOperationRequest).filter(request => !request.dry_run);

beforeEach(async () => {
    services.runBulkOperation.mockReset();
    await changeAppLanguage('en');
});

describe('bulk reassignment and reviewers', () => {
    it('lists the tasks that need a new reviewer and applies the suggestions in one confirmation (refuse mode)', async () => {
        services.runBulkOperation.mockImplementation(server('refuse'));
        const { user } = renderPanel();
        await apply(user);
        const region = await screen.findByRole('region', { name: '2 tasks need a new reviewer' });
        expect(writes()).toHaveLength(0);
        // Stopping at the list changed nothing, so nothing is announced as applied.
        expect(screen.queryByText(/Applied to/)).not.toBeInTheDocument();
        expect(within(region).getByText('Task 1')).toBeVisible();
        expect(within(region).getByText('Task 3')).toBeVisible();
        expect(within(region).queryByText('Task 2')).not.toBeInTheDocument();
        expect(within(region).getAllByText('Suggested reviewer: alpha-review (alpha).')).toHaveLength(2);
        expect(within(region).queryByRole('button', { name: 'Reassign and keep reviewers' })).not.toBeInTheDocument();
        await user.click(within(region).getByRole('button', { name: 'Reassign and use suggested reviewers' }));
        await waitFor(() => expect(writes()).toHaveLength(1));
        expect(writes()[0]).toMatchObject({ action: 'set_assignee', task_ids: [1, 2, 3], payload: { assignee_id: 9, routing_resolution: 'apply_suggestion' } });
        expect(await screen.findByText('Applied to 3 tasks.')).toBeVisible();
        expect(services.runBulkOperation.mock.calls.map(call => [call[0].dry_run, call[0].payload.routing_resolution])).toEqual([[true, undefined], [true, 'apply_suggestion'], [false, 'apply_suggestion']]);
    });

    it('in warn mode also offers to keep the reviewers, which sends the plain change', async () => {
        services.runBulkOperation.mockImplementation(server('warn'));
        const { user } = renderPanel();
        await apply(user);
        const region = await screen.findByRole('region', { name: '2 tasks need a new reviewer' });
        await user.click(within(region).getByRole('button', { name: 'Reassign and keep reviewers' }));
        await waitFor(() => expect(writes()).toHaveLength(1));
        expect(writes()[0].payload).toEqual({ assignee_id: 9 });
    });

    it('goes back from the list without writing anything', async () => {
        services.runBulkOperation.mockImplementation(server('refuse'));
        const { user } = renderPanel();
        await apply(user);
        await user.click(within(await screen.findByRole('region', { name: '2 tasks need a new reviewer' })).getByRole('button', { name: 'Back' }));
        expect(screen.queryByRole('region', { name: /need a new reviewer/ })).not.toBeInTheDocument();
        expect(writes()).toHaveLength(0);
    });

    it('applies straight away when no task needs a new reviewer', async () => {
        services.runBulkOperation.mockImplementation(async (request: TaskBulkOperationRequest) => ({
            dry_run: request.dry_run, requested_count: 3, succeeded_count: 3, failed_count: 0, task_versions: {}, input_revisions: {},
            results: request.task_ids.map(id => ({ task_id: id, outcome: request.dry_run ? 'would_update' : 'updated', changes: {}, warnings: [] })),
        }));
        const { user } = renderPanel();
        await apply(user);
        await waitFor(() => expect(writes()).toHaveLength(1));
        expect(screen.queryByRole('region', { name: /need a new reviewer/ })).not.toBeInTheDocument();
        expect(writes()[0].payload).toEqual({ assignee_id: 9 });
    });

    it('still rejects a task that fails for another reason', async () => {
        services.runBulkOperation.mockImplementation(async (request: TaskBulkOperationRequest) => ({
            dry_run: true, requested_count: 1, succeeded_count: 0, failed_count: 1, task_versions: {}, input_revisions: {},
            results: [{ task_id: request.task_ids[0], outcome: 'failed', changes: {}, warnings: [], error: 'Version changed' }],
        }));
        const { user } = renderPanel();
        await apply(user);
        expect(await screen.findByText(/Nothing was changed/)).toBeVisible();
        expect(screen.queryByRole('region', { name: /need a new reviewer/ })).not.toBeInTheDocument();
    });

    it('reaches the confirmation with the keyboard and applies it with Enter', async () => {
        services.runBulkOperation.mockImplementation(server('refuse'));
        const { user } = renderPanel();
        await apply(user);
        const region = await screen.findByRole('region', { name: '2 tasks need a new reviewer' });
        const primary = within(region).getByRole('button', { name: 'Reassign and use suggested reviewers' });
        primary.focus();
        await user.keyboard('{Enter}');
        await waitFor(() => expect(writes()).toHaveLength(1));
    });

    it('shows the list in Russian', async () => {
        await changeAppLanguage('ru');
        services.runBulkOperation.mockImplementation(server('refuse'));
        try {
            const { user } = renderPanel();
            const select = await screen.findByRole('combobox');
            await waitFor(() => expect(within(select).getByRole('option', { name: 'Vendor Agent' })).toBeInTheDocument());
            await user.selectOptions(select, 'Vendor Agent');
            await user.click(screen.getAllByRole('button').find(button => button.textContent === 'Применить')!);
            const region = await screen.findByRole('region', { name: '2 задачам нужен новый ревьюер' });
            expect(within(region).getByRole('button', { name: 'Переназначить и взять предложенных ревьюеров' })).toBeVisible();
            expect(within(region).getAllByText(/Ревьюер от того же издателя/)).toHaveLength(2);
        } finally {
            await changeAppLanguage('en');
        }
    });
});

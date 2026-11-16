import { beforeEach, describe, expect, it, vi } from 'vitest';
import { screen, waitFor, within } from '@testing-library/react';
import { renderWithProviders } from '../../test/renderWithProviders';
import { TaskBulkOperationsPanel } from './TaskBulkOperationsPanel';

const services = vi.hoisted(() => ({
    runBulkOperation: vi.fn(),
    getById: vi.fn(),
    getMilestones: vi.fn(),
}));

vi.mock('../../services/taskService', () => ({ taskService: { runBulkOperation: services.runBulkOperation } }));
vi.mock('../../services/teamService', () => ({ teamService: { getByIteration: vi.fn().mockResolvedValue([]) } }));
vi.mock('../../services/projectService', () => ({
    projectService: { getAll: vi.fn().mockResolvedValue([{ id: 7, name: 'Calendar' }]), getMilestones: services.getMilestones },
}));
vi.mock('../../services/iterationService', () => ({ iterationService: { getById: services.getById, getAll: vi.fn().mockResolvedValue([]) } }));

const selected = [{ id: 1, title: 'Task 1', version: 1 }, { id: 2, title: 'Task 2', version: 1 }];

const renderPanel = () => renderWithProviders(
    <TaskBulkOperationsPanel iterationId={1} selectedTasks={selected} matchingCount={2} onSelectAll={vi.fn()} onClearSelection={vi.fn()} />,
);

const lastRequest = () => services.runBulkOperation.mock.calls.at(-1)![0];

describe('TaskBulkOperationsPanel more changes', () => {
    beforeEach(() => {
        Object.values(services).forEach(mock => mock.mockReset());
        services.getById.mockResolvedValue({ id: 1, name: 'Iteration', project_id: null });
        services.getMilestones.mockResolvedValue([{ id: 31, name: 'Beta' }]);
        services.runBulkOperation.mockImplementation(async (request: { dry_run: boolean; task_ids: number[] }) => ({
            dry_run: request.dry_run, requested_count: 2, succeeded_count: 2, failed_count: 0, task_versions: {}, input_revisions: {},
            results: request.task_ids.map(id => ({ task_id: id, outcome: request.dry_run ? 'would_update' : 'updated', changes: {}, warnings: [] })),
        }));
    });

    const choose = async (user: ReturnType<typeof renderPanel>['user'], name: string) => {
        await user.click(screen.getByRole('button', { name: 'More changes' }));
        await user.click(await screen.findByRole('menuitem', { name }));
    };

    it('lists every change the bar used to offer, including the clearing ones', async () => {
        const { user } = renderPanel();
        await waitFor(() => expect(services.getById).toHaveBeenCalled());
        await user.click(screen.getByRole('button', { name: 'More changes' }));
        const names = (await screen.findAllByRole('menuitem')).map(item => item.textContent);
        expect(names).toEqual(['Set project', 'Clear project', 'Set milestone', 'Clear milestone', 'Add labels', 'Remove labels', 'Optional or deferred', 'Delete tasks']);
    });

    it('does not offer Clear project when the iteration belongs to a project', async () => {
        services.getById.mockResolvedValue({ id: 1, name: 'Iteration', project_id: 7, project: { id: 7, name: 'Calendar' } });
        const { user } = renderPanel();
        await waitFor(() => expect(services.getById).toHaveBeenCalled());
        await user.click(screen.getByRole('button', { name: 'More changes' }));
        expect(await screen.findByRole('menuitem', { name: 'Set project' })).toBeInTheDocument();
        await waitFor(() => expect(screen.queryByRole('menuitem', { name: 'Clear project' })).toBeNull());
    });

    it('clears the project and clears the milestone', async () => {
        const { user } = renderPanel();
        await waitFor(() => expect(services.getById).toHaveBeenCalled());
        await choose(user, 'Clear project');
        await waitFor(() => expect(screen.getByRole('button', { name: 'Apply' })).toBeEnabled());
        await user.click(screen.getByRole('button', { name: 'Apply' }));
        await waitFor(() => expect(services.runBulkOperation).toHaveBeenCalledTimes(2));
        expect(lastRequest()).toMatchObject({ action: 'clear_project', dry_run: false, task_ids: [1, 2] });
    });

    it('clears the milestone', async () => {
        const { user } = renderPanel();
        await choose(user, 'Clear milestone');
        await user.click(screen.getByRole('button', { name: 'Apply' }));
        await waitFor(() => expect(services.runBulkOperation).toHaveBeenCalledTimes(2));
        expect(lastRequest()).toMatchObject({ action: 'clear_milestone', dry_run: false, task_ids: [1, 2] });
    });

    it('sets the optional flag and the deferred flag together or alone', async () => {
        const { user } = renderPanel();
        await choose(user, 'Optional or deferred');
        expect(screen.getByRole('button', { name: 'Apply' })).toBeDisabled();
        await user.selectOptions(screen.getByRole('combobox', { name: 'Optional' }), 'Set optional');
        await user.selectOptions(screen.getByRole('combobox', { name: 'Deferred' }), 'Set deferred');
        await user.click(screen.getByRole('button', { name: 'Apply' }));
        await waitFor(() => expect(services.runBulkOperation).toHaveBeenCalledTimes(2));
        expect(lastRequest()).toMatchObject({ action: 'set_flags', payload: { is_optional: true, is_deferred: true }, dry_run: false });
    });

    it('lets an iteration without a project pick a project, then one of its milestones', async () => {
        const { user } = renderPanel();
        await waitFor(() => expect(services.getById).toHaveBeenCalled());
        await choose(user, 'Set milestone');
        const bar = screen.getByTestId('task-bulk-operations');
        const milestone = within(bar).getByRole('combobox', { name: 'Milestone' });
        expect(milestone).toBeDisabled();
        await user.selectOptions(await within(bar).findByRole('combobox', { name: 'Project' }), 'Calendar');
        await waitFor(() => expect(milestone).toBeEnabled());
        await user.selectOptions(milestone, 'Beta');
        await user.click(screen.getByRole('button', { name: 'Apply' }));
        await waitFor(() => expect(services.runBulkOperation).toHaveBeenCalledTimes(2));
        expect(lastRequest()).toMatchObject({ action: 'set_milestone', payload: { milestone_id: 31 }, dry_run: false });
    });

    it('shows the project of a project-scoped iteration and picks only a milestone', async () => {
        services.getById.mockResolvedValue({ id: 1, name: 'Iteration', project_id: 7, project: { id: 7, name: 'Calendar' } });
        const { user } = renderPanel();
        await waitFor(() => expect(services.getById).toHaveBeenCalled());
        await choose(user, 'Set milestone');
        expect(await screen.findByText('Calendar')).toBeInTheDocument();
        expect(screen.queryByRole('combobox', { name: 'Project' })).toBeNull();
        await user.selectOptions(await screen.findByRole('combobox', { name: 'Milestone' }), 'Beta');
        await user.click(screen.getByRole('button', { name: 'Apply' }));
        await waitFor(() => expect(services.runBulkOperation).toHaveBeenCalledTimes(2));
        expect(lastRequest()).toMatchObject({ action: 'set_milestone', payload: { milestone_id: 31 } });
    });
});

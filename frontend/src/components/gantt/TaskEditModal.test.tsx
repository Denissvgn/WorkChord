import { act, fireEvent, screen } from '@testing-library/react';
import { expect, it, vi } from 'vitest';
import { renderWithProviders } from '../../test/renderWithProviders';
import { TaskEditModal } from './TaskEditModal';
import type { GanttTask } from '../../types/gantt';
import type { TaskDetail, TaskUpdate } from '../../types/task';

const api = vi.hoisted(() => ({ getDetail: vi.fn() }));
vi.mock('../../services/taskService', () => ({ taskService: api }));
vi.mock('../../services/teamService', () => ({ teamService: { getByIteration: vi.fn().mockResolvedValue([{ id: 7, name: 'Sam' }]) } }));
vi.mock('../tasks/TaskContextSummary', () => ({ TaskContextSummary: () => null }));
vi.mock('../tasks/TaskReadView', () => ({ TaskReadView: ({ task }: { task: { title: string } }) => (
    <div data-testid="read-view">{task.title}</div>
) }));
vi.mock('../tasks/TaskForm', () => ({ TaskForm: ({ initialData, onSaveSandbox, onSuccess }: {
    initialData: { title: string }; onSaveSandbox?: (update: TaskUpdate) => void; onSuccess: () => void;
}) => (
    <button type="button" data-testid="form" onClick={() => { onSaveSandbox?.({ title: 'Saved', assignee_id: 7 } as TaskUpdate); onSuccess(); }}>
        {initialData.title}
    </button>
) }));

const ganttTask = { id: 9, title: 'Preview title', priority: 5, effort_days: 2, status: 'todo', tags: [], dependencies: [] } as unknown as GanttTask;

const resolveDetail = () => api.getDetail.mockResolvedValue({
    task: { id: 9, title: 'Saved title', version: 3, iteration_id: 1 },
    dependencies: { items: [] },
} as unknown as TaskDetail);

it('opens a Gantt task read-first, like the other views', async () => {
    resolveDetail();
    renderWithProviders(<TaskEditModal task={ganttTask} iterationId={1} isOpen onClose={() => undefined} />);
    expect(await screen.findByTestId('read-view')).toHaveTextContent('Saved title');
    expect(screen.queryByTestId('form')).not.toBeInTheDocument();
});

it('opens the form over the preview edits and keeps changes in the preview', async () => {
    resolveDetail();
    const onSaveSandbox = vi.fn();
    const onClose = vi.fn();
    renderWithProviders(<TaskEditModal task={ganttTask} iterationId={1} isOpen sandboxMode onClose={onClose} onSaveSandbox={onSaveSandbox} />);
    const form = await screen.findByTestId('form');
    expect(form).toHaveTextContent('Preview title');
    await act(async () => { await new Promise(resolve => setTimeout(resolve, 0)); });
    fireEvent.click(form);
    expect(onSaveSandbox).toHaveBeenCalledWith(9, expect.objectContaining({ title: 'Saved', assignee: { id: 7, name: 'Sam' } }));
    expect(onClose).toHaveBeenCalledTimes(1);
});

import { useEffect, useState } from 'react';
import { act, screen, waitFor } from '@testing-library/react';
import { beforeEach, expect, it, vi } from 'vitest';
import { renderWithProviders } from '../../test/renderWithProviders';
import { CurrentTaskModal } from './GuardedTaskModal';
import type { Task, TaskDetail } from '../../types/task';

const service = vi.hoisted(() => ({ getDetail: vi.fn() }));
vi.mock('../../services/taskService', () => ({ taskService: service }));
vi.mock('./TaskForm', () => ({ TaskForm: ({ initialData, onDirtyChange }: { initialData: Task; onDirtyChange: (dirty: boolean) => void }) => {
    const [title, setTitle] = useState(initialData.title);
    useEffect(() => { onDirtyChange(title !== initialData.title); }, [title, initialData.title, onDirtyChange]);
    return <><input aria-label="Draft title" value={title} onChange={event => setTitle(event.target.value)} />
        <span data-testid="observed-version">{initialData.version}</span>
        <span data-testid="acceptance-current">{String(initialData.is_accepted)}</span>
        <span data-testid="criterion">{initialData.brief?.acceptance_criteria[0]?.text}</span></>;
} }));
beforeEach(() => service.getDetail.mockReset());
const detail = (id = 9, version = 2, title = 'Current task') => ({ task: { id, version, title, iteration_id: null },
    dependencies: { items: [] } } as unknown as TaskDetail);

it('preserves typing and the original version when a newer background read arrives', async () => {
    service.getDetail.mockResolvedValueOnce(detail()).mockResolvedValueOnce(detail(9, 3, 'External edit'));
    const { user, queryClient } = renderWithProviders(<CurrentTaskModal taskId={9} onClose={() => undefined} />);
    await user.clear(await screen.findByRole('textbox', { name: 'Draft title' }));
    await user.type(screen.getByRole('textbox', { name: 'Draft title' }), 'Unsaved intent');
    await act(() => queryClient.invalidateQueries({ queryKey: ['taskEditor'] }));
    await waitFor(() => expect(service.getDetail).toHaveBeenCalledTimes(2));
    expect(screen.getByRole('textbox', { name: 'Draft title' })).toHaveValue('Unsaved intent');
    expect(screen.getByTestId('observed-version')).toHaveTextContent('2');
    expect(screen.getByRole('dialog')).toHaveAccessibleName('Current task');
});

it('cancels an obsolete opening and never initializes the next task from its delayed result', async () => {
    let finish!: (value: TaskDetail) => void;
    service.getDetail.mockImplementationOnce(() => new Promise(resolve => { finish = resolve; }))
        .mockResolvedValueOnce(detail(10, 4, 'Next task'));
    const view = renderWithProviders(<CurrentTaskModal key={9} taskId={9} onClose={() => undefined} />);
    await waitFor(() => expect(service.getDetail).toHaveBeenCalledTimes(1));
    const signal = service.getDetail.mock.calls[0][2] as AbortSignal;
    view.rerender(<CurrentTaskModal key={10} taskId={10} onClose={() => undefined} />);
    expect(await screen.findByRole('textbox', { name: 'Draft title' })).toHaveValue('Next task');
    expect(signal.aborted).toBe(true);
    await act(async () => finish(detail(9, 1, 'Obsolete response')));
    expect(screen.getByRole('textbox', { name: 'Draft title' })).toHaveValue('Next task');
});

it('ignores a lower version and removes server actions when access is denied', async () => {
    service.getDetail.mockResolvedValueOnce(detail(9, 4)).mockResolvedValueOnce(detail(9, 2, 'Old task'))
        .mockRejectedValueOnce({ response: { status: 403 } });
    const { queryClient } = renderWithProviders(<CurrentTaskModal taskId={9} onClose={() => undefined} />);
    await screen.findByRole('textbox', { name: 'Draft title' });
    await act(() => queryClient.invalidateQueries({ queryKey: ['taskEditor'] }));
    expect(screen.getByTestId('observed-version')).toHaveTextContent('4');
    await act(() => queryClient.invalidateQueries({ queryKey: ['taskEditor'] }));
    await screen.findByRole('alert');
    expect(screen.queryByRole('textbox', { name: 'Draft title' })).not.toBeInTheDocument();
});

it('rejects mismatched task identities instead of opening an unrelated editor', async () => {
    service.getDetail.mockResolvedValueOnce(detail(10));
    renderWithProviders(<CurrentTaskModal taskId={9} onClose={() => undefined} />);
    await screen.findByRole('alert');
    expect(screen.queryByRole('textbox', { name: 'Draft title' })).not.toBeInTheDocument();
});

it('initializes version, title, criterion and acceptance together from the new opening', async () => {
    const current = detail(9, 5, 'Reviewed new title');
    current.task.is_accepted = false;
    current.task.brief = { acceptance_criteria: [{ id: 'result', revision: 2, text: 'Current criterion' }] } as Task['brief'];
    service.getDetail.mockResolvedValueOnce(current);
    const view = renderWithProviders(<CurrentTaskModal taskId={9} onClose={() => undefined} />);
    view.queryClient.setQueryData(['task', 9], { ...current.task, version: 2, is_accepted: true });
    expect(await screen.findByRole('textbox', { name: 'Draft title' })).toHaveValue('Reviewed new title');
    expect(screen.getByTestId('observed-version')).toHaveTextContent('5');
    expect(screen.getByTestId('criterion')).toHaveTextContent('Current criterion');
    expect(screen.getByTestId('acceptance-current')).toHaveTextContent('false');
});

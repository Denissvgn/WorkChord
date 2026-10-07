import { act, screen } from '@testing-library/react';
import { expect, it, vi } from 'vitest';
import { createTestQueryClient, renderWithProviders } from '../../test/renderWithProviders';
import { TaskEditorDrawer } from './TaskEditorDrawer';
import type { TaskDetail } from '../../types/task';

const api = vi.hoisted(() => ({ getDetail: vi.fn() }));
vi.mock('../../services/taskService', () => ({ taskService: api }));
vi.mock('./TaskContextSummary', () => ({ TaskContextSummary: () => null }));
vi.mock('./TaskForm', () => ({ TaskForm: ({ initialData }: { initialData: { version: number } }) => (
    <div data-testid="editor-version">{initialData.version}</div>
) }));

it('waits for the current read instead of initializing a reopened editor from another opening', async () => {
    const queryClient = createTestQueryClient();
    queryClient.setQueryData(['taskEditor', 9], { id: 9, title: 'Deliverable', version: 2 });
    let complete!: (detail: TaskDetail) => void;
    api.getDetail.mockReturnValue(new Promise<TaskDetail>(resolve => { complete = resolve; }));
    renderWithProviders(<TaskEditorDrawer taskId={9} open onClose={() => undefined} />, { queryClient });
    expect(screen.queryByTestId('editor-version')).not.toBeInTheDocument();
    await act(async () => complete({ task: { id: 9, title: 'Deliverable', version: 3 },
        dependencies: { items: [] } } as unknown as TaskDetail));
    expect(await screen.findByTestId('editor-version')).toHaveTextContent('3');
});

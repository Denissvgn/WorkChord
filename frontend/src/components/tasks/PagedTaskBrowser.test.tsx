import { screen, waitFor } from '@testing-library/react';
import { beforeEach, expect, it, vi } from 'vitest';
import { renderWithProviders } from '../../test/renderWithProviders';
import { PagedTaskBrowser } from './PagedTaskBrowser';
const lookup = vi.hoisted(() => vi.fn());
vi.mock('../../services/taskService', () => ({ taskService: { lookup } }));
vi.mock('./TaskEditorDrawer', () => ({ TaskEditorDrawer: ({ taskId }: { taskId: number | null }) => taskId ? <div>Selected #{taskId}</div> : null }));
beforeEach(() => { lookup.mockReset(); });
it('loads bounded pages explicitly and retains selected work', async () => {
    lookup.mockResolvedValueOnce({ items: [{ id: 1, title: 'First task', status: 'planned' }], has_more: true, next_after_id: 1 })
        .mockResolvedValueOnce({ items: [{ id: 2, title: 'Second task', status: 'active' }], has_more: false, next_after_id: null });
    const { user } = renderWithProviders(<PagedTaskBrowser iterationId={7} />);
    await user.click(await screen.findByRole('button', { name: '#1 · First task' }));
    await user.click(screen.getByRole('button', { name: 'Load more' }));
    expect(await screen.findByRole('button', { name: '#2 · Second task' })).toBeVisible();
    expect(screen.getByRole('button', { name: '#1 · First task' })).toHaveAttribute('aria-current', 'true');
    expect(lookup.mock.calls[1][0]).toMatchObject({ iteration_id: 7, after_id: 1 });
});
it('restarts filtered reads and hides results on failed reads', async () => {
    lookup.mockResolvedValueOnce({ items: [{ id: 1, title: 'Private task', status: 'planned' }], has_more: true, next_after_id: 1 });
    const { user } = renderWithProviders(<PagedTaskBrowser iterationId={7} />);
    await screen.findByRole('button', { name: '#1 · Private task' });
    lookup.mockRejectedValue(new Error('Access revoked'));
    await user.selectOptions(screen.getByRole('combobox'), 'closed');
    await waitFor(() => expect(lookup.mock.calls.at(-1)?.[0]).toMatchObject({ task_status: 'closed', after_id: 0 }));
    expect(screen.queryByRole('button', { name: '#1 · Private task' })).toBeNull();
});

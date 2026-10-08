import { expect, it, vi } from 'vitest';
import { act, screen, waitFor } from '@testing-library/react';
import { createTestQueryClient, renderWithProviders } from '../test/renderWithProviders';
import MyWorkPage from './MyWorkPage';

const api = vi.hoisted(() => ({ get: vi.fn() }));
vi.mock('../services/api', () => ({ default: api }));
vi.mock('../components/tasks/PersonCapacity', () => ({ PersonCapacity: () => null }));
vi.mock('../components/tasks/TaskWorkPanel', () => ({ TaskWorkPanel: () => null }));
vi.mock('../components/tasks/TaskTimelinePanel', () => ({ TaskTimelinePanel: () => null }));
vi.mock('../components/tasks/DeliveryDependencies', () => ({ DeliveryDependencies: () => null }));
vi.mock('../components/tasks/TaskDiscussion', () => ({ TaskDiscussion: () => null }));
vi.mock('../components/tasks/TimeEntriesPanel', () => ({ TimeEntriesPanel: () => null }));

it('waits for a current task read before initializing a clean editor', async () => {
    const client = createTestQueryClient();
    const previous = { id: 9, iteration_id: null, project_id: 1, title: 'Previous task title',
        version: 1, status: 'planned', priority: 50, effort_days: null, effort_hours: null,
        tags: [], dependencies: [], brief: null, parent_id: null };
    const current = { ...previous, title: 'Current task title', version: 2 };
    client.setQueryData(['task', 9], previous);
    let resolveDetail!: (value: unknown) => void;
    api.get.mockImplementation((path: string) => {
        if (path === '/tasks/9/detail') return new Promise(resolve => { resolveDetail = resolve; });
        if (path === '/tasks/my-work') return Promise.resolve({ data: {
            state: 'ready', queues: { active: [] }, has_more: false, next_after_id: null } });
        if (path === '/projects/page') return Promise.resolve({ data: {
            items: [{ id: 1, name: 'Project' }], has_more: false, upper_id: 1 } });
        if (path === '/tasks/owner-options' || path === '/tasks/lookup') {
            return Promise.resolve({ data: { items: [], has_more: false } });
        }
        return Promise.resolve({ data: [] });
    });
    renderWithProviders(<MyWorkPage />, { queryClient: client, initialEntries: ['/my-work?task=9'] });
    try {
        await waitFor(() => expect(resolveDetail).toBeTypeOf('function'));
        const openedBeforeCurrentRead = screen.queryByRole('textbox', { name: /Task title/i });
        await act(async () => resolveDetail({ data: { task: current,
            dependencies: { items: [], has_more: false }, children: { items: [], has_more: false }, ancestors: [] } }));
        const title = await screen.findByRole('textbox', { name: /Task title/i });
        expect(title).toHaveValue('Current task title');
        expect(openedBeforeCurrentRead).toBeNull();
    } finally {
        client.clear();
    }
});

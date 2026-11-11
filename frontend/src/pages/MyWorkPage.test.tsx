import { expect, it, vi } from 'vitest';
import { act, fireEvent, screen, waitFor } from '@testing-library/react';
import { createTestQueryClient, renderWithProviders } from '../test/renderWithProviders';
import MyWorkPage from './MyWorkPage';
import { IdentityContext } from '../features/identity/identityContext';
import { buildTaskEditorDefaults } from '../components/tasks/taskEditorContract';
import { writeTaskDraft } from '../components/tasks/taskDraftStorage';
import type { Task } from '../types/task';

const api = vi.hoisted(() => ({ get: vi.fn(), put: vi.fn(), post: vi.fn() }));
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

it('recovers user input with its original observed version instead of silently rebasing it', async () => {
    const original = { id: 9, iteration_id: null, project_id: 1, title: 'Original task', version: 1,
        status: 'planned', priority: 50, effort_days: null, effort_hours: null, tags: [], dependencies: [], brief: null, parent_id: null } as unknown as Task;
    const key = 'workchord-draft:local:direct:null:1:9';
    writeTaskDraft(key, { ...buildTaskEditorDefaults({ task: original }), title: 'Recovered user intent' });
    api.get.mockImplementation(async (path: string) => {
        if (path === '/tasks/9/detail') return { data: { task: { ...original, title: 'External task edit', version: 3 }, dependencies: { items: [] }, children: { items: [] }, ancestors: [] } };
        if (path === '/tasks/my-work') return { data: { state: 'ready', queues: {}, has_more: false } };
        if (path === '/projects/page') return { data: { items: [{ id: 1, name: 'Project' }], has_more: false } };
        if (path === '/tasks/owner-options' || path === '/tasks/lookup') return { data: { items: [], has_more: false } };
        return { data: [] };
    });
    const view = renderWithProviders(<IdentityContext.Provider value={{ identity: { mode: 'trusted_local' } as never, refresh: vi.fn(), signOut: vi.fn() }}>
        <MyWorkPage /></IdentityContext.Provider>, { initialEntries: ['/my-work?task=9'] });
    expect(await screen.findByRole('textbox', { name: /Task title/i })).toHaveValue('Recovered user intent');
    await waitFor(() => expect(JSON.parse(sessionStorage.getItem(key)!).values.expected_version).toBe(1));
    view.unmount();
    sessionStorage.removeItem(key);
});

it('lets a local session choose who it works as instead of a dead end, then counts each queue', async () => {
    const refresh = vi.fn();
    api.get.mockImplementation(async (path: string) => {
        if (path === '/tasks/my-work') return { data: { state: 'profile_unlinked', queues: {}, has_more: false, next_after_id: null } };
        if (path === '/team-member-profiles') return { data: [{ id: 4, display_name: 'Sam Ortiz', profile_kind: 'human' }, { id: 5, display_name: 'Build agent', profile_kind: 'agent' }] };
        return { data: [] };
    });
    api.put.mockResolvedValue({ data: { profile: { id: 4, display_name: 'Sam Ortiz', verified: false } } });
    const view = renderWithProviders(<IdentityContext.Provider value={{ identity: { mode: 'trusted_local', principal: null, profile: null } as never, refresh, signOut: vi.fn() }}>
        <MyWorkPage /></IdentityContext.Provider>, { initialEntries: ['/my-work'] });
    expect(await screen.findByRole('heading', { name: 'Who are you working as?' })).toBeInTheDocument();
    expect(screen.queryByText(/Ask a workspace operator/)).toBeNull();
    const person = await screen.findByRole('combobox', { name: 'Person profile' });
    expect(screen.queryByRole('option', { name: 'Build agent' })).toBeNull();
    fireEvent.change(person, { target: { value: '4' } });
    fireEvent.click(screen.getByRole('button', { name: 'Work as this person' }));
    await waitFor(() => expect(api.put).toHaveBeenCalledWith('/auth/local-profile', { profile_id: 4 }));
    await waitFor(() => expect(refresh).toHaveBeenCalled());
    view.unmount();

    api.get.mockImplementation(async (path: string) => {
        if (path === '/tasks/my-work') return { data: { state: 'ready', has_more: false, next_after_id: null,
            queues: { active: [], queued: [{ id: 7, title: 'Assigned to my row', status: 'planned', project_name: 'Calendar' }], blocked: [], awaiting_review: [] } } };
        return { data: [] };
    });
    renderWithProviders(<IdentityContext.Provider value={{ identity: { mode: 'trusted_local', principal: null, profile: { id: 4, display_name: 'Sam Ortiz', verified: false } } as never, refresh, signOut: vi.fn() }}>
        <MyWorkPage /></IdentityContext.Provider>, { initialEntries: ['/my-work?queue=queued'] });
    expect(await screen.findByRole('button', { name: 'Up next · 1' })).toBeInTheDocument();
    expect(screen.getByText('Working as Sam Ortiz · local, not verified')).toBeInTheDocument();
    expect(await screen.findByRole('button', { name: '#7 · Assigned to my row' })).toBeInTheDocument();
});

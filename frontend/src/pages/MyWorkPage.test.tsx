import { describe, expect, it, vi } from 'vitest';
import { act, fireEvent, screen, waitFor, within } from '@testing-library/react';
import { createTestQueryClient, renderWithProviders } from '../test/renderWithProviders';
import MyWorkPage from './MyWorkPage';
import { IdentityContext } from '../features/identity/identityContext';
import { buildTaskEditorDefaults } from '../components/tasks/taskEditorContract';
import { writeTaskDraft } from '../components/tasks/taskDraftStorage';
import type { Task } from '../types/task';
import { useLocation } from 'react-router-dom';
import { expectPageChrome } from '../test/pageChrome';
import { taskDetailResponse } from '../test/fixtures/taskDetail';
import i18n, { ensureLanguageResources } from '../i18n/i18n';

const api = vi.hoisted(() => ({ get: vi.fn(), put: vi.fn(), post: vi.fn() }));
vi.mock('../services/api', () => ({ default: api }));
vi.mock('../components/tasks/PersonCapacity', () => ({ PersonCapacity: ({ profileId, manage }: { profileId: number; manage: boolean }) => <div data-testid="capacity">{profileId}:{String(manage)}</div> }));
vi.mock('../components/tasks/TaskWorkPanel', () => ({ TaskWorkPanel: () => null }));
vi.mock('../components/tasks/TaskTimelinePanel', () => ({ TaskTimelinePanel: () => null }));
vi.mock('../components/tasks/DeliveryDependencies', () => ({ DeliveryDependencies: () => null }));
vi.mock('../components/tasks/TaskDiscussion', () => ({ TaskDiscussion: () => null }));
vi.mock('../components/tasks/TimeEntriesPanel', () => ({ TimeEntriesPanel: () => null }));

it('opens a task in the shared read view after a current read', async () => {
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
            state: 'ready', queues: { active: [{ id: 9, title: 'Current task title', status: 'planned', iteration_id: null }] }, has_more: false, next_after_id: null } });
        if (path === '/projects/page') return Promise.resolve({ data: {
            items: [{ id: 1, name: 'Project' }], has_more: false, upper_id: 1 } });
        if (path === '/tasks/owner-options' || path === '/tasks/lookup') {
            return Promise.resolve({ data: { items: [], has_more: false } });
        }
        return Promise.resolve({ data: [] });
    });
    renderWithProviders(<MyWorkPage />, { queryClient: client, initialEntries: ['/my-work'] });
    try {
        fireEvent.click(await screen.findByRole('button', { name: '#9 · Current task title' }));
        await waitFor(() => expect(resolveDetail).toBeTypeOf('function'));
        const openedBeforeCurrentRead = screen.queryByRole('textbox', { name: /Task title/i });
        await act(async () => resolveDetail({ data: { task: current,
            dependencies: { items: [], has_more: false }, children: { items: [], has_more: false }, ancestors: [] } }));
        expect(await screen.findByRole('button', { name: 'Edit all fields' })).toBeInTheDocument();
        expect(screen.queryByRole('textbox', { name: /Task title/i })).toBeNull();
        fireEvent.click(screen.getByRole('button', { name: 'Edit all fields' }));
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
    const view = renderWithProviders(<IdentityContext.Provider value={{ identity: { mode: 'trusted_local', profile: { id: 4, display_name: 'Sam' } } as never, refresh: vi.fn(), signOut: vi.fn() }}>
        <MyWorkPage /></IdentityContext.Provider>, { initialEntries: ['/my-work?task=9'] });
    fireEvent.click(await screen.findByRole('button', { name: 'Edit all fields' }));
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
    expect(screen.queryByTestId('capacity')).toBeNull();
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
    expect(screen.getByTestId('capacity')).toHaveTextContent('4:true');
    const title = await screen.findByRole('button', { name: '#7 · Assigned to my row' });
    // My Work uses the same 44 px row as the task list: status, title, then the menu on hover.
    expect(title.closest('[data-task-row]')).toHaveClass('h-11');
    expect(screen.getByRole('button', { name: /^Status: Planned/ })).toBeInTheDocument();
});

it('keeps a task the chosen local person accepted out of Blocked, and still flags a closed task with no recorded acceptor', async () => {
    const local = { mode: 'trusted_local', principal: null, profile: { id: 4, display_name: 'Sam Ortiz', verified: false } } as never;
    const unrecorded = { id: 12, title: 'Closed before the acceptor was recorded', status: 'closed', iteration_id: null,
        project_name: 'Calendar', acceptance_current: false };
    let queues: Record<string, unknown[]> = { active: [], queued: [], blocked: [unrecorded], awaiting_review: [] };
    api.get.mockImplementation(async (path: string) => {
        if (path === '/tasks/my-work') return { data: { state: 'ready', has_more: false, next_after_id: null, queues } };
        return { data: [] };
    });
    const view = renderWithProviders(<IdentityContext.Provider value={{ identity: local, refresh: vi.fn(), signOut: vi.fn() }}>
        <MyWorkPage /></IdentityContext.Provider>, { initialEntries: ['/my-work?queue=blocked'] });
    expect(await screen.findByRole('button', { name: 'Blocked · 1' })).toBeInTheDocument();
    expect(await screen.findByRole('button', { name: '#12 · Closed before the acceptor was recorded' })).toBeInTheDocument();
    expect(screen.getByText(/Closed · acceptance needs reconciliation/)).toBeInTheDocument();
    view.unmount();

    // Once the acceptance records who accepted it, the server leaves the task out of every My Work queue.
    queues = { active: [], queued: [], blocked: [], awaiting_review: [] };
    renderWithProviders(<IdentityContext.Provider value={{ identity: local, refresh: vi.fn(), signOut: vi.fn() }}>
        <MyWorkPage /></IdentityContext.Provider>, { initialEntries: ['/my-work?queue=blocked'] });
    expect(await screen.findByRole('button', { name: 'Blocked · 0' })).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: /^#12 · / })).toBeNull();
    expect(screen.queryByText(/acceptance needs reconciliation/)).toBeNull();
});

it.each(['active', 'review', 'inbox'])('explains the operator identity and offers Lock before loading the %s person queue', async queue => {
    sessionStorage.setItem('workchord_admin_api_key', 'operator-key');
    api.get.mockImplementation(async (path: string) => {
        if (path === '/tasks/my-work') return { data: { state: 'profile_unlinked', queues: {}, has_more: false, next_after_id: null } };
        return { data: [] };
    });
    const view = renderWithProviders(<IdentityContext.Provider value={{ identity: { mode: 'trusted_local', principal: null, profile: { id: 4, display_name: 'Sam Ortiz', verified: false } } as never, refresh: vi.fn(), signOut: vi.fn() }}>
        <MyWorkPage /></IdentityContext.Provider>, { initialEntries: [`/my-work?queue=${queue}`] });
    expect(await screen.findByText('The admin key in this tab replaces the chosen person. You are acting as the operator. Lock editing to use your person profile.')).toBeInTheDocument();
    expect(screen.queryByText('Ask a workspace operator to link your account to your human work profile.')).not.toBeInTheDocument();
    expect(api.get.mock.calls.some(([path]) => ['/tasks/my-work', '/tasks/review-queue', '/notifications'].includes(path))).toBe(false);
    expect(screen.queryByTestId('capacity')).not.toBeInTheDocument();
    await view.user.click(screen.getByRole('button', { name: 'Lock' }));
    expect(sessionStorage.getItem('workchord_admin_api_key')).toBeNull();
});

describe('My Work opening queue', () => {
    const queuesWithUpNextOnly = () => api.get.mockImplementation(async (path: string) => {
        if (path === '/tasks/my-work') return { data: { state: 'ready', has_more: false, next_after_id: null,
            queues: { active: [], queued: [{ id: 7, title: 'Up next task', status: 'planned', project_name: 'Calendar' }], blocked: [], awaiting_review: [] } } };
        return { data: [] };
    });

    it('opens Up next when Doing is empty and Up next has work', async () => {
        queuesWithUpNextOnly();
        renderWithProviders(<MyWorkPage />, { initialEntries: ['/my-work'] });
        expect(await screen.findByRole('button', { name: '#7 · Up next task' })).toBeInTheDocument();
        expect(screen.queryByText(i18n.t('emptyStates.myWork.queueBody'))).toBeNull();
        expect(screen.getByRole('button', { name: 'Up next · 1' })).toHaveAttribute('aria-pressed', 'true');
    });

    it('keeps the queue the URL names, even when it is empty', async () => {
        queuesWithUpNextOnly();
        renderWithProviders(<MyWorkPage />, { initialEntries: ['/my-work?queue=active'] });
        expect(await screen.findByText(i18n.t('emptyStates.myWork.queueBody'))).toBeInTheDocument();
        expect(screen.queryByRole('button', { name: '#7 · Up next task' })).toBeNull();
        expect(screen.getByRole('button', { name: 'Doing · 0' })).toHaveAttribute('aria-pressed', 'true');
    });
});

describe('My Work rows', () => {
    const fullTask = (id: number, iterationId: number, overrides: Partial<Task> = {}) => ({
        id, iteration_id: iterationId, project_id: null, parent_id: null, title: `Task ${id}`, priority: 2, effort_days: 3, effort_hours: 24,
        assignee: null, status: 'planned', is_overdue: false, is_delayed: false, is_composite: false, is_optional: false, is_deferred: false,
        tags: [], sort_order: id, external_links: [], request_count: 0, version: 1, children: [], dependencies: [],
        agent_readiness: { is_ready: true, blockers: [], warnings: [], criteria: [] }, ...overrides,
    }) as unknown as Task;
    const reference = (id: number, iterationId: number, status: Task['status'] = 'planned') => ({ id, title: `Task ${id}`, status, version: 1, iteration_id: iterationId, project_id: null, parent_id: null, owner_profile_id: null });
    const rowOf = (title: string) => screen.getByRole('button', { name: `#${title.replace('Task ', '')} · ${title}` }).closest<HTMLElement>('[data-task-row]')!;

    const arrange = (tasks: Task[], { shown = tasks, more, reviewers = {}, agentConnected = false }: { shown?: Task[]; more?: (path: string, config?: { params?: Record<string, unknown> }) => unknown; reviewers?: Record<number, string>; agentConnected?: boolean } = {}) => {
        api.get.mockImplementation(async (path: string, config?: { params?: Record<string, unknown> }) => {
            const extra = more?.(path, config);
            if (extra !== undefined) return extra;
            // My Work names the reviewer agent of each submitted task it returns, null when anyone reviews.
            if (path === '/tasks/my-work') return { data: { state: 'ready', has_more: false, next_after_id: null,
                queues: { active: shown.map(item => ({ ...reference(item.id, item.iteration_id as number, item.status), reviewer_name: item.status === 'resolved' ? reviewers[item.id] ?? null : null })),
                    queued: [], blocked: [], awaiting_review: [] } } };
            const iteration = /^\/iterations\/(\d+)\/(tasks|team)$/.exec(path);
            if (iteration?.[2] === 'tasks') return { data: tasks.filter(item => item.iteration_id === Number(iteration[1])) };
            if (iteration?.[2] === 'team') return { data: [{ id: 5, name: 'Ada', profile_id: 50, profile: { id: 50, profile_kind: 'human', agent_connected: false } }, { id: 6, name: 'Build agent', profile_id: 60, profile: { id: 60, profile_kind: 'agent', agent_connected: agentConnected } }] };
            return { data: [] };
        });
        api.post.mockImplementation(async (path: string, body: { dry_run: boolean; task_ids: number[] }) => ({ data: path === '/tasks/bulk-operations' ? {
            dry_run: body.dry_run, requested_count: body.task_ids.length, succeeded_count: body.task_ids.length, failed_count: 0,
            task_versions: Object.fromEntries(body.task_ids.map(id => [id, 1])), input_revisions: { 1: 3 },
            results: body.task_ids.map(id => ({ task_id: id, outcome: body.dry_run ? 'would_update' : 'updated', changes: {}, warnings: [] })),
        } : {} }));
    };

    it('shows priority, an assignee picker and effort, like the task list', async () => {
        arrange([fullTask(1, 1, { assignee: { id: 5, name: 'Ada' }, priority: 3, effort_days: 4 })]);
        renderWithProviders(<MyWorkPage />, { initialEntries: ['/my-work'] });
        const row = (await screen.findByRole('button', { name: '#1 · Task 1' })).closest<HTMLElement>('[data-task-row]')!;
        await waitFor(() => expect(within(row).getByRole('combobox', { name: 'Assignee: Task 1' })).toHaveValue('5'));
        expect(row).toHaveTextContent('P3');
        expect(row).toHaveTextContent('4d');
        expect(within(row).getByRole('option', { name: 'Build agent' })).toBeInTheDocument();
    });

    it('names the same state chip as the Tasks list, chosen by priority', async () => {
        const notReady = { is_ready: false, definition_ready: false, start_ready: false, blockers: [], warnings: [], criteria: [] };
        const prerequisite = fullTask(9, 1);
        const tasks = [
            fullTask(1, 1, { blocked_reason: 'Waiting on legal', agent_readiness: notReady }),
            fullTask(2, 1, { agent_readiness: notReady }),
            fullTask(3, 1, { dependencies: [9], agent_readiness: { ...notReady, definition_ready: true } }),
            fullTask(4, 1, { agent_readiness: { ...notReady, definition_ready: true, start_ready: true } }),
            fullTask(5, 1, { status: 'resolved' }),
        ];
        arrange([...tasks, prerequisite], { shown: tasks });
        renderWithProviders(<MyWorkPage />, { initialEntries: ['/my-work'] });
        await screen.findByRole('button', { name: '#1 · Task 1' });
        const chipText = (title: string) => rowOf(title).querySelector('span.rounded-full')?.textContent;
        await waitFor(() => expect(chipText('Task 2')).toBe('Needs definition'));
        expect(chipText('Task 1')).toBe('Blocked');
        expect(chipText('Task 3')).toBe('Waits for 1');
        expect(chipText('Task 4')).toBe('Ready to start');
        expect(chipText('Task 5')).toBe('In review');
        tasks.forEach(item => expect(rowOf(item.title).querySelectorAll('span.rounded-full')).toHaveLength(1));
    });

    it('shows the agent status under the name of an agent assignee, with the Reviewer beside it', async () => {
        const agent = { id: 6, name: 'Build agent' };
        const claim = { id: 3, name: 'builder', display_name: 'Builder' };
        arrange([
            fullTask(1, 1, { assignee: agent, agent_working: false }),
            fullTask(2, 1, { assignee: agent, agent_working: true }),
            fullTask(3, 1, { assignee: agent, agent_working: true, claimed_by: claim, status: 'active' }),
            fullTask(4, 1, { assignee: agent, agent_working: false, status: 'resolved' }),
            fullTask(5, 1, { assignee: { id: 5, name: 'Ada' }, agent_working: false }),
            fullTask(7, 1, { assignee: { id: 5, name: 'Ada' }, agent_working: false, status: 'resolved' }),
        ], { reviewers: { 4: 'Review bot' } });
        renderWithProviders(<IdentityContext.Provider value={{ identity: { mode: 'authenticated', workspace_role: 'operator' } as never, refresh: vi.fn(), signOut: vi.fn() }}>
            <MyWorkPage /></IdentityContext.Provider>, { initialEntries: ['/my-work'] });
        await screen.findByRole('button', { name: '#1 · Task 1' });
        const lineOf = (title: string) => rowOf(title).querySelector('[data-agent-dispatch]')?.textContent;
        await waitFor(() => expect(lineOf('Task 1')).toBe('Agent status: No agent connected'));
        expect(lineOf('Task 2')).toBe('Agent status: Queued');
        expect(lineOf('Task 3')).toBe('Agent status: Working');
        await waitFor(() => expect(rowOf('Task 4')).toHaveTextContent('Reviewer: Review bot'));
        expect(lineOf('Task 4')).toBe('Agent status: Waiting for review');
        // A person has no status line; a submitted task with no reviewer agent can be reviewed by anyone.
        expect(lineOf('Task 5')).toBeUndefined();
        expect(rowOf('Task 7')).toHaveTextContent('Reviewer: anyone');
        expect(rowOf('Task 1')).not.toHaveTextContent('Reviewer');
        // Whether the agent is connected comes with the team read, not the agent roster.
        expect(api.get.mock.calls.some(([path]) => path === '/agent/actors')).toBe(false);
        // My Work already named both reviewers, so no task is read again for them.
        expect(api.get.mock.calls.filter(([path]) => /^\/tasks\/\d+\/detail$/.test(path))).toEqual([]);
    });

    it('tells a local reader without the agent roster that a connected agent has not been sent the task yet', async () => {
        const agent = { id: 6, name: 'Build agent' };
        arrange([
            fullTask(1, 1, { assignee: agent, agent_working: false }),
            fullTask(2, 1, { assignee: agent, agent_working: true }),
            fullTask(3, 1, { assignee: agent, agent_working: true, claimed_by: { id: 3, name: 'builder', display_name: 'Builder' }, status: 'active' }),
            fullTask(4, 1, { assignee: agent, agent_working: false, status: 'closed' }),
        ], { agentConnected: true });
        renderWithProviders(<IdentityContext.Provider value={{ identity: { mode: 'trusted_local', principal: null, profile: { id: 4, display_name: 'Sam Ortiz', verified: false } } as never, refresh: vi.fn(), signOut: vi.fn() }}>
            <MyWorkPage /></IdentityContext.Provider>, { initialEntries: ['/my-work'] });
        await screen.findByRole('button', { name: '#1 · Task 1' });
        const lineOf = (title: string) => rowOf(title).querySelector('[data-agent-dispatch]')?.textContent;
        // The same line an operator sees: the team read says the agent is connected.
        await waitFor(() => expect(lineOf('Task 1')).toBe('Agent status: Not sent to the agent yet'));
        expect(lineOf('Task 2')).toBe('Agent status: Queued');
        expect(lineOf('Task 3')).toBe('Agent status: Working');
        // A closed task has no status line.
        expect(lineOf('Task 4')).toBeUndefined();
        expect(api.get.mock.calls.some(([path]) => path === '/agent/actors')).toBe(false);
    });

    it('names the Reviewer on every page of My Work, following the continuation cursor', async () => {
        const first = [1, 2].map(id => fullTask(id, 1, { status: 'resolved' }));
        const second = [3, 4].map(id => fullTask(id, 1, { status: 'resolved' }));
        const names: Record<number, string | null> = { 1: 'Review bot', 2: null, 3: 'Second bot', 4: null };
        const page = (items: Task[], hasMore: boolean) => ({ data: { state: 'ready', has_more: hasMore, next_after_id: hasMore ? items[items.length - 1].id : null,
            queues: { active: [], queued: [], blocked: [], awaiting_review: items.map(item => ({ ...reference(item.id, 1, 'resolved'), reviewer_name: names[item.id] })) } } });
        arrange([...first, ...second], { more: (path, config) => path === '/tasks/my-work'
            ? config?.params?.after_id === 2 ? page(second, false) : page(first, true) : undefined });
        const { user } = renderWithProviders(<MyWorkPage />, { initialEntries: ['/my-work?queue=awaiting_review'] });
        await screen.findByRole('button', { name: '#1 · Task 1' });
        await waitFor(() => expect(rowOf('Task 1')).toHaveTextContent('Reviewer: Review bot'));
        expect(rowOf('Task 2')).toHaveTextContent('Reviewer: anyone');
        await user.click(screen.getByRole('button', { name: 'Load more' }));
        await screen.findByRole('button', { name: '#3 · Task 3' });
        expect(api.get).toHaveBeenCalledWith('/tasks/my-work', { params: { after_id: 2 } });
        await waitFor(() => expect(rowOf('Task 3')).toHaveTextContent('Reviewer: Second bot'));
        expect(rowOf('Task 4')).toHaveTextContent('Reviewer: anyone');
        expect(screen.queryByRole('button', { name: 'Load more' })).toBeNull();
        expect(api.get.mock.calls.filter(([path]) => /^\/tasks\/\d+\/detail$/.test(path))).toEqual([]);
    });

    it('reads the Reviewer of each task in the review queue from the task detail read', async () => {
        const tasks = [fullTask(4, 1, { status: 'resolved' }), fullTask(5, 1, { status: 'resolved' })];
        arrange(tasks, { more: path => {
            // The review queue lists tasks without naming their reviewer.
            if (path === '/tasks/review-queue') return { data: { items: tasks.map(item => reference(item.id, 1, 'resolved')), has_more: false, next_after_id: null, limit: 50 } };
            const detail = /^\/tasks\/(\d+)\/detail$/.exec(path);
            if (detail) return { data: taskDetailResponse(tasks.find(item => item.id === Number(detail[1]))!, detail[1] === '4' ? 'Review bot' : null) };
            return undefined;
        } });
        renderWithProviders(<MyWorkPage />, { initialEntries: ['/my-work?queue=review'] });
        await screen.findByRole('button', { name: '#4 · Task 4' });
        await waitFor(() => expect(rowOf('Task 4')).toHaveTextContent('Reviewer: Review bot'));
        expect(rowOf('Task 5')).toHaveTextContent('Reviewer: anyone');
        expect(api.get).toHaveBeenCalledWith('/tasks/4/detail', expect.objectContaining({ params: { limit: 1 } }));
        expect(api.get).toHaveBeenCalledWith('/tasks/5/detail', expect.objectContaining({ params: { limit: 1 } }));
    });

    it('selects a range and assigns it from the bulk bar without a mode to enter', async () => {
        arrange([1, 2, 3, 4].map(id => fullTask(id, 1)));
        const { user } = renderWithProviders(<MyWorkPage />, { initialEntries: ['/my-work'] });
        await screen.findByRole('button', { name: '#1 · Task 1' });
        await waitFor(() => expect(within(rowOf('Task 1')).getByRole('combobox', { name: 'Assignee: Task 1' })).toBeInTheDocument());
        expect(screen.getAllByRole('checkbox')).toHaveLength(4);

        await user.click(await screen.findByRole('checkbox', { name: 'Select: Task 1' }));
        await user.keyboard('{Shift>}');
        await user.click(screen.getByRole('checkbox', { name: 'Select: Task 3' }));
        await user.keyboard('{/Shift}');
        expect(screen.getByText('Selected tasks: 3')).toBeInTheDocument();
        await user.click(screen.getByRole('button', { name: 'Assign' }));
        await user.selectOptions(await screen.findByRole('combobox', { name: 'Choose assignee' }), 'Ada');
        await user.click(screen.getByRole('button', { name: 'Apply' }));

        await waitFor(() => expect(api.post.mock.calls.filter(([path]) => path === '/tasks/bulk-operations')).toHaveLength(2));
        const applied = api.post.mock.calls.filter(([path]) => path === '/tasks/bulk-operations').at(-1)![1];
        expect(applied).toMatchObject({ action: 'set_assignee', payload: { assignee_id: 5 }, dry_run: false, task_ids: [1, 2, 3] });
    });

    it('keeps a selection to one iteration, because a bulk change applies to one', async () => {
        arrange([fullTask(1, 1), fullTask(2, 2)]);
        const { user } = renderWithProviders(<MyWorkPage />, { initialEntries: ['/my-work'] });
        await screen.findByRole('button', { name: '#1 · Task 1' });
        await waitFor(() => expect(within(rowOf('Task 2')).getByRole('combobox', { name: 'Assignee: Task 2' })).toBeInTheDocument());

        fireEvent.mouseOver(rowOf('Task 1'));
        await user.click(await screen.findByRole('checkbox', { name: 'Select: Task 1' }));
        const other = await within(rowOf('Task 2')).findByRole('checkbox', { name: 'Select: Task 2' });
        expect(other).toBeDisabled();
        expect(other).toHaveAttribute('title', expect.stringContaining('one iteration'));
    });
});

const signedInIdentity = { mode: 'managed', authenticated: true, principal: { id: 7, kind: 'human', display_name: 'Ada' }, profile: { id: 4, display_name: 'Ada' }, projects: {}, workspace_role: 'member' } as const;
const SignedInWork = () => <IdentityContext.Provider value={{ identity: { ...signedInIdentity, configured: true, csrf_token: null }, refresh: vi.fn(), signOut: vi.fn() }}><MyWorkPage /></IdentityContext.Provider>;

const Location = () => <output data-testid="location">{useLocation().search}</output>;

it.each(['active', 'queued', 'blocked', 'awaiting_review', 'review'])('loads the Notifications count without deliveries from the %s queue until Notifications opens', async queue => {
    api.get.mockImplementation(async (path: string) => {
        if (path === '/tasks/my-work') return { data: { state: 'ready', queues: {}, has_more: false, next_after_id: null } };
        if (path === '/notifications') return { data: { items: [
            { id: 1, task_id: 7, title: 'Task updated', event_type: 'status_changed', read: false },
        ], has_more: true, next_after_id: 1 } };
        if (path === '/notifications/deliveries') return { data: { items: [
            { id: 2, task_id: 7, title: 'First delivery', status: 'sent', attempt_count: 1, max_attempts: 3 },
            { id: 3, task_id: 7, title: 'Second delivery', status: 'sent', attempt_count: 1, max_attempts: 3 },
        ], has_more: false, next_after_id: null } };
        return { data: { items: [], has_more: false, next_after_id: null } };
    });
    renderWithProviders(<SignedInWork />, { initialEntries: [`/my-work?queue=${queue}`] });

    const notifications = await screen.findByRole('button', { name: 'Notifications · 1+', pressed: false });
    expect(await screen.findByRole('button', { name: 'To review · 0' })).toBeInTheDocument();
    expect(api.get).not.toHaveBeenCalledWith('/notifications/deliveries', expect.anything());

    fireEvent.click(notifications);
    expect(await screen.findByText(/First delivery/)).toBeInTheDocument();
    expect(screen.getByText(/Second delivery/)).toBeInTheDocument();
    expect(api.get).toHaveBeenCalledWith('/notifications/deliveries', { params: { after_id: 0 } });
    expect(screen.getByRole('button', { name: 'Notifications · 1+', pressed: true })).toBeInTheDocument();
});

it('switches six counted queues and preserves the choice in the URL', async () => {
    api.get.mockImplementation(async (path: string) => {
        if (path === '/tasks/my-work') return { data: { state: 'ready', queues: { active: [], queued: [], blocked: [{ id: 7, title: 'Blocked task', status: 'planned', iteration_id: null }], awaiting_review: [] }, has_more: true, next_after_id: 7 } };
        if (path === '/tasks/review-queue' || path.startsWith('/notifications')) return { data: { items: [], has_more: false } };
        return { data: [] };
    });
    const { container } = renderWithProviders(<><SignedInWork /><Location /></>, { initialEntries: ['/my-work?queue=blocked'] });
    const group = within(container.querySelector('.seg') as HTMLElement);
    await waitFor(() => expect(group.getAllByRole('button')).toHaveLength(6));
    expect(await group.findByRole('button', { name: 'Blocked · 1+', pressed: true })).toBeInTheDocument();
    fireEvent.click(group.getByRole('button', { name: 'Up next · 0+' }));
    expect(screen.getByTestId('location')).toHaveTextContent('queue=queued');
    expect(group.getByRole('button', { name: 'Up next · 0+', pressed: true })).toBeInTheDocument();
    expectPageChrome(container, { status: 'migrated' });
});


it.each(['active', 'inbox'])('hides Notifications for a local person on the %s URL and explains why without requesting it', async queue => {
    api.get.mockImplementation(async (path: string) => ({ data: path === '/tasks/my-work'
        ? { state: 'ready', queues: {}, has_more: false } : { items: [], has_more: false } }));
    renderWithProviders(<IdentityContext.Provider value={{ identity: { mode: 'trusted_local', authenticated: false, principal: null, profile: { id: 4, display_name: 'Sam' } } as never, refresh: vi.fn(), signOut: vi.fn() }}><MyWorkPage /></IdentityContext.Provider>, { initialEntries: [`/my-work?queue=${queue}`] });
    expect(await screen.findByRole('button', { name: 'Doing · 0' })).toBeInTheDocument();
    expect(screen.getByText('Notifications are available only to a signed-in account, not a local person profile.')).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: /Notifications/ })).not.toBeInTheDocument();
    expect(api.get.mock.calls.some(([path]) => path.startsWith('/notifications'))).toBe(false);
});

it('shows postponed, canceled and superseded work as their own states and filters by each', async () => {
    await ensureLanguageResources('en');
    await i18n.changeLanguage('en');
    api.get.mockImplementation(async (path: string) => {
        if (path === '/tasks/my-work') return { data: { state: 'ready', has_more: false, next_after_id: null, queues: { active: [
            { id: 1, title: 'Live work', status: 'active', iteration_id: null },
            { id: 2, title: 'Paused work', status: 'postponed', displayed_state: 'postponed', iteration_id: null },
            // Canceled work keeps the status it had; it must read as canceled, not active.
            { id: 3, title: 'Dropped work', status: 'active', displayed_state: 'canceled', iteration_id: null },
            { id: 4, title: 'Replaced work', status: 'planned', displayed_state: 'superseded', iteration_id: null },
        ], queued: [], blocked: [], awaiting_review: [] } } };
        if (path === '/tasks/review-queue' || path.startsWith('/notifications')) return { data: { items: [], has_more: false } };
        return { data: [] };
    });
    renderWithProviders(<SignedInWork />, { initialEntries: ['/my-work?queue=active'] });
    const rowOf = async (title: string) => (await screen.findByRole('button', { name: new RegExp(`· ${title}$`) })).closest('[data-task-row]') as HTMLElement;
    expect(within(await rowOf('Paused work')).getByText('Postponed', { selector: '[data-task-state]' })).toBeVisible();
    expect(within(await rowOf('Dropped work')).getByText('Canceled', { selector: '[data-task-state]' })).toBeVisible();
    expect(within(await rowOf('Replaced work')).getByText('Superseded', { selector: '[data-task-state]' })).toBeVisible();
    expect((await rowOf('Live work')).querySelector('[data-task-state]')).toBeNull();

    const filter = screen.getByRole('combobox', { name: 'State' });
    expect(within(filter).getAllByRole('option').map(option => option.textContent)).toEqual(
        ['All states', 'Planned', 'Active', 'Resolved', 'Closed', 'Postponed', 'Canceled', 'Superseded']);
    // Choosing a state narrows the queue by what each task is shown as, not the status it kept.
    fireEvent.change(filter, { target: { value: 'active' } });
    expect(screen.getByRole('button', { name: /· Live work$/ })).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: /· Dropped work$/ })).not.toBeInTheDocument();
    fireEvent.change(filter, { target: { value: 'canceled' } });
    expect(screen.getByRole('button', { name: /· Dropped work$/ })).toBeInTheDocument();
    expect(screen.queryByRole('button', { name: /· Live work$/ })).not.toBeInTheDocument();
    fireEvent.change(filter, { target: { value: 'closed' } });
    expect(screen.getByText('Nothing in this queue is Closed.')).toBeInTheDocument();
});

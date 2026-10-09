import { QueryObserver } from '@tanstack/react-query';
import { expect, it, vi } from 'vitest';
import { createWorkspaceQueryClient, installWorkspaceQueryPolicy } from './workspaceQueryPolicy';
import { WORKSPACE_QUERY_POLICIES } from './workQueryFreshness';

it.each(['hidden', 'disabled', 'unauthorized', 'too-many-pages'])('does not poll %s work', state => {
    const client = createWorkspaceQueryClient('account');
    const stop = installWorkspaceQueryPolicy(client);
    const observer = new QueryObserver(client, { queryKey: ['human-my-work'],
        queryFn: async () => ({ loaded: true }), enabled: state !== 'disabled' });
    const unsubscribe = observer.subscribe(() => {});
    try {
        client.setQueryData(['human-my-work'], state === 'too-many-pages' ? { pages: Array(6).fill({}) } : { loaded: true });
        const query = client.getQueryCache().find({ queryKey: ['human-my-work'] })!;
        if (state === 'hidden') vi.spyOn(document, 'visibilityState', 'get').mockReturnValue('hidden');
        if (state === 'unauthorized') query.setState({ error: { response: { status: 403 } } as unknown as Error });
        const interval = client.defaultQueryOptions({ queryKey: query.queryKey }).refetchInterval;
        expect(typeof interval === 'function' && interval(query)).toBe(false);
    } finally {
        unsubscribe(); stop(); vi.restoreAllMocks();
    }
});

it('backs off transient polling without enabling history or editor refresh', () => {
    const client = createWorkspaceQueryClient('account');
    const stop = installWorkspaceQueryPolicy(client);
    const observer = new QueryObserver(client, { queryKey: ['tasks'], queryFn: async () => [] });
    const unsubscribe = observer.subscribe(() => {});
    try {
        const query = client.getQueryCache().find({ queryKey: ['tasks'] })!;
        query.setState({ fetchFailureCount: 2 });
        const interval = client.defaultQueryOptions({ queryKey: query.queryKey }).refetchInterval;
        expect(typeof interval === 'function' && interval(query)).toBe(120000);
        expect(client.defaultQueryOptions({ queryKey: ['time-history', 1] }).refetchInterval).toBe(false);
        expect(client.defaultQueryOptions({ queryKey: ['taskEditor', 1] }).refetchInterval).toBe(false);
    } finally { unsubscribe(); stop(); }
});

it('keeps the legacy fallback while explicit unrelated effects avoid work invalidation', async () => {
    const client = createWorkspaceQueryClient('account');
    const stop = installWorkspaceQueryPolicy(client);
    try {
        client.setQueryData(['human-my-work'], { loaded: true });
        await client.getMutationCache().build(client, { mutationFn: async () => ({}), meta: { workQueryRoots: [] } }).execute(undefined);
        expect(client.getQueryState(['human-my-work'])?.isInvalidated).toBe(false);
        await client.getMutationCache().build(client, { mutationFn: async () => ({}) }).execute(undefined);
        expect(client.getQueryState(['human-my-work'])?.isInvalidated).toBe(true);
        client.setQueryData(['project-summary', 1], { total: 1 });
        await client.getMutationCache().build(client, { mutationFn: async () => ({}) }).execute(undefined);
        expect(client.getQueryState(['project-summary', 1])?.isInvalidated).toBe(true);
    } finally { stop(); }
});

it('aborts old account requests and cannot repopulate the replacement cache', async () => {
    const old = createWorkspaceQueryClient('old-access');
    const stop = installWorkspaceQueryPolicy(old);
    let finish!: (value: string) => void;
    let aborted = false;
    const pending = old.fetchQuery({ queryKey: ['tasks'], queryFn: ({ signal }) => {
        signal.addEventListener('abort', () => { aborted = true; });
        return new Promise<string>(resolve => { finish = resolve; });
    } }).catch(() => undefined);
    stop();
    const current = createWorkspaceQueryClient('new-access');
    const stopCurrent = installWorkspaceQueryPolicy(current);
    try {
        finish('Old private data');
        await pending;
        expect(aborted).toBe(true);
        expect(old.getQueryData(['tasks'])).toBeUndefined();
        expect(current.getQueryData(['tasks'])).toBeUndefined();
        expect(current.getDefaultOptions().queries?.meta?.workspaceAccess).toBe('new-access');
    } finally { stopCurrent(); }
});

it('declares the operational, editor and immutable roots separately', () => {
    expect(WORKSPACE_QUERY_POLICIES['human-my-work']).toBe('live');
    expect(WORKSPACE_QUERY_POLICIES['planning-navigation-summary']).toBe('live');
    expect(WORKSPACE_QUERY_POLICIES['taskEditor']).toBe('editor');
    expect(WORKSPACE_QUERY_POLICIES['time-history']).toBe('history');
});

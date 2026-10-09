import { act, waitFor } from '@testing-library/react';
import { QueryClientProvider } from '@tanstack/react-query';
import { renderHook } from '@testing-library/react';
import { expect, it, vi } from 'vitest';
import { createWorkspaceQueryClient, installWorkspaceQueryPolicy } from './workspaceQueryPolicy';
import { useLiveWindow, validateWindowCursor, deduplicateWindow } from './useLiveWindow';

it('retains four pages plus head discovery after many loads, without changing selection', async () => {
    const client = createWorkspaceQueryClient('one-user'); const stop = installWorkspaceQueryPolicy(client);
    const read = vi.fn(async ({ pageParam }: { pageParam: number }) => ({ items: [{ id: pageParam + 1 }], has_more: true, next_after_id: pageParam + 1 }));
    const view = renderHook(() => useLiveWindow({ queryKey: ['human-my-work'], initialPageParam: 0,
        queryFn: read, getNextPageParam: page => page.next_after_id }), { wrapper: ({ children }) => <QueryClientProvider client={client}>{children}</QueryClientProvider> });
    await waitFor(() => expect(view.result.current.isSuccess).toBe(true));
    for (let i = 0; i < 12; i++) await act(() => view.result.current.fetchNextPage());
    expect(view.result.current.data?.pages).toHaveLength(4);
    expect(view.result.current.outsideWindow).toBe(true);
    const before = read.mock.calls.length;
    await act(() => client.refetchQueries({ type: 'active' }));
    expect(read.mock.calls.length - before).toBeLessThanOrEqual(5);
    await act(() => view.result.current.restart());
    await waitFor(() => expect(view.result.current.data?.pageParams[0]).toBe(0));
    view.unmount(); stop();
});

it.each([0, -1, NaN, undefined])('rejects missing, cyclic or backward cursor %s', cursor => {
    expect(() => validateWindowCursor({ has_more: true }, 2, cursor)).toThrow();
});

it('respects observed upper bounds and removes duplicate window rows', () => {
    expect(() => validateWindowCursor({ has_more: true }, { after: 2, upper: 4 }, { after: 5, upper: 4 })).toThrow();
    expect(deduplicateWindow({ pages: [{ items: [{ id: 1 }, { id: 2 }] }, { items: [{ id: 2 }, { id: 3 }] }], pageParams: [0, 2] })
        .pages.flatMap(page => page.items).map(item => item.id)).toEqual([1, 2, 3]);
});

it('removes unauthorized cached data and stops scheduled retries', async () => {
    const client = createWorkspaceQueryClient('one-user'); const stop = installWorkspaceQueryPolicy(client);
    client.setQueryData(['human-my-work'], { private: 'old work' });
    await client.fetchQuery({ queryKey: ['human-my-work'], staleTime: 0, queryFn: () => Promise.reject({ response: { status: 403 } }) }).catch(() => undefined);
    expect(client.getQueryData(['human-my-work'])).toBeUndefined();
    stop();
});

it('uses at most five foreground requests per interval after deep pagination', async () => {
    vi.useFakeTimers();
    const client = createWorkspaceQueryClient('clock-user'); const stop = installWorkspaceQueryPolicy(client);
    let version = 1;
    const read = vi.fn(async ({ pageParam }: { pageParam: number }) => ({ items: [{ id: pageParam + 1, version }], has_more: true, next_after_id: pageParam + 1 }));
    const view = renderHook(() => useLiveWindow({ queryKey: ['human-my-work'], initialPageParam: 0,
        queryFn: read, getNextPageParam: page => page.next_after_id }), { wrapper: ({ children }) => <QueryClientProvider client={client}>{children}</QueryClientProvider> });
    try {
        await act(async () => { await vi.advanceTimersByTimeAsync(1); });
        for (let i = 0; i < 10; i++) await act(async () => { await view.result.current.fetchNextPage(); await vi.advanceTimersByTimeAsync(1); });
        const before = read.mock.calls.length; version = 2;
        await act(async () => { await vi.advanceTimersByTimeAsync(30000); });
        expect(read.mock.calls.length - before).toBeLessThanOrEqual(5);
        expect(read.mock.calls.length - before).toBeGreaterThan(0);
        expect(view.result.current.data?.pages.flatMap(page => page.items).every(item => item.version === 2)).toBe(true);
        expect(view.result.current.outsideWindow).toBe(true);
    } finally { view.unmount(); stop(); vi.useRealTimers(); }
});

import { useInfiniteQuery, useQuery, useQueryClient, type InfiniteData, type QueryKey, type UseInfiniteQueryOptions } from '@tanstack/react-query';
import { useState } from 'react';

const position = (value: unknown): number => {
    if (value === null || value === undefined) return 0;
    if (typeof value === 'number') return value;
    if (typeof value === 'object' && 'after' in value) return Number(value.after);
    return Number.NaN;
};

export const validateWindowCursor = (page: unknown, current: unknown, next: unknown) => {
    if (!page || typeof page !== 'object') throw new Error('The page response is incomplete.');
    const more = (page as { has_more?: boolean }).has_more;
    if ('has_more' in page && typeof more !== 'boolean') throw new Error('The page completeness flag is invalid.');
    if (!('has_more' in page) && !('next_cursor' in page)) throw new Error('The page completeness flag is missing.');
    if (more && (next === null || next === undefined)) throw new Error('The page is incomplete: a continuation cursor is missing.');
    if (next !== null && next !== undefined && (!Number.isSafeInteger(position(next)) || position(next) <= position(current))) {
        throw new Error('The continuation cursor is invalid. Reload the latest window.');
    }
    const upper = (next as { upper?: number } | null)?.upper;
    if (upper !== undefined && (!Number.isSafeInteger(upper) || position(next) > upper)) throw new Error('The continuation exceeds its observed window.');
};

export const deduplicateWindow = <T, P>(data: InfiniteData<T, P>): InfiniteData<T, P> => {
    const seen = new Set<unknown>();
    const newest = new Map<unknown, { version: number; item: unknown }>();
    for (const page of data.pages) {
        const value = page as { items?: unknown[]; queues?: Record<string, unknown[]> };
        const rows = value.items ?? (value.queues ? Object.values(value.queues).flat() : []);
        for (const item of rows) {
            const row = item as { id?: number; task_id?: number; version?: number };
            const key = row.id ?? row.task_id;
            if (key !== undefined && (!newest.has(key) || (row.version ?? 0) > newest.get(key)!.version)) {
                newest.set(key, { version: row.version ?? 0, item });
            }
        }
    }
    const filter = (items: unknown[]) => items.filter(item => {
        const row = item as { id?: number; task_id?: number };
        const id = row.id ?? row.task_id;
        if (id === undefined) return true;
        if (seen.has(id) || newest.get(id)?.item !== item) return false;
        seen.add(id); return true;
    });
    return { ...data, pages: data.pages.map(page => {
        const value = page as { items?: unknown[]; queues?: Record<string, unknown[]> };
        if (Array.isArray(value.items)) return { ...value, items: filter(value.items) } as T;
        if (value.queues) return { ...value, queues: Object.fromEntries(Object.entries(value.queues).map(([queue, rows]) => [queue, filter(rows)])) } as T;
        return page;
    }) };
};

export function useLiveWindow<T, P>(options: UseInfiniteQueryOptions<T, Error, InfiniteData<T, P>, QueryKey, P>) {
    const client = useQueryClient();
    const [generation, setGeneration] = useState(0);
    const key = [...options.queryKey, 'window', generation];
    const original = options.queryFn;
    const read: NonNullable<typeof options.queryFn> = async context => {
        if (typeof original !== 'function') throw new Error('This window has no reader.');
        const page = await original(context);
        const next = options.getNextPageParam(page, [page], context.pageParam as P, [context.pageParam as P]);
        validateWindowCursor(page, context.pageParam, next);
        return page;
    };
    // feedback-policy: query loading,error,retry,empty - consumers retain explicit errors and window controls.
    const result = useInfiniteQuery({ ...options, queryKey: key, gcTime: 0, queryFn: read, maxPages: 4, select: data => deduplicateWindow(data) });
    const outsideWindow = Boolean(result.data?.pageParams.length && JSON.stringify(result.data.pageParams[0]) !== JSON.stringify(options.initialPageParam));
    // feedback-policy: query loading,error,retry,empty - head failure is visible; discovery never replaces a draft.
    const head = useQuery({ queryKey: ['live-window-head', ...options.queryKey],
        enabled: outsideWindow && options.enabled !== false,
        queryFn: ({ signal }) => {
            if (typeof original !== 'function') throw new Error('This window has no reader.');
            return read({ signal, client, queryKey: options.queryKey, pageParam: options.initialPageParam,
                direction: 'forward', meta: options.meta });
        } });
    return { ...result, outsideWindow, headError: outsideWindow && head.isError,
        headUpdatedAt: head.dataUpdatedAt,
        restart: async () => {
            await client.cancelQueries({ queryKey: key, exact: true });
            setGeneration(value => value + 1);
        } };
}

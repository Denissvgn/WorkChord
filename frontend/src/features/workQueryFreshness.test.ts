import { QueryClient, QueryObserver } from '@tanstack/react-query';
import { expect, it } from 'vitest';
import { installWorkFreshness } from './workQueryFreshness';

const roots = ['human-my-work', 'human-review-queue', 'personal-inbox',
    'personal-deliveries', 'time-entries', 'time-report'];

const cases = roots.flatMap(root => ['polling', 'mutation'].map(behavior => ({ root, behavior })));

it.each(cases)('applies $behavior freshness to $root', async ({ root, behavior }) => {
    const client = new QueryClient();
    const stop = installWorkFreshness(client);
    try {
        client.setQueryData([root], { loaded: true });
        if (behavior === 'polling') {
            const observer = new QueryObserver(client, {
                queryKey: [root], queryFn: async () => ({ loaded: true }), enabled: true });
            const unsubscribe = observer.subscribe(() => {});
            try {
                const query = client.getQueryCache().find({ queryKey: [root] })!;
                expect(query.isActive()).toBe(true);
                const interval = client.defaultQueryOptions({ queryKey: query.queryKey }).refetchInterval;
                expect(interval).toBeTypeOf('function');
                if (typeof interval === 'function') expect(interval(query)).toBe(30000);
            } finally {
                unsubscribe();
            }
        } else {
            await client.getMutationCache().build(client, { mutationFn: async () => ({ saved: true }) }).execute(undefined);
            expect(client.getQueryState([root])?.isInvalidated).toBe(true);
        }
    } finally {
        stop();
        client.clear();
    }
});

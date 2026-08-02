import type { QueryClient, QueryCacheNotifyEvent } from '@tanstack/react-query';
import { planningNavigationSummaryKey } from './usePlanningNavigationSummary';

const READINESS_INPUT_QUERY_ROOTS = new Set(['tasks', 'team', 'gantt']);

export const installPlanningNavigationInvalidation = (queryClient: QueryClient) => (
    queryClient.getQueryCache().subscribe((event: QueryCacheNotifyEvent) => {
        if (
            event.type !== 'updated'
            || event.action.type !== 'invalidate'
            || !READINESS_INPUT_QUERY_ROOTS.has(String(event.query.queryKey[0]))
        ) {
            return;
        }

        void queryClient.invalidateQueries({
            queryKey: planningNavigationSummaryKey(),
        });
    })
);

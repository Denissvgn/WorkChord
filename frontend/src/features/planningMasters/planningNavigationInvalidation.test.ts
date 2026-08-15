import { QueryClient } from '@tanstack/react-query';
import { describe, expect, it } from 'vitest';
import { installPlanningNavigationInvalidation } from './planningNavigationInvalidation';
import { planningNavigationSummaryKey } from './usePlanningNavigationSummary';

describe('planning navigation invalidation', () => {
    it('marks the compact summary stale when a planning input is invalidated', async () => {
        const queryClient = new QueryClient();
        const unsubscribe = installPlanningNavigationInvalidation(queryClient);
        queryClient.setQueryData(planningNavigationSummaryKey(7), { task_count: 3 });
        queryClient.setQueryData(['tasks', 7], []);

        await queryClient.invalidateQueries({ queryKey: ['tasks', 7] });

        expect(queryClient.getQueryState(planningNavigationSummaryKey(7))?.isInvalidated)
            .toBe(true);
        unsubscribe();
    });
});

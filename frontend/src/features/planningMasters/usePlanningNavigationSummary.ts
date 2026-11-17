import { useMemo } from 'react';
import { useQuery } from '@tanstack/react-query';
import { iterationService } from '../../services/iterationService';
import { useIterationStore } from '../../store/iterationStore';
import type { Iteration, IterationPlanningReadinessSummary } from '../../types/iteration';
import { PLANNING_STEP_IDS } from './planningReturn';

export const planningNavigationSummaryKey = (iterationId?: number) => (
    iterationId === undefined
        ? ['planning-navigation-summary'] as const
        : ['planning-navigation-summary', iterationId] as const
);

/**
 * How far one iteration's plan is, read from its planning readiness response: the
 * checkpoints done of the total, and the first checkpoint that is not complete.
 *
 * Null without an iteration or without a complete response (all six checkpoints): there is
 * no progress to show, and nothing is worked out in the browser.
 */
export const planProgress = (
    iteration: Iteration | null,
    summary: IterationPlanningReadinessSummary | undefined,
) => {
    if (iteration === null || !summary?.checkpoints) return null;
    const byId = new Map(summary.checkpoints.map(item => [item.id, item.state]));
    if (PLANNING_STEP_IDS.some(id => !byId.has(id))) return null;
    const total = PLANNING_STEP_IDS.length;
    const done = PLANNING_STEP_IDS.filter(id => byId.get(id) === 'done').length;
    return {
        ready: { done, total, pct: Math.round((done / total) * 100) },
        nextId: PLANNING_STEP_IDS.find(id => byId.get(id) !== 'done') ?? '',
    };
};

const NO_PROGRESS = { done: 0, total: PLANNING_STEP_IDS.length, pct: 0 };

export const usePlanningNavigationSummary = () => {
    const { selectedIterationId, setSelectedIterationId } = useIterationStore();
    // feedback-policy: query loading,error,retry,empty - shell consumers render
    // compact loading, unavailable, retry, and no-period states.
    const iterationsQuery = useQuery({
        queryKey: ['iterations'],
        queryFn: iterationService.getAll,
        staleTime: 60000,
    });
    const iterations = useMemo(() => iterationsQuery.data ?? [], [iterationsQuery.data]);
    const currentIteration = useMemo<Iteration | null>(
        () => iterations.find(iteration => iteration.id === selectedIterationId) ?? null,
        [iterations, selectedIterationId],
    );
    const hasCurrentIteration = selectedIterationId > 0 && currentIteration !== null;
    // feedback-policy: query loading,error,retry,empty - the sidebar owns progress
    // loading/retry UI; the top bar labels unavailable planning attention.
    const summaryQuery = useQuery({
        queryKey: planningNavigationSummaryKey(selectedIterationId),
        queryFn: () => iterationService.getPlanningReadiness(selectedIterationId),
        enabled: hasCurrentIteration,
        staleTime: 60000,
    });

    const progress = useMemo(
        () => planProgress(currentIteration, summaryQuery.data),
        [currentIteration, summaryQuery.data],
    );

    const refetch = async () => Promise.allSettled([
        iterationsQuery.refetch(),
        ...(hasCurrentIteration ? [summaryQuery.refetch()] : []),
    ]);

    return {
        iterations,
        currentIteration,
        selectedIterationId,
        selectIteration: setSelectedIterationId,
        ready: progress?.ready ?? NO_PROGRESS,
        /** The first checkpoint that is not complete. */
        nextId: progress?.nextId ?? '',
        isIterationsLoading: iterationsQuery.isLoading,
        isIterationsError: iterationsQuery.isError && iterationsQuery.data === undefined,
        isIterationsFetching: iterationsQuery.isFetching,
        isReadinessLoading: hasCurrentIteration && summaryQuery.isLoading,
        isReadinessError: (
            hasCurrentIteration
            && summaryQuery.isError
            && summaryQuery.data === undefined
        ),
        isReadinessFetching: hasCurrentIteration && summaryQuery.isFetching,
        // True only once an iteration is resolved and a complete readiness response has arrived;
        // `ready` is not a real count before that.
        isPlanProgressKnown: hasCurrentIteration && progress !== null,
        refetch,
    };
};

import { useMemo } from 'react';
import { useQuery } from '@tanstack/react-query';
import { iterationService } from '../../services/iterationService';
import { useIterationStore } from '../../store/iterationStore';
import type { Iteration } from '../../types/iteration';
import { deriveStatus, readiness } from './masters';
import type { PlanReadiness } from './masters';

export const planningNavigationSummaryKey = (iterationId?: number) => (
    iterationId === undefined
        ? ['planning-navigation-summary'] as const
        : ['planning-navigation-summary', iterationId] as const
);

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

    const readinessData = useMemo<PlanReadiness>(() => ({
        iterationCount: iterations.length,
        hasCurrentIteration,
        currentIterationName: currentIteration?.name ?? '',
        currentIterationStart: currentIteration?.start_date ?? '',
        currentIterationEnd: currentIteration?.end_date ?? '',
        currentIterationDays: currentIteration?.working_days ?? 0,
        teamMemberCount: summaryQuery.data?.team_member_count ?? 0,
        teamCapacity: summaryQuery.data?.team_capacity_hours ?? 0,
        teamMembersNoCap: summaryQuery.data?.team_members_no_capacity ?? 0,
        taskCount: summaryQuery.data?.task_count ?? 0,
        tasksWithoutAssignee: summaryQuery.data?.tasks_without_assignee ?? 0,
        tasksWithoutEffort: summaryQuery.data?.tasks_without_effort ?? 0,
        hasGanttSchedule: summaryQuery.data?.has_schedule ?? false,
        ganttLastBuilt: '',
        riskCount: summaryQuery.data?.risk_count ?? 0,
        inboxCount: 0,
    }), [currentIteration, hasCurrentIteration, iterations.length, summaryQuery.data]);
    const ready = useMemo(
        () => readiness(deriveStatus(readinessData)),
        [readinessData],
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
        ready,
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
        refetch,
    };
};

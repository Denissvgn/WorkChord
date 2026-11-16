import { useMemo } from 'react';
import { useQuery } from '@tanstack/react-query';
import { iterationService } from '../../services/iterationService';
import { useIterationStore } from '../../store/iterationStore';
import type { Iteration, IterationPlanningReadinessSummary } from '../../types/iteration';
import { deriveStatus, nextStep, readiness } from './masters';
import type { PlanReadiness } from './masters';

export const planningNavigationSummaryKey = (iterationId?: number) => (
    iterationId === undefined
        ? ['planning-navigation-summary'] as const
        : ['planning-navigation-summary', iterationId] as const
);

/**
 * How far one iteration's plan is, from its planning readiness response: the checkpoints
 * done of the total, and the first checkpoint that is not complete.
 */
export const planProgress = (
    iteration: Iteration | null,
    iterationCount: number,
    summary: IterationPlanningReadinessSummary | undefined,
) => {
    const readinessData: PlanReadiness = {
        iterationCount,
        hasCurrentIteration: iteration !== null,
        currentIterationName: iteration?.name ?? '',
        currentIterationStart: iteration?.start_date ?? '',
        currentIterationEnd: iteration?.end_date ?? '',
        currentIterationDays: iteration?.working_days ?? 0,
        teamMemberCount: summary?.team_member_count ?? 0,
        teamCapacity: summary?.team_capacity_hours ?? 0,
        teamMembersNoCap: summary?.team_members_no_capacity ?? 0,
        taskCount: summary?.task_count ?? 0,
        tasksWithoutAssignee: summary?.tasks_without_assignee ?? 0,
        tasksWithoutEffort: summary?.tasks_without_effort ?? 0,
        tasksAgentWithoutCapacity: summary?.tasks_agent_without_capacity ?? 0,
        teamAgentCount: summary?.team_agent_count ?? 0,
        hasGanttSchedule: summary?.has_schedule ?? false,
        ganttLastBuilt: '',
        riskCount: summary?.risk_count ?? 0,
        inboxCount: 0,
        checkpointStates: Object.fromEntries((summary?.checkpoints ?? []).map(item => [item.id, item.state])),
    };
    const status = deriveStatus(readinessData);
    return { ready: readiness(status), nextId: nextStep(status) };
};

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

    const { ready, nextId } = useMemo(
        () => planProgress(currentIteration, iterations.length, summaryQuery.data),
        [currentIteration, iterations.length, summaryQuery.data],
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
        /** The first checkpoint that is not complete. */
        nextId,
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
        // True only once an iteration is resolved and its readiness response has arrived;
        // `ready` is not a real count before that.
        isPlanProgressKnown: hasCurrentIteration && summaryQuery.data !== undefined,
        refetch,
    };
};

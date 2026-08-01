import { useEffect, useMemo } from 'react';
import { useQuery } from '@tanstack/react-query';
import { ganttService } from '../../services/ganttService';
import { iterationService } from '../../services/iterationService';
import { taskService } from '../../services/taskService';
import { teamService } from '../../services/teamService';
import { triageService } from '../../services/triageService';
import { useIterationStore } from '../../store/iterationStore';
import type { Iteration } from '../../types/iteration';
import type { Task } from '../../types/task';
import type { TeamMember } from '../../types/team';
import { deriveStatus, nextStep, readiness } from './masters';
import type { PlanReadiness } from './masters';

type PlanningReadinessOptions = {
    includeInbox?: boolean;
    autoSelectFirst?: boolean;
};

const flattenTasks = (list: Task[] = []): Task[] => {
    const out: Task[] = [];
    for (const task of list) {
        out.push(task);
        if (task.children?.length) out.push(...flattenTasks(task.children as Task[]));
    }
    return out;
};

export const usePlanningReadiness = ({
    includeInbox = false,
    autoSelectFirst = false,
}: PlanningReadinessOptions = {}) => {
    const { selectedIterationId, setSelectedIterationId } = useIterationStore();

    // feedback-policy: query loading,error,retry,empty - aggregate state is returned to the owning workspace.
    const iterationsQuery = useQuery({
        queryKey: ['iterations'],
        queryFn: iterationService.getAll,
        staleTime: 60000,
    });

    const iterations = useMemo(() => iterationsQuery.data ?? [], [iterationsQuery.data]);

    useEffect(() => {
        if (!iterationsQuery.isSuccess) return;

        const selectedExists = iterations.some(iteration => iteration.id === selectedIterationId);
        if (selectedIterationId > 0 && !selectedExists) {
            setSelectedIterationId(0);
            return;
        }

        if (autoSelectFirst && selectedIterationId === 0 && iterations.length > 0) {
            setSelectedIterationId(iterations[0].id);
        }
    }, [
        autoSelectFirst,
        iterations,
        iterationsQuery.isSuccess,
        selectedIterationId,
        setSelectedIterationId,
    ]);

    const currentIteration = useMemo<Iteration | null>(
        () => iterations.find(iteration => iteration.id === selectedIterationId) ?? null,
        [iterations, selectedIterationId],
    );

    const hasCurrentIteration = selectedIterationId > 0 && currentIteration !== null;

    // feedback-policy: query loading,error,retry,empty - aggregate state is returned to the owning workspace.
    const teamQuery = useQuery({
        queryKey: ['team', selectedIterationId],
        queryFn: () => teamService.getByIteration(selectedIterationId),
        enabled: hasCurrentIteration,
        staleTime: 60000,
    });

    // feedback-policy: query loading,error,retry,empty - aggregate state is returned to the owning workspace.
    const tasksQuery = useQuery({
        queryKey: ['tasks', selectedIterationId],
        queryFn: () => taskService.getByIteration(selectedIterationId),
        enabled: hasCurrentIteration,
        staleTime: 60000,
    });

    // feedback-policy: query loading,error,retry,empty - aggregate state is returned to the owning workspace.
    const ganttQuery = useQuery({
        queryKey: ['gantt', selectedIterationId],
        queryFn: () => ganttService.getChart(selectedIterationId),
        enabled: hasCurrentIteration,
        staleTime: 60000,
    });

    // feedback-policy: query loading,error,retry,empty - aggregate state is returned to the owning workspace.
    const inboxQuery = useQuery({
        queryKey: ['triage', { active: true, limit: 100 }],
        queryFn: () => triageService.getAll({ active: true, limit: 100 }),
        enabled: includeInbox,
        staleTime: 60000,
    });

    const teamMembers = useMemo(() => (teamQuery.data ?? []) as TeamMember[], [teamQuery.data]);
    const tasks = useMemo(() => (tasksQuery.data ?? []) as Task[], [tasksQuery.data]);
    const allTasks = useMemo(() => flattenTasks(tasks), [tasks]);

    const teamMembersNoCap = useMemo(
        () => teamMembers.filter(member => {
            const planned = (member as TeamMember & { planned?: number | null }).planned;
            return planned === null || planned === undefined;
        }).length,
        [teamMembers],
    );

    const teamCapacity = useMemo(
        () => teamMembers.reduce((total, member) => (
            total + ((member as TeamMember & { cap?: number }).cap ?? 0)
        ), 0),
        [teamMembers],
    );

    const readinessData = useMemo<PlanReadiness>(() => ({
        iterationCount: iterations.length,
        hasCurrentIteration,
        currentIterationName: currentIteration?.name ?? '',
        currentIterationStart: currentIteration?.start_date ?? '',
        currentIterationEnd: currentIteration?.end_date ?? '',
        currentIterationDays: currentIteration?.working_days ?? 0,
        teamMemberCount: teamMembers.length,
        teamCapacity,
        teamMembersNoCap,
        taskCount: allTasks.length,
        tasksWithoutAssignee: allTasks.filter(task => !task.assignee).length,
        tasksWithoutEffort: allTasks.filter(task => !task.effort_days || task.effort_days <= 0).length,
        hasGanttSchedule: ganttQuery.data?.schedule_result != null,
        ganttLastBuilt: '',
        riskCount: allTasks.filter(task => task.is_overdue).length,
        inboxCount: includeInbox ? (inboxQuery.data?.length ?? 0) : 0,
    }), [
        allTasks,
        currentIteration,
        ganttQuery.data,
        hasCurrentIteration,
        inboxQuery.data,
        includeInbox,
        iterations.length,
        teamCapacity,
        teamMembers.length,
        teamMembersNoCap,
    ]);

    const status = useMemo(() => deriveStatus(readinessData), [readinessData]);
    const ready = useMemo(() => readiness(status), [status]);
    const nextId = useMemo(() => nextStep(status), [status]);

    const readinessError = teamQuery.error
        ?? tasksQuery.error
        ?? ganttQuery.error
        ?? (includeInbox ? inboxQuery.error : null);
    const queryError = iterationsQuery.error ?? readinessError;
    const isReadinessLoading = (
        hasCurrentIteration
        && (teamQuery.isLoading || tasksQuery.isLoading || ganttQuery.isLoading)
    ) || (includeInbox && inboxQuery.isLoading);
    const isReadinessFetching = (
        hasCurrentIteration
        && (teamQuery.isFetching || tasksQuery.isFetching || ganttQuery.isFetching)
    ) || (includeInbox && inboxQuery.isFetching);

    const refetch = async () => {
        await Promise.all([
            iterationsQuery.refetch(),
            ...(hasCurrentIteration ? [teamQuery.refetch(), tasksQuery.refetch(), ganttQuery.refetch()] : []),
            ...(includeInbox ? [inboxQuery.refetch()] : []),
        ]);
    };

    return {
        selectedIterationId,
        setSelectedIterationId,
        selectIteration: setSelectedIterationId,
        iterations,
        currentIteration,
        hasCurrentIteration,
        teamMembers,
        tasks,
        allTasks,
        gantt: ganttQuery.data,
        inboxItems: inboxQuery.data ?? [],
        readinessData,
        status,
        ready,
        nextId,
        isLoading: iterationsQuery.isLoading || isReadinessLoading,
        isError: Boolean(queryError),
        isIterationsLoading: iterationsQuery.isLoading,
        isIterationsError: Boolean(iterationsQuery.error),
        isIterationsFetching: iterationsQuery.isFetching,
        isReadinessLoading,
        isReadinessError: Boolean(readinessError),
        isReadinessFetching,
        error: queryError,
        refetch,
    };
};

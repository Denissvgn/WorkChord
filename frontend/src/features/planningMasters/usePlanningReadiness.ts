import { useEffect, useMemo } from 'react';
import { useQuery } from '@tanstack/react-query';
import { ganttService } from '../../services/ganttService';
import { iterationService } from '../../services/iterationService';
import { taskService } from '../../services/taskService';
import { teamService } from '../../services/teamService';
import { triageService } from '../../services/triageService';
import { useIterationStore } from '../../store/iterationStore';
import type { GanttResponse } from '../../types/gantt';
import type { Iteration } from '../../types/iteration';
import type { Task } from '../../types/task';
import type { TeamMember } from '../../types/team';
import { deriveStatus, nextStep, readiness } from './masters';
import type { PlanReadiness } from './masters';
import {
    hasPositivePlanningEffort,
    isPlanningLeafTask,
} from './planningTaskIssues';

type PlanningReadinessOptions = {
    includeInbox?: boolean;
    autoSelectFirst?: boolean;
};

const HOURS_PER_DAY = 8;
const ISO_DATE = /^\d{4}-\d{2}-\d{2}$/;
const MILLISECONDS_PER_DAY = 86_400_000;

export type PlanningTeamMember = TeamMember & {
    capacity_hours: number;
    planned_hours: number;
};

export type PlanningQueryFeedback = {
    enabled: boolean;
    hasData: boolean;
    dataUpdatedAt: number;
    isLoading: boolean;
    isFetching: boolean;
    isError: boolean;
    isBlockingError: boolean;
    isRefetchError: boolean;
    error: unknown;
    refetch: () => Promise<unknown>;
};

type QueryFeedbackSource = {
    data: unknown;
    dataUpdatedAt: number;
    error: unknown;
    isLoading: boolean;
    isFetching: boolean;
    isError: boolean;
    refetch: () => Promise<unknown>;
};

const queryFeedback = (
    query: QueryFeedbackSource,
    enabled: boolean,
): PlanningQueryFeedback => {
    const hasData = query.data !== undefined;
    return {
        enabled,
        hasData,
        dataUpdatedAt: query.dataUpdatedAt,
        isLoading: query.isLoading,
        isFetching: query.isFetching,
        isError: query.isError,
        isBlockingError: query.isError && !hasData,
        isRefetchError: query.isError && hasData,
        error: query.error,
        refetch: query.refetch,
    };
};

export const flattenTasks = (list: Task[] = []): Task[] => {
    const out: Task[] = [];
    for (const task of list) {
        out.push(task);
        if (task.children?.length) out.push(...flattenTasks(task.children));
    }
    return out;
};

export const planningLeafTasks = (list: Task[] = []): Task[] => (
    flattenTasks(list).filter(isPlanningLeafTask)
);

const finitePositive = hasPositivePlanningEffort;

const parseIsoDay = (value: string): number | null => {
    if (!ISO_DATE.test(value)) return null;
    const [year, month, day] = value.split('-').map(Number);
    const timestamp = Date.UTC(year, month - 1, day);
    const parsed = new Date(timestamp);
    if (
        parsed.getUTCFullYear() !== year
        || parsed.getUTCMonth() !== month - 1
        || parsed.getUTCDate() !== day
    ) {
        return null;
    }
    return Math.floor(timestamp / MILLISECONDS_PER_DAY);
};

const dayToIso = (epochDay: number) => (
    new Date(epochDay * MILLISECONDS_PER_DAY).toISOString().slice(0, 10)
);

const isStandardWeekend = (epochDay: number) => {
    const weekday = new Date(epochDay * MILLISECONDS_PER_DAY).getUTCDay();
    return weekday === 0 || weekday === 6;
};

const vacationWorkingDays = (
    member: TeamMember,
    iteration: Iteration,
    gantt: GanttResponse | undefined,
) => {
    const iterationStart = parseIsoDay(iteration.start_date);
    const iterationEnd = parseIsoDay(iteration.end_date);
    if (iterationStart === null || iterationEnd === null || iterationStart > iterationEnd) {
        return 0;
    }

    const hasCalendarProjection = gantt !== undefined;
    const nonWorkingDates = new Set([
        ...(gantt?.holidays ?? []),
        ...(gantt?.weekends ?? []),
    ]);
    const vacationDates = new Set<string>();

    for (const vacation of member.vacations) {
        const vacationStart = parseIsoDay(vacation.start_date);
        const vacationEnd = parseIsoDay(vacation.end_date);
        if (vacationStart === null || vacationEnd === null || vacationStart > vacationEnd) {
            continue;
        }

        const start = Math.max(iterationStart, vacationStart);
        const end = Math.min(iterationEnd, vacationEnd);
        for (let day = start; day <= end; day += 1) {
            const isoDay = dayToIso(day);
            const isWorkingDay = hasCalendarProjection
                ? !nonWorkingDates.has(isoDay)
                : !isStandardWeekend(day);
            if (isWorkingDay) vacationDates.add(isoDay);
        }
    }

    return Math.min(
        Math.max(0, iteration.working_days),
        vacationDates.size,
    );
};

const boundedPercentage = (value: number) => (
    Number.isFinite(value) ? Math.min(100, Math.max(0, value)) / 100 : 0
);

const boundedCoefficient = (value: number) => (
    Number.isFinite(value) && value > 0 ? value : 0
);

const roundHours = (value: number) => Math.round(value * 100) / 100;

export const enrichPlanningTeamMembers = ({
    members,
    tasks,
    iteration,
    gantt,
}: {
    members: TeamMember[];
    tasks: Task[];
    iteration: Iteration | null;
    gantt?: GanttResponse;
}): PlanningTeamMember[] => {
    const plannedHoursByMember = new Map<number, number>();
    for (const task of planningLeafTasks(tasks)) {
        if (!task.assignee || !finitePositive(task.effort_days)) continue;
        plannedHoursByMember.set(
            task.assignee.id,
            (plannedHoursByMember.get(task.assignee.id) ?? 0)
                + task.effort_days * HOURS_PER_DAY,
        );
    }

    return members.map(member => {
        if (!iteration) {
            return {
                ...member,
                capacity_hours: 0,
                planned_hours: roundHours(plannedHoursByMember.get(member.id) ?? 0),
            };
        }

        const workingDays = Math.max(0, iteration.working_days);
        const availableDays = Math.max(
            0,
            workingDays - vacationWorkingDays(member, iteration, gantt),
        );
        const capacityHours = availableDays
            * boundedPercentage(member.availability_percent)
            * (1 - boundedPercentage(member.operational_utilization))
            * boundedCoefficient(member.professionalism_coefficient)
            * HOURS_PER_DAY;

        return {
            ...member,
            capacity_hours: roundHours(Math.max(0, capacityHours)),
            planned_hours: roundHours(plannedHoursByMember.get(member.id) ?? 0),
        };
    });
};

const hasSavedDateRange = (task: Task) => {
    if (!task.start_date || !task.end_date) return false;
    const start = parseIsoDay(task.start_date);
    const end = parseIsoDay(task.end_date);
    return start !== null && end !== null && start <= end;
};

export const hasSavedPlanningSchedule = (tasks: Task[]) => {
    const leaves = planningLeafTasks(tasks);
    return leaves.length > 0 && leaves.every(task => (
        finitePositive(task.effort_days) && hasSavedDateRange(task)
    ));
};

export const countPlanningExceptions = (
    tasks: Task[],
    members: PlanningTeamMember[],
) => (
    planningLeafTasks(tasks).filter(task => (
        task.is_overdue
        || task.is_delayed
        || task.is_outside_constraints
    )).length
    + members.filter(member => (
        member.planned_hours > member.capacity_hours
        && member.planned_hours > 0
    )).length
);

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

    const rawTeamMembers = useMemo(() => teamQuery.data ?? [], [teamQuery.data]);
    const tasks = useMemo(() => tasksQuery.data ?? [], [tasksQuery.data]);
    const allTasks = useMemo(() => flattenTasks(tasks), [tasks]);
    const leafTasks = useMemo(() => planningLeafTasks(tasks), [tasks]);

    const teamMembers = useMemo(
        () => enrichPlanningTeamMembers({
            members: rawTeamMembers,
            tasks,
            iteration: currentIteration,
            gantt: ganttQuery.data,
        }),
        [currentIteration, ganttQuery.data, rawTeamMembers, tasks],
    );

    const teamMembersNoCap = useMemo(
        () => teamMembers.filter(member => member.capacity_hours <= 0).length,
        [teamMembers],
    );

    const teamCapacity = useMemo(
        () => roundHours(teamMembers.reduce(
            (total, member) => total + member.capacity_hours,
            0,
        )),
        [teamMembers],
    );
    const planningExceptionCount = useMemo(
        () => countPlanningExceptions(tasks, teamMembers),
        [tasks, teamMembers],
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
        taskCount: leafTasks.length,
        tasksWithoutAssignee: leafTasks.filter(task => !task.assignee).length,
        tasksWithoutEffort: leafTasks.filter(task => !finitePositive(task.effort_days)).length,
        hasGanttSchedule: hasSavedPlanningSchedule(tasks),
        ganttLastBuilt: '',
        riskCount: planningExceptionCount,
        inboxCount: includeInbox ? (inboxQuery.data?.length ?? 0) : 0,
    }), [
        currentIteration,
        hasCurrentIteration,
        inboxQuery.data,
        includeInbox,
        iterations.length,
        leafTasks,
        planningExceptionCount,
        tasks,
        teamCapacity,
        teamMembers.length,
        teamMembersNoCap,
    ]);

    const status = useMemo(() => deriveStatus(readinessData), [readinessData]);
    const ready = useMemo(() => readiness(status), [status]);
    const nextId = useMemo(() => nextStep(status), [status]);

    const queryStates = {
        iterations: queryFeedback(iterationsQuery, true),
        team: queryFeedback(teamQuery, hasCurrentIteration),
        tasks: queryFeedback(tasksQuery, hasCurrentIteration),
        gantt: queryFeedback(ganttQuery, hasCurrentIteration),
        inbox: queryFeedback(inboxQuery, includeInbox),
    };
    const readinessError = [
        queryStates.team,
        queryStates.tasks,
        queryStates.gantt,
        queryStates.inbox,
    ].find(query => query.isBlockingError)?.error ?? null;
    const queryError = queryStates.iterations.isBlockingError
        ? iterationsQuery.error
        : readinessError;
    const isReadinessLoading = (
        hasCurrentIteration
        && (teamQuery.isLoading || tasksQuery.isLoading || ganttQuery.isLoading)
    ) || (includeInbox && inboxQuery.isLoading);
    const isReadinessFetching = (
        hasCurrentIteration
        && (teamQuery.isFetching || tasksQuery.isFetching || ganttQuery.isFetching)
    ) || (includeInbox && inboxQuery.isFetching);

    const refetch = async () => {
        return Promise.allSettled([
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
        planningLeafTasks: leafTasks,
        gantt: ganttQuery.data,
        inboxItems: inboxQuery.data ?? [],
        readinessData,
        status,
        ready,
        nextId,
        isLoading: iterationsQuery.isLoading || isReadinessLoading,
        isError: Boolean(queryError),
        isIterationsLoading: iterationsQuery.isLoading,
        isIterationsError: queryStates.iterations.isBlockingError,
        isIterationsFetching: iterationsQuery.isFetching,
        isReadinessLoading,
        isReadinessError: Boolean(readinessError),
        isReadinessFetching,
        isFetching: iterationsQuery.isFetching || isReadinessFetching,
        queryStates,
        error: queryError,
        refetch,
    };
};

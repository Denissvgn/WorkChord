import type { PlanningStepId } from './planningReturn';
import type { PlanningTaskIssue } from './planningTaskIssues';

// Readiness inputs and the recovery action each checkpoint offers. Checkpoint states come from the server.

// ── Readiness data (from real API) ──────────────────────────────────────────

export interface PlanReadiness {
    iterationCount: number;
    hasCurrentIteration: boolean;
    currentIterationName: string;
    currentIterationStart: string;
    currentIterationEnd: string;
    currentIterationDays: number;
    teamMemberCount: number;
    teamCapacity: number;
    teamMembersNoCap: number;
    taskCount: number;
    tasksWithoutAssignee: number;
    tasksWithoutEffort: number;
    /** Planned leaves an agent is working on that have no capacity row. */
    tasksAgentWithoutCapacity?: number;
    /** Capacity rows whose profile is an agent. */
    teamAgentCount?: number;
    hasGanttSchedule: boolean;
    ganttLastBuilt: string;
    riskCount: number;
    inboxCount: number;
}

type PlanningRecoveryKind =
    | 'create-period'
    | 'add-team'
    | 'repair-capacity'
    | 'add-work'
    | 'repair-assignee'
    | 'repair-effort'
    | 'build-schedule'
    | 'review-plan';

interface PlanningRecoveryAction {
    kind: PlanningRecoveryKind;
    ownerStep: PlanningStepId;
    route: string;
    count?: number;
    planningIssue?: PlanningTaskIssue;
    query?: Record<string, string>;
}

const rankedTaskRecovery = (
    r: PlanReadiness,
): PlanningRecoveryAction | null => {
    const candidates = ([
        {
            kind: 'repair-assignee',
            ownerStep: 'blockers',
            route: '/tasks',
            count: r.tasksWithoutAssignee,
            planningIssue: 'unassigned',
        },
        {
            kind: 'repair-effort',
            ownerStep: 'blockers',
            route: '/tasks',
            count: r.tasksWithoutEffort,
            planningIssue: 'missing-effort',
        },
    ] satisfies PlanningRecoveryAction[]).filter(
        candidate => (candidate.count ?? 0) > 0,
    );

    candidates.sort((left, right) => {
        const countDifference = (right.count ?? 0) - (left.count ?? 0);
        if (countDifference !== 0) return countDifference;
        return left.kind === 'repair-assignee' ? -1 : 1;
    });
    return candidates[0] ?? null;
};

/**
 * Resolve the single workspace action owned by a selected checkpoint.
 *
 * Prerequisites are checked in stage order. Simultaneous task exceptions are
 * ranked by affected-task count, with assignment first on an exact tie.
 */
export const derivePlanningRecovery = (
    selectedStepId: PlanningStepId,
    r: PlanReadiness,
): PlanningRecoveryAction => {
    const createPeriod: PlanningRecoveryAction = {
        kind: 'create-period',
        ownerStep: 'iteration',
        route: '/iterations',
    };
    if (selectedStepId === 'iteration' || !r.hasCurrentIteration) {
        return createPeriod;
    }

    if (selectedStepId === 'team') {
        return r.teamMemberCount === 0
            ? { kind: 'add-team', ownerStep: 'team', route: '/team' }
            : {
                kind: r.teamMembersNoCap > 0 ? 'repair-capacity' : 'add-team',
                ownerStep: 'team',
                route: '/team',
                ...(r.teamMembersNoCap > 0 ? { count: r.teamMembersNoCap } : {}),
            };
    }

    if (selectedStepId === 'work') {
        return {
            kind: 'add-work',
            ownerStep: 'work',
            route: '/tasks',
            ...(r.taskCount === 0 ? { query: { create: '1' } } : {}),
        };
    }

    if (selectedStepId === 'blockers') {
        if (r.taskCount === 0) {
            return {
                kind: 'add-work',
                ownerStep: 'work',
                route: '/tasks',
                query: { create: '1' },
            };
        }
        const taskRecovery = rankedTaskRecovery(r);
        // Only agent-held work is left: one action adds the capacity rows.
        if (!taskRecovery && (r.tasksAgentWithoutCapacity ?? 0) > 0) {
            return { kind: 'repair-capacity', ownerStep: 'team', route: '/team', count: r.tasksAgentWithoutCapacity };
        }
        // Assigning needs people on the iteration: send the user to step 2 first.
        if (taskRecovery?.kind === 'repair-assignee' && r.teamMemberCount === 0) {
            return { kind: 'add-team', ownerStep: 'team', route: '/team' };
        }
        return taskRecovery ?? {
            kind: 'add-work',
            ownerStep: 'blockers',
            route: '/tasks',
        };
    }

    if (r.teamMemberCount === 0) {
        return { kind: 'add-team', ownerStep: 'team', route: '/team' };
    }
    if (r.teamMembersNoCap > 0) {
        return {
            kind: 'repair-capacity',
            ownerStep: 'team',
            route: '/team',
            count: r.teamMembersNoCap,
        };
    }
    if (r.taskCount === 0) {
        return {
            kind: 'add-work',
            ownerStep: 'work',
            route: '/tasks',
            query: { create: '1' },
        };
    }

    const taskRecovery = rankedTaskRecovery(r);
    if (taskRecovery) return taskRecovery;

    if (!r.hasGanttSchedule || selectedStepId === 'schedule') {
        return {
            kind: 'build-schedule',
            ownerStep: 'schedule',
            route: '/gantt',
        };
    }
    return {
        kind: 'review-plan',
        ownerStep: 'review',
        route: '/gantt',
    };
};

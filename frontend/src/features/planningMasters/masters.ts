import { PLANNING_STEP_IDS } from './planningReturn';
import type { PlanningStepId } from './planningReturn';
import type { PlanningTaskIssue } from './planningTaskIssues';

// Readiness inputs and the wording of each checkpoint's status.

type StepState = 'done' | 'warn' | 'blocked' | 'todo';

interface StepStatus {
    state: StepState;
    summary?: string;
    missing?: string[];
}

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
    /** Server-owned checkpoint states; when present they decide each step's state. */
    checkpointStates?: Partial<Record<PlanningStepId, StepState>>;
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

// ── Status derivation (mirrors design's deriveStatus) ───────────────────────

export function deriveStatus(r: PlanReadiness): Record<string, StepStatus> {
    const out: Record<string, StepStatus> = {};

    // iteration
    out.iteration = !r.hasCurrentIteration
        ? {
            state: 'todo',
            missing: ['No planning period selected'],
          }
        : {
            state: 'done',
            summary: `${r.currentIterationName} · ${r.currentIterationStart}–${r.currentIterationEnd}`,
          };

    // team
    out.team = r.teamMemberCount === 0
        ? { state: out.iteration.state === 'done' ? 'todo' : 'blocked', missing: ['No people on this iteration'] }
        : r.teamMembersNoCap > 0
            ? { state: 'warn', missing: [`${r.teamMembersNoCap} person without allocation`] }
            : { state: 'done', summary: `${r.teamMemberCount} people · ${r.teamCapacity}h cap` };

    // work
    out.work = r.taskCount === 0
        ? { state: out.iteration.state === 'done' ? 'todo' : 'blocked', missing: ['No tasks for this iteration'] }
        : { state: 'done', summary: `${r.taskCount} tasks added` };

    // blockers
    const blockerDetails = [
        r.tasksWithoutAssignee > 0 ? `${r.tasksWithoutAssignee} unassigned` : null,
        r.tasksWithoutEffort > 0 ? `${r.tasksWithoutEffort} missing effort` : null,
        (r.tasksAgentWithoutCapacity ?? 0) > 0 ? `${r.tasksAgentWithoutCapacity} agent working, no capacity row` : null,
    ].filter(Boolean) as string[];
    out.blockers = r.taskCount === 0
        ? { state: 'blocked', missing: ['Add work first'] }
        : blockerDetails.length > 0
            ? { state: 'warn', missing: blockerDetails }
            : { state: 'done', summary: 'No blockers' };

    // schedule
    const canBuild = [
        out.iteration,
        out.team,
        out.work,
        out.blockers,
    ].every(step => step.state === 'done');
    out.schedule = !canBuild
        ? { state: 'blocked', missing: ['Complete earlier steps first'] }
        : !r.hasGanttSchedule
            ? { state: 'todo', missing: ['Schedule not built'] }
            : { state: 'done', summary: r.ganttLastBuilt ? `Built ${r.ganttLastBuilt}` : 'Schedule built' };

    // review
    out.review = out.schedule.state !== 'done'
        ? { state: 'blocked', missing: ['Build the schedule first'] }
        : r.riskCount > 0
            ? { state: 'warn', missing: [`${r.riskCount} risk${r.riskCount === 1 ? '' : 's'} to acknowledge`] }
            : { state: 'done', summary: 'Plan ready to share' };

    // People and the PM agent read the same server checkpoints, so the server's
    // state wins; the local inputs above only supply the wording.
    for (const [id, state] of Object.entries(r.checkpointStates ?? {})) {
        if (state && out[id] && out[id].state !== state) out[id] = { ...out[id], state };
    }
    return out;
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

export function nextStep(status: Record<string, StepStatus>): string {
    for (const id of PLANNING_STEP_IDS) {
        if (status[id].state !== 'done') return id;
    }
    return 'review';
}

export function readiness(status: Record<string, StepStatus>): { done: number; total: number; pct: number } {
    const total = PLANNING_STEP_IDS.length;
    const done = PLANNING_STEP_IDS.filter(id => status[id].state === 'done').length;
    return { done, total, pct: Math.round((done / total) * 100) };
}

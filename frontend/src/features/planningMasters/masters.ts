import type { PlanningStepId } from './planningReturn';
import type { PlanningTaskIssue } from './planningTaskIssues';

// Step definitions and status derivation — mirrors the design's data.jsx model

export type StepState = 'done' | 'warn' | 'blocked' | 'todo';

export interface StepStatus {
    state: StepState;
    summary?: string;
    missing?: string[];
}

export interface MasterStepDef {
    id: string;
    title: string;
    desc: string;
    why: string;
    primary: string;
    secondary: string;
    expert: string;
    route: string;
    secondaryRoute?: string;
}

export const STEP_DEFS: MasterStepDef[] = [
    {
        id: 'iteration',
        title: 'Create planning period',
        desc: 'Pick the dates you\'re planning for. We\'ll use these as the boundary for capacity and scheduling.',
        why: 'Without dates, we can\'t compute people-days, surface deadlines, or build a schedule.',
        primary: 'New planning period',
        secondary: 'Use existing iteration',
        expert: 'Open Iterations',
        route: '/iterations',
    },
    {
        id: 'team',
        title: 'Add people and capacity',
        desc: 'Bring in the people who\'ll do this work, and set their allocation for the period.',
        why: 'Capacity is what makes a plan realistic. Skip this and you\'ll over-commit.',
        primary: 'Add people',
        secondary: 'Import from last iteration',
        expert: 'Open Team',
        route: '/team',
    },
    {
        id: 'work',
        title: 'Add work',
        desc: 'Bring in tasks for this iteration — from intake, the backlog, or by drafting new ones.',
        why: 'Every task needs an owner, an effort estimate, and a project so it can be scheduled.',
        primary: 'Add tasks',
        secondary: 'Pull from intake',
        expert: 'Open Tasks',
        route: '/tasks',
        secondaryRoute: '/triage',
    },
    {
        id: 'blockers',
        title: 'Resolve scheduling blockers',
        desc: 'Clean up tasks that can\'t be scheduled yet — missing owner, missing effort, or unresolved dependencies.',
        why: 'The scheduler skips work it can\'t place. Fix these before building, or they\'ll spill to next period.',
        primary: 'Review blockers',
        secondary: 'Move to next period',
        expert: 'Open Tasks → blocked',
        route: '/tasks',
    },
    {
        id: 'schedule',
        title: 'Build schedule',
        desc: 'Place every ready task on the calendar. Try changes before committing — nothing moves until you apply.',
        why: 'This is where the plan becomes real. You can re-build any time as new info arrives.',
        primary: 'Build schedule',
        secondary: 'Try changes (sandbox)',
        expert: 'Open Schedule',
        route: '/gantt',
    },
    {
        id: 'review',
        title: 'Review plan',
        desc: 'Walk the plan with your team — load by person, risks, deadlines, and a one-page summary to share.',
        why: 'Catch issues before the iteration starts. Sharing the plan creates buy-in and surfaces gaps.',
        primary: 'Open review',
        secondary: 'Export summary',
        expert: 'Open Schedule → Review',
        route: '/gantt',
        secondaryRoute: '/gantt',
    },
];

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
    hasGanttSchedule: boolean;
    ganttLastBuilt: string;
    riskCount: number;
    inboxCount: number;
}

export type PlanningRecoveryKind =
    | 'create-period'
    | 'add-team'
    | 'repair-capacity'
    | 'add-work'
    | 'repair-assignee'
    | 'repair-effort'
    | 'build-schedule'
    | 'review-plan';

export interface PlanningRecoveryAction {
    kind: PlanningRecoveryKind;
    ownerStep: PlanningStepId;
    route: string;
    count?: number;
    planningIssue?: PlanningTaskIssue;
    query?: Record<string, string>;
}

export const EMPTY_READINESS: PlanReadiness = {
    iterationCount: 0, hasCurrentIteration: false,
    currentIterationName: '', currentIterationStart: '', currentIterationEnd: '',
    currentIterationDays: 0,
    teamMemberCount: 0, teamCapacity: 0, teamMembersNoCap: 0,
    taskCount: 0, tasksWithoutAssignee: 0, tasksWithoutEffort: 0,
    hasGanttSchedule: false, ganttLastBuilt: '', riskCount: 0, inboxCount: 0,
};

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
        return rankedTaskRecovery(r) ?? {
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
    const order = STEP_DEFS.map(s => s.id);
    for (const id of order) {
        if (status[id].state !== 'done') return id;
    }
    return 'review';
}

export function readiness(status: Record<string, StepStatus>): { done: number; total: number; pct: number } {
    const total = STEP_DEFS.length;
    const done = STEP_DEFS.filter(s => status[s.id].state === 'done').length;
    return { done, total, pct: Math.round((done / total) * 100) };
}

type Translate = (key: string, options?: Record<string, unknown>) => string;

/** Translate readiness summaries without storing display prose in domain state. */
export function localizeStatus(
    status: Record<string, StepStatus>,
    r: PlanReadiness,
    translate: Translate,
): Record<string, StepStatus> {
    const result: Record<string, StepStatus> = {};
    for (const definition of STEP_DEFS) {
        const current = status[definition.id];
        let summary: string | undefined;
        let missing: string[] | undefined;

        if (definition.id === 'iteration') {
            summary = current.state === 'done'
                ? translate('plan.status.periodReady', {
                    name: r.currentIterationName,
                    start: r.currentIterationStart,
                    end: r.currentIterationEnd,
                })
                : undefined;
            missing = current.state === 'done' ? undefined : [translate('plan.status.noPeriod')];
        } else if (definition.id === 'team') {
            summary = current.state === 'done'
                ? translate('plan.status.teamReady', { count: r.teamMemberCount, capacity: r.teamCapacity })
                : undefined;
            missing = current.state === 'done'
                ? undefined
                : [r.teamMembersNoCap > 0
                    ? translate('plan.status.peopleWithoutAllocation', { count: r.teamMembersNoCap })
                    : translate('plan.status.noPeople')];
        } else if (definition.id === 'work') {
            summary = current.state === 'done'
                ? translate('plan.status.workReady', { count: r.taskCount })
                : undefined;
            missing = current.state === 'done'
                ? undefined
                : [translate('plan.status.noTasks')];
        } else if (definition.id === 'blockers') {
            summary = current.state === 'done' ? translate('plan.status.noBlockers') : undefined;
            missing = current.state === 'done'
                ? undefined
                : r.taskCount === 0
                    ? [translate('plan.status.addWorkFirst')]
                    : [
                        ...(r.tasksWithoutAssignee > 0
                            ? [translate('plan.status.unassignedTasks', {
                                count: r.tasksWithoutAssignee,
                            })]
                            : []),
                        ...(r.tasksWithoutEffort > 0
                            ? [translate('plan.status.tasksWithoutEffort', {
                                count: r.tasksWithoutEffort,
                            })]
                            : []),
                    ];
        } else if (definition.id === 'schedule') {
            summary = current.state === 'done' ? translate('plan.status.scheduleBuilt') : undefined;
            missing = current.state === 'done'
                ? undefined
                : [current.state === 'blocked'
                    ? translate('plan.status.completeEarlierSteps')
                    : translate('plan.status.scheduleNotBuilt')];
        } else {
            summary = current.state === 'done' ? translate('plan.status.planReady') : undefined;
            missing = current.state === 'done'
                ? undefined
                : [current.state === 'blocked'
                    ? translate('plan.status.buildScheduleFirst')
                    : translate('plan.status.risksToAcknowledge', { count: r.riskCount })];
        }

        result[definition.id] = { state: current.state, summary, missing };
    }
    return result;
}

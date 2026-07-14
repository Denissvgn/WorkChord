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
        route: '/',
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
        : (r.tasksWithoutAssignee > 0 || r.tasksWithoutEffort > 0)
            ? {
                state: 'warn',
                missing: [
                    r.tasksWithoutAssignee > 0 ? `${r.tasksWithoutAssignee} unassigned` : null,
                    r.tasksWithoutEffort > 0   ? `${r.tasksWithoutEffort} missing effort` : null,
                ].filter(Boolean) as string[],
              }
            : { state: 'done', summary: `${r.taskCount} tasks · all ready` };

    // blockers
    const blockerCount = (r.tasksWithoutAssignee > 0 ? 1 : 0) + (r.tasksWithoutEffort > 0 ? 1 : 0);
    out.blockers = r.taskCount === 0
        ? { state: 'blocked', missing: ['Add work first'] }
        : blockerCount > 0
            ? { state: 'warn', missing: [`${blockerCount} blocker${blockerCount === 1 ? '' : 's'} to clear`] }
            : { state: 'done', summary: 'No blockers' };

    // schedule
    const canBuild = out.iteration.state === 'done'
        && out.team.state !== 'blocked' && out.work.state !== 'blocked';
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

export function nextStep(status: Record<string, StepStatus>): string {
    const order = STEP_DEFS.map(s => s.id);
    for (const id of order) {
        if (status[id].state === 'todo' || status[id].state === 'warn') return id;
    }
    for (const id of order) {
        if (status[id].state === 'blocked') return id;
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
            missing = current.state === 'done' ? undefined : [
                ...(r.taskCount === 0 ? [translate('plan.status.noTasks')] : []),
                ...(r.tasksWithoutAssignee > 0
                    ? [translate('plan.status.unassignedTasks', { count: r.tasksWithoutAssignee })]
                    : []),
                ...(r.tasksWithoutEffort > 0
                    ? [translate('plan.status.tasksWithoutEffort', { count: r.tasksWithoutEffort })]
                    : []),
            ];
        } else if (definition.id === 'blockers') {
            const blockerCount = (r.tasksWithoutAssignee > 0 ? 1 : 0) + (r.tasksWithoutEffort > 0 ? 1 : 0);
            summary = current.state === 'done' ? translate('plan.status.noBlockers') : undefined;
            missing = current.state === 'done'
                ? undefined
                : [r.taskCount === 0
                    ? translate('plan.status.addWorkFirst')
                    : translate('plan.status.blockersToClear', { count: blockerCount })];
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

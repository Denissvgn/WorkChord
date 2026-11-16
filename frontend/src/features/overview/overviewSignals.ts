import type { TaskFilters } from '../../components/tasks/TaskFiltersBar';
import type { AgentPipeline } from '../../types/agent';
import type { Iteration } from '../../types/iteration';
import type { Task } from '../../types/task';
import { defaultFilters } from '../../utils/taskFilterDefaults';
import { selectVisibleWork } from '../../utils/visibleWork';
import { writeFiltersToSearchParams } from '../savedViews/taskViewParams';
import type { ScopeIteration, ScopeProject } from '../scope/workScope';

/**
 * The task lists Overview counts. Each count is a link to its list in Tasks, and each
 * count is taken with the list's own filter, so the list always holds that many tasks.
 */
export const OVERVIEW_TASK_LISTS = {
    total: {},
    done: { status: 'closed' },
    atRisk: { planningIssue: 'at-risk' },
    blocked: { isBlocked: true },
    toAssign: { planningIssue: 'unassigned' },
} as const satisfies Record<string, Partial<TaskFilters>>;

export type OverviewTaskList = keyof typeof OVERVIEW_TASK_LISTS;

export const overviewListFilters = (list: OverviewTaskList): TaskFilters => ({
    ...defaultFilters,
    ...OVERVIEW_TASK_LISTS[list],
});

/** The tasks the Tasks list shows for this list: the leaves of the filtered tree. */
export const listTasks = (roots: Task[], list: OverviewTaskList) => (
    selectVisibleWork(roots, overviewListFilters(list)).leaves
);

/** The Tasks link that shows `list`; `extra` adds parameters such as a selection mode. */
export const taskListHref = (list: OverviewTaskList, extra: Record<string, string> = {}) => {
    const params = writeFiltersToSearchParams(new URLSearchParams(), overviewListFilters(list));
    Object.entries(extra).forEach(([key, value]) => params.set(key, value));
    const search = params.toString();
    return search ? `/tasks?${search}` : '/tasks';
};

/** The stages of the agent pipeline, in the order a task moves through them. */
export const PIPELINE_STAGES = [
    'needs_definition',
    'ready_to_assign',
    'assigned_waiting',
    'start_ready',
    'executing',
    'verification_required',
    'recovery_required',
] as const satisfies ReadonlyArray<keyof AgentPipeline>;

export type PipelineStage = typeof PIPELINE_STAGES[number];

/** The Tasks link that opens the pipeline view on one stage. */
export const pipelineStageHref = (stage: PipelineStage) => (
    `/tasks?${new URLSearchParams({ layout: 'pipeline', stage }).toString()}`
);

/** The pipeline tasks that belong to one scope, by the rule the pipeline view applies. */
export const pipelineTasksInScope = (
    tasks: Task[],
    project: ScopeProject | undefined,
    iteration: ScopeIteration | undefined,
) => tasks.filter(task => (
    (project === undefined || project === 'all' || task.project_id === project)
    && (iteration === undefined || (iteration === 'backlog' ? task.iteration_id === null : task.iteration_id === iteration))
));

const DONE_STATUSES = new Set(['resolved', 'closed']);

/** True when today falls within the iteration's dates. */
export const isOpenIteration = (iteration: Pick<Iteration, 'start_date' | 'end_date'>, today: string) => (
    iteration.start_date.slice(0, 10) <= today && today <= iteration.end_date.slice(0, 10)
);

/**
 * The iterations Overview counts: the one in scope, or with All projects every
 * iteration that is open today, earliest first.
 */
export const iterationsInView = (
    iterations: Iteration[],
    project: ScopeProject | undefined,
    iteration: ScopeIteration | undefined,
    today: string,
): Iteration[] => {
    if (project === 'all') {
        return iterations
            .filter(item => isOpenIteration(item, today))
            .sort((left, right) => left.start_date.localeCompare(right.start_date) || left.id - right.id);
    }
    if (typeof iteration !== 'number') return [];
    return iterations.filter(item => item.id === iteration);
};

const MS_PER_DAY = 86_400_000;

const parseDay = (value: string) => {
    const timestamp = Date.parse(`${value.slice(0, 10)}T00:00:00Z`);
    return Number.isNaN(timestamp) ? null : timestamp;
};

/** Working days left in the iteration after today, spread evenly over its calendar days. */
export const workingDaysLeft = (iteration: Iteration, today: string) => {
    const workingDays = Math.max(0, iteration.working_days || 0);
    const start = parseDay(iteration.start_date);
    const end = parseDay(iteration.end_date);
    const now = parseDay(today);
    if (start === null || end === null || now === null || end < start) return workingDays;
    if (now < start) return workingDays;
    if (now > end) return 0;
    const calendarDays = Math.round((end - start) / MS_PER_DAY) + 1;
    const elapsed = Math.round((now - start) / MS_PER_DAY) + 1;
    const dayNo = Math.min(workingDays, Math.max(1, Math.ceil((elapsed / calendarDays) * workingDays)));
    return Math.max(0, workingDays - dayNo);
};

export type DeliveryRisk = 'overdue' | 'late-start' | 'outside-limits' | 'blocked' | null;

/** Why an open task threatens delivery, most severe reason first. */
export const deliveryRisk = (task: Task): DeliveryRisk => {
    if (task.is_overdue) return 'overdue';
    if (task.is_delayed) return 'late-start';
    if (task.is_outside_constraints) return 'outside-limits';
    if (task.blocked_reason?.trim()) return 'blocked';
    return null;
};

const RISK_RANK: Record<Exclude<DeliveryRisk, null>, number> = {
    overdue: 0,
    'late-start': 1,
    'outside-limits': 2,
    blocked: 3,
};

const workNowRank = (task: Task) => {
    const risk = deliveryRisk(task);
    if (risk) return RISK_RANK[risk];
    return task.status === 'active' ? 4 : 5;
};

const dueTime = (task: Task) => (task.end_date ? parseDay(task.end_date) ?? Number.POSITIVE_INFINITY : Number.POSITIVE_INFINITY);

/** The next open tasks to work on, highest delivery risk first, then by due date and priority. */
export const selectWorkNow = (roots: Task[], limit = 5) => {
    const open = selectVisibleWork(roots).leaves.filter(task => !DONE_STATUSES.has(task.status) && !task.is_deferred);
    const ranked = [...open].sort((left, right) => (
        workNowRank(left) - workNowRank(right)
        || dueTime(left) - dueTime(right)
        || left.priority - right.priority
        || left.id - right.id
    ));
    return { tasks: ranked.slice(0, limit), openCount: open.length };
};

/** Severity order of the attention item: the first kind with work wins. */
export const ATTENTION_KINDS = ['blocked', 'reviews', 'to-assign', 'plan'] as const;
export type AttentionKind = typeof ATTENTION_KINDS[number];

export interface AttentionCandidate {
    kind: AttentionKind;
    count: number;
    /** The iteration the item is about; with several open iterations each has its own item. */
    iteration: Iteration | null;
}

/** The most severe candidate: kinds in severity order, then the larger count, then the earlier iteration. */
export const pickAttention = (candidates: AttentionCandidate[]): AttentionCandidate | null => {
    const rank = (kind: AttentionKind) => ATTENTION_KINDS.indexOf(kind);
    const sorted = candidates
        .filter(candidate => candidate.count > 0)
        .sort((left, right) => (
            rank(left.kind) - rank(right.kind)
            || right.count - left.count
            || (left.iteration?.start_date ?? '').localeCompare(right.iteration?.start_date ?? '')
            || (left.iteration?.id ?? 0) - (right.iteration?.id ?? 0)
        ));
    return sorted[0] ?? null;
};

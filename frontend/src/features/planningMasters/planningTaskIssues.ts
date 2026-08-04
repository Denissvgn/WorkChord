import type { Task } from '../../types/task';
import {
    withPlanMasterReturn,
} from './planningReturn';
import type { PlanningStepId } from './planningReturn';

export const PLANNING_TASK_ISSUE_PARAM = 'planningIssue';
export const PLANNING_ITERATION_PARAM = 'iterationId';

export const PLANNING_TASK_ISSUES = [
    'unassigned',
    'missing-effort',
    'any',
] as const;

export type PlanningTaskIssue = typeof PLANNING_TASK_ISSUES[number];

export const parsePlanningTaskIssue = (
    value: unknown,
): PlanningTaskIssue | null => (
    typeof value === 'string'
    && PLANNING_TASK_ISSUES.includes(value as PlanningTaskIssue)
        ? value as PlanningTaskIssue
        : null
);

export const parsePlanningIterationId = (value: unknown): number | null => {
    if (typeof value !== 'string' || !/^[1-9]\d*$/.test(value)) return null;
    const parsed = Number(value);
    return Number.isSafeInteger(parsed) ? parsed : null;
};

export const isPlanningLeafTask = (task: Task) => (
    !task.is_deferred
    && !task.is_composite
    && !task.children?.length
);

export const hasPositivePlanningEffort = (value: number) => (
    Number.isFinite(value) && value > 0
);

export const taskMatchesPlanningIssue = (
    task: Task,
    issue: PlanningTaskIssue,
) => {
    if (!isPlanningLeafTask(task)) return false;
    const isUnassigned = !task.assignee;
    const isMissingEffort = !hasPositivePlanningEffort(task.effort_days);

    if (issue === 'unassigned') return isUnassigned;
    if (issue === 'missing-effort') return isMissingEffort;
    return isUnassigned || isMissingEffort;
};

export const planningIssueTasksHref = ({
    issue,
    iterationId,
    returnStepId,
}: {
    issue: PlanningTaskIssue;
    iterationId: number;
    returnStepId: PlanningStepId;
}) => withPlanMasterReturn('/tasks', returnStepId, {
    panel: 'filters',
    [PLANNING_TASK_ISSUE_PARAM]: issue,
    ...(iterationId > 0
        ? { [PLANNING_ITERATION_PARAM]: String(iterationId) }
        : {}),
});

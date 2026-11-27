import type { TFunction } from 'i18next';
import type { RoutingCheck, RoutingIssue, RoutingReviewer, RoutingRung, TaskBulkOperationResult, TaskRouting } from '../types/task';
import { normalizeApiError } from './apiError';

export const ROUTING_INCONSISTENT = 'routing_inconsistent';

/** The issues the project's review policy treats as blocking. */
export const routingConflicts = (check: RoutingCheck) => check.issues.filter(issue => issue.severity === 'conflict');

/** True when saving the change would leave the task with a routing the project policy does not allow. */
export const routingNeedsResolution = (check: RoutingCheck | null | undefined): check is RoutingCheck => (
    Boolean(check) && check!.structured && !check!.consistent
);

/** The reviewer a check proposes: the dedicated field first, then the suggestion's own reviewer. */
export const suggestedReviewerOf = (check: RoutingCheck): RoutingReviewer | null => (
    check.suggested_reviewer ?? check.suggestion?.reviewer ?? null
);

/** The routing check the server returns with a refused change (409 `routing_inconsistent`), or null for any other error. */
export const routingCheckFromError = (error: unknown): RoutingCheck | null => {
    const normalized = normalizeApiError(error, '');
    if (normalized.status !== 409 || normalized.code !== ROUTING_INCONSISTENT) return null;
    const details = normalized.details;
    if (!details || typeof details !== 'object') return null;
    const check = (details as { routing_check?: unknown }).routing_check;
    return check && typeof check === 'object' ? check as RoutingCheck : null;
};

/** Bulk results whose reassignment needs a decision about the routing, whether refused or only warned. */
export const resultsNeedingRouting = (results: TaskBulkOperationResult[]) => (
    results.filter(result => routingNeedsResolution(result.routing_check))
);

/** A model catalog entry as people read it: its key, effort and publisher. */
export const rungLabel = (t: TFunction, rung: RoutingRung | RoutingReviewer) => {
    const label = rung.effort && rung.effort !== 'unknown' ? t('taskReassign.withEffort', { key: rung.catalog_key, effort: rung.effort }) : rung.catalog_key;
    return rung.publisher_key ? t('taskReassign.withPublisher', { label, publisher: rung.publisher_key }) : label;
};

/** What saving a suggested routing changes, one line per part that differs, for people to read before they accept it. */
export const routingChangeLines = (t: TFunction, before: TaskRouting | null | undefined, after: TaskRouting | null | undefined) => {
    if (!after) return [];
    const none = t('common.none');
    const rung = (value: RoutingRung | null | undefined) => (value ? rungLabel(t, value) : none);
    const ladder = (value: TaskRouting | null | undefined) => (value?.escalation.length ? value.escalation.map(item => rungLabel(t, item)).join(', ') : none);
    const lines: string[] = [];
    if (before?.first_rung?.catalog_key !== after.first_rung?.catalog_key) lines.push(t('taskReassign.changeFirstRung', { before: rung(before?.first_rung), after: rung(after.first_rung) }));
    if (ladder(before) !== ladder(after)) lines.push(t('taskReassign.changeEscalation', { before: ladder(before), after: ladder(after) }));
    if (before?.reviewer?.catalog_key !== after.reviewer?.catalog_key) lines.push(t('taskReassign.changeReviewer', { before: rung(before?.reviewer), after: rung(after.reviewer) }));
    return lines;
};

/** The model keys a routing names, to tell whether two routings send the work the same way. */
export const routingShape = (routing: TaskRouting | null | undefined) => JSON.stringify([
    routing?.first_rung?.catalog_key ?? null, routing?.escalation.map(item => item.catalog_key) ?? [], routing?.reviewer?.catalog_key ?? null,
]);

/** One task of a bulk reassignment whose routing the suggestion would rewrite, or that has no suggestion. */
export interface RoutingChangeItem {
    taskId: number;
    issues: RoutingIssue[];
    before: TaskRouting | null;
    after: TaskRouting | null;
}

const changedRouting = (result: TaskBulkOperationResult) => {
    const change = result.changes?.routing as { old?: TaskRouting | null; new?: TaskRouting | null } | undefined;
    return change?.new ? change : null;
};

/**
 * The tasks a "use the suggested routing" confirmation would touch: every task whose dry run with the
 * suggestion rewrites its routing, plus the tasks that conflict and have no suggestion to apply.
 */
export const routingChangeItems = (needing: TaskBulkOperationResult[], applied: TaskBulkOperationResult[]): RoutingChangeItem[] => {
    const items = new Map<number, RoutingChangeItem>();
    for (const result of needing) {
        const check = result.routing_check!;
        items.set(result.task_id, { taskId: result.task_id, issues: check.issues, before: check.routing ?? null, after: null });
    }
    for (const result of applied) {
        const change = changedRouting(result);
        if (!change) continue;
        const known = items.get(result.task_id);
        items.set(result.task_id, { taskId: result.task_id, issues: known?.issues ?? [], before: change.old ?? known?.before ?? null, after: change.new! });
    }
    return [...items.values()];
};

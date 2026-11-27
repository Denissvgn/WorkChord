import type { TFunction } from 'i18next';
import type { RoutingCheck, RoutingReviewer, RoutingRung, TaskBulkOperationResult } from '../types/task';
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

import type { Task } from '../../types/task';

export type AttentionSeverity = 'critical' | 'warning' | 'advisory';

export type AttentionKind =
    | 'overdue'
    | 'project-risk'
    | 'pace'
    | 'project-update'
    | 'unassigned'
    | 'intake';

export type RankableAttention = {
    id: string;
    kind: AttentionKind;
    severity: AttentionSeverity;
    urgency: number;
    magnitude: number;
};

const severityRank: Record<AttentionSeverity, number> = {
    critical: 3,
    warning: 2,
    advisory: 1,
};

const kindTieBreaker: Record<AttentionKind, number> = {
    overdue: 0,
    'project-risk': 1,
    pace: 2,
    'project-update': 3,
    unassigned: 4,
    intake: 5,
};

const compareStableKeys = (left: string, right: string) => {
    if (left < right) return -1;
    if (left > right) return 1;
    return 0;
};

export const compareAttentionRank = (
    left: RankableAttention,
    right: RankableAttention,
) => (
    severityRank[right.severity] - severityRank[left.severity]
    || right.urgency - left.urgency
    || kindTieBreaker[left.kind] - kindTieBreaker[right.kind]
    || right.magnitude - left.magnitude
    || compareStableKeys(left.id, right.id)
);

export const rankAttentionItems = <Item extends RankableAttention>(
    items: readonly Item[],
) => [...items].sort(compareAttentionRank);

const taskDueTime = (task: Task) => {
    if (!task.end_date) return Number.POSITIVE_INFINITY;
    const timestamp = Date.parse(`${task.end_date}T00:00:00`);
    return Number.isNaN(timestamp) ? Number.POSITIVE_INFINITY : timestamp;
};

const taskStatusRank = (task: Task) => (
    task.status === 'active' ? 0 : 1
);

export const rankAttentionTaskCandidates = (
    tasks: readonly Task[],
) => [...tasks].sort((left, right) => (
    Number(right.is_overdue) - Number(left.is_overdue)
    || taskStatusRank(left) - taskStatusRank(right)
    || taskDueTime(left) - taskDueTime(right)
    || left.priority - right.priority
    || left.sort_order - right.sort_order
    || left.id - right.id
));

import type { TaskStatus } from './task';

export type GitHubAutomationEventType =
    | 'github_pr_opened'
    | 'github_pr_reopened'
    | 'github_pr_ready_for_review'
    | 'github_pr_synchronize'
    | 'github_pr_closed'
    | 'github_pr_merged';

export type GitHubAutomationTargetStatus = Exclude<TaskStatus, 'planned'>;
export type GitHubAutomationOutcome = 'applied' | 'skipped' | 'failed';

export interface GitHubStatusAutomationRule {
    id: number;
    name: string;
    description?: string | null;
    enabled: boolean;
    github_event_type: GitHubAutomationEventType;
    from_status?: TaskStatus | null;
    target_status: GitHubAutomationTargetStatus;
    reason_template?: string | null;
    sort_order: number;
    created_at: string;
    updated_at: string;
}

export interface GitHubStatusAutomationRuleCreate {
    name: string;
    description?: string | null;
    enabled: boolean;
    github_event_type: GitHubAutomationEventType;
    from_status?: TaskStatus | null;
    target_status: GitHubAutomationTargetStatus;
    reason_template?: string | null;
    sort_order: number;
}

export type GitHubStatusAutomationRuleUpdate = Partial<GitHubStatusAutomationRuleCreate>;

export interface GitHubStatusAutomationResult {
    rule_id: number;
    outcome: GitHubAutomationOutcome;
    from_status: string;
    target_status: string;
    reason?: string | null;
    error?: string | null;
}

export interface GitHubPullSubmission {
    run_id: number;
    commit_sha: string;
    commit_url?: string | null;
    pr_url?: string | null;
    submitted_at?: string | null;
    reviews: { assignment_id: number; actor_id?: number | null; state: string }[];
}

export interface GitHubPullReconciliation {
    link_id: number;
    url?: string | null;
    title?: string | null;
    /** unobserved, open, draft, merged or closed_unmerged. */
    state: string;
    submitted_sha?: string | null;
    submissions: GitHubPullSubmission[];
    observed_head_sha?: string | null;
    target_branch?: string | null;
    checks: { state?: string | null; total?: number | null; sha?: string | null; error?: string | null };
    merged: boolean;
    merge_commit_sha?: string | null;
    merged_at?: string | null;
    closed_at?: string | null;
    observed_at?: string | null;
    observation_source?: string | null;
    observation_error?: string | null;
    review: { accepted: boolean; state: string };
    differences: string[];
    next_owner: string;
    next_action: string;
}

export interface GitHubReconciliation {
    task_id: number;
    task_status: string;
    accepted: boolean;
    replacement?: { role: 'original' | 'replacement'; original_task_id: number; replacement_task_id: number } | null;
    successor?: { task_id: number; status: string; pull_requests: GitHubPullReconciliation[] } | null;
    pull_requests: GitHubPullReconciliation[];
}

export interface DeliveryPrerequisiteHold {
    case: string;
    reason: string;
    next_owner: string;
    next_action: string;
}

export interface DeliveryPrerequisite {
    id: number;
    kind: 'task' | 'milestone';
    target_id?: number;
    title?: string;
    ready: boolean;
    reason: string | null;
    target_branch?: string | null;
    merge?: { state: string; verified: boolean; target_branch: string } | null;
    hold?: DeliveryPrerequisiteHold | null;
}

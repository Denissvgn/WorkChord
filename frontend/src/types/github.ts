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

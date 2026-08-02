import i18n from '../../i18n/i18n';
import { useState, type FormEvent } from 'react';
import { useTranslation } from 'react-i18next';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { Bot, CircleDot, GitBranch, History, Link as LinkIcon, Plus, RefreshCw, Trash2, X } from 'lucide-react';
import { taskService } from '../../services/taskService';
import type { ExternalLink, Task } from '../../types/task';
import { getApiErrorMessage } from '../../utils/apiError';
import { QueryErrorState } from '../feedback/QueryState';
import { safeExternalHref } from '../../utils/safeUrl';
import clsx from 'clsx';
import { RequestSourceLinksPanel } from '../requestSources/RequestSourceLinksPanel';
import { formatDateTime } from '../../utils/formatDate';

const t = i18n.t.bind(i18n);

interface TaskTimelinePanelProps {
    task: Task;
}

const itemLabels: Record<string, string> = {
    task_created: 'surfaces.taskTimeline.events.taskCreated',
    task_updated: 'surfaces.taskTimeline.events.taskUpdated',
    task_claimed: 'surfaces.taskTimeline.events.taskClaimed',
    task_claim_renewed: 'surfaces.taskTimeline.events.claimRenewed',
    task_claim_released: 'surfaces.taskTimeline.events.claimReleased',
    status_changed: 'surfaces.taskTimeline.events.statusChanged',
    agent_run_started: 'surfaces.taskTimeline.events.runStarted',
    agent_run_finished: 'surfaces.taskTimeline.events.runFinished',
    github_pr_opened: 'surfaces.taskTimeline.events.githubPrOpened',
    github_pr_edited: 'surfaces.taskTimeline.events.githubPrUpdated',
    github_pr_reopened: 'surfaces.taskTimeline.events.githubPrReopened',
    github_pr_synchronize: 'surfaces.taskTimeline.events.githubPrUpdated',
    github_pr_ready_for_review: 'surfaces.taskTimeline.events.githubPrReady',
    github_pr_converted_to_draft: 'surfaces.taskTimeline.events.githubPrDraft',
    github_pr_closed: 'surfaces.taskTimeline.events.githubPrClosed',
    github_pr_merged: 'surfaces.taskTimeline.events.githubPrMerged',
    github_status_automation_failed: 'surfaces.taskTimeline.events.githubAutomationFailed',
    release_shipped: 'surfaces.taskTimeline.events.releaseShipped',
};

const providerLabel = (provider: string) => (
    provider
        .split(/[_\s-]+/)
        .filter(Boolean)
        .map(part => part.charAt(0).toUpperCase() + part.slice(1))
        .join(' ') || t('surfaces.taskTimeline.external')
);

const linkLabel = (link: ExternalLink) => (
    link.title || link.external_key || link.url || providerLabel(link.provider)
);

const githubUrlPattern = /^(https?:\/\/)?(www\.)?github\.com\/[^/\s]+\/[^/\s]+\/(?:(pull|issues)\/\d+(?:[/?#].*)?|tree\/[^?\s#]+(?:[/?#].*)?)$/i;

const metadataString = (link: ExternalLink, key: string) => {
    const value = link.metadata_json?.[key];
    return typeof value === 'string' ? value : null;
};

const metadataNumber = (link: ExternalLink, key: string) => {
    const value = link.metadata_json?.[key];
    if (typeof value === 'number') return value;
    if (typeof value === 'string' && /^\d+$/.test(value)) return Number(value);
    return null;
};

const githubTypeLabel = (type: string | null) => {
    if (type === 'pull_request') return 'PR';
    if (type === 'issue') return t('surfaces.taskTimeline.issue');
    if (type === 'branch') return t('surfaces.taskTimeline.branch');
    return null;
};

const githubDetails = (link: ExternalLink) => {
    if (link.provider !== 'github') return null;

    const repo = metadataString(link, 'repo_full_name');
    const type = githubTypeLabel(metadataString(link, 'github_type'));
    const number = metadataNumber(link, 'number');
    const branch = metadataString(link, 'branch');
    const target = number !== null ? `#${number}` : branch;
    return [repo, type, target].filter(Boolean).join(' · ');
};

const isRefreshableGitHubPr = (link: ExternalLink) => (
    !link.is_legacy
    && Boolean(link.id)
    && link.provider === 'github'
    && metadataString(link, 'github_type') === 'pull_request'
);

const linkTooltip = (link: ExternalLink) => {
    const parts = [linkLabel(link), githubDetails(link)];
    const refreshedAt = metadataString(link, 'status_refreshed_at');
    const refreshError = metadataString(link, 'status_refresh_error');
    if (refreshedAt) parts.push(t('surfaces.taskTimeline.refreshedAt', { date: formatDateTime(refreshedAt) }));
    if (refreshError) parts.push(t('surfaces.taskTimeline.refreshError', { error: refreshError }));
    return parts.filter(Boolean).join('\n');
};

export const TaskTimelinePanel = ({ task }: TaskTimelinePanelProps) => {
    useTranslation();
    const [nowMs] = useState(() => Date.now());
    const [githubUrl, setGithubUrl] = useState('');
    const [linkError, setLinkError] = useState<string | null>(null);
    const [deletingLinkId, setDeletingLinkId] = useState<number | null>(null);
    const [refreshingLinkId, setRefreshingLinkId] = useState<number | null>(null);
    const queryClient = useQueryClient();

    const timelineQuery = useQuery({
        queryKey: ['task-timeline', task.id],
        queryFn: () => taskService.getTimeline(task.id),
    });
    const linksQuery = useQuery({
        queryKey: ['task-external-links', task.id],
        queryFn: () => taskService.getExternalLinks(task.id),
        initialData: task.external_links,
    });
    const timelineData = timelineQuery.data;
    const isLoading = timelineQuery.isLoading;
    const externalLinks = linksQuery.data ?? task.external_links;
    const linksAreFetching = linksQuery.isFetching;

    const createGitHubLinkMutation = useMutation({
        mutationFn: (url: string) => taskService.createGitHubExternalLink(task.id, { url }),
        onSuccess: () => {
            setGithubUrl('');
            setLinkError(null);
            queryClient.invalidateQueries({ queryKey: ['task-external-links', task.id] });
        },
        onError: (error: unknown) => {
            setLinkError(getApiErrorMessage(error, t('surfaces.taskTimeline.failedToLinkGitHub')));
        },
    });

    const deleteLinkMutation = useMutation({
        mutationFn: (linkId: number) => taskService.deleteExternalLink(linkId),
        onSuccess: () => {
            setLinkError(null);
            queryClient.invalidateQueries({ queryKey: ['task-external-links', task.id] });
        },
        onError: (error: unknown) => {
            setLinkError(getApiErrorMessage(error, t('surfaces.taskTimeline.failedToDeleteLink')));
        },
    });

    const refreshGitHubLinkMutation = useMutation({
        mutationFn: (linkId: number) => taskService.refreshGitHubExternalLink(linkId),
        onSuccess: () => {
            setLinkError(null);
            queryClient.invalidateQueries({ queryKey: ['task-external-links', task.id] });
        },
        onError: (error: unknown) => {
            setLinkError(getApiErrorMessage(error, t('surfaces.taskTimeline.failedToRefreshGitHub')));
        },
    });

    const claimIsStale = task.claim_expires_at
        ? new Date(task.claim_expires_at).getTime() < nowMs
        : false;

    const handleGitHubLinkSubmit = (event: FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        const trimmedUrl = githubUrl.trim();

        if (!trimmedUrl) {
            setLinkError(t('surfaces.taskTimeline.enterGitHubUrl'));
            return;
        }

        if (!githubUrlPattern.test(trimmedUrl)) {
            setLinkError(t('surfaces.taskTimeline.pasteGitHubPRIssueOrBranchURL'));
            return;
        }

        createGitHubLinkMutation.mutate(trimmedUrl);
    };

    const handleDeleteLink = (linkId: number) => {
        setDeletingLinkId(linkId);
        deleteLinkMutation.mutate(linkId, {
            onSettled: () => setDeletingLinkId(null),
        });
    };

    const handleRefreshLink = (linkId: number) => {
        setRefreshingLinkId(linkId);
        refreshGitHubLinkMutation.mutate(linkId, {
            onSettled: () => setRefreshingLinkId(null),
        });
    };

    const handleRequestLinksChanged = () => {
        queryClient.invalidateQueries({ queryKey: ['tasks'] });
        queryClient.invalidateQueries({ queryKey: ['tasks', task.iteration_id] });
        queryClient.invalidateQueries({ queryKey: ['task', task.id] });
        if (task.project_id) {
            queryClient.invalidateQueries({ queryKey: ['projectSummary', task.project_id] });
            queryClient.invalidateQueries({ queryKey: ['projectTasks', task.project_id] });
        }
    };

    return (
        <div className="border border-border rounded-lg p-4 bg-surface-muted space-y-4">
            <div className="flex items-center justify-between gap-3">
                <div className="flex items-center gap-2 text-sm font-medium text-content-primary">
                    <History className="w-4 h-4 text-content-secondary" />
                    {t('surfaces.taskTimeline.timeline')}
                    <span className="rounded-full bg-action-muted px-2 py-0.5 text-wc-micro font-medium text-action">
                        {task.request_count ?? 0} {t('surfaces.taskTimeline.requests')}
                    </span>
                </div>
                <span className="text-xs text-content-secondary">v{task.version}</span>
            </div>

            {timelineQuery.isError && (
                <QueryErrorState error={timelineQuery.error} onRetry={() => void timelineQuery.refetch()} />
            )}
            {linksQuery.isError && (
                <QueryErrorState error={linksQuery.error} onRetry={() => void linksQuery.refetch()} />
            )}

            <div className="space-y-3">
                {task.claimed_by && (
                    <span className={clsx(
                        "inline-flex items-center gap-1 px-2 py-1 rounded-full border",
                        claimIsStale
                            ? "bg-feedback-warning-muted text-feedback-warning-foreground border-feedback-warning-border"
                            : "bg-action-muted text-action border-action"
                    )}>
                        <Bot className="w-3 h-3" />
                        {claimIsStale ? t('surfaces.taskTimeline.staleClaim') : t('surfaces.taskTimeline.claimed')}: {task.claimed_by.display_name}
                    </span>
                )}

                <RequestSourceLinksPanel
                    targetType="task"
                    targetId={task.id}
                    initialCount={task.request_count ?? 0}
                    title={t('surfaces.taskTimeline.requestSources')}
                    compact
                    onChanged={handleRequestLinksChanged}
                />

                <div className="rounded-md border border-border bg-surface-card p-3">
                    <div className="mb-2 flex items-center justify-between gap-2">
                        <div className="flex items-center gap-2 text-xs font-semibold uppercase text-content-secondary">
                            <LinkIcon className="h-3.5 w-3.5" />
                            {t('surfaces.taskTimeline.externalLinks')}
                        </div>
                        {linksAreFetching && (
                            <span className="text-wc-micro text-content-tertiary">{t('surfaces.taskTimeline.refreshing')}</span>
                        )}
                    </div>

                    <form onSubmit={handleGitHubLinkSubmit} className="mb-3 flex flex-col gap-2 sm:flex-row">
                        <input
                            type="text"
                            value={githubUrl}
                            onChange={event => {
                                setGithubUrl(event.target.value);
                                if (linkError) setLinkError(null);
                            }}
                            placeholder={t('surfaces.taskTimeline.pasteGitHubPRIssueOrBranchURL')}
                            className="min-w-0 flex-1 rounded-md border border-border-strong px-3 py-1.5 text-xs text-content-primary shadow-sm focus:border-action focus:outline-none focus:ring-1 focus:ring-focus"
                        />
                        <button
                            type="submit"
                            disabled={createGitHubLinkMutation.isPending || !githubUrl.trim()}
                            className="inline-flex items-center justify-center gap-1 rounded-md bg-action px-3 py-1.5 text-xs font-medium text-content-emphasis transition hover:bg-action-hover disabled:cursor-not-allowed disabled:opacity-50"
                        >
                            <Plus className="h-3.5 w-3.5" />
                            {t('surfaces.taskTimeline.link')}
                        </button>
                    </form>

                    {linkError && (
                        <div className="mb-3 flex items-start justify-between gap-2 rounded-md border border-feedback-danger-border bg-feedback-danger-muted px-3 py-2 text-xs text-feedback-danger-foreground">
                            <span>{linkError}</span>
                            <button
                                type="button"
                                onClick={() => setLinkError(null)}
                                className="shrink-0 rounded p-0.5 text-feedback-danger hover:bg-feedback-danger-muted-hover"
                                aria-label={t('surfaces.taskTimeline.dismissExternalLinkError')}
                            >
                                <X className="h-3.5 w-3.5" />
                            </button>
                        </div>
                    )}

                    {externalLinks.length > 0 ? (
                        <div className="flex flex-wrap gap-2">
                            {externalLinks.map((link, index) => {
                                const label = linkLabel(link);
                                const details = githubDetails(link);
                                const refreshError = metadataString(link, 'status_refresh_error');
                                const content = (
                                    <>
                                        <GitBranch className="h-3 w-3 shrink-0 text-content-secondary" />
                                        <span className="truncate">{label}</span>
                                        <span className="shrink-0 text-content-tertiary">
                                            {details || providerLabel(link.provider)}
                                        </span>
                                        {link.status && (
                                            <span className="shrink-0 rounded-full bg-action-muted px-1.5 py-0.5 text-wc-micro font-medium text-action">
                                                {link.status}
                                            </span>
                                        )}
                                        {refreshError && (
                                            <span className="shrink-0 rounded-full bg-feedback-danger-muted px-1.5 py-0.5 text-wc-micro font-medium text-feedback-danger-foreground">
                                                {t('surfaces.taskTimeline.refreshFailed')}
                                            </span>
                                        )}
                                        {link.is_legacy && (
                                            <span className="shrink-0 rounded-full bg-feedback-warning-muted px-1.5 py-0.5 text-wc-micro font-medium text-feedback-warning-foreground">
                                                {t('surfaces.taskTimeline.legacy')}
                                            </span>
                                        )}
                                    </>
                                );

                                return (
                                    <span
                                        key={`${link.id ?? 'legacy'}-${index}`}
                                        className="inline-flex max-w-full items-center overflow-hidden rounded-full border border-border bg-surface-muted text-xs text-content-primary"
                                    >
                                        {link.url ? (
                                            <a
                                                href={safeExternalHref(link.url)}
                                                target="_blank"
                                                rel="noreferrer"
                                                title={linkTooltip(link)}
                                                className="inline-flex min-w-0 max-w-[320px] items-center gap-1 px-2 py-1 hover:text-action"
                                            >
                                                {content}
                                            </a>
                                        ) : (
                                            <span
                                                className="inline-flex min-w-0 max-w-[320px] items-center gap-1 px-2 py-1"
                                                title={linkTooltip(link)}
                                            >
                                                {content}
                                            </span>
                                        )}
                                        {isRefreshableGitHubPr(link) && (
                                            <button
                                                type="button"
                                                onClick={() => handleRefreshLink(link.id!)}
                                                disabled={refreshGitHubLinkMutation.isPending}
                                                className="task-link-icon-action inline-flex shrink-0 items-center justify-center border-l border-border text-content-tertiary hover:bg-action-muted hover:text-action disabled:cursor-not-allowed disabled:opacity-50"
                                                aria-label={t('surfaces.taskTimeline.refreshNamedLink', { label })}
                                                title={t('surfaces.taskTimeline.refreshGitHubStatus')}
                                            >
                                                <RefreshCw className={clsx(
                                                    "h-3 w-3",
                                                    refreshingLinkId === link.id && "animate-spin"
                                                )} />
                                            </button>
                                        )}
                                        {!link.is_legacy && link.id && (
                                            <button
                                                type="button"
                                                onClick={() => handleDeleteLink(link.id!)}
                                                disabled={deleteLinkMutation.isPending}
                                                className="task-link-icon-action inline-flex shrink-0 items-center justify-center border-l border-border text-content-tertiary hover:bg-feedback-danger-muted hover:text-feedback-danger-foreground disabled:cursor-not-allowed disabled:opacity-50"
                                                aria-label={t('surfaces.taskTimeline.deleteNamedLink', { label })}
                                                title={t('surfaces.taskTimeline.deleteLink')}
                                            >
                                                <Trash2 className={clsx(
                                                    "h-3 w-3",
                                                    deletingLinkId === link.id && "opacity-50"
                                                )} />
                                            </button>
                                        )}
                                    </span>
                                );
                            })}
                        </div>
                    ) : !linksQuery.isError ? (
                        <div className="text-xs text-content-secondary">{t('surfaces.taskTimeline.noExternalLinksYet')}</div>
                    ) : null}
                </div>
            </div>

            {timelineQuery.isError ? null : isLoading ? (
                <div className="text-sm text-content-secondary">{t('surfaces.taskTimeline.loadingTimeline')}</div>
            ) : timelineData && timelineData.items.length > 0 ? (
                <div className="space-y-3 max-h-72 overflow-y-auto pr-1">
                    {timelineData.items.map((item, index) => {
                        const artifactLinks = Array.isArray(item.payload.artifact_links)
                            ? item.payload.artifact_links as string[]
                            : [];
                        const artifactLabel = typeof item.payload.artifact_label === 'string'
                            ? item.payload.artifact_label
                            : t('common.artifact');
                        const title = itemLabels[item.title] ? t(itemLabels[item.title]) : item.title;

                        return (
                            <div key={`${item.item_type}-${item.timestamp}-${index}`} className="flex gap-3">
                                <div className="pt-1">
                                    <CircleDot className={clsx(
                                        "w-3.5 h-3.5",
                                        item.actor_type === 'agent' ? "text-action" : "text-content-tertiary"
                                    )} />
                                </div>
                                <div className="min-w-0 flex-1">
                                    <div className="flex items-center justify-between gap-2">
                                        <span className="text-sm font-medium text-content-primary truncate">{title}</span>
                                        <span className="text-wc-micro text-content-secondary flex-shrink-0">
                                            {formatDateTime(item.timestamp)}
                                        </span>
                                    </div>
                                    <div className="text-xs text-content-secondary mt-0.5">
                                        {item.actor_type || t('common.system')}
                                        {item.trace_id && <span> - {item.trace_id}</span>}
                                    </div>
                                    {typeof item.payload.summary === 'string' && item.payload.summary && (
                                        <p className="text-xs text-content-primary mt-1">{item.payload.summary}</p>
                                    )}
                                    {artifactLinks.length > 0 && (
                                        <div className="flex flex-wrap gap-1 mt-2">
                                            {artifactLinks.map((link) => (
                                                <a
                                                    key={link}
                                                    href={safeExternalHref(link)}
                                                    target="_blank"
                                                    rel="noreferrer"
                                                    className="text-xs text-action bg-action-muted px-2 py-0.5 rounded border border-action"
                                                >
                                                    {artifactLabel}
                                                </a>
                                            ))}
                                        </div>
                                    )}
                                </div>
                            </div>
                        );
                    })}
                </div>
            ) : (
                <div className="text-sm text-content-secondary">{t('surfaces.taskTimeline.noEventsYet')}</div>
            )}
        </div>
    );
};

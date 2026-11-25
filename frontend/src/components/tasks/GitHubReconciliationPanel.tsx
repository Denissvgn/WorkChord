import { useId } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { githubService } from '../../services/githubService';
import { taskService } from '../../services/taskService';
import type { TaskViewSession, TaskViewSessionUpdate } from './taskViewSession';
import type { GitHubPullReconciliation, GitHubReconciliation } from '../../types/github';
import type { Task } from '../../types/task';
import { useProjectEditAccess } from '../../features/identity/useProjectEditAccess';
import { getApiErrorMessage } from '../../utils/apiError';
import { formatDateTime } from '../../utils/formatDate';
import { Button } from '../common/Button';
import { QueryErrorState } from '../feedback/QueryState';

const shortSha = (sha?: string | null) => (sha ? sha.slice(0, 7) : null);
const KNOWN_DIFFERENCES = ['never_observed', 'observation_failed', 'head_differs_from_submission', 'checks_not_observed_for_head',
    'merged_without_acceptance', 'closed_without_merge', 'task_replaced'];
const KNOWN_OWNERS = ['pm', 'worker', 'reviewer', 'none'];
const KNOWN_STATES = ['unobserved', 'open', 'draft', 'merged', 'closed_unmerged'];
const KNOWN_REVIEWS = ['not_requested', 'queued', 'accepted', 'fulfilled', 'cancelled'];
const KNOWN_SOURCES = ['webhook', 'refresh'];
const KNOWN_CHECKS = ['success', 'failure', 'pending', 'not_observed'];

const Row = ({ label, children }: { label: string; children: React.ReactNode }) => (
    <div className="grid grid-cols-[minmax(7rem,9rem)_1fr] gap-x-3 text-sm max-[520px]:grid-cols-1">
        <dt className="text-content-secondary">{label}</dt>
        <dd className="min-w-0 break-words">{children}</dd>
    </div>
);

const Sha = ({ sha }: { sha?: string | null }) => (sha
    ? <code className="font-mono text-xs" title={sha}>{shortSha(sha)}</code> : null);

const PullRequest = ({ pull, language }: { pull: GitHubPullReconciliation; language: string }) => {
    const { t } = useTranslation();
    const headDiffers = pull.differences.includes('head_differs_from_submission');
    const state = KNOWN_STATES.includes(pull.state) ? t(`teamwork.ghState_${pull.state}`) : pull.state;
    const checks = pull.checks.state
        ? (KNOWN_CHECKS.includes(pull.checks.state) ? t(`teamwork.ghChecks_${pull.checks.state}`) : pull.checks.state)
        : null;
    const review = pull.review.accepted ? t('teamwork.ghAccepted')
        : KNOWN_REVIEWS.includes(pull.review.state) ? t(`teamwork.ghReview_${pull.review.state}`) : pull.review.state;
    const source = pull.observation_source && (KNOWN_SOURCES.includes(pull.observation_source) ? t(`teamwork.ghSource_${pull.observation_source}`) : pull.observation_source);
    const owner = KNOWN_OWNERS.includes(pull.next_owner) ? t(`teamwork.ghOwner_${pull.next_owner}`) : pull.next_owner;
    const when = (value?: string | null) => (value ? formatDateTime(value, language) : null);
    return <li className="space-y-3 rounded-md border border-border p-3">
        <div className="flex flex-wrap items-center justify-between gap-2">
            <p className="min-w-0 break-words font-medium">
                {pull.url
                    ? <a className="underline underline-offset-2" href={pull.url} target="_blank" rel="noreferrer">{pull.title ?? pull.url}</a>
                    : pull.title ?? t('teamwork.ghUntitledPull')}
            </p>
            <span className="rounded-full bg-surface-muted px-2 py-0.5 text-xs font-medium">{state}</span>
        </div>
        <dl className="space-y-1.5">
            <Row label={t('teamwork.ghSubmitted')}>{pull.submitted_sha ? <Sha sha={pull.submitted_sha} /> : t('teamwork.ghNoSubmission')}</Row>
            <Row label={t('teamwork.ghHead')}>
                {pull.observed_head_sha ? <Sha sha={pull.observed_head_sha} /> : t('teamwork.ghHeadUnknown')}
                {headDiffers && <span className="ml-2 text-feedback-warning-foreground">{t('teamwork.ghHeadStale')}</span>}
            </Row>
            <Row label={t('teamwork.ghChecks')}>
                {checks ?? t('teamwork.ghChecksUnknown')}
                {pull.checks.total != null && <> · {t('teamwork.ghChecksTotal', { count: pull.checks.total })}</>}
                {pull.checks.error && <span className="ml-2 text-feedback-danger-foreground">{pull.checks.error}</span>}
            </Row>
            <Row label={t('teamwork.ghTargetBranch')}>{pull.target_branch ? <code className="font-mono text-xs">{pull.target_branch}</code> : t('teamwork.ghBranchUnknown')}</Row>
            <Row label={t('teamwork.ghOutcome')}>
                {pull.merged
                    ? <>{t('teamwork.ghMerged', { when: when(pull.merged_at) ?? t('teamwork.ghTimeUnknown') })}{pull.merge_commit_sha && <> · <Sha sha={pull.merge_commit_sha} /></>}</>
                    : pull.closed_at ? t('teamwork.ghClosedUnmerged', { when: when(pull.closed_at) })
                        : pull.state === 'unobserved' ? t('teamwork.ghNotObserved') : t('teamwork.ghNotMerged')}
            </Row>
            <Row label={t('teamwork.ghObserved')}>
                {pull.observed_at ? t('teamwork.ghObservedAt', { when: when(pull.observed_at) }) : t('teamwork.ghNeverObserved')}
                {source && <> · {source}</>}
            </Row>
            <Row label={t('teamwork.ghReview')}>{review}</Row>
        </dl>
        {pull.observation_error && <p role="status" className="rounded-md bg-feedback-danger-muted px-3 py-2 text-sm text-feedback-danger-foreground">{t('teamwork.ghObservationFailed', { error: pull.observation_error })}</p>}
        {pull.differences.length > 0 && <div>
            <p className="text-sm font-medium">{t('teamwork.ghDifferences')}</p>
            <ul className="list-disc pl-5 text-sm">{pull.differences.map(code =>
                <li key={code}>{KNOWN_DIFFERENCES.includes(code) ? t(`teamwork.ghDiff_${code}`) : code}</li>)}</ul>
        </div>}
        <p className="text-sm"><span className="font-medium">{t('teamwork.ghNext', { owner })}</span>{' '}{pull.next_action}</p>
    </li>;
};

/** Per linked pull request: the submitted commit against what GitHub last showed, and who acts next. */
export const GitHubReconciliationPanel = ({ task, session, onSession, onTaskUpdated }: {
    task: Task; session: TaskViewSession; onSession: TaskViewSessionUpdate; onTaskUpdated: (task: Task) => void;
}) => {
    const { t, i18n } = useTranslation();
    const headingId = useId();
    const queryClient = useQueryClient();
    const { canEdit } = useProjectEditAccess(task.project_id);
    const key = ['github-reconciliation', task.id, task.version];
    // feedback-policy: query loading,error,retry,empty - a failed read keeps a retry and never shows a stale view as current.
    const view = useQuery({ queryKey: key, queryFn: ({ signal }) => githubService.getReconciliation(task.id, signal) });
    // feedback-policy: mutation pending,inline - catch-up disables repeat runs and names a failure beside the action.
    const catchUp = useMutation({
        mutationFn: async () => {
            const latestView = await githubService.catchUp(task.id);
            // Catch-up records new observations, which advances the task version; hand over the current task.
            let latest: Task | null = null;
            try { latest = await taskService.getById(task.id); } catch { /* The view is still current; the next read of the task refreshes it. */ }
            return { latestView, latest };
        },
        onMutate: () => onSession({ catchUpDone: false }),
        onSuccess: ({ latestView, latest }) => {
            queryClient.setQueryData<GitHubReconciliation>(key, latestView);
            queryClient.setQueryData<GitHubReconciliation>(['github-reconciliation', task.id, latest?.version ?? task.version], latestView);
            void queryClient.invalidateQueries({ queryKey: ['delivery-dependencies'] });
            onSession({ catchUpDone: true });
            if (latest) onTaskUpdated(latest);
        },
    });
    const data = view.data;
    const pulls = data?.pull_requests ?? [];
    const successorPulls = data?.successor?.pull_requests ?? [];
    return <section aria-labelledby={headingId} className="space-y-3 rounded-md border border-border p-3">
        <div className="flex flex-wrap items-center justify-between gap-2">
            <h3 id={headingId} className="font-medium">{t('teamwork.ghReconciliation')}</h3>
            {canEdit && <Button type="button" variant="secondary" size="sm" isLoading={catchUp.isPending} disabled={view.isLoading}
                onClick={() => catchUp.mutate()}>{t('teamwork.ghRunCatchUp')}</Button>}
        </div>
        <p className="text-sm text-content-secondary">{t('teamwork.ghHelp')}</p>
        {view.isLoading && <p role="status">{t('common.loading')}</p>}
        {view.isError && <QueryErrorState error={view.error} fallback={t('teamwork.ghLoadFailed')} onRetry={() => void view.refetch()} />}
        {catchUp.isError && <p role="alert" className="text-sm text-feedback-danger-foreground">{getApiErrorMessage(catchUp.error, t('teamwork.ghCatchUpFailed'))}</p>}
        {session.catchUpDone && !catchUp.isPending && !catchUp.isError && <p role="status" className="text-sm text-content-secondary">{t('teamwork.ghCatchUpDone')}</p>}
        {data?.replacement && <p className="rounded-md bg-surface-muted px-3 py-2 text-sm">
            {data.replacement.role === 'original'
                ? t('teamwork.ghReplacedBy', { id: data.replacement.replacement_task_id })
                : t('teamwork.ghReplacesTask', { id: data.replacement.original_task_id })}</p>}
        {data && pulls.length === 0 && <p className="text-sm">{t('teamwork.ghNoPulls')}</p>}
        {pulls.length > 0 && <ul className="space-y-3">{pulls.map(pull => <PullRequest key={pull.link_id} pull={pull} language={i18n.language} />)}</ul>}
        {successorPulls.length > 0 && <div className="space-y-2">
            <p className="text-sm font-medium">{t('teamwork.ghSuccessorPulls', { id: data?.successor?.task_id })}</p>
            <ul className="space-y-3">{successorPulls.map(pull => <PullRequest key={pull.link_id} pull={pull} language={i18n.language} />)}</ul>
        </div>}
    </section>;
};

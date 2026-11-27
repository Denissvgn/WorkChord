import { useTranslation } from 'react-i18next';
import type { TFunction } from 'i18next';
import type { RoutingCheck, TaskBulkOperationResult } from '../../types/task';
import { rungLabel, routingConflicts, suggestedReviewerOf } from '../../utils/routingCheck';

const issueText = (t: TFunction, issue: RoutingCheck['issues'][number]) => (
    t(`taskReassign.issues.${issue.code}`, { defaultValue: issue.message, key: issue.catalog_key ?? '', publisher: issue.publisher_key ?? '' })
);

/**
 * What a reassignment would do to the task's routing: the conflicts with the project's review
 * policy, the warnings, and the reviewer the server suggests instead. Shown before anything is saved.
 */
export const RoutingCheckNotice = ({ check, assigneeName }: { check: RoutingCheck; assigneeName: string }) => {
    const { t } = useTranslation();
    if (!check.structured || check.issues.length === 0) return null;
    const conflicts = routingConflicts(check);
    const warnings = check.issues.filter(issue => issue.severity !== 'conflict');
    const reviewer = suggestedReviewerOf(check);
    const firstRung = check.suggestion?.first_rung ?? null;
    const refused = check.conflict_mode === 'refuse';
    return (
        <div role="group" aria-label={t('taskReassign.noticeLabel')} data-routing-check={conflicts.length > 0 ? 'conflict' : 'warning'}
            className="flex flex-col gap-2 rounded-md border border-feedback-warning-border bg-feedback-warning-muted px-3 py-3 text-sm text-feedback-warning-foreground">
            <p className="font-semibold">
                {conflicts.length > 0 ? t('taskReassign.conflictTitle', { name: assigneeName }) : t('taskReassign.warningTitle', { name: assigneeName })}
            </p>
            <ul className="list-disc pl-5">
                {[...conflicts, ...warnings].map((issue, index) => <li key={`${issue.code}-${index}`}>{issueText(t, issue)}</li>)}
            </ul>
            {conflicts.length > 0 && (
                <p>{refused ? t('taskReassign.refuseHint') : t('taskReassign.warnHint')}</p>
            )}
            {check.suggestion ? (
                <p>
                    {reviewer && <span className="block">{t('taskReassign.suggestedReviewer', { reviewer: rungLabel(t, reviewer) })}</span>}
                    {firstRung && <span className="block">{t('taskReassign.suggestedFirstRung', { rung: rungLabel(t, firstRung) })}</span>}
                </p>
            ) : conflicts.length > 0 && <p>{t('taskReassign.noSuggestion')}</p>}
        </div>
    );
};

/**
 * The tasks of a bulk reassignment that need a new reviewer, each with what conflicts and which
 * reviewer is suggested, so one confirmation can apply them all.
 */
export const RoutingResultsList = ({ results, titleOf }: { results: TaskBulkOperationResult[]; titleOf: (taskId: number) => string }) => {
    const { t } = useTranslation();
    return (
        <ul className="flex flex-col gap-1.5 text-sm" aria-label={t('taskReassign.bulkList')}>
            {results.map(result => {
                const check = result.routing_check!;
                const reviewer = suggestedReviewerOf(check);
                const conflicts = routingConflicts(check);
                const reasons = (conflicts.length > 0 ? conflicts : check.issues).map(issue => issueText(t, issue)).join(' ');
                return (
                    <li key={result.task_id} data-routing-task={result.task_id}>
                        <span className="font-medium">{titleOf(result.task_id)}</span>
                        {': '}{reasons}{' '}
                        <span className="text-content-secondary">
                            {reviewer ? t('taskReassign.suggestedReviewer', { reviewer: rungLabel(t, reviewer) }) : t('taskReassign.noSuggestion')}
                        </span>
                    </li>
                );
            })}
        </ul>
    );
};

import { useTranslation } from 'react-i18next';
import type { TFunction } from 'i18next';
import type { RoutingCheck } from '../../types/task';
import { routingChangeLines, routingConflicts, type RoutingChangeItem } from '../../utils/routingCheck';

type Issue = RoutingCheck['issues'][number];

const issueText = (t: TFunction, issue: Issue) => (
    t(`taskReassign.issues.${issue.code}`, { defaultValue: issue.message, key: issue.catalog_key ?? '', publisher: issue.publisher_key ?? '' })
);

/** What the suggested routing would change, part by part, so nothing is saved unseen. */
const ChangeLines = ({ lines }: { lines: string[] }) => (
    lines.length > 0 ? <ul className="list-disc pl-5">{lines.map(line => <li key={line}>{line}</li>)}</ul> : null
);

/**
 * What a reassignment would do to the task's routing: the conflicts with the project's review
 * policy, the warnings, and what the suggested routing would change. Shown before anything is saved.
 */
export const RoutingCheckNotice = ({ check, assigneeName }: { check: RoutingCheck; assigneeName: string }) => {
    const { t } = useTranslation();
    if (!check.structured || check.issues.length === 0) return null;
    const conflicts = routingConflicts(check);
    const warnings = check.issues.filter(issue => issue.severity !== 'conflict');
    const refused = check.conflict_mode === 'refuse';
    const changes = routingChangeLines(t, check.routing, check.suggestion);
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
                <p>
                    {check.suggestion
                        ? (refused ? t('taskReassign.refuseHint') : t('taskReassign.warnHint'))
                        : (refused ? t('taskReassign.refuseNoSuggestionHint') : t('taskReassign.warnNoSuggestionHint'))}
                </p>
            )}
            {check.suggestion && (
                <div>
                    <p className="font-medium">{t('taskReassign.suggestionChanges')}</p>
                    {changes.length > 0 ? <ChangeLines lines={changes} /> : <p>{t('taskReassign.suggestionNoChange')}</p>}
                </div>
            )}
        </div>
    );
};

/**
 * The tasks a bulk "use the suggested routing" confirmation would change, each with what conflicts
 * and exactly what the routing becomes, so one confirmation applies nothing that was not shown.
 */
export const RoutingResultsList = ({ items, titleOf }: { items: RoutingChangeItem[]; titleOf: (taskId: number) => string }) => {
    const { t } = useTranslation();
    return (
        <ul className="flex flex-col gap-2 text-sm" aria-label={t('taskReassign.bulkList')}>
            {items.map(item => {
                const conflicts = item.issues.filter(issue => issue.severity === 'conflict');
                const reasons = (conflicts.length > 0 ? conflicts : item.issues).map(issue => issueText(t, issue)).join(' ');
                return (
                    <li key={item.taskId} data-routing-task={item.taskId}>
                        <span className="font-medium">{titleOf(item.taskId)}</span>
                        {reasons ? `: ${reasons}` : ''}
                        {item.after ? <ChangeLines lines={routingChangeLines(t, item.before, item.after)} /> : <span className="block">{t('taskReassign.noSuggestion')}</span>}
                    </li>
                );
            })}
        </ul>
    );
};

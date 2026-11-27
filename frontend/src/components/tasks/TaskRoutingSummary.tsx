import { useTranslation } from 'react-i18next';
import type { TaskRouting } from '../../types/task';
import { rungLabel } from '../../utils/routingCheck';

const Row = ({ label, children }: { label: string; children: React.ReactNode }) => (
    <div className="flex flex-col gap-0.5">
        <dt className="text-xs text-content-secondary">{label}</dt>
        <dd className="text-sm font-medium text-content-primary">{children}</dd>
    </div>
);

/** The structured routing of a task: who runs it first, when it escalates and who reviews it. */
export const TaskRoutingSummary = ({ routing }: { routing: TaskRouting | null | undefined }) => {
    const { t } = useTranslation();
    const hasRouting = Boolean(routing && (routing.first_rung || routing.escalation.length > 0 || routing.reviewer));
    if (!routing || !hasRouting) return <p className="text-sm text-content-secondary">{t('taskReassign.noRouting')}</p>;
    return (
        <dl className="grid grid-cols-1 gap-3 sm:grid-cols-2">
            <Row label={t('taskReassign.firstRung')}>{routing.first_rung ? rungLabel(t, routing.first_rung) : t('common.none')}</Row>
            <Row label={t('taskReassign.reviewer')}>
                {routing.reviewer ? rungLabel(t, routing.reviewer) : t('common.none')}
                {routing.reviewer?.instructions && <span className="block text-xs font-normal text-content-secondary">{routing.reviewer.instructions}</span>}
            </Row>
            <Row label={t('taskReassign.escalation')}>
                {routing.escalation.length > 0 ? (
                    <>
                        <ol className="list-decimal pl-5">
                            {routing.escalation.map(rung => <li key={rung.catalog_key}>{rungLabel(t, rung)}</li>)}
                        </ol>
                        <span className="block text-xs font-normal text-content-secondary">{t('taskReassign.escalateAfter', { count: routing.escalate_after_failed_runs })}</span>
                    </>
                ) : t('common.none')}
            </Row>
            {routing.after_last_rung && <Row label={t('taskReassign.afterLastRung')}>{routing.after_last_rung}</Row>}
            {routing.notes && <Row label={t('taskReassign.notes')}>{routing.notes}</Row>}
        </dl>
    );
};

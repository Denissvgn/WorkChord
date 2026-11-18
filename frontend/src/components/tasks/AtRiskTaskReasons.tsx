import { useTranslation } from 'react-i18next';
import { atRiskReasons } from '../../features/planningMasters/atRiskReasons';
import type { Task } from '../../types/task';

/** The reasons an opened task is at risk, shown while the Tasks list is filtered to at-risk work. */
export const AtRiskTaskReasons = ({ task }: { task: Task }) => {
    const { t } = useTranslation();
    const reasons = atRiskReasons(task, t);
    if (reasons.length === 0) return null;
    return <section aria-label={t('planSchedule.whyAtRisk')} className="mb-4 rounded-md border border-border-subtle bg-surface-muted p-3 text-sm">
        <h3 className="font-medium text-content-primary">{t('planSchedule.whyAtRisk')}</h3>
        <ul className="mt-1 list-disc pl-5 text-content-secondary">{reasons.map(reason => <li key={reason}>{reason}</li>)}</ul>
    </section>;
};

import { useTranslation } from 'react-i18next';
import type { WorkMetrics } from '../../types/workMetrics';

export const WorkMetricsLine = ({ metrics }: { metrics?: WorkMetrics | null }) => {
    const { t, i18n } = useTranslation();
    if (metrics?.metric_contract_version !== 2) return null;
    const values = [
        ['implemented', metrics.implemented_tasks], ['accepted', metrics.accepted_tasks],
        ['overdueDelivery', metrics.overdue_tasks], ['lateStart', metrics.late_start_tasks],
        ['iterationOverflow', metrics.iteration_overflow_tasks],
    ] as const;
    return <dl className="flex flex-wrap gap-x-6 gap-y-3 border-y border-border-subtle py-3" aria-label={t('workStatus.deliveryMetrics')}>
        {values.map(([label, value]) => <div key={label} className="flex items-baseline gap-2">
            <dt className="text-sm text-content-secondary">{t(`workStatus.${label}`)}</dt>
            <dd className="font-semibold tabular-nums text-content-primary">{value === undefined ? '—' : new Intl.NumberFormat(i18n.language).format(value)}</dd>
        </div>)}
    </dl>;
};

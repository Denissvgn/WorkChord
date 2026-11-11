import { useTranslation } from 'react-i18next';
import type { WorkMetrics } from '../../types/workMetrics';
import type { MetricScope, WorkMetricName } from '../../services/taskService';
import { formatCount } from '../../utils/workNumbers';
import { MetricCount } from './MetricCount';

/** Delivery counts; with a scope, each one opens the tasks it counts. */
export const WorkMetricsLine = ({ metrics, scope = null }: { metrics?: WorkMetrics | null; scope?: MetricScope | null }) => {
    const { t, i18n } = useTranslation();
    if (metrics?.metric_contract_version !== 2) return null;
    const values = [
        ['implemented', 'implemented', metrics.implemented_tasks], ['accepted', 'accepted', metrics.accepted_tasks],
        ['overdueDelivery', 'overdue', metrics.overdue_tasks], ['lateStart', 'late_start', metrics.late_start_tasks],
        ['iterationOverflow', 'iteration_overflow', metrics.iteration_overflow_tasks],
    ] as const satisfies ReadonlyArray<readonly [string, WorkMetricName, number | undefined]>;
    return <dl className="flex flex-wrap gap-x-6 gap-y-3 border-y border-border-subtle py-3" aria-label={t('workStatus.deliveryMetrics')}>
        {values.map(([label, metric, value]) => {
            const text = formatCount(value, i18n.language);
            return <div key={label} className="flex items-baseline gap-2">
                <dt className="text-sm text-content-secondary">{t(`workStatus.${label}`)}</dt>
                <dd className="font-semibold tabular-nums text-content-primary">
                    {text === null ? t('common.unknown')
                        : <MetricCount metric={metric} scope={value ? scope : null} title={t(`workStatus.${label}`)}>{text}</MetricCount>}
                </dd>
            </div>;
        })}
    </dl>;
};

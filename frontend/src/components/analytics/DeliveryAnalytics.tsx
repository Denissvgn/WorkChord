import { useQuery } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { Link } from 'react-router-dom';
import { deliveryMetricsService } from '../../services/deliveryMetricsService';
import { QueryErrorState } from '../feedback/QueryState';
import type { DeliveryQueueItem } from '../../types/deliveryMetrics';
import { formatDateTime } from '../../utils/formatDate';
import { useScopeLink } from '../../features/scope/useScopeLink';
import { useAnalyticsScope } from './useAnalyticsScope';

/** Delivery history for the scope chosen in the scope bar. */
export const DeliveryAnalytics = ({ days }: { days: number }) => {
    const { t, i18n } = useTranslation();
    const scopeLink = useScopeLink();
    const params = useAnalyticsScope(days);
    const enabled = params !== undefined;
    // feedback-policy: query loading,error,retry,empty
    const report = useQuery({ queryKey: ['deliveryMetrics', params], queryFn: () => deliveryMetricsService.get(params!), enabled });
    const number = new Intl.NumberFormat(i18n.language, { maximumFractionDigits: 2 });
    const duration = (seconds: number | null) => seconds === null ? t('deliveryAnalytics.unknown')
        : seconds > 0 && seconds < 864 ? `<${number.format(0.01)}` : number.format(seconds / 86400);
    const queue = (title: string, items: DeliveryQueueItem[]) => <section className="min-w-0">
        <h3 className="mb-3 font-semibold">{title}</h3>
        {items.length === 0 ? <p className="text-sm text-content-secondary">{t('deliveryAnalytics.queueEmpty')}</p> : <ul className="divide-y divide-border-subtle">
            {items.map(item => <li key={item.task_id} className="flex items-baseline justify-between gap-4 py-3">
                <Link className="min-w-0 wrap-break-word text-action underline-offset-4 hover:underline" to={scopeLink(`/tasks?task=${item.task_id}`)}>{item.title}</Link>
                <span className="shrink-0 text-sm tabular-nums text-content-secondary">{duration(item.age_seconds)} {t('deliveryAnalytics.elapsedDays')}</span>
            </li>)}
        </ul>}
    </section>;
    const data = !enabled || report.isError ? undefined : report.data;
    return <section className="space-y-5 border-y border-border-subtle py-6" aria-labelledby="delivery-analytics-title">
        <div className="flex flex-wrap items-start justify-between gap-4">
            <div><h2 id="delivery-analytics-title" className="text-lg font-semibold">{t('deliveryAnalytics.title')}</h2>
                <p className="mt-1 max-w-prose text-sm text-content-secondary">{t('deliveryAnalytics.description')}</p></div>
        </div>
        {(!enabled || report.isLoading) && <p role="status">{t('common.loading')}</p>}
        {enabled && report.isError && <QueryErrorState error={report.error} onRetry={() => { void report.refetch(); }} />}
        {data && <>
            <p className="text-sm text-content-secondary">{t('deliveryAnalytics.observedWindow', {
                start: formatDateTime(data.window_start, i18n.language), end: formatDateTime(data.window_end, i18n.language) })}</p>
            <dl className="flex flex-wrap gap-x-8 gap-y-3">
                {([['accepted', data.accepted_leaf_tasks], ['rejected', data.rejection_events], ['canceled', data.canceled_leaf_tasks], ['reopened', data.reopened_events]] as const)
                    .map(([label, value]) => <div key={label} className="flex items-baseline gap-2"><dt className="text-sm text-content-secondary">{t(`deliveryAnalytics.${label}`)}</dt><dd className="font-semibold tabular-nums">{number.format(value)}</dd></div>)}
            </dl>
            {data.lead_time.sample_count + data.cycle_time.sample_count + data.review_delay.sample_count === 0 && <p className="text-sm text-content-secondary">{t('deliveryAnalytics.noSamples')}</p>}
            <div className="overflow-x-auto">
                <table className="w-full min-w-136 text-left text-sm">
                    <caption className="pb-3 text-left text-content-secondary">{t('deliveryAnalytics.durationBasis')}</caption>
                    <thead><tr className="border-b border-border-subtle">{['measure', 'mean', 'median', 'samples', 'unknown', 'censored'].map(label => <th className="px-3 py-2 font-medium" key={label} scope="col">{t(`deliveryAnalytics.${label}`)}</th>)}</tr></thead>
                    <tbody>{([['lead', data.lead_time], ['cycle', data.cycle_time], ['review', data.review_delay]] as const).map(([label, values]) => <tr key={label} className="border-b border-border-subtle">
                        <th className="px-3 py-3 font-medium" scope="row">{t(`deliveryAnalytics.${label}`)}</th>
                        <td className="px-3 py-3 tabular-nums">{duration(values.mean)}</td><td className="px-3 py-3 tabular-nums">{duration(values.median)}</td>
                        <td className="px-3 py-3 tabular-nums">{number.format(values.sample_count)}</td><td className="px-3 py-3 tabular-nums">{number.format(values.unknown_count)}</td><td className="px-3 py-3 tabular-nums">{number.format(values.censored_count)}</td>
                    </tr>)}</tbody>
                </table>
            </div>
            <p className="max-w-prose text-sm text-content-secondary">{t('deliveryAnalytics.coverage', { events: data.coverage.window_observation_count ?? data.coverage.observation_count,
                missing: data.coverage.current_leaves_without_capture, legacy: data.coverage.legacy_closed_acceptance_unknown })}</p>
            <div className="grid gap-6 lg:grid-cols-2">{queue(t('deliveryAnalytics.reviewQueue'), data.review_queue)}{queue(t('deliveryAnalytics.recoveryQueue'), data.recovery_queue)}</div>
            {data.queues_truncated && <p className="text-sm text-content-secondary">{t('deliveryAnalytics.queueLimit')}</p>}
        </>}
    </section>;
};

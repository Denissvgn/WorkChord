import { useTranslation } from 'react-i18next';
import type { IterationSummary } from '../../types/iteration';
import type { TaskDisplayedState } from '../../types/task';
import { STATE_TONE, toneSoftVar, toneVar } from '../ui/tone';
import { formatCount, formatPercent } from '../../utils/workNumbers';
import { MetricCount } from '../tasks/MetricCount';

/** States inside the iteration's totals; postponed work is still counted there. */
const ORDER: TaskDisplayedState[] = ['planned', 'active', 'resolved', 'closed', 'postponed'];
/** Withdrawn work: outside every total, counted apart. */
const ENDED: TaskDisplayedState[] = ['canceled', 'superseded'];

/** How the iteration's tasks split by status, in the canonical status colours, with a table view. */
export const StatusDistribution = ({ summary }: { summary: IterationSummary }) => {
    const { t, i18n } = useTranslation();
    const locale = i18n.resolvedLanguage ?? i18n.language;
    const counts = ORDER.map(status => ({ status, count: summary.status_counts?.[status] ?? 0 }));
    const ended = ENDED.map(status => ({ status, count: summary.status_counts?.[status] ?? 0 }));
    const total = counts.reduce((sum, item) => sum + item.count, 0);
    const endedTotal = ended.reduce((sum, item) => sum + item.count, 0);
    const scope = { iteration_id: summary.id };
    const accepted = summary.accepted_tasks ?? 0;
    if (total === 0 && endedTotal === 0) return null;
    return (
        <section className="card card-pad space-y-3" aria-labelledby="status-distribution-title">
            <h2 id="status-distribution-title" className="text-base font-semibold">{t('analytics.status.title')}</h2>
            <p className="text-sm text-content-secondary">{t('analytics.status.summary', { total, accepted })}
                {endedTotal > 0 && ` ${t('stoppedWork.endedOutside', { count: endedTotal })}`}</p>
            {total > 0 && <div className="flex h-8 w-full overflow-hidden rounded-md" role="img"
                aria-label={counts.map(item => `${t(`statuses.${item.status}`)} ${item.count}`).join(', ')}>
                {counts.filter(item => item.count > 0).map(item => (
                    <span key={item.status} title={`${t(`statuses.${item.status}`)}: ${item.count}`}
                        // Soft tint with a solid status edge keeps the count readable in every theme.
                        className="flex min-w-6 items-center justify-center text-xs font-semibold text-content-primary"
                        style={{ width: `${item.count / total * 100}%`, background: toneSoftVar[STATE_TONE[item.status]], borderBottom: `4px solid ${toneVar[STATE_TONE[item.status]]}` }}>
                        {formatCount(item.count, locale)}
                    </span>
                ))}
            </div>}
            <ul className="flex flex-wrap gap-x-5 gap-y-1 text-sm">
                {counts.map(item => (
                    <li key={item.status} className="flex items-center gap-2">
                        <span aria-hidden="true" className="h-3 w-3 rounded-sm" style={{ background: toneVar[STATE_TONE[item.status]] }} />
                        <MetricCount metric={item.status} scope={item.count > 0 ? scope : null} title={t(`statuses.${item.status}`)}>
                            {t(`statuses.${item.status}`)} {formatCount(item.count, locale)}
                        </MetricCount>
                    </li>
                ))}
                {ended.map(item => <li key={item.status} className="flex items-center gap-2">
                    <span aria-hidden="true" className="h-3 w-3 rounded-sm border border-dashed" style={{ borderColor: toneVar[STATE_TONE[item.status]] }} />
                    <MetricCount metric={item.status} scope={item.count > 0 ? scope : null} title={t(`statuses.${item.status}`)}>
                        {t(`statuses.${item.status}`)} {formatCount(item.count, locale)}
                    </MetricCount>
                </li>)}
                <li className="flex items-center gap-2">
                    <MetricCount metric="accepted" scope={accepted > 0 ? scope : null} title={t('metricList.accepted')}>
                        {t('analytics.status.accepted', { count: accepted })}
                    </MetricCount>
                </li>
            </ul>
            <details>
                <summary className="cursor-pointer text-sm font-medium text-action">
                    {t('analytics.showTable')}<span className="sr-only">: {t('analytics.status.title')}</span>
                </summary>
                <table className="mt-2 w-full max-w-md text-left text-sm">
                    <caption className="sr-only">{t('analytics.status.title')}</caption>
                    <thead><tr className="border-b border-border-subtle">
                        <th scope="col" className="py-2 font-medium">{t('analytics.status.status')}</th>
                        <th scope="col" className="py-2 text-right font-medium">{t('analytics.status.tasks')}</th>
                        <th scope="col" className="py-2 text-right font-medium">{t('analytics.status.share')}</th>
                    </tr></thead>
                    <tbody>
                        {counts.map(item => <tr key={item.status} className="border-b border-border-subtle">
                            <th scope="row" className="py-2 font-normal">{t(`statuses.${item.status}`)}</th>
                            <td className="text-right tabular-nums">{formatCount(item.count, locale)}</td>
                            <td className="text-right tabular-nums">{formatPercent(total > 0 ? item.count / total * 100 : 0, locale)}</td>
                        </tr>)}
                        {ended.map(item => <tr key={item.status} className="border-b border-border-subtle">
                            <th scope="row" className="py-2 font-normal">{t(`statuses.${item.status}`)}</th>
                            <td className="text-right tabular-nums">{formatCount(item.count, locale)}</td>
                            <td className="text-right text-content-secondary">{t('stoppedWork.outsideTotals')}</td>
                        </tr>)}
                        <tr><th scope="row" className="py-2 font-normal">{t('analytics.status.acceptedRow')}</th>
                            <td className="text-right tabular-nums">{formatCount(accepted, locale)}</td><td /></tr>
                    </tbody>
                </table>
            </details>
        </section>
    );
};

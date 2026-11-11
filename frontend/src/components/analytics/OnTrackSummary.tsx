import { useTranslation } from 'react-i18next';
import { Link } from 'react-router-dom';
import type { IterationSummary } from '../../types/iteration';
import { formatDate } from '../../utils/formatDate';
import { formatEffortDays } from '../../utils/workNumbers';
import { MetricCount } from '../tasks/MetricCount';
import { planMasterStepHref } from '../../features/planningMasters/planningReturn';

type Verdict = 'done' | 'noSchedule' | 'late' | 'atRisk' | 'onTrack';

/** Capacity still available: the iteration's capacity spread evenly over its working days. */
const capacityLeft = (summary: IterationSummary) => {
    if (!summary.team_capacity_days || !summary.working_days || summary.remaining_working_days == null) return null;
    return summary.team_capacity_days * summary.remaining_working_days / summary.working_days;
};

const onTrackVerdict = (summary: IterationSummary): Verdict => {
    const open = (summary.status_counts?.planned ?? 0) + (summary.status_counts?.active ?? 0);
    if (summary.total_tasks > 0 && open === 0) return 'done';
    if (!summary.scheduled_finish) return 'noSchedule';
    if (summary.scheduled_finish > summary.end_date) return 'late';
    const left = capacityLeft(summary);
    if (left !== null && (summary.remaining_effort_days ?? 0) > left) return 'atRisk';
    return 'onTrack';
};

/** Answers "are we on track for the end date?" in one line, then shows why. */
export const OnTrackSummary = ({ summary }: { summary: IterationSummary }) => {
    const { t, i18n } = useTranslation();
    const locale = i18n.resolvedLanguage ?? i18n.language;
    const verdict = onTrackVerdict(summary);
    const left = capacityLeft(summary);
    const remaining = summary.remaining_effort_days ?? 0;
    const scale = Math.max(remaining, left ?? 0, 0.0001);
    const effort = (value: number | null) => formatEffortDays(value, locale) ?? t('common.unknown');
    const scope = { iteration_id: summary.id };
    const tone = verdict === 'late' ? 'text-feedback-danger-foreground' : verdict === 'atRisk' || verdict === 'noSchedule' ? 'text-feedback-warning-foreground' : 'text-feedback-success-foreground';
    return (
        <section className="card card-pad space-y-4" aria-labelledby="on-track-title">
            <h3 id="on-track-title" className="text-base font-semibold">{t('analytics.onTrack.title')}</h3>
            <p className="text-lg">
                <strong className={tone}>{t(`analytics.onTrack.verdict_${verdict}`)}</strong>{' '}
                {summary.scheduled_finish
                    ? t('analytics.onTrack.finishAgainstEnd', { finish: formatDate(summary.scheduled_finish, locale), end: formatDate(summary.end_date, locale) })
                    : t('analytics.onTrack.endsOn', { end: formatDate(summary.end_date, locale) })}
                {verdict === 'noSchedule' && <> <Link to={planMasterStepHref('schedule')} className="font-medium text-action underline">{t('analytics.onTrack.planIt')}</Link></>}
            </p>
            <p className="text-sm text-content-secondary">
                {t('analytics.onTrack.effortLine', { remaining: effort(remaining), capacity: left === null ? t('analytics.onTrack.capacityUnknown') : effort(left), days: summary.remaining_working_days ?? 0 })}
                {(summary.unknown_estimate_tasks ?? 0) > 0 && <>{' · '}
                    <MetricCount metric="unknown_estimate" scope={scope} title={t('analytics.onTrack.unknownTitle')} className="text-feedback-warning-foreground">
                        {t('analytics.onTrack.unknownEstimates', { count: summary.unknown_estimate_tasks })}
                    </MetricCount></>}
                {(summary.overdue_tasks_count ?? 0) > 0 && <>{' · '}
                    <MetricCount metric="overdue" scope={scope} title={t('metricList.overdue')} className="text-feedback-danger-foreground">
                        {t('analytics.onTrack.overdue', { count: summary.overdue_tasks_count })}
                    </MetricCount></>}
                {(summary.blocked_tasks ?? 0) > 0 && <>{' · '}
                    <MetricCount metric="blocked" scope={scope} title={t('metricList.blocked')} className="text-feedback-warning-foreground">
                        {t('analytics.onTrack.blocked', { count: summary.blocked_tasks })}
                    </MetricCount></>}
            </p>
            <div className="space-y-2" aria-hidden="true">
                {([['remaining', remaining, 'var(--wc-status-active)'], ['capacity', left, 'var(--wc-status-resolved)']] as const).map(([key, value, color]) => (
                    <div key={key} className="grid grid-cols-[9rem_1fr_5rem] items-center gap-3 text-sm">
                        <span className="text-content-secondary">{t(`analytics.onTrack.${key}`)}</span>
                        <span className="h-3 rounded-full bg-surface-subtle">
                            {value !== null && <span className="block h-3 rounded-full" style={{ width: `${Math.min(100, value / scale * 100)}%`, background: color }} />}
                        </span>
                        <span className="text-right tabular-nums">{effort(value)}</span>
                    </div>
                ))}
            </div>
            <details>
                <summary className="cursor-pointer text-sm font-medium text-action">{t('analytics.showTable')}</summary>
                <table className="mt-2 w-full max-w-md text-left text-sm">
                    <caption className="sr-only">{t('analytics.onTrack.title')}</caption>
                    <tbody>
                        <tr className="border-b border-border-subtle"><th scope="row" className="py-2 font-medium">{t('analytics.onTrack.remaining')}</th><td className="tabular-nums">{effort(remaining)}</td></tr>
                        <tr className="border-b border-border-subtle"><th scope="row" className="py-2 font-medium">{t('analytics.onTrack.capacity')}</th><td className="tabular-nums">{left === null ? t('analytics.onTrack.capacityUnknown') : effort(left)}</td></tr>
                        <tr className="border-b border-border-subtle"><th scope="row" className="py-2 font-medium">{t('analytics.onTrack.workingDaysLeft')}</th><td className="tabular-nums">{summary.remaining_working_days ?? t('common.unknown')}</td></tr>
                        <tr className="border-b border-border-subtle"><th scope="row" className="py-2 font-medium">{t('analytics.onTrack.scheduledFinish')}</th><td>{summary.scheduled_finish ? formatDate(summary.scheduled_finish, locale) : t('analytics.onTrack.notScheduled')}</td></tr>
                        <tr><th scope="row" className="py-2 font-medium">{t('analytics.onTrack.unknownTitle')}</th><td className="tabular-nums">{summary.unknown_estimate_tasks ?? 0}</td></tr>
                    </tbody>
                </table>
            </details>
        </section>
    );
};

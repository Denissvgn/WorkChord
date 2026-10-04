import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { Link } from 'react-router-dom';
import { deliveryMetricsService } from '../../services/deliveryMetricsService';
import { projectService } from '../../services/projectService';
import { QueryErrorState } from '../feedback/QueryState';
import type { DeliveryQueueItem } from '../../types/deliveryMetrics';

export const DeliveryAnalytics = ({ iterationId }: { iterationId?: number }) => {
    const { t, i18n } = useTranslation();
    const [scope, setScope] = useState(iterationId ? 'iteration' : 'project');
    const [projectId, setProjectId] = useState<number>();
    const [days, setDays] = useState(30);
    const effectiveScope = scope === 'iteration' && iterationId ? 'iteration' : 'project';
    // feedback-policy: query loading,error,retry,empty
    const projects = useQuery({ queryKey: ['projects', 'delivery-analytics'], queryFn: projectService.getAll,
        enabled: effectiveScope === 'project' });
    const availableProjects = projects.isError ? [] : projects.data ?? [];
    const params = effectiveScope === 'iteration' ? { iteration_id: iterationId, lookback_days: days }
        : { project_id: projectId, lookback_days: days };
    const enabled = effectiveScope === 'iteration' ? Boolean(iterationId) : availableProjects.some(project => project.id === projectId);
    // feedback-policy: query loading,error,retry,empty
    const report = useQuery({ queryKey: ['deliveryMetrics', params], queryFn: () => deliveryMetricsService.get(params), enabled });
    const number = new Intl.NumberFormat(i18n.language, { maximumFractionDigits: 2 });
    const duration = (seconds: number | null) => seconds === null ? t('deliveryAnalytics.unknown') : number.format(seconds / 86400);
    const queue = (title: string, items: DeliveryQueueItem[]) => <section className="min-w-0">
        <h4 className="mb-3 font-semibold">{title}</h4>
        {items.length === 0 ? <p className="text-sm text-content-secondary">{t('deliveryAnalytics.queueEmpty')}</p> : <ul className="divide-y divide-border-subtle">
            {items.map(item => <li key={item.task_id} className="flex items-baseline justify-between gap-4 py-3">
                <Link className="min-w-0 break-words text-action underline-offset-4 hover:underline" to={`/tasks?task=${item.task_id}`}>{item.title}</Link>
                <span className="shrink-0 text-sm tabular-nums text-content-secondary">{duration(item.age_seconds)} {t('deliveryAnalytics.elapsedDays')}</span>
            </li>)}
        </ul>}
    </section>;
    const data = !enabled || report.isError || (effectiveScope === 'project' && projects.isError) ? undefined : report.data;
    return <section className="space-y-5 border-y border-border-subtle py-6" aria-labelledby="delivery-analytics-title">
        <div className="flex flex-wrap items-start justify-between gap-4">
            <div><h3 id="delivery-analytics-title" className="text-lg font-semibold">{t('deliveryAnalytics.title')}</h3>
                <p className="mt-1 max-w-prose text-sm text-content-secondary">{t('deliveryAnalytics.description')}</p></div>
            <div className="flex flex-wrap gap-3">
                <label className="text-sm">{t('deliveryAnalytics.scope')}<select className="ml-2 rounded border px-2 py-1" value={effectiveScope} onChange={event => setScope(event.target.value)}>
                    {Boolean(iterationId) && <option value="iteration">{t('deliveryAnalytics.iteration')}</option>}
                    <option value="project">{t('deliveryAnalytics.project')}</option>
                </select></label>
                {effectiveScope === 'project' && <label className="text-sm">{t('deliveryAnalytics.project')}<select className="ml-2 max-w-52 rounded border px-2 py-1" value={projectId ?? ''} onChange={event => setProjectId(event.target.value ? Number(event.target.value) : undefined)}>
                    <option value="">{t('deliveryAnalytics.chooseProject')}</option>
                    {availableProjects.map(project => <option key={project.id} value={project.id}>{project.name}</option>)}
                </select></label>}
                <label className="text-sm">{t('deliveryAnalytics.window')}<select className="ml-2 rounded border px-2 py-1" value={days} onChange={event => setDays(Number(event.target.value))}>
                    {[30, 90, 180, 366].map(value => <option key={value} value={value}>{t('deliveryAnalytics.days', { count: value })}</option>)}
                </select></label>
            </div>
        </div>
        {effectiveScope === 'project' && projects.isLoading && <p role="status">{t('common.loading')}</p>}
        {effectiveScope === 'project' && projects.isError && <QueryErrorState error={projects.error} onRetry={() => { void projects.refetch(); }} />}
        {!enabled && <p className="text-sm text-content-secondary">{t(availableProjects.length === 0 && !projects.isLoading ? 'deliveryAnalytics.noProjects' : 'deliveryAnalytics.chooseScope')}</p>}
        {enabled && report.isLoading && <p role="status">{t('common.loading')}</p>}
        {enabled && report.isError && <QueryErrorState error={report.error} onRetry={() => { void report.refetch(); }} />}
        {data && <>
            <p className="text-sm text-content-secondary">{t('deliveryAnalytics.observedWindow', {
                start: new Date(data.window_start).toLocaleString(i18n.language), end: new Date(data.window_end).toLocaleString(i18n.language) })}</p>
            <dl className="flex flex-wrap gap-x-8 gap-y-3">
                {([['accepted', data.accepted_leaf_tasks], ['rejected', data.rejection_events], ['canceled', data.canceled_leaf_tasks], ['reopened', data.reopened_events]] as const)
                    .map(([label, value]) => <div key={label} className="flex items-baseline gap-2"><dt className="text-sm text-content-secondary">{t(`deliveryAnalytics.${label}`)}</dt><dd className="font-semibold tabular-nums">{number.format(value)}</dd></div>)}
            </dl>
            {data.lead_time.sample_count + data.cycle_time.sample_count + data.review_delay.sample_count === 0 && <p className="text-sm text-content-secondary">{t('deliveryAnalytics.noSamples')}</p>}
            <div className="overflow-x-auto">
                <table className="w-full min-w-[34rem] text-left text-sm">
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

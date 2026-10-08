import { useLiveWindow } from '../../features/useLiveWindow';
import { LiveWindowStatus } from '../../components/feedback/LiveWindowStatus';
import { useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { format, startOfMonth } from 'date-fns';
import { useTimeEntries } from '../../features/timeEntries/useTimeEntries';
import { timeEntryService, timeAccessDenied } from '../../services/timeEntryService';
import { Button } from '../common/Button';
import { Input } from '../common/Input';
import { CollapsibleSection } from '../common/CollapsibleSection';
import { QueryErrorState } from '../feedback/QueryState';
import { getApiErrorMessage } from '../../utils/apiError';
import { TimeEntriesPanel } from '../tasks/TimeEntriesPanel';

export const TimeEntriesReport = ({ projectId }: { projectId: number }) => {
    const { enabled, capability } = useTimeEntries();
    const { t } = useTranslation();
    if (capability.isError) return <QueryErrorState error={capability.error} fallback={t('timeEntries.reportFailed')} onRetry={() => void capability.refetch()} />;
    if (!enabled) return null;
    return <CollapsibleSection title={t('timeEntries.report')}><ReportContent projectId={projectId} /></CollapsibleSection>;
};

const ReportContent = ({ projectId }: { projectId: number }) => {
    const { t, i18n } = useTranslation();
    const { identity } = useTimeEntries();
    const [start, setStart] = useState(format(startOfMonth(new Date()), 'yyyy-MM-dd'));
    const [end, setEnd] = useState(format(new Date(), 'yyyy-MM-dd'));
    const [scope, setScope] = useState<'mine' | 'project'>('mine');
    const canManage = identity?.workspace_role === 'owner' || identity?.workspace_role === 'operator'
        || identity?.projects[String(projectId)] === 'manager';
    const filters = { project_id: projectId, start, end, scope };
    // feedback-policy: query loading,error,retry,empty - errors hide cached scope totals and rows.
    const report = useLiveWindow({ queryKey: ['time-report', projectId, start, end, scope],
        enabled: Boolean(start && end && end >= start), initialPageParam: { after: 0, upper: undefined as number | undefined },
        queryFn: ({ pageParam, signal }) => timeEntryService.report(filters, pageParam.after, pageParam.upper, signal),
        getNextPageParam: page => page.has_more ? { after: page.next_after_id!, upper: page.upper_id } : undefined });
    // feedback-policy: mutation pending,inline - bounded authorized downloads expose failures and disable repeats.
    const download = useMutation({ mutationFn: (kind: 'entries' | 'totals') => timeEntryService.export(filters, kind),
        onSuccess: blob => {
            const url = URL.createObjectURL(blob); const link = document.createElement('a');
            link.href = url; link.download = 'recorded-time.csv'; link.click(); setTimeout(() => URL.revokeObjectURL(url), 1000);
        } });
    const totals = report.data?.pages[0]?.totals;
    const privateUnavailable = report.isError || timeAccessDenied(download.error);
    const value = (n: number | null | undefined, estimate = false) => n == null ? t(estimate ? 'timeEntries.unknownEstimate' : 'timeEntries.unknown') : n.toLocaleString(i18n.resolvedLanguage);
    return <section className="space-y-4" aria-label={t('timeEntries.report')}>
        <p className="text-sm text-content-secondary">{t('timeEntries.reportHelp')}</p>
        <div className="grid gap-3 sm:grid-cols-3">
            <Input label={t('timeEntries.start')} type="date" value={start} onChange={event => setStart(event.target.value)} />
            <Input label={t('timeEntries.end')} type="date" value={end} onChange={event => setEnd(event.target.value)} />
            <div><label className="field-lbl" htmlFor={`time-scope-${projectId}`}>{t('timeEntries.scope')}</label>
                <select id={`time-scope-${projectId}`} className="input w-full" value={scope} onChange={event => setScope(event.target.value as 'mine' | 'project')}>
                    <option value="mine">{t('timeEntries.mine')}</option>{canManage && <option value="project">{t('timeEntries.team')}</option>}
                </select></div>
        </div>
        {(!start || !end || end < start) && <p role="alert" className="text-sm text-feedback-danger-foreground">{t('timeEntries.invalid')}</p>}
        <LiveWindowStatus window={report} />
        {report.isLoading && <p role="status">{t('common.loading')}</p>}
        {report.isError && <QueryErrorState error={report.error} fallback={t('timeEntries.reportFailed')} onRetry={() => void report.refetch()} />}
        {!privateUnavailable && totals && <>
            <dl className="flex flex-wrap gap-x-6 gap-y-2 text-sm">
                <div><dt className="text-content-secondary">{t('timeEntries.total')}</dt><dd className="font-medium tabular-nums">{value(totals.recorded_minutes)}</dd></div>
                <div><dt className="text-content-secondary">{t('timeEntries.projectMinutes')}</dt><dd className="font-medium tabular-nums">{value(totals.project_work_minutes)}</dd></div>
            </dl>
            <p className="text-sm text-content-secondary">{t('timeEntries.coverage', { recorded: totals.tasks_with_records, total: totals.task_count })}</p>
            {!totals.task_count && <p className="text-sm text-content-secondary">{t('timeEntries.empty')}</p>}
            <div className="overflow-x-auto"><table className="w-full text-left text-sm">
                <caption className="sr-only">{t('timeEntries.report')}</caption>
                <thead><tr className="border-b border-border"><th scope="col" className="p-2">{t('timeEntries.task')}</th><th scope="col" className="p-2"><span className="hidden sm:inline">{t('timeEntries.recorded')}</span><span className="sm:hidden">{t('timeEntries.recordedShort')}</span></th><th scope="col" className="p-2"><span className="hidden sm:inline">{t('timeEntries.estimate')}</span><span className="sm:hidden">{t('timeEntries.estimateShort')}</span></th></tr></thead>
                <tbody>{report.data?.pages.flatMap(page => page.items).map(row => <tr key={row.task_id} className="border-b border-border">
                    <th scope="row" className="max-w-64 break-words p-2 font-medium">#{row.task_id} · {row.task_title ?? t('timeEntries.unavailable')}</th>
                    <td className="p-2 tabular-nums">{value(row.recorded_minutes)}</td><td className="p-2 tabular-nums">{row.estimate_state === 'unavailable' ? t('timeEntries.unavailable') : value(row.estimate_hours, true)}</td>
                </tr>)}</tbody>
            </table></div>
            {report.hasNextPage && <Button type="button" variant="secondary" size="sm" disabled={report.isFetchingNextPage} onClick={() => void report.fetchNextPage()}>{t('timeEntries.moreReport')}</Button>}
        </>}
        <div className="flex flex-wrap gap-2">
            <Button type="button" variant="secondary" size="sm" disabled={download.isPending || privateUnavailable || !totals} onClick={() => download.mutate('totals')}>{t('timeEntries.exportTotals')}</Button>
            {scope === 'mine' && <Button type="button" variant="secondary" size="sm" disabled={download.isPending || privateUnavailable || !totals} onClick={() => download.mutate('entries')}>{t('timeEntries.exportEntries')}</Button>}
        </div>
        {download.isPending && <p role="status">{t('common.loading')}</p>}
        {download.isError && <div role="alert" className="space-y-2 text-sm text-feedback-danger-foreground"><p>{getApiErrorMessage(download.error, t('timeEntries.exportFailed'))}</p>
            <Button type="button" variant="secondary" size="sm" disabled={report.isFetching} onClick={async () => { const result = await report.refetch(); if (!result.isError) download.reset(); }}>{t('timeEntries.reloadEntries')}</Button>
        </div>}
        <TimeEntriesPanel projectId={projectId} start={start} end={end} embedded />
    </section>;
};

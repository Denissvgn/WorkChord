import { useState } from 'react';
import type { ReactNode } from 'react';
import { useQuery } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { Link } from 'react-router-dom';
import { Modal } from '../common/Modal';
import { QueryErrorState } from '../feedback/QueryState';
import { taskService } from '../../services/taskService';
import type { MetricScope, WorkMetricName } from '../../services/taskService';

/**
 * A count that opens the tasks it counts. The server picks them with the same
 * predicate as the count, so the list always has that many tasks.
 */
export const MetricCount = ({ metric, scope, title, children, className }: {
    metric: WorkMetricName; scope: MetricScope | null; title: string; children: ReactNode; className?: string;
}) => {
    const { t } = useTranslation();
    const [open, setOpen] = useState(false);
    // feedback-policy: query loading,error,retry,empty - the dialog keeps explicit loading, retry and empty feedback.
    const matches = useQuery({
        queryKey: ['metric-matches', metric, scope],
        queryFn: ({ signal }) => taskService.metricMatches({ ...scope!, metric }, signal),
        enabled: open && scope !== null,
    });
    if (scope === null) return <span className={className}>{children}</span>;
    return <>
        <button type="button" onClick={() => setOpen(true)} aria-haspopup="dialog"
            className={`rounded underline decoration-dotted underline-offset-4 hover:text-action focus:outline-none focus-visible:ring-2 focus-visible:ring-focus ${className ?? ''}`}>
            {children}
        </button>
        <Modal open={open} title={title} closeLabel={t('actions.close')} onClose={() => setOpen(false)} className="max-w-xl">
            {matches.isLoading && <p role="status">{t('common.loading')}</p>}
            {matches.isError && <QueryErrorState error={matches.error} fallback={t('metricList.loadFailed')} onRetry={() => void matches.refetch()} />}
            {matches.data && <>
                <p className="mb-3 text-sm text-content-secondary" role="status">
                    {matches.data.has_more ? t('metricList.firstItems', { count: matches.data.items.length }) : t('metricList.count', { count: matches.data.items.length })}
                </p>
                {matches.data.items.length === 0 ? <p className="text-sm">{t('metricList.empty')}</p> : (
                    <ul className="max-h-[60vh] divide-y divide-border overflow-y-auto">
                        {matches.data.items.map(item => <li key={item.id} className="flex flex-col py-2">
                            <Link to={`/tasks?task=${item.id}`} className="min-h-9 break-words font-medium text-action hover:underline" onClick={() => setOpen(false)}>
                                #{item.id} · {item.title}
                            </Link>
                            <span className="text-xs text-content-secondary">
                                {t(`statuses.${item.status}`, { defaultValue: item.status })}
                                {item.project_name && ` · ${item.project_name}`}
                                {` · ${item.iteration_name ?? t('teamwork.backlog')}`}
                            </span>
                        </li>)}
                    </ul>
                )}
            </>}
        </Modal>
    </>;
};

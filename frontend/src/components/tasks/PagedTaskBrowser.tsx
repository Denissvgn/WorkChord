import { useLiveWindow } from '../../features/useLiveWindow';
import { LiveWindowStatus } from '../../components/feedback/LiveWindowStatus';
import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { Button } from '../common/Button';
import { QueryErrorState, QueryLoadingState } from '../feedback/QueryState';
import { useSearchParams } from 'react-router-dom';
import { taskService } from '../../services/taskService';

export const PagedTaskBrowser = ({ iterationId }: { iterationId: number }) => {
    const { t } = useTranslation();
    const [query, setQuery] = useState('');
    const [status, setStatus] = useState('');
    const [params, setParams] = useSearchParams();
    // feedback-policy: query loading,error,retry,empty - bounded pages retain explicit recovery and completeness.
    const tasks = useLiveWindow({
        queryKey: ['taskBrowser', iterationId, query, status],
        initialPageParam: 0,
        queryFn: ({ pageParam, signal }) => taskService.lookup({ iteration_id: iterationId, q: query || undefined,
            task_status: status || undefined, after_id: pageParam, limit: 100 }, signal),
        getNextPageParam: page => page.has_more ? page.next_after_id : undefined,
    });
    const items = tasks.isError ? [] : [...new Map(tasks.data?.pages.flatMap(page => page.items)
        .map(item => [item.id, item])).values()];
    return <section className="space-y-4" aria-label={t('pagination.browseTitle')}>
        <h2 className="text-lg font-semibold">{t('pagination.browseTitle')}</h2>
        <p className="text-sm text-content-secondary">{t('pagination.graphLimit')}</p>
        <div className="flex flex-wrap items-end gap-3">
            <label className="min-w-0 flex-1"><span className="field-lbl">{t('pagination.search')}</span>
                <input className="input w-full" value={query} onChange={event => setQuery(event.target.value)} maxLength={200} /></label>
            <label><span className="field-lbl">{t('pagination.status')}</span>
                <select className="input" value={status} onChange={event => setStatus(event.target.value)}>
                    <option value="">{t('pagination.allStatuses')}</option>
                    {['planned', 'active', 'resolved', 'closed'].map(value => <option key={value} value={value}>{t(`statuses.${value}`)}</option>)}
                </select></label>
            <Button variant="secondary" disabled={tasks.isFetching} onClick={() => void tasks.refetch()}>{t('actions.refresh')}</Button>
        </div>
        <p role="status" className="text-sm text-content-secondary">{t(tasks.hasNextPage ? 'pagination.partial' : 'pagination.loaded', { count: items.length })}</p>
        <LiveWindowStatus window={tasks} />
        {tasks.isLoading && <QueryLoadingState />}
        {tasks.isError && <QueryErrorState error={tasks.error} onRetry={() => void tasks.refetch()} />}
        <ul className="divide-y divide-border">{items.map(task => <li key={task.id} className="flex flex-wrap items-center justify-between gap-2 py-2">
            <Button variant="ghost" className="min-w-0 whitespace-normal text-left" aria-current={params.get('task') === String(task.id) ? 'true' : undefined} onClick={() => { const next = new URLSearchParams(params); next.set('task', String(task.id)); setParams(next); }}>#{task.id} · {task.title}</Button>
            <span className="text-sm text-content-secondary">{t(`statuses.${task.status}`)}</span>
        </li>)}</ul>
        {tasks.isSuccess && items.length === 0 && <p>{t('pagination.empty')}</p>}
        {tasks.hasNextPage && <Button variant="secondary" disabled={tasks.isFetchingNextPage} onClick={() => void tasks.fetchNextPage()}>{t('teamwork.loadMore')}</Button>}
    </section>;
};

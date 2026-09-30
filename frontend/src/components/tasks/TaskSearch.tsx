import { useEffect, useId, useState } from 'react';
import { useInfiniteQuery } from '@tanstack/react-query';
import { Link, useSearchParams } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { taskService } from '../../services/taskService';
import { Button } from '../common/Button';
import { QueryErrorState } from '../feedback/QueryState';

export const TaskSearch = () => {
    const { t } = useTranslation();
    const id = useId();
    const [params, setParams] = useSearchParams();
    const text = params.get('q')?.slice(0, 200) ?? '';
    const [query, setQuery] = useState(text);
    useEffect(() => { const timer = setTimeout(() => setQuery(text.trim()), 200); return () => clearTimeout(timer); }, [text]);
    // feedback-policy: query loading,error,retry,empty - scoped results keep explicit loading, retry and empty feedback.
    const results = useInfiniteQuery({ queryKey: ['task-search', query], enabled: query.length > 0,
        initialPageParam: 0, queryFn: ({ pageParam }) => taskService.lookup({ q: query, after_id: pageParam, limit: 20 }),
        getNextPageParam: page => page.has_more ? page.next_after_id : undefined });
    return <section className="space-y-2" aria-labelledby={`${id}-label`}>
        <label id={`${id}-label`} htmlFor={`${id}-search`} className="field-lbl">{t('teamwork.searchTasks')}</label>
        <input id={`${id}-search`} type="search" className="input w-full" value={text} maxLength={200} placeholder={t('teamwork.searchHint')}
            onChange={event => { const next = new URLSearchParams(params); if (event.target.value) next.set('q', event.target.value); else next.delete('q'); setParams(next, { replace: true }); }} />
        {query && <>
            {results.isLoading && <p role="status">{t('common.loading')}</p>}
            {results.isError && <QueryErrorState error={results.error} fallback={t('teamwork.loadFailed')} onRetry={() => void results.refetch()} />}
            {results.isSuccess && results.data.pages.every(page => page.items.length === 0) && <p role="status" className="text-sm text-content-secondary">{t('teamwork.noResults')}</p>}
            <ul className="divide-y divide-border">{results.data?.pages.flatMap(page => page.items).map(task => {
                const next = new URLSearchParams(params); next.set('task', String(task.id));
                return <li key={task.id} className="py-2"><Link className="inline-block min-h-9 break-words font-medium text-action hover:underline" to={`/tasks?${next}`}>#{task.id} · {task.title}</Link>
                    <p className="text-sm text-content-secondary">{task.project_name ?? t('teamwork.workspace')} · {task.iteration_name ?? t('teamwork.backlog')} · {t(`statuses.${task.status}`)}</p></li>;
            })}</ul>
            {results.hasNextPage && <Button size="sm" variant="secondary" disabled={results.isFetchingNextPage} onClick={() => void results.fetchNextPage()}>{t('teamwork.loadMore')}</Button>}
        </>}
    </section>;
};

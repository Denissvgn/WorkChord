import { PageLayout, PageHeader } from '../components/ui';
import { PersonCapacity } from '../components/tasks/PersonCapacity';
import { useIdentity } from '../features/identity/identityContext';
import { useInfiniteQuery, useMutation, useQuery } from '@tanstack/react-query';
import { useSearchParams } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import api from '../services/api';
import { taskService } from '../services/taskService';
import { discussionService } from '../services/discussionService';
import type { TaskReference, TaskReferencePage } from '../types/task';
import { GuardedTaskModal } from '../components/tasks/GuardedTaskModal';
import { Button } from '../components/common/Button';
import { QueryErrorState } from '../components/feedback/QueryState';
import { getApiErrorMessage } from '../utils/apiError';

const QUEUES = ['active', 'queued', 'blocked', 'awaiting_review', 'review', 'inbox'] as const;
type Queue = typeof QUEUES[number];
interface WorkPage { state: string; queues: Record<string, TaskReference[]>; has_more: boolean; next_after_id: number | null }

const MyWorkPage = () => {
    const { t } = useTranslation();
    const identity = useIdentity()?.identity;
    const [params, setParams] = useSearchParams();
    const queue: Queue = QUEUES.includes(params.get('queue') as Queue) ? params.get('queue') as Queue : 'active';
    const selectedId = Number(params.get('task')) || null;
    // feedback-policy: query loading,error,retry,empty - scoped results keep explicit loading, retry and empty feedback.
    const work = useInfiniteQuery({ queryKey: ['human-my-work'], initialPageParam: 0,
        queryFn: async ({ pageParam }) => (await api.get<WorkPage>('/tasks/my-work', { params: { after_id: pageParam } })).data,
        getNextPageParam: page => page.has_more ? page.next_after_id : undefined });
    // feedback-policy: query loading,error,retry,empty - scoped results keep explicit loading, retry and empty feedback.
    const reviews = useInfiniteQuery({ queryKey: ['human-review-queue'], enabled: queue === 'review', initialPageParam: 0,
        queryFn: async ({ pageParam }) => (await api.get<TaskReferencePage>('/tasks/review-queue', { params: { after_id: pageParam } })).data,
        getNextPageParam: page => page.has_more ? page.next_after_id : undefined });
    // feedback-policy: query loading,error,retry,empty - scoped results keep explicit loading, retry and empty feedback.
    const inbox = useInfiniteQuery({ queryKey: ['personal-inbox'], enabled: queue === 'inbox', initialPageParam: 0,
        queryFn: ({ pageParam }) => discussionService.inbox(pageParam), getNextPageParam: page => page.has_more ? page.next_after_id : undefined });
    // feedback-policy: query loading,error,retry,empty - scoped results keep explicit loading, retry and empty feedback.
    const deliveries = useInfiniteQuery({ queryKey: ['personal-deliveries'], enabled: queue === 'inbox', initialPageParam: 0,
        queryFn: ({ pageParam }) => discussionService.deliveries(pageParam), getNextPageParam: page => page.has_more ? page.next_after_id : undefined });
    // feedback-policy: query loading,error,retry,empty - scoped results keep explicit loading, retry and empty feedback.
    const detail = useQuery({ queryKey: ['task', selectedId], enabled: selectedId !== null, queryFn: () => taskService.getById(selectedId!) });
    // feedback-policy: mutation pending,inline - disable repeat writes and retain the draft on failure.
    const read = useMutation({ mutationFn: ({ id, value }: { id: number; value: boolean }) => discussionService.read(id, value), onSuccess: () => inbox.refetch() });
    // feedback-policy: mutation pending,inline - disable repeat writes and retain the draft on failure.
    const retry = useMutation({ mutationFn: discussionService.retry, onSuccess: () => deliveries.refetch() });
    const selectedQuery = queue === 'inbox' ? inbox : queue === 'review' ? reviews : work;
    const items = queue === 'review' ? reviews.data?.pages.flatMap(page => page.items) ?? [] : work.data?.pages.flatMap(page => page.queues[queue] ?? []) ?? [];
    const selectTask = (id: number | null) => { const next = new URLSearchParams(params); if (id) next.set('task', String(id)); else next.delete('task'); setParams(next); };

    return <PageLayout><PageHeader title={t('teamwork.myWork')} subtitle={t('teamwork.myWorkHelp')} /><section className="space-y-5">
        {identity?.profile && <PersonCapacity key={identity.profile.id} profileId={identity.profile.id} manage />}
        <nav aria-label={t('teamwork.workQueues')} className="flex flex-wrap gap-2">{QUEUES.map(key => <Button key={key} variant={queue === key ? 'primary' : 'secondary'} size="sm" aria-pressed={queue === key}
            onClick={() => { const next = new URLSearchParams(params); next.set('queue', key); next.delete('task'); setParams(next); }}>{t(`teamwork.queue_${key}`)}</Button>)}</nav>
        {selectedQuery.isLoading && <p role="status">{t('common.loading')}</p>}
        {selectedQuery.isError && <QueryErrorState error={selectedQuery.error} fallback={t('teamwork.loadFailed')} onRetry={() => void selectedQuery.refetch()} />}
        {queue !== 'review' && queue !== 'inbox' && work.data?.pages[0].state !== 'ready' && work.data && <p className="rounded-md border border-border p-4 text-sm">{t(`teamwork.state_${work.data.pages[0].state}`)}</p>}
        {queue !== 'inbox' && <ul className="divide-y divide-border">{items.map(task => <li key={task.id} className="flex flex-col gap-1 py-3">
            <button type="button" className="min-h-9 break-words text-left font-medium text-action hover:underline" onClick={() => selectTask(task.id)}>#{task.id} · {task.title}</button>
            <p className="text-sm text-content-secondary">{task.project_name ?? t('teamwork.workspace')} · {task.iteration_name ?? t('teamwork.backlog')} · {task.status === 'closed' && task.acceptance_current === false ? t('teamwork.acceptanceNeedsReview') : t(`statuses.${task.status}`)}</p>
            {task.blocked_reason && <p className="text-sm text-feedback-warning-foreground">{task.blocked_reason}</p>}
        </li>)}</ul>}
        {queue !== 'inbox' && selectedQuery.isSuccess && items.length === 0 && <p className="text-sm text-content-secondary">{t('teamwork.emptyQueue')}</p>}
        {queue === 'inbox' && <>
            <ul className="divide-y divide-border">{inbox.data?.pages.flatMap(page => page.items).map(item => <li key={item.id} className="flex flex-wrap items-center justify-between gap-2 py-3">
                <div className="min-w-0"><button type="button" className="min-h-9 break-words text-left font-medium text-action hover:underline" onClick={() => selectTask(item.task_id)}>{item.title}</button>
                    <p className="text-sm text-content-secondary">{t(`teamwork.event_${item.event_type}`)} · {t(item.read ? 'teamwork.read' : 'teamwork.unread')}</p></div>
                <Button size="sm" variant="ghost" disabled={read.isPending} onClick={() => read.mutate({ id: item.id, value: !item.read })}>{t(item.read ? 'teamwork.markUnread' : 'teamwork.markRead')}</Button>
            </li>)}</ul>
            {inbox.data?.pages.every(page => page.items.length === 0) && <p>{t('teamwork.emptyInbox')}</p>}
            <details className="rounded-md border border-border p-3"><summary className="cursor-pointer font-medium">{t('teamwork.deliveryStatus')}</summary>
                {deliveries.isLoading && <p role="status">{t('common.loading')}</p>}
                {deliveries.isError && <QueryErrorState error={deliveries.error} fallback={t('teamwork.loadFailed')} onRetry={() => void deliveries.refetch()} />}
                {deliveries.data?.pages.flatMap(page => page.items).map(item => <div key={item.id} className="flex flex-wrap items-center gap-2 py-2 text-sm"><span>{item.title} · {t(`teamwork.delivery_${item.status}`)} · {item.attempt_count}/{item.max_attempts}</span>
                    {item.status === 'failed' && <Button size="sm" variant="secondary" disabled={retry.isPending} onClick={() => retry.mutate(item.id)}>{t('teamwork.retry')}</Button>}</div>)}
                {deliveries.hasNextPage && <Button size="sm" variant="ghost" disabled={deliveries.isFetchingNextPage} onClick={() => void deliveries.fetchNextPage()}>{t('teamwork.loadMore')}</Button>}
            </details>
            {(read.isError || retry.isError) && <p role="alert" className="text-sm text-feedback-danger-foreground">{getApiErrorMessage(read.error ?? retry.error, t('teamwork.saveFailed'))}</p>}
        </>}
        {selectedQuery.hasNextPage && <Button variant="secondary" disabled={selectedQuery.isFetchingNextPage} onClick={() => void selectedQuery.fetchNextPage()}>{t('teamwork.loadMore')}</Button>}
        {selectedId && detail.isLoading && <p role="status">{t('common.loading')}</p>}
        {selectedId && detail.isError && <div><QueryErrorState error={detail.error} fallback={t('teamwork.taskUnavailable')} onRetry={() => void detail.refetch()} /><Button variant="ghost" onClick={() => selectTask(null)}>{t('actions.close')}</Button></div>}
        {selectedId && detail.data && <GuardedTaskModal key={detail.data.id} title={detail.data.title} closeLabel={t('actions.close')} iterationId={detail.data.iteration_id} initialData={detail.data}
            onClose={() => { selectTask(null); void work.refetch(); void reviews.refetch(); }} />}
    </section></PageLayout>;
};

export default MyWorkPage;

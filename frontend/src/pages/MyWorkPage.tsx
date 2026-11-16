import { useCallback, useMemo } from 'react';
import { useLiveWindow } from '../features/useLiveWindow';
import { LiveWindowStatus } from '../components/feedback/LiveWindowStatus';
import { PageLayout, PageHeader, PageToolbar, ViewSwitch } from '../components/ui';
import { PersonCapacity } from '../components/tasks/PersonCapacity';
import { useIdentity } from '../features/identity/identityContext';
import { LocalProfilePicker } from '../features/identity/LocalProfilePicker';
import { NotificationsPanel } from '../components/notifications/NotificationsPanel';
import { useIterationStore } from '../store/iterationStore';
import { useMutation } from '@tanstack/react-query';
import { useSearchParams } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import api from '../services/api';
import { discussionService } from '../services/discussionService';
import type { TaskReference, TaskReferencePage } from '../types/task';
import { TaskEditorDrawer } from '../components/tasks/TaskEditorDrawer';
import { TaskRow } from '../components/tasks/TaskRow';
import { TaskSelectionBar } from '../components/tasks/TaskSelectionBar';
import { getEffectiveEffort } from '../components/tasks/taskRowValues';
import { useTaskRowEdits } from '../components/tasks/useTaskRowEdits';
import { useIterationRowData } from '../components/tasks/useIterationRowData';
import { useTaskSelection } from '../components/tasks/useTaskSelection';
import { agentRowValues, useAgentRowFacts } from '../components/tasks/useAgentRowFacts';
import { taskStateChip } from '../components/tasks/taskStateChip';
import type { TaskStateChip } from '../components/tasks/taskStateChip';
import { Button } from '../components/common/Button';
import { QueryErrorState } from '../components/feedback/QueryState';
import { getApiErrorMessage } from '../utils/apiError';

const QUEUES = ['active', 'queued', 'blocked', 'awaiting_review', 'review', 'inbox'] as const;
const WORK_QUEUES: readonly string[] = ['active', 'queued', 'blocked', 'awaiting_review'];
type Queue = typeof QUEUES[number];
interface WorkPage { state: string; queues: Record<string, TaskReference[]>; has_more: boolean; next_after_id: number | null }

const MyWorkPage = () => {
    const { t } = useTranslation();
    const identityContext = useIdentity();
    const identity = identityContext?.identity;
    const local = identity?.mode === 'trusted_local' && !identity.principal;
    const { selectedIterationId } = useIterationStore();
    const [params, setParams] = useSearchParams();
    const queue: Queue = QUEUES.includes(params.get('queue') as Queue) ? params.get('queue') as Queue : 'active';
    const selectedId = Number(params.get('task')) || null;
    // feedback-policy: query loading,error,retry,empty - scoped results keep explicit loading, retry and empty feedback.
    const work = useLiveWindow({ queryKey: ['human-my-work'], enabled: !local || !!identity?.profile, initialPageParam: 0,
        queryFn: async ({ pageParam }) => (await api.get<WorkPage>('/tasks/my-work', { params: { after_id: pageParam } })).data,
        getNextPageParam: page => page.has_more ? page.next_after_id : undefined });
    // feedback-policy: query loading,error,retry,empty - scoped results keep explicit loading, retry and empty feedback.
    const reviews = useLiveWindow({ queryKey: ['human-review-queue'], enabled: !local || !!identity?.profile, initialPageParam: 0,
        queryFn: async ({ pageParam }) => (await api.get<TaskReferencePage>('/tasks/review-queue', { params: { after_id: pageParam } })).data,
        getNextPageParam: page => page.has_more ? page.next_after_id : undefined });
    // feedback-policy: query loading,error,retry,empty - scoped results keep explicit loading, retry and empty feedback.
    const inbox = useLiveWindow({ queryKey: ['personal-inbox'], enabled: !local || !!identity?.profile, initialPageParam: 0,
        queryFn: ({ pageParam }) => discussionService.inbox(pageParam), getNextPageParam: page => page.has_more ? page.next_after_id : undefined });
    // feedback-policy: query loading,error,retry,empty - scoped results keep explicit loading, retry and empty feedback.
    const deliveries = useLiveWindow({ queryKey: ['personal-deliveries'], enabled: !local || !!identity?.profile, initialPageParam: 0,
        queryFn: ({ pageParam }) => discussionService.deliveries(pageParam), getNextPageParam: page => page.has_more ? page.next_after_id : undefined });
    // feedback-policy: mutation pending,inline - disable repeat writes and retain the draft on failure.
    const read = useMutation({ mutationFn: ({ id, value }: { id: number; value: boolean }) => discussionService.read(id, value), onSuccess: () => inbox.refetch() });
    // feedback-policy: mutation pending,inline - disable repeat writes and retain the draft on failure.
    const retry = useMutation({ mutationFn: discussionService.retry, onSuccess: () => deliveries.refetch() });
    const selectedQuery = queue === 'inbox' ? inbox : queue === 'review' ? reviews : work;
    const reviewPages = reviews.data?.pages;
    const workPages = work.data?.pages;
    const items = useMemo(
        () => queue === 'review' ? reviewPages?.flatMap(page => page.items) ?? [] : workPages?.flatMap(page => page.queues[queue] ?? []) ?? [],
        [queue, reviewPages, workPages],
    );
    const workState = work.data?.pages[0].state;
    const workQueue = WORK_QUEUES.includes(queue);
    const queueLabel = (key: Queue) => {
        const source = key === 'review' ? reviews : key === 'inbox' ? inbox : work;
        const pages = source.data?.pages;
        const count = !pages ? null : key === 'review' || key === 'inbox'
            ? pages.reduce((total, page) => total + ('items' in page ? page.items.length : 0), 0)
            : pages.reduce((total, page) => total + ('queues' in page ? (page.queues[key]?.length ?? 0) : 0), 0);
        return `${t(`teamwork.queue_${key}`)} · ${count === null ? '…' : `${count}${source.hasNextPage ? '+' : ''}`}`;
    };
    const rowEdits = useTaskRowEdits();
    // A task reference carries no priority, assignee or effort; those come from the iteration's tasks, as in the Tasks list.
    const rowData = useIterationRowData(items.map(task => task.iteration_id));
    // My Work already names the reviewer of each submitted task it returns; the review queue does not, so those are read per task.
    const knownReviewers = useMemo(() => workQueue
        ? new Map(items.filter(item => item.status === 'resolved').map(item => [item.id, item.reviewer_name ?? null] as const))
        : undefined, [workQueue, items]);
    const agentFacts = useAgentRowFacts(items, knownReviewers);
    const leaves = useMemo(() => items.flatMap(item => {
        const full = rowData.tasksById.get(item.id);
        return full && item.iteration_id !== null && !full.is_composite && (full.children?.length ?? 0) === 0 ? [full] : [];
    }), [items, rowData.tasksById]);
    const selectableIds = useMemo(() => new Set(leaves.map(task => task.id)), [leaves]);
    const order = useMemo(() => leaves.map(task => task.id), [leaves]);
    const iterationOf = useCallback((id: number) => rowData.tasksById.get(id)?.iteration_id, [rowData.tasksById]);
    const selection = useTaskSelection({ selectableIds, order, iterationOf });
    const selectedTasks = useMemo(() => leaves.filter(task => selection.selectedIds.has(task.id)), [leaves, selection.selectedIds]);
    const scopeIterationId = selectedTasks[0]?.iteration_id ?? null;
    const selectTask = (id: number | null) => { const next = new URLSearchParams(params); if (id) next.set('task', String(id)); else next.delete('task'); setParams(next); };

    if (local && !identity?.profile) return <PageLayout><PageHeader title={t('teamwork.myWork')} purpose={t('teamwork.myWorkHelp')} />
        <section aria-labelledby="my-work-profile" className="max-w-xl space-y-2">
            <h2 id="my-work-profile" className="text-base font-semibold">{t('identity.localProfileTitle')}</h2>
            <LocalProfilePicker current={null} onChosen={() => identityContext?.refresh()} />
        </section></PageLayout>;

    return <PageLayout><PageHeader title={t('teamwork.myWork')} purpose={t('teamwork.myWorkHelp')} />
        <PageToolbar label={t('teamwork.workQueues')} viewSwitch={<ViewSwitch<Queue> label={t('teamwork.workQueues')}
            options={QUEUES.map(key => ({ value: key, label: queueLabel(key) }))} value={queue}
            onChange={key => { const next = new URLSearchParams(params); next.set('queue', key); next.delete('task'); setParams(next); }} />} />
        <section className="space-y-5">
        {local && identity?.profile && <p className="text-sm text-content-secondary">{t('identity.workingAsLocal', { name: identity.profile.display_name })}</p>}
        {identity?.profile && <PersonCapacity key={identity.profile.id} profileId={identity.profile.id} manage />}
        <LiveWindowStatus window={selectedQuery} />
        {selectedQuery.isLoading && <p role="status">{t('common.loading')}</p>}
        {selectedQuery.isError && <QueryErrorState error={selectedQuery.error} fallback={t('teamwork.loadFailed')} onRetry={() => void selectedQuery.refetch()} />}
        {workQueue && workState && workState !== 'ready' && <p className="rounded-md border border-border p-4 text-sm">{t(`teamwork.state_${workState}`)}</p>}
        {queue !== 'inbox' && rowData.error && <QueryErrorState error={rowData.error} fallback={t('queryFeedback.optionLoadFailed')} onRetry={rowData.refetch} />}
        {queue !== 'inbox' && scopeIterationId !== null && <TaskSelectionBar iterationId={scopeIterationId} selectedTasks={selectedTasks}
            matchingCount={selection.matchingIds.length} onSelectAll={selection.selectAll} onClearSelection={selection.clear} />}
        {queue !== 'inbox' && items.length > 0 && <ul className="rounded-lg border border-border bg-surface-card">{items.map(task => {
            const full = rowData.tasksById.get(task.id);
            const canPick = selectableIds.has(task.id);
            const assigneeOptions = rowData.optionsByIteration.get(task.iteration_id ?? -1);
            const agentRow = agentRowValues(full ?? task, assigneeOptions, agentFacts);
            // The same chip as the Tasks list once the iteration's tasks load; until then only what the reference says.
            const chip: TaskStateChip | null = full ? taskStateChip(full, rowData.tasksById)
                : task.blocked_reason ? { kind: 'blocked' } : task.status === 'resolved' ? { kind: 'inReview' } : null;
            return <li key={task.id}>
                <TaskRow id={task.id} title={task.title} titleText={`#${task.id} · ${task.title}`} status={task.status}
                    statusLocked={full ? full.is_composite || (full.children?.length ?? 0) > 0 : false}
                    priority={full?.priority}
                    chip={chip}
                    meta={[task.project_name ?? t('teamwork.workspace'), task.iteration_name ?? t('teamwork.backlog'),
                        task.status === 'closed' && task.acceptance_current === false ? t('teamwork.acceptanceNeedsReview') : null, task.blocked_reason].filter(Boolean).join(' · ')}
                    assignee={full ? full.assignee ?? null : undefined}
                    assigneeOptions={assigneeOptions}
                    dispatch={agentRow.dispatch}
                    reviewer={agentRow.reviewer}
                    onAssign={full && task.iteration_id !== null ? assigneeId => rowEdits.assign(task, assigneeId) : undefined}
                    effort={full ? getEffectiveEffort(full) : undefined}
                    overdue={full?.is_overdue}
                    onOpen={() => selectTask(task.id)}
                    onStatusChange={status => rowEdits.changeStatus(task, status)}
                    menuItems={[{ label: t('taskList.openTask'), onSelect: () => selectTask(task.id) }]}
                    selected={selection.selectedIds.has(task.id)}
                    selectionActive={selection.selectionActive}
                    onToggleSelect={canPick ? ({ shiftKey }) => selection.toggle(task.id, shiftKey) : undefined}
                    selectDisabledReason={canPick && !selection.canAdd(task.id) ? t('taskList.selectOneIteration') : undefined} />
            </li>;
        })}</ul>}
        {queue !== 'inbox' && selectedQuery.isSuccess && items.length === 0 && !(workQueue && workState !== 'ready') && <p className="text-sm text-content-secondary">{t('teamwork.emptyQueue')}</p>}
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
            {/* Iteration notifications (status changes and overdue work) live with the personal inbox. */}
            {selectedIterationId > 0 && <details className="rounded-md border border-border p-3"><summary className="cursor-pointer font-medium">{t('teamwork.iterationNotifications')}</summary>
                <NotificationsPanel iterationId={selectedIterationId} className="mt-3 w-full border-0" /></details>}
            {(read.isError || retry.isError) && <p role="alert" className="text-sm text-feedback-danger-foreground">{getApiErrorMessage(read.error ?? retry.error, t('teamwork.saveFailed'))}</p>}
        </>}
        {selectedQuery.hasNextPage && <Button variant="secondary" disabled={selectedQuery.isFetchingNextPage} onClick={() => void selectedQuery.fetchNextPage()}>{t('teamwork.loadMore')}</Button>}
        {selectedId && <TaskEditorDrawer key={selectedId} taskId={selectedId} open title={task => task?.title ?? t('taskEditor.editTask')}
            onClose={() => { selectTask(null); if (queue === 'review') void reviews.refetch(); else if (queue === 'inbox') void inbox.refetch(); else void work.refetch(); }} />}
    </section></PageLayout>;
};

export default MyWorkPage;

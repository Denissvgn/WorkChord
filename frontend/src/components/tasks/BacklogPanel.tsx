import { useLiveWindow } from '../../features/useLiveWindow';
import { LiveWindowStatus } from '../../components/feedback/LiveWindowStatus';
import { useId, useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Link, useSearchParams } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { taskService } from '../../services/taskService';
import { projectService } from '../../services/projectService';
import { Button } from '../common/Button';
import { QueryErrorState } from '../feedback/QueryState';
import { GuardedTaskModal } from './GuardedTaskModal';

export const BacklogPanel = () => {
    const { t } = useTranslation();
    const id = useId();
    const [params, setParams] = useSearchParams();
    const projectId = Number(params.get('backlogProject')) || null;
    const [creating, setCreating] = useState(false);
    // feedback-policy: query loading,error,retry,empty - scoped results keep explicit loading, retry and empty feedback.
    const projects = useQuery({ queryKey: ['projects'], queryFn: projectService.getAll });
    // feedback-policy: query loading,error,retry,empty - scoped results keep explicit loading, retry and empty feedback.
    const tasks = useLiveWindow({ queryKey: ['backlog', projectId], initialPageParam: 0,
        queryFn: ({ pageParam }) => taskService.lookup({ project_id: projectId ?? undefined, backlog_only: true, after_id: pageParam }),
        getNextPageParam: page => page.has_more ? page.next_after_id : undefined });
    return <section className="space-y-3" aria-labelledby={`${id}-title`}>
        <h2 id={`${id}-title`} className="text-lg font-semibold">{t('teamwork.projectBacklog')}</h2>
        <div className="flex flex-wrap items-end gap-3"><div className="min-w-0 flex-1"><label className="field-lbl" htmlFor={`${id}-project`}>{t('teamwork.project')}</label>
            <select id={`${id}-project`} className="input w-full" value={projectId ?? ''} onChange={event => { const next = new URLSearchParams(params); if (event.target.value) next.set('backlogProject', event.target.value); else next.delete('backlogProject'); setParams(next); }}>
                <option value="">{t('teamwork.allProjects')}</option>{projects.data?.map(project => <option key={project.id} value={project.id}>{project.name}</option>)}
            </select></div><Button disabled={!projectId || !projects.data?.some(project => project.id === projectId)} onClick={() => setCreating(true)}>{t('teamwork.captureTask')}</Button></div>
        {!projectId && <p className="text-sm text-content-secondary">{t('teamwork.chooseProject')}</p>}
        {projects.isLoading && <p role="status">{t('common.loading')}</p>}
        {projects.isError && <QueryErrorState error={projects.error} fallback={t('teamwork.loadFailed')} onRetry={() => void projects.refetch()} />}
        <LiveWindowStatus window={tasks} />
        {tasks.isLoading && <p role="status">{t('common.loading')}</p>}
        {tasks.isError && <QueryErrorState error={tasks.error} fallback={t('teamwork.loadFailed')} onRetry={() => void tasks.refetch()} />}
        <ul className="divide-y divide-border">{tasks.data?.pages.flatMap(page => page.items).map(task => {
            const next = new URLSearchParams(params); next.set('task', String(task.id));
            return <li key={task.id} className="py-2"><Link className="inline-block min-h-9 break-words font-medium text-action hover:underline" to={`/tasks?${next}`}>#{task.id} · {task.title}</Link><p className="text-sm text-content-secondary">{task.project_name} · {t(`statuses.${task.status}`)}</p></li>;
        })}</ul>
        {tasks.isSuccess && tasks.data.pages.every(page => page.items.length === 0) && <p className="text-sm text-content-secondary">{t('teamwork.emptyBacklog')}</p>}
        {tasks.hasNextPage && <Button variant="secondary" disabled={tasks.isFetchingNextPage} onClick={() => void tasks.fetchNextPage()}>{t('teamwork.loadMore')}</Button>}
        {creating && projectId && <GuardedTaskModal title={t('teamwork.captureTask')} closeLabel={t('actions.close')} iterationId={null} parentProjectId={projectId}
            onClose={() => { setCreating(false); void tasks.refetch(); }} />}
    </section>;
};

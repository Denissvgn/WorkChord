import { useEffect, useId, useState } from 'react';
import { useMutation, useQuery } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import api from '../../services/api';
import { taskService } from '../../services/taskService';
import { projectService } from '../../services/projectService';
import type { Task } from '../../types/task';
import { Button } from '../common/Button';
import { QueryErrorState } from '../feedback/QueryState';
import { getApiErrorMessage } from '../../utils/apiError';

interface Dependency { id: number; kind: 'task' | 'milestone'; target_id?: number; title?: string; ready: boolean; reason: string | null }

export const DeliveryDependencies = ({ task, disabled, onPending, onUpdated }: { task: Task; disabled: boolean; onPending: (pending: boolean) => void; onUpdated: (task: Task) => void }) => {
    const { t } = useTranslation();
    const id = useId();
    const [expanded, setExpanded] = useState(false);
    const [kind, setKind] = useState<'task' | 'milestone'>('task');
    const [text, setText] = useState('');
    const [projectId, setProjectId] = useState<number | null>(task.project_id ?? null);
    const [targetId, setTargetId] = useState<number | null>(null);
    // feedback-policy: query loading,error,retry,empty - scoped results keep explicit loading, retry and empty feedback.
    const edges = useQuery({ queryKey: ['delivery-dependencies', task.id, task.version], enabled: expanded, queryFn: async () => (await api.get<Dependency[]>(`/tasks/${task.id}/delivery-dependencies`)).data });
    // feedback-policy: query loading,error,retry,empty - scoped results keep explicit loading, retry and empty feedback.
    const tasks = useQuery({ queryKey: ['dependency-task-search', text], enabled: expanded && kind === 'task' && text.trim().length > 0,
        queryFn: () => taskService.lookup({ q: text, limit: 20 }) });
    // feedback-policy: query loading,error,retry,empty - scoped results keep explicit loading, retry and empty feedback.
    const projects = useQuery({ queryKey: ['projects'], enabled: expanded && kind === 'milestone', queryFn: projectService.getAll });
    // feedback-policy: query loading,error,retry,empty - scoped results keep explicit loading, retry and empty feedback.
    const milestones = useQuery({ queryKey: ['projectMilestones', projectId], enabled: expanded && kind === 'milestone' && projectId !== null,
        queryFn: () => projectService.getMilestones(projectId!) });
    // feedback-policy: mutation pending,inline - disable repeat writes and retain the draft on failure.
    const mutation = useMutation({ mutationFn: async (remove?: number) => {
        if (remove) await api.delete(`/tasks/${task.id}/delivery-dependencies/${remove}`, { params: { expected_version: task.version } });
        else await api.post(`/tasks/${task.id}/delivery-dependencies`, { kind, target_id: targetId, expected_version: task.version });
        return taskService.getById(task.id);
    }, onSuccess: async latest => { setTargetId(null); setText(''); await edges.refetch(); onUpdated(latest); } });
    useEffect(() => onPending(mutation.isPending), [mutation.isPending, onPending]);
    return <details className="space-y-3 rounded-md border border-border p-3" onToggle={event => setExpanded(event.currentTarget.open)}>
        <summary className="cursor-pointer font-medium">{t('teamwork.deliveryDependencies')}</summary>
        <p className="text-sm text-content-secondary">{t('teamwork.dependenciesHelp')}</p>
        {edges.isLoading && <p role="status">{t('common.loading')}</p>}
        {edges.isError && <QueryErrorState error={edges.error} fallback={t('teamwork.loadFailed')} onRetry={() => void edges.refetch()} />}
        <ul className="space-y-2">{edges.data?.map(edge => <li key={edge.id} className="flex flex-wrap items-center justify-between gap-2 text-sm">
            <span>{edge.title ?? t('teamwork.taskUnavailable')} · {t(edge.ready ? 'teamwork.prerequisiteReady' : 'teamwork.prerequisiteWaiting')}</span>
            <Button type="button" variant="ghost" size="sm" disabled={disabled} onClick={() => mutation.mutate(edge.id)}>{t('teamwork.unlink')}</Button>
        </li>)}</ul>
        <fieldset disabled={disabled} className="space-y-2"><legend className="text-sm font-medium">{t('teamwork.addPrerequisite')}</legend>
            <label className="field-lbl" htmlFor={`${id}-kind`}>{t('teamwork.prerequisiteType')}</label>
            <select id={`${id}-kind`} className="input w-full" value={kind} onChange={event => { setKind(event.target.value as 'task' | 'milestone'); setTargetId(null); }}><option value="task">{t('teamwork.task')}</option><option value="milestone">{t('teamwork.milestone')}</option></select>
            {kind === 'task' ? <><label className="field-lbl" htmlFor={`${id}-search`}>{t('teamwork.searchTasks')}</label><input id={`${id}-search`} className="input w-full" value={text} maxLength={200} onChange={event => { setText(event.target.value); setTargetId(null); }} />
                {tasks.isLoading && <p role="status">{t('common.loading')}</p>}
                {tasks.isSuccess && tasks.data.items.length === 0 && <p>{t('teamwork.noResults')}</p>}
                {tasks.isError && <QueryErrorState error={tasks.error} fallback={t('teamwork.loadFailed')} onRetry={() => void tasks.refetch()} />}
                <label className="field-lbl" htmlFor={`${id}-target`}>{t('teamwork.prerequisite')}</label><select id={`${id}-target`} className="input w-full" value={targetId ?? ''} onChange={event => setTargetId(Number(event.target.value) || null)}><option value="">{t('teamwork.chooseTask')}</option>{tasks.data?.items.filter(item => item.id !== task.id).map(item => <option key={item.id} value={item.id}>#{item.id} · {item.title}</option>)}</select></>
                : <><label className="field-lbl" htmlFor={`${id}-project`}>{t('teamwork.project')}</label><select id={`${id}-project`} className="input w-full" value={projectId ?? ''} onChange={event => { setProjectId(Number(event.target.value) || null); setTargetId(null); }}><option value="">{t('teamwork.chooseProject')}</option>{projects.data?.map(item => <option key={item.id} value={item.id}>{item.name}</option>)}</select>
                    {(projects.isLoading || milestones.isLoading) && <p role="status">{t('common.loading')}</p>}
                    {milestones.isSuccess && milestones.data.length === 0 && <p>{t('teamwork.noResults')}</p>}
                    {(projects.isError || milestones.isError) && <QueryErrorState error={projects.error ?? milestones.error} fallback={t('teamwork.loadFailed')} onRetry={() => { void projects.refetch(); void milestones.refetch(); }} />}
                    <label className="field-lbl" htmlFor={`${id}-milestone`}>{t('teamwork.milestone')}</label><select id={`${id}-milestone`} className="input w-full" value={targetId ?? ''} onChange={event => setTargetId(Number(event.target.value) || null)}><option value="">{t('teamwork.chooseMilestone')}</option>{milestones.data?.map(item => <option key={item.id} value={item.id}>{item.name}</option>)}</select></>}
            <Button type="button" size="sm" disabled={!targetId || disabled} isLoading={mutation.isPending} onClick={() => mutation.mutate(undefined)}>{t('teamwork.addPrerequisite')}</Button>
        </fieldset>
        {mutation.isError && <p role="alert" className="text-sm text-feedback-danger-foreground">{getApiErrorMessage(mutation.error, t('teamwork.saveFailed'))}</p>}
    </details>;
};

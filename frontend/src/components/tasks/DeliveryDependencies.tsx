import { useEffect, useId, useRef, useState } from 'react';
import { useMutation, useQuery } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import api from '../../services/api';
import { taskService } from '../../services/taskService';
import { projectService } from '../../services/projectService';
import { githubService } from '../../services/githubService';
import type { Task } from '../../types/task';
import type { DeliveryPrerequisite } from '../../types/github';
import { Button } from '../common/Button';
import { QueryErrorState } from '../feedback/QueryState';
import { getApiErrorMessage, getApiErrorStatus } from '../../utils/apiError';
import type { MutationFeedbackMeta } from '../../features/mutationFeedback';
import { useTaskViewSession, type TaskViewSession, type TaskViewSessionUpdate } from './taskViewSession';
import { PREREQUISITE_RETARGET_FEATURE, useProjectEditAccess } from '../../features/identity/useProjectEditAccess';

import { Select } from '../../components/common/Select';

type Dependency = DeliveryPrerequisite;
const HOLD_CASES = ['not_accepted', 'open_pull_request', 'merged_on_other_branch', 'merge_branch_unknown', 'closed_unmerged', 'not_observed'];
const HOLD_OWNERS = ['pm', 'worker', 'reviewer'];

interface BranchDraft { edge: number; draft: string; base: string }
const readBranchDraft = (key: string | null): BranchDraft | null => {
    try {
        const value = JSON.parse(key ? sessionStorage.getItem(key) ?? 'null' : 'null');
        if (!value || typeof value.savedAt !== 'number' || Date.now() - value.savedAt < 0 || Date.now() - value.savedAt >= 86400000
            || !Number.isSafeInteger(value.edge) || value.edge < 1 || typeof value.draft !== 'string' || value.draft.length > 255
            || typeof value.base !== 'string' || value.base.length > 255) return null;
        return { edge: value.edge, draft: value.draft, base: value.base };
    } catch { return null; }
};

const BranchLine = ({ edge }: { edge: Dependency }) => {
    const { t } = useTranslation();
    if (edge.kind !== 'task') return null;
    return <p className="text-xs text-content-secondary">
        {edge.target_branch ? <>{t('teamwork.branchRequired')} <code className="font-mono">{edge.target_branch}</code></> : t('teamwork.branchNone')}
    </p>;
};

const Hold = ({ edge }: { edge: Dependency }) => {
    const { t } = useTranslation();
    if (!edge.hold) return null;
    const label = HOLD_CASES.includes(edge.hold.case) ? t(`teamwork.holdCase_${edge.hold.case}`) : edge.hold.case;
    const owner = HOLD_OWNERS.includes(edge.hold.next_owner) ? t(`teamwork.ghOwner_${edge.hold.next_owner}`) : edge.hold.next_owner;
    return <div className="rounded-md bg-surface-muted px-3 py-2 text-sm">
        <p className="font-medium">{label}</p>
        <p>{t('teamwork.ghNext', { owner })} {edge.hold.next_action}</p>
    </div>;
};

const ignoreDirty = () => undefined;

/** Without a held session or draft scope (the full form), the list keeps its own state and does not persist drafts. */
export const DeliveryDependencies = ({ task, disabled, draftKey = null, session: heldSession, onSession: onHeldSession, onDirty = ignoreDirty, onPending, onUpdated }: {
    task: Task; disabled: boolean; draftKey?: string | null; session?: TaskViewSession; onSession?: TaskViewSessionUpdate;
    onDirty?: (dirty: boolean) => void; onPending: (pending: boolean) => void; onUpdated: (task: Task) => void;
}) => {
    const [ownSession, ownUpdate] = useTaskViewSession(null);
    const session = heldSession ?? ownSession;
    const onSession = onHeldSession ?? ownUpdate;
    const { t } = useTranslation();
    const id = useId();
    const storageKey = draftKey ? `${draftKey}:prerequisite-branch` : null;
    const sessionOpen = session.prerequisitesOpen;
    const conflict = session.branchConflict;
    const setExpanded = (open: boolean) => onSession({ prerequisitesOpen: open });
    const setConflict = (next: boolean) => onSession({ branchConflict: next });
    const [draft, setEditing] = useState<BranchDraft | null>(() => readBranchDraft(storageKey));
    const expanded = sessionOpen || draft !== null;
    const [kind, setKind] = useState<'task' | 'milestone'>('task');
    const [text, setText] = useState('');
    const [projectId, setProjectId] = useState<number | null>(task.project_id ?? null);
    const [targetId, setTargetId] = useState<number | null>(null);
    const [branch, setBranch] = useState('');
    const { canEdit, features } = useProjectEditAccess(task.project_id);
    const canRetarget = canEdit && features.includes(PREREQUISITE_RETARGET_FEATURE);
    const branchInput = useRef<HTMLInputElement>(null);
    const editingEdge = draft?.edge;
    // Opening the form moves the keyboard to its field; closing it returns focus to the page by unmounting.
    useEffect(() => { if (editingEdge !== undefined) branchInput.current?.focus(); }, [editingEdge]);
    // feedback-policy: query loading,error,retry,empty - scoped results keep explicit loading, retry and empty feedback.
    const edges = useQuery({ queryKey: ['delivery-dependencies', task.id, task.version], enabled: expanded, queryFn: async () => (await api.get<Dependency[]>(`/tasks/${task.id}/delivery-dependencies`)).data });
    // A restored draft for a prerequisite that no longer exists is dropped rather than shown or counted as unsaved.
    const editing = draft && !(edges.isSuccess && !edges.data.some(item => item.id === draft.edge)) ? draft : null;
    const dirty = editing !== null && editing.draft !== editing.base;
    useEffect(() => {
        onDirty(dirty);
        if (!storageKey) return;
        try {
            if (dirty && editing) sessionStorage.setItem(storageKey, JSON.stringify({ ...editing, savedAt: Date.now() }));
            else sessionStorage.removeItem(storageKey);
        } catch { /* The draft stays in memory when storage is unavailable. */ }
    }, [dirty, editing, onDirty, storageKey]);
    useEffect(() => () => onDirty(false), [onDirty]);
    // feedback-policy: query loading,error,retry,empty - scoped results keep explicit loading, retry and empty feedback.
    const tasks = useQuery({ queryKey: ['dependency-task-search', text], enabled: expanded && kind === 'task' && text.trim().length > 0,
        queryFn: () => taskService.lookup({ q: text, limit: 20 }) });
    // feedback-policy: query loading,error,retry,empty - scoped results keep explicit loading, retry and empty feedback.
    const projects = useQuery({ queryKey: ['projects'], enabled: expanded && kind === 'milestone', queryFn: projectService.getAll });
    // feedback-policy: query loading,error,retry,empty - scoped results keep explicit loading, retry and empty feedback.
    const milestones = useQuery({ queryKey: ['projectMilestones', projectId], enabled: expanded && kind === 'milestone' && projectId !== null,
        queryFn: () => projectService.getMilestones(projectId!) });
    // feedback-policy: mutation pending,inline - disable repeat writes and retain the draft on failure.
    const mutation = useMutation({
        meta: { success: (_data, remove) => t(remove ? 'feedback.dependencyRemoved' : 'feedback.dependencyAdded', { name: task.title }) } satisfies MutationFeedbackMeta,
        mutationFn: async (remove?: number) => {
        if (remove) await api.delete(`/tasks/${task.id}/delivery-dependencies/${remove}`, { params: { expected_version: task.version } });
        else await api.post(`/tasks/${task.id}/delivery-dependencies`, { kind, target_id: targetId, expected_version: task.version,
            ...(kind === 'task' && branch.trim() ? { target_branch: branch.trim() } : {}) });
        return taskService.getById(task.id);
    }, onSuccess: async latest => { setTargetId(null); setText(''); setBranch(''); await edges.refetch(); onUpdated(latest); } });
    // feedback-policy: mutation pending,inline - keep the draft when the branch is rejected; a stale version refreshes and says so.
    const retarget = useMutation({
        meta: { success: () => t('feedback.prerequisiteBranchSaved', { name: task.title }) } satisfies MutationFeedbackMeta,
        mutationFn: async ({ edge, target }: { edge: number; target: string | null }) => {
            await githubService.retargetPrerequisite(task.id, edge, task.version, target);
            return taskService.getById(task.id);
        },
        onSuccess: async latest => { setEditing(null); setConflict(false); await edges.refetch(); onUpdated(latest); },
        onError: async error => {
            if (getApiErrorStatus(error) !== 409) return;
            setConflict(true);
            try {
                const latest = await taskService.getById(task.id);
                await edges.refetch();
                onUpdated(latest);
            } catch { /* The notice stays; the list can be refreshed by reopening the task. */ }
        },
    });
    useEffect(() => onPending(mutation.isPending || retarget.isPending), [mutation.isPending, retarget.isPending, onPending]);
    const save = (edge: number, target: string) => retarget.mutate({ edge, target: target.trim() === '' ? null : target.trim() });
    return <details open={expanded} className="space-y-3 rounded-md border border-border p-3" onToggle={event => setExpanded(event.currentTarget.open)}>
        <summary className="cursor-pointer font-medium">{t('teamwork.deliveryDependencies')}</summary>
        <p className="text-sm text-content-secondary">{t('teamwork.dependenciesHelp')}</p>
        {edges.isLoading && <p role="status">{t('common.loading')}</p>}
        {edges.isError && <QueryErrorState error={edges.error} fallback={t('teamwork.loadFailed')} onRetry={() => void edges.refetch()} />}
        <ul className="space-y-3">{edges.data?.map(edge => {
            const open = editing?.edge === edge.id;
            return <li key={edge.id} className="space-y-2 text-sm">
                <div className="flex flex-wrap items-center justify-between gap-2">
                    <span>{edge.title ?? t('teamwork.taskUnavailable')} · {t(edge.ready ? 'teamwork.prerequisiteReady' : 'teamwork.prerequisiteWaiting')}</span>
                    <span className="flex flex-wrap gap-1">
                        {canRetarget && edge.kind === 'task' && edge.title !== undefined && !open && <Button type="button" variant="ghost" size="sm" disabled={disabled || retarget.isPending}
                            aria-label={t(edge.target_branch ? 'teamwork.changeBranchFor' : 'teamwork.setBranchFor', { name: edge.title })}
                            onClick={() => { retarget.reset(); setConflict(false); setEditing({ edge: edge.id, draft: edge.target_branch ?? '', base: edge.target_branch ?? '' }); }}>
                            {t(edge.target_branch ? 'teamwork.changeBranch' : 'teamwork.setBranch')}</Button>}
                        {canEdit && <Button type="button" variant="ghost" size="sm" disabled={disabled} onClick={() => mutation.mutate(edge.id)}>{t('teamwork.unlink')}</Button>}
                    </span>
                </div>
                <BranchLine edge={edge} />
                <Hold edge={edge} />
                {open && <form className="space-y-2 rounded-md border border-border p-3" onSubmit={event => { event.preventDefault(); save(edge.id, editing.draft); }}>
                    <label className="field-lbl" htmlFor={`${id}-branch-${edge.id}`}>{t('teamwork.targetBranch')}</label>
                    <input id={`${id}-branch-${edge.id}`} className="input w-full" value={editing.draft} maxLength={255} ref={branchInput}
                        aria-describedby={`${id}-branch-help-${edge.id}`} aria-invalid={retarget.isError && !conflict}
                        onChange={event => setEditing({ ...editing, draft: event.target.value })} />
                    <p id={`${id}-branch-help-${edge.id}`} className="text-xs text-content-secondary">{t('teamwork.targetBranchHelp')}</p>
                    {conflict && <p role="alert" className="text-sm text-feedback-warning-foreground">{t('teamwork.branchConflict')}</p>}
                    {retarget.isError && !conflict && <p role="alert" className="text-sm text-feedback-danger-foreground">{getApiErrorMessage(retarget.error, t('teamwork.saveFailed'))}</p>}
                    <div className="flex flex-wrap gap-2">
                        <Button type="submit" size="sm" isLoading={retarget.isPending} disabled={disabled}>{t('teamwork.saveBranch')}</Button>
                        {edge.target_branch && <Button type="button" variant="secondary" size="sm" disabled={disabled || retarget.isPending}
                            onClick={() => save(edge.id, '')}>{t('teamwork.clearBranch')}</Button>}
                        <Button type="button" variant="ghost" size="sm" disabled={retarget.isPending}
                            onClick={() => { setEditing(null); setConflict(false); retarget.reset(); }}>{t('teamwork.cancelBranch')}</Button>
                    </div>
                </form>}
            </li>;
        })}</ul>
        {canEdit && <fieldset disabled={disabled} className="space-y-2"><legend className="text-sm font-medium">{t('teamwork.addPrerequisite')}</legend>
            <label className="field-lbl" htmlFor={`${id}-kind`}>{t('teamwork.prerequisiteType')}</label>
            <Select id={`${id}-kind`} className="input w-full" value={kind} onChange={event => { setKind(event.target.value as 'task' | 'milestone'); setTargetId(null); }}><option value="task">{t('teamwork.task')}</option><option value="milestone">{t('teamwork.milestone')}</option></Select>
            {kind === 'task' ? <><label className="field-lbl" htmlFor={`${id}-search`}>{t('teamwork.searchTasks')}</label><input id={`${id}-search`} className="input w-full" value={text} maxLength={200} onChange={event => { setText(event.target.value); setTargetId(null); }} />
                {tasks.isLoading && <p role="status">{t('common.loading')}</p>}
                {tasks.isSuccess && tasks.data.items.length === 0 && <p>{t('teamwork.noResults')}</p>}
                {tasks.isError && <QueryErrorState error={tasks.error} fallback={t('teamwork.loadFailed')} onRetry={() => void tasks.refetch()} />}
                <label className="field-lbl" htmlFor={`${id}-target`}>{t('teamwork.prerequisite')}</label><Select id={`${id}-target`} className="input w-full" value={targetId ?? ''} onChange={event => setTargetId(Number(event.target.value) || null)}><option value="">{t('teamwork.chooseTask')}</option>{tasks.data?.items.filter(item => item.id !== task.id).map(item => <option key={item.id} value={item.id}>#{item.id} · {item.title}</option>)}</Select>
                <label className="field-lbl" htmlFor={`${id}-new-branch`}>{t('teamwork.targetBranchOptional')}</label>
                <input id={`${id}-new-branch`} className="input w-full" value={branch} maxLength={255} aria-describedby={`${id}-new-branch-help`} onChange={event => setBranch(event.target.value)} />
                <p id={`${id}-new-branch-help`} className="text-xs text-content-secondary">{t('teamwork.targetBranchHelp')}</p></>
                : <><label className="field-lbl" htmlFor={`${id}-project`}>{t('teamwork.project')}</label><Select id={`${id}-project`} className="input w-full" value={projectId ?? ''} onChange={event => { setProjectId(Number(event.target.value) || null); setTargetId(null); }}><option value="">{t('teamwork.chooseProject')}</option>{projects.data?.map(item => <option key={item.id} value={item.id}>{item.name}</option>)}</Select>
                    {(projects.isLoading || milestones.isLoading) && <p role="status">{t('common.loading')}</p>}
                    {milestones.isSuccess && milestones.data.length === 0 && <p>{t('teamwork.noResults')}</p>}
                    {(projects.isError || milestones.isError) && <QueryErrorState error={projects.error ?? milestones.error} fallback={t('teamwork.loadFailed')} onRetry={() => { void projects.refetch(); void milestones.refetch(); }} />}
                    <label className="field-lbl" htmlFor={`${id}-milestone`}>{t('teamwork.milestone')}</label><Select id={`${id}-milestone`} className="input w-full" value={targetId ?? ''} onChange={event => setTargetId(Number(event.target.value) || null)}><option value="">{t('teamwork.chooseMilestone')}</option>{milestones.data?.map(item => <option key={item.id} value={item.id}>{item.name}</option>)}</Select></>}
            <Button type="button" size="sm" disabled={!targetId || disabled} isLoading={mutation.isPending} onClick={() => mutation.mutate(undefined)}>{t('teamwork.addPrerequisite')}</Button>
        </fieldset>}
        {mutation.isError && <p role="alert" className="text-sm text-feedback-danger-foreground">{getApiErrorMessage(mutation.error, t('teamwork.saveFailed'))}</p>}
    </details>;
};

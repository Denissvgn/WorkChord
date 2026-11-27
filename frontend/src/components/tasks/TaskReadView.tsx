import { TaskAssigneeDisplay } from './TaskAssigneeDisplay';
import { useTaskAssigneeDisplay } from './useTaskAssigneeDisplay';
import { useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useSearchParams } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import clsx from 'clsx';
import { Link2, Pencil } from 'lucide-react';
import type { Task, TaskBrief } from '../../types/task';
import { taskService } from '../../services/taskService';
import { Button } from '../common/Button';
import { ButtonLink } from '../common/ButtonLink';
import { Input } from '../common/Input';
import { useScopeLink } from '../../features/scope/useScopeLink';
import { useToast } from '../feedback/toast';
import { getApiErrorMessage, normalizeApiError } from '../../utils/apiError';
import type { MutationFeedbackMeta } from '../../features/mutationFeedback';
import { formatDate } from '../../utils/formatDate';
import { pillToneClassName, STATE_TONE } from '../ui/tone';
import { isEndedState, stateOf } from '../../utils/taskState';
import { emptyTaskBrief } from './taskEditorContract';
import { TaskBriefEditor } from './TaskBriefEditor';
import { TaskWorkPanel } from './TaskWorkPanel';
import { TaskRoutingSummary } from './TaskRoutingSummary';
import { TaskReassign } from './TaskReassign';
import { useAdminAccess } from '../../hooks/useAdminAccess';
import { clearAdminApiKey } from '../../utils/adminAccess';
import { DeliveryDependencies } from './DeliveryDependencies';
import { GitHubReconciliationPanel } from './GitHubReconciliationPanel';
import { useTaskViewSession, type TaskViewSession, type TaskViewSessionUpdate } from './taskViewSession';
import { TaskDiscussion } from './TaskDiscussion';
import { TimeEntriesPanel } from './TimeEntriesPanel';
import { TaskTimelinePanel } from './TaskTimelinePanel';

export type TaskViewPart = 'brief' | 'work' | 'activity';
export const TASK_PART_PARAM = 'part';
const PARTS: TaskViewPart[] = ['brief', 'work', 'activity'];

const parsePart = (value: string | null): TaskViewPart => (PARTS.includes(value as TaskViewPart) ? value as TaskViewPart : 'brief');

/**
 * The one next transition people usually take from each status. Start and submit run at once with a
 * standard reason; review needs a result per criterion, so it opens Work & review.
 */
const NEXT_TRANSITION: Partial<Record<Task['status'], { action: string; labelKey: string; reasonKey?: string }>> = {
    planned: { action: 'start_manual', labelKey: 'domain.action_start_manual', reasonKey: 'taskView.startReason' },
    active: { action: 'resolve_manual', labelKey: 'domain.action_resolve_manual', reasonKey: 'taskView.submitReason' },
    resolved: { action: 'review', labelKey: 'taskView.reviewWork' },
};

/** True when the server rejected the command because it wants a reason from the person. */
const reasonRequired = (error: unknown) => {
    const normalized = normalizeApiError(error, '');
    if (normalized.status !== 422 && normalized.code !== 'reason_required') return false;
    return normalized.code === 'reason_required'
        || normalized.fieldErrors.some(item => item.field === 'reason' || /\breason\b/i.test(item.message))
        || /\breason\b/i.test(normalized.message);
};

const BriefField = ({ label, value }: { label: string; value: string }) => (
    value.trim() ? (
        <div className="flex flex-col gap-1.5">
            <h3 className="text-xs font-semibold uppercase tracking-wide text-content-secondary">{label}</h3>
            <p className="whitespace-pre-wrap text-sm leading-relaxed text-content-primary">{value}</p>
        </div>
    ) : null
);

/**
 * Read-first task view: Brief, Work & review, Activity. Nothing is an input
 * until a section is edited; the part is kept in the URL beside ?task=<id>.
 */
export const TaskReadView = ({ task, draftKey, session: heldSession, onSession: onHeldSession, onTaskUpdated, onOpenTask, onEditAll, onDirty, onPending, onReload }: {
    /** Panel state held by the drawer across version remounts; the view keeps its own when none is given. */
    session?: TaskViewSession;
    onSession?: TaskViewSessionUpdate;
    task: Task;
    draftKey: string | null;
    onTaskUpdated: (task: Task) => void;
    /** Opens another task from a link in this view, such as a superseded task's successor; the drawer closes and navigates. */
    onOpenTask?: (taskId: number) => void;
    onEditAll: () => void;
    onDirty: (dirty: boolean) => void;
    onPending: (pending: boolean) => void;
    onReload: () => void;
}) => {
    const { t, i18n } = useTranslation();
    const assigneeDisplay = useTaskAssigneeDisplay(task, task.iteration_id);
    const scopeLink = useScopeLink();
    const toast = useToast();
    const queryClient = useQueryClient();
    const [params, setParams] = useSearchParams();
    const part = parsePart(params.get(TASK_PART_PARAM));
    const [briefDraft, setBriefDraft] = useState<TaskBrief | null>(null);
    const [reasonDraft, setReasonDraft] = useState<string | null>(null);
    const [sectionDirty, setSectionDirty] = useState(false);
    // A saved reassignment replaces the control (it is keyed by version), so the new one takes focus back.
    const [refocusVersion, setRefocusVersion] = useState<number | null>(null);
    const [ownSession, ownUpdate] = useTaskViewSession(draftKey);
    const session = heldSession ?? ownSession;
    const updateSession = onHeldSession ?? ownUpdate;
    const editingBrief = briefDraft !== null;
    const locked = editingBrief || sectionDirty;

    const setPart = (next: TaskViewPart) => {
        const nextParams = new URLSearchParams(params);
        if (next === 'brief') nextParams.delete(TASK_PART_PARAM); else nextParams.set(TASK_PART_PARAM, next);
        setParams(nextParams, { replace: true });
    };
    const startBriefEdit = () => {
        setPart('brief');
        setBriefDraft(task.brief ? structuredClone(task.brief) : { ...emptyTaskBrief(), context: task.description ?? '' });
        onDirty(true);
    };
    const markDirty = (dirty: boolean) => { setSectionDirty(dirty); onDirty(dirty || editingBrief); };

    // feedback-policy: mutation pending,inline
    const saveBrief = useMutation({
        mutationFn: (brief: TaskBrief) => taskService.writeBrief(task.id, task.version, brief),
        onMutate: () => onPending(true),
        onSuccess: latest => {
            setBriefDraft(null);
            onDirty(false);
            onTaskUpdated(latest);
            void queryClient.invalidateQueries({ queryKey: ['tasks'] });
            toast.success(t('taskView.briefSaved', { title: latest.title }));
        },
        onSettled: () => onPending(false),
    });

    // Canceled and superseded work keeps the status it had, but it is not work to start, submit or review.
    const next = isEndedState(stateOf(task)) ? undefined : NEXT_TRANSITION[task.status];
    // Shared with Work & review, so the header and the panel read one availability snapshot.
    // feedback-policy: query loading,error,retry,empty
    const actions = useQuery({ queryKey: ['taskActions', task.id, task.version], queryFn: () => taskService.actions(task.id), enabled: Boolean(next?.reasonKey) });
    // feedback-policy: mutation pending,inline
    const transition = useMutation({
        meta: { success: (_data, variables) => t('feedback.commandDone', { action: t(`domain.action_${(variables as { action: string }).action}`), name: task.title }) } satisfies MutationFeedbackMeta,
        mutationFn: ({ action, reason }: { action: string; reason: string }) => taskService.command(task.id, {
            action, expected_version: task.version, reason,
            expected_claim_generation: actions.data?.claim_generation, expected_running_run_ids: actions.data?.running_run_ids,
            expected_live_assignment_ids: actions.data?.live_assignment_ids,
        }),
        onMutate: () => onPending(true),
        onSuccess: latest => {
            setReasonDraft(null);
            onTaskUpdated(latest);
            void queryClient.invalidateQueries({ queryKey: ['tasks'] });
        },
        onError: error => { if (reasonRequired(error)) setReasonDraft(current => current ?? ''); },
        onSettled: () => onPending(false),
    });
    const criteriaCount = task.brief?.acceptance_criteria.length ?? 0;
    const runNext = () => {
        if (!next) return;
        const available = actions.data?.actions.find(item => item.action === next.action)?.allowed;
        // Review, a blocked action and a submit without criteria are explained in Work & review.
        if (!next.reasonKey || !available || (next.action === 'resolve_manual' && criteriaCount === 0)) { setPart('work'); return; }
        transition.mutate({ action: next.action, reason: t(next.reasonKey) });
    };

    const progressFor = (criterionId: string) => task.progress?.criteria.find(item => item.criterion_id === criterionId);
    const criteria = task.brief?.acceptance_criteria ?? [];
    const doneCount = criteria.filter(criterion => progressFor(criterion.id)?.state === 'completed').length;
    // A connected agent that has not been sent the task gets it through dispatch, not a manual start,
    // in the header and in Work & review alike. The link opens the pipeline's dispatch panel; in the
    // pipeline that panel is already above.
    // With the admin key the server treats the browser as an operator, and manual start and submit are
    // taken as a person, so those two are not offered until editing is locked again.
    const { actingAsOperator } = useAdminAccess();
    const operatorKeyBlocksNext = actingAsOperator && (next?.action === 'start_manual' || next?.action === 'resolve_manual');
    const offerDispatch = task.status === 'planned' && !isEndedState(stateOf(task)) && assigneeDisplay.dispatch === 'notSentYet';
    const dispatchShown = params.get('layout') === 'pipeline';
    // Owner is shown only when it is known to differ from the assignee's profile: with no assignee,
    // or once that profile has been read. While it loads, fails or has no team row, Owner stays hidden.
    const ownerDiffers = Boolean(task.owner) && (!task.assignee
        || (assigneeDisplay.profileId !== undefined && task.owner?.id !== assigneeDisplay.profileId));
    const copyLink = async () => {
        const url = new URL(window.location.href);
        url.searchParams.set('task', String(task.id));
        try {
            await navigator.clipboard.writeText(url.toString());
            toast.success(t('taskView.linkCopied'));
        } catch {
            toast.error(t('taskView.linkCopyFailed'));
        }
    };
    const partLabel = (value: TaskViewPart) => (
        value === 'brief' ? t('taskView.partBrief')
            : value === 'work' ? (criteria.length > 0 ? t('taskView.partWorkCount', { done: doneCount, total: criteria.length }) : t('taskView.partWork'))
                : t('taskView.partActivity')
    );

    return (
        <div className="task-read-view flex flex-col gap-5">
            <header className="sticky top-0 z-10 -mx-4 flex flex-col gap-3 border-b border-border bg-surface-card px-4 pb-0 pt-1 sm:-mx-6 sm:px-6">
                <div className="flex flex-wrap items-center gap-x-3 gap-y-2 text-sm">
                    <span data-task-state={stateOf(task)} className={clsx('rounded-full px-2.5 py-0.5 text-xs font-semibold', pillToneClassName[STATE_TONE[stateOf(task)]])}>
                        {t(`statuses.${stateOf(task)}`)}
                    </span>
                    {stateOf(task) === 'superseded' && task.successor_task_id && (
                        <Button type="button" variant="ghost" size="sm" onClick={() => {
                            if (onOpenTask) { onOpenTask(task.successor_task_id as number); return; }
                            const next = new URLSearchParams(params); next.set('task', String(task.successor_task_id)); next.delete(TASK_PART_PARAM); setParams(next);
                        }}>
                            {t('stoppedWork.supersededBy', { id: task.successor_task_id })}
                        </Button>
                    )}
                    <TaskAssigneeDisplay task={task} iterationId={task.iteration_id} />
                    {task.owner && ownerDiffers && <span className="text-content-secondary">{t('taskView.owner')} <b className="font-semibold text-content-primary">{task.owner.name}</b></span>}
                    {task.end_date && <span className="text-content-secondary">{t('taskView.due')} <b className="font-semibold text-content-primary">{formatDate(task.end_date, i18n.language)}</b></span>}
                    <span className="flex-1" />
                    <Button type="button" variant="ghost" size="sm" aria-label={t('taskView.copyLink')} title={t('taskView.copyLink')} onClick={() => { void copyLink(); }}>
                        <Link2 className="h-4 w-4" aria-hidden="true" />
                    </Button>
                    {offerDispatch && !dispatchShown && (locked
                        ? <Button type="button" size="sm" disabled>{t('taskView.sendToAgent')}</Button>
                        : <ButtonLink size="sm" to={scopeLink(`/tasks?layout=pipeline&task=${task.id}`)}>{t('taskView.sendToAgent')}</ButtonLink>)}
                    {next && !offerDispatch && !operatorKeyBlocksNext && (
                        <Button type="button" size="sm" disabled={locked || reasonDraft !== null || (Boolean(next.reasonKey) && actions.isLoading)}
                            isLoading={transition.isPending && reasonDraft === null} onClick={runNext}>
                            {t(next.labelKey)}
                        </Button>
                    )}
                </div>
                {next && !offerDispatch && operatorKeyBlocksNext && (
                    <div role="status" className="flex flex-wrap items-center gap-x-3 gap-y-2 rounded-md bg-surface-muted px-3 py-2 text-sm text-content-secondary">
                        <span>{t('taskView.takenAsPerson')}</span>
                        <Button type="button" size="sm" variant="secondary" onClick={clearAdminApiKey}>{t('taskView.lockEditing')}</Button>
                    </div>
                )}
                {locked && <p role="status" className="rounded-md bg-surface-muted px-3 py-2 text-sm text-content-secondary">{t('taskView.saveToChangeStatus')}</p>}
                {next && reasonDraft !== null && (
                    <form className="flex flex-col gap-2 rounded-md border border-border px-3 py-3"
                        onSubmit={event => { event.preventDefault(); if (reasonDraft.trim()) transition.mutate({ action: next.action, reason: reasonDraft.trim() }); }}>
                        <p className="text-sm text-content-secondary">{t('taskView.reasonNeeded')}</p>
                        <Input label={t('domain.reason')} required value={reasonDraft} maxLength={2000} disabled={transition.isPending}
                            onChange={event => setReasonDraft(event.target.value)} />
                        <div className="flex justify-end gap-2">
                            <Button type="button" variant="ghost" size="sm" disabled={transition.isPending} onClick={() => { setReasonDraft(null); transition.reset(); }}>{t('taskView.cancelReason')}</Button>
                            <Button type="submit" size="sm" disabled={!reasonDraft.trim()} isLoading={transition.isPending}>{t(next.labelKey)}</Button>
                        </div>
                    </form>
                )}
                {transition.isError && !reasonRequired(transition.error) && (
                    <p role="alert" className="text-sm text-feedback-danger-foreground">{getApiErrorMessage(transition.error, t('taskView.statusChangeFailed'))}</p>
                )}
                <nav aria-label={t('taskView.parts')} className="flex gap-1">
                    {PARTS.map(value => (
                        <Button key={value} type="button" aria-current={part === value ? 'page' : undefined}
                            onClick={() => setPart(value)}
                            className={clsx('border-b-2 px-3 py-2.5 text-sm', part === value
                                ? 'border-action font-semibold text-content-primary'
                                : 'border-transparent font-medium text-content-secondary hover:text-content-primary')} variant="secondary">
                            {partLabel(value)}
                        </Button>
                    ))}
                </nav>
            </header>

            {part === 'brief' && !editingBrief && (
                <section aria-label={t('taskView.partBrief')} className="flex flex-col gap-5">
                    <div className="flex items-start justify-between gap-3">
                        {task.brief ? <BriefField label={t('taskView.goal')} value={task.brief.goal} />
                            : <p className="whitespace-pre-wrap text-sm leading-relaxed text-content-primary">{task.description || t('taskView.noBrief')}</p>}
                        <Button type="button" variant="secondary" size="sm" onClick={startBriefEdit}>
                            <Pencil className="mr-1 h-3.5 w-3.5" aria-hidden="true" />{t('taskView.editBrief')}
                        </Button>
                    </div>
                    {task.brief && (
                        <>
                            <div className="grid grid-cols-1 gap-5 sm:grid-cols-2">
                                <BriefField label={t('taskView.inScope')} value={task.brief.scope} />
                                <BriefField label={t('taskView.outOfScope')} value={task.brief.exclusions} />
                            </div>
                            <BriefField label={t('taskView.context')} value={task.brief.context} />
                            <div className="flex flex-col gap-2">
                                <div className="flex items-baseline justify-between">
                                    <h3 className="text-xs font-semibold uppercase tracking-wide text-content-secondary">{t('taskView.acceptanceCriteria')}</h3>
                                    {criteria.length > 0 && <Button type="button" className="text-sm font-medium text-action hover:underline" onClick={() => setPart('work')} variant="secondary">{t('taskView.seeEvidence')}</Button>}
                                </div>
                                <ol className="flex flex-col gap-2">
                                    {criteria.map(criterion => {
                                        const state = progressFor(criterion.id)?.state ?? 'pending';
                                        return (
                                            <li key={criterion.id} className="flex items-start gap-3 rounded-lg border border-border px-3 py-2.5">
                                                <span className={clsx('mt-0.5 shrink-0 rounded-full px-2 py-0.5 text-xs font-semibold',
                                                    state === 'completed' ? 'bg-feedback-success-muted text-feedback-success-foreground' : 'bg-surface-subtle text-content-secondary')}>
                                                    {t(`domain.${state}`)}
                                                </span>
                                                <span className="text-sm leading-relaxed">{criterion.text}</span>
                                            </li>
                                        );
                                    })}
                                </ol>
                            </div>
                            <div className="grid grid-cols-1 gap-5 sm:grid-cols-2">
                                <BriefField label={t('taskView.verification')} value={task.brief.verification} />
                                <BriefField label={t('taskView.artifacts')} value={task.brief.artifact_expectations} />
                            </div>
                        </>
                    )}
                    <section aria-label={t('taskReassign.title')} className="flex flex-col gap-3 border-t border-border-subtle pt-4">
                        <h3 className="text-xs font-semibold uppercase tracking-wide text-content-secondary">{t('taskReassign.title')}</h3>
                        <TaskRoutingSummary routing={task.brief?.routing} />
                        {task.iteration_id !== null && (
                            <TaskReassign key={`${task.id}:${task.version}`} task={task} disabled={locked} focusOnMount={refocusVersion === task.version}
                                onSaved={updated => setRefocusVersion(updated.version)} onTaskUpdated={onTaskUpdated} onPending={onPending} />
                        )}
                    </section>
                    <div className="flex flex-col gap-3 border-t border-border-subtle pt-4">
                        <div className="flex items-baseline justify-between">
                            <h3 className="text-xs font-semibold uppercase tracking-wide text-content-secondary">{t('taskView.planning')}</h3>
                            <Button type="button" variant="secondary" size="sm" onClick={onEditAll}>{t('taskView.editPlanning')}</Button>
                        </div>
                        <dl className="grid grid-cols-2 gap-3 text-sm sm:grid-cols-4">
                            <div><dt className="text-xs text-content-secondary">{t('taskView.effort')}</dt><dd className="font-semibold">{task.effort_days === null ? t('domain.unknownEstimate') : t('units.daysCompact', { count: task.effort_days })}</dd></div>
                            <div><dt className="text-xs text-content-secondary">{t('taskView.priority')}</dt><dd className="font-semibold">{t('taskView.priorityValue', { priority: task.priority })}</dd></div>
                            <div><dt className="text-xs text-content-secondary">{t('taskView.waitsFor')}</dt><dd className="font-semibold">{task.dependencies.length > 0 ? t('taskView.waitsForCount', { count: task.dependencies.length }) : t('common.none')}</dd></div>
                            <div><dt className="text-xs text-content-secondary">{t('taskView.scheduled')}</dt><dd className="font-semibold">{task.start_date && task.end_date ? `${formatDate(task.start_date, i18n.language)} – ${formatDate(task.end_date, i18n.language)}` : t('taskView.notScheduled')}</dd></div>
                        </dl>
                    </div>
                </section>
            )}

            {part === 'brief' && briefDraft && (
                <form className="flex flex-col gap-4" onSubmit={event => { event.preventDefault(); saveBrief.mutate(briefDraft); }}>
                    <TaskBriefEditor part="essential" value={briefDraft} onChange={setBriefDraft} disabled={saveBrief.isPending} />
                    <details>
                        <summary className="cursor-pointer text-sm text-content-secondary">{t('quickCapture.moreFields')}</summary>
                        <div className="mt-4"><TaskBriefEditor part="details" value={briefDraft} onChange={setBriefDraft} disabled={saveBrief.isPending} /></div>
                    </details>
                    <p className="text-xs text-content-secondary">{t('taskView.criterionRevisionHelp')}</p>
                    {saveBrief.isError && <p role="alert" className="text-sm text-feedback-danger-foreground">{getApiErrorMessage(saveBrief.error, t('taskView.briefSaveFailed'))}</p>}
                    <footer className="sticky bottom-0 -mx-4 flex items-center justify-between gap-3 border-t border-border bg-surface-card px-4 py-3 sm:-mx-6 sm:px-6">
                        <span className="text-sm text-content-secondary">{t('taskView.unsavedBrief')}</span>
                        <div className="flex gap-2">
                            <Button type="button" variant="secondary" disabled={saveBrief.isPending} onClick={() => { setBriefDraft(null); onDirty(false); saveBrief.reset(); }}>{t('taskView.discard')}</Button>
                            <Button type="submit" isLoading={saveBrief.isPending}>{t('taskView.saveBrief')}</Button>
                        </div>
                    </footer>
                </form>
            )}

            {part === 'work' && (
                <section aria-label={t('taskView.partWork')} className="flex flex-col gap-5">
                    <TaskWorkPanel key={`${task.id}:${task.version}`} task={task} draftKey={draftKey} disabled={editingBrief}
                        onEditBrief={startBriefEdit} onDirty={markDirty} onPending={onPending} onReload={onReload}
                        offerDispatch={offerDispatch}
                        onUpdated={onTaskUpdated} />
                    <GitHubReconciliationPanel task={task} session={session} onSession={updateSession} onTaskUpdated={onTaskUpdated} />
                    <DeliveryDependencies task={task} disabled={editingBrief} draftKey={draftKey} session={session} onSession={updateSession} onDirty={markDirty} onPending={onPending} onUpdated={onTaskUpdated} />
                    {task.project_id && <TimeEntriesPanel projectId={task.project_id} taskId={task.id} draftKey={draftKey} disabled={editingBrief}
                        onDirty={markDirty} onPending={onPending} />}
                </section>
            )}

            {part === 'activity' && (
                <section aria-label={t('taskView.partActivity')} className="flex flex-col gap-5">
                    <TaskDiscussion taskId={task.id} draftKey={draftKey} disabled={editingBrief} onDirty={markDirty} onPending={onPending} />
                    <TaskTimelinePanel task={task} />
                </section>
            )}

            <div className="border-t border-border-subtle pt-3">
                <Button type="button" variant="ghost" size="sm" onClick={onEditAll}>{t('taskView.editAllFields')}</Button>
            </div>
        </div>
    );
};

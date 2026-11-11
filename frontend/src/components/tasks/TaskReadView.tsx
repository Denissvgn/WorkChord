import { useState } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import { useSearchParams } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import clsx from 'clsx';
import { Link2, Pencil } from 'lucide-react';
import type { Task, TaskBrief } from '../../types/task';
import { taskService } from '../../services/taskService';
import { Button } from '../common/Button';
import { useToast } from '../feedback/toast';
import { getApiErrorMessage } from '../../utils/apiError';
import { formatDate } from '../../utils/formatDate';
import { pillToneClassName, STATUS_TONE } from '../ui/tone';
import { TaskBriefEditor } from './TaskBriefEditor';
import { TaskWorkPanel } from './TaskWorkPanel';
import { DeliveryDependencies } from './DeliveryDependencies';
import { TaskDiscussion } from './TaskDiscussion';
import { TimeEntriesPanel } from './TimeEntriesPanel';
import { TaskTimelinePanel } from './TaskTimelinePanel';

export type TaskViewPart = 'brief' | 'work' | 'activity';
export const TASK_PART_PARAM = 'part';
const PARTS: TaskViewPart[] = ['brief', 'work', 'activity'];

const parsePart = (value: string | null): TaskViewPart => (PARTS.includes(value as TaskViewPart) ? value as TaskViewPart : 'brief');

/** The one next transition people usually take from each status. */
const NEXT_TRANSITION: Partial<Record<Task['status'], { action: string; labelKey: string }>> = {
    planned: { action: 'start_manual', labelKey: 'domain.action_start_manual' },
    active: { action: 'resolve_manual', labelKey: 'domain.action_resolve_manual' },
    resolved: { action: 'review', labelKey: 'taskView.reviewWork' },
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
export const TaskReadView = ({ task, draftKey, onTaskUpdated, onEditAll, onDirty, onPending, onReload }: {
    task: Task;
    draftKey: string | null;
    onTaskUpdated: (task: Task) => void;
    onEditAll: () => void;
    onDirty: (dirty: boolean) => void;
    onPending: (pending: boolean) => void;
    onReload: () => void;
}) => {
    const { t, i18n } = useTranslation();
    const toast = useToast();
    const queryClient = useQueryClient();
    const [params, setParams] = useSearchParams();
    const part = parsePart(params.get(TASK_PART_PARAM));
    const [briefDraft, setBriefDraft] = useState<TaskBrief | null>(null);
    const [workAction, setWorkAction] = useState<string | undefined>(undefined);
    const [sectionDirty, setSectionDirty] = useState(false);
    const editingBrief = briefDraft !== null;
    const locked = editingBrief || sectionDirty;

    const setPart = (next: TaskViewPart) => {
        const nextParams = new URLSearchParams(params);
        if (next === 'brief') nextParams.delete(TASK_PART_PARAM); else nextParams.set(TASK_PART_PARAM, next);
        setParams(nextParams, { replace: true });
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

    const progressFor = (criterionId: string) => task.progress?.criteria.find(item => item.criterion_id === criterionId);
    const criteria = task.brief?.acceptance_criteria ?? [];
    const doneCount = criteria.filter(criterion => progressFor(criterion.id)?.state === 'completed').length;
    const next = NEXT_TRANSITION[task.status];
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
                    <span className={clsx('rounded-full px-2.5 py-0.5 text-xs font-semibold', pillToneClassName[STATUS_TONE[task.status]])}>
                        {t(`statuses.${task.status}`)}
                    </span>
                    <span className="text-content-secondary">{t('taskView.assignee')} <b className="font-semibold text-content-primary">{task.assignee?.name ?? t('common.unassigned')}</b></span>
                    <span className="text-content-secondary">{t('taskView.owner')} <b className="font-semibold text-content-primary">{task.owner?.name ?? t('domain.unassignedOwner')}</b></span>
                    {task.end_date && <span className="text-content-secondary">{t('taskView.due')} <b className="font-semibold text-content-primary">{formatDate(task.end_date, i18n.language)}</b></span>}
                    <span className="flex-1" />
                    <Button type="button" variant="ghost" size="sm" aria-label={t('taskView.copyLink')} title={t('taskView.copyLink')} onClick={() => { void copyLink(); }}>
                        <Link2 className="h-4 w-4" aria-hidden="true" />
                    </Button>
                    {next && (
                        <Button type="button" size="sm" disabled={locked} onClick={() => { setWorkAction(next.action); setPart('work'); }}>
                            {t(next.labelKey)}
                        </Button>
                    )}
                </div>
                {locked && <p role="status" className="rounded-md bg-surface-muted px-3 py-2 text-sm text-content-secondary">{t('taskView.saveToChangeStatus')}</p>}
                <nav aria-label={t('taskView.parts')} className="flex gap-1">
                    {PARTS.map(value => (
                        <button key={value} type="button" aria-current={part === value ? 'page' : undefined}
                            onClick={() => setPart(value)}
                            className={clsx('border-b-2 px-3 py-2.5 text-sm', part === value
                                ? 'border-action font-semibold text-content-primary'
                                : 'border-transparent font-medium text-content-secondary hover:text-content-primary')}>
                            {partLabel(value)}
                        </button>
                    ))}
                </nav>
            </header>

            {part === 'brief' && !editingBrief && (
                <section aria-label={t('taskView.partBrief')} className="flex flex-col gap-5">
                    <div className="flex items-start justify-between gap-3">
                        {task.brief ? <BriefField label={t('taskView.goal')} value={task.brief.goal} />
                            : <p className="whitespace-pre-wrap text-sm leading-relaxed text-content-primary">{task.description || t('taskView.noBrief')}</p>}
                        <Button type="button" variant="secondary" size="sm" onClick={() => {
                            if (task.brief) { setBriefDraft(structuredClone(task.brief)); onDirty(true); } else { onEditAll(); }
                        }}>
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
                                    {criteria.length > 0 && <button type="button" className="text-sm font-medium text-action hover:underline" onClick={() => setPart('work')}>{t('taskView.seeEvidence')}</button>}
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
                    <TaskBriefEditor value={briefDraft} onChange={setBriefDraft} disabled={saveBrief.isPending} />
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
                    <TaskWorkPanel key={`${task.id}:${task.version}:${workAction ?? ''}`} task={task} draftKey={draftKey} disabled={editingBrief}
                        initialAction={workAction} onDirty={markDirty} onPending={onPending} onReload={onReload}
                        onUpdated={latest => { setWorkAction(undefined); onTaskUpdated(latest); }} />
                    <DeliveryDependencies task={task} disabled={locked} onPending={onPending} onUpdated={onTaskUpdated} />
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

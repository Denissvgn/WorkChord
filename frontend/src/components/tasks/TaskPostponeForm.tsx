import { useId, useState } from 'react';
import { useMutation, useQuery } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { taskService } from '../../services/taskService';
import type { ReactivationRequirementInput, ReactivationRequirementKind, Task, TaskActions } from '../../types/task';
import { getApiErrorMessage } from '../../utils/apiError';
import { Button } from '../common/Button';
import { Select } from '../common/Select';
import { Textarea } from '../common/Textarea';
import { QueryErrorState } from '../feedback/QueryState';
import type { MutationFeedbackMeta } from '../../features/mutationFeedback';
import { useActiveMount } from './useDraftDismissal';

type RowKind = 'predecessor_accepted' | 'linked_task' | 'linked_triage' | 'date' | 'owner_decision';
interface Row { key: number; kind: RowKind; taskId: number | null; triageId: string; date: string; description: string }

const MAX_REQUIREMENTS = 20;
const emptyRow = (key: number): Row => ({ key, kind: 'predecessor_accepted', taskId: null, triageId: '', date: '', description: '' });

/** The server's shape for a row, or null while the row is incomplete. */
const requirementInput = (row: Row): ReactivationRequirementInput | null => {
    const kind: ReactivationRequirementKind = row.kind === 'linked_task' || row.kind === 'linked_triage' ? 'linked_resolved' : row.kind;
    if (row.kind === 'predecessor_accepted' || row.kind === 'linked_task') return row.taskId ? { kind, task_id: row.taskId } : null;
    if (row.kind === 'linked_triage') { const id = Number(row.triageId); return Number.isSafeInteger(id) && id > 0 ? { kind, triage_item_id: id } : null; }
    if (row.kind === 'date') return row.date ? { kind, on_date: row.date } : null;
    return row.description.trim() ? { kind, description: row.description.trim() } : null;
};

const tomorrow = () => {
    const day = new Date();
    day.setDate(day.getDate() + 1);
    return `${day.getFullYear()}-${String(day.getMonth() + 1).padStart(2, '0')}-${String(day.getDate()).padStart(2, '0')}`;
};

const TaskTarget = ({ id, task, value, onChange, disabled }: { id: string; task: Task; value: number | null; onChange: (value: number | null) => void; disabled: boolean }) => {
    const { t } = useTranslation();
    const [text, setText] = useState('');
    // feedback-policy: query loading,error,retry,empty - the search shows loading, retry and empty feedback.
    const found = useQuery({ queryKey: ['postpone-task-search', text], enabled: text.trim().length > 0, queryFn: () => taskService.lookup({ q: text, limit: 20 }) });
    return <div className="space-y-2">
        <label className="field-lbl" htmlFor={`${id}-search`}>{t('domain.postponeSearchTasks')}</label>
        <input id={`${id}-search`} className="input w-full" value={text} maxLength={200} disabled={disabled} onChange={event => { setText(event.target.value); onChange(null); }} />
        {found.isLoading && <p role="status" className="text-sm text-content-secondary">{t('common.loading')}</p>}
        {found.isSuccess && found.data.items.length === 0 && <p role="status" className="text-sm text-content-secondary">{t('domain.postponeNoTasks')}</p>}
        {found.isError && <QueryErrorState error={found.error} fallback={t('domain.postponeSearchFailed')} onRetry={() => void found.refetch()} />}
        <label className="field-lbl" htmlFor={`${id}-task`}>{t('domain.postponeTask')}</label>
        <Select id={`${id}-task`} className="input w-full" value={value ?? ''} disabled={disabled} onChange={event => onChange(Number(event.target.value) || null)}>
            <option value="">{t('domain.postponeChooseTask')}</option>
            {found.data?.items.filter(item => item.id !== task.id).map(item => <option key={item.id} value={item.id}>#{item.id} · {item.title}</option>)}
        </Select>
    </div>;
};

/**
 * Postpones planned, active or resolved work with a reason and the requirements that bring it back.
 * It names what the postponement will release before the person confirms.
 */
export const TaskPostponeForm = ({ task, actions, disabled, disabledReasons = [], onPending, onUpdated }: {
    task: Task; actions: TaskActions | undefined; disabled: boolean; /** Why the form cannot be used for a reason outside it, such as unsaved progress. */ disabledReasons?: string[];
    onPending: (pending: boolean) => void; onUpdated: (task: Task) => void;
}) => {
    const { t } = useTranslation();
    const id = useId();
    const isActive = useActiveMount();
    const [open, setOpen] = useState(false);
    const [reason, setReason] = useState('');
    const [nextKey, setNextKey] = useState(2);
    const [rows, setRows] = useState<Row[]>([emptyRow(1)]);
    // feedback-policy: mutation pending,inline
    const postpone = useMutation({
        meta: { success: t('feedback.postponed', { name: task.title }) } satisfies MutationFeedbackMeta,
        mutationFn: () => taskService.postpone(task.id, { expected_version: task.version, reason: reason.trim(),
            requirements: rows.map(requirementInput).filter((item): item is ReactivationRequirementInput => item !== null),
            expected_claim_generation: actions?.claim_generation, expected_running_run_ids: actions?.running_run_ids,
            expected_live_assignment_ids: actions?.live_assignment_ids }),
        onSuccess: response => { setOpen(false); setReason(''); setRows([emptyRow(1)]); onUpdated(response.task); },
        onSettled: () => { if (isActive()) onPending(false); },
        // feedback-policy: mutation pending,inline
    });
    const update = (key: number, patch: Partial<Row>) => setRows(current => current.map(row => row.key === key ? { ...row, ...patch } : row));
    const complete = rows.every(row => requirementInput(row) !== null);
    const missing = [...disabledReasons, !reason.trim() && t('domain.postponeNeedsReason'), !complete && t('domain.postponeNeedsRequirements')].filter(Boolean);
    const runs = actions?.running_run_ids.length ?? 0;
    const assignments = actions?.live_assignment_ids.length ?? 0;
    const holdsClaim = Boolean(task.claimed_by);
    const returnsTo = task.status === 'resolved' ? 'resolved' : 'planned';
    return <section className="space-y-3 border-t border-border pt-3" aria-labelledby={`${id}-heading`}>
        <h4 id={`${id}-heading`} className="font-medium text-content-primary">{t('domain.postponeHeading')}</h4>
        <p className="text-sm text-content-secondary">{t('domain.postponeHelp')}</p>
        {!open && <Button type="button" variant="secondary" disabled={disabled} onClick={() => setOpen(true)}>{t('domain.postponeOpen')}</Button>}
        {open && <form className="space-y-4" onSubmit={event => { event.preventDefault(); if (!disabled && missing.length === 0) { onPending(true); postpone.mutate(); } }}>
            <Textarea label={t('domain.postponeReason')} required value={reason} maxLength={2000} disabled={postpone.isPending}
                onChange={event => setReason(event.target.value)} />
            <div className="space-y-3">
                {rows.map((row, index) => <fieldset key={row.key} disabled={postpone.isPending} className="space-y-2 rounded-md border border-border p-3">
                    <legend className="px-1 text-sm font-medium">{t('domain.requirementN', { n: index + 1 })}</legend>
                    <label className="field-lbl" htmlFor={`${id}-${row.key}-kind`}>{t('domain.requirementKind')}</label>
                    <Select id={`${id}-${row.key}-kind`} className="input w-full" value={row.kind}
                        onChange={event => update(row.key, { kind: event.target.value as RowKind, taskId: null })}>
                        {(['predecessor_accepted', 'linked_task', 'linked_triage', 'date', 'owner_decision'] as const).map(kind => <option key={kind} value={kind}>{t(`domain.reqKind_${kind}`)}</option>)}
                    </Select>
                    {(row.kind === 'predecessor_accepted' || row.kind === 'linked_task') && <TaskTarget id={`${id}-${row.key}`} task={task} value={row.taskId} disabled={postpone.isPending} onChange={taskId => update(row.key, { taskId })} />}
                    {row.kind === 'linked_triage' && <div>
                        <label className="field-lbl" htmlFor={`${id}-${row.key}-triage`}>{t('domain.postponeTriageItem')}</label>
                        <input id={`${id}-${row.key}-triage`} className="input w-full" inputMode="numeric" pattern="[0-9]*" value={row.triageId} maxLength={12}
                            onChange={event => update(row.key, { triageId: event.target.value.trim() })} />
                    </div>}
                    {row.kind === 'date' && <div>
                        <label className="field-lbl" htmlFor={`${id}-${row.key}-date`}>{t('domain.postponeDate')}</label>
                        <input id={`${id}-${row.key}-date`} type="date" className="input w-full" min={tomorrow()} value={row.date} onChange={event => update(row.key, { date: event.target.value })} />
                    </div>}
                    {row.kind === 'owner_decision' && <Textarea label={t('domain.postponeDecision')} maxLength={2000} value={row.description}
                        onChange={event => update(row.key, { description: event.target.value })} />}
                    {rows.length > 1 && <Button type="button" variant="ghost" size="sm" onClick={() => setRows(current => current.filter(item => item.key !== row.key))}>{t('domain.removeRequirement', { n: index + 1 })}</Button>}
                </fieldset>)}
                {rows.length < MAX_REQUIREMENTS && <Button type="button" variant="secondary" size="sm" disabled={postpone.isPending}
                    onClick={() => { setRows(current => [...current, emptyRow(nextKey)]); setNextKey(key => key + 1); }}>{t('domain.addRequirement')}</Button>}
            </div>
            <div className="space-y-1 rounded-md bg-surface-muted px-3 py-2 text-sm" aria-labelledby={`${id}-release`} role="group">
                <p id={`${id}-release`} className="font-medium text-content-primary">{t('domain.releaseHeading')}</p>
                <ul className="list-disc space-y-1 pl-5 text-content-secondary">
                    {holdsClaim && <li>{t('domain.releaseClaim')}</li>}
                    {runs > 0 && <li>{t('domain.releaseRuns', { count: runs })}</li>}
                    {assignments > 0 && <li>{t('domain.releaseAssignments', { count: assignments })}</li>}
                    {!holdsClaim && runs === 0 && assignments === 0 && <li>{t('domain.releaseNothing')}</li>}
                    <li>{t(`domain.returnsTo_${returnsTo}`)}</li>
                </ul>
            </div>
            {postpone.isError && <p role="alert" className="text-sm text-feedback-danger-foreground">{getApiErrorMessage(postpone.error, t('domain.postponeFailed'))}</p>}
            <div className="flex flex-wrap items-center gap-2">
                <Button type="submit" isLoading={postpone.isPending} disabled={disabled || missing.length > 0} aria-describedby={missing.length ? `${id}-missing` : undefined}>{t('domain.postponeConfirm')}</Button>
                <Button type="button" variant="ghost" disabled={postpone.isPending} onClick={() => { setOpen(false); postpone.reset(); }}>{t('domain.postponeCancel')}</Button>
                {missing.length > 0 && <p id={`${id}-missing`} className="w-full text-sm text-content-secondary">{missing.join(' ')}</p>}
            </div>
        </form>}
    </section>;
};

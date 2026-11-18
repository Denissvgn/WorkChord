import { useActiveMount } from './useDraftDismissal';
import { usePlanningObservation } from '../../features/usePlanningObservation';
import type { ObservedRevisions } from '../../services/planningInputService';
import { planningInputService } from '../../services/planningInputService';
import type { Iteration } from '../../types/iteration';
import { useEffect, useId, useState } from 'react';
import { useMutation, useQuery } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { taskService } from '../../services/taskService';
import { iterationService } from '../../services/iterationService';
import type { CriterionProgress, Task } from '../../types/task';
import { getApiErrorMessage } from '../../utils/apiError';
import { Button } from '../common/Button';
import { Input } from '../common/Input';
import { QueryErrorState, QueryLoadingState } from '../feedback/QueryState';
import { TaskReviewer } from './TaskReviewer';
import { useTaskReviewer } from './useTaskReviewer';
import type { MutationFeedbackMeta } from '../../features/mutationFeedback';

import { Select } from '../../components/common/Select';

const DRAFT_TTL_MS = 86400000;
const PROGRESS_STATES = ['pending', 'in_progress', 'completed'];
const sameProgress = (left: CriterionProgress, right: CriterionProgress) => left.criterion_id === right.criterion_id
    && left.criterion_revision === right.criterion_revision && left.state === right.state && left.evidence === right.evidence;
const progressRows = (value: unknown): CriterionProgress[] | null => Array.isArray(value) && value.length <= 100
    && value.every((item: CriterionProgress) => typeof item?.criterion_id === 'string' && Number.isInteger(item.criterion_revision)
        && typeof item.evidence === 'string' && PROGRESS_STATES.includes(item.state)) ? value as CriterionProgress[] : null;

const sameRow = (left: CriterionProgress, right: CriterionProgress) => left.criterion_id === right.criterion_id && left.criterion_revision === right.criterion_revision;

/**
 * Lays a saved progress draft over the current criteria. Only rows the person edited (they differ
 * from the progress the draft was taken from) are laid over; every other row shows the current
 * server value, and rows for removed or reworded criteria are dropped, so the panel always lists the
 * current brief. The draft is stale only when an edited criterion now has saved progress on the
 * server that differs from what the draft was taken from. A brief edit clears saved progress, which
 * is not a competing write, so a brief change alone never makes the draft stale. A draft without a
 * recorded base treats every changed row as edited.
 */
const restoreProgress = (stored: { version?: unknown; criteria?: unknown; base?: unknown } | null, initial: CriterionProgress[],
    saved: CriterionProgress[], version: number) => {
    const rows = progressRows(stored?.criteria);
    if (!stored || !rows) return { criteria: initial, version, base: initial };
    const base = progressRows(stored.base);
    const edits = rows.filter(item => {
        const observed = base?.find(row => sameRow(row, item));
        return !observed || !sameProgress(observed, item);
    });
    const criteria = initial.map(row => edits.find(item => sameRow(item, row)) ?? row);
    const conflict = stored.version !== version && criteria.some((row, index) => {
        if (sameProgress(row, initial[index]) || !edits.includes(row)) return false;
        if (!base) return true;
        const recorded = saved.find(item => sameRow(item, row));
        const observed = base.find(item => sameRow(item, row));
        return recorded !== undefined && (!observed || !sameProgress(observed, recorded));
    });
    // A conflicting draft keeps the progress it was taken from until the person keeps or discards it.
    return conflict && Number.isInteger(stored.version) ? { criteria, version: stored.version as number, base: base ?? [] } : { criteria, version, base: initial };
};

export const TaskWorkPanel = ({ task, disabled, draftKey, onDirty, onPending, onUpdated, onReload, onEditBrief, offerDispatch = false }: {
    task: Task; disabled: boolean; draftKey: string | null; onDirty: (dirty: boolean) => void;
    onPending: (pending: boolean) => void; onUpdated: (task: Task) => void; onReload: () => void;
    /** Opens the brief for editing, so a missing acceptance criterion can be added. */
    onEditBrief?: () => void;
    /**
     * A connected agent has not been sent the task: it gets the task through dispatch, which the
     * task view's header offers, so manual Start work is not offered here.
     */
    offerDispatch?: boolean;
}) => {
    const { t } = useTranslation();
    const isActive = useActiveMount();
    const id = useId();
    const key = draftKey ? `${draftKey}:progress` : null;
    const initial = (task.brief?.acceptance_criteria ?? []).map(criterion => task.progress?.criteria.find(item => item.criterion_id === criterion.id && item.criterion_revision === criterion.revision)
        ?? { criterion_id: criterion.id, criterion_revision: criterion.revision, state: 'pending' as const, evidence: '' });
    const [restored] = useState(() => {
        try {
            const stored = JSON.parse(key ? sessionStorage.getItem(key) ?? 'null' : 'null');
            return restoreProgress(stored && Date.now() - stored.savedAt < DRAFT_TTL_MS ? stored : null, initial, task.progress?.criteria ?? [], task.version);
        } catch { return restoreProgress(null, initial, [], task.version); }
    });
    const [base, setBase] = useState(restored.base);
    const [draftVersion, setDraftVersion] = useState(restored.version);
    const [criteria, setCriteria] = useState<CriterionProgress[]>(restored.criteria);
    const [reason, setReason] = useState(() => { try { const stored = JSON.parse(key ? sessionStorage.getItem(key) ?? 'null' : 'null'); return stored && Date.now() - stored.savedAt < DRAFT_TTL_MS && typeof stored.reason === 'string' ? stored.reason : ''; } catch { return ''; } });
    const savedCommand = () => {
        try { const value = JSON.parse(key ? sessionStorage.getItem(key) ?? 'null' : 'null');
            if (value && Date.now() - value.savedAt < DRAFT_TTL_MS && typeof value.action === 'string' && value.action.length < 50 && typeof value.iterationId === 'string'
                && value.commandRevisions && Object.entries(value.commandRevisions).length <= 500
                && Object.entries(value.commandRevisions).every(([id, revision]) => /^[1-9][0-9]*$/.test(id) && Number.isSafeInteger(revision) && Number(revision) > 0)) return value;
        } catch { /* Keep the original server observation if a local context is malformed. */ }
        return null;
    };
    const [sourceRevisions] = useState<ObservedRevisions>(() => task.iteration_id !== null && task.iteration_revision
        ? { [task.iteration_id]: savedCommand()?.commandRevisions[task.iteration_id] ?? task.iteration_revision } : {});
    const [commandRevisions, setCommandRevisions] = useState<ObservedRevisions>(() => savedCommand()?.commandRevisions ?? sourceRevisions);
    const targetContext = usePlanningObservation<Iteration>();
    const [action, setAction] = useState(() => savedCommand()?.action ?? '');
    const [contextError, setContextError] = useState<unknown>(null);
    const [iterationId, setIterationId] = useState<string>(() => savedCommand()?.iterationId ?? '');
    const staleDraft = draftVersion !== task.version;
    const criteriaDirty = JSON.stringify(criteria) !== JSON.stringify(initial);
    const dirty = staleDraft || criteriaDirty || reason.length > 0 || action.length > 0;
    useEffect(() => {
        onDirty(dirty);
        if (!key) return;
        try {
            // `base` is the server progress the draft was taken from, so a later read can tell a brief edit from a conflicting progress write.
            if (dirty) sessionStorage.setItem(key, JSON.stringify({ version: draftVersion, savedAt: Date.now(), criteria, base, reason, action, iterationId, commandRevisions }));
            else sessionStorage.removeItem(key);
        } catch { /* The in-page draft remains usable. */ }
    }, [dirty, criteria, reason, key, onDirty, draftVersion, action, iterationId, commandRevisions, base]);
    useEffect(() => () => onDirty(false), [onDirty]);
    // feedback-policy: query loading,error,retry,empty
    const actions = useQuery({
        queryKey: ['taskActions', task.id, task.version], queryFn: () => taskService.actions(task.id),
        // feedback-policy: query loading,error,retry,empty
    });
    // feedback-policy: query loading,error,retry,empty
    const iterations = useQuery({
        queryKey: ['iterations'], queryFn: iterationService.getAll, enabled: action === 'commit',
        // feedback-policy: query loading,error,retry,empty
    });
    const reviewCriteria = task.brief?.acceptance_criteria ?? [];
    const reviewer = useTaskReviewer(task);
    const reviewerName = reviewer.data?.reviewer_name;
    // Who decides acceptance is only known once the work is submitted and the reviewer is loaded.
    const acceptanceNote = task.status !== 'resolved' || !reviewer.data ? null
        : reviewerName && reviewerName !== task.assignee?.name ? t('domain.acceptSeparateReviewer') : t('domain.acceptAnyone');
    const submitBlocked = task.status === 'active' && reviewCriteria.length === 0;
    const [reviewResults, setReviewResults] = useState<Record<string, { result: '' | 'pass' | 'fail'; note: string }>>({});
    const resultFor = (criterionId: string) => reviewResults[criterionId] ?? { result: '' as const, note: '' };
    // The same per-criterion packet the reviewer skill records, so a worker reads one rework format.
    const reviewEvidence = reviewCriteria.length === 0 ? '' : JSON.stringify({ criteria: reviewCriteria.map(criterion => ({
        id: criterion.id, revision: criterion.revision, result: resultFor(criterion.id).result || 'not_checked', note: resultFor(criterion.id).note.trim(),
    })) });
    const allCriteriaPass = reviewCriteria.every(criterion => resultFor(criterion.id).result === 'pass');
    const someCriterionFails = reviewCriteria.some(criterion => resultFor(criterion.id).result === 'fail');
    const reviewEvidenceTooLong = reviewEvidence.length > 8000;
    // feedback-policy: mutation pending,inline
    const command = useMutation({
        meta: { success: (_data, operation) => operation === 'progress' ? t('feedback.progressSaved', { name: task.title })
            : operation === 'accept' ? t('feedback.accepted', { name: task.title })
                : operation === 'reject' ? t('feedback.changesRequested', { name: task.title })
                    : t('feedback.commandDone', { action: t(`domain.action_${action}`, { defaultValue: action }), name: task.title }) } satisfies MutationFeedbackMeta,
        mutationFn: async (operation: 'progress' | 'command' | 'accept' | 'reject') => {
            if (operation === 'progress') return taskService.progress(task.id, { expected_version: draftVersion, criteria, artifacts: task.progress?.artifacts ?? [] });
            if (operation === 'accept' || operation === 'reject') return taskService.review(task.id, { expected_version: task.version,
                brief_revision: task.brief_revision ?? 0, artifact_revision: task.artifact_revision ?? 0, verdict: operation, reason, evidence: reviewEvidence });
            return taskService.command(task.id, { action, expected_version: task.version, reason,
                iteration_id: action === 'commit' ? Number(iterationId) : undefined,
                expected_revisions: ['commit', 'uncommit'].includes(action) ? commandRevisions : undefined,
                expected_claim_generation: actions.data?.claim_generation, expected_running_run_ids: actions.data?.running_run_ids,
                expected_live_assignment_ids: actions.data?.live_assignment_ids });
        },
        onSuccess: latest => { if (!isActive()) return; if (key) { try { sessionStorage.removeItem(key); } catch { /* Storage may be unavailable. */ } } onDirty(false); onUpdated(latest); },
        onError: () => undefined,
        onSettled: () => { if (isActive()) onPending(false); },
        // feedback-policy: mutation pending,inline
    });
    const chooseIteration = async (value: string) => {
        setIterationId(value); setCommandRevisions(sourceRevisions); targetContext.reset();
        if (!value) return;
        const observed = await targetContext.read('iteration', Number(value));
        if (observed) setCommandRevisions({ ...sourceRevisions, ...observed.expected_revisions });
    };
    const compareCommandContext = async () => {
        const current = (await taskService.getDetail(task.id)).task;
        if (current.version !== task.version || current.iteration_id !== task.iteration_id) throw new Error('Reload current task state before reapplying this command.');
        const source = current.iteration_id !== null && current.iteration_revision ? { [current.iteration_id]: current.iteration_revision } : {};
        const target = action === 'commit' && iterationId ? await planningInputService.readInitial<Iteration>('iteration', Number(iterationId)) : null;
        setCommandRevisions({ ...source, ...target?.expected_revisions }); setContextError(null);
    };
    const run = (operation: 'progress' | 'command' | 'accept' | 'reject') => { onPending(true); command.mutate(operation); };
    const pending = command.isPending;
    const canReview = actions.data?.actions.find(item => item.action === 'review')?.allowed;
    const canAccept = actions.data?.actions.find(item => item.action === 'accept_review')?.allowed;
    const manualActions = ['start_manual', 'resolve_manual', 'block', 'unblock', 'cancel', 'reopen', 'commit', 'uncommit']
        .filter(item => !(offerDispatch && item === 'start_manual'));
    const available = actions.data?.actions.filter(item => item.allowed && manualActions.includes(item.action)) ?? [];
    return <section className="space-y-4 border-t border-border pt-4" aria-labelledby={`${id}-heading`}>
        <h3 id={`${id}-heading`} className="text-base font-semibold text-content-primary">{t('domain.workAndReview')}</h3>
        {task.canceled_at && <p className="text-sm text-content-secondary">{t('domain.canceled')}: {task.canceled_reason}</p>}
        {task.blocked_reason && <p className="text-sm text-feedback-warning-foreground">{t('domain.blocked')}: {task.blocked_reason}</p>}
        <TaskReviewer task={task} />
        {submitBlocked && <div role="alert" className="space-y-2 text-sm text-feedback-warning-foreground">
            <p>{t('domain.submitNeedsCriterion')}</p>
            {onEditBrief && <Button type="button" size="sm" variant="secondary" disabled={disabled} onClick={onEditBrief}>{t('taskView.editBrief')}</Button>}
        </div>}
        {actions.isLoading && <QueryLoadingState className="min-h-12" />}
        {actions.isError && <QueryErrorState error={actions.error} fallback={t('domain.actionsFailed')} onRetry={() => void actions.refetch()} />}
        {Boolean(contextError) && <p role="alert" className="text-sm text-feedback-danger-foreground">{getApiErrorMessage(contextError, t('domain.reloadReview'))}</p>}
        {command.isError && <div role="alert" className="space-y-2 text-sm text-feedback-danger-foreground">
            <p>{getApiErrorMessage(command.error, t('domain.saveFailed'))}</p>
            {['commit', 'uncommit'].includes(action) && <Button type="button" size="sm" variant="secondary" onClick={() => { void compareCommandContext().catch(setContextError); }}>{t('planningInput.reviewAgain')}</Button>}
            <Button type="button" variant="secondary" size="sm" onClick={onReload}>{t('domain.reloadReview')}</Button>
        </div>}
        {staleDraft && <div role="alert" className="space-y-2 text-sm text-feedback-warning-foreground">
            <p>{t('domain.staleProgress')}</p>
            <Button type="button" size="sm" variant="secondary" disabled={pending}
                onClick={() => { setDraftVersion(task.version); setBase(initial); }}>{t('taskEditor.keepDraftWithCurrentVersion')}</Button>
        </div>}
        {task.brief && <fieldset disabled={disabled || pending || reason.length > 0 || Boolean(task.canceled_at) || task.status === 'closed'} className="space-y-3">
            <legend className="mb-2 font-medium text-content-primary">{t('domain.progress')}</legend>
            <p className="text-sm text-content-secondary">{t('domain.progressHelp')}{acceptanceNote && ` ${acceptanceNote}`}</p>
            {criteria.length === 0 && <p className="text-sm text-content-secondary">{t('domain.noCriteria')}</p>}
            {criteria.map(item => <div className="space-y-2" key={item.criterion_id}>
                <label className="field-lbl" htmlFor={`${id}-${item.criterion_id}-state`}>{task.brief?.acceptance_criteria.find(criterion => criterion.id === item.criterion_id)?.text ?? t('domain.retiredCriterion')}</label>
                <Select id={`${id}-${item.criterion_id}-state`} className="input w-full" value={item.state}
                    onChange={event => setCriteria(values => values.map(row => row.criterion_id === item.criterion_id ? { ...row, state: event.target.value as CriterionProgress['state'] } : row))}>
                    {(['pending', 'in_progress', 'completed'] as const).map(state => <option value={state} key={state}>{t(`domain.${state}`)}</option>)}
                </Select>
                <label className="field-lbl" htmlFor={`${id}-${item.criterion_id}-evidence`}>{t('domain.evidence')}</label>
                <textarea id={`${id}-${item.criterion_id}-evidence`} className="input min-h-20 w-full" maxLength={8000} value={item.evidence}
                    onChange={event => setCriteria(values => values.map(row => row.criterion_id === item.criterion_id ? { ...row, evidence: event.target.value } : row))} />
            </div>)}
            <Button type="button" variant="secondary" size="sm" onClick={() => run('progress')} disabled={staleDraft} isLoading={pending}>{t('domain.saveProgress')}</Button>
        </fieldset>}
        {dirty && <div className="flex flex-wrap items-center gap-2 text-sm">
            <span className="text-content-secondary">{t('domain.progressDraft')}</span>
            <Button type="button" variant="ghost" size="sm" disabled={pending} onClick={() => { setCriteria(initial); setReason(''); setDraftVersion(task.version); setBase(initial); }}>{t('domain.discardProgress')}</Button>
        </div>}
        <fieldset disabled={disabled || pending || criteriaDirty || staleDraft || actions.isError || actions.isLoading} className="space-y-3">
            <Input label={t('domain.reason')} required value={reason} maxLength={2000} onChange={event => setReason(event.target.value)} />
            {available.length > 0 ? <div className="flex flex-wrap items-end gap-2">
                <div className="min-w-0 flex-1">
                    <label className="field-lbl" htmlFor={`${id}-action`}>{t('domain.action')}</label>
                    <Select id={`${id}-action`} className="input w-full" value={action} onChange={event => { setAction(event.target.value); setIterationId(''); targetContext.reset(); setCommandRevisions(sourceRevisions); }}>
                        <option value="">{t('domain.chooseAction')}</option>
                        {available.map(item => <option value={item.action} key={item.action}>{t(`domain.action_${item.action}`)}</option>)}
                    </Select>
                </div>
                <Button type="button" variant="secondary" disabled={!reason.trim() || !available.some(item => item.action === action) || submitBlocked && action === 'resolve_manual' || ['commit', 'uncommit'].includes(action) && (targetContext.loading || task.iteration_id !== null && !commandRevisions[task.iteration_id] || action === 'commit' && (!iterationId || !commandRevisions[Number(iterationId)]))}
                    onClick={() => run('command')}>{t('domain.applyAction')}</Button>
            </div> : <p className="text-sm text-content-secondary">{t('domain.noActions')}</p>}
            {action === 'commit' && <div>
                {targetContext.loading && <QueryLoadingState className="min-h-12" />}
                {Boolean(targetContext.error) && <QueryErrorState error={targetContext.error} onRetry={() => void chooseIteration(iterationId)} />}
                {iterations.isLoading && <QueryLoadingState className="min-h-12" />}
                {iterations.isError && <QueryErrorState error={iterations.error} fallback={t('domain.iterationsFailed')} onRetry={() => void iterations.refetch()} />}
                <label className="field-lbl" htmlFor={`${id}-iteration`}>{t('domain.iteration')}</label>
                <Select id={`${id}-iteration`} className="input w-full" value={iterationId} onChange={event => void chooseIteration(event.target.value)}>
                    <option value="">{t('domain.chooseIteration')}</option>
                    {iterations.data?.filter(item => item.project_id === task.project_id || item.project_id === null).map(item => <option key={item.id} value={item.id}>{item.name}</option>)}
                </Select>
            </div>}
            {task.status === 'resolved' && canReview && reviewCriteria.length > 0 && <fieldset className="space-y-3">
                <legend className="mb-1 font-medium text-content-primary">{t('domain.reviewResults')}</legend>
                <p className="text-sm text-content-secondary">{t('domain.reviewResultsHelp')}</p>
                {reviewCriteria.map(criterion => <div key={criterion.id} className="space-y-2">
                    <label className="field-lbl" htmlFor={`${id}-${criterion.id}-result`}>{t('domain.resultFor', { criterion: criterion.text })}</label>
                    <Select id={`${id}-${criterion.id}-result`} className="input w-full" value={resultFor(criterion.id).result}
                        onChange={event => setReviewResults(values => ({ ...values, [criterion.id]: { ...resultFor(criterion.id), result: event.target.value as '' | 'pass' | 'fail' } }))}>
                        <option value="">{t('domain.resultNotChecked')}</option>
                        <option value="pass">{t('domain.resultPass')}</option>
                        <option value="fail">{t('domain.resultFail')}</option>
                    </Select>
                    <label className="field-lbl" htmlFor={`${id}-${criterion.id}-note`}>{t('domain.resultNote')}</label>
                    <textarea id={`${id}-${criterion.id}-note`} className="input min-h-16 w-full" maxLength={1000} value={resultFor(criterion.id).note}
                        onChange={event => setReviewResults(values => ({ ...values, [criterion.id]: { ...resultFor(criterion.id), note: event.target.value } }))} />
                </div>)}
                {reviewEvidenceTooLong && <p role="alert" className="text-sm text-feedback-danger-foreground">{t('domain.reviewEvidenceTooLong')}</p>}
            </fieldset>}
            {task.status === 'resolved' && <p className="text-sm text-content-secondary">{task.assignee?.name
                ? t('domain.reworkOwner', { name: task.assignee.name })
                : t('domain.reworkOwnerNone')}</p>}
            {task.status === 'resolved' && <div className="flex flex-wrap gap-2">
                <Button type="button" disabled={!canAccept || !reason.trim() || JSON.stringify(criteria) !== JSON.stringify(initial) || !allCriteriaPass || reviewEvidenceTooLong} onClick={() => run('accept')}>{t('domain.accept')}</Button>
                <Button type="button" variant="secondary" disabled={!canReview || !reason.trim() || (reviewCriteria.length > 0 && !someCriterionFails) || reviewEvidenceTooLong} onClick={() => run('reject')}>{t('domain.requestRework')}</Button>
            </div>}
        </fieldset>
        <details className="text-sm text-content-secondary">
            <summary className="cursor-pointer">{t('domain.unavailableActions')}</summary>
            <ul className="mt-2 space-y-2">{actions.data?.actions.filter(item => !item.allowed).map(item => <li key={item.action}>
                <span className="font-medium">{t(`domain.action_${item.action}`)}</span>: {item.blockers.map(blocker => blocker.message).join(' ')}
            </li>)}</ul>
        </details>
    </section>;
};

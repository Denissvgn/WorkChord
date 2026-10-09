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

export const TaskWorkPanel = ({ task, disabled, draftKey, onDirty, onPending, onUpdated, onReload }: {
    task: Task; disabled: boolean; draftKey: string | null; onDirty: (dirty: boolean) => void;
    onPending: (pending: boolean) => void; onUpdated: (task: Task) => void; onReload: () => void;
}) => {
    const { t } = useTranslation();
    const isActive = useActiveMount();
    const id = useId();
    const key = draftKey ? `${draftKey}:progress` : null;
    const initial = (task.brief?.acceptance_criteria ?? []).map(criterion => task.progress?.criteria.find(item => item.criterion_id === criterion.id && item.criterion_revision === criterion.revision)
        ?? { criterion_id: criterion.id, criterion_revision: criterion.revision, state: 'pending' as const, evidence: '' });
    const [draftVersion, setDraftVersion] = useState(() => {
        try { const stored = JSON.parse(key ? sessionStorage.getItem(key) ?? 'null' : 'null'); return stored && Number.isInteger(stored.version) && Date.now() - stored.savedAt < 86400000 ? stored.version as number : task.version; } catch { return task.version; }
    });
    const [criteria, setCriteria] = useState<CriterionProgress[]>(() => {
        try {
            const stored = JSON.parse(key ? sessionStorage.getItem(key) ?? 'null' : 'null');
            if (stored && Date.now() - stored.savedAt < 86400000 && Array.isArray(stored.criteria) && stored.criteria.length <= 100
                && stored.criteria.every((item: CriterionProgress) => typeof item.criterion_id === "string" && Number.isInteger(item.criterion_revision)
                    && typeof item.evidence === 'string' && ['pending', 'in_progress', 'completed'].includes(item.state))) return stored.criteria;
        } catch { /* Keep the server evidence when a draft is unavailable. */ }
        return initial;
    });
    const [reason, setReason] = useState(() => { try { const stored = JSON.parse(key ? sessionStorage.getItem(key) ?? 'null' : 'null'); return stored && Date.now() - stored.savedAt < 86400000 && typeof stored.reason === 'string' ? stored.reason : ''; } catch { return ''; } });
    const savedCommand = () => {
        try { const value = JSON.parse(key ? sessionStorage.getItem(key) ?? 'null' : 'null');
            if (value && Date.now() - value.savedAt < 86400000 && typeof value.action === 'string' && value.action.length < 50 && typeof value.iterationId === 'string'
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
            if (dirty) sessionStorage.setItem(key, JSON.stringify({ version: draftVersion, savedAt: Date.now(), criteria, reason, action, iterationId, commandRevisions }));
            else sessionStorage.removeItem(key);
        } catch { /* The in-page draft remains usable. */ }
    }, [dirty, criteria, reason, key, onDirty, draftVersion, action, iterationId, commandRevisions]);
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
    // feedback-policy: mutation pending,inline
    const command = useMutation({
        mutationFn: async (operation: 'progress' | 'command' | 'accept' | 'reject') => {
            if (operation === 'progress') return taskService.progress(task.id, { expected_version: draftVersion, criteria, artifacts: task.progress?.artifacts ?? [] });
            if (operation === 'accept' || operation === 'reject') return taskService.review(task.id, { expected_version: task.version,
                brief_revision: task.brief_revision ?? 0, artifact_revision: task.artifact_revision ?? 0, verdict: operation, reason });
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
    const available = actions.data?.actions.filter(item => item.allowed && ['start_manual', 'resolve_manual', 'block', 'unblock', 'cancel', 'reopen', 'commit', 'uncommit'].includes(item.action)) ?? [];
    return <section className="space-y-4 border-t border-border pt-4" aria-labelledby={`${id}-heading`}>
        <h3 id={`${id}-heading`} className="text-base font-semibold text-content-primary">{t('domain.workAndReview')}</h3>
        {task.canceled_at && <p className="text-sm text-content-secondary">{t('domain.canceled')}: {task.canceled_reason}</p>}
        {task.blocked_reason && <p className="text-sm text-feedback-warning-foreground">{t('domain.blocked')}: {task.blocked_reason}</p>}
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
            <Button type="button" size="sm" variant="secondary" disabled={pending || criteria.some(item => !initial.some(current => current.criterion_id === item.criterion_id && current.criterion_revision === item.criterion_revision))}
                onClick={() => setDraftVersion(task.version)}>{t('taskEditor.keepDraftWithCurrentVersion')}</Button>
        </div>}
        {task.brief && <fieldset disabled={disabled || pending || reason.length > 0 || Boolean(task.canceled_at) || task.status === 'closed'} className="space-y-3">
            <legend className="mb-2 font-medium text-content-primary">{t('domain.progress')}</legend>
            <p className="text-sm text-content-secondary">{t('domain.progressHelp')}</p>
            {criteria.length === 0 && <p className="text-sm text-content-secondary">{t('domain.noCriteria')}</p>}
            {criteria.map(item => <div className="space-y-2" key={item.criterion_id}>
                <label className="field-lbl" htmlFor={`${id}-${item.criterion_id}-state`}>{task.brief?.acceptance_criteria.find(criterion => criterion.id === item.criterion_id)?.text ?? t('domain.retiredCriterion')}</label>
                <select id={`${id}-${item.criterion_id}-state`} className="input w-full" value={item.state}
                    onChange={event => setCriteria(values => values.map(row => row.criterion_id === item.criterion_id ? { ...row, state: event.target.value as CriterionProgress['state'] } : row))}>
                    {(['pending', 'in_progress', 'completed'] as const).map(state => <option value={state} key={state}>{t(`domain.${state}`)}</option>)}
                </select>
                <label className="field-lbl" htmlFor={`${id}-${item.criterion_id}-evidence`}>{t('domain.evidence')}</label>
                <textarea id={`${id}-${item.criterion_id}-evidence`} className="input min-h-20 w-full" maxLength={8000} value={item.evidence}
                    onChange={event => setCriteria(values => values.map(row => row.criterion_id === item.criterion_id ? { ...row, evidence: event.target.value } : row))} />
            </div>)}
            <Button type="button" variant="secondary" size="sm" onClick={() => run('progress')} disabled={staleDraft} isLoading={pending}>{t('domain.saveProgress')}</Button>
        </fieldset>}
        {dirty && <div className="flex flex-wrap items-center gap-2 text-sm">
            <span className="text-content-secondary">{t('domain.progressDraft')}</span>
            <Button type="button" variant="ghost" size="sm" disabled={pending} onClick={() => { setCriteria(initial); setReason(''); setDraftVersion(task.version); }}>{t('domain.discardProgress')}</Button>
        </div>}
        <fieldset disabled={disabled || pending || criteriaDirty || staleDraft || actions.isError || actions.isLoading} className="space-y-3">
            <Input label={t('domain.reason')} value={reason} maxLength={2000} onChange={event => setReason(event.target.value)} />
            {available.length > 0 ? <div className="flex flex-wrap items-end gap-2">
                <div className="min-w-0 flex-1">
                    <label className="field-lbl" htmlFor={`${id}-action`}>{t('domain.action')}</label>
                    <select id={`${id}-action`} className="input w-full" value={action} onChange={event => { setAction(event.target.value); setIterationId(''); targetContext.reset(); setCommandRevisions(sourceRevisions); }}>
                        <option value="">{t('domain.chooseAction')}</option>
                        {available.map(item => <option value={item.action} key={item.action}>{t(`domain.action_${item.action}`)}</option>)}
                    </select>
                </div>
                <Button type="button" variant="secondary" disabled={!reason.trim() || !available.some(item => item.action === action) || ['commit', 'uncommit'].includes(action) && (targetContext.loading || task.iteration_id !== null && !commandRevisions[task.iteration_id] || action === 'commit' && (!iterationId || !commandRevisions[Number(iterationId)]))}
                    onClick={() => run('command')}>{t('domain.applyAction')}</Button>
            </div> : <p className="text-sm text-content-secondary">{t('domain.noActions')}</p>}
            {action === 'commit' && <div>
                {targetContext.loading && <QueryLoadingState className="min-h-12" />}
                {Boolean(targetContext.error) && <QueryErrorState error={targetContext.error} onRetry={() => void chooseIteration(iterationId)} />}
                {iterations.isLoading && <QueryLoadingState className="min-h-12" />}
                {iterations.isError && <QueryErrorState error={iterations.error} fallback={t('domain.iterationsFailed')} onRetry={() => void iterations.refetch()} />}
                <label className="field-lbl" htmlFor={`${id}-iteration`}>{t('domain.iteration')}</label>
                <select id={`${id}-iteration`} className="input w-full" value={iterationId} onChange={event => void chooseIteration(event.target.value)}>
                    <option value="">{t('domain.chooseIteration')}</option>
                    {iterations.data?.filter(item => item.project_id === task.project_id || item.project_id === null).map(item => <option key={item.id} value={item.id}>{item.name}</option>)}
                </select>
            </div>}
            {task.status === 'resolved' && <div className="flex flex-wrap gap-2">
                <Button type="button" disabled={!canAccept || !reason.trim() || JSON.stringify(criteria) !== JSON.stringify(initial)} onClick={() => run('accept')}>{t('domain.accept')}</Button>
                <Button type="button" variant="secondary" disabled={!canReview || !reason.trim()} onClick={() => run('reject')}>{t('domain.requestRework')}</Button>
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

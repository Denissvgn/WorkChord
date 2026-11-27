import { useId, useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import type { TFunction } from 'i18next';
import { taskService } from '../../services/taskService';
import type { ReactivationRequirement, Task } from '../../types/task';
import { getApiErrorMessage } from '../../utils/apiError';
import { formatDate } from '../../utils/formatDate';
import { Button } from '../common/Button';
import { Textarea } from '../common/Textarea';
import { QueryErrorState, QueryLoadingState } from '../feedback/QueryState';
import { useIdentity } from '../../features/identity/identityContext';
import type { MutationFeedbackMeta } from '../../features/mutationFeedback';
import { useActiveMount } from './useDraftDismissal';

/** A live root, so a met requirement that does not change the task's version still refreshes. */
const postponementKey = (taskId: number) => ['taskActions', taskId, 'postponement'];

const requirementText = (t: TFunction, language: string, item: ReactivationRequirement) => {
    if (item.kind === 'date') return t('domain.reqText_date', { date: item.on_date ? formatDate(item.on_date, language) : '' });
    if (item.kind === 'owner_decision') return t('domain.reqText_owner', { description: item.description ?? '' });
    if (item.kind === 'linked_resolved' && item.triage_item_id) return t('domain.reqText_triage', { id: item.triage_item_id });
    if (item.task_id) return t(item.kind === 'predecessor_accepted' ? 'domain.reqText_predecessor' : 'domain.reqText_task', { id: item.task_id });
    return t('domain.reqText_deleted');
};

const OwnerDecision = ({ task, requirement, disabled, onPending, onUpdated }: {
    task: Task; requirement: ReactivationRequirement; disabled: boolean; onPending: (pending: boolean) => void; onUpdated: (task: Task) => void;
}) => {
    const { t } = useTranslation();
    const id = useId();
    const isActive = useActiveMount();
    const [decision, setDecision] = useState('');
    const queryClient = useQueryClient();
    // feedback-policy: mutation pending,inline
    const record = useMutation({
        meta: { success: t('feedback.decisionRecorded', { name: task.title }) } satisfies MutationFeedbackMeta,
        mutationFn: () => taskService.recordOwnerDecision(task.id, requirement.id, { expected_version: task.version, decision: decision.trim() }),
        onSuccess: response => { setDecision(''); queryClient.setQueryData(postponementKey(task.id), response.postponement); void queryClient.invalidateQueries({ queryKey: ['taskActions'] }); onUpdated(response.task); },
        onSettled: () => { if (isActive()) onPending(false); },
        // feedback-policy: mutation pending,inline
    });
    return <div className="mt-2 space-y-2">
        <Textarea label={t('domain.decisionLabel')} required value={decision} maxLength={2000} disabled={disabled || record.isPending} onChange={event => setDecision(event.target.value)} />
        {record.isError && <p role="alert" className="text-sm text-feedback-danger-foreground">{getApiErrorMessage(record.error, t('domain.decisionFailed'))}</p>}
        <div className="flex flex-wrap items-center gap-2">
            <Button type="button" size="sm" isLoading={record.isPending} disabled={disabled || !decision.trim()} aria-describedby={!decision.trim() ? `${id}-missing` : undefined}
                onClick={() => { onPending(true); record.mutate(); }}>{t('domain.recordDecision')}</Button>
            {!decision.trim() && <p id={`${id}-missing`} className="text-sm text-content-secondary">{t('domain.decisionNeedsText')}</p>}
        </div>
    </div>;
};

/**
 * What a postponed task is waiting for: the reason, each requirement as met or not met, a place for the
 * owner to record an owner-decision requirement, and Reactivate for a person who may decide.
 */
export const TaskPostponementPanel = ({ task, canReactivate, disabled, disabledReasons = [], onPending, onUpdated }: {
    task: Task; canReactivate: boolean; disabled: boolean; disabledReasons?: string[]; onPending: (pending: boolean) => void; onUpdated: (task: Task) => void;
}) => {
    const { t, i18n } = useTranslation();
    const id = useId();
    const isActive = useActiveMount();
    const identity = useIdentity()?.identity;
    const [reason, setReason] = useState('');
    // feedback-policy: query loading,error,retry,empty
    const postponement = useQuery({ queryKey: postponementKey(task.id), queryFn: async () => (await taskService.getDetail(task.id, { limit: 1 })).postponement ?? null });
    const queryClient = useQueryClient();
    // feedback-policy: mutation pending,inline
    const reactivate = useMutation({
        meta: { success: t('feedback.reactivated', { name: task.title }) } satisfies MutationFeedbackMeta,
        mutationFn: () => taskService.reactivate(task.id, { expected_version: task.version, reason: reason.trim() }),
        onSuccess: response => { setReason(''); queryClient.setQueryData(postponementKey(task.id), response.postponement); onUpdated(response.task); },
        onSettled: () => { if (isActive()) onPending(false); },
        // feedback-policy: mutation pending,inline
    });
    const record = postponement.data ?? null;
    // The server lets the workspace owner, and a trusted-local browser with no signed-in person, record the decision.
    const isOwner = identity !== undefined && identity !== null && identity.access !== 'observe'
        && (identity.principal?.kind === 'human' && identity.workspace_role === 'owner' || identity.mode === 'trusted_local' && !identity.principal);
    const missing = [...disabledReasons, !reason.trim() && t('domain.reactivateNeedsReason')].filter(Boolean);
    return <section className="space-y-3 border-t border-border pt-3" aria-labelledby={`${id}-heading`}>
        <h4 id={`${id}-heading`} className="font-medium text-content-primary">{t('domain.postponedHeading')}</h4>
        {postponement.isLoading && <QueryLoadingState className="min-h-12" />}
        {postponement.isError && <QueryErrorState error={postponement.error} fallback={t('domain.postponementFailed')} onRetry={() => void postponement.refetch()} />}
        {postponement.isSuccess && !record && <p role="status" className="text-sm text-content-secondary">{t('domain.postponementNoRecord')}</p>}
        {record && <div className="space-y-3 text-sm">
            <p className="text-content-secondary">{t('domain.postponedSince', { date: formatDate(record.postponed_at, i18n.language) })}</p>
            <div><p className="font-medium text-content-primary">{t('domain.postponedReason')}</p><p className="whitespace-pre-wrap">{record.reason}</p></div>
            <div>
                <p id={`${id}-waiting`} className="font-medium text-content-primary">{t('domain.waitingFor')}</p>
                <ul aria-labelledby={`${id}-waiting`} className="mt-1 space-y-2">
                    {record.requirements.map(item => <li key={item.id} className="rounded-md border border-border px-3 py-2">
                        <span className={item.met ? 'font-semibold text-feedback-success-foreground' : 'font-semibold text-feedback-warning-foreground'}>{item.met ? t('domain.reqMet') : t('domain.reqUnmet')}</span>
                        {' '}{requirementText(t, i18n.language, item)}
                        {item.met && item.met_at && <span className="text-content-secondary"> ({t('domain.metOn', { date: formatDate(item.met_at, i18n.language) })})</span>}
                        {!item.met && item.kind === 'owner_decision' && (isOwner
                            ? <OwnerDecision task={task} requirement={item} disabled={disabled} onPending={onPending} onUpdated={onUpdated} />
                            : <p role="status" className="mt-1 text-content-secondary">{t('domain.decisionOwnerOnly')}</p>)}
                    </li>)}
                </ul>
            </div>
        </div>}
        {canReactivate && <div className="space-y-2">
            <Textarea label={t('domain.reactivateReason')} required value={reason} maxLength={2000} disabled={disabled || reactivate.isPending} onChange={event => setReason(event.target.value)} />
            {reactivate.isError && <p role="alert" className="text-sm text-feedback-danger-foreground">{getApiErrorMessage(reactivate.error, t('domain.reactivateFailed'))}</p>}
            <div className="flex flex-wrap items-center gap-2">
                <Button type="button" isLoading={reactivate.isPending} disabled={disabled || missing.length > 0} aria-describedby={missing.length ? `${id}-missing` : undefined}
                    onClick={() => { onPending(true); reactivate.mutate(); }}>{t('domain.action_reactivate')}</Button>
                {missing.length > 0 && <p id={`${id}-missing`} className="text-sm text-content-secondary">{missing.join(' ')}</p>}
            </div>
            {record && <p className="text-xs text-content-secondary">{t(`domain.reactivateReturns_${record.from_status === 'resolved' ? 'resolved' : 'planned'}`)}</p>}
        </div>}
    </section>;
};

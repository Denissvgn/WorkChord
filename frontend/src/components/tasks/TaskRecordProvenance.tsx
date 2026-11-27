import { useId, useState } from 'react';
import { useMutation } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { taskService } from '../../services/taskService';
import type { ManualProvenanceExecutor, Task } from '../../types/task';
import { getApiErrorMessage, getApiNextStep } from '../../utils/apiError';
import { Button } from '../common/Button';
import { Input } from '../common/Input';
import { Select } from '../common/Select';
import { Textarea } from '../common/Textarea';
import { useIdentity } from '../../features/identity/identityContext';
import type { MutationFeedbackMeta } from '../../features/mutationFeedback';
import { RefusalNextStepNote } from './RefusalNextStepNote';
import { useActiveMount } from './useDraftDismissal';

const positive = (value: string) => /^[1-9]\d{0,9}$/.test(value.trim()) ? Number(value.trim()) : null;

/**
 * Recording who executed resolved work that was delivered outside recorded runs, and the exact commits they delivered,
 * so a reviewer can be shown to be independent of it. Only a signed-in workspace owner or operator or a project manager is
 * offered the form; everyone else, including a trusted-local browser with no signed-in person, is told why it is
 * unavailable and whom to ask.
 */
export const TaskRecordProvenance = ({ task, disabled, disabledReasons = [], onPending, onUpdated }: {
    task: Task; disabled: boolean; /** Why the action is disabled for a reason outside this form, such as unsaved progress. */ disabledReasons?: string[]; onPending: (pending: boolean) => void; onUpdated: (task: Task) => void;
}) => {
    const { t } = useTranslation();
    const id = useId();
    const isActive = useActiveMount();
    const identity = useIdentity()?.identity;
    const [kind, setKind] = useState<ManualProvenanceExecutor['kind']>('human');
    const [executorId, setExecutorId] = useState('');
    // The artifact revision a record was made for: the form stays closed until the artifact changes or a person asks to record again.
    const [recordedFor, setRecordedFor] = useState<number | null>(null);
    const [bindingId, setBindingId] = useState('');
    const [head, setHead] = useState('');
    const [commits, setCommits] = useState('');
    const [pullRequest, setPullRequest] = useState('');
    const [base, setBase] = useState('');
    const [reason, setReason] = useState('');
    const signedInHuman = identity?.principal?.kind === 'human' && identity.access !== 'observe';
    const operator = identity?.workspace_role === 'owner' || identity?.workspace_role === 'operator';
    const projectManager = task.project_id != null && identity?.projects?.[String(task.project_id)] === 'manager';
    const mayRecord = signedInHuman && (operator || projectManager);
    const trustedLocalBrowser = identity?.mode === 'trusted_local' && !identity.principal;
    const unavailable = !identity ? null : trustedLocalBrowser ? t('domain.provenanceTrustedLocal')
        : mayRecord ? null : t('domain.provenanceNoAuthority');
    const executorNumber = positive(executorId);
    const bindingNumber = bindingId.trim() ? positive(bindingId) : undefined;
    // feedback-policy: mutation pending,inline
    const record = useMutation({
        meta: { success: t('feedback.provenanceRecorded', { name: task.title }) } satisfies MutationFeedbackMeta,
        mutationFn: async () => {
            const executor: ManualProvenanceExecutor = kind === 'human'
                ? { kind, principal_id: executorNumber ?? undefined }
                : { kind, actor_id: executorNumber ?? undefined, ...(bindingNumber ? { model_binding_id: bindingNumber } : {}) };
            await taskService.recordProvenance(task.id, {
                expected_version: task.version, artifact_revision: task.artifact_revision ?? 0, executor, head_commit_url: head.trim(),
                commit_urls: commits.split('\n').map(line => line.trim()).filter(Boolean),
                ...(pullRequest.trim() ? { pr_url: pullRequest.trim() } : {}), ...(base.trim() ? { base_commit_url: base.trim() } : {}),
                reason: reason.trim(),
            });
            return (await taskService.getDetail(task.id)).task;
        },
        onSuccess: latest => { setReason(''); setRecordedFor(task.artifact_revision ?? 0); onUpdated(latest); },
        onSettled: () => { if (isActive()) onPending(false); },
        // feedback-policy: mutation pending,inline
    });
    // Everything that keeps the button disabled is named, so it never looks broken.
    const missing = [...disabledReasons,
        executorNumber === null && t(kind === 'human' ? 'domain.provenanceNeedsPerson' : 'domain.provenanceNeedsAgent'),
        bindingNumber === null && t('domain.provenanceBadBinding'),
        !head.trim() && t('domain.provenanceNeedsHead'),
        !pullRequest.trim() && !base.trim() && t('domain.provenanceNeedsCandidate'),
        !reason.trim() && t('domain.provenanceNeedsReason'),
    ].filter(Boolean);
    const refusalStep = record.isError ? getApiNextStep(record.error) : null;
    return <section className="space-y-3 border-t border-border pt-3" aria-labelledby={`${id}-heading`}>
        <h4 id={`${id}-heading`} className="font-medium text-content-primary">{t('domain.recordProvenance')}</h4>
        <p className="text-sm text-content-secondary">{t('domain.recordProvenanceHelp')}</p>
        {unavailable && <p role="status" className="text-sm text-content-secondary">{unavailable}</p>}
        {mayRecord && recordedFor === (task.artifact_revision ?? 0) && <div className="flex flex-wrap items-center gap-2">
            <p role="status" className="text-sm text-content-secondary">{t('domain.provenanceDone')}</p>
            <Button type="button" size="sm" variant="secondary" onClick={() => setRecordedFor(null)}>{t('domain.provenanceRecordAgain')}</Button>
        </div>}
        {mayRecord && recordedFor !== (task.artifact_revision ?? 0) && <form className="space-y-3" onSubmit={event => { event.preventDefault(); if (missing.length === 0 && !record.isPending) { onPending(true); record.mutate(); } }}>
            <Select label={t('domain.provenanceExecutorKind')} value={kind} disabled={disabled || record.isPending}
                onChange={event => { setKind(event.target.value as ManualProvenanceExecutor['kind']); setExecutorId(''); }}>
                <option value="human">{t('domain.provenanceKindHuman')}</option>
                <option value="agent">{t('domain.provenanceKindAgent')}</option>
            </Select>
            <Input label={t(kind === 'human' ? 'domain.provenancePersonId' : 'domain.provenanceAgentId')} required inputMode="numeric" value={executorId}
                disabled={disabled || record.isPending} onChange={event => setExecutorId(event.target.value)} />
            {kind === 'agent' && <Input label={t('domain.provenanceBindingId')} inputMode="numeric" value={bindingId}
                disabled={disabled || record.isPending} onChange={event => setBindingId(event.target.value)} />}
            <Input label={t('domain.provenanceHead')} required type="url" value={head} maxLength={1000} disabled={disabled || record.isPending}
                onChange={event => setHead(event.target.value)} />
            <Textarea label={t('domain.provenanceCommits')} help={t('domain.provenanceCommitsHelp')} rows={3} value={commits}
                disabled={disabled || record.isPending} onChange={event => setCommits(event.target.value)} />
            <Input label={t('domain.provenancePullRequest')} type="url" value={pullRequest} maxLength={1000} disabled={disabled || record.isPending}
                onChange={event => setPullRequest(event.target.value)} />
            <Input label={t('domain.provenanceBase')} type="url" value={base} maxLength={1000} disabled={disabled || record.isPending}
                onChange={event => setBase(event.target.value)} />
            <Input label={t('domain.provenanceReason')} required value={reason} maxLength={2000} disabled={disabled || record.isPending}
                onChange={event => setReason(event.target.value)} />
            {record.isError && <div role="alert" className="space-y-1 text-sm text-feedback-danger-foreground">
                <p>{getApiErrorMessage(record.error, t('domain.provenanceFailed'))}</p>
                {refusalStep && <RefusalNextStepNote step={refusalStep} />}
            </div>}
            <div className="flex flex-wrap items-center gap-2">
                <Button type="submit" isLoading={record.isPending} aria-describedby={missing.length ? `${id}-missing` : undefined}
                    disabled={disabled || missing.length > 0}>{t('domain.recordProvenance')}</Button>
                {missing.length > 0 && <p id={`${id}-missing`} className="text-sm text-content-secondary">{missing.join(' ')}</p>}
            </div>
        </form>}
    </section>;
};

import { useEffect, useId, useRef, useState } from 'react';
import { useMutation, useQuery } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { taskService } from '../../services/taskService';
import type { Task } from '../../types/task';
import { getApiErrorMessage } from '../../utils/apiError';
import { stateOf } from '../../utils/taskState';
import { Button } from '../common/Button';
import { Select } from '../common/Select';
import { Textarea } from '../common/Textarea';
import { QueryErrorState } from '../feedback/QueryState';
import type { MutationFeedbackMeta } from '../../features/mutationFeedback';
import { useActiveMount } from './useDraftDismissal';

/**
 * Records that closed or accepted work already delivered this task's work: the task is superseded, nothing is
 * reopened, and its dependents, delivery prerequisites and releases move to the successor. The server decides who may.
 */
export const TaskSupersedeForm = ({ task, disabled, disabledReasons = [], onPending, onUpdated }: {
    task: Task; disabled: boolean; /** Why the form cannot be used for a reason outside it, such as unsaved progress. */ disabledReasons?: string[];
    onPending: (pending: boolean) => void; onUpdated: (task: Task) => void;
}) => {
    const { t } = useTranslation();
    const id = useId();
    const isActive = useActiveMount();
    const [open, setOpen] = useState(false);
    const [text, setText] = useState('');
    // The search runs once typing pauses, so each keystroke is not a request.
    const [query, setQuery] = useState('');
    useEffect(() => { const timer = window.setTimeout(() => setQuery(text), 300); return () => window.clearTimeout(timer); }, [text]);
    const [successorId, setSuccessorId] = useState<number | null>(null);
    const [reason, setReason] = useState('');
    const searchRef = useRef<HTMLInputElement>(null);
    const openRef = useRef<HTMLButtonElement>(null);
    const wasOpen = useRef(false);
    // The button that opens the form unmounts with it, so focus follows the form and returns on discard.
    useEffect(() => {
        if (open) searchRef.current?.focus(); else if (wasOpen.current) openRef.current?.focus();
        wasOpen.current = open;
    }, [open]);
    // feedback-policy: query loading,error,retry,empty - the search shows loading, retry and empty feedback.
    const found = useQuery({
        queryKey: ['supersede-successor-search', task.project_id, query], enabled: open && task.project_id != null,
        queryFn: () => taskService.lookup({ project_id: task.project_id ?? undefined, task_status: 'closed', leaf_only: true, q: query.trim() || undefined, limit: 20 }),
    });
    const candidates = found.data?.items.filter(item => item.id !== task.id && stateOf(item) === 'closed') ?? [];
    const successor = candidates.find(item => item.id === successorId) ?? null;
    const reset = () => { setOpen(false); setText(''); setSuccessorId(null); setReason(''); };
    // feedback-policy: mutation pending,inline
    const supersede = useMutation({
        meta: { success: t('stoppedWork.superseded', { name: task.title }) } satisfies MutationFeedbackMeta,
        mutationFn: async () => {
            await taskService.supersede(task.id, { successor_task_id: successor!.id, expected_original_version: task.version,
                expected_successor_version: successor!.version, reason: reason.trim() });
            return (await taskService.getDetail(task.id, { limit: 1 })).task;
        },
        onSuccess: latest => { reset(); onUpdated(latest); },
        onSettled: () => { if (isActive()) onPending(false); },
    });
    const missing = [...disabledReasons, !successor && t('stoppedWork.supersedeNeedsSuccessor'), !reason.trim() && t('stoppedWork.supersedeNeedsReason')].filter(Boolean);
    return <section className="space-y-3 border-t border-border pt-3" aria-labelledby={`${id}-heading`}>
        <h4 id={`${id}-heading`} className="font-medium text-content-primary">{t('stoppedWork.supersedeHeading')}</h4>
        <p className="text-sm text-content-secondary">{t('stoppedWork.supersedeHelp')}</p>
        {!open && <Button ref={openRef} type="button" variant="secondary" disabled={disabled} onClick={() => setOpen(true)}>{t('stoppedWork.supersedeOpen')}</Button>}
        {open && <form className="space-y-4" onSubmit={event => { event.preventDefault(); if (!disabled && missing.length === 0) { onPending(true); supersede.mutate(); } }}>
            <div className="space-y-2">
                <label className="field-lbl" htmlFor={`${id}-search`}>{t('stoppedWork.supersedeSearch')}</label>
                <input ref={searchRef} id={`${id}-search`} className="input w-full" value={text} maxLength={200} disabled={supersede.isPending}
                    onChange={event => { setText(event.target.value); setSuccessorId(null); }} />
                {found.isLoading && <p role="status" className="text-sm text-content-secondary">{t('common.loading')}</p>}
                {found.isSuccess && candidates.length === 0 && <p role="status" className="text-sm text-content-secondary">{t('stoppedWork.supersedeNoCandidates')}</p>}
                {found.isSuccess && found.data.has_more && <p role="status" className="text-sm text-content-secondary">{t('stoppedWork.supersedeMoreMatches')}</p>}
                {found.isError && <QueryErrorState error={found.error} fallback={t('stoppedWork.supersedeSearchFailed')} onRetry={() => void found.refetch()} />}
                <label className="field-lbl" htmlFor={`${id}-successor`}>{t('stoppedWork.supersedeSuccessor')}</label>
                <Select id={`${id}-successor`} className="input w-full" value={successorId ?? ''} disabled={supersede.isPending}
                    onChange={event => setSuccessorId(Number(event.target.value) || null)}>
                    <option value="">{t('stoppedWork.supersedeChoose')}</option>
                    {candidates.map(item => <option key={item.id} value={item.id}>#{item.id} · {item.title}</option>)}
                </Select>
            </div>
            <Textarea label={t('stoppedWork.supersedeReason')} required value={reason} maxLength={4000} disabled={supersede.isPending}
                onChange={event => setReason(event.target.value)} />
            <p className="rounded-md bg-surface-muted px-3 py-2 text-sm text-content-secondary">{t('stoppedWork.supersedeEffect')}</p>
            {supersede.isError && <p role="alert" className="text-sm text-feedback-danger-foreground">{getApiErrorMessage(supersede.error, t('stoppedWork.supersedeFailed'))}</p>}
            <div className="flex flex-wrap items-center gap-2">
                <Button type="submit" isLoading={supersede.isPending} disabled={disabled || missing.length > 0} aria-describedby={missing.length ? `${id}-missing` : undefined}>{t('stoppedWork.supersedeConfirm')}</Button>
                <Button type="button" variant="ghost" disabled={supersede.isPending} onClick={() => { reset(); supersede.reset(); }}>{t('stoppedWork.supersedeCancel')}</Button>
                {missing.length > 0 && <p id={`${id}-missing`} className="w-full text-sm text-content-secondary">{missing.join(' ')}</p>}
            </div>
        </form>}
    </section>;
};

import { useQuery } from '@tanstack/react-query';
import {
    AlertCircle
} from 'lucide-react';
import type { FormEvent } from 'react';
import { useMemo, useState } from 'react';
import { taskService } from '../../services/taskService';
import type { Iteration } from '../../types/iteration';
import type {
    TriageActionRequest,
    TriageDuplicateRequest,
    TriageItem,
    TriageSnoozeRequest
} from '../../types/triage';
import { Button } from '../common/Button';
import { Input, RequiredIndicator } from '../common/Input';
import { Modal } from '../common/Modal';
import { Select } from '../common/Select';
import { QueryErrorState } from '../feedback/QueryState';
import { StatusPill } from './StatusPill';

import { ViewSwitch } from '../ui/ViewSwitch';
import { flattenTasks, optionalText, t, type DuplicateActionDefaults, type TriageLifecycleAction } from './triageUtils';
interface TriageActionModalProps {
    action: TriageLifecycleAction;
    item: TriageItem;
    allTriageItems: TriageItem[];
    iterations: Iteration[];
    selectedIterationId: number;
    defaultSnooze: string;
    defaultDuplicate?: DuplicateActionDefaults;
    isSubmitting: boolean;
    error?: string | null;
    onSubmit: (payload: TriageActionRequest | TriageSnoozeRequest | TriageDuplicateRequest) => void;
    onClose: () => void;
}

export const TriageActionModal = ({
    action,
    item,
    allTriageItems,
    iterations,
    selectedIterationId,
    defaultSnooze,
    defaultDuplicate,
    isSubmitting,
    error,
    onSubmit,
    onClose,
}: TriageActionModalProps) => {
    const fallbackIterationId = defaultDuplicate?.iterationId || item.iteration_hint_id || selectedIterationId || iterations[0]?.id || 0;
    const [reason, setReason] = useState('');
    const [snoozedUntil, setSnoozedUntil] = useState(defaultSnooze);
    const [duplicateTargetType, setDuplicateTargetType] = useState<'triage' | 'task'>(defaultDuplicate?.targetType ?? 'triage');
    const [duplicateItemId, setDuplicateItemId] = useState(
        defaultDuplicate?.targetType === 'triage' ? String(defaultDuplicate.targetId) : ''
    );
    const [duplicateIterationId, setDuplicateIterationId] = useState(String(fallbackIterationId || ''));
    const [duplicateTaskId, setDuplicateTaskId] = useState(
        defaultDuplicate?.targetType === 'task' ? String(defaultDuplicate.targetId) : ''
    );
    const [linkRequestToDuplicateTask, setLinkRequestToDuplicateTask] = useState(
        defaultDuplicate?.targetType === 'task'
    );

    const parsedDuplicateIterationId = Number(duplicateIterationId);
    // feedback-policy: query loading,error,retry,empty - no target keeps submission disabled; errors offer retry.
    const { data: duplicateTasks = [], error: duplicateTasksError, refetch: refetchDuplicateTasks } = useQuery({
        queryKey: ['tasks', parsedDuplicateIterationId],
        queryFn: () => taskService.getByIteration(parsedDuplicateIterationId),
        enabled: action === 'duplicate' && duplicateTargetType === 'task' && parsedDuplicateIterationId > 0,
    });

    const flatDuplicateTasks = useMemo(() => flattenTasks(duplicateTasks), [duplicateTasks]);
    const otherTriageItems = useMemo(
        () => allTriageItems.filter(candidate => candidate.id !== item.id),
        [allTriageItems, item.id]
    );
    const triageDuplicateOptions = useMemo(() => {
        const options = otherTriageItems.map(candidate => ({
            id: candidate.id,
            title: candidate.title,
        }));
        if (
            defaultDuplicate?.targetType === 'triage'
            && !options.some(option => option.id === defaultDuplicate.targetId)
        ) {
            options.unshift({ id: defaultDuplicate.targetId, title: defaultDuplicate.title });
        }
        return options;
    }, [defaultDuplicate, otherTriageItems]);
    const taskDuplicateOptions = useMemo(() => {
        const options = flatDuplicateTasks.map(task => ({
            id: task.id,
            title: task.title,
            depth: task.depth,
        }));
        if (
            defaultDuplicate?.targetType === 'task'
            && !options.some(option => option.id === defaultDuplicate.targetId)
        ) {
            options.unshift({ id: defaultDuplicate.targetId, title: defaultDuplicate.title, depth: 0 });
        }
        return options;
    }, [defaultDuplicate, flatDuplicateTasks]);

    const modalTitle = t({
        accept: 'surfaces.triagePage.acceptIntake',
        decline: 'surfaces.triagePage.declineIntake',
        snooze: 'surfaces.triagePage.snoozeIntake',
        clarify: 'surfaces.triagePage.askForClarification',
        duplicate: 'surfaces.triagePage.markDuplicate',
    }[action]);

    const submitLabel = t({
        accept: 'surfaces.triagePage.accept',
        decline: 'surfaces.triagePage.decline',
        snooze: 'surfaces.triagePage.snooze',
        clarify: 'surfaces.triagePage.askForClarification',
        duplicate: 'surfaces.triagePage.markDuplicate',
    }[action]);

    const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        const trimmedReason = optionalText(reason);

        if (action === 'snooze' || action === 'clarify') {
            onSubmit({
                snoozed_until: new Date(snoozedUntil).toISOString(),
                reason: trimmedReason,
            });
            return;
        }

        if (action === 'duplicate') {
            if (duplicateTargetType === 'triage') {
                onSubmit({
                    duplicate_of_id: Number(duplicateItemId),
                    duplicate_task_id: null,
                    reason: trimmedReason,
                });
                return;
            }
            onSubmit({
                duplicate_of_id: null,
                duplicate_task_id: Number(duplicateTaskId),
                link_request_to_duplicate_task: linkRequestToDuplicateTask,
                reason: trimmedReason,
            });
            return;
        }

        onSubmit({ reason: trimmedReason });
    };

    const duplicateSubmitDisabled = action === 'duplicate'
        && ((duplicateTargetType === 'triage' && !duplicateItemId) || (duplicateTargetType === 'task' && !duplicateTaskId));

    return (
        <Modal open closeLabel={t('surfaces.triagePage.close')} title={modalTitle} onClose={onClose} className="max-w-2xl">
            <form onSubmit={handleSubmit} className="space-y-4">
                {duplicateTasksError && (
                    <QueryErrorState
                        error={duplicateTasksError}
                        fallback={t('queryFeedback.optionLoadFailed')}
                        onRetry={() => void refetchDuplicateTasks()}
                    />
                )}
                {error && (
                    <div className="flex items-start gap-2 rounded-md bg-feedback-danger-muted p-3 text-sm text-feedback-danger-foreground">
                        <AlertCircle className="mt-0.5 h-4 w-4 flex-shrink-0" />
                        <span>{error}</span>
                    </div>
                )}

                <div className="rounded-md border border-border bg-surface-muted p-3">
                    <div className="flex items-center justify-between gap-3">
                        <p className="truncate font-medium text-content-primary">{item.title}</p>
                        <StatusPill status={item.status} />
                    </div>
                    {item.source && <p className="mt-1 text-xs text-content-secondary">{item.source}{item.external_key ? ` / ${item.external_key}` : ''}</p>}
                </div>

                {action === 'clarify' && (
                    <p className="text-sm text-content-secondary">{t('surfaces.triagePage.clarificationHelp')}</p>
                )}

                {(action === 'snooze' || action === 'clarify') && (
                    <Input
                        label={t(action === 'clarify' ? 'surfaces.triagePage.reviewAgainOn' : 'surfaces.triagePage.snoozedUntil')}
                        type="datetime-local"
                        value={snoozedUntil}
                        onChange={event => setSnoozedUntil(event.target.value)}
                        required
                    />
                )}

                {action === 'duplicate' && (
                    <div className="space-y-3">
                        <ViewSwitch label={t('surfaces.triagePage.duplicateOf')} value={duplicateTargetType}
                            options={[{ value: 'triage', label: t('surfaces.triagePage.triageItem') }, { value: 'task', label: t('surfaces.triagePage.task') }]}
                            onChange={value => { setDuplicateTargetType(value); setLinkRequestToDuplicateTask(value === 'task'); }} />

                        {duplicateTargetType === 'triage' ? (
                            <Select label={<>{t('surfaces.triagePage.duplicateOf')}<RequiredIndicator /></>} value={duplicateItemId} onChange={event => setDuplicateItemId(event.target.value)} required><option value="">{t('surfaces.triagePage.selectIntakeItem')}</option>{triageDuplicateOptions.map(candidate => (
                                <option key={candidate.id} value={candidate.id}>
                                    #{candidate.id} {candidate.title}
                                </option>
                            ))}</Select>
                        ) : (
                            <div className="grid grid-cols-1 gap-3 md:grid-cols-2">
                                <Select label={<>{t('surfaces.triagePage.taskIteration')}<RequiredIndicator /></>} value={duplicateIterationId} onChange={event => {
                                    setDuplicateIterationId(event.target.value);
                                    setDuplicateTaskId('');
                                }} required><option value="">{t('surfaces.triagePage.selectIteration')}</option>{iterations.map(iteration => (
                                    <option key={iteration.id} value={iteration.id}>{iteration.name}</option>
                                ))}</Select>
                                <Select label={<>{t('surfaces.triagePage.task')}<RequiredIndicator /></>} value={duplicateTaskId} onChange={event => setDuplicateTaskId(event.target.value)} required disabled={!parsedDuplicateIterationId}><option value="">{t('surfaces.triagePage.selectTask')}</option>{taskDuplicateOptions.map(task => (
                                    <option key={task.id} value={task.id}>
                                        {'-'.repeat(task.depth)} {task.title}
                                    </option>
                                ))}</Select>
                                <label className="flex items-start gap-2 rounded-md border border-action bg-action-muted p-3 text-sm text-action md:col-span-2">
                                    <input
                                        type="checkbox"
                                        checked={linkRequestToDuplicateTask}
                                        onChange={event => setLinkRequestToDuplicateTask(event.target.checked)}
                                        className="mt-0.5 rounded border-action text-action focus:ring-focus"
                                    />
                                    <span>{t('surfaces.triagePage.linkThisIntakeAsARequestOnTheDuplicateTask')}</span>
                                </label>
                            </div>
                        )}
                    </div>
                )}

                <div>
                    <label htmlFor="triage-action-reason" className="mb-1 block text-sm font-medium text-content-primary">
                        {t(action === 'clarify' ? 'surfaces.triagePage.clarificationQuestion' : 'surfaces.triagePage.reason')}
                        {action === 'clarify' && <RequiredIndicator />}
                    </label>
                    <textarea
                        id="triage-action-reason"
                        value={reason}
                        required={action === 'clarify'}
                        onChange={event => setReason(event.target.value)}
                        className="min-h-[90px] w-full rounded-md border border-border-strong px-3 py-2 shadow-sm focus:border-action focus:outline-none focus:ring-1 focus:ring-focus"
                    />
                </div>

                <div className="flex justify-end gap-2 pt-2">
                    <Button type="button" variant="ghost" onClick={onClose}>{t('surfaces.triagePage.cancel')}</Button>
                    <Button type="submit" isLoading={isSubmitting} disabled={duplicateSubmitDisabled}>
                        {submitLabel}
                    </Button>
                </div>
            </form>
        </Modal>
    );
};


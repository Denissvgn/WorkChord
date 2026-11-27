import { useEffect, useRef, useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import type { RoutingCheck, RoutingResolution, Task, TaskRouting } from '../../types/task';
import { taskService } from '../../services/taskService';
import { getApiErrorMessage } from '../../utils/apiError';
import { routingCheckFromError, routingNeedsResolution, routingShape } from '../../utils/routingCheck';
import { Button } from '../common/Button';
import { QueryErrorState } from '../feedback/QueryState';
import { useToast } from '../feedback/toast';
import { AssigneeSelect } from './AssigneeSelect';
import { RoutingCheckNotice } from './RoutingCheckNotice';
import { useAssigneeOptions } from './useTaskRowEdits';

/**
 * Reassigns one task from its page. Before anything is saved the server checks the task's
 * routing against the chosen assignee and the project's review policy, so a conflict and the
 * suggested reviewer are shown first; the person then reassigns with the suggestion, or, where
 * the project only warns, without it.
 */
export const TaskReassign = ({ task, disabled = false, focusOnMount = false, onTaskUpdated, onPending, onSaved }: {
    task: Task;
    disabled?: boolean;
    onTaskUpdated: (task: Task) => void;
    onPending: (pending: boolean) => void;
    /** Put focus on the assignee control when this mounts, after a save that replaced the view. */
    focusOnMount?: boolean;
    /** The reassignment was saved; called before the updated task is handed on. */
    onSaved?: (updated: Task) => void;
}) => {
    const { t } = useTranslation();
    const queryClient = useQueryClient();
    const toast = useToast();
    const { options, error: optionsError, refetch: refetchOptions } = useAssigneeOptions(task.iteration_id);
    const formRef = useRef<HTMLFormElement>(null);
    useEffect(() => { if (focusOnMount) formRef.current?.querySelector('select')?.focus(); }, [focusOnMount]);
    const [choice, setChoice] = useState<number | null | undefined>(undefined);
    const [refused, setRefused] = useState<RoutingCheck | null>(null);
    const changing = choice !== undefined && choice !== (task.assignee?.id ?? null);
    const assigneeToCheck = changing && choice !== null ? choice : null;
    // feedback-policy: query loading,error,retry,empty - saving waits for the routing check; a failed check offers retry.
    const check = useQuery({
        queryKey: ['tasks', 'routing-check', task.id, task.version, assigneeToCheck],
        queryFn: () => taskService.routingCheck(task.id, assigneeToCheck),
        enabled: assigneeToCheck !== null,
    });
    const activeCheck = refused ?? (assigneeToCheck !== null ? check.data ?? null : null);
    const needsResolution = routingNeedsResolution(activeCheck);
    const chosenName = options.find(option => option.id === choice)?.name ?? t('common.unassigned');

    // feedback-policy: mutation pending,inline - the result is announced here and the refused change keeps its conflict on screen.
    const save = useMutation({
        mutationFn: ({ resolution }: { resolution: RoutingResolution; shown: TaskRouting | null }) => taskService.update(task.id, {
            assignee_id: choice ?? null, expected_version: task.version, routing_resolution: resolution,
        }),
        onMutate: () => onPending(true),
        onSuccess: (updated, { resolution, shown }) => {
            setChoice(undefined);
            setRefused(null);
            onSaved?.(updated);
            onTaskUpdated(updated);
            void queryClient.invalidateQueries({ queryKey: ['tasks'] });
            void queryClient.invalidateQueries({ queryKey: ['workload'] });
            toast.success(t('taskReassign.reassigned', { title: updated.title }));
            // What was saved is what the server made of the suggestion; say so when it is not what was shown.
            if (resolution === 'apply_suggestion' && shown && routingShape(updated.brief?.routing) !== routingShape(shown)) {
                toast.info(t('taskReassign.savedDiffers', { title: updated.title }));
            }
        },
        onError: error => setRefused(routingCheckFromError(error)),
        onSettled: () => onPending(false),
    });

    const choose = (next: number | null | undefined) => {
        setChoice(next);
        setRefused(null);
        save.reset();
    };
    const waiting = assigneeToCheck !== null && !refused && (check.isLoading || check.isError);
    const canSave = changing && !waiting && !disabled && !save.isPending;
    const refuses = needsResolution && activeCheck.conflict_mode === 'refuse';
    const suggestion = needsResolution && Boolean(activeCheck.suggestion);
    const refusedMessage = save.isError && !refused ? getApiErrorMessage(save.error, t('taskReassign.reassignFailed')) : null;

    return (
        <form ref={formRef} className="flex flex-col gap-3" aria-label={t('taskReassign.reassignForm')}
            onSubmit={event => { event.preventDefault(); if (canSave && !needsResolution) save.mutate({ resolution: 'check', shown: null }); }}>
            <div className="flex flex-wrap items-end gap-3">
                <label className="flex flex-col gap-1 text-xs text-content-secondary">
                    {t('taskReassign.reassignTo')}
                    <AssigneeSelect aria-label={t('taskReassign.reassignTo')} value={choice === undefined ? task.assignee?.id ?? null : choice}
                        options={options} emptyLabel={t('common.unassigned')} disabled={disabled || save.isPending || task.iteration_id === null}
                        className="h-9 min-w-48 rounded-md border border-border-strong bg-surface-card px-2 text-sm text-content-primary focus:outline-hidden focus-visible:ring-2 focus-visible:ring-focus"
                        onChange={choose} />
                </label>
            </div>
            {/* Mounted before it has text, so a conflict that appears is announced. */}
            <p role="status" className="sr-only">{needsResolution && changing ? t('taskReassign.conflictStatus', { name: chosenName }) : ''}</p>
            {optionsError != null && <QueryErrorState error={optionsError} fallback={t('queryFeedback.optionLoadFailed')} onRetry={() => void refetchOptions()} />}
            {assigneeToCheck !== null && !refused && check.isLoading && <p role="status" className="text-sm text-content-secondary">{t('taskReassign.checking')}</p>}
            {assigneeToCheck !== null && !refused && check.isError && (
                <QueryErrorState error={check.error} fallback={t('taskReassign.checkFailed')} onRetry={() => void check.refetch()} />
            )}
            {activeCheck && changing && <RoutingCheckNotice check={activeCheck} assigneeName={chosenName} />}
            {changing && (
                <div className="flex flex-wrap items-center gap-2">
                    {!needsResolution && !waiting && <Button type="submit" size="sm" disabled={!canSave} isLoading={save.isPending}>{t('taskReassign.reassign')}</Button>}
                    {needsResolution && suggestion && <Button type="button" size="sm" disabled={!canSave} isLoading={save.isPending} onClick={() => save.mutate({ resolution: 'apply_suggestion', shown: activeCheck?.suggestion ?? null })}>{t('taskReassign.reassignWithSuggestion')}</Button>}
                    {needsResolution && !refuses && <Button type="button" size="sm" variant="secondary" disabled={!canSave} onClick={() => save.mutate({ resolution: 'check', shown: null })}>{t('taskReassign.reassignAnyway')}</Button>}
                    <Button type="button" size="sm" variant="ghost" disabled={save.isPending} onClick={() => choose(undefined)}>{t('actions.cancel')}</Button>
                </div>
            )}
            {refusedMessage && <p role="alert" className="text-sm text-feedback-danger-foreground">{refusedMessage}</p>}
        </form>
    );
};

import { useId, useRef, useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { Layers } from 'lucide-react';
import { taskService } from '../../services/taskService';
import { Button } from '../common/Button';
import { Modal } from '../common/Modal';
import { QueryErrorState } from '../feedback/QueryState';
import { useToast } from '../feedback/toast';
import { getApiErrorMessage } from '../../utils/apiError';

interface TaskMergeDialogProps {
    iterationId: number;
    /** The tasks to merge, all in `iterationId`. Mounted only while the dialog is open. */
    taskIds: number[];
    onClose: () => void;
    /** Called once the merge is saved. */
    onMerged: () => void;
}

/** Merges two or more tasks of one iteration under a new parent task, with an undo in the toast. */
export const TaskMergeDialog = ({ iterationId, taskIds, onClose, onMerged }: TaskMergeDialogProps) => {
    const { t } = useTranslation();
    const toast = useToast();
    const queryClient = useQueryClient();
    const titleRef = useRef<HTMLInputElement>(null);
    const titleId = useId();
    const [parentTitle, setParentTitle] = useState('');
    // feedback-policy: query loading,error,retry,empty - the dialog needs only the iteration revision; the list behind it shows the load failure.
    const { data: tasks, refetch } = useQuery({ queryKey: ['tasks', iterationId], queryFn: () => taskService.getByIteration(iterationId) });
    // The revision seen when the dialog opened; a failed merge asks to review again before another try.
    const [revision, setRevision] = useState<number | undefined>(() => tasks?.[0]?.iteration_revision);
    const mergeRevision = revision ?? tasks?.[0]?.iteration_revision;

    // feedback-policy: mutation pending,inline,toast - the dialog stays open with the error and a retry; success reports through the toast with an undo.
    const mutation = useMutation({
        mutationFn: (data: { task_ids: number[]; parent_title: string; expected_revision: number }) => taskService.mergeTasks(iterationId, data),
        onSuccess: (parent, variables) => {
            queryClient.invalidateQueries({ queryKey: ['tasks', iterationId] });
            queryClient.invalidateQueries({ queryKey: ['gantt'] });
            toast.success(t('taskList.mergeSuccess', { count: variables.task_ids.length }), {
                dedupeKey: `task-merge-${parent.id}`,
                durationMs: 10_000,
                actionLabel: t('taskList.undo'),
                onAction: async () => {
                    try {
                        await taskService.unmergeTask(parent.id, true, parent.iteration_revision);
                        await Promise.all([
                            queryClient.invalidateQueries({ queryKey: ['tasks', iterationId] }),
                            queryClient.invalidateQueries({ queryKey: ['gantt'] }),
                            queryClient.invalidateQueries({ queryKey: ['workload'] }),
                        ]);
                        toast.success(t('taskList.mergeRestored'));
                    } catch (error) {
                        toast.error(getApiErrorMessage(error, t('taskList.mergeUndoFailed')));
                        throw error;
                    }
                },
            });
            onMerged();
            onClose();
        },
    });

    const confirm = () => {
        if (taskIds.length >= 2 && parentTitle.trim() && mergeRevision !== undefined) {
            mutation.mutate({ task_ids: taskIds, parent_title: parentTitle.trim(), expected_revision: mergeRevision });
        }
    };

    return (
        <Modal
            open
            title={<span className="flex items-center gap-2 text-feedback-indigo"><Layers className="h-5 w-5" />{t('taskList.mergeModalTitle')}</span>}
            closeLabel={t('actions.close')}
            onClose={() => { if (!mutation.isPending) onClose(); }}
            closeDisabled={mutation.isPending}
            initialFocusRef={titleRef}
            className="max-w-md"
        >
            {mutation.isError && <Button type="button" variant="secondary" disabled={mutation.isPending} onClick={() => {
                void refetch().then(result => setRevision(result.data?.[0]?.iteration_revision));
            }}>{t('planningInput.reviewAgain')}</Button>}
            <p className="mb-4 text-content-secondary">{t('taskList.selectedTasks', { count: taskIds.length })}</p>
            <div className="mb-4">
                <label className="mb-1 block text-sm font-medium text-content-primary" htmlFor={titleId}>{t('taskList.parentTitleLabel')}</label>
                <input
                    id={titleId}
                    ref={titleRef}
                    type="text"
                    value={parentTitle}
                    onChange={event => setParentTitle(event.target.value)}
                    placeholder={t('taskList.parentTitlePlaceholder')}
                    className="w-full rounded-md border border-border-strong px-3 py-2 focus:outline-hidden focus:ring-2 focus:ring-focus"
                />
            </div>
            {mutation.isError && (
                <QueryErrorState
                    className="mb-4"
                    error={mutation.error}
                    fallback={t('taskList.mergeFailed')}
                    onRetry={() => { if (mutation.variables) mutation.mutate(mutation.variables); }}
                />
            )}
            <div className="flex justify-end gap-3">
                <Button variant="secondary" onClick={onClose} disabled={mutation.isPending}>{t('actions.cancel')}</Button>
                <Button variant="primary" onClick={confirm} disabled={mergeRevision === undefined || !parentTitle.trim() || mutation.isPending} isLoading={mutation.isPending}>
                    {t('taskList.mergeTasks')}
                </Button>
            </div>
        </Modal>
    );
};

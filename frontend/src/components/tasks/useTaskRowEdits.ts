import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { taskService } from '../../services/taskService';
import { teamService } from '../../services/teamService';
import { canTransition } from '../../features/taskTransitions';
import type { MutationFeedbackMeta } from '../../features/mutationFeedback';
import type { Task, TaskStatus } from '../../types/task';
import type { TaskRowAssigneeOption } from './TaskRow';

type RowTarget = { id: number; title: string; status: TaskStatus; version: number };

/** The people and agents a task in this iteration can be given to; empty without an iteration. */
export const useAssigneeOptions = (iterationId: number | null) => {
    // feedback-policy: query loading,error,retry,empty - the list shows the load failure with a retry; the picker keeps only Unassigned and the current assignee until it loads.
    const { data = [], error, refetch } = useQuery({
        queryKey: ['team', iterationId],
        queryFn: () => teamService.getByIteration(iterationId as number),
        enabled: iterationId !== null,
    });
    const options: TaskRowAssigneeOption[] = data.map(member => ({ id: member.id, name: member.name, kind: member.profile?.profile_kind }));
    return { options, error, refetch };
};

/** Inline writes for a task row: a status move and a new assignee, each reversible from the toast. */
export const useTaskRowEdits = () => {
    const queryClient = useQueryClient();
    const { t } = useTranslation();
    const refresh = () => Promise.all([
        queryClient.invalidateQueries({ queryKey: ['tasks'] }),
        queryClient.invalidateQueries({ queryKey: ['workload'] }),
        queryClient.invalidateQueries({ queryKey: ['gantt'] }),
        queryClient.invalidateQueries({ queryKey: ['human-my-work'] }),
    ]);

    // feedback-policy: mutation pending,toast - one write at a time; the global listener announces the result and the failure.
    const statusMutation = useMutation({
        mutationFn: ({ task, status }: { task: RowTarget; status: TaskStatus }) => taskService.changeStatus(task.id, status, undefined, task.version),
        meta: {
            success: (data) => t('feedback.statusChanged', { name: (data as { task: Task }).task.title, status: t(`statuses.${(data as { task: Task }).task.status}`) }),
            undo: (data, variables) => {
                const changed = (data as { task: Task }).task;
                const { task } = variables as { task: RowTarget };
                if (!canTransition(changed.status, task.status)) return null;
                return { run: () => taskService.changeStatus(changed.id, task.status, t('feedback.undoReason'), changed.version) };
            },
        } satisfies MutationFeedbackMeta,
        onSuccess: () => refresh(),
    });

    // feedback-policy: mutation pending,toast - one write at a time; the global listener announces the result and the failure.
    const assignMutation = useMutation({
        mutationFn: ({ task, assigneeId }: { task: RowTarget; assigneeId: number | null }) => taskService.update(task.id, { assignee_id: assigneeId, expected_version: task.version }),
        meta: { success: (data) => t('feedback.saved', { kind: t('feedback.kinds.task'), name: (data as Task).title }) } satisfies MutationFeedbackMeta,
        onSuccess: () => refresh(),
    });

    const pending = statusMutation.isPending || assignMutation.isPending;
    return {
        changeStatus: (task: RowTarget, status: TaskStatus) => { if (!pending) statusMutation.mutate({ task, status }); },
        assign: (task: RowTarget, assigneeId: number | null) => { if (!pending) assignMutation.mutate({ task, assigneeId }); },
        pending,
    };
};

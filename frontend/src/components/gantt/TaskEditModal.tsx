import { useMemo, useState } from 'react';
import { Loader2 } from 'lucide-react';
import { useQuery } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { taskService } from '../../services/taskService';
import { teamService } from '../../services/teamService';
import type { GanttTask } from '../../types/gantt';
import type { Task, TaskUpdate } from '../../types/task';
import { Button } from '../common/Button';
import { ConfirmDialog } from '../common/ConfirmDialog';
import { TaskForm } from '../tasks/TaskForm';
import { SlideOverDrawer } from '../ui/SlideOverDrawer';
import { QueryErrorState } from '../feedback/QueryState';

interface TaskEditModalProps {
    task: GanttTask | null;
    iterationId: number;
    isOpen: boolean;
    onClose: () => void;
    sandboxMode?: boolean;
    onSaveSandbox?: (taskId: number, updatedData: Partial<GanttTask>) => void;
}

const mergeGanttDraft = (task: GanttTask, fullTask: Task): Task => ({
    ...fullTask,
    title: task.title,
    description: task.description ?? fullTask.description,
    project_id: task.project_id ?? fullTask.project_id,
    milestone_id: task.milestone_id ?? fullTask.milestone_id,
    priority: task.priority,
    effort_days: task.effort_days,
    effort_hours: task.effort_hours ?? fullTask.effort_hours,
    assignee: task.assignee ?? fullTask.assignee,
    status: task.status,
    min_start_date: task.min_start_date,
    max_end_date: task.max_end_date,
    is_optional: task.is_optional,
    is_deferred: task.is_deferred ?? fullTask.is_deferred,
    tags: task.tags,
    dependencies: task.dependencies,
    version: task.version ?? fullTask.version,
});

export const TaskEditModal = ({
    task,
    iterationId,
    isOpen,
    onClose,
    sandboxMode = false,
    onSaveSandbox,
}: TaskEditModalProps) => {
    if (!isOpen || !task) return null;

    return (
        <TaskEditModalContent
            key={`${task.id}:${sandboxMode ? 'sandbox' : 'direct'}`}
            task={task}
            iterationId={iterationId}
            onClose={onClose}
            sandboxMode={sandboxMode}
            onSaveSandbox={onSaveSandbox}
        />
    );
};

interface TaskEditModalContentProps {
    task: GanttTask;
    iterationId: number;
    onClose: () => void;
    sandboxMode: boolean;
    onSaveSandbox?: (taskId: number, updatedData: Partial<GanttTask>) => void;
}

const TaskEditModalContent = ({
    task,
    iterationId,
    onClose,
    sandboxMode,
    onSaveSandbox,
}: TaskEditModalContentProps) => {
    const { t } = useTranslation();
    const [dirty, setDirty] = useState(false);
    const [showDiscardWarning, setShowDiscardWarning] = useState(false);
    const { data: fullTask, isLoading, isError, refetch } = useQuery({
        queryKey: ['task', task.id],
        queryFn: () => taskService.getById(task.id),
    });
    const { data: teamMembers = [], isError: teamError, error: teamQueryError, refetch: refetchTeam } = useQuery({
        queryKey: ['team', iterationId],
        queryFn: () => teamService.getByIteration(iterationId),
    });
    const editorTask = useMemo(
        () => fullTask ? mergeGanttDraft(task, fullTask) : null,
        [fullTask, task],
    );

    const requestClose = () => {
        if (dirty) {
            setShowDiscardWarning(true);
            return;
        }
        onClose();
    };

    const saveSandbox = (update: TaskUpdate) => {
        const assignee = update.assignee_id == null
            ? null
            : teamMembers.find(member => member.id === update.assignee_id) ?? null;
        onSaveSandbox?.(task.id, {
            title: update.title,
            description: update.description,
            project_id: update.project_id,
            milestone_id: update.milestone_id,
            priority: update.priority,
            effort_days: update.effort_days,
            effort_hours: update.effort_hours,
            assignee: assignee ? { id: assignee.id, name: assignee.name } : null,
            status: update.status as GanttTask['status'],
            min_start_date: update.min_start_date,
            max_end_date: update.max_end_date,
            is_optional: update.is_optional,
            is_deferred: update.is_deferred,
            tags: update.tags,
            dependencies: update.depends_on,
            version: update.expected_version,
            sandbox_update: update,
        });
    };

    return (
        <SlideOverDrawer
            open
            title={t('taskEditor.editTask')}
            subtitle={t('taskEditor.taskCode', { id: task.id })}
            ariaLabel={t('taskEditor.editTask')}
            closeLabel={t('taskEditor.close')}
            onClose={requestClose}
            className="max-w-2xl"
        >
                    <div className="flex min-h-full flex-col p-6">
                        {isLoading && (
                            <div className="flex flex-1 items-center justify-center gap-2 text-content-secondary">
                                <Loader2 className="h-5 w-5 animate-spin" />
                                {t('common.loading')}
                            </div>
                        )}
                        {isError && (
                            <div role="alert" className="space-y-3 rounded-md border border-feedback-danger-border bg-feedback-danger-muted p-4 text-feedback-danger-foreground">
                                <p>{t('taskEditor.loadFailed')}</p>
                                <Button type="button" size="sm" variant="secondary" onClick={() => refetch()}>
                                    {t('taskEditor.retry')}
                                </Button>
                            </div>
                        )}
                        {teamError && <QueryErrorState error={teamQueryError} onRetry={() => void refetchTeam()} fallback={t('queryFeedback.optionLoadFailed')} />}
                        {editorTask && (
                            <TaskForm
                                iterationId={iterationId}
                                initialData={editorTask}
                                mode={sandboxMode ? 'sandbox' : 'direct'}
                                onSaveSandbox={saveSandbox}
                                onDirtyChange={setDirty}
                                confirmUnsavedOnCancel={false}
                                onSuccess={onClose}
                                onCancel={requestClose}
                            />
                        )}
                    </div>
            <ConfirmDialog
                open={showDiscardWarning}
                title={t('taskEditor.unsavedTitle')}
                description={t('taskEditor.unsavedBody')}
                confirmLabel={t('taskEditor.discard')}
                cancelLabel={t('taskEditor.keepEditing')}
                closeLabel={t('actions.close')}
                tone="warning"
                onCancel={() => setShowDiscardWarning(false)}
                onConfirm={onClose}
            />
        </SlideOverDrawer>
    );
};

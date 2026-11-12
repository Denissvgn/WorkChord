import { useCallback } from 'react';
import { useQuery } from '@tanstack/react-query';
import { teamService } from '../../services/teamService';
import type { GanttTask } from '../../types/gantt';
import type { Task, TaskUpdate } from '../../types/task';
import { TaskEditorDrawer } from '../tasks/TaskEditorDrawer';

interface TaskEditModalProps {
    task: GanttTask | null;
    iterationId: number;
    isOpen: boolean;
    onClose: () => void;
    sandboxMode?: boolean;
    onSaveSandbox?: (taskId: number, updatedData: Partial<GanttTask>) => void;
}

/** Layers the unsaved preview edits shown on the chart over the task as last saved. */
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

/**
 * Opens a Gantt task in the same task drawer as the other views: read first, with
 * "Edit all fields" for the full form. While previewing changes, it opens straight
 * in the form and keeps the edits in the preview instead of saving them.
 */
export const TaskEditModal = ({
    task,
    iterationId,
    isOpen,
    onClose,
    sandboxMode = false,
    onSaveSandbox,
}: TaskEditModalProps) => {
    // Names the chosen assignee on the preview bar. The form reads the same query for its assignee
    // picker and owns its loading, error and retry, so a member can only be picked once this has data.
    const { data: teamMembers = [] } = useQuery({
        queryKey: ['team', iterationId],
        queryFn: () => teamService.getByIteration(iterationId),
        enabled: isOpen && sandboxMode,
    });
    const prepareTask = useCallback(
        (fullTask: Task) => (task ? mergeGanttDraft(task, fullTask) : fullTask),
        [task],
    );

    const saveSandbox = (update: TaskUpdate) => {
        if (!task) return;
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
        <TaskEditorDrawer
            taskId={task?.id ?? null}
            iterationId={iterationId}
            open={isOpen && !!task}
            onClose={onClose}
            mode={sandboxMode ? 'sandbox' : 'direct'}
            prepareTask={sandboxMode ? prepareTask : undefined}
            onSaveSandbox={saveSandbox}
        />
    );
};

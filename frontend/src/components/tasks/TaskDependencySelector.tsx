import i18n from '../../i18n/i18n';
import { useQuery } from '@tanstack/react-query';
import { taskService } from '../../services/taskService';
import type { Task } from '../../types/task';
import { QueryErrorState, QueryLoadingState } from '../feedback/QueryState';

const t = i18n.t.bind(i18n);

interface TaskDependencySelectorProps {
    iterationId: number;
    currentTaskId?: number;
    selectedIds: number[];
    onChange: (ids: number[]) => void;
}

export const TaskDependencySelector = ({ iterationId, currentTaskId, selectedIds, onChange }: TaskDependencySelectorProps) => {
    const tasksQuery = useQuery({
        queryKey: ['tasks', iterationId],
        queryFn: () => taskService.getByIteration(iterationId),
    });
    const tasks = tasksQuery.data;

    const handleChange = (taskId: number, checked: boolean) => {
        if (checked) {
            onChange([...selectedIds, taskId]);
        } else {
            onChange(selectedIds.filter(id => id !== taskId));
        }
    };

    // Flatten task tree with depth
    const flatTasks: { id: number, title: string, depth: number }[] = [];
    const flatten = (nodes: Task[], depth: number = 0) => {
        nodes.forEach(node => {
            flatTasks.push({ id: node.id, title: node.title, depth });
            if (node.children) flatten(node.children, depth + 1);
        });
    };
    if (tasks) flatten(tasks);

    return (
        <div className="space-y-1">
            {tasksQuery.isLoading && <QueryLoadingState className="min-h-16 py-3" />}
            {tasksQuery.isError && (
                <QueryErrorState
                    error={tasksQuery.error}
                    fallback={t('queryFeedback.optionLoadFailed')}
                    onRetry={() => void tasksQuery.refetch()}
                />
            )}
            {flatTasks
                .filter(t => t.id !== currentTaskId) // Cannot depend on self
                .map(task => (
                    <label
                        key={task.id}
                        className="flex items-center gap-2 p-1 hover:bg-surface-subtle rounded"
                        style={{ paddingLeft: `${task.depth * 1}rem` }}
                    >
                        <input
                            type="checkbox"
                            checked={selectedIds.includes(task.id)}
                            onChange={(e) => handleChange(task.id, e.target.checked)}
                            className="rounded border-border-strong text-action focus:ring-focus flex-shrink-0"
                        />
                        <span className="text-sm truncate" title={task.title}>{task.title}</span>
                    </label>
                ))}
            {!tasksQuery.isLoading && !tasksQuery.isError && flatTasks.length === 0 && <span className="text-xs text-content-tertiary">{t('surfaces.taskDependencies.noOtherTasksAvailable')}</span>}
        </div>
    );
};

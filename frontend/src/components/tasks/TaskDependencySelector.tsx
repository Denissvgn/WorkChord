import i18n from '../../i18n/i18n';
import { useQuery } from '@tanstack/react-query';
import { taskService } from '../../services/taskService';
import { useState } from 'react';
import { Input } from '../common/Input';
import { Button } from '../common/Button';
import { QueryErrorState, QueryLoadingState } from '../feedback/QueryState';

const t = i18n.t.bind(i18n);

interface TaskDependencySelectorProps {
    iterationId: number | null;
    projectId?: number | null;
    currentTaskId?: number;
    selectedIds: number[];
    onChange: (ids: number[]) => void;
}

export const TaskDependencySelector = ({ iterationId, projectId, currentTaskId, selectedIds, onChange }: TaskDependencySelectorProps) => {
    const [search, setSearch] = useState('');
    const [afterId, setAfterId] = useState(0);
    const tasksQuery = useQuery({
        queryKey: ['taskLookup', iterationId, projectId, search, afterId],
        queryFn: () => taskService.lookup({ iteration_id: iterationId ?? undefined, project_id: projectId ?? undefined,
            backlog_only: iterationId === null, q: search || undefined, after_id: afterId, limit: 50 }),
        enabled: iterationId !== null || projectId != null,
        // feedback-policy: query loading,error,retry,empty
    });
    const flatTasks = tasksQuery.data?.items ?? [];

    const handleChange = (taskId: number, checked: boolean) => {
        if (checked) {
            onChange([...selectedIds, taskId]);
        } else {
            onChange(selectedIds.filter(id => id !== taskId));
        }
    };

    return (
        <div className="space-y-2">
            <Input label={t("domain.findDependency")} value={search} maxLength={200} onChange={event => { setSearch(event.target.value); setAfterId(0); }} />
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
            <div className="flex gap-2">
                {afterId > 0 && <Button type="button" size="sm" variant="ghost" onClick={() => setAfterId(0)}>{t("domain.firstPage")}</Button>}
                {tasksQuery.data?.has_more && <Button type="button" size="sm" variant="secondary" onClick={() => setAfterId(tasksQuery.data!.next_after_id!)}>{t("domain.moreResults")}</Button>}
            </div>
            {!tasksQuery.isLoading && !tasksQuery.isError && flatTasks.length === 0 && <span className="text-xs text-content-tertiary">{t('surfaces.taskDependencies.noOtherTasksAvailable')}</span>}
        </div>
    );
};

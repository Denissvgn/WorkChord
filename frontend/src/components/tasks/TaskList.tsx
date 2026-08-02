import { useEffect, useMemo, useRef, useState } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import {
    ChevronRight, ChevronDown, CheckCircle2, Circle,
    Trash2, Plus, Edit, CornerDownRight, AlertTriangle, ArrowUpDown, GripVertical, Layers, Unlink, Bot, ClipboardCheck
} from 'lucide-react';
import { taskService } from '../../services/taskService';
import { labelService } from '../../services/labelService';
import { Button } from '../common/Button';
import { ConfirmDialog } from '../common/ConfirmDialog';
import { Modal } from '../common/Modal';
import { TaskForm } from './TaskForm';
import { TaskAgentReadinessBadge } from './TaskAgentReadinessBadge';
import { TaskBulkOperationsPanel } from './TaskBulkOperationsPanel';
import type { Task } from '../../types/task';
import type { Label } from '../../types/label';
import type { TaskFilters } from './TaskFiltersBar';
import clsx from 'clsx';
import { filterTaskWithChildren } from '../../utils/taskFilters';
import {
    DndContext,
    closestCenter,
    KeyboardSensor,
    PointerSensor,
    useSensor,
    useSensors,
} from '@dnd-kit/core';
import type { DragEndEvent } from '@dnd-kit/core';
import {
    arrayMove,
    SortableContext,
    sortableKeyboardCoordinates,
    useSortable,
    verticalListSortingStrategy,
} from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
import { getApiErrorMessage } from '../../utils/apiError';
import { QueryErrorState } from '../feedback/QueryState';
import { useToast } from '../feedback/toast';
import { OverflowMenu } from '../ui';

export type SortKey = 'priority' | 'sort_order' | 'status' | 'title';
type TaskOrderRequest = Parameters<typeof taskService.reorder>[0];
type ReorderVariables = {
    order: TaskOrderRequest;
    undoOrder: TaskOrderRequest;
};

// Calculate effective effort for composite tasks (sum of children)
const getEffectiveEffort = (task: Task): number => {
    if (task.children && task.children.length > 0) {
        return task.children.reduce((sum, child) => sum + getEffectiveEffort(child), 0);
    }
    return task.effort_days || 0;
};

// Get dependency task names from taskMap
const getDependencyNames = (depIds: number[], taskMap: Map<number, Task>): string[] => {
    return depIds.map(id => taskMap.get(id)?.title || `#${id}`).slice(0, 3);
};

interface TaskListProps {
    iterationId: number;
    filters?: TaskFilters;
    sortKey: SortKey;
    onSortKeyChange: (sortKey: SortKey) => void;
    hasActiveFilters?: boolean;
    activeViewName?: string;
    onClearFilters?: () => void;
    onCreateTask?: () => void;
}

export const TaskList = ({
    iterationId,
    filters,
    sortKey,
    onSortKeyChange,
    hasActiveFilters = false,
    activeViewName,
    onClearFilters,
    onCreateTask,
}: TaskListProps) => {
    const queryClient = useQueryClient();
    const { t } = useTranslation();
    const toast = useToast();
    const [editingTask, setEditingTask] = useState<Task | null>(null);
    const [addingChildTo, setAddingChildTo] = useState<number | null>(null);
    const [deletingTask, setDeletingTask] = useState<Task | null>(null);

    // Merge mode state
    const [isMergeMode, setIsMergeMode] = useState(false);
    const [selectedTaskIds, setSelectedTaskIds] = useState<Set<number>>(new Set());
    const [showMergeModal, setShowMergeModal] = useState(false);
    const [mergeParentTitle, setMergeParentTitle] = useState('');
    const mergeTitleRef = useRef<HTMLInputElement>(null);
    const [isBulkMode, setIsBulkMode] = useState(false);
    const [selectedBulkTaskIds, setSelectedBulkTaskIds] = useState<Set<number>>(new Set());
    const [nowMs, setNowMs] = useState(() => Date.now());

    useEffect(() => {
        const timer = window.setInterval(() => setNowMs(Date.now()), 60_000);
        return () => window.clearInterval(timer);
    }, []);

    const { data: tasks, isLoading, error: tasksError, refetch: refetchTasks } = useQuery({
        queryKey: ['tasks', iterationId],
        queryFn: () => taskService.getByIteration(iterationId),
    });

    const { data: labelGroups = [], error: labelsError, refetch: refetchLabels } = useQuery({
        queryKey: ['label-groups'],
        queryFn: () => labelService.getGroups(),
    });

    const { data: allLabelGroups = [], error: allLabelsError, refetch: refetchAllLabels } = useQuery({
        queryKey: ['label-groups', { includeInactive: true }],
        queryFn: () => labelService.getGroups({ include_inactive: true }),
    });

    const deleteMutation = useMutation({
        mutationFn: taskService.delete,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['tasks', iterationId] });
            queryClient.invalidateQueries({ queryKey: ['workload'] });
            queryClient.invalidateQueries({ queryKey: ['gantt'] });
            toast.success(t('taskList.deleteSuccess', {
                title: deletingTask?.title ?? t('tasks.title'),
            }));
            setDeletingTask(null);
        },
    });

    const reorderMutation = useMutation({
        mutationFn: ({ order }: ReorderVariables) => taskService.reorder(order),
        onSuccess: (_response, variables) => {
            queryClient.invalidateQueries({ queryKey: ['tasks', iterationId] });
            toast.success(t('taskList.reorderSaved'), {
                dedupeKey: `task-order-${Date.now()}`,
                durationMs: 10_000,
                actionLabel: t('taskList.undo'),
                onAction: async () => {
                    try {
                        await taskService.reorder(variables.undoOrder);
                        await queryClient.invalidateQueries({ queryKey: ['tasks', iterationId] });
                        toast.success(t('taskList.reorderRestored'));
                    } catch (error) {
                        toast.error(getApiErrorMessage(error, t('taskList.reorderUndoFailed')));
                        throw error;
                    }
                },
            });
        },
    });

    const mergeMutation = useMutation({
        mutationFn: (data: { task_ids: number[]; parent_title: string }) =>
            taskService.mergeTasks(iterationId, data),
        onSuccess: (parent, variables) => {
            queryClient.invalidateQueries({ queryKey: ['tasks', iterationId] });
            queryClient.invalidateQueries({ queryKey: ['gantt'] });
            toast.success(t('taskList.mergeSuccess', { count: variables.task_ids.length }), {
                dedupeKey: `task-merge-${parent.id}`,
                durationMs: 10_000,
                actionLabel: t('taskList.undo'),
                onAction: async () => {
                    try {
                        await taskService.unmergeTask(parent.id, true);
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
            // Reset merge mode
            setIsMergeMode(false);
            setSelectedTaskIds(new Set());
            setShowMergeModal(false);
            setMergeParentTitle('');
        },
    });

    const unmergeMutation = useMutation({
        mutationFn: (taskId: number) => taskService.unmergeTask(taskId, true),
        onSuccess: async () => {
            // Explicitly refetch - this is more reliable than invalidateQueries
            await queryClient.refetchQueries({ queryKey: ['tasks', iterationId] });
            await queryClient.refetchQueries({ queryKey: ['gantt'] });
            await queryClient.refetchQueries({ queryKey: ['workload'] });
            toast.success(t('taskList.unmergeSuccess'));
        },
    });


    // Toggle task selection for merge
    const toggleTaskSelection = (taskId: number) => {
        setSelectedTaskIds(prev => {
            const next = new Set(prev);
            if (next.has(taskId)) {
                next.delete(taskId);
            } else {
                next.add(taskId);
            }
            return next;
        });
    };

    // Check if a task can be selected for merge (must be leaf task - no children)
    const canSelectForMerge = (task: Task): boolean => {
        return !task.children || task.children.length === 0;
    };

    const toggleBulkTaskSelection = (taskId: number) => {
        setSelectedBulkTaskIds(prev => {
            const next = new Set(prev);
            if (next.has(taskId)) {
                next.delete(taskId);
            } else {
                next.add(taskId);
            }
            return next;
        });
    };

    // Handle merge confirmation
    const handleMergeConfirm = () => {
        if (selectedTaskIds.size >= 2 && mergeParentTitle.trim()) {
            mergeMutation.mutate({
                task_ids: Array.from(selectedTaskIds),
                parent_title: mergeParentTitle.trim()
            });
        }
    };

    // Filter and sort tasks based on filters and selected key
    const filteredAndSortedTasks = useMemo(() => {
        if (!tasks) return [];

        // Apply filters
        const filtered = tasks
            .map(task => filterTaskWithChildren(task, filters, labelGroups))
            .filter((t): t is Task => t !== null);

        // Sort
        const sorted = [...filtered];
        sorted.sort((a, b) => {
            if (sortKey === 'priority') return a.priority - b.priority;
            if (sortKey === 'sort_order') return a.sort_order - b.sort_order;
            if (sortKey === 'status') {
                const order: Record<string, number> = { 'planned': 0, 'active': 1, 'resolved': 2, 'closed': 3 };
                return (order[a.status] ?? 0) - (order[b.status] ?? 0);
            }
            if (sortKey === 'title') return a.title.localeCompare(b.title);
            return 0;
        });
        return sorted;
    }, [tasks, sortKey, filters, labelGroups]);

    const visibleTasks = useMemo(() => {
        const flatten = (taskList: Task[]): Task[] => {
            const flattened: Task[] = [];
            taskList.forEach(task => {
                flattened.push(task);
                if (task.children?.length) {
                    flattened.push(...flatten(task.children));
                }
            });
            return flattened;
        };
        return flatten(filteredAndSortedTasks);
    }, [filteredAndSortedTasks]);
    const selectedBulkTasks = useMemo(
        () => visibleTasks.filter(task => selectedBulkTaskIds.has(task.id)),
        [visibleTasks, selectedBulkTaskIds]
    );

    const labelsBySlug = useMemo(() => {
        const map = new Map<string, Label>();
        allLabelGroups.forEach(group => {
            group.labels.forEach(label => {
                map.set(label.slug, label);
            });
        });
        return map;
    }, [allLabelGroups]);

    // Helper to find a task by ID in the tree
    const findTaskById = (taskId: number, taskList: Task[] = tasks || []): Task | undefined => {
        for (const task of taskList) {
            if (task.id === taskId) return task;
            if (task.children) {
                const found = findTaskById(taskId, task.children);
                if (found) return found;
            }
        }
        return undefined;
    };

    // Build flat map of taskId -> task for dependency name lookups
    const taskMap = useMemo(() => {
        const map = new Map<number, Task>();
        const addToMap = (taskList: Task[]) => {
            taskList.forEach(t => {
                map.set(t.id, t);
                if (t.children) addToMap(t.children);
            });
        };
        if (tasks) addToMap(tasks);
        return map;
    }, [tasks]);

    // Get parent task's priority for new subtask form
    const parentTaskForForm = addingChildTo ? findTaskById(addingChildTo) : undefined;

    const sensors = useSensors(
        useSensor(PointerSensor),
        useSensor(KeyboardSensor, {
            coordinateGetter: sortableKeyboardCoordinates,
        })
    );

    // Handle drag end for root-level tasks
    const handleDragEnd = (event: DragEndEvent) => {
        const { active, over } = event;
        if (!over || active.id === over.id) return;

        const oldIndex = filteredAndSortedTasks.findIndex(t => t.id === active.id);
        const newIndex = filteredAndSortedTasks.findIndex(t => t.id === over.id);

        if (oldIndex !== -1 && newIndex !== -1) {
            const reordered = arrayMove(filteredAndSortedTasks, oldIndex, newIndex);
            const newOrderIds = reordered.map(t => t.id);
            reorderMutation.mutate({
                order: { taskIds: newOrderIds, iterationId, parentId: null },
                undoOrder: {
                    taskIds: filteredAndSortedTasks.map(task => task.id),
                    iterationId,
                    parentId: null,
                },
            });
        }
    };

    // Handle drag end for child tasks within a parent
    const handleChildDragEnd = (parentTask: Task, event: DragEndEvent) => {
        const { active, over } = event;
        if (!over || active.id === over.id || !parentTask.children) return;

        const oldIndex = parentTask.children.findIndex(t => t.id === active.id);
        const newIndex = parentTask.children.findIndex(t => t.id === over.id);

        if (oldIndex !== -1 && newIndex !== -1) {
            const reordered = arrayMove(parentTask.children, oldIndex, newIndex);
            const newOrderIds = reordered.map(t => t.id);
            reorderMutation.mutate({
                order: { taskIds: newOrderIds, iterationId, parentId: parentTask.id },
                undoOrder: {
                    taskIds: parentTask.children.map(task => task.id),
                    iterationId,
                    parentId: parentTask.id,
                },
            });
        }
    };

    const isDraggingEnabled = sortKey === 'sort_order' && !reorderMutation.isPending;

    if (isLoading) return <div>{t('taskList.loading')}</div>;
    if (tasksError || labelsError || allLabelsError) return <QueryErrorState error={tasksError ?? labelsError ?? allLabelsError} onRetry={() => { void refetchTasks(); void refetchLabels(); void refetchAllLabels(); }} />;

    return (
        <div className="space-y-4">
            {reorderMutation.isError && (
                <QueryErrorState
                    error={reorderMutation.error}
                    fallback={t('taskList.reorderFailed')}
                    onRetry={() => {
                        if (reorderMutation.variables) reorderMutation.mutate(reorderMutation.variables);
                    }}
                />
            )}
            {(deleteMutation.isPending
                || reorderMutation.isPending
                || mergeMutation.isPending
                || unmergeMutation.isPending) && (
                <p className="sr-only" role="status" aria-live="polite">
                    {deleteMutation.isPending
                        ? t('taskList.deletingTask')
                        : reorderMutation.isPending
                            ? t('taskList.savingOrder')
                            : mergeMutation.isPending
                                ? t('taskList.mergingTasks')
                                : t('taskList.splittingTask')}
                </p>
            )}
            {unmergeMutation.isError && (
                <QueryErrorState
                    error={unmergeMutation.error}
                    fallback={t('taskList.unmergeFailed')}
                    onRetry={() => {
                        if (unmergeMutation.variables) unmergeMutation.mutate(unmergeMutation.variables);
                    }}
                />
            )}
            {isMergeMode || isBulkMode ? (
                <div
                    className="mb-2 flex flex-wrap items-center gap-2 rounded-lg border border-action bg-action-muted px-3 py-2"
                    role="region"
                    aria-label={isMergeMode ? t('taskList.mergeTasks') : t('taskList.bulkEdit')}
                >
                    <div className="min-w-0 flex-1">
                        <div className="text-sm font-semibold text-content-primary">
                            {isMergeMode ? t('taskList.mergeTasks') : t('taskList.bulkEdit')}
                        </div>
                        <div className="text-xs text-content-secondary" aria-live="polite">
                            {isMergeMode
                                ? t('taskList.mergeHint')
                                : t('taskList.selectedTasks', { count: selectedBulkTaskIds.size })}
                        </div>
                    </div>
                    {isMergeMode && selectedTaskIds.size >= 2 && (
                        <Button
                            variant="primary"
                            size="sm"
                            onClick={() => {
                                mergeMutation.reset();
                                setShowMergeModal(true);
                            }}
                        >
                            {t('taskList.mergeSelected', { count: selectedTaskIds.size })}
                        </Button>
                    )}
                    {isBulkMode && (
                        <>
                            <Button
                                variant="secondary"
                                size="sm"
                                onClick={() => setSelectedBulkTaskIds(new Set(visibleTasks.map(task => task.id)))}
                                disabled={visibleTasks.length === 0}
                            >
                                {t('taskList.selectVisible')}
                            </Button>
                            {selectedBulkTaskIds.size > 0 && (
                                <Button
                                    variant="ghost"
                                    size="sm"
                                    onClick={() => setSelectedBulkTaskIds(new Set())}
                                >
                                    {t('actions.clear')}
                                </Button>
                            )}
                        </>
                    )}
                    <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => {
                            setIsMergeMode(false);
                            setIsBulkMode(false);
                            setSelectedTaskIds(new Set());
                            setSelectedBulkTaskIds(new Set());
                        }}
                    >
                        {isMergeMode ? t('taskList.cancelMerge') : t('taskList.cancelBulkEdit')}
                    </Button>
                </div>
            ) : (
                <div className="mb-2 flex flex-wrap items-center justify-end gap-2">
                <div className="flex items-center gap-2">
                    <ArrowUpDown className="w-4 h-4 text-content-secondary" />
                    <select
                        value={sortKey}
                        onChange={e => onSortKeyChange(e.target.value as SortKey)}
                        aria-label={t('taskList.sortTasks')}
                        className="text-sm border border-border-strong rounded-md px-2 py-1 bg-surface-card"
                    >
                        <option value="priority">{t('taskList.sortPriority')}</option>
                        <option value="sort_order">{t('taskList.sortManual')}</option>
                        <option value="status">{t('taskList.sortStatus')}</option>
                        <option value="title">{t('taskList.sortTitle')}</option>
                    </select>
                </div>
                    <OverflowMenu
                        label={t('taskList.organizeTasks')}
                        items={[
                            {
                                label: t('taskList.mergeTasks'),
                                icon: <Layers className="h-4 w-4" aria-hidden="true" />,
                                onSelect: () => {
                                    setIsMergeMode(true);
                                    setIsBulkMode(false);
                                    setSelectedBulkTaskIds(new Set());
                                },
                            },
                            {
                                label: t('taskList.bulkEdit'),
                                icon: <ClipboardCheck className="h-4 w-4" aria-hidden="true" />,
                                onSelect: () => {
                                    setIsBulkMode(true);
                                    setIsMergeMode(false);
                                    setSelectedTaskIds(new Set());
                                },
                            },
                        ]}
                    />
                </div>
            )}

            {isBulkMode && selectedBulkTaskIds.size > 0 && (
                <TaskBulkOperationsPanel
                    iterationId={iterationId}
                    selectedTasks={selectedBulkTasks}
                    selectedTaskIds={Array.from(selectedBulkTaskIds)}
                    onClearSelection={() => setSelectedBulkTaskIds(new Set())}
                    onApplied={() => undefined}
                />
            )}

            {isDraggingEnabled ? (
                <DndContext
                    sensors={sensors}
                    collisionDetection={closestCenter}
                    onDragEnd={handleDragEnd}
                >
                    <SortableContext
                        items={filteredAndSortedTasks.map(t => t.id)}
                        strategy={verticalListSortingStrategy}
                    >
                        {filteredAndSortedTasks.map((task) => (
                            <SortableTaskItem
                                key={task.id}
                                task={task}
                                onEdit={setEditingTask}
                                onAddSubtask={setAddingChildTo}
                                onDelete={(t) => setDeletingTask(t)}
                                onUnmerge={(id) => unmergeMutation.mutate(id)}
                                isUnmergePending={unmergeMutation.isPending}
                                level={0}
                                sensors={sensors}
                                onChildDragEnd={handleChildDragEnd}
                                isDraggingEnabled={isDraggingEnabled}
                                taskMap={taskMap}
                                isMergeMode={isMergeMode}
                                selectedTaskIds={selectedTaskIds}
                                canSelectForMerge={canSelectForMerge}
                                toggleTaskSelection={toggleTaskSelection}
                                isBulkMode={isBulkMode}
                                selectedBulkTaskIds={selectedBulkTaskIds}
                                toggleBulkTaskSelection={toggleBulkTaskSelection}
                                labelsBySlug={labelsBySlug}
                                nowMs={nowMs}
                            />
                        ))}
                    </SortableContext>
                </DndContext>
            ) : (
                filteredAndSortedTasks.map((task) => (
                    <TaskItemContent
                        key={task.id}
                        task={task}
                        onEdit={setEditingTask}
                        onAddSubtask={setAddingChildTo}
                        onDelete={(t) => setDeletingTask(t)}
                        onUnmerge={(id) => unmergeMutation.mutate(id)}
                        isUnmergePending={unmergeMutation.isPending}
                        level={0}
                        sensors={sensors}
                        onChildDragEnd={handleChildDragEnd}
                        isDraggingEnabled={false}
                        taskMap={taskMap}
                        isMergeMode={isMergeMode}
                        selectedTaskIds={selectedTaskIds}
                        canSelectForMerge={canSelectForMerge}
                        toggleTaskSelection={toggleTaskSelection}
                        isBulkMode={isBulkMode}
                        selectedBulkTaskIds={selectedBulkTaskIds}
                        toggleBulkTaskSelection={toggleBulkTaskSelection}
                        labelsBySlug={labelsBySlug}
                        nowMs={nowMs}
                    />
                ))
            )}

            {filteredAndSortedTasks?.length === 0 && (
                <div className="rounded-lg border border-dashed border-border bg-surface-muted px-6 py-12 text-center">
                    <h3 className="text-base font-semibold text-content-primary">
                        {tasks && tasks.length > 0
                            ? t('taskList.noFilterMatches')
                            : t('taskList.noTasks')}
                    </h3>
                    <p className="mx-auto mt-1 max-w-lg text-sm text-content-secondary">
                        {tasks && tasks.length > 0
                            ? activeViewName
                                ? t('taskList.noFilterMatchesViewBody', { view: activeViewName })
                                : t('taskList.noFilterMatchesBody')
                            : t('taskList.noTasksBody')}
                    </p>
                    <div className="mt-4 flex justify-center gap-2">
                        {tasks && tasks.length > 0 && hasActiveFilters && onClearFilters ? (
                            <Button variant="secondary" onClick={onClearFilters}>
                                {t('taskList.clearFilters')}
                            </Button>
                        ) : onCreateTask ? (
                            <Button variant="primary" onClick={onCreateTask}>
                                <Plus className="mr-1 h-4 w-4" aria-hidden="true" />
                                {t('tasks.newTask')}
                            </Button>
                        ) : null}
                    </div>
                </div>
            )}

            <Modal
                open={Boolean(editingTask || addingChildTo)}
                title={editingTask ? t('tasks.editTask') : t('tasks.addSubtask')}
                closeLabel={t('actions.close')}
                onClose={() => { setEditingTask(null); setAddingChildTo(null); }}
            >
                {(editingTask || addingChildTo) && (
                        <TaskForm
                            iterationId={iterationId}
                            initialData={editingTask || undefined}
                            parentId={addingChildTo}
                            parentPriority={parentTaskForForm?.priority}
                            parentProjectId={parentTaskForForm?.project_id ?? null}
                            parentMilestoneId={parentTaskForForm?.milestone_id ?? null}
                            onSuccess={() => { setEditingTask(null); setAddingChildTo(null); }}
                            onCancel={() => { setEditingTask(null); setAddingChildTo(null); }}
                        />
                )}
            </Modal>

            <ConfirmDialog
                open={deletingTask !== null}
                title={t('taskList.deleteTaskTitle')}
                description={<>
                    {deletingTask && (
                        <span>
                            {t('taskList.deleteTaskBody', { title: deletingTask.title })}
                            {deletingTask.children && deletingTask.children.length > 0 && (
                                <span className="block mt-2 text-feedback-danger">
                                    {t('taskList.deleteSubtasksWarning', { count: deletingTask.children.length })}
                                </span>
                            )}
                        </span>
                    )}
                    {deleteMutation.isError && <span role="alert" className="mt-2 block text-feedback-danger-foreground">{getApiErrorMessage(deleteMutation.error, t('queryFeedback.fallback'))}</span>}
                </>}
                confirmLabel={t('actions.delete')}
                cancelLabel={t('actions.cancel')}
                closeLabel={t('actions.close')}
                pending={deleteMutation.isPending}
                onCancel={() => setDeletingTask(null)}
                onConfirm={() => { if (deletingTask) deleteMutation.mutate(deletingTask.id); }}
            />

            {/* Merge Modal */}
            <Modal
                open={showMergeModal}
                title={<span className="flex items-center gap-2 text-feedback-indigo"><Layers className="h-5 w-5" />{t('taskList.mergeModalTitle')}</span>}
                closeLabel={t('actions.close')}
                onClose={() => { if (!mergeMutation.isPending) { setShowMergeModal(false); setMergeParentTitle(''); } }}
                closeDisabled={mergeMutation.isPending}
                initialFocusRef={mergeTitleRef}
                className="max-w-md"
            >
                {showMergeModal && (
                    <>
                        <p className="mb-4 text-content-secondary">
                            {t('taskList.selectedTasks', { count: selectedTaskIds.size })}
                        </p>
                        <div className="mb-4">
                            <label className="block text-sm font-medium text-content-primary mb-1">
                                {t('taskList.parentTitleLabel')}
                            </label>
                            <input
                                ref={mergeTitleRef}
                                type="text"
                                value={mergeParentTitle}
                                onChange={(e) => setMergeParentTitle(e.target.value)}
                                placeholder={t('taskList.parentTitlePlaceholder')}
                                className="w-full px-3 py-2 border border-border-strong rounded-md focus:outline-none focus:ring-2 focus:ring-focus"
                            />
                        </div>
                        {mergeMutation.isError && (
                            <QueryErrorState
                                className="mb-4"
                                error={mergeMutation.error}
                                fallback={t('taskList.mergeFailed')}
                                onRetry={() => {
                                    if (mergeMutation.variables) mergeMutation.mutate(mergeMutation.variables);
                                }}
                            />
                        )}
                        <div className="flex justify-end gap-3">
                            <Button
                                variant="secondary"
                                onClick={() => {
                                    setShowMergeModal(false);
                                    setMergeParentTitle('');
                                }}
                                disabled={mergeMutation.isPending}
                            >
                                {t('actions.cancel')}
                            </Button>
                            <Button
                                variant="primary"
                                onClick={handleMergeConfirm}
                                disabled={!mergeParentTitle.trim() || mergeMutation.isPending}
                                isLoading={mergeMutation.isPending}
                            >
                                {t('taskList.mergeTasks')}
                            </Button>
                        </div>
                    </>
                )}
            </Modal>
        </div>
    );
};

interface TaskItemProps {
    task: Task;
    onEdit: (t: Task) => void;
    onAddSubtask: (id: number) => void;
    onDelete: (task: Task) => void;
    onUnmerge: (taskId: number) => void;
    isUnmergePending: boolean;
    level: number;
    sensors: ReturnType<typeof useSensors>;
    onChildDragEnd: (parent: Task, event: DragEndEvent) => void;
    isDraggingEnabled: boolean;
    taskMap: Map<number, Task>;
    // Merge mode props
    isMergeMode: boolean;
    selectedTaskIds: Set<number>;
    canSelectForMerge: (task: Task) => boolean;
    toggleTaskSelection: (taskId: number) => void;
    isBulkMode: boolean;
    selectedBulkTaskIds: Set<number>;
    toggleBulkTaskSelection: (taskId: number) => void;
    labelsBySlug: Map<string, Label>;
    nowMs: number;
}

// Sortable wrapper for root-level tasks
const SortableTaskItem = (props: TaskItemProps) => {
    const {
        attributes,
        listeners,
        setNodeRef,
        transform,
        transition,
        isDragging
    } = useSortable({ id: props.task.id });

    const style = {
        transform: CSS.Transform.toString(transform),
        transition,
        zIndex: isDragging ? 50 : 'auto',
        opacity: isDragging ? 0.8 : 1,
    };

    return (
        <div ref={setNodeRef} style={style}>
            <TaskItemContent
                {...props}
                dragHandleProps={{ ...attributes, ...listeners }}
            />
        </div>
    );
};

interface TaskItemContentProps extends TaskItemProps {
    dragHandleProps?: Record<string, unknown>;
}

const TaskItemContent = ({
    task,
    onEdit,
    onAddSubtask,
    onDelete,
    onUnmerge,
    isUnmergePending,
    level,
    sensors,
    onChildDragEnd,
    isDraggingEnabled,
    dragHandleProps,
    taskMap,
    isMergeMode,
    selectedTaskIds,
    canSelectForMerge,
    toggleTaskSelection,
    isBulkMode,
    selectedBulkTaskIds,
    toggleBulkTaskSelection,
    labelsBySlug,
    nowMs,
}: TaskItemContentProps) => {
    const [isExpanded, setIsExpanded] = useState(true);
    const { t } = useTranslation();
    const hasChildren = task.children && task.children.length > 0;
    const isSelectable = isBulkMode ? true : canSelectForMerge(task);
    const isSelected = isBulkMode ? selectedBulkTaskIds.has(task.id) : selectedTaskIds.has(task.id);

    const getPriorityBadge = (priority: number) => {
        if (priority <= 3) return { bg: 'bg-feedback-danger-muted', text: 'text-feedback-danger-foreground', label: `P${priority}` };
        if (priority <= 6) return { bg: 'bg-feedback-warning-muted', text: 'text-feedback-warning-foreground', label: `P${priority}` };
        return { bg: 'bg-surface-subtle', text: 'text-content-secondary', label: `P${priority}` };
    };

    const priorityBadge = getPriorityBadge(task.priority);
    const detailsCount = Number(task.is_optional)
        + Number(task.is_deferred)
        + Number(Boolean(task.claimed_by))
        + Number(task.dependencies.length > 0)
        + task.tags.length
        + 1;
    const statusClassName = task.status === 'planned'
        ? 'text-status-planned'
        : task.status === 'active'
            ? 'text-status-active'
            : 'text-status-resolved';

    return (
        <div className="group">
            <div
                className={clsx(
                    "flex items-center gap-3 p-3 bg-surface-card border rounded-lg hover:shadow-sm transition-all relative",
                    task.is_overdue ? "border-feedback-danger-border" : "border-border",
                    task.is_deferred && "opacity-75 bg-surface-muted",
                    isMergeMode && isSelected && "border-feedback-indigo-border bg-feedback-indigo-muted",
                    isBulkMode && isSelected && "border-action bg-action-muted"
                )}
                style={{ marginLeft: level * 24 }}
            >
                {level > 0 && (
                    <CornerDownRight className="absolute -left-5 top-1/2 -translate-y-1/2 w-4 h-4 text-content-tertiary" />
                )}

                {/* Selection checkbox */}
                {(isMergeMode || isBulkMode) && (
                    <input
                        type="checkbox"
                        checked={isSelected}
                        disabled={!isSelectable}
                        onChange={() => {
                            if (!isSelectable) return;
                            if (isBulkMode) {
                                toggleBulkTaskSelection(task.id);
                            } else {
                                toggleTaskSelection(task.id);
                            }
                        }}
                        className={clsx(
                            "w-5 h-5 rounded border-2 cursor-pointer",
                            isSelectable
                                ? "border-feedback-indigo-border text-feedback-indigo focus:ring-focus"
                                : "border-border-strong cursor-not-allowed opacity-50"
                        )}
                        title={isBulkMode ? t('taskList.selectForBulkEdit') : (isSelectable ? t('taskList.selectForMerge') : t('taskList.taskHasSubtasks'))}
                    />
                )}

                {/* Drag Handle - only visible when sorting manually */}
                {isDraggingEnabled && dragHandleProps && (
                    <button
                        type="button"
                        aria-label={t('literalWords.drag')}
                        className="p-1 text-content-tertiary cursor-grab active:cursor-grabbing hover:text-content-secondary touch-none"
                        {...dragHandleProps}
                    >
                        <GripVertical className="w-4 h-4" />
                    </button>
                )}

                {hasChildren ? (
                    <button
                        type="button"
                        aria-expanded={isExpanded}
                        aria-label={isExpanded ? t('surfaces.ganttChart.collapseAll') : t('literalWords.expand')}
                        onClick={() => setIsExpanded(!isExpanded)}
                        className="rounded p-1 hover:bg-surface-subtle"
                    >
                        {isExpanded ? <ChevronDown className="h-4 w-4" /> : <ChevronRight className="h-4 w-4" />}
                    </button>
                ) : (
                    <span className="h-6 w-6 shrink-0" aria-hidden="true" />
                )}

                <div className={clsx("shrink-0", statusClassName)}>
                    {task.status === 'resolved' || task.status === 'closed'
                        ? <CheckCircle2 className="h-5 w-5" />
                        : <Circle className="h-5 w-5" />}
                    <span className="sr-only">
                        {t('taskList.taskStatus', {
                            status: t(`statuses.${task.status}`, { defaultValue: task.status }),
                        })}
                    </span>
                </div>

                <div className="min-w-0 flex-1">
                    <div className="flex items-center gap-2 flex-wrap">
                        <span className={clsx("text-xs font-medium px-1.5 py-0.5 rounded", priorityBadge.bg, priorityBadge.text)}>
                            {priorityBadge.label}
                        </span>

                        <span className={clsx("min-w-0 font-medium", task.status === 'closed' && "line-through text-content-secondary")}>
                            {task.title}
                        </span>

                        {task.is_overdue && (
                            <span className="flex items-center text-xs text-feedback-danger-foreground bg-feedback-danger-muted px-2 py-0.5 rounded-full">
                                <AlertTriangle className="w-3 h-3 mr-1" /> {t('taskList.overdue')}
                            </span>
                        )}

                        <span className="text-xs tabular-nums text-content-secondary">
                            {t('units.daysCompact', { count: getEffectiveEffort(task) })}
                        </span>
                    </div>
                    <div className="mt-1 text-xs text-content-secondary">
                        {t('taskList.assignee')}: {task.assignee?.name ?? t('common.unassigned')}
                    </div>
                    <details className="mt-2 text-xs text-content-secondary">
                        <summary className="w-fit cursor-pointer rounded text-content-secondary hover:text-content-primary focus:outline-none focus:ring-2 focus:ring-focus">
                            {t('taskList.detailsCount', { count: detailsCount })}
                        </summary>
                        <div className="mt-2 flex flex-wrap items-center gap-1.5 border-t border-border-subtle pt-2">
                            {task.is_optional && (
                                <span className="rounded-full bg-surface-subtle px-2 py-0.5 text-content-secondary">
                                    {t('taskList.optional')}
                                </span>
                            )}
                            {task.is_deferred && (
                                <span className="rounded-full bg-surface-hover px-2 py-0.5 text-content-secondary">
                                    {t('taskList.deferred')}
                                </span>
                            )}
                            {task.claimed_by && (
                                <span className={clsx(
                                    "flex items-center rounded-full px-2 py-0.5",
                                    task.claim_expires_at && new Date(task.claim_expires_at).getTime() < nowMs
                                        ? "text-feedback-warning-foreground bg-feedback-warning-muted"
                                        : "text-action bg-status-active-muted"
                                )}>
                                    <Bot className="mr-1 h-3 w-3" aria-hidden="true" />
                                    {task.claimed_by.display_name}
                                </span>
                            )}
                            <TaskAgentReadinessBadge readiness={task.agent_readiness} />
                            {task.dependencies.length > 0 && (
                                <span>
                                    {t('taskList.dependsOn')}: {getDependencyNames(task.dependencies, taskMap).join(', ')}
                                    {task.dependencies.length > 3 && ` +${task.dependencies.length - 3}`}
                                </span>
                            )}
                            {task.tags.map((tag, idx) => {
                                const label = labelsBySlug.get(tag);
                                return label ? (
                                    <span
                                        key={idx}
                                        className="rounded-full border px-2 py-0.5"
                                        style={{
                                            color: label.color,
                                            backgroundColor: `${label.color}1A`,
                                            borderColor: `${label.color}66`,
                                        }}
                                    >
                                        {tag}
                                    </span>
                                ) : (
                                    <span key={idx} className="rounded-full bg-feedback-purple-muted px-2 py-0.5 text-feedback-purple-foreground">
                                        {tag}
                                    </span>
                                );
                            })}
                        </div>
                    </details>
                </div>

                <div className="flex items-center gap-1">
                    <Button variant="ghost" size="sm" title={t('tasks.editTask')} aria-label={t('tasks.editTask')} onClick={() => onEdit(task)}>
                        <Edit className="w-4 h-4" />
                    </Button>
                    <OverflowMenu
                        label={t('taskList.taskActions', { title: task.title })}
                        items={[
                            {
                                label: t('tasks.addSubtask'),
                                icon: <Plus className="h-4 w-4" aria-hidden="true" />,
                                onSelect: () => onAddSubtask(task.id),
                            },
                            ...(hasChildren ? [{
                                label: t('taskList.unmergeTitle'),
                                icon: <Unlink className="h-4 w-4" aria-hidden="true" />,
                                onSelect: () => onUnmerge(task.id),
                                disabled: isUnmergePending,
                            }] : []),
                            {
                                label: t('actions.delete'),
                                icon: <Trash2 className="h-4 w-4" aria-hidden="true" />,
                                onSelect: () => onDelete(task),
                                tone: 'danger' as const,
                            },
                        ]}
                    />
                </div>
            </div>

            {hasChildren && isExpanded && (
                <div className="mt-2 space-y-2">
                    {isDraggingEnabled ? (
                        <DndContext
                            sensors={sensors}
                            collisionDetection={closestCenter}
                            onDragEnd={(event) => onChildDragEnd(task, event)}
                        >
                            <SortableContext
                                items={task.children.map(c => c.id)}
                                strategy={verticalListSortingStrategy}
                            >
                                {task.children.map(child => (
                                    <SortableChildTaskItem
                                        key={child.id}
                                        task={child}
                                        onEdit={onEdit}
                                        onAddSubtask={onAddSubtask}
                                        onDelete={onDelete}
                                        onUnmerge={onUnmerge}
                                        isUnmergePending={isUnmergePending}
                                        level={level + 1}
                                        sensors={sensors}
                                        onChildDragEnd={onChildDragEnd}
                                        isDraggingEnabled={isDraggingEnabled}
                                        taskMap={taskMap}
                                        isMergeMode={isMergeMode}
                                        selectedTaskIds={selectedTaskIds}
                                        canSelectForMerge={canSelectForMerge}
                                        toggleTaskSelection={toggleTaskSelection}
                                        isBulkMode={isBulkMode}
                                        selectedBulkTaskIds={selectedBulkTaskIds}
                                        toggleBulkTaskSelection={toggleBulkTaskSelection}
                                        labelsBySlug={labelsBySlug}
                                        nowMs={nowMs}
                                    />
                                ))}
                            </SortableContext>
                        </DndContext>
                    ) : (
                        task.children.map(child => (
                            <TaskItemContent
                                key={child.id}
                                task={child}
                                onEdit={onEdit}
                                onAddSubtask={onAddSubtask}
                                onDelete={onDelete}
                                onUnmerge={onUnmerge}
                                isUnmergePending={isUnmergePending}
                                level={level + 1}
                                sensors={sensors}
                                onChildDragEnd={onChildDragEnd}
                                isDraggingEnabled={false}
                                taskMap={taskMap}
                                isMergeMode={isMergeMode}
                                selectedTaskIds={selectedTaskIds}
                                canSelectForMerge={canSelectForMerge}
                                toggleTaskSelection={toggleTaskSelection}
                                isBulkMode={isBulkMode}
                                selectedBulkTaskIds={selectedBulkTaskIds}
                                toggleBulkTaskSelection={toggleBulkTaskSelection}
                                labelsBySlug={labelsBySlug}
                                nowMs={nowMs}
                            />
                        ))
                    )}
                </div>
            )}
        </div>
    );
};

// Sortable wrapper for child tasks
const SortableChildTaskItem = (props: TaskItemProps) => {
    const {
        attributes,
        listeners,
        setNodeRef,
        transform,
        transition,
        isDragging
    } = useSortable({ id: props.task.id });

    const style = {
        transform: CSS.Transform.toString(transform),
        transition,
        zIndex: isDragging ? 50 : 'auto',
        opacity: isDragging ? 0.8 : 1,
    };

    return (
        <div ref={setNodeRef} style={style}>
            <TaskItemContent
                {...props}
                dragHandleProps={{ ...attributes, ...listeners }}
            />
        </div>
    );
};

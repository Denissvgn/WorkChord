import { isGraphLimitError } from '../../utils/graphLimitError';
import { atRiskReasons } from '../../features/planningMasters/atRiskReasons';
import { PagedTaskBrowser } from './PagedTaskBrowser';
import { stateTextClassName } from '../ui/tone';
import { stateOf } from '../../utils/taskState';
import { LabelChip } from '../labels/LabelChip';
import { Fragment, useCallback, useEffect, useId, useLayoutEffect, useMemo, useState } from 'react';
import type { ReactNode } from 'react';
import { createPortal } from 'react-dom';
import { useVirtualizer } from '@tanstack/react-virtual';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import {
    ChevronRight, ChevronDown,
    Trash2, Plus, Edit, AlertTriangle, GripVertical, Unlink, Bot, Info
} from 'lucide-react';
import { taskService } from '../../services/taskService';
import { labelService } from '../../services/labelService';
import { Button } from '../common/Button';
import { InlineEmptyState } from '../ui/InlineEmptyState';
import { NextStepEmptyState } from '../../features/firstRun/NextStepEmptyState';
import { firstRunPlanHref } from '../../features/firstRun/firstRunSteps';
import { useScopeLink } from '../../features/scope/useScopeLink';
import { ConfirmDialog } from '../common/ConfirmDialog';
import { GuardedTaskDrawer } from './GuardedTaskDrawer';
import { selectVisibleWork } from '../../utils/visibleWork';
import { WorkFreshness } from '../feedback/WorkFreshness';
import { TaskAgentReadinessBadge } from './TaskAgentReadinessBadge';
import { TaskSelectionBar } from './TaskSelectionBar';
import { TaskRow } from './TaskRow';
import { useTaskSelection } from './useTaskSelection';
import { taskStateChip } from './taskStateChip';
import { getEffectiveEffort } from './taskRowValues';
import type { TaskRowAssigneeOption } from './TaskRow';
import { useAssigneeOptions, useTaskRowEdits } from './useTaskRowEdits';
import { agentRowValues, useAgentRowFacts } from './useAgentRowFacts';
import type { AgentRowFacts } from './useAgentRowFacts';
import type { Task, TaskDisplayedState, TaskStatus } from '../../types/task';
import type { Label } from '../../types/label';
import type { TaskFilters } from './TaskFiltersBar';
import clsx from 'clsx';
import { filterTaskBySearch, filterTaskWithChildren } from '../../utils/taskFilters';
import { useSearchParams } from 'react-router-dom';
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
import { QueryErrorState, QueryLoadingState } from '../feedback/QueryState';
import { useToast } from '../feedback/toast';

export type SortKey = 'priority' | 'sort_order' | 'status' | 'title';
export type TaskMode = 'bulk' | 'merge';
/** Lifecycle order for status groups: the work in hand first, finished work last. */
const STATUS_GROUP_ORDER = ['active', 'planned', 'resolved', 'closed', 'postponed', 'canceled', 'superseded'];
/** Longer lists render only the rows near the viewport. */
const VIRTUALIZE_AFTER_ROWS = 80;
/** Every row is 44 px tall, its bottom line included. */
const ROW_HEIGHT = 44;
type RowItem = { kind: 'group'; status: string; count: number; collapsed: boolean } | { kind: 'task'; task: Task };
const rowItemKey = (item: RowItem) => item.kind === 'group' ? `group:${item.status}` : `task:${item.task.id}`;
type TaskOrderRequest = Parameters<typeof taskService.reorder>[0];
type ReorderVariables = {
    order: TaskOrderRequest;
    undoOrder: TaskOrderRequest;
};

// Get dependency task names from taskMap
const getDependencyNames = (depIds: number[], taskMap: Map<number, Task>): string[] => {
    return depIds.map(id => taskMap.get(id)?.title || `#${id}`).slice(0, 3);
};

interface TaskListProps {
    iterationId: number;
    filters?: TaskFilters;
    sortKey: SortKey;
    /** Group the rows by status; manual order always shows one list. */
    groupByStatus?: boolean;
    /** A row shown above the tasks, inside the list, such as quick add. */
    leadingRow?: ReactNode;
    /** Where the bulk bar shows while tasks are selected, in place of the toolbar; it sits above the list when this is left out. */
    selectionBarHost?: HTMLElement | null;
    hasActiveFilters?: boolean;
    activeViewName?: string;
    onClearFilters?: () => void;
    onCreateTask?: () => void;
    /** A hand-off asked to start with tasks selected; clearing the selection reports `null`. */
    requestedMode?: TaskMode | null;
    onModeChange?: (mode: TaskMode | null) => void;
    /** Select every matching task once when a hand-off opens the list to assign work. */
    preselectAllInBulk?: boolean;
    /** Open a task in the page's read-first view (keeps ?task=<id> in the URL). */
    onOpenTask?: (task: Task) => void;
}

export const TaskList = ({
    iterationId,
    filters,
    sortKey,
    groupByStatus = true,
    leadingRow,
    selectionBarHost,
    hasActiveFilters = false,
    activeViewName,
    onClearFilters,
    onCreateTask,
    requestedMode,
    onModeChange,
    preselectAllInBulk = false,
    onOpenTask,
}: TaskListProps) => {
    const queryClient = useQueryClient();
    const { t } = useTranslation();
    const scopeLink = useScopeLink();
    const toast = useToast();
    const [editingTask, setEditingTask] = useState<Task | null>(null);
    const [searchParams, setSearchParams] = useSearchParams();
    const searchText = searchParams.get('q')?.slice(0, 200) ?? '';
    const [addingChildTo, setAddingChildTo] = useState<number | null>(null);
    const [deletingTask, setDeletingTask] = useState<Task | null>(null);

    // Selection is direct: any row can be ticked, with no mode to enter first.
    const [nowMs, setNowMs] = useState(() => Date.now());
    const [collapsedParents, setCollapsedParents] = useState<Set<number>>(() => new Set());
    const toggleParent = useCallback((taskId: number) => setCollapsedParents(previous => {
        const next = new Set(previous);
        if (next.has(taskId)) next.delete(taskId); else next.add(taskId);
        return next;
    }), []);

    useEffect(() => {
        const timer = window.setInterval(() => setNowMs(Date.now()), 60_000);
        return () => window.clearInterval(timer);
    }, []);

    const { data: tasks, isLoading, error: tasksError, refetch: refetchTasks, isRefetchError, isFetching } = useQuery({
        queryKey: ['tasks', iterationId],
        queryFn: () => taskService.getByIteration(iterationId),
    });

    const iterationRevision = tasks?.[0]?.iteration_revision;

    const { data: labelGroups = [], error: labelsError, refetch: refetchLabels } = useQuery({
        queryKey: ['label-groups'],
        queryFn: () => labelService.getGroups(),
    });

    const { data: allLabelGroups = [], error: allLabelsError, refetch: refetchAllLabels } = useQuery({
        queryKey: ['label-groups', { includeInactive: true }],
        queryFn: () => labelService.getGroups({ include_inactive: true }),
    });

    const deleteMutation = useMutation({
        mutationFn: (task: Task) => taskService.delete(task.id, task.version, task.iteration_revision),
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
        onSuccess: (response, variables) => {
            queryClient.invalidateQueries({ queryKey: ['tasks', iterationId] });
            toast.success(t('taskList.reorderSaved'), {
                dedupeKey: `task-order-${Date.now()}`,
                durationMs: 10_000,
                actionLabel: t('taskList.undo'),
                onAction: async () => {
                    try {
                        await taskService.reorder({ ...variables.undoOrder, expectedRevision: response.iteration_revision });
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

    const unmergeMutation = useMutation({
        mutationFn: (taskId: number) => taskService.unmergeTask(taskId, true, iterationRevision),
        onSuccess: async () => {
            // Explicitly refetch - this is more reliable than invalidateQueries
            await queryClient.refetchQueries({ queryKey: ['tasks', iterationId] });
            await queryClient.refetchQueries({ queryKey: ['gantt'] });
            await queryClient.refetchQueries({ queryKey: ['workload'] });
            toast.success(t('taskList.unmergeSuccess'));
        },
    });


    // Filter and sort tasks based on filters and selected key
    const filteredAndSortedTasks = useMemo(() => {
        if (!tasks) return [];

        // Apply filters
        // Search narrows this list in place, by title or #ID.
        const filtered = tasks
            .map(task => filterTaskWithChildren(task, filters, labelGroups))
            .filter((t): t is Task => t !== null)
            .map(task => filterTaskBySearch(task, searchText))
            .filter((t): t is Task => t !== null);

        // Sort
        const sorted = [...filtered];
        sorted.sort((a, b) => {
            if (sortKey === 'priority') return a.priority - b.priority;
            if (sortKey === 'sort_order') return a.sort_order - b.sort_order;
            if (sortKey === 'status') {
                const order: Record<string, number> = { 'planned': 0, 'active': 1, 'resolved': 2, 'closed': 3, 'postponed': 4, 'canceled': 5, 'superseded': 6 };
                return (order[stateOf(a)] ?? 0) - (order[stateOf(b)] ?? 0);
            }
            if (sortKey === 'title') return a.title.localeCompare(b.title);
            return 0;
        });
        return sorted;
    }, [tasks, sortKey, filters, labelGroups, searchText]);

    const visibleTasks = useMemo(() => selectVisibleWork(filteredAndSortedTasks).leaves, [filteredAndSortedTasks]);
    const selectableIds = useMemo(() => new Set(visibleTasks.map(task => task.id)), [visibleTasks]);

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
                order: { taskIds: newOrderIds, iterationId, parentId: null, expectedRevision: iterationRevision },
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
                order: { taskIds: newOrderIds, iterationId, parentId: parentTask.id, expectedRevision: iterationRevision },
                undoOrder: {
                    taskIds: parentTask.children.map(task => task.id),
                    iterationId,
                    parentId: parentTask.id,
                },
            });
        }
    };

    const isDraggingEnabled = sortKey === 'sort_order' && !reorderMutation.isPending;

    // Group by status unless the list is in manual order, where one sequence is dragged.
    const grouped = groupByStatus && sortKey !== 'sort_order';
    const [collapsedGroups, setCollapsedGroups] = useState<Set<string>>(() => new Set(['closed']));
    const toggleGroup = (status: string) => setCollapsedGroups(previous => {
        const next = new Set(previous);
        if (next.has(status)) next.delete(status); else next.add(status);
        return next;
    });
    const rowItems = useMemo<RowItem[]>(() => {
        if (!grouped) return filteredAndSortedTasks.map(task => ({ kind: 'task' as const, task }));
        const groupStatus = (status: string) => status === 'in_progress' ? 'active' : status;
        const order = [...STATUS_GROUP_ORDER, ...new Set(filteredAndSortedTasks.map(task => groupStatus(stateOf(task))).filter(status => !STATUS_GROUP_ORDER.includes(status)))];
        return order.flatMap(status => {
            const inGroup = filteredAndSortedTasks.filter(task => groupStatus(stateOf(task)) === status);
            if (inGroup.length === 0) return [];
            const collapsed = collapsedGroups.has(status);
            return [{ kind: 'group' as const, status, count: inGroup.length, collapsed },
                ...(collapsed ? [] : inGroup.map(task => ({ kind: 'task' as const, task })))];
        });
    }, [grouped, filteredAndSortedTasks, collapsedGroups]);
    // The workspace scrolls inside #workspace-main; without it (as in tests) every row renders.
    const [rowsNode, setRowsNode] = useState<HTMLDivElement | null>(null);
    const scrollElement = rowsNode?.closest<HTMLElement>('#workspace-main') ?? null;
    const virtualizeRows = !isDraggingEnabled && scrollElement !== null && rowItems.length > VIRTUALIZE_AFTER_ROWS;
    const { options: assigneeOptions, error: assigneeOptionsError, refetch: refetchAssigneeOptions } = useAssigneeOptions(iterationId);
    // Every row the list shows, parents and the children of expanded parents, for the Reviewer reads.
    const displayedTasks = useMemo(() => {
        const shown: Task[] = [];
        const walk = (task: Task) => {
            shown.push(task);
            if (!collapsedParents.has(task.id)) task.children?.forEach(walk);
        };
        rowItems.forEach(item => { if (item.kind === 'task') walk(item.task); });
        return shown;
    }, [rowItems, collapsedParents]);
    const agentFacts = useAgentRowFacts(displayedTasks);
    const rowEdits = useTaskRowEdits();
    // The order a person sees, used to select a range between two ticked rows.
    const selectionOrder = useMemo(() => {
        const ids: number[] = [];
        const walk = (task: Task) => {
            if (!task.children || task.children.length === 0) { if (selectableIds.has(task.id)) ids.push(task.id); return; }
            if (!collapsedParents.has(task.id)) task.children.forEach(walk);
        };
        rowItems.forEach(item => { if (item.kind === 'task') walk(item.task); });
        return ids;
    }, [rowItems, collapsedParents, selectableIds]);
    const selection = useTaskSelection({ selectableIds, order: selectionOrder });
    const clearSelection = () => { selection.clear(); if (requestedMode) onModeChange?.(null); };
    // Only tasks still in the list count, so a filter change never leaves a hidden task selected.
    const selectedTasks = useMemo(() => visibleTasks.filter(task => selection.selectedIds.has(task.id)), [visibleTasks, selection.selectedIds]);
    // A hand-off to assign work starts with every matching task selected, once.
    // Adjusting state during render (not in an effect) avoids a cascading render.
    const [preselectApplied, setPreselectApplied] = useState(false);
    if (requestedMode !== 'bulk' && preselectApplied) {
        setPreselectApplied(false);
    } else if (requestedMode === 'bulk' && preselectAllInBulk && !preselectApplied && visibleTasks.length > 0) {
        setPreselectApplied(true);
        selection.replace(visibleTasks.map(task => task.id));
    }
    const rowContext: RowContext = {
        onOpen: onOpenTask ?? setEditingTask,
        onOpenSuccessor: (id: number) => { const next = new URLSearchParams(searchParams); next.set('task', String(id)); setSearchParams(next); },
        onAddSubtask: setAddingChildTo,
        onDelete: setDeletingTask,
        onUnmerge: id => unmergeMutation.mutate(id),
        isUnmergePending: unmergeMutation.isPending,
        sensors,
        onChildDragEnd: handleChildDragEnd,
        isDraggingEnabled,
        taskMap,
        labelsBySlug,
        nowMs,
        selectedIds: selection.selectedIds,
        selectableIds,
        onToggleSelect: selection.toggle,
        collapsedParents,
        onToggleParent: toggleParent,
        assigneeOptions,
        agentFacts,
        onAssign: (task: Task, assigneeId: number | null) => rowEdits.assign(task, assigneeId),
        onStatusChange: (task: Task, status: TaskStatus) => rowEdits.changeStatus(task, status),
        showRiskReasons: filters?.planningIssue === 'at-risk',
    };
    const renderRowItem = (item: RowItem) => item.kind === 'group' ? (
        <h2 className="m-0">
            <Button data-page-chrome-control="button" type="button" aria-expanded={!item.collapsed} onClick={() => toggleGroup(item.status)}
                className="flex min-h-7 w-full items-center gap-2 border-b border-border-subtle bg-surface-muted px-3 text-left text-sm font-semibold text-content-primary hover:bg-surface-hover focus:outline-hidden focus-visible:ring-2 focus-visible:ring-focus" variant="plain">
                {item.collapsed ? <ChevronRight aria-hidden="true" className="h-4 w-4" /> : <ChevronDown aria-hidden="true" className="h-4 w-4" />}
                <span className={stateTextClassName[item.status as TaskDisplayedState]}>
                    {t(`statuses.${item.status}`, { defaultValue: item.status })}
                </span>
                <span className="tabular-nums font-normal text-content-secondary">{t('taskList.groupCount', { count: item.count })}</span>
            </Button>
        </h2>
    ) : (
        <TaskItemContent task={item.task} level={0} ctx={rowContext} />
    );

    const selectionBarNode = selectedTasks.length > 0 && (
        <TaskSelectionBar
            iterationId={iterationId}
            selectedTasks={selectedTasks}
            matchingCount={visibleTasks.length}
            onSelectAll={selection.selectAll}
            onClearSelection={clearSelection}
            openAssign={preselectAllInBulk}
        />
    );

    if (isGraphLimitError(tasksError)) return <PagedTaskBrowser key={iterationId} iterationId={iterationId} />;
    if (isLoading) return <QueryLoadingState message={t('taskList.loading')} />;
    if ((!tasks && tasksError) || labelsError || allLabelsError) return <QueryErrorState error={tasksError ?? labelsError ?? allLabelsError} onRetry={() => { void refetchTasks(); void refetchLabels(); void refetchAllLabels(); }} />;

    return (
        <div className="space-y-4">
            <WorkFreshness stale={isRefetchError} refreshing={isFetching} onRefresh={() => { void refetchTasks(); }} />
            {assigneeOptionsError && (
                <QueryErrorState error={assigneeOptionsError} fallback={t('queryFeedback.optionLoadFailed')} onRetry={() => { void refetchAssigneeOptions(); }} />
            )}
            {reorderMutation.isError && (
                <QueryErrorState
                    error={reorderMutation.error}
                    fallback={t('taskList.reorderFailed')}
                    onRetry={() => {
                        void refetchTasks(); reorderMutation.reset();
                    }}
                />
            )}
            {(deleteMutation.isPending
                || reorderMutation.isPending
                || unmergeMutation.isPending) && (
                <p className="sr-only" role="status" aria-live="polite">
                    {deleteMutation.isPending
                        ? t('taskList.deletingTask')
                        : reorderMutation.isPending
                            ? t('taskList.savingOrder')
                            : t('taskList.splittingTask')}
                </p>
            )}
            {unmergeMutation.isError && (
                <QueryErrorState
                    error={unmergeMutation.error}
                    fallback={t('taskList.unmergeFailed')}
                    onRetry={() => {
                        void refetchTasks(); unmergeMutation.reset();
                    }}
                />
            )}
            {selectionBarHost ? (selectionBarNode && createPortal(selectionBarNode, selectionBarHost)) : selectionBarNode}

            <div ref={setRowsNode} className="rounded-lg border border-border bg-surface-card">
            {leadingRow && <div className="task-list-leading-row">{leadingRow}</div>}
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
                            <SortableTaskItem key={task.id} task={task} level={0} ctx={rowContext} />
                        ))}
                    </SortableContext>
                </DndContext>
            ) : virtualizeRows && rowsNode && scrollElement ? (
                <VirtualTaskRows items={rowItems} rowsNode={rowsNode} scrollElement={scrollElement} renderItem={renderRowItem} />
            ) : (
                rowItems.map(item => <Fragment key={rowItemKey(item)}>{renderRowItem(item)}</Fragment>)
            )}
            </div>

            {filteredAndSortedTasks?.length === 0 && (
                tasks && tasks.length > 0 ? (
                    <InlineEmptyState
                        headingLevel={2}
                        title={t('emptyStates.filtered.title')}
                        description={activeViewName ? t('taskList.noFilterMatchesViewBody', { view: activeViewName }) : t('taskList.noFilterMatchesBody')}
                        actions={hasActiveFilters && onClearFilters ? (
                            <Button variant="secondary" onClick={onClearFilters}>{t('emptyStates.filtered.clear')}</Button>
                        ) : undefined}
                    />
                ) : (
                    <NextStepEmptyState
                        title={t('emptyStates.tasks.title')}
                        description={t('emptyStates.tasks.body')}
                        fallback={onCreateTask
                            ? { label: t('emptyStates.tasks.action'), onClick: onCreateTask }
                            : { label: t('firstRun.steps.tasks.title'), to: scopeLink(firstRunPlanHref('work')) }}
                    />
                )
            )}

            {(editingTask || addingChildTo) && <GuardedTaskDrawer
                key={editingTask?.id ?? `child-${addingChildTo}`}
                title={editingTask ? t('tasks.editTask') : t('tasks.addSubtask')}
                closeLabel={t('actions.close')}
                onClose={() => { setEditingTask(null); setAddingChildTo(null); }}
                iterationId={iterationId} initialData={editingTask || undefined}
                parentId={addingChildTo} parentPriority={parentTaskForForm?.priority}
                parentProjectId={parentTaskForForm?.project_id ?? null}
                parentMilestoneId={parentTaskForForm?.milestone_id ?? null}
            />}

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
                onConfirm={() => { if (deletingTask) deleteMutation.mutate(deletingTask); }}
            />

        </div>
    );
};

/**
 * Renders only the rows near the viewport of the workspace scroller. Rows are
 * placed with `top`, not a transform, so a row's menu keeps its backdrop and layering.
 */
const VirtualTaskRows = ({ items, rowsNode, scrollElement, renderItem }: {
    items: RowItem[]; rowsNode: HTMLElement; scrollElement: HTMLElement; renderItem: (item: RowItem) => ReactNode;
}) => {
    'use no memo';
    const [scrollMargin, setScrollMargin] = useState(0);
    useLayoutEffect(() => {
        // Content above the list (filters, bulk panel) moves its offset in the scroller.
        const measure = () => setScrollMargin(rowsNode.getBoundingClientRect().top - scrollElement.getBoundingClientRect().top + scrollElement.scrollTop);
        measure();
        if (typeof ResizeObserver === 'undefined') return undefined;
        const observer = new ResizeObserver(measure);
        observer.observe(scrollElement.firstElementChild ?? scrollElement);
        return () => observer.disconnect();
    }, [rowsNode, scrollElement]);
    // Stable callbacks: new ones on every render would reset the measurements.
    const estimateSize = useCallback((index: number) => {
        const item = items[index];
        return item?.kind === 'task' && item.task.children?.length ? ROW_HEIGHT * (1 + item.task.children.length) : ROW_HEIGHT;
    }, [items]);
    const getItemKey = useCallback((index: number) => items[index] ? rowItemKey(items[index]) : index, [items]);
    const getScrollElement = useCallback(() => scrollElement, [scrollElement]);
    // eslint-disable-next-line react-hooks/incompatible-library -- 'use no memo' keeps this component uncompiled, so the virtualizer is read fresh each render.
    const virtualizer = useVirtualizer({ count: items.length, getScrollElement, estimateSize, getItemKey, overscan: 12, scrollMargin });
    return (
        <div style={{ height: virtualizer.getTotalSize(), position: 'relative' }}>
            {virtualizer.getVirtualItems().map(virtualRow => (
                <div key={virtualRow.key} data-index={virtualRow.index} ref={virtualizer.measureElement}
                    style={{ position: 'absolute', left: 0, width: '100%', top: virtualRow.start - scrollMargin }}>
                    {renderItem(items[virtualRow.index])}
                </div>
            ))}
        </div>
    );
};

/** What every row of the list shares: selection, hierarchy state and inline edits. */
interface RowContext {
    onOpen: (task: Task) => void;
    /** Opens the task that delivers a superseded task's work. */
    onOpenSuccessor: (taskId: number) => void;
    onAddSubtask: (id: number) => void;
    onDelete: (task: Task) => void;
    onUnmerge: (taskId: number) => void;
    isUnmergePending: boolean;
    sensors: ReturnType<typeof useSensors>;
    onChildDragEnd: (parent: Task, event: DragEndEvent) => void;
    isDraggingEnabled: boolean;
    taskMap: Map<number, Task>;
    labelsBySlug: Map<string, Label>;
    nowMs: number;
    selectedIds: Set<number>;
    selectableIds: Set<number>;
    onToggleSelect: (taskId: number, shiftKey: boolean) => void;
    collapsedParents: Set<number>;
    onToggleParent: (taskId: number) => void;
    assigneeOptions: TaskRowAssigneeOption[];
    agentFacts: AgentRowFacts;
    onAssign: (task: Task, assigneeId: number | null) => void;
    onStatusChange: (task: Task, status: TaskStatus) => void;
    /** Names why each task is at risk, when the list was opened from Plan's at-risk signals. */
    showRiskReasons: boolean;
}

interface TaskItemProps {
    task: Task;
    level: number;
    ctx: RowContext;
}

// Sortable wrapper for root-level and child tasks
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
                dragging={isDragging}
            />
        </div>
    );
};

interface TaskItemContentProps extends TaskItemProps {
    dragHandleProps?: Record<string, unknown>;
    dragging?: boolean;
}

const TaskItemContent = ({ task, level, ctx, dragHandleProps, dragging = false }: TaskItemContentProps) => {
    const [showDetails, setShowDetails] = useState(false);
    const detailsId = useId();
    const { t } = useTranslation();
    const hasChildren = task.children && task.children.length > 0;
    const isExpanded = !ctx.collapsedParents.has(task.id);
    const isSelectable = ctx.selectableIds.has(task.id);

    const detailsCount = Number(task.is_optional)
        + Number(task.is_deferred)
        + Number(Boolean(task.claimed_by))
        + Number(task.dependencies.length > 0)
        + task.tags.length
        + 1;
    const claimExpired = Boolean(task.claim_expires_at && new Date(task.claim_expires_at).getTime() < ctx.nowMs);

    const handle = ctx.isDraggingEnabled && dragHandleProps ? (
        <Button data-page-chrome-control="button"
            type="button"
            aria-label={`${t('literalWords.drag')}: ${task.title}`} title={`${t('literalWords.drag')}: ${task.title}`}
                className="shrink-0 cursor-grab touch-none p-1 text-content-tertiary hover:text-content-secondary active:cursor-grabbing"
            {...dragHandleProps}
         variant="plain">
            <GripVertical className="w-4 h-4" />
        </Button>
    ) : undefined;

    const lead = (
        <>
            {hasChildren ? (
                <Button data-page-chrome-control="button"
                    type="button"
                    aria-label={`${isExpanded ? t('surfaces.ganttChart.collapseAll') : t('literalWords.expand')}: ${task.title}`} title={`${isExpanded ? t('surfaces.ganttChart.collapseAll') : t('literalWords.expand')}: ${task.title}`}
                    aria-expanded={isExpanded}
                    onClick={() => ctx.onToggleParent(task.id)}
                    className="shrink-0 rounded p-1 hover:bg-surface-subtle"
                 variant="plain">
                    {isExpanded ? <ChevronDown className="h-4 w-4" /> : <ChevronRight className="h-4 w-4" />}
                </Button>
            ) : (
                <span className="h-6 w-6 shrink-0" aria-hidden="true" />
            )}
        </>
    );

    const childProps = (child: Task) => ({ task: child, level: level + 1, ctx });
    const agentRow = agentRowValues(task, ctx.assigneeOptions, ctx.agentFacts);

    return (
        <div className="group">
            <TaskRow
                id={task.id}
                title={task.title}
                status={task.status}
                state={stateOf(task)}
                successor={task.successor_task_id ? { id: task.successor_task_id, onOpen: () => ctx.onOpenSuccessor(task.successor_task_id as number) } : null}
                statusLocked={task.is_composite || Boolean(hasChildren)}
                priority={task.priority}
                chip={taskStateChip(task, ctx.taskMap)}
                assignee={task.assignee ?? null}
                assigneeOptions={ctx.assigneeOptions}
                onAssign={assigneeId => ctx.onAssign(task, assigneeId)}
                dispatch={agentRow.dispatch}
                reviewer={agentRow.reviewer}
                effort={getEffectiveEffort(task)}
                level={level}
                lead={lead}
                handle={handle}
                revealed={dragging}
                onOpen={() => ctx.onOpen(task)}
                onStatusChange={status => ctx.onStatusChange(task, status)}
                selected={ctx.selectedIds.has(task.id)}
                onToggleSelect={isSelectable ? ({ shiftKey }) => ctx.onToggleSelect(task.id, shiftKey) : undefined}
                selectDisabledReason={isSelectable ? undefined : t('taskList.selectParentUnavailable')}
                reasons={ctx.showRiskReasons ? atRiskReasons(task, t) : undefined}
                overdue={task.is_overdue}
                deferred={task.is_deferred}
                menuItems={[
                    {
                        label: t('taskList.detailsCount', { count: detailsCount }),
                        icon: <Info className="h-4 w-4" aria-hidden="true" />,
                        onSelect: () => setShowDetails(value => !value),
                    },
                    {
                        label: t('tasks.editTask'),
                        icon: <Edit className="h-4 w-4" aria-hidden="true" />,
                        onSelect: () => ctx.onOpen(task),
                    },
                    {
                        label: t('tasks.addSubtask'),
                        icon: <Plus className="h-4 w-4" aria-hidden="true" />,
                        onSelect: () => ctx.onAddSubtask(task.id),
                    },
                    ...(hasChildren ? [{
                        label: t('taskList.unmergeTitle'),
                        icon: <Unlink className="h-4 w-4" aria-hidden="true" />,
                        onSelect: () => ctx.onUnmerge(task.id),
                        disabled: ctx.isUnmergePending,
                    }] : []),
                    {
                        label: t('actions.delete'),
                        icon: <Trash2 className="h-4 w-4" aria-hidden="true" />,
                        onSelect: () => ctx.onDelete(task),
                        tone: 'danger' as const,
                    },
                ]}
            />

            {showDetails && (
                <div id={detailsId} className="flex flex-wrap items-center gap-1.5 border-b border-border-subtle bg-surface-muted py-2 pr-3 text-xs text-content-secondary"
                    style={{ paddingLeft: 40 + level * 24 }}>
                    {task.is_overdue && (
                        <span className="flex items-center rounded-full bg-feedback-danger-muted px-2 py-0.5 text-feedback-danger-foreground">
                            <AlertTriangle aria-hidden="true" className="mr-1 h-3 w-3" /> {t('taskList.overdue')}
                        </span>
                    )}
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
                        <span className={clsx("flex items-center rounded-full px-2 py-0.5",
                            claimExpired ? "text-feedback-warning-foreground bg-feedback-warning-muted" : "text-action bg-status-active-muted")}>
                            <Bot className="mr-1 h-3 w-3" aria-hidden="true" />
                            {claimExpired
                                ? t('taskList.claimExpired', { name: task.claimed_by.display_name })
                                : t('taskList.claimedBy', { name: task.claimed_by.display_name })}
                        </span>
                    )}
                    <TaskAgentReadinessBadge readiness={task.agent_readiness} />
                    {task.dependencies.length > 0 && (
                        <span>
                            {t('taskList.dependsOn')}: {getDependencyNames(task.dependencies, ctx.taskMap).join(', ')}
                            {task.dependencies.length > 3 && ` +${task.dependencies.length - 3}`}
                        </span>
                    )}
                    {task.tags.map((tag, idx) => {
                        const label = ctx.labelsBySlug.get(tag);
                        return <LabelChip key={idx} color={label?.color}>{tag}</LabelChip>;
                    })}
                </div>
            )}

            {hasChildren && isExpanded && (
                <div>
                    {ctx.isDraggingEnabled ? (
                        <DndContext
                            sensors={ctx.sensors}
                            collisionDetection={closestCenter}
                            onDragEnd={(event) => ctx.onChildDragEnd(task, event)}
                        >
                            <SortableContext
                                items={task.children.map(c => c.id)}
                                strategy={verticalListSortingStrategy}
                            >
                                {task.children.map(child => <SortableTaskItem key={child.id} {...childProps(child)} />)}
                            </SortableContext>
                        </DndContext>
                    ) : (
                        task.children.map(child => <TaskItemContent key={child.id} {...childProps(child)} />)
                    )}
                </div>
            )}
        </div>
    );
};

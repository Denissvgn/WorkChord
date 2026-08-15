import { useState, useMemo, useId, useRef } from 'react';
import { useTranslation } from 'react-i18next';
import { Link } from 'react-router-dom';
import {
    DndContext,
    closestCorners,
    KeyboardSensor,
    PointerSensor,
    useSensor,
    useSensors,
    DragOverlay,
    defaultDropAnimationSideEffects,
} from '@dnd-kit/core';
import type { DragStartEvent, DragEndEvent } from '@dnd-kit/core';
import { sortableKeyboardCoordinates } from '@dnd-kit/sortable';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { taskService } from '../../../services/taskService';
import { teamService } from '../../../services/teamService';
import { labelService } from '../../../services/labelService';
import type { Task, TaskStatus, TaskUpdate } from '../../../types/task';
import type { TaskFilters } from '../TaskFiltersBar';
import { filterTaskWithChildren } from '../../../utils/taskFilters';
import { KanbanColumn } from './KanbanColumn';
import { KanbanCard } from './KanbanCard';
import { createPortal } from 'react-dom';
import { STATUS_TONE } from '../../ui/tone';
import { QueryErrorState, QueryLoadingState } from '../../feedback/QueryState';
import { Button } from '../../common/Button';
import { Modal } from '../../common/Modal';

interface KanbanBoardProps {
    iterationId: number;
    filters?: TaskFilters;
}

type ColumnId = 'planned-unassigned' | 'planned-assigned' | 'active' | 'resolved' | 'closed';

const COLUMNS: { id: ColumnId; titleKey: string; status: TaskStatus }[] = [
    { id: 'planned-unassigned', titleKey: 'backlogUnassigned', status: 'planned' },
    { id: 'planned-assigned', titleKey: 'readyAssigned', status: 'planned' },
    { id: 'active', titleKey: 'inProgress', status: 'active' },
    { id: 'resolved', titleKey: 'resolved', status: 'resolved' },
    { id: 'closed', titleKey: 'closed', status: 'closed' },
];

const VALID_TRANSITIONS: Record<TaskStatus, TaskStatus[]> = {
    planned: ['active'],
    active: ['resolved'],
    resolved: ['active', 'closed'],
    closed: [],
};

type BoardTaskUpdate = Pick<TaskUpdate, 'assignee_id'> & {
    status?: TaskStatus;
};

type OwnershipSelection = {
    task: Task;
    updates: BoardTaskUpdate;
    targetColumn: ColumnId;
};

export const KanbanBoard = ({ iterationId, filters }: KanbanBoardProps) => {
    const { t } = useTranslation();
    const queryClient = useQueryClient();
    const [activeId, setActiveId] = useState<number | null>(null);
    const [ownershipSelection, setOwnershipSelection] = useState<OwnershipSelection | null>(null);
    const [selectedAssigneeId, setSelectedAssigneeId] = useState<number | null>(null);
    const assigneeSelectId = useId();
    const assigneeSelectRef = useRef<HTMLSelectElement>(null);

    // Data Fetching
    const tasksQuery = useQuery({
        queryKey: ['tasks', iterationId],
        queryFn: () => taskService.getByIteration(iterationId),
    });

    const teamQuery = useQuery({
        queryKey: ['team', iterationId],
        queryFn: () => teamService.getByIteration(iterationId),
    });

    const labelsQuery = useQuery({
        queryKey: ['label-groups'],
        queryFn: () => labelService.getGroups(),
    });
    const tasks = useMemo(() => tasksQuery.data ?? [], [tasksQuery.data]);
    const team = useMemo(() => teamQuery.data ?? [], [teamQuery.data]);
    const labelGroups = useMemo(() => labelsQuery.data ?? [], [labelsQuery.data]);

    // feedback-policy: mutation pending,inline - drag is locked while saving and selection failures stay recoverable.
    const updateTaskMutation = useMutation({
        mutationFn: async ({ task, updates }: { task: Task; updates: BoardTaskUpdate }) => {
            const { status, ...fieldUpdates } = updates;
            let expectedVersion = task.version;
            if (status && status !== task.status && !VALID_TRANSITIONS[task.status]?.includes(status)) {
                throw new Error(t('surfaces.kanbanBoard.invalidTransition', { from: task.status, to: status }));
            }
            if (Object.keys(fieldUpdates).length > 0) {
                const updated = await taskService.update(task.id, {
                    ...fieldUpdates,
                    expected_version: expectedVersion,
                });
                expectedVersion = updated.version;
            }
            if (status && status !== task.status) {
                return taskService.changeStatus(
                    task.id,
                    status,
                    t('surfaces.kanbanBoard.movedOnBoard'),
                    expectedVersion,
                );
            }
            return null;
        },
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['tasks', iterationId] });
            queryClient.invalidateQueries({ queryKey: ['gantt'] });
            queryClient.invalidateQueries({ queryKey: ['workload'] });
        },
    });

    const closeOwnershipSelection = () => {
        if (updateTaskMutation.isPending) return;
        setOwnershipSelection(null);
        setSelectedAssigneeId(null);
        updateTaskMutation.reset();
    };

    const confirmOwnershipSelection = async () => {
        if (!ownershipSelection || selectedAssigneeId === null || updateTaskMutation.isPending) return;

        try {
            await updateTaskMutation.mutateAsync({
                task: ownershipSelection.task,
                updates: {
                    ...ownershipSelection.updates,
                    assignee_id: selectedAssigneeId,
                },
            });
            setOwnershipSelection(null);
            setSelectedAssigneeId(null);
        } catch {
            // The mutation's visible recovery state keeps the selection open.
        }
    };

    // Filtering & Grouping
    const filteredTasks = useMemo(() => {
        return tasks
            .map(task => filterTaskWithChildren(task, filters, labelGroups))
            .filter((t): t is Task => t !== null);
    }, [tasks, filters, labelGroups]);

    const columns = useMemo(() => {
        const cols: Record<ColumnId, Task[]> = {
            'planned-unassigned': [],
            'planned-assigned': [],
            'active': [],
            'resolved': [],
            'closed': [],
        };

        const flatten = (list: Task[]) => {
            list.forEach(task => {
                // Determine column
                let colId: ColumnId = 'planned-unassigned';
                if (task.status === 'planned') {
                    colId = task.assignee ? 'planned-assigned' : 'planned-unassigned';
                } else if (task.status === 'active') colId = 'active';
                else if (task.status === 'resolved') colId = 'resolved';
                else if (task.status === 'closed') colId = 'closed';

                cols[colId].push(task);

                // For now, we only show top-level tasks or handle children differently?
                // The current list view handles hierarchy. In Kanban, typically we flatten or show parents.
                // Assuming flattening for the board or just showing root.
                // Let's show all matching tasks flat for simplicity in this version,
                // OR just root tasks. Let's stick to root tasks as per task list structure,
                // but if filters match children, the helper returns the parent with filtered children.
                // The task list normally renders tree. Kanban usually renders cards.
                // If I have subtasks, where do they go?
                // Visualizing subtasks in Kanban is hard.
                // Decision: Only show items that are visible in the list.
                // If the filter returns a hierarchy, we only render the top-level items returned.
            });
        };

        flatten(filteredTasks);
        return cols;
    }, [filteredTasks]);

    // Sensors
    const sensors = useSensors(
        useSensor(PointerSensor, { activationConstraint: { distance: 5 } }),
        useSensor(KeyboardSensor, { coordinateGetter: sortableKeyboardCoordinates })
    );

    const handleDragStart = (event: DragStartEvent) => {
        if (updateTaskMutation.isPending || ownershipSelection) return;
        setActiveId(event.active.id as number);
    };

    const handleDragEnd = (event: DragEndEvent) => {
        if (updateTaskMutation.isPending) return;
        const { active, over } = event;
        setActiveId(null);

        if (!over) return;

        const activeTask = tasks.find(t => t.id === active.id);
        if (!activeTask) return; // Should search in full tree if needed

        // Find root-level task if not found (in case we flatten later, but for now we rely on tasks being flat-ish or only dragging roots)
        // Actually `tasks` from service is flat list? No, it's tree. `children` prop.
        // We need to find the task deeply.

        const findTaskDeep = (id: number, list: Task[]): Task | undefined => {
            for (const t of list) {
                if (t.id === id) return t;
                if (t.children) {
                    const found = findTaskDeep(id, t.children);
                    if (found) return found;
                }
            }
            return undefined;
        };
        const task = findTaskDeep(active.id as number, tasks);
        if (!task) return;


        const overId = over.id;
        // Determine target column
        let targetColumn: ColumnId | undefined;

        if (COLUMNS.some(c => c.id === overId)) {
            targetColumn = overId as ColumnId;
        } else {
            // Dropped on another task? Find its column.
            // Simplified: if dropped on a task, we assume the same column as that task.
            // We need to reverse lookup the column of the `over` task.
            // This is expensive to do on every drop without a map.
            // Let's iterate columns.
            for (const col of COLUMNS) {
                if (columns[col.id].some(t => t.id === overId)) {
                    targetColumn = col.id;
                    break;
                }
            }
        }

        if (!targetColumn) return;

        // Calculate updates
        const updates: BoardTaskUpdate = {};

        // Status updates based on column
        if (targetColumn === 'planned-unassigned') {
            updates.status = 'planned';
            updates.assignee_id = null; // Forced unassign
        } else if (targetColumn === 'planned-assigned') {
            updates.status = 'planned';
        } else if (targetColumn === 'active') {
            updates.status = 'active';
        } else if (targetColumn === 'resolved') {
            updates.status = 'resolved';
        } else if (targetColumn === 'closed') {
            updates.status = 'closed';
        }

        const ownershipWouldChange = !task.assignee
            && (targetColumn === 'planned-assigned' || targetColumn === 'active');

        if (ownershipWouldChange) {
            updateTaskMutation.reset();
            setSelectedAssigneeId(null);
            setOwnershipSelection({ task, updates, targetColumn });
            return;
        }

        // Apply update if changed
        const statusChanged = updates.status && updates.status !== task.status;
        const assigneeChanged = updates.assignee_id !== undefined && updates.assignee_id !== task.assignee?.id;

        if (statusChanged || assigneeChanged) {
            updateTaskMutation.mutate({ task, updates });
        }
    };

    // Helper for overlay: find deeply
    const overlayTask = useMemo(() => {
        if (!activeId) return null;
        const find = (list: Task[]): Task | undefined => {
            for (const t of list) {
                if (t.id === activeId) return t;
                if (t.children) {
                    const f = find(t.children);
                    if (f) return f;
                }
            }
            return undefined;
        };
        return find(tasks);
    }, [activeId, tasks]);


    if (tasksQuery.isLoading || teamQuery.isLoading || labelsQuery.isLoading) return <QueryLoadingState />;
    const queryError = tasksQuery.error ?? teamQuery.error ?? labelsQuery.error;
    if (queryError) return <QueryErrorState error={queryError} onRetry={() => { void tasksQuery.refetch(); void teamQuery.refetch(); void labelsQuery.refetch(); }} />;
    const ownershipColumnTitle = ownershipSelection
        ? t(`surfaces.kanbanBoard.columns.${COLUMNS.find(column => column.id === ownershipSelection.targetColumn)?.titleKey ?? 'inProgress'}`)
        : '';

    return (
        <DndContext
            sensors={sensors}
            collisionDetection={closestCorners}
            onDragStart={handleDragStart}
            onDragEnd={handleDragEnd}
            onDragCancel={() => setActiveId(null)}
        >
            <div className="space-y-3" aria-busy={updateTaskMutation.isPending}>
                {updateTaskMutation.isError && (
                    <QueryErrorState
                        error={updateTaskMutation.error}
                        fallback={t('surfaces.kanbanBoard.updateFailed')}
                        onRetry={() => {
                            updateTaskMutation.reset();
                            void tasksQuery.refetch();
                        }}
                    />
                )}
                <div className="flex h-full gap-4 overflow-x-auto pb-4 items-start">
                    {COLUMNS.map((col) => (
                        <KanbanColumn
                            key={col.id}
                            id={col.id}
                            title={t(`surfaces.kanbanBoard.columns.${col.titleKey}`)}
                            tasks={columns[col.id]}
                            count={columns[col.id].length}
                            tone={STATUS_TONE[col.status]}
                        />
                    ))}
                </div>
            </div>

            {createPortal(
                <DragOverlay dropAnimation={{ sideEffects: defaultDropAnimationSideEffects({ styles: { active: { opacity: '0.5' } } }) }}>
                    {overlayTask ? <KanbanCard task={overlayTask} /> : null}
                </DragOverlay>,
                document.body
            )}

            <Modal
                open={Boolean(ownershipSelection)}
                title={team.length > 0
                    ? t('surfaces.kanbanBoard.chooseAssignee')
                    : t('surfaces.kanbanBoard.noAssigneeAvailable')}
                description={ownershipSelection
                    ? team.length > 0
                        ? t('surfaces.kanbanBoard.chooseAssigneeDescription', {
                            title: ownershipSelection.task.title,
                            column: ownershipColumnTitle,
                        })
                        : t('surfaces.kanbanBoard.noAssigneeAvailableDescription', {
                            title: ownershipSelection.task.title,
                        })
                    : ''}
                onClose={closeOwnershipSelection}
                closeLabel={t('actions.close')}
                closeDisabled={updateTaskMutation.isPending}
                initialFocusRef={team.length > 0 ? assigneeSelectRef : undefined}
                footer={(
                    <div className="flex flex-wrap justify-end gap-3">
                        <Button
                            type="button"
                            variant="secondary"
                            disabled={updateTaskMutation.isPending}
                            onClick={closeOwnershipSelection}
                        >
                            {t('actions.cancel')}
                        </Button>
                        {team.length > 0 ? (
                            <Button
                                type="button"
                                isLoading={updateTaskMutation.isPending}
                                disabled={selectedAssigneeId === null}
                                onClick={() => { void confirmOwnershipSelection(); }}
                            >
                                {t('surfaces.kanbanBoard.assignAndMove')}
                            </Button>
                        ) : (
                            <Link
                                to={`/team?action=assign&iterationId=${iterationId}`}
                                className="btn primary"
                                onClick={closeOwnershipSelection}
                            >
                                {t('surfaces.kanbanBoard.addTeamMember')}
                            </Link>
                        )}
                    </div>
                )}
            >
                {ownershipSelection && team.length > 0 ? (
                    <div className="space-y-4">
                        <label className="block text-sm font-medium text-content-primary" htmlFor={assigneeSelectId}>
                            {t('surfaces.kanbanBoard.assignee')}
                        </label>
                        <select
                            ref={assigneeSelectRef}
                            id={assigneeSelectId}
                            value={selectedAssigneeId ?? ''}
                            onChange={event => setSelectedAssigneeId(event.target.value ? Number(event.target.value) : null)}
                            disabled={updateTaskMutation.isPending}
                            className="w-full rounded-md border border-border-strong bg-surface-card px-3 py-2 text-base text-content-primary shadow-sm focus:outline-none focus:ring-2 focus:ring-focus disabled:cursor-not-allowed disabled:opacity-60"
                        >
                            <option value="">{t('surfaces.kanbanBoard.chooseAssigneePlaceholder')}</option>
                            {team.map(member => (
                                <option key={member.id} value={member.id}>{member.name}</option>
                            ))}
                        </select>
                        {updateTaskMutation.isError && (
                            <p role="alert" className="text-sm text-feedback-danger-foreground">
                                {t('surfaces.kanbanBoard.assignmentMoveFailed')}
                            </p>
                        )}
                    </div>
                ) : undefined}
            </Modal>
        </DndContext>
    );
};

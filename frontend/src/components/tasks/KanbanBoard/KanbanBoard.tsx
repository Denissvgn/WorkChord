import { ButtonLink } from '../../common/ButtonLink';
import { isGraphLimitError } from '../../../utils/graphLimitError';
import { PagedTaskBrowser } from '../PagedTaskBrowser';
import { useState, useMemo, useId, useRef } from 'react';
import { useTranslation } from 'react-i18next';
import { useSearchParams } from 'react-router-dom';
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
import type { Task, TaskBatchUpdateResponse, TaskStatus, TaskUpdate } from '../../../types/task';
import type { TaskFilters } from '../TaskFiltersBar';
import { selectVisibleWork } from '../../../utils/visibleWork';
import { filterTaskBySearch } from '../../../utils/taskFilters';
import { AssigneePicker } from '../AssigneePicker';
import { planningInputService } from '../../../services/planningInputService';
import type { TeamMemberProfile } from '../../../types/team';
import { TaskEditorDrawer } from '../TaskEditorDrawer';
import { WorkFreshness } from '../../feedback/WorkFreshness';
import { KanbanColumn } from './KanbanColumn';
import type { BoardCardContext } from './KanbanCard';
import { KanbanCard } from './KanbanCard';
import { createPortal } from 'react-dom';
import { STATUS_TONE } from '../../ui/tone';
import { QueryErrorState, QueryLoadingState } from '../../feedback/QueryState';
import { Button } from '../../common/Button';
import { Modal } from '../../common/Modal';
import { feedbackMessage } from '../../../features/mutationFeedback';
import type { MutationFeedbackMeta } from '../../../features/mutationFeedback';
import { canTransition } from '../../../features/taskTransitions';

interface KanbanBoardProps {
    iterationId: number;
    filters?: TaskFilters;
}

type ColumnId = 'planned-unassigned' | 'planned-assigned' | 'active' | 'resolved' | 'closed';

const COLUMNS: { id: ColumnId; titleKey: string; status: TaskStatus; captionKey?: 'noAssignee' | 'assigned' }[] = [
    // Headers use the lifecycle names of the vocabulary (the same words as status everywhere else);
    // Planned splits by whether someone owns it, and the caption says which half a column is.
    { id: 'planned-unassigned', titleKey: 'plannedUnassigned', status: 'planned', captionKey: 'noAssignee' },
    { id: 'planned-assigned', titleKey: 'plannedAssigned', status: 'planned', captionKey: 'assigned' },
    { id: 'active', titleKey: 'active', status: 'active' },
    { id: 'resolved', titleKey: 'resolved', status: 'resolved' },
    { id: 'closed', titleKey: 'closed', status: 'closed' },
];


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
    const [openedTaskId, setOpenedTaskId] = useState<number | null>(null);
    const openTrigger = useRef<HTMLElement | null>(null);
    const [ownershipSelection, setOwnershipSelection] = useState<OwnershipSelection | null>(null);
    const [selectedAssigneeId, setSelectedAssigneeId] = useState<number | null>(null);
    const assigneeSelectId = useId();
    const [selectedProfile, setSelectedProfile] = useState<TeamMemberProfile | null>(null);
    // The list's search applies to the board too: the same ?q= in the toolbar narrows both views.
    const [searchParams] = useSearchParams();
    const searchText = searchParams.get('q')?.slice(0, 200) ?? '';

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
        meta: {
            success: (_data, variables) => feedbackMessage(t, 'saved', 'task', (variables as { task: Task }).task.title),
            // Moves the card back: same status and assignee as before the move.
            undo: (data, variables) => {
                const { task, updates } = variables as { task: Task; updates: BoardTaskUpdate };
                const moved = (data as TaskBatchUpdateResponse).updated_tasks.find(item => item.id === task.id);
                if (!moved) return null;
                // A status the server cannot move back to directly gets no Undo.
                if (updates.status && updates.status !== task.status && !canTransition(updates.status, task.status)) return null;
                const restore: TaskUpdate = {};
                if (updates.status && updates.status !== task.status) restore.status = task.status;
                if ('assignee_id' in updates) restore.assignee_id = task.assignee?.id ?? null;
                return { run: () => taskService.batchUpdate(iterationId, { expected_revision: moved.iteration_revision,
                    tasks: [{ task_id: task.id, expected_version: moved.version, update: restore, status_reason: t('feedback.undoReason') }] }) };
            },
        } satisfies MutationFeedbackMeta,
        mutationFn: async ({ task, updates, profile }: { task: Task; updates: BoardTaskUpdate; profile?: TeamMemberProfile | null }) => {
            const { status, ...fieldUpdates } = updates;
            if (status && status !== task.status && !canTransition(task.status, status)) {
                throw new Error(t('surfaces.kanbanBoard.invalidTransition', { from: task.status, to: status }));
            }
            let expectedRevision = task.iteration_revision;
            if (profile) {
                // A person or agent outside the iteration joins it first; re-reading the team keeps a retry from adding them twice.
                const currentMembers = await teamService.getByIteration(iterationId);
                let member = currentMembers.find(candidate => candidate.profile_id === profile.id);
                if (!member) {
                    const context = await planningInputService.readInitial('member', iterationId, true, { profile_id: profile.id });
                    member = await teamService.create(iterationId, {
                        profile_id: profile.id, name: profile.display_name,
                        position: profile.headline?.trim() || t(profile.profile_kind === 'agent' ? 'assigneePicker.agentRole' : 'assigneePicker.personRole'),
                        email: profile.email ?? undefined,
                        availability_percent: 100, professionalism_coefficient: 1,
                        operational_utilization: profile.profile_kind === 'agent' ? 0 : 20,
                    }, context.expected_revisions);
                }
                fieldUpdates.assignee_id = member.id;
                // Adding capacity changes the iteration revision that the move must carry.
                const context = await planningInputService.readInitial('iteration', iterationId);
                expectedRevision = context.expected_revisions[iterationId];
                queryClient.setQueryData(['team', iterationId], [...currentMembers.filter(candidate => candidate.id !== member.id), member]);
            }
            return taskService.batchUpdate(iterationId, {
                expected_revision: expectedRevision,
                tasks: [{ task_id: task.id, expected_version: task.version,
                    update: { ...fieldUpdates, status }, status_reason: t('surfaces.kanbanBoard.movedOnBoard') }],
            });
        },
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['team', iterationId] });
            queryClient.invalidateQueries({ queryKey: ['tasks', iterationId] });
            queryClient.invalidateQueries({ queryKey: ['gantt'] });
            queryClient.invalidateQueries({ queryKey: ['workload'] });
        },
    });

    const closeOwnershipSelection = () => {
        if (updateTaskMutation.isPending) return;
        setOwnershipSelection(null);
        setSelectedAssigneeId(null);
        setSelectedProfile(null);
        updateTaskMutation.reset();
    };

    const confirmOwnershipSelection = async () => {
        if (!ownershipSelection || (selectedAssigneeId === null && !selectedProfile) || updateTaskMutation.isPending) return;

        try {
            await updateTaskMutation.mutateAsync({
                task: ownershipSelection.task,
                updates: {
                    ...ownershipSelection.updates,
                    assignee_id: selectedAssigneeId,
                },
                profile: selectedProfile,
            });
            setOwnershipSelection(null);
            setSelectedAssigneeId(null);
            setSelectedProfile(null);
        } catch {
            // The mutation's visible recovery state keeps the selection open.
        }
    };

    // Filtering & Grouping
    const searchedTasks = useMemo(() => tasks
        .map(task => filterTaskBySearch(task, searchText))
        .filter((task): task is Task => task !== null), [tasks, searchText]);
    const filteredTasks = useMemo(() => selectVisibleWork(searchedTasks, filters, labelGroups).leaves, [searchedTasks, filters, labelGroups]);

    // What a card shows beyond its task: the task map its state chip reads.
    const taskMap = useMemo(() => {
        const map = new Map<number, Task>();
        const walk = (list: Task[]) => list.forEach(task => {
            map.set(task.id, task);
            if (task.children) walk(task.children);
        });
        walk(tasks);
        return map;
    }, [tasks]);
    const cardContext = useMemo<BoardCardContext>(() => ({ taskMap }), [taskMap]);

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

        // Cards can be nested tasks, so look through the whole tree.
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
            setSelectedProfile(null);
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


    if (isGraphLimitError(tasksQuery.error)) return <PagedTaskBrowser key={iterationId} iterationId={iterationId} />;
    if (tasksQuery.isLoading || teamQuery.isLoading || labelsQuery.isLoading) return <QueryLoadingState />;
    const queryError = tasksQuery.error ?? teamQuery.error ?? labelsQuery.error;
    if (queryError) return <QueryErrorState error={queryError} onRetry={() => { void tasksQuery.refetch(); void teamQuery.refetch(); void labelsQuery.refetch(); }} />;
    const ownershipColumnTitle = ownershipSelection
        ? t(`surfaces.kanbanBoard.columns.${COLUMNS.find(column => column.id === ownershipSelection.targetColumn)?.titleKey ?? 'active'}`)
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
                <WorkFreshness stale={tasksQuery.isRefetchError}
                    refreshing={tasksQuery.isFetching} onRefresh={() => { void tasksQuery.refetch(); }} />
                <TaskEditorDrawer open={openedTaskId !== null} taskId={openedTaskId} iterationId={iterationId}
                    onClose={() => setOpenedTaskId(null)} restoreFocusRef={openTrigger} />
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
                {/* Fluid columns share the width; empty ones fold, so all five fit at 1440. */}
                <div className="flex h-full items-start gap-3 overflow-x-auto pb-4">
                    {COLUMNS.map((col) => (
                        <KanbanColumn
                            key={col.id}
                            id={col.id}
                            onOpen={(task, trigger) => { openTrigger.current = trigger ?? null; setOpenedTaskId(task.id); }}
                            title={t(`statuses.${col.status}`)}
                            caption={col.captionKey ? t(`surfaces.kanbanBoard.captions.${col.captionKey}`) : undefined}
                            tasks={columns[col.id]}
                            count={columns[col.id].length}
                            tone={STATUS_TONE[col.status]}
                            context={cardContext}
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
                title={t('surfaces.kanbanBoard.chooseAssignee')}
                description={ownershipSelection
                    ? t('surfaces.kanbanBoard.chooseAssigneeDescription', {
                        title: ownershipSelection.task.title,
                        column: ownershipColumnTitle,
                    })
                    : ''}
                onClose={closeOwnershipSelection}
                closeLabel={t('actions.close')}
                closeDisabled={updateTaskMutation.isPending}
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
                        {team.length === 0 && (
                            <ButtonLink
                                to={`/plan?step=team&iteration=${iterationId}`}

                                onClick={closeOwnershipSelection}
                             variant="secondary">
                                {t('surfaces.kanbanBoard.addTeamMember')}
                            </ButtonLink>
                        )}
                        <Button
                            type="button"
                            isLoading={updateTaskMutation.isPending}
                            disabled={selectedAssigneeId === null && !selectedProfile}
                            onClick={() => { void confirmOwnershipSelection(); }}
                        >
                            {selectedProfile ? t('assigneePicker.addAndAssign') : t('surfaces.kanbanBoard.assignAndMove')}
                        </Button>
                    </div>
                )}
            >
                {ownershipSelection ? (
                    <div className="space-y-4">
                        <AssigneePicker
                            id={assigneeSelectId}
                            members={team}
                            value={selectedAssigneeId}
                            profile={selectedProfile}
                            disabled={updateTaskMutation.isPending}
                            allowAdd
                            onChange={(memberId, profile) => { setSelectedAssigneeId(memberId); setSelectedProfile(profile); }}
                        />
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

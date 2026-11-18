import { useCallback, useMemo, useState } from 'react';
import type { ReactNode } from 'react';
import { TaskEditorDrawer } from '../tasks/TaskEditorDrawer';
import i18n from '../../i18n/i18n';
import type { Task } from '../../types/task';
import { TaskRow } from '../tasks/TaskRow';
import { TaskSelectionBar } from '../tasks/TaskSelectionBar';
import { taskStateChip } from '../tasks/taskStateChip';
import { getEffectiveEffort } from '../tasks/taskRowValues';
import { useTaskRowEdits } from '../tasks/useTaskRowEdits';
import { useIterationRowData } from '../tasks/useIterationRowData';
import { agentRowValues, useAgentRowFacts } from '../tasks/useAgentRowFacts';
import { useTaskSelection } from '../tasks/useTaskSelection';
import { QueryErrorState } from '../feedback/QueryState';

const t = i18n.t.bind(i18n);

export interface ProjectTaskSection {
    key: string;
    heading?: ReactNode;
    tasks: Task[];
}

interface ProjectTaskTreeProps {
    /** Lists of tasks shown one after another. They share one selection and one bulk bar. */
    sections: ProjectTaskSection[];
    /**
     * Every task of the project, with children, when the sections show only some of them. The
     * Waits chip reads dependency status from these and from each shown iteration's tasks, never
     * from the shown rows alone, where a finished dependency would be missing and count as open.
     */
    dependencyTasks?: Task[];
}

/** The tree as one flat, indented list, so each task is a divided row, not a card inside a card. */
const flattenTree = (tasks: Task[], level = 0): { task: Task; level: number }[] => tasks.flatMap(task => [
    { task, level },
    ...flattenTree(task.children ?? [], level + 1),
]);

const isLeaf = (task: Task) => !task.is_composite && (task.children?.length ?? 0) === 0;

export const ProjectTaskTree = ({ sections, dependencyTasks }: ProjectTaskTreeProps) => {
    const [selectedTask, setSelectedTask] = useState<number | null>(null);
    const rowEdits = useTaskRowEdits();
    const flatSections = useMemo(() => sections.map(section => ({ ...section, rows: flattenTree(section.tasks) })), [sections]);
    const flat = useMemo(() => flatSections.flatMap(section => section.rows), [flatSections]);
    const taskMap = useMemo(() => new Map(flat.map(({ task }) => [task.id, task])), [flat]);
    // Only tasks of an iteration can be picked for, or changed together; backlog tasks have no team.
    // Each iteration's tasks load as the Tasks list loads them, for the dependency status of the chips.
    const { optionsByIteration, tasksById: iterationTasks, error: optionsError, refetch: refetchOptions } = useIterationRowData(flat.map(({ task }) => task.iteration_id));
    const dependencyMap = useMemo(() => {
        const map = new Map<number, Task>();
        flattenTree(dependencyTasks ?? []).forEach(({ task }) => map.set(task.id, task));
        taskMap.forEach((task, id) => map.set(id, task));
        iterationTasks.forEach((task, id) => map.set(id, task));
        return map;
    }, [dependencyTasks, taskMap, iterationTasks]);
    const flatTasks = useMemo(() => flat.map(({ task }) => task), [flat]);
    const agentFacts = useAgentRowFacts(flatTasks);

    const leaves = useMemo(() => flat.filter(({ task }) => isLeaf(task) && task.iteration_id !== null).map(({ task }) => task), [flat]);
    const selectableIds = useMemo(() => new Set(leaves.map(task => task.id)), [leaves]);
    const order = useMemo(() => leaves.map(task => task.id), [leaves]);
    const iterationOf = useCallback((id: number) => taskMap.get(id)?.iteration_id, [taskMap]);
    const selection = useTaskSelection({ selectableIds, order, iterationOf });
    const selectedTasks = useMemo(() => leaves.filter(task => selection.selectedIds.has(task.id)), [leaves, selection.selectedIds]);
    const scopeIterationId = selectedTasks[0]?.iteration_id ?? null;

    if (flat.length === 0) {
        return (
            <div className="rounded-lg border border-dashed border-border bg-surface-muted py-10 text-center text-content-tertiary">
                {t('surfaces.projectTaskTree.noLinkedTasks')}
            </div>
        );
    }

    return (
        <>
            <TaskEditorDrawer taskId={selectedTask} open={selectedTask !== null} onClose={() => setSelectedTask(null)} />
            {optionsError && <QueryErrorState error={optionsError} fallback={t('queryFeedback.optionLoadFailed')} onRetry={refetchOptions} />}
            {scopeIterationId !== null && (
                <TaskSelectionBar
                    iterationId={scopeIterationId}
                    selectedTasks={selectedTasks}
                    matchingCount={selection.matchingIds.length}
                    onSelectAll={selection.selectAll}
                    onClearSelection={selection.clear}
                />
            )}
            {flatSections.map(section => (
                <div key={section.key} className="mb-4 last:mb-0">
                    {section.heading && <h3 className="mb-2 text-sm font-semibold text-content-primary">{section.heading}</h3>}
                    <ul className="rounded-md border border-border bg-surface-card">
                        {section.rows.map(({ task, level }) => {
                            const canPick = isLeaf(task) && task.iteration_id !== null;
                            const assigneeOptions = optionsByIteration.get(task.iteration_id ?? -1);
                            const agentRow = agentRowValues(task, assigneeOptions, agentFacts);
                            return (
                                <li key={task.id}>
                                    <TaskRow
                                        id={task.id}
                                        title={task.title}
                                        status={task.status}
                                        statusLocked={task.is_composite || (task.children?.length ?? 0) > 0}
                                        priority={task.priority}
                                        chip={taskStateChip(task, dependencyMap)}
                                        assignee={task.assignee ?? null}
                                        assigneeOptions={assigneeOptions}
                                        dispatch={agentRow.dispatch}
                                        reviewer={agentRow.reviewer}
                                        onAssign={task.iteration_id === null ? undefined : assigneeId => rowEdits.assign(task, assigneeId)}
                                        effort={getEffectiveEffort(task)}
                                        level={level}
                                        overdue={task.is_overdue}
                                        meta={[task.iteration_id === null ? t('domain.backlog') : null, task.canceled_at ? t('domain.canceled') : null, task.milestone?.name].filter(Boolean).join(' · ')}
                                        onOpen={() => setSelectedTask(task.id)}
                                        onStatusChange={status => rowEdits.changeStatus(task, status)}
                                        menuItems={[{ label: t('taskList.openTask'), onSelect: () => setSelectedTask(task.id) }]}
                                        selected={selection.selectedIds.has(task.id)}
                                        onToggleSelect={canPick ? ({ shiftKey }) => selection.toggle(task.id, shiftKey) : undefined}
                                        selectDisabledReason={canPick && !selection.canAdd(task.id) ? t('taskList.selectOneIteration') : undefined}
                                    />
                                </li>
                            );
                        })}
                    </ul>
                </div>
            ))}
        </>
    );
};

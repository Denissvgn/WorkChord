import { useState } from 'react';
import { TaskEditorDrawer } from '../tasks/TaskEditorDrawer';
import i18n from '../../i18n/i18n';
import type { Task } from '../../types/task';
import { TaskRow } from '../tasks/TaskRow';
import { taskStateChip } from '../tasks/taskStateChip';
import { useTaskRowEdits } from '../tasks/useTaskRowEdits';

const t = i18n.t.bind(i18n);

interface ProjectTaskTreeProps {
    tasks: Task[];
}

const getEffectiveEffort = (task: Task): number | null => {
    if (task.children && task.children.length > 0) {
        const values = task.children.map(getEffectiveEffort);
        return values.some(value => value === null) ? null : values.reduce<number>((sum, value) => sum + (value ?? 0), 0);
    }
    return task.effort_days;
};

/** The tree as one flat, indented list, so each task is a divided row, not a card inside a card. */
const flattenTree = (tasks: Task[], level = 0): { task: Task; level: number }[] => tasks.flatMap(task => [
    { task, level },
    ...flattenTree(task.children ?? [], level + 1),
]);

const ProjectTaskRow = ({ task, level, taskMap, onOpen }: { task: Task; level: number; taskMap: Map<number, Task>; onOpen: (id: number) => void }) => {
    const rowEdits = useTaskRowEdits();
    return (
        <li>
            <TaskRow
                id={task.id}
                title={task.title}
                status={task.status}
                statusLocked={task.is_composite || (task.children?.length ?? 0) > 0}
                priority={task.priority}
                chip={taskStateChip(task, taskMap)}
                assignee={task.owner ?? task.assignee ?? null}
                effort={getEffectiveEffort(task)}
                level={level}
                overdue={task.is_overdue}
                meta={[task.iteration_id === null ? t('domain.backlog') : null, task.canceled_at ? t('domain.canceled') : null, task.milestone?.name].filter(Boolean).join(' · ')}
                onOpen={() => onOpen(task.id)}
                onStatusChange={status => rowEdits.changeStatus(task, status)}
                menuItems={[{ label: t('taskList.openTask'), onSelect: () => onOpen(task.id) }]}
            />
        </li>
    );
};

export const ProjectTaskTree = ({ tasks }: ProjectTaskTreeProps) => {
    const [selectedTask, setSelectedTask] = useState<number | null>(null);
    if (tasks.length === 0) {
        return (
            <div className="rounded-lg border border-dashed border-border bg-surface-muted py-10 text-center text-content-tertiary">
                {t('surfaces.projectTaskTree.noLinkedTasks')}
            </div>
        );
    }

    const flat = flattenTree(tasks);
    const taskMap = new Map(flat.map(({ task }) => [task.id, task]));

    return (
        <>
            <TaskEditorDrawer taskId={selectedTask} open={selectedTask !== null} onClose={() => setSelectedTask(null)} />
            <ul className="rounded-md border border-border bg-surface-card">
                {flat.map(({ task, level }) => (
                    <ProjectTaskRow key={task.id} task={task} level={level} taskMap={taskMap} onOpen={setSelectedTask} />
                ))}
            </ul>
        </>
    );
};

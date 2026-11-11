import { useState } from 'react';
import { TaskEditorDrawer } from '../tasks/TaskEditorDrawer';
import i18n from '../../i18n/i18n';
import {
    AlertTriangle,
    CheckCircle2,
    Circle,
    CornerDownRight,
    MessageSquare,
    User,
} from 'lucide-react';
import clsx from 'clsx';
import type { Task } from '../../types/task';
import { formatDate } from '../../utils/formatDate';
import { pillToneClassName, priorityChipClassName, STATUS_TONE, statusTextClassName } from '../ui/tone';

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

const ProjectTaskRow = ({ task, level, onOpen }: { task: Task; level: number; onOpen: (id: number) => void }) => (
    <li className="relative flex items-center gap-3 py-2 pr-3" style={{ paddingLeft: 12 + level * 22 }}>
        {level > 0 && (
            <CornerDownRight aria-hidden="true" className="h-4 w-4 shrink-0 text-content-tertiary" />
        )}
        <div className={statusTextClassName[task.status]}>
            {task.status === 'closed' ? <CheckCircle2 className="h-5 w-5" /> : <Circle className="h-5 w-5" />}
        </div>
        <div className="min-w-0 flex-1">
            <div className="flex flex-wrap items-center gap-2">
                <button type="button" className="truncate text-left font-medium text-content-primary hover:underline" onClick={() => onOpen(task.id)}>{task.title}</button>
                {task.iteration_id === null && <span className="text-sm text-content-secondary">{t("domain.backlog")}</span>}
                {task.canceled_at && <span className="text-sm text-content-secondary">{t("domain.canceled")}</span>}
                <span className={clsx('rounded-full border px-2 py-0.5 text-xs font-medium', pillToneClassName[STATUS_TONE[task.status]])}>
                    {t(`statuses.${task.status}`)}
                </span>
                <span className={clsx('rounded-full px-2 py-0.5 text-xs', priorityChipClassName(task.priority))}>
                    P{task.priority}
                </span>
                <span className="rounded-full bg-surface-subtle px-2 py-0.5 text-xs text-content-secondary">
                    {getEffectiveEffort(task) === null ? t("domain.unknownEstimate") : t("units.daysCompact", { count: getEffectiveEffort(task)! })}
                </span>
                {task.milestone && (
                    <span className="rounded-full border border-border bg-surface-subtle px-2 py-0.5 text-xs font-medium text-content-secondary">
                        {task.milestone.name}
                    </span>
                )}
                {(task.request_count ?? 0) > 0 && (
                    <span className="inline-flex items-center gap-1 rounded-full border border-border bg-surface-subtle px-2 py-0.5 text-xs font-medium text-content-secondary">
                        <MessageSquare aria-hidden="true" className="h-3 w-3" />
                        {task.request_count}
                    </span>
                )}
                {task.is_overdue && (
                    <span className="inline-flex items-center rounded-full bg-feedback-danger-muted px-2 py-0.5 text-xs text-feedback-danger-foreground">
                        <AlertTriangle aria-hidden="true" className="mr-1 h-3 w-3" />
                        {t('surfaces.projectTaskTree.overdue')}
                    </span>
                )}
            </div>
            <div className="mt-1 flex flex-wrap items-center gap-3 text-sm text-content-secondary">
                {task.assignee && (
                    <span className="inline-flex items-center gap-1">
                        <User aria-hidden="true" className="h-3.5 w-3.5" />
                        {task.owner?.name ?? task.assignee.name}
                    </span>
                )}
                {task.start_date && task.end_date && (
                    <span>{formatDate(task.start_date)} {t('surfaces.projectTaskTree.to')} {formatDate(task.end_date)}</span>
                )}
                {task.dependencies.length > 0 && (
                    <span>{t('surfaces.projectTaskTree.dependencies', { count: task.dependencies.length })}</span>
                )}
            </div>
        </div>
    </li>
);

export const ProjectTaskTree = ({ tasks }: ProjectTaskTreeProps) => {
    const [selectedTask, setSelectedTask] = useState<number | null>(null);
    if (tasks.length === 0) {
        return (
            <div className="rounded-lg border border-dashed border-border bg-surface-muted py-10 text-center text-content-tertiary">
                {t('surfaces.projectTaskTree.noLinkedTasks')}
            </div>
        );
    }

    return (
        <>
            <TaskEditorDrawer taskId={selectedTask} open={selectedTask !== null} onClose={() => setSelectedTask(null)} />
            <ul className="divide-y divide-border-subtle rounded-md border border-border bg-surface-card">
                {flattenTree(tasks).map(({ task, level }) => (
                    <ProjectTaskRow key={task.id} task={task} level={level} onOpen={setSelectedTask} />
                ))}
            </ul>
        </>
    );
};

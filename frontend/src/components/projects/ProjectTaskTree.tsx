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
import { pillToneClassName, STATUS_TONE } from '../ui/tone';

const t = i18n.t.bind(i18n);

interface ProjectTaskTreeProps {
    tasks: Task[];
}

const getEffectiveEffort = (task: Task): number => {
    if (task.children && task.children.length > 0) {
        return task.children.reduce((sum, child) => sum + getEffectiveEffort(child), 0);
    }
    return task.effort_days || 0;
};

const ProjectTaskRow = ({ task, level }: { task: Task; level: number }) => {
    const hasChildren = Boolean(task.children?.length);

    return (
        <div className="space-y-2">
            <div
                className={clsx(
                    'relative flex items-center gap-3 rounded-lg border bg-surface-card px-3 py-2',
                    task.is_overdue ? 'border-feedback-danger-border bg-feedback-danger-muted' : 'border-border'
                )}
                style={{ marginLeft: level * 22 }}
            >
                {level > 0 && (
                    <CornerDownRight className="absolute -left-5 top-1/2 h-4 w-4 -translate-y-1/2 text-content-tertiary" />
                )}
                <div className={clsx('text-content-tertiary', task.status === 'closed' && 'text-feedback-success')}>
                    {task.status === 'closed' ? <CheckCircle2 className="h-5 w-5" /> : <Circle className="h-5 w-5" />}
                </div>
                <div className="min-w-0 flex-1">
                    <div className="flex flex-wrap items-center gap-2">
                        <span className="truncate font-medium text-content-primary">{task.title}</span>
                        <span className={clsx('rounded-full border px-2 py-0.5 text-xs font-medium', pillToneClassName[STATUS_TONE[task.status]])}>
                            {t(`statuses.${task.status}`)}
                        </span>
                        <span className="rounded-full bg-surface-subtle px-2 py-0.5 text-xs text-content-secondary">
                            P{task.priority}
                        </span>
                        <span className="rounded-full bg-surface-subtle px-2 py-0.5 text-xs text-content-secondary">
                            {getEffectiveEffort(task)}d
                        </span>
                        {task.milestone && (
                            <span className="rounded-full border border-feedback-indigo-border bg-feedback-indigo-muted px-2 py-0.5 text-xs font-medium text-feedback-indigo-foreground">
                                {task.milestone.name}
                            </span>
                        )}
                        {(task.request_count ?? 0) > 0 && (
                            <span className="inline-flex items-center gap-1 rounded-full border border-action bg-action-muted px-2 py-0.5 text-xs font-medium text-action">
                                <MessageSquare className="h-3 w-3" />
                                {task.request_count}
                            </span>
                        )}
                        {task.is_overdue && (
                            <span className="inline-flex items-center rounded-full bg-feedback-danger-muted px-2 py-0.5 text-xs text-feedback-danger-foreground">
                                <AlertTriangle className="mr-1 h-3 w-3" />
                                {t('surfaces.projectTaskTree.overdue')}
                            </span>
                        )}
                    </div>
                    <div className="mt-1 flex flex-wrap items-center gap-3 text-xs text-content-secondary">
                        {task.assignee && (
                            <span className="inline-flex items-center gap-1">
                                <User className="h-3 w-3" />
                                {task.assignee.name}
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
            </div>

            {hasChildren && (
                <div className="space-y-2">
                    {task.children.map(child => (
                        <ProjectTaskRow key={child.id} task={child} level={level + 1} />
                    ))}
                </div>
            )}
        </div>
    );
};

export const ProjectTaskTree = ({ tasks }: ProjectTaskTreeProps) => {
    if (tasks.length === 0) {
        return (
            <div className="rounded-lg border border-dashed border-border bg-surface-muted py-10 text-center text-content-tertiary">
                {t('surfaces.projectTaskTree.noLinkedTasks')}
            </div>
        );
    }

    return (
        <div className="space-y-2">
            {tasks.map(task => (
                <ProjectTaskRow key={task.id} task={task} level={0} />
            ))}
        </div>
    );
};

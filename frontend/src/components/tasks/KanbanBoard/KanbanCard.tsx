import i18n from '../../../i18n/i18n';
import { useSortable } from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
import type { Task } from '../../../types/task';
import { Bot, Clock, User as UserIcon, AlertCircle } from 'lucide-react';
import clsx from 'clsx';

const t = i18n.t.bind(i18n);

interface KanbanCardProps {
    task: Task;
}

export const KanbanCard = ({ task }: KanbanCardProps) => {
    const {
        attributes,
        listeners,
        setNodeRef,
        transform,
        transition,
        isDragging,
    } = useSortable({
        id: task.id,
        data: {
            type: 'Task',
            task,
        },
    });

    const style = {
        transform: CSS.Translate.toString(transform),
        transition,
    };

    const getPriorityColor = (priority: number) => {
        if (priority <= 3) return 'bg-feedback-danger'; // High
        if (priority <= 6) return 'bg-feedback-warning'; // Medium
        return 'bg-feedback-info'; // Low
    };

    const priorityColor = getPriorityColor(task.priority);

    if (isDragging) {
        return (
            <div
                ref={setNodeRef}
                style={style}
                className="opacity-50 bg-surface-muted border-2 border-dashed border-border-strong rounded-lg h-[120px]"
            />
        );
    }

    return (
        <div
            ref={setNodeRef}
            style={style}
            {...attributes}
            {...listeners}
            aria-label={task.title}
            className="group relative bg-surface-card p-4 rounded-xl border border-border-subtle shadow-sm hover:shadow-md transition-all duration-200 cursor-grab active:cursor-grabbing select-none hover:border-border focus:outline-none focus-visible:ring-2 focus-visible:ring-focus focus-visible:ring-offset-2"
        >
            {/* Priority Strip */}
            <div className={clsx("absolute left-0 top-3 bottom-3 w-1 rounded-r-full", priorityColor)} />

            <div className="pl-3">
                {/* Header: ID and Badges */}
                <div className="flex justify-between items-start mb-2">
                    <span className="text-xs font-mono text-content-tertiary">#{task.id}</span>
                    {task.is_overdue && (
                        <div className="text-feedback-danger" title={t('surfaces.kanbanCard.overdue')}>
                            <AlertCircle className="w-4 h-4" />
                        </div>
                    )}
                    {task.claimed_by && (
                        <div className="text-action" title={t('surfaces.kanbanCard.claimedBy', { name: task.claimed_by.display_name })}>
                            <Bot className="w-4 h-4" />
                        </div>
                    )}
                </div>

                {/* Title */}
                <h4 className="text-sm font-medium text-content-primary leading-snug mb-3 line-clamp-2">
                    {task.title}
                </h4>

                {/* Footer: Meta Info */}
                <div className="flex items-center justify-between text-xs text-content-secondary">
                    <div className="flex items-center gap-2">
                        {task.assignee ? (
                            <div className="flex items-center gap-1.5 bg-surface-muted px-2 py-1 rounded-md">
                                <span className="w-4 h-4 rounded-full bg-feedback-indigo-muted text-feedback-indigo-foreground flex items-center justify-center text-[10px] font-bold">
                                    {task.assignee.name.charAt(0)}
                                </span>
                                <span className="max-w-[80px] truncate">{task.assignee.name}</span>
                            </div>
                        ) : (
                            <div className="flex items-center gap-1.5 px-2 py-1 rounded-md text-content-tertiary border border-border-subtle border-dashed">
                                <UserIcon className="w-3 h-3" />
                                <span>{t('surfaces.kanbanCard.unassigned')}</span>
                            </div>
                        )}
                    </div>

                    <div className="flex items-center gap-1 bg-surface-muted px-2 py-1 rounded-md">
                        <Clock className="w-3 h-3 text-content-tertiary" />
                        <span>{task.effort_days}d</span>
                    </div>
                </div>
            </div>
        </div>
    );
};

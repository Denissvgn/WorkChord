import { useSortable } from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
import { useTranslation } from 'react-i18next';
import type { Task } from '../../../types/task';
import { AlertCircle, Bot, GripVertical } from 'lucide-react';
import clsx from 'clsx';
import { formatClaimUntil } from './claimTime';
import { priorityChipClassName } from '../../ui/tone';
import { agentRowValues } from '../useAgentRowFacts';
import type { AgentRowFacts } from '../useAgentRowFacts';
import type { TaskRowAssigneeOption } from '../TaskRow';
import { taskStateChip } from '../taskStateChip';
import { getEffectiveEffort } from '../taskRowValues';
import { AgentDispatchLine, AssigneeKindIcon, EffortValue, TaskStateChipBadge } from '../taskRowParts';

/** What a card needs beyond its task, the same inputs a list row takes, shared by every card on the board. */
export interface BoardCardContext {
    taskMap: Map<number, Task>;
    assigneeOptions: TaskRowAssigneeOption[];
    agentFacts: AgentRowFacts;
}

interface KanbanCardProps {
    task: Task;
    onOpen?: (task: Task, trigger?: HTMLElement) => void;
    context?: BoardCardContext;
}

/** One task on the board: the same title, state chip, assignee and effort a list row shows. */
export const KanbanCard = ({ task, onOpen, context }: KanbanCardProps) => {
    const { t, i18n } = useTranslation();
    const claimUntil = task.claim_expires_at ? formatClaimUntil(task.claim_expires_at, i18n.language) : null;
    const chip = context ? taskStateChip(task, context.taskMap) : null;
    const { dispatch } = context ? agentRowValues(task, context.assigneeOptions, context.agentFacts) : { dispatch: null };
    const assigneeKind = context?.assigneeOptions.find(option => option.id === task.assignee?.id)?.kind;
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
            data-task-card={task.id}
            className="group relative bg-surface-card p-4 rounded-xl border border-border-subtle shadow-sm hover:shadow-md transition-all duration-200 cursor-grab active:cursor-grabbing select-none hover:border-border focus:outline-none focus-visible:ring-2 focus-visible:ring-focus focus-visible:ring-offset-2"
        >
            <div>
                {/* Header: the one task ID, its priority and the move handle */}
                <div className="flex items-start justify-between gap-2">
                    <span className="flex items-center gap-1.5 pt-1 text-xs tabular-nums text-content-secondary">#{task.id}
                        <span className={clsx('rounded px-1 font-medium', priorityChipClassName(task.priority))}>P{task.priority}</span></span>
                    <button type="button" {...attributes} {...listeners} aria-label={t('workStatus.moveTask', { title: task.title })} title={t('workStatus.moveTask', { title: task.title })}
                        className="-mr-2 -mt-2 flex h-11 w-11 shrink-0 cursor-grab items-center justify-center rounded-md text-content-secondary hover:bg-surface-hover focus-visible:outline focus-visible:outline-2 focus-visible:outline-focus">
                        <GripVertical className="h-4 w-4" aria-hidden="true" />
                    </button>
                </div>
                {(task.is_overdue || task.claimed_by) && (
                    <div className="mb-2 flex flex-wrap items-center gap-x-3 gap-y-1 text-xs">
                        {task.is_overdue && (
                            <span className="flex items-center gap-1 text-feedback-danger-foreground">
                                <AlertCircle className="h-4 w-4" aria-hidden="true" />
                                {t('surfaces.kanbanCard.overdue')}
                            </span>
                        )}
                        {task.claimed_by && (
                            <span className="flex items-center gap-1 text-content-secondary">
                                <Bot className="h-4 w-4 shrink-0" aria-hidden="true" />
                                {claimUntil
                                    ? t('surfaces.kanbanCard.claimHeldUntil', { name: task.claimed_by.display_name, time: claimUntil })
                                    : t('surfaces.kanbanCard.claimedBy', { name: task.claimed_by.display_name })}
                            </span>
                        )}
                    </div>
                )}

                {/* Title */}
                {'parent_context' in task && Array.isArray(task.parent_context) && task.parent_context.length > 0 &&
                    <p className="mb-1 truncate text-xs text-content-secondary">{task.parent_context.join(' / ')}</p>}
                <h4 className={clsx('text-sm font-medium leading-snug text-content-primary', chip ? 'mb-2' : 'mb-3')}>
                    <button type="button" className="text-left hover:underline focus-visible:outline focus-visible:outline-2 focus-visible:outline-focus"
                        aria-label={t('workStatus.openTask', { title: task.title })}
                        onClick={event => onOpen?.(task, event.currentTarget)}>{task.title}</button>
                </h4>
                {chip && <TaskStateChipBadge chip={chip} className="mb-3" />}

                {/* Footer: the assignee with its kind, the agent status under it, and the effort */}
                <div className="flex items-start justify-between gap-2 text-xs text-content-secondary">
                    <span data-assignee-cell="" className="flex min-w-0 flex-col">
                        <span className="flex min-w-0 items-center gap-1.5">
                            <AssigneeKindIcon kind={assigneeKind} className="h-3.5 w-3.5" />
                            <span className="min-w-0 truncate" title={task.assignee?.name ?? t('common.unassigned')}>
                                {task.assignee?.name ?? t('common.unassigned')}
                            </span>
                        </span>
                        {dispatch && <AgentDispatchLine dispatch={dispatch} className="block truncate pl-[1.125rem] text-wc-micro text-content-tertiary" />}
                    </span>
                    <EffortValue effort={getEffectiveEffort(task)} className="shrink-0 text-right" />
                </div>
            </div>
        </div>
    );
};

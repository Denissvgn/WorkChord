import { useState } from 'react';
import type { ReactNode } from 'react';
import clsx from 'clsx';
import { Bot, CheckCircle2, Circle, CornerDownRight, User } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { OverflowMenu } from '../ui/OverflowMenu';
import type { OverflowMenuItem } from '../ui/OverflowMenu';
import { statusTextClassName } from '../ui/tone';
import { canTransition, TASK_TRANSITIONS } from '../../features/taskTransitions';
import { isDone } from './taskStateChip';
import type { TaskStateChip } from './taskStateChip';
import type { TaskStatus } from '../../types/task';

const chipClassName: Record<TaskStateChip['kind'], string> = {
    blocked: 'bg-feedback-danger-muted text-feedback-danger-foreground',
    needsDefinition: 'bg-feedback-warning-muted text-feedback-warning-foreground',
    waits: 'bg-surface-subtle text-content-secondary',
    ready: 'bg-action-muted text-action',
    inReview: 'bg-surface-subtle text-content-secondary',
};

export interface TaskRowAssigneeOption { id: number; name: string; kind?: 'human' | 'agent' | 'hybrid' }

export interface TaskRowProps {
    id: number;
    title: string;
    /** Text shown as the title when it differs from the plain title, such as "#12 · Title". */
    titleText?: string;
    status: TaskStatus;
    /** Composite tasks take their status from their children, so it is not changed here. */
    statusLocked?: boolean;
    priority?: number | null;
    chip?: TaskStateChip | null;
    /** Secondary text after the title, such as the project and iteration. */
    meta?: ReactNode;
    /** The assignee column is left out when this is undefined. */
    assignee?: { id?: number; name: string } | null;
    assigneeOptions?: TaskRowAssigneeOption[];
    onAssign?: (assigneeId: number | null) => void;
    /** Days; `undefined` leaves the column out and `null` shows an unknown estimate. */
    effort?: number | null;
    level?: number;
    /** Hierarchy controls shown before the status, such as an expander or a drag handle. */
    lead?: ReactNode;
    onOpen: () => void;
    onStatusChange?: (status: TaskStatus) => void;
    menuItems: OverflowMenuItem[];
    selected?: boolean;
    /** Some rows are selected, so every checkbox stays visible. */
    selectionActive?: boolean;
    /** Leaves out the checkbox for rows that cannot be selected. */
    onToggleSelect?: (options: { shiftKey: boolean }) => void;
    overdue?: boolean;
    deferred?: boolean;
    className?: string;
}

/**
 * One 44 px task row for the list, My Work and the project task tree. At rest it holds the
 * status, the title and the assignee; the checkbox and the menu appear on hover and focus.
 */
export const TaskRow = ({
    id, title, titleText, status, statusLocked = false, priority, chip, meta, assignee, assigneeOptions, onAssign, effort,
    level = 0, lead, onOpen, onStatusChange, menuItems, selected = false, selectionActive = false, onToggleSelect,
    overdue = false, deferred = false, className,
}: TaskRowProps) => {
    const { t } = useTranslation();
    const [hovered, setHovered] = useState(false);
    const [focused, setFocused] = useState(false);
    const revealed = hovered || focused || selected || selectionActive;
    const statusName = t(`statuses.${status}`, { defaultValue: status });
    const transitions = statusLocked ? [] : TASK_TRANSITIONS[status] ?? [];
    const statusIcon = isDone(status) ? <CheckCircle2 aria-hidden="true" className="h-4 w-4" /> : <Circle aria-hidden="true" className="h-4 w-4" />;
    const assigneeKind = assigneeOptions?.find(option => option.id === assignee?.id)?.kind;
    const AssigneeIcon = assigneeKind === 'agent' ? Bot : User;
    const assigneeName = assignee?.name ?? t('common.unassigned');
    const options = assignee && assignee.id !== undefined && !assigneeOptions?.some(option => option.id === assignee.id)
        ? [{ id: assignee.id, name: assignee.name }, ...(assigneeOptions ?? [])]
        : assigneeOptions ?? [];

    return (
        <div
            data-task-row={id}
            className={clsx(
                'relative flex min-h-11 items-center gap-2 border-b border-border-subtle bg-surface-card pr-2 hover:bg-surface-hover',
                overdue && 'border-l-4 border-l-feedback-danger-border',
                deferred && 'bg-surface-muted opacity-75',
                selected && 'bg-action-muted',
                className,
            )}
            style={{ paddingLeft: 8 + level * 24 }}
            onMouseEnter={() => setHovered(true)}
            onMouseLeave={() => setHovered(false)}
            onFocus={() => setFocused(true)}
            onBlur={event => { if (!event.currentTarget.contains(event.relatedTarget as Node | null)) setFocused(false); }}
        >
            {/* The slot keeps its width, so the row does not shift when the checkbox appears. */}
            <span className="flex h-5 w-5 shrink-0 items-center justify-center">
                {revealed && onToggleSelect && (
                    <input
                        type="checkbox"
                        checked={selected}
                        onChange={() => undefined}
                        onClick={event => onToggleSelect({ shiftKey: event.shiftKey })}
                        aria-label={t('taskList.selectTask', { title })}
                        className="h-4 w-4 cursor-pointer rounded border-border-strong text-action focus:ring-focus"
                    />
                )}
            </span>

            {level > 0 && <CornerDownRight aria-hidden="true" className="h-4 w-4 shrink-0 text-content-tertiary" />}
            {lead}

            {transitions.length > 0 && onStatusChange ? (
                <OverflowMenu
                    alwaysMenu
                    align="start"
                    label={`${t('taskList.taskStatus', { status: statusName })}: ${title}`}
                    className="shrink-0"
                    triggerClassName={clsx('btn ghost icon sm', statusTextClassName[status])}
                    trigger={statusIcon}
                    items={transitions.filter(next => canTransition(status, next)).map(next => ({
                        label: t(`statuses.${next}`, { defaultValue: next }),
                        onSelect: () => onStatusChange(next),
                    }))}
                />
            ) : (
                <span className={clsx('flex h-8 w-8 shrink-0 items-center justify-center', statusTextClassName[status])}
                    title={t('taskList.taskStatus', { status: statusName })}>
                    {statusIcon}
                    <span className="sr-only">{t('taskList.taskStatus', { status: statusName })}</span>
                </span>
            )}

            {priority != null && (
                <span className="shrink-0 text-xs tabular-nums text-content-tertiary" title={t('taskList.priorityTitle', { priority })}>
                    P{priority}
                </span>
            )}

            <button
                data-page-chrome-control="button"
                type="button"
                onClick={onOpen}
                title={title}
                className={clsx(
                    'min-w-0 flex-1 truncate text-left font-medium hover:text-action hover:underline focus:outline-none focus-visible:ring-2 focus-visible:ring-focus',
                    status === 'closed' && 'text-content-secondary line-through',
                )}
            >
                {titleText ?? title}
            </button>

            {meta && <span className="hidden min-w-0 max-w-[16rem] shrink truncate text-xs text-content-secondary lg:block">{meta}</span>}

            {chip && (
                <span className={clsx('hidden shrink-0 whitespace-nowrap rounded-full px-2 py-0.5 text-xs sm:inline', chipClassName[chip.kind])}>
                    {chip.kind === 'waits' ? t('taskList.dependsOnCount', { count: chip.count }) : t(chipLabelKey[chip.kind])}
                </span>
            )}

            {assignee !== undefined && (
                <span className="hidden w-36 shrink-0 items-center gap-1 text-xs text-content-secondary md:flex">
                    <AssigneeIcon aria-hidden="true" className="h-3.5 w-3.5 shrink-0" />
                    {onAssign ? (
                        <select data-page-chrome-control="select"
                            aria-label={`${t('taskList.assignee')}: ${title}`}
                            value={assignee?.id ?? ''}
                            onChange={event => onAssign(event.target.value === '' ? null : Number(event.target.value))}
                            className="h-8 min-w-0 flex-1 cursor-pointer appearance-none truncate rounded border-0 bg-transparent px-1 text-xs text-content-secondary hover:bg-surface-subtle focus:outline-none focus-visible:ring-2 focus-visible:ring-focus"
                        >
                            <option value="">{t('common.unassigned')}</option>
                            {options.map(option => <option key={option.id} value={option.id}>{option.name}</option>)}
                        </select>
                    ) : (
                        <span className="min-w-0 truncate" title={assigneeName}>
                            <span className="sr-only">{t('taskList.assignee')}: </span>{assigneeName}
                        </span>
                    )}
                </span>
            )}

            {effort !== undefined && (effort === null ? (
                <span className="w-12 shrink-0 text-right text-xs text-content-tertiary" title={t('domain.unknownEstimate')}>
                    <span aria-hidden="true">—</span>
                    <span className="sr-only">{t('domain.unknownEstimate')}</span>
                </span>
            ) : (
                <span className="w-12 shrink-0 text-right text-xs tabular-nums text-content-secondary">{t('units.daysCompact', { count: effort })}</span>
            ))}

            {/* The slot keeps its width, so the row does not shift when the menu appears. */}
            <span className="flex h-8 w-8 shrink-0 items-center justify-center">
                {revealed && <OverflowMenu label={t('taskList.taskActions', { title })} items={menuItems} alwaysMenu triggerClassName="btn ghost icon sm" />}
            </span>
        </div>
    );
};

const chipLabelKey = {
    blocked: 'taskList.blocked',
    needsDefinition: 'taskList.needsDefinition',
    ready: 'taskList.readyToStart',
    inReview: 'taskList.inReview',
} as const;

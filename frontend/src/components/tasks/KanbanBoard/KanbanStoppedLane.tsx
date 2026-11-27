import { useId, useState } from 'react';
import clsx from 'clsx';
import { ChevronDown, ChevronRight } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import type { Task } from '../../../types/task';
import { Button } from '../../common/Button';
import { pillToneClassName, STATE_TONE } from '../../ui/tone';
import { stateOf } from '../../../utils/taskState';

interface KanbanStoppedLaneProps {
    /** `postponed` for paused work, `ended` for canceled and superseded work. */
    kind: 'postponed' | 'ended';
    tasks: Task[];
    /** Open when a filter asks for exactly this work. */
    defaultOpen?: boolean;
    onOpen: (task: Task, trigger?: HTMLElement) => void;
    onOpenTask: (taskId: number) => void;
}

/**
 * Work that is not in a board column: postponed work waiting to return, and canceled or superseded work that has
 * ended. The lane starts collapsed; its cards are read-only, since neither lane is a place work is moved to.
 */
export const KanbanStoppedLane = ({ kind, tasks, defaultOpen = false, onOpen, onOpenTask }: KanbanStoppedLaneProps) => {
    const { t } = useTranslation();
    const id = useId();
    const [open, setOpen] = useState(defaultOpen);
    // A filter chosen after the board loaded opens the lane it asks for; closing it by hand still works.
    const [askedOpen, setAskedOpen] = useState(defaultOpen);
    if (askedOpen !== defaultOpen) {
        setAskedOpen(defaultOpen);
        if (defaultOpen) setOpen(true);
    }
    if (tasks.length === 0) return null;
    const title = kind === 'postponed' ? t('statuses.postponed') : t('stoppedWork.endedLane');
    return (
        <section aria-labelledby={`${id}-title`} data-board-lane={kind} className="rounded-xl border border-border-subtle bg-surface-muted/50">
            <h3 id={`${id}-title`} className="m-0 text-sm font-semibold">
                <Button type="button" variant="plain" aria-expanded={open} aria-controls={`${id}-list`} onClick={() => setOpen(value => !value)}
                    className="flex min-h-9 w-full items-center gap-2 px-3 text-left focus:outline-hidden focus-visible:ring-2 focus-visible:ring-focus">
                    {open ? <ChevronDown aria-hidden="true" className="h-4 w-4" /> : <ChevronRight aria-hidden="true" className="h-4 w-4" />}
                    <span>{title}</span>
                    <span className="rounded-full bg-surface-subtle px-2 py-0.5 text-xs font-medium tabular-nums text-content-secondary">{tasks.length}</span>
                </Button>
            </h3>
            <div id={`${id}-list`} hidden={!open} className="px-3 pb-3">
                <p className="mb-2 text-xs text-content-secondary">{t(kind === 'postponed' ? 'stoppedWork.postponedLaneHelp' : 'stoppedWork.endedLaneHelp')}</p>
                <ul className="divide-y divide-border-subtle rounded-md border border-border bg-surface-card">
                    {tasks.map(task => {
                        const state = stateOf(task);
                        return (
                            <li key={task.id} className="flex flex-wrap items-center gap-2 px-3 py-2 text-sm">
                                <span data-task-state={state} className={clsx('shrink-0 rounded-full px-2 py-0.5 text-xs font-semibold', pillToneClassName[STATE_TONE[state]])}>
                                    {t(`statuses.${state}`)}
                                </span>
                                <Button type="button" variant="plain" onClick={event => onOpen(task, event.currentTarget)}
                                    className={clsx('min-w-0 flex-1 truncate text-left font-medium hover:text-action hover:underline focus:outline-hidden focus-visible:ring-2 focus-visible:ring-focus',
                                        kind === 'ended' && 'text-content-secondary line-through')}>
                                    {task.title}
                                </Button>
                                {task.assignee && <span className="text-xs text-content-secondary">{task.assignee.name}</span>}
                                {state === 'superseded' && task.successor_task_id && (
                                    <Button type="button" variant="ghost" size="sm" onClick={() => onOpenTask(task.successor_task_id as number)}>
                                        {t('stoppedWork.supersededBy', { id: task.successor_task_id })}
                                    </Button>
                                )}
                            </li>
                        );
                    })}
                </ul>
            </div>
        </section>
    );
};

import { useDroppable } from '@dnd-kit/core';
import { SortableContext, verticalListSortingStrategy } from '@dnd-kit/sortable';
import { useTranslation } from 'react-i18next';
import type { Task } from '../../../types/task';
import { KanbanCard } from './KanbanCard';
import clsx from 'clsx';
import { useMemo, useState } from 'react';
import type { PillTone } from '../../ui/tone';
import { toneDotClassName } from '../../ui/tone';
import { Button } from '../../common/Button';

/** Cards a column shows before "Show more": a long column stays scannable. */
const COLUMN_PAGE_SIZE = 20;

interface KanbanColumnProps {
    id: string;
    title: string;
    tasks: Task[];
    count: number;
    tone: PillTone;
    onOpen?: (task: Task, trigger?: HTMLElement) => void;
}

export const KanbanColumn = ({ id, title, tasks, count, tone, onOpen }: KanbanColumnProps) => {
    const { t } = useTranslation();
    const { setNodeRef, isOver } = useDroppable({
        id: id,
        data: {
            type: 'Column',
            containerId: id,
        },
    });
    const [shown, setShown] = useState(COLUMN_PAGE_SIZE);
    const visible = useMemo(() => tasks.slice(0, shown), [tasks, shown]);
    const taskIds = useMemo(() => visible.map(task => task.id), [visible]);
    const remaining = tasks.length - visible.length;

    // An empty column folds to a narrow strip that is still a drop target.
    if (tasks.length === 0) {
        return (
            <section
                ref={setNodeRef}
                aria-label={t('surfaces.kanbanColumn.emptyColumn', { title })}
                className={clsx(
                    'flex w-12 shrink-0 flex-col items-center gap-2 self-stretch rounded-xl border border-dashed border-border-subtle py-3 transition-colors',
                    isOver && 'border-action bg-action-muted/50',
                )}
            >
                <span className={clsx('h-2 w-2 rounded-full', toneDotClassName[tone])} aria-hidden="true" />
                <span className="text-xs tabular-nums text-content-secondary" aria-hidden="true">0</span>
                <h3 className="text-sm font-semibold text-content-secondary [writing-mode:vertical-rl]" aria-hidden="true">{title}</h3>
            </section>
        );
    }

    return (
        <section className="flex h-full min-w-[200px] flex-1 basis-0 flex-col" aria-label={title}>
            {/* Header */}
            <div className="mb-4 flex items-center justify-between gap-2 px-1">
                <div className="flex min-w-0 items-center gap-2">
                    <div className={clsx('h-2 w-2 shrink-0 rounded-full', toneDotClassName[tone])} aria-hidden="true" />
                    <h3 className="truncate text-sm font-semibold text-content-primary">{title}</h3>
                </div>
                <span className="rounded-full bg-surface-subtle px-2 py-0.5 text-xs font-medium tabular-nums text-content-secondary">
                    {count}
                </span>
            </div>

            {/* Droppable Area */}
            <div
                ref={setNodeRef}
                className={clsx(
                    'flex-1 space-y-3 overflow-y-auto rounded-xl border border-transparent bg-surface-muted/50 p-2 transition-colors',
                    isOver && 'border-action bg-action-muted/50',
                )}
            >
                <SortableContext items={taskIds} strategy={verticalListSortingStrategy}>
                    {visible.map((task) => (
                        <KanbanCard key={task.id} task={task} onOpen={onOpen} />
                    ))}
                </SortableContext>
                {remaining > 0 && (
                    <Button type="button" variant="ghost" size="sm" className="w-full"
                        onClick={() => setShown(value => value + COLUMN_PAGE_SIZE)}>
                        {t('surfaces.kanbanColumn.showMore', { count: Math.min(COLUMN_PAGE_SIZE, remaining), remaining })}
                    </Button>
                )}
            </div>
        </section>
    );
};

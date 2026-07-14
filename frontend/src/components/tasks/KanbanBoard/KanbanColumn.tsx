import i18n from '../../../i18n/i18n';
import { useDroppable } from '@dnd-kit/core';
import { SortableContext, verticalListSortingStrategy } from '@dnd-kit/sortable';
import type { Task } from '../../../types/task';
import { KanbanCard } from './KanbanCard';
import clsx from 'clsx';
import { useMemo } from 'react';
import type { PillTone } from '../../ui/tone';
import { toneDotClassName } from '../../ui/tone';

const t = i18n.t.bind(i18n);

interface KanbanColumnProps {
    id: string;
    title: string;
    tasks: Task[];
    count: number;
    tone: PillTone;
}

export const KanbanColumn = ({ id, title, tasks, count, tone }: KanbanColumnProps) => {
    const { setNodeRef, isOver } = useDroppable({
        id: id,
        data: {
            type: 'Column',
            containerId: id,
        },
    });

    const taskIds = useMemo(() => tasks.map(t => t.id), [tasks]);

    return (
        <div className="flex flex-col w-[320px] shrink-0 h-full">
            {/* Header */}
            <div className="flex items-center justify-between mb-4 px-1">
                <div className="flex items-center gap-2">
                    <div className={clsx("w-2 h-2 rounded-full", toneDotClassName[tone])} />
                    <h3 className="font-semibold text-content-primary text-sm">{title}</h3>
                </div>
                <span className="bg-surface-subtle text-content-secondary text-xs px-2 py-0.5 rounded-full font-medium">
                    {count}
                </span>
            </div>

            {/* Droppable Area */}
            <div
                ref={setNodeRef}
                className={clsx(
                    "flex-1 bg-surface-muted/50 rounded-xl p-2 border border-transparent transition-colors overflow-y-auto space-y-3",
                    isOver && "bg-action-muted/50 border-action"
                )}
            >
                <SortableContext items={taskIds} strategy={verticalListSortingStrategy}>
                    {tasks.map((task) => (
                        <KanbanCard key={task.id} task={task} />
                    ))}
                </SortableContext>

                {tasks.length === 0 && (
                    <div className="h-24 border-2 border-dashed border-border-subtle rounded-lg flex items-center justify-center text-content-tertiary text-xs">
                        {t('surfaces.kanbanColumn.dropItemsHere')}
                    </div>
                )}
            </div>
        </div>
    );
};

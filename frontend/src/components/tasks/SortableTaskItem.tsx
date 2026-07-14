import { useSortable } from '@dnd-kit/sortable';
import { CSS } from '@dnd-kit/utilities';
import { GripVertical } from 'lucide-react';
import type { ReactNode } from 'react';
import { useTranslation } from 'react-i18next';

interface SortableTaskItemProps {
    id: number;
    children: ReactNode;
    disabled?: boolean;
}

export const SortableTaskItem = ({ id, children, disabled }: SortableTaskItemProps) => {
    const { t } = useTranslation();
    const {
        attributes,
        listeners,
        setNodeRef,
        transform,
        transition,
        isDragging
    } = useSortable({ id, disabled });

    const style = {
        transform: CSS.Transform.toString(transform),
        transition,
        zIndex: isDragging ? 50 : 'auto',
        opacity: isDragging ? 0.8 : 1,
    };

    return (
        <div ref={setNodeRef} style={style} className="flex items-start gap-2">
            <button
                className="mt-3 p-1 text-content-tertiary cursor-grab active:cursor-grabbing hover:text-content-secondary touch-none"
                {...attributes}
                {...listeners}
                aria-label={t('taskList.reorderTask')}
            >
                <GripVertical className="w-4 h-4" aria-hidden="true" />
            </button>
            <div className="flex-1">{children}</div>
        </div>
    );
};

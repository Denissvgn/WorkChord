import { useState } from 'react';
import { TaskBulkOperationsPanel } from './TaskBulkOperationsPanel';
import type { BulkSelectedTask } from './TaskBulkOperationsPanel';
import { TaskMergeDialog } from './TaskMergeDialog';

interface TaskSelectionBarProps {
    /** The iteration every selected task belongs to; bulk changes apply to one iteration at a time. */
    iterationId: number;
    selectedTasks: BulkSelectedTask[];
    matchingCount: number;
    onSelectAll: () => void;
    onClearSelection: () => void;
    openAssign?: boolean;
}

/** The sticky bulk bar with its merge dialog, for any list of task rows that can be selected. */
export const TaskSelectionBar = ({ iterationId, selectedTasks, matchingCount, onSelectAll, onClearSelection, openAssign }: TaskSelectionBarProps) => {
    const [merging, setMerging] = useState(false);
    return (
        <>
            <TaskBulkOperationsPanel
                iterationId={iterationId}
                selectedTasks={selectedTasks}
                matchingCount={matchingCount}
                onSelectAll={onSelectAll}
                onClearSelection={onClearSelection}
                onMerge={() => setMerging(true)}
                openAssign={openAssign}
            />
            {merging && (
                <TaskMergeDialog
                    iterationId={iterationId}
                    taskIds={selectedTasks.map(task => task.id)}
                    onClose={() => setMerging(false)}
                    onMerged={onClearSelection}
                />
            )}
        </>
    );
};

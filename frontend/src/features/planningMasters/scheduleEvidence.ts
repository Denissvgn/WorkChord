import type { GanttTask } from '../../types/gantt';

export const scheduleLeaves = (tasks: GanttTask[], deferred = false): GanttTask[] => tasks.flatMap(task => {
    const excluded = deferred || Boolean(task.is_deferred);
    if (excluded) return [];
    return task.children?.length ? scheduleLeaves(task.children, excluded) : task.is_composite ? [] : [task];
});

import type { Task } from '../../types/task';

/** The effort a row shows: a parent adds up its children, and one unknown child makes the total unknown. */
export const getEffectiveEffort = (task: Task): number | null => {
    if (task.children && task.children.length > 0) {
        const values = task.children.map(getEffectiveEffort);
        return values.some(value => value === null) ? null : values.reduce<number>((sum, value) => sum + (value ?? 0), 0);
    }
    return task.effort_days;
};

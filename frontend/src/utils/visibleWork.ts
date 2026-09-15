import type { Task } from '../types/task';
import type { TaskFilters } from '../components/tasks/TaskFiltersBar';
import type { LabelGroup } from '../types/label';
import { filterTaskWithChildren } from './taskFilters';

export type VisibleLeaf = Task & { parent_context: string[] };

export const selectVisibleWork = (tasks: Task[], filters?: TaskFilters, groups: LabelGroup[] = []) => {
    const tree = tasks.map(task => filterTaskWithChildren(task, filters, groups)).filter((task): task is Task => task !== null);
    const leaves: VisibleLeaf[] = [];
    const visit = (task: Task, parents: string[], deferred: boolean, optional: boolean) => {
        const isDeferred = deferred || task.is_deferred;
        const isOptional = optional || task.is_optional;
        if (task.is_composite || task.children?.length) {
            task.children?.forEach(child => visit(child, [...parents, task.title], isDeferred, isOptional));
        } else leaves.push({ ...task, parent_context: parents, is_deferred: isDeferred, is_optional: isOptional });
    };
    tree.forEach(task => visit(task, [], false, false));
    return { tree, leaves };
};

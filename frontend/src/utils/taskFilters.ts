import type { Task } from '../types/task';
import type { LabelGroup } from '../types/label';
import type { TaskFilters } from '../components/tasks/TaskFiltersBar';

const taskHasAnyTag = (task: Task, selectedTags: Set<string>) => {
    if (selectedTags.size === 0) return true;
    return task.tags?.some(tag => selectedTags.has(tag)) ?? false;
};

const getSelectedGroupSlugs = (filters: TaskFilters, labelGroups: LabelGroup[]) => {
    const selectedGroupKeys = new Set(filters.labelGroupKeys);
    return new Set(
        labelGroups
            .filter(group => selectedGroupKeys.has(group.key))
            .flatMap(group => group.labels.map(label => label.slug))
    );
};

// Helper function to check if a task matches filters (including children recursively)
export const taskMatchesFilters = (
    task: Task,
    filters: TaskFilters | undefined,
    labelGroups: LabelGroup[] = [],
): boolean => {
    if (!filters) return true;

    // Check assignee
    if (filters.assigneeId !== null) {
        const isUnassignedFilter = filters.assigneeId === -1;
        const matchesSelf = isUnassignedFilter
            ? !task.assignee
            : task.assignee?.id === filters.assigneeId;

        const hasMatchingAssignee =
            matchesSelf ||
            (task.children?.some(c => taskMatchesFilters(c, {
                ...filters,
                priority: null,
                status: null,
                hasDependency: null,
                isOverdue: null,
                agentReady: null,
                startDateFrom: '',
                startDateTo: '',
                endDateFrom: '',
                endDateTo: ''
            }, labelGroups)));

        if (!hasMatchingAssignee) return false;
    }

    // Check project
    if (filters.projectId !== null) {
        const matchesSelf = task.project_id === filters.projectId;
        const childProjectFilters = {
            ...filters,
            assigneeId: null,
            priority: null,
            status: null,
            hasDependency: null,
            isOverdue: null,
            agentReady: null,
            startDateFrom: '',
            startDateTo: '',
            endDateFrom: '',
            endDateTo: ''
        };
        const hasMatchingProject =
            matchesSelf ||
            (task.children?.some(c => taskMatchesFilters(c, childProjectFilters, labelGroups)));

        if (!hasMatchingProject) return false;
    }

    // Check priority (only for leaf tasks or composite priority)
    if (filters.priority !== null && task.priority !== filters.priority) {
        return false;
    }

    // Check status
    if (filters.status !== null && task.status !== filters.status) {
        return false;
    }

    // Check dependencies
    if (filters.hasDependency !== null) {
        const hasDeps = task.dependencies && task.dependencies.length > 0;
        if (filters.hasDependency && !hasDeps) return false;
        if (!filters.hasDependency && hasDeps) return false;
    }

    // Check overdue state
    if (filters.isOverdue !== null && task.is_overdue !== filters.isOverdue) {
        return false;
    }

    if (filters.agentReady !== null && task.agent_readiness.is_ready !== filters.agentReady) {
        return false;
    }

    // Check start date range
    if (filters.startDateFrom && task.start_date) {
        if (task.start_date < filters.startDateFrom) return false;
    }
    if (filters.startDateTo && task.start_date) {
        if (task.start_date > filters.startDateTo) return false;
    }

    // Check end date range
    if (filters.endDateFrom && task.end_date) {
        if (task.end_date < filters.endDateFrom) return false;
    }
    if (filters.endDateTo && task.end_date) {
        if (task.end_date > filters.endDateTo) return false;
    }

    if (filters.labelSlugs.length > 0) {
        const selectedLabels = new Set(filters.labelSlugs);
        if (!taskHasAnyTag(task, selectedLabels)) return false;
    }

    if (filters.labelGroupKeys.length > 0) {
        const selectedGroupSlugs = getSelectedGroupSlugs(filters, labelGroups);
        if (selectedGroupSlugs.size === 0) return false;
        if (!taskHasAnyTag(task, selectedGroupSlugs)) return false;
    }

    return true;
};

// Recursively filter children
export const filterTaskWithChildren = (
    task: Task,
    filters: TaskFilters | undefined,
    labelGroups: LabelGroup[] = [],
): Task | null => {
    if (!filters) return task;

    // Filter children first
    let filteredChildren: Task[] = [];
    if (task.children && task.children.length > 0) {
        filteredChildren = task.children
            .map(child => filterTaskWithChildren(child, filters, labelGroups))
            .filter((c): c is Task => c !== null);
    }

    // Check if this task matches or has matching children
    const selfMatches = taskMatchesFilters(task, filters, labelGroups);
    const hasMatchingChildren = filteredChildren.length > 0;

    if (selfMatches || hasMatchingChildren) {
        return {
            ...task,
            children: filteredChildren
        };
    }

    return null;
};

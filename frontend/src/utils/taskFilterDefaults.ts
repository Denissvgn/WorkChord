import type { TaskFilters } from '../components/tasks/TaskFiltersBar';

export const defaultFilters: TaskFilters = {
    assigneeId: null,
    projectId: null,
    priority: null,
    status: null,
    hasDependency: null,
    isOverdue: null,
    agentReady: null,
    startDateFrom: '',
    startDateTo: '',
    endDateFrom: '',
    endDateTo: '',
    labelSlugs: [],
    labelGroupKeys: [],
};

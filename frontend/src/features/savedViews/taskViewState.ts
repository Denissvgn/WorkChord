import type { SavedView } from '../../types/savedView';
import type { TaskFilters } from '../../components/tasks/TaskFiltersBar';
import type { SortKey } from '../../components/tasks/TaskList';
import { defaultFilters } from '../../utils/taskFilterDefaults';
import { parsePlanningTaskIssue } from '../planningMasters/planningTaskIssues';
const SORT_KEYS: SortKey[] = ['priority', 'sort_order', 'status', 'title'];

const stringListFromValue = (value: unknown) => (
    Array.isArray(value) && value.every(item => typeof item === 'string') ? value : []
);

const nullableNumberFromValue = (value: unknown) => (
    typeof value === 'number' || value === null ? value : null
);

const nullableBooleanFromValue = (value: unknown) => (
    typeof value === 'boolean' || value === null ? value : null
);

const stringFromValue = (value: unknown) => (
    typeof value === 'string' ? value : ''
);

const nullableStringFromValue = (value: unknown) => (
    typeof value === 'string' || value === null ? value : null
);

export const filtersFromSavedView = (view: SavedView): TaskFilters => {
    const raw = view.filters_json;
    return {
        ...defaultFilters,
        planningIssue: parsePlanningTaskIssue(raw.planningIssue),
        assigneeId: nullableNumberFromValue(raw.assigneeId),
        projectId: nullableNumberFromValue(raw.projectId),
        priority: nullableNumberFromValue(raw.priority),
        status: nullableStringFromValue(raw.status),
        hasDependency: nullableBooleanFromValue(raw.hasDependency),
        isOverdue: nullableBooleanFromValue(raw.isOverdue),
        isIterationOverflow: nullableBooleanFromValue(raw.isIterationOverflow),
        agentReady: nullableBooleanFromValue(raw.agentReady),
        startDateFrom: stringFromValue(raw.startDateFrom),
        startDateTo: stringFromValue(raw.startDateTo),
        endDateFrom: stringFromValue(raw.endDateFrom),
        endDateTo: stringFromValue(raw.endDateTo),
        labelSlugs: stringListFromValue(raw.labelSlugs),
        labelGroupKeys: stringListFromValue(raw.labelGroupKeys),
    };
};

export const sortKeyFromSavedView = (view: SavedView): SortKey | null => {
    const sortKey = view.sort_json.sortKey;
    return typeof sortKey === 'string' && SORT_KEYS.includes(sortKey as SortKey)
        ? sortKey as SortKey
        : null;
};

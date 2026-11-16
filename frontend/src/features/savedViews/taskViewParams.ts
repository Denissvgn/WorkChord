import type { TaskFilters } from '../../components/tasks/TaskFiltersBar';
import type { SortKey } from '../../components/tasks/TaskList';
import { defaultFilters } from '../../utils/taskFilterDefaults';
import { PLANNING_TASK_ISSUE_PARAM, parsePlanningTaskIssue } from '../planningMasters/planningTaskIssues';

/**
 * The Tasks view lives in the URL: filters, sort and grouping are query parameters, so a
 * copied link, a reload and Back show the same list. Defaults are left out of the URL.
 */
export const TASK_FILTER_PARAMS = {
    planningIssue: PLANNING_TASK_ISSUE_PARAM,
    assigneeId: 'assignee',
    projectId: 'projectId',
    priority: 'priority',
    status: 'status',
    hasDependency: 'waits',
    isOverdue: 'overdue',
    isIterationOverflow: 'overflow',
    isBlocked: 'blocked',
    agentReady: 'agentReady',
    startDateFrom: 'startFrom',
    startDateTo: 'startTo',
    endDateFrom: 'endFrom',
    endDateTo: 'endTo',
    labelSlugs: 'label',
    labelGroupKeys: 'labelGroup',
} as const satisfies Record<keyof TaskFilters, string>;

export const TASK_SORT_PARAM = 'sort';
export const TASK_GROUP_PARAM = 'group';

const TASK_STATUSES = ['planned', 'active', 'resolved', 'closed'];
const DATE_PATTERN = /^\d{4}-\d{2}-\d{2}$/;
const UNASSIGNED_VALUE = 'none';
const SORT_PARAM_VALUES: Record<SortKey, string | null> = {
    priority: null,
    sort_order: 'manual',
    status: 'status',
    title: 'title',
};

const positiveInteger = (value: string | null): number | null => {
    if (value === null || !/^[1-9]\d*$/.test(value)) return null;
    const parsed = Number(value);
    return Number.isSafeInteger(parsed) ? parsed : null;
};

const yesNo = (value: string | null): boolean | null => (
    value === 'yes' ? true : value === 'no' ? false : null
);

const yesNoParam = (value: boolean | null | undefined) => (
    value === true ? 'yes' : value === false ? 'no' : null
);

const dateParam = (value: string | null) => (value && DATE_PATTERN.test(value) ? value : '');

const uniqueValues = (values: string[]) => [...new Set(values.filter(Boolean))];

export const filtersFromSearchParams = (params: URLSearchParams): TaskFilters => {
    const assignee = params.get(TASK_FILTER_PARAMS.assigneeId);
    const priority = positiveInteger(params.get(TASK_FILTER_PARAMS.priority));
    const status = params.get(TASK_FILTER_PARAMS.status);
    return {
        ...defaultFilters,
        planningIssue: parsePlanningTaskIssue(params.get(TASK_FILTER_PARAMS.planningIssue)),
        assigneeId: assignee === UNASSIGNED_VALUE ? -1 : positiveInteger(assignee),
        projectId: positiveInteger(params.get(TASK_FILTER_PARAMS.projectId)),
        priority: priority !== null && priority <= 10 ? priority : null,
        status: status && TASK_STATUSES.includes(status) ? status : null,
        hasDependency: yesNo(params.get(TASK_FILTER_PARAMS.hasDependency)),
        isOverdue: yesNo(params.get(TASK_FILTER_PARAMS.isOverdue)),
        isIterationOverflow: yesNo(params.get(TASK_FILTER_PARAMS.isIterationOverflow)),
        isBlocked: yesNo(params.get(TASK_FILTER_PARAMS.isBlocked)),
        agentReady: yesNo(params.get(TASK_FILTER_PARAMS.agentReady)),
        startDateFrom: dateParam(params.get(TASK_FILTER_PARAMS.startDateFrom)),
        startDateTo: dateParam(params.get(TASK_FILTER_PARAMS.startDateTo)),
        endDateFrom: dateParam(params.get(TASK_FILTER_PARAMS.endDateFrom)),
        endDateTo: dateParam(params.get(TASK_FILTER_PARAMS.endDateTo)),
        labelSlugs: uniqueValues(params.getAll(TASK_FILTER_PARAMS.labelSlugs)),
        labelGroupKeys: uniqueValues(params.getAll(TASK_FILTER_PARAMS.labelGroupKeys)),
    };
};

/** Writes every filter into `params`, removing the ones that are off. */
export const writeFiltersToSearchParams = (params: URLSearchParams, filters: TaskFilters) => {
    const single: [keyof TaskFilters, string | null][] = [
        ['planningIssue', filters.planningIssue],
        ['assigneeId', filters.assigneeId === -1 ? UNASSIGNED_VALUE : filters.assigneeId === null ? null : String(filters.assigneeId)],
        ['projectId', filters.projectId === null ? null : String(filters.projectId)],
        ['priority', filters.priority === null ? null : String(filters.priority)],
        ['status', filters.status],
        ['hasDependency', yesNoParam(filters.hasDependency)],
        ['isOverdue', yesNoParam(filters.isOverdue)],
        ['isIterationOverflow', yesNoParam(filters.isIterationOverflow)],
        ['isBlocked', yesNoParam(filters.isBlocked)],
        ['agentReady', yesNoParam(filters.agentReady)],
        ['startDateFrom', filters.startDateFrom || null],
        ['startDateTo', filters.startDateTo || null],
        ['endDateFrom', filters.endDateFrom || null],
        ['endDateTo', filters.endDateTo || null],
    ];
    single.forEach(([key, value]) => {
        const param = TASK_FILTER_PARAMS[key];
        if (value === null) params.delete(param);
        else params.set(param, value);
    });
    params.delete(TASK_FILTER_PARAMS.labelSlugs);
    uniqueValues(filters.labelSlugs).forEach(slug => params.append(TASK_FILTER_PARAMS.labelSlugs, slug));
    params.delete(TASK_FILTER_PARAMS.labelGroupKeys);
    uniqueValues(filters.labelGroupKeys).forEach(key => params.append(TASK_FILTER_PARAMS.labelGroupKeys, key));
    return params;
};

/** True when the URL names any filter or a sort, so it carries a view of its own. */
export const searchParamsNameView = (params: URLSearchParams) => (
    Object.values(TASK_FILTER_PARAMS).some(param => params.has(param)) || params.has(TASK_SORT_PARAM)
);

export const sortKeyFromSearchParams = (params: URLSearchParams): SortKey => {
    const value = params.get(TASK_SORT_PARAM);
    const match = (Object.entries(SORT_PARAM_VALUES) as [SortKey, string | null][])
        .find(([, param]) => param !== null && param === value);
    return match?.[0] ?? 'priority';
};

export const writeSortKeyToSearchParams = (params: URLSearchParams, sortKey: SortKey) => {
    const value = SORT_PARAM_VALUES[sortKey];
    if (value === null) params.delete(TASK_SORT_PARAM);
    else params.set(TASK_SORT_PARAM, value);
    return params;
};

export const groupByStatusFromSearchParams = (params: URLSearchParams) => params.get(TASK_GROUP_PARAM) !== 'none';

/** Number of active conditions, one per chip. */
export const activeFilterCount = (filters: TaskFilters) => (
    Number(filters.planningIssue !== null)
    + Number(filters.assigneeId !== null)
    + Number(filters.projectId !== null)
    + Number(filters.priority !== null)
    + Number(filters.status !== null)
    + Number(filters.hasDependency !== null)
    + Number(filters.isOverdue !== null)
    + Number(filters.isIterationOverflow != null)
    + Number(filters.isBlocked != null)
    + Number(filters.agentReady !== null)
    + Number(Boolean(filters.startDateFrom))
    + Number(Boolean(filters.startDateTo))
    + Number(Boolean(filters.endDateFrom))
    + Number(Boolean(filters.endDateTo))
    + filters.labelSlugs.length
    + filters.labelGroupKeys.length
);

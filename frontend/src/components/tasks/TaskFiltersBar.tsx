import { useMemo } from 'react';
import { useQuery } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { teamService } from '../../services/teamService';
import { projectService } from '../../services/projectService';
import { labelService } from '../../services/labelService';
import { defaultFilters } from '../../utils/taskFilterDefaults';
import { labelDisplay, labelGroupDisplay } from '../../i18n/seedDisplay';
import { QueryErrorState } from '../feedback/QueryState';
import { formatDate } from '../../utils/formatDate';
import { FilterBar, type FilterBarFilter } from '../ui';
import type { PlanningTaskIssue } from '../../features/planningMasters/planningTaskIssues';

export interface TaskFilters {
    planningIssue: PlanningTaskIssue | null;
    assigneeId: number | null;
    projectId: number | null;
    priority: number | null;
    status: string | null;
    hasDependency: boolean | null;
    isOverdue: boolean | null;
    isIterationOverflow?: boolean | null;
    isBlocked?: boolean | null;
    agentReady: boolean | null;
    startDateFrom: string;
    startDateTo: string;
    endDateFrom: string;
    endDateTo: string;
    labelSlugs: string[];
    labelGroupKeys: string[];
}

interface TaskFiltersBarProps {
    iterationId: number;
    filters: TaskFilters;
    onFiltersChange: (filters: TaskFilters) => void;
}

const YES = 'yes';
const NO = 'no';
const LABEL_CHIP = 'label:';
const LABEL_GROUP_CHIP = 'labelGroup:';
const DATE_FILTERS = ['startDateFrom', 'startDateTo', 'endDateFrom', 'endDateTo'] as const;
/** Assignee and status stay in the row, so the compact toolbar keeps one line down to a 1024px viewport. */
const QUICK_FILTERS = 2;

const yesNoValue = (value: boolean | null | undefined) => (value === true ? YES : value === false ? NO : '');
const yesNoFilter = (value: string) => (value === '' ? null : value === YES);
const numberFilter = (value: string) => (value === '' ? null : Number(value));

/**
 * The task filters in the shared FilterBar: the two most used conditions in the row, the rest under
 * More filters, and one removable chip for every active condition, including each label.
 */
export const TaskFiltersBar = ({ iterationId, filters, onFiltersChange }: TaskFiltersBarProps) => {
    const { t } = useTranslation();

    const teamQuery = useQuery({
        queryKey: ['team', iterationId],
        queryFn: () => teamService.getByIteration(iterationId),
    });

    const projectsQuery = useQuery({
        queryKey: ['projects'],
        queryFn: projectService.getAll,
    });

    const labelsQuery = useQuery({
        queryKey: ['label-groups'],
        queryFn: () => labelService.getGroups(),
    });
    const teamMembers = teamQuery.data;
    const projects = projectsQuery.data;
    const labelGroups = useMemo(() => labelsQuery.data ?? [], [labelsQuery.data]);
    const optionQueries = [teamQuery, projectsQuery, labelsQuery];
    const optionError = optionQueries.find(query => query.isError)?.error;

    const labels = useMemo(() => labelGroups.flatMap(group => group.labels.map(label => ({
        slug: label.slug,
        name: `${labelDisplay(label).name} · ${labelGroupDisplay(group).name}`,
    }))), [labelGroups]);

    const yesNoOptions = (yes: string, no: string) => [{ value: YES, label: yes }, { value: NO, label: no }];
    const dateLabels: Record<typeof DATE_FILTERS[number], string> = {
        startDateFrom: t('taskFilters.startFrom'),
        startDateTo: t('taskFilters.startTo'),
        endDateFrom: t('taskFilters.endFrom'),
        endDateTo: t('taskFilters.endTo'),
    };

    const assigneeOptions = [
        { value: '-1', label: t('taskFilters.unassigned') },
        ...(teamMembers ?? []).map(member => ({ value: String(member.id), label: member.name })),
    ];
    // A person or project the options do not list yet still names the condition.
    if (filters.assigneeId !== null && !assigneeOptions.some(option => option.value === String(filters.assigneeId))) {
        assigneeOptions.push({ value: String(filters.assigneeId), label: `#${filters.assigneeId}` });
    }
    const projectOptions = (projects ?? []).map(project => ({ value: String(project.id), label: project.name }));
    if (filters.projectId !== null && !projectOptions.some(option => option.value === String(filters.projectId))) {
        projectOptions.push({ value: String(filters.projectId), label: `#${filters.projectId}` });
    }

    const barFilters: FilterBarFilter[] = [
        {
            id: 'assigneeId',
            label: t('taskFilters.assignee'),
            value: filters.assigneeId === null ? '' : String(filters.assigneeId),
            options: assigneeOptions,
        },
        {
            id: 'status',
            label: t('taskFilters.status'),
            value: filters.status ?? '',
            options: [
                { value: 'planned', label: t('taskFilters.statusPlanned') },
                { value: 'active', label: t('taskFilters.statusActive') },
                { value: 'resolved', label: t('taskFilters.statusResolved') },
                { value: 'closed', label: t('taskFilters.statusClosed') },
            ],
        },
        {
            id: 'isBlocked',
            label: t('workStatus.blocked'),
            value: yesNoValue(filters.isBlocked),
            options: yesNoOptions(t('taskFilters.yes'), t('taskFilters.no')),
        },
        {
            id: 'planningIssue',
            label: t('taskFilters.planningReadiness'),
            value: filters.planningIssue ?? '',
            options: [
                { value: 'any', label: t('taskFilters.planningIssueAny') },
                { value: 'unassigned', label: t('taskFilters.planningIssueUnassigned') },
                { value: 'missing-effort', label: t('taskFilters.planningIssueMissingEffort') },
                { value: 'unscheduled', label: t('planSchedule.withoutDates') },
                { value: 'at-risk', label: t('plan.page.atRisk') },
            ],
        },
        {
            id: 'isOverdue',
            label: t('taskFilters.overdue'),
            value: yesNoValue(filters.isOverdue),
            options: yesNoOptions(t('taskFilters.yes'), t('taskFilters.no')),
        },
        {
            id: 'projectId',
            label: t('taskFilters.project'),
            value: filters.projectId === null ? '' : String(filters.projectId),
            options: projectOptions,
        },
        {
            id: 'priority',
            label: t('taskFilters.priority'),
            value: filters.priority === null ? '' : String(filters.priority),
            options: Array.from({ length: 10 }, (_, index) => ({ value: String(index + 1), label: String(index + 1) })),
        },
        {
            id: 'hasDependency',
            label: t('taskFilters.dependencies'),
            value: yesNoValue(filters.hasDependency),
            options: yesNoOptions(t('taskFilters.yes'), t('taskFilters.no')),
        },
        {
            id: 'agentReady',
            label: t('taskFilters.agentReadiness'),
            value: yesNoValue(filters.agentReady),
            options: yesNoOptions(t('taskFilters.ready'), t('taskFilters.notReady')),
        },
        {
            id: 'isIterationOverflow',
            label: t('workStatus.iterationOverflow'),
            value: yesNoValue(filters.isIterationOverflow),
            options: yesNoOptions(t('taskFilters.yes'), t('taskFilters.no')),
        },
        ...DATE_FILTERS.map(key => ({
            id: key,
            label: dateLabels[key],
            type: 'date' as const,
            value: filters[key],
            options: filters[key] ? [{ value: filters[key], label: formatDate(filters[key]) }] : [],
        })),
        // A label group or label is added from its list; each chosen one is a chip of its own.
        {
            id: 'labelGroupKeys',
            label: t('taskFilters.labelGroups'),
            value: '',
            options: labelGroups
                .filter(group => !filters.labelGroupKeys.includes(group.key))
                .map(group => ({ value: group.key, label: labelGroupDisplay(group).name })),
        },
        {
            id: 'labelSlugs',
            label: t('taskFilters.labels'),
            value: '',
            options: labels.filter(label => !filters.labelSlugs.includes(label.slug)).map(label => ({ value: label.slug, label: label.name })),
        },
        ...filters.labelGroupKeys.map(key => {
            const group = labelGroups.find(candidate => candidate.key === key);
            return {
                id: `${LABEL_GROUP_CHIP}${key}`,
                label: t('taskFilters.labelGroups'),
                value: key,
                options: [{ value: key, label: group ? labelGroupDisplay(group).name : key }],
                chipOnly: true,
            };
        }),
        ...filters.labelSlugs.map(slug => ({
            id: `${LABEL_CHIP}${slug}`,
            label: t('taskFilters.labels'),
            value: slug,
            options: [{ value: slug, label: labels.find(label => label.slug === slug)?.name ?? slug }],
            chipOnly: true,
        })),
    ];

    const changeFilter = (id: string, value: string) => {
        if (id.startsWith(LABEL_CHIP)) {
            const slug = id.slice(LABEL_CHIP.length);
            onFiltersChange({ ...filters, labelSlugs: filters.labelSlugs.filter(candidate => candidate !== slug) });
            return;
        }
        if (id.startsWith(LABEL_GROUP_CHIP)) {
            const key = id.slice(LABEL_GROUP_CHIP.length);
            onFiltersChange({ ...filters, labelGroupKeys: filters.labelGroupKeys.filter(candidate => candidate !== key) });
            return;
        }
        switch (id) {
            case 'labelSlugs':
                if (value && !filters.labelSlugs.includes(value)) onFiltersChange({ ...filters, labelSlugs: [...filters.labelSlugs, value] });
                return;
            case 'labelGroupKeys':
                if (value && !filters.labelGroupKeys.includes(value)) onFiltersChange({ ...filters, labelGroupKeys: [...filters.labelGroupKeys, value] });
                return;
            case 'assigneeId':
            case 'projectId':
            case 'priority':
                onFiltersChange({ ...filters, [id]: numberFilter(value) });
                return;
            case 'status':
                onFiltersChange({ ...filters, status: value || null });
                return;
            case 'planningIssue':
                onFiltersChange({ ...filters, planningIssue: (value as PlanningTaskIssue) || null });
                return;
            case 'isOverdue':
            case 'isBlocked':
            case 'hasDependency':
            case 'agentReady':
            case 'isIterationOverflow':
                onFiltersChange({ ...filters, [id]: yesNoFilter(value) });
                return;
            default:
                if ((DATE_FILTERS as readonly string[]).includes(id)) onFiltersChange({ ...filters, [id]: value });
        }
    };

    return (
        <>
            <FilterBar filters={barFilters} quickLimit={QUICK_FILTERS} onChange={changeFilter} onClear={() => onFiltersChange(defaultFilters)} />
            {optionError && (
                <QueryErrorState
                    className="mt-2"
                    error={optionError}
                    fallback={t('queryFeedback.optionLoadFailed')}
                    onRetry={() => optionQueries.forEach(query => void query.refetch())}
                />
            )}
        </>
    );
};

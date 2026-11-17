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
    milestoneId: number | null;
    needsAttention: boolean | null;
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
    agentFilter?: { value: string; options: string[]; onChange: (value: string) => void };
    hideProject?: boolean;
    onClear?: () => void;
}

const YES = 'yes';
const NO = 'no';
const LABEL_CHIP = 'label:';
const LABEL_GROUP_CHIP = 'labelGroup:';
const DATE_FILTERS = ['startDateFrom', 'startDateTo', 'endDateFrom', 'endDateTo'] as const;
/** Assignee, Status, Label, Milestone and Needs attention are the quick filters; everything else is under More filters. */
const QUICK_FILTERS = 5;

const yesNoValue = (value: boolean | null | undefined) => (value === true ? YES : value === false ? NO : '');
const yesNoFilter = (value: string) => (value === '' ? null : value === YES);
const numberFilter = (value: string) => (value === '' ? null : Number(value));

/**
 * The task filters in the shared FilterBar: five quick filters in the row, every other condition under
 * More filters, and one removable chip for every active condition, including each label.
 */
export const TaskFiltersBar = ({ iterationId, filters, onFiltersChange, agentFilter, hideProject, onClear }: TaskFiltersBarProps) => {
    const { t } = useTranslation();

    const teamQuery = useQuery({
        queryKey: ['team', iterationId],
        queryFn: () => teamService.getByIteration(iterationId),
        enabled: iterationId > 0,
    });

    const projectsQuery = useQuery({
        queryKey: ['projects'],
        queryFn: projectService.getAll,
    });

    const labelsQuery = useQuery({
        queryKey: ['label-groups'],
        queryFn: () => labelService.getGroups(),
    });
    // feedback-policy: query loading,error,retry,empty - the list is empty while loading; a failure shows with retry below.
    const milestonesQuery = useQuery({
        queryKey: ['projectMilestones', 'portfolio', 'filter'],
        queryFn: () => projectService.getRoadmapMilestones(null),
    });
    const teamMembers = teamQuery.data;
    const projects = projectsQuery.data;
    const labelGroups = useMemo(() => labelsQuery.data ?? [], [labelsQuery.data]);
    const optionQueries = [teamQuery, projectsQuery, labelsQuery, milestonesQuery];
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

    const milestoneOptions = (milestonesQuery.data?.items ?? [])
        .filter(milestone => filters.projectId === null || milestone.project_id === filters.projectId)
        .map(milestone => ({ value: String(milestone.id), label: milestone.name }));
    if (filters.milestoneId !== null && !milestoneOptions.some(option => option.value === String(filters.milestoneId))) {
        milestoneOptions.push({ value: String(filters.milestoneId), label: `#${filters.milestoneId}` });
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
            id: 'labelSlugs',
            label: t('taskFilters.label'),
            value: '',
            options: labels.filter(label => !filters.labelSlugs.includes(label.slug)).map(label => ({ value: label.slug, label: label.name })),
        },
        {
            id: 'milestoneId',
            label: t('taskFilters.milestone'),
            value: filters.milestoneId === null ? '' : String(filters.milestoneId),
            options: milestoneOptions,
        },
        {
            id: 'needsAttention',
            label: t('taskFilters.needsAttention'),
            value: yesNoValue(filters.needsAttention),
            options: yesNoOptions(t('taskFilters.yes'), t('taskFilters.no')),
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
            label: t('taskFilters.label'),
            value: slug,
            options: [{ value: slug, label: labels.find(label => label.slug === slug)?.name ?? slug }],
            chipOnly: true,
        })),
    ];

    const visibleFilters = hideProject ? barFilters.map(filter => filter.id === 'projectId' ? { ...filter, chipOnly: true } : filter) : barFilters;
    // Agent follows the five quick filters, so it sits under More filters and never pushes one of them out of the row.
    if (agentFilter) visibleFilters.push({ id: 'agent', label: t('taskFilters.agent'), value: agentFilter.value, options: [...new Set([...agentFilter.options, ...(agentFilter.value ? [agentFilter.value] : [])])].map(name => ({ value: name, label: name })) });

    const changeFilter = (id: string, value: string) => {
        if (id === 'agent') { agentFilter?.onChange(value); return; }
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
            case 'milestoneId':
            case 'priority':
                onFiltersChange({ ...filters, [id]: numberFilter(value) });
                return;
            case 'status':
                onFiltersChange({ ...filters, status: value || null });
                return;
            case 'planningIssue':
                onFiltersChange({ ...filters, planningIssue: (value as PlanningTaskIssue) || null });
                return;
            case 'needsAttention':
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
            <FilterBar filters={visibleFilters} quickLimit={QUICK_FILTERS} onChange={changeFilter} onClear={onClear ?? (() => onFiltersChange(defaultFilters))} />
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

import { useMemo, useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { ChevronDown, ChevronRight, X, FileText, XCircle } from 'lucide-react';
import { Button } from '../common/Button';
import { teamService } from '../../services/teamService';
import { projectService } from '../../services/projectService';
import { labelService } from '../../services/labelService';
import { TaskTextEditorModal } from './TaskTextEditorModal';
import { defaultFilters } from '../../utils/taskFilterDefaults';
import { labelDisplay, labelGroupDisplay } from '../../i18n/seedDisplay';
import { QueryErrorState, QueryLoadingState } from '../feedback/QueryState';
import type { PlanningTaskIssue } from '../../features/planningMasters/planningTaskIssues';

export interface TaskFilters {
    planningIssue: PlanningTaskIssue | null;
    assigneeId: number | null;
    projectId: number | null;
    priority: number | null;
    status: string | null;
    hasDependency: boolean | null;
    isOverdue: boolean | null;
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

// FilterBadge component for showing/removing active filters
const FilterBadge = ({
    label,
    value,
    onRemove,
}: {
    label: string;
    value: string;
    onRemove: () => void;
}) => {
    const { t } = useTranslation();
    return (
        <span className="inline-flex items-center gap-1 px-2 py-0.5 rounded-full bg-action-muted text-action text-xs font-medium border border-action">
            <span className="text-content-secondary">{label}:</span>
            <span>{value}</span>
            <button
                onClick={onRemove}
                className="ml-1 hover:text-action hover:bg-status-active-muted rounded-full p-0.5"
                aria-label={t('taskFilters.removeFilter', { label })}
            >
                <XCircle className="w-3 h-3" />
            </button>
        </span>
    );
};

export const TaskFiltersBar = ({ iterationId, filters, onFiltersChange }: TaskFiltersBarProps) => {
    const { t } = useTranslation();
    const [isAdvancedOpen, setIsAdvancedOpen] = useState(false);
    const [isTextEditorOpen, setIsTextEditorOpen] = useState(false);

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
    const optionsLoading = optionQueries.some(query => query.isLoading);

    const labels = useMemo(() => {
        return labelGroups.flatMap(group =>
            group.labels.map(label => ({
                ...label,
                name: labelDisplay(label).name,
                groupKey: group.key,
                groupName: labelGroupDisplay(group).name,
            }))
        );
    }, [labelGroups]);

    const selectedGroups = labelGroups.filter(group => filters.labelGroupKeys.includes(group.key));
    const selectedLabels = labels.filter(label => filters.labelSlugs.includes(label.slug));

    // Quick filter helpers
    const assigneeName = useMemo(() => {
        if (filters.assigneeId === null) return null;
        if (filters.assigneeId === -1) return t('taskFilters.unassigned');
        return teamMembers?.find(m => m.id === filters.assigneeId)?.name || null;
    }, [filters.assigneeId, teamMembers, t]);

    const statusDisplay: Record<string, string> = {
        planned: t('taskFilters.statusPlanned'),
        active: t('taskFilters.statusActive'),
        resolved: t('taskFilters.statusResolved'),
        closed: t('taskFilters.statusClosed'),
    };
    const planningIssueDisplay: Record<PlanningTaskIssue, string> = {
        any: t('taskFilters.planningIssueAny'),
        unassigned: t('taskFilters.planningIssueUnassigned'),
        'missing-effort': t('taskFilters.planningIssueMissingEffort'),
    };

    const hasActiveFilters =
        filters.planningIssue !== null ||
        filters.assigneeId !== null ||
        filters.projectId !== null ||
        filters.priority !== null ||
        filters.status !== null ||
        filters.hasDependency !== null ||
        filters.isOverdue !== null ||
        filters.agentReady !== null ||
        filters.startDateFrom ||
        filters.startDateTo ||
        filters.endDateFrom ||
        filters.endDateTo ||
        filters.labelSlugs.length > 0 ||
        filters.labelGroupKeys.length > 0;

    // Check if only quick filters are active (no advanced filters)
    const hasOnlyQuickFilters =
        (
            filters.planningIssue !== null
            || filters.assigneeId !== null
            || filters.status !== null
            || filters.isOverdue !== null
        ) &&
        !filters.projectId &&
        !filters.priority &&
        filters.hasDependency === null &&
        filters.agentReady === null &&
        !filters.startDateFrom &&
        !filters.startDateTo &&
        !filters.endDateFrom &&
        !filters.endDateTo &&
        filters.labelSlugs.length === 0 &&
        filters.labelGroupKeys.length === 0;

    const resetFilters = () => {
        onFiltersChange(defaultFilters);
    };

    // Badge removal handlers
    const removePlanningIssueFilter = () => onFiltersChange({
        ...filters,
        planningIssue: null,
    });
    const removeAssigneeFilter = () => onFiltersChange({ ...filters, assigneeId: null });
    const removeStatusFilter = () => onFiltersChange({ ...filters, status: null });
    const removeOverdueFilter = () => onFiltersChange({ ...filters, isOverdue: null });
    const removeProjectFilter = () => onFiltersChange({ ...filters, projectId: null });
    const removePriorityFilter = () => onFiltersChange({ ...filters, priority: null });
    const removeDependencyFilter = () => onFiltersChange({ ...filters, hasDependency: null });
    const removeAgentReadyFilter = () => onFiltersChange({ ...filters, agentReady: null });

    const addLabelGroup = (key: string) => {
        if (!key || filters.labelGroupKeys.includes(key)) return;
        onFiltersChange({
            ...filters,
            labelGroupKeys: [...filters.labelGroupKeys, key],
        });
    };

    const removeLabelGroup = (key: string) => {
        onFiltersChange({
            ...filters,
            labelGroupKeys: filters.labelGroupKeys.filter(groupKey => groupKey !== key),
        });
    };

    const addLabel = (slug: string) => {
        if (!slug || filters.labelSlugs.includes(slug)) return;
        onFiltersChange({
            ...filters,
            labelSlugs: [...filters.labelSlugs, slug],
        });
    };

    const removeLabel = (slug: string) => {
        onFiltersChange({
            ...filters,
            labelSlugs: filters.labelSlugs.filter(labelSlug => labelSlug !== slug),
        });
    };

    // Build active badges list
    const activeBadges: { label: string; value: string; onRemove: () => void }[] = [];

    if (filters.planningIssue) {
        activeBadges.push({
            label: t('taskFilters.planningReadiness'),
            value: planningIssueDisplay[filters.planningIssue],
            onRemove: removePlanningIssueFilter,
        });
    }
    if (assigneeName) {
        activeBadges.push({ label: t('taskFilters.assignee'), value: assigneeName, onRemove: removeAssigneeFilter });
    }
    if (filters.status) {
        activeBadges.push({ label: t('taskFilters.status'), value: statusDisplay[filters.status] || filters.status, onRemove: removeStatusFilter });
    }
    if (filters.isOverdue !== null) {
        activeBadges.push({ label: t('taskFilters.overdue'), value: filters.isOverdue ? t('taskFilters.yes') : t('taskFilters.no'), onRemove: removeOverdueFilter });
    }
    if (filters.projectId) {
        const projectName = projects?.find(p => p.id === filters.projectId)?.name || `#${filters.projectId}`;
        activeBadges.push({ label: t('taskFilters.project'), value: projectName, onRemove: removeProjectFilter });
    }
    if (filters.priority) {
        activeBadges.push({ label: t('taskFilters.priority'), value: String(filters.priority), onRemove: removePriorityFilter });
    }
    if (filters.hasDependency !== null) {
        activeBadges.push({ label: t('taskFilters.dependencies'), value: filters.hasDependency ? t('taskFilters.yes') : t('taskFilters.no'), onRemove: removeDependencyFilter });
    }
    if (filters.agentReady !== null) {
        activeBadges.push({ label: t('taskFilters.agentReadiness'), value: filters.agentReady ? t('taskFilters.ready') : t('taskFilters.notReady'), onRemove: removeAgentReadyFilter });
    }

    return (
        <div className="space-y-3 p-4">
            {optionsLoading && <QueryLoadingState className="mb-3 min-h-16 py-3" />}
            {optionError && (
                <QueryErrorState
                    className="mb-3"
                    error={optionError}
                    fallback={t('queryFeedback.optionLoadFailed')}
                    onRetry={() => optionQueries.forEach(query => void query.refetch())}
                />
            )}
            {/* Quick Filters - always visible */}
            <div className="flex items-center gap-3 flex-wrap">
                <span className="text-xs font-semibold text-content-secondary uppercase tracking-wide">{t('taskFilters.quickFilters')}</span>

                <select
                    value={filters.planningIssue ?? ''}
                    onChange={event => onFiltersChange({
                        ...filters,
                        planningIssue: (
                            event.target.value as PlanningTaskIssue
                        ) || null,
                    })}
                    aria-label={t('taskFilters.planningReadiness')}
                    className="px-2 py-1.5 text-sm border border-border-strong rounded-md bg-surface-card focus:outline-none focus:ring-1 focus:ring-focus"
                >
                    <option value="">{t('taskFilters.planningReadiness')}</option>
                    <option value="any">{t('taskFilters.planningIssueAny')}</option>
                    <option value="unassigned">{t('taskFilters.planningIssueUnassigned')}</option>
                    <option value="missing-effort">{t('taskFilters.planningIssueMissingEffort')}</option>
                </select>

                {/* Assignee */}
                <select
                    value={filters.assigneeId ?? ''}
                    onChange={e => onFiltersChange({
                        ...filters,
                        assigneeId: e.target.value ? parseInt(e.target.value) : null
                    })}
                    aria-label={t('taskFilters.assignee')}
                    className="px-2 py-1.5 text-sm border border-border-strong rounded-md bg-surface-card focus:outline-none focus:ring-1 focus:ring-focus"
                >
                    <option value="">{t('taskFilters.assignee')}</option>
                    <option value="-1">{t('taskFilters.unassigned')}</option>
                    {teamMembers?.map(m => (
                        <option key={m.id} value={m.id}>{m.name}</option>
                    ))}
                </select>

                {/* Status */}
                <select
                    value={filters.status ?? ''}
                    onChange={e => onFiltersChange({
                        ...filters,
                        status: e.target.value || null
                    })}
                    aria-label={t('taskFilters.status')}
                    className="px-2 py-1.5 text-sm border border-border-strong rounded-md bg-surface-card focus:outline-none focus:ring-1 focus:ring-focus"
                >
                    <option value="">{t('taskFilters.status')}</option>
                    <option value="planned">{t('taskFilters.statusPlanned')}</option>
                    <option value="active">{t('taskFilters.statusActive')}</option>
                    <option value="resolved">{t('taskFilters.statusResolved')}</option>
                    <option value="closed">{t('taskFilters.statusClosed')}</option>
                </select>

                {/* Overdue */}
                <select
                    value={filters.isOverdue === null ? '' : filters.isOverdue ? 'yes' : 'no'}
                    onChange={e => onFiltersChange({
                        ...filters,
                        isOverdue: e.target.value === '' ? null : e.target.value === 'yes'
                    })}
                    aria-label={t('taskFilters.overdue')}
                    className="px-2 py-1.5 text-sm border border-border-strong rounded-md bg-surface-card focus:outline-none focus:ring-1 focus:ring-focus"
                >
                    <option value="">{t('taskFilters.overdue')}</option>
                    <option value="yes">{t('taskFilters.overdue')}</option>
                    <option value="no">{t('taskFilters.notOverdue')}</option>
                </select>

                {/* Active filter badges */}
                {activeBadges.length > 0 && (
                    <div className="flex gap-1 items-center ml-2 flex-wrap">
                        {activeBadges.slice(0, 4).map((badge, idx) => (
                            <FilterBadge key={idx} {...badge} />
                        ))}
                        {activeBadges.length > 4 && (
                            <span className="text-xs text-content-secondary ml-1">
                                +{activeBadges.length - 4} more
                            </span>
                        )}
                    </div>
                )}
            </div>

            {/* Advanced toggle + actions */}
            <div className="flex items-center justify-between mt-3 pt-3 border-t border-border-subtle">
                <div className="flex items-center gap-2">
                    <Button
                        variant="ghost"
                        size="sm"
                        onClick={() => setIsAdvancedOpen(!isAdvancedOpen)}
                        className="text-content-secondary"
                    >
                        {isAdvancedOpen ? (
                            <ChevronDown className="w-4 h-4 mr-1" />
                        ) : (
                            <ChevronRight className="w-4 h-4 mr-1" />
                        )}
                        {t('taskFilters.advancedFilters')}
                        {!hasOnlyQuickFilters && hasActiveFilters && (
                            <span className="ml-1 bg-surface-hover text-content-primary text-xs rounded-full px-1.5">
                                {activeBadges.filter(b => !['assignee', 'status', 'overdue'].includes(b.label.toLowerCase())).length}
                            </span>
                        )}
                    </Button>

                    {hasActiveFilters && (
                        <Button variant="ghost" size="sm" onClick={resetFilters} className="text-content-secondary">
                            <X className="w-4 h-4 mr-1" />
                            {t('taskFilters.reset')}
                        </Button>
                    )}
                </div>

                <Button
                    variant="outline"
                    size="sm"
                    onClick={() => setIsTextEditorOpen(true)}
                    className="text-content-secondary border-dashed hover:border-action hover:text-action"
                >
                    <FileText className="w-4 h-4 mr-1" />
                    {t('taskFilters.textMode')}
                </Button>
            </div>

            {/* Advanced filters - collapsible */}
            {isAdvancedOpen && (
                <div className="grid grid-cols-2 md:grid-cols-4 lg:grid-cols-6 gap-3 mt-3 pt-3 border-t border-border-subtle">
                    {/* Project filter */}
                    <div>
                        <label className="block text-xs font-medium text-content-secondary mb-1">{t('taskFilters.project')}</label>
                        <select
                            value={filters.projectId ?? ''}
                            onChange={e => onFiltersChange({
                                ...filters,
                                projectId: e.target.value ? parseInt(e.target.value) : null
                            })}
                            className="w-full px-2 py-1 text-sm border border-border-strong rounded"
                        >
                            <option value="">{t('taskFilters.all')}</option>
                            {projects?.map(project => (
                                <option key={project.id} value={project.id}>{project.name}</option>
                            ))}
                        </select>
                    </div>

                    {/* Priority filter */}
                    <div>
                        <label className="block text-xs font-medium text-content-secondary mb-1">{t('taskFilters.priority')}</label>
                        <select
                            value={filters.priority ?? ''}
                            onChange={e => onFiltersChange({
                                ...filters,
                                priority: e.target.value ? parseInt(e.target.value) : null
                            })}
                            className="w-full px-2 py-1 text-sm border border-border-strong rounded"
                        >
                            <option value="">{t('taskFilters.all')}</option>
                            {[1, 2, 3, 4, 5, 6, 7, 8, 9, 10].map(p => (
                                <option key={p} value={p}>{p}</option>
                            ))}
                        </select>
                    </div>

                    {/* Has dependency filter */}
                    <div>
                        <label className="block text-xs font-medium text-content-secondary mb-1">{t('taskFilters.dependencies')}</label>
                        <select
                            value={filters.hasDependency === null ? '' : filters.hasDependency ? 'yes' : 'no'}
                            onChange={e => onFiltersChange({
                                ...filters,
                                hasDependency: e.target.value === '' ? null : e.target.value === 'yes'
                            })}
                            className="w-full px-2 py-1 text-sm border border-border-strong rounded"
                        >
                            <option value="">{t('taskFilters.all')}</option>
                            <option value="yes">{t('taskFilters.yes')}</option>
                            <option value="no">{t('taskFilters.no')}</option>
                        </select>
                    </div>

                    {/* Agent readiness filter */}
                    <div>
                        <label className="block text-xs font-medium text-content-secondary mb-1">{t('taskFilters.agentReadiness')}</label>
                        <select
                            value={filters.agentReady === null ? '' : filters.agentReady ? 'ready' : 'not-ready'}
                            onChange={e => onFiltersChange({
                                ...filters,
                                agentReady: e.target.value === '' ? null : e.target.value === 'ready'
                            })}
                            className="w-full px-2 py-1 text-sm border border-border-strong rounded"
                        >
                            <option value="">{t('taskFilters.any')}</option>
                            <option value="ready">{t('taskFilters.ready')}</option>
                            <option value="not-ready">{t('taskFilters.notReady')}</option>
                        </select>
                    </div>

                    {/* Label group filter */}
                    <div>
                        <label className="block text-xs font-medium text-content-secondary mb-1">{t('taskFilters.labelGroups')}</label>
                        <select
                            value=""
                            onChange={e => addLabelGroup(e.target.value)}
                            className="w-full px-2 py-1 text-sm border border-border-strong rounded"
                        >
                            <option value="">{t('taskFilters.add')}</option>
                            {labelGroups
                                .filter(group => !filters.labelGroupKeys.includes(group.key))
                                .map(group => (
                                    <option key={group.key} value={group.key}>{group.name}</option>
                                ))}
                        </select>
                        {selectedGroups.length > 0 && (
                            <div className="mt-1 flex flex-wrap gap-1">
                                {selectedGroups.map(group => (
                                    <button
                                        key={group.key}
                                        type="button"
                                        onClick={() => removeLabelGroup(group.key)}
                                        className="text-wc-micro px-1.5 py-0.5 rounded border border-border bg-surface-muted text-content-secondary hover:bg-surface-subtle"
                                    >
                                        {group.name} ×
                                    </button>
                                ))}
                            </div>
                        )}
                    </div>

                    {/* Label filter */}
                    <div>
                        <label className="block text-xs font-medium text-content-secondary mb-1">{t('taskFilters.labels')}</label>
                        <select
                            value=""
                            onChange={e => addLabel(e.target.value)}
                            className="w-full px-2 py-1 text-sm border border-border-strong rounded"
                        >
                            <option value="">{t('taskFilters.add')}</option>
                            {labels
                                .filter(label => !filters.labelSlugs.includes(label.slug))
                                .map(label => (
                                    <option key={label.slug} value={label.slug}>
                                        {label.name} · {label.groupName}
                                    </option>
                                ))}
                        </select>
                        {selectedLabels.length > 0 && (
                            <div className="mt-1 flex flex-wrap gap-1">
                                {selectedLabels.map(label => (
                                    <button
                                        key={label.slug}
                                        type="button"
                                        onClick={() => removeLabel(label.slug)}
                                        className="text-wc-micro px-1.5 py-0.5 rounded border border-border bg-surface-muted text-content-secondary hover:bg-surface-subtle"
                                    >
                                        {label.slug} ×
                                    </button>
                                ))}
                            </div>
                        )}
                    </div>

                    {/* Start date from */}
                    <div>
                        <label className="block text-xs font-medium text-content-secondary mb-1">{t('taskFilters.startFrom')}</label>
                        <input
                            type="date"
                            value={filters.startDateFrom}
                            onChange={e => onFiltersChange({ ...filters, startDateFrom: e.target.value })}
                            className="w-full px-2 py-1 text-sm border border-border-strong rounded"
                        />
                    </div>

                    {/* Start date to */}
                    <div>
                        <label className="block text-xs font-medium text-content-secondary mb-1">{t('taskFilters.startTo')}</label>
                        <input
                            type="date"
                            value={filters.startDateTo}
                            onChange={e => onFiltersChange({ ...filters, startDateTo: e.target.value })}
                            className="w-full px-2 py-1 text-sm border border-border-strong rounded"
                        />
                    </div>

                    {/* End date from */}
                    <div>
                        <label className="block text-xs font-medium text-content-secondary mb-1">{t('taskFilters.endFrom')}</label>
                        <input
                            type="date"
                            value={filters.endDateFrom}
                            onChange={e => onFiltersChange({ ...filters, endDateFrom: e.target.value })}
                            className="w-full px-2 py-1 text-sm border border-border-strong rounded"
                        />
                    </div>

                    {/* End date to */}
                    <div>
                        <label className="block text-xs font-medium text-content-secondary mb-1">{t('taskFilters.endTo')}</label>
                        <input
                            type="date"
                            value={filters.endDateTo}
                            onChange={e => onFiltersChange({ ...filters, endDateTo: e.target.value })}
                            className="w-full px-2 py-1 text-sm border border-border-strong rounded"
                        />
                    </div>
                </div>
            )}

            {isTextEditorOpen && (
                <TaskTextEditorModal
                    iterationId={iterationId}
                    onClose={() => setIsTextEditorOpen(false)}
                />
            )}
        </div>
    );
};

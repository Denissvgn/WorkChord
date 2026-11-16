import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { Link, useNavigate, useSearchParams } from 'react-router-dom';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import {
    addMonths,
    endOfMonth,
    endOfQuarter,
    endOfYear,
    format,
    startOfMonth,
    startOfQuarter,
    startOfYear,
} from 'date-fns';
import {
    AlertTriangle,
    FolderOpen,
    List,
    LoaderCircle,
    Map as MapIcon,
    Plus,
    Search,
    Target,
} from 'lucide-react';
import clsx from 'clsx';
import { Button } from '../components/common/Button';
import { Input } from '../components/common/Input';
import { useConfirmDialog } from '../components/common/useConfirmDialog';
import { QueryErrorState, QueryLoadingState, QueryStaleState } from '../components/feedback/QueryState';
import { InitiativeForm } from '../components/projects/InitiativeForm';
import { InitiativeGroupHeader } from '../components/projects/InitiativeGroupHeader';
import { ProjectForm } from '../components/projects/ProjectForm';
import { RoadmapView } from '../components/projects/RoadmapView';
import {
    HEALTH_NEEDS_ATTENTION,
    NONE_VALUE,
    PORTFOLIO_PARAMS,
    PROJECT_HEALTHS,
    PROJECT_STATUSES,
    groupByInitiative,
    hasActiveFilters,
    matchesPortfolioFilters,
    ownerKeyForProject,
    readPortfolioFilters,
    readPortfolioView,
    readSavedViewId,
    readTimelineWindow,
    type PortfolioFilters,
    type PortfolioView,
} from '../components/projects/projectPortfolio';
import { projectHealthBadgeClassName, projectStatusBadgeClassName } from '../components/projects/projectStatusStyles';
import {
    FilterBar,
    InlineEmptyState,
    OverflowMenu,
    PageHeader,
    PageLayout,
    PageToolbar,
    SegmentedControl,
    SlideOverDrawer,
    TableFrame,
    ViewSwitch,
    type FilterBarFilter,
} from '../components/ui';
import { projectService } from '../services/projectService';
import { savedViewService } from '../services/savedViewService';
import { getApiErrorMessage } from '../utils/apiError';
import { formatPortfolioOwnerLabel } from '../utils/teamMemberLabels';
import { formatDate } from '../utils/formatDate';
import type { SavedView } from '../types/savedView';
import type {
    Initiative,
    Project,
    ProjectHealth,
    ProjectPortfolioSummary,
    ProjectStatus,
} from '../types/project';
import { feedbackMessage } from '../features/mutationFeedback';
import type { MutationFeedbackMeta } from '../features/mutationFeedback';
import { formatEffortDays } from '../utils/workNumbers';

const projectStatusLabelKeys: Record<ProjectStatus, string> = {
    proposed: 'surfaces.projectsPage.proposed',
    planned: 'surfaces.projectsPage.planned',
    active: 'surfaces.projectsPage.active',
    paused: 'surfaces.projectsPage.paused',
    completed: 'surfaces.projectsPage.completed',
    canceled: 'surfaces.projectsPage.canceled',
};

const projectHealthLabelKeys: Record<ProjectHealth, string> = {
    unknown: 'surfaces.projectsPage.unknown',
    on_track: 'surfaces.projectsPage.onTrack',
    at_risk: 'surfaces.projectsPage.atRisk',
    off_track: 'surfaces.projectsPage.offTrack',
};

/** The filters a saved projects view carries: search, status and health. */
const projectFiltersFromSavedView = (view: SavedView) => {
    const raw = view.filters_json;
    return {
        search: typeof raw.search === 'string' ? raw.search : '',
        status: typeof raw.status === 'string' && raw.status in projectStatusLabelKeys ? raw.status : '',
        health: typeof raw.health === 'string' && raw.health in projectHealthLabelKeys ? raw.health : '',
    };
};

type SortKey = 'name' | 'status' | 'owner' | 'target' | 'tasks' | 'effort' | 'signals';
const SORT_COLUMNS: Array<{ key: SortKey; labelKey: string; center?: boolean }> = [
    { key: 'name', labelKey: 'surfaces.projectsPage.project' },
    { key: 'status', labelKey: 'surfaces.projectsPage.status' },
    { key: 'owner', labelKey: 'surfaces.projectsPage.owner' },
    { key: 'target', labelKey: 'surfaces.projectsPage.target' },
    { key: 'tasks', labelKey: 'surfaces.projectsPage.tasks', center: true },
    { key: 'effort', labelKey: 'surfaces.projectsPage.effort', center: true },
    { key: 'signals', labelKey: 'surfaces.projectsPage.signals' },
];
const RISK_ORDER: Record<string, number> = { unknown: 1, on_track: 0, at_risk: 2, off_track: 3 };

/** The URL key of each FilterBar filter. */
const FILTER_PARAM: Record<string, string> = {
    status: PORTFOLIO_PARAMS.status,
    health: PORTFOLIO_PARAMS.health,
    owner: PORTFOLIO_PARAMS.owner,
    initiative: PORTFOLIO_PARAMS.initiative,
};
const ALL_FILTER_PARAMS = [
    PORTFOLIO_PARAMS.search,
    PORTFOLIO_PARAMS.status,
    PORTFOLIO_PARAMS.health,
    PORTFOLIO_PARAMS.owner,
    PORTFOLIO_PARAMS.initiative,
    PORTFOLIO_PARAMS.attention,
];

type WindowPreset = 'quarter' | 'sixMonths' | 'year' | 'fit';
const WINDOW_PRESETS: Array<{ value: Exclude<WindowPreset, 'fit'>; labelKey: string; range: () => [Date, Date] }> = [
    { value: 'quarter', labelKey: 'surfaces.roadmapPage.presetQuarter', range: () => { const start = startOfQuarter(new Date()); return [start, endOfQuarter(start)]; } },
    { value: 'sixMonths', labelKey: 'surfaces.roadmapPage.presetSixMonths', range: () => { const start = startOfMonth(new Date()); return [start, endOfMonth(addMonths(start, 5))]; } },
    { value: 'year', labelKey: 'surfaces.roadmapPage.presetYear', range: () => { const start = startOfYear(new Date()); return [start, endOfYear(start)]; } },
];
const inputDate = (date: Date) => format(date, 'yyyy-MM-dd');

const ProjectSummaryCells = ({
    isLoading,
    summary,
    health,
}: {
    isLoading: boolean;
    summary?: ProjectPortfolioSummary;
    health: ProjectHealth;
}) => {
    const { t, i18n } = useTranslation();

    if (isLoading) {
        return (
            <>
                {[0, 1, 2].map(cell => (
                    <td key={cell} aria-hidden="true" className="px-4 py-3">
                        <span className="mx-auto block h-4 w-16 animate-pulse rounded bg-surface-subtle" />
                    </td>
                ))}
            </>
        );
    }

    if (!summary) {
        return (
            <>
                <td className="px-3 py-3 text-center text-content-tertiary">—</td>
                <td className="px-3 py-3 text-center text-content-tertiary">—</td>
                <td className="px-3 py-3">
                    <span className={clsx('rounded-full border px-2 py-0.5 text-xs font-medium', projectHealthBadgeClassName(health))}>{t(projectHealthLabelKeys[health])}</span>
                </td>
            </>
        );
    }

    return (
        <>
            <td className="px-3 py-3 text-center">
                <span className="font-medium text-content-primary">{summary.total_tasks ?? 0}</span>
                <span className="ml-1 text-xs text-content-secondary">
                    / {summary.completed_tasks ?? 0} {t('surfaces.projectsPage.done')}
                </span>
            </td>
            <td className="px-3 py-3 text-center">
                <span className="font-medium text-content-primary">
                    {formatEffortDays(summary.remaining_effort_days, i18n.language) ?? t('common.unknown')}
                </span>
                <span className="ml-1 text-xs text-content-secondary">
                    / {formatEffortDays(summary.total_effort_days, i18n.language) ?? t('common.unknown')}
                </span>
            </td>
            <td className="px-3 py-3">
                {/* Health and the delivery signals read together in one place. */}
                <div className="flex flex-wrap gap-1.5">
                    {/* Each chip names what it measures; an unknown date risk adds nothing the Target column does not show. */}
                    <span className={clsx('rounded-full border px-2 py-0.5 text-xs font-medium', projectHealthBadgeClassName(health))}>
                        {t('surfaces.projectsPage.healthSignal', { value: t(projectHealthLabelKeys[health]) })}
                    </span>
                    {summary.target_date_risk !== 'unknown' && (
                        <span className={clsx('inline-flex items-center rounded-full border px-2 py-0.5 text-xs font-medium', projectHealthBadgeClassName(summary.target_date_risk))}>
                            {t('surfaces.projectsPage.targetSignal', { value: t(projectHealthLabelKeys[summary.target_date_risk as ProjectHealth] ?? 'surfaces.projectsPage.unknown') })}
                        </span>
                    )}
                    {(summary.blocked_tasks ?? 0) > 0 && (
                        <span className="inline-flex items-center rounded-full bg-feedback-warning-muted px-2 py-0.5 text-xs text-feedback-warning-foreground">
                            <AlertTriangle aria-hidden="true" className="mr-1 h-3 w-3" />
                            <span aria-hidden="true">{summary.blocked_tasks}</span>
                            <span className="sr-only">
                                {t('surfaces.projectsPage.blockedTaskCount', { count: summary.blocked_tasks })}
                            </span>
                        </span>
                    )}
                    {(summary.overdue_tasks ?? 0) > 0 && (
                        <span className="inline-flex items-center rounded-full bg-feedback-danger-muted px-2 py-0.5 text-xs text-feedback-danger-foreground">
                            <Target aria-hidden="true" className="mr-1 h-3 w-3" />
                            <span aria-hidden="true">{summary.overdue_tasks}</span>
                            <span className="sr-only">
                                {t('surfaces.projectsPage.overdueTaskCount', { count: summary.overdue_tasks })}
                            </span>
                        </span>
                    )}
                </div>
            </td>
        </>
    );
};

const ProjectRow = ({
    isSummaryLoading,
    onEdit,
    project,
    summary,
}: {
    isSummaryLoading: boolean;
    onEdit: (project: Project) => void;
    project: Project;
    summary?: ProjectPortfolioSummary;
}) => {
    const { t } = useTranslation();
    const navigate = useNavigate();
    // The whole row opens the project; the name stays a link for keyboard and new-tab use.
    const openRow = (event: React.MouseEvent<HTMLTableRowElement>) => {
        if ((event.target as HTMLElement).closest('a, button, [role="menu"]')) return;
        navigate(`/projects/${project.id}`);
    };
    return (
        <tr className="group cursor-pointer border-b border-border-subtle hover:bg-surface-muted" onClick={openRow}>
            <td className="py-3 pl-6 pr-3">
                <Link to={`/projects/${project.id}`} className="font-medium text-content-primary hover:text-action">
                    {project.name}
                </Link>
                {project.description && (
                    <p className="mt-1 max-w-md truncate text-xs text-content-secondary" title={project.description}>{project.description}</p>
                )}
            </td>
            <td className="px-3 py-3">
                <span className={clsx('whitespace-nowrap rounded-full border px-2 py-0.5 text-xs font-medium', projectStatusBadgeClassName(project.status))}>
                    {t(projectStatusLabelKeys[project.status])}
                </span>
            </td>
            <td className="px-3 py-3 text-sm text-content-secondary">
                {formatPortfolioOwnerLabel(project.owner_profile, project.owner, project.owner_id, '—')}
            </td>
            <td className="whitespace-nowrap px-3 py-3 text-sm text-content-secondary">{formatDate(project.target_date)}</td>
            <ProjectSummaryCells isLoading={isSummaryLoading} summary={summary} health={project.health} />
            <td className="sticky right-0 bg-surface-card px-2 py-3 text-right group-hover:bg-surface-muted">
                <OverflowMenu
                    label={t('surfaces.projectsPage.rowActions', { name: project.name })}
                    items={[
                        { label: t('surfaces.projectsPage.open'), onSelect: () => navigate(`/projects/${project.id}`) },
                        { label: t('surfaces.projectsPage.edit'), onSelect: () => onEdit(project) },
                    ]}
                />
            </td>
        </tr>
    );
};

const ProjectsPage = () => {
    const { t } = useTranslation();
    const queryClient = useQueryClient();
    const navigate = useNavigate();
    const [searchParams, setSearchParams] = useSearchParams();
    const [isCreating, setIsCreating] = useState(false);
    const [editingProject, setEditingProject] = useState<Project | null>(null);
    const [isCreatingInitiative, setIsCreatingInitiative] = useState(false);
    const { requestConfirmation, confirmationDialog } = useConfirmDialog();
    const [editingInitiative, setEditingInitiative] = useState<Initiative | null>(null);
    const [initiativeError, setInitiativeError] = useState<string | null>(null);
    // Search, filters, the view and the timeline window live in the address, so
    // switching views keeps them and a link reopens the same portfolio.
    const view: PortfolioView = readPortfolioView(searchParams);
    const filters: PortfolioFilters = useMemo(() => readPortfolioFilters(searchParams), [searchParams]);
    const timelineWindow = useMemo(() => readTimelineWindow(searchParams), [searchParams]);
    const requestedSavedViewId = readSavedViewId(searchParams);
    const appliedSavedViewIdRef = useRef<number | null>(null);

    const { data: projectsData, isLoading, error: projectsError, refetch: refetchProjects } = useQuery({
        queryKey: ['projects'],
        queryFn: projectService.getAll,
    });

    const { data: initiativesData, isLoading: initiativesLoading, error: initiativesError, refetch: refetchInitiatives } = useQuery({
        queryKey: ['initiatives'],
        queryFn: projectService.getInitiatives,
    });

    const {
        data: portfolioSummaries,
        error: portfolioSummariesError,
        isLoading: portfolioSummariesLoading,
        refetch: refetchPortfolioSummaries,
    } = useQuery({
        queryKey: ['projectSummary', 'portfolio'],
        queryFn: projectService.getPortfolioSummaries,
        enabled: Boolean(projectsData),
        staleTime: 30000,
    });

    const { data: requestedSavedView, error: savedViewError, refetch: refetchSavedView } = useQuery({
        queryKey: ['saved-view', requestedSavedViewId],
        queryFn: () => savedViewService.getById(requestedSavedViewId as number),
        enabled: Boolean(requestedSavedViewId),
    });
    const projects = useMemo(() => projectsData ?? [], [projectsData]);
    const initiatives = useMemo(() => initiativesData ?? [], [initiativesData]);
    const portfolioSummariesByProject = useMemo(
        () => new Map((portfolioSummaries ?? []).map(summary => [summary.project_id, summary])),
        [portfolioSummaries],
    );

    const updateParams = useCallback((changes: Record<string, string | null>) => {
        setSearchParams(current => {
            const next = new URLSearchParams(current);
            Object.entries(changes).forEach(([key, value]) => {
                if (value) next.set(key, value);
                else next.delete(key);
            });
            return next;
        }, { replace: true });
    }, [setSearchParams]);

    /** A filter change leaves the saved view it started from. */
    const updateFilters = useCallback((changes: Record<string, string | null>) => {
        updateParams(requestedSavedViewId !== null ? { ...changes, [PORTFOLIO_PARAMS.view]: null } : changes);
    }, [requestedSavedViewId, updateParams]);

    // Leaving a saved view lets the same view be opened again later.
    useEffect(() => {
        if (requestedSavedViewId === null) appliedSavedViewIdRef.current = null;
    }, [requestedSavedViewId]);

    useEffect(() => {
        if (
            !requestedSavedViewId ||
            !requestedSavedView ||
            appliedSavedViewIdRef.current === requestedSavedViewId ||
            requestedSavedView.view_type !== 'projects' ||
            !requestedSavedView.is_valid
        ) {
            return;
        }
        appliedSavedViewIdRef.current = requestedSavedViewId;
        const saved = projectFiltersFromSavedView(requestedSavedView);
        updateParams({
            ...Object.fromEntries(ALL_FILTER_PARAMS.map(key => [key, null])),
            [PORTFOLIO_PARAMS.search]: saved.search || null,
            [PORTFOLIO_PARAMS.status]: saved.status || null,
            [PORTFOLIO_PARAMS.health]: saved.health || null,
        });
    }, [requestedSavedView, requestedSavedViewId, updateParams]);

    const activeSavedView = requestedSavedViewId !== null && requestedSavedView?.view_type === 'projects'
        ? requestedSavedView
        : null;

    const filteredProjects = useMemo(
        () => projects.filter(project => matchesPortfolioFilters(project, filters)),
        [projects, filters],
    );
    const filtersActive = hasActiveFilters(filters);
    const hasActiveProjectFilters = filtersActive || Boolean(activeSavedView);
    // Initiatives are part of the portfolio too: with no projects yet, their
    // headers still show (empty) so they can be seen and edited.
    const hasPortfolio = projects.length > 0 || initiatives.length > 0;
    const showViews = filteredProjects.length > 0 || (hasPortfolio && !filtersActive);

    const [sort, setSort] = useState<{ key: SortKey; descending: boolean }>({ key: 'name', descending: false });
    const toggleSort = (key: SortKey) => setSort(current => ({ key, descending: current.key === key ? !current.descending : false }));
    const sortedProjects = useMemo(() => {
        const value = (project: Project): string | number => {
            const summary = portfolioSummariesByProject.get(project.id);
            switch (sort.key) {
                case 'status': return project.status;
                case 'owner': return formatPortfolioOwnerLabel(project.owner_profile, project.owner, project.owner_id, '').toLocaleLowerCase();
                case 'target': return project.target_date ?? '9999-12-31';
                case 'tasks': return summary?.total_tasks ?? -1;
                case 'effort': return summary?.remaining_effort_days ?? -1;
                // Worst first when descending: risk, then blocked and overdue work.
                case 'signals': return (RISK_ORDER[summary?.target_date_risk ?? 'unknown'] ?? 0) * 10000 + (summary?.blocked_tasks ?? 0) + (summary?.overdue_tasks ?? 0);
                default: return project.name.toLocaleLowerCase();
            }
        };
        return [...filteredProjects].sort((left, right) => {
            const a = value(left);
            const b = value(right);
            const order = typeof a === 'number' && typeof b === 'number' ? a - b : String(a).localeCompare(String(b));
            return sort.descending ? -order : order;
        });
    }, [filteredProjects, portfolioSummariesByProject, sort]);
    const listGroups = useMemo(
        () => groupByInitiative(sortedProjects, project => project, initiatives, !filtersActive),
        [sortedProjects, initiatives, filtersActive],
    );
    const initiativesById = useMemo(() => new Map(initiatives.map(initiative => [initiative.id, initiative])), [initiatives]);

    const clearProjectFilters = () => {
        updateFilters(Object.fromEntries(ALL_FILTER_PARAMS.map(key => [key, null])));
    };

    const projectCountByInitiative = useMemo(() => {
        const counts = new Map<number, number>();
        projects.forEach(project => {
            if (project.initiative_id) {
                counts.set(project.initiative_id, (counts.get(project.initiative_id) ?? 0) + 1);
            }
        });
        return counts;
    }, [projects]);
    const activeProjectCount = projects.filter(project => !['completed', 'canceled'].includes(project.status)).length;
    const atRiskProjectCount = projects.filter(project => ['at_risk', 'off_track'].includes(project.health)).length;
    // "No risk flags" is only true when every project's health has been assessed.
    const unassessedProjectCount = projects.filter(project => project.health === 'unknown').length;
    const unassignedProjectCount = projects.filter(project => !project.initiative_id).length;

    const ownerOptions = useMemo(() => {
        const owners = new Map<string, string>();
        projects.forEach(project => {
            const key = ownerKeyForProject(project);
            if (key) owners.set(key, formatPortfolioOwnerLabel(project.owner_profile, project.owner, project.owner_id));
        });
        return Array.from(owners, ([value, label]) => ({ value, label }))
            .sort((a, b) => a.label.localeCompare(b.label) || a.value.localeCompare(b.value));
    }, [projects]);

    const filterBarFilters: FilterBarFilter[] = [
        {
            id: 'status',
            label: t('surfaces.projectsPage.status'),
            value: filters.status,
            options: PROJECT_STATUSES.map(status => ({ value: status, label: t(projectStatusLabelKeys[status]) })),
        },
        {
            id: 'health',
            label: t('surfaces.projectsPage.health'),
            value: filters.health || (filters.attention === 'at_risk' ? HEALTH_NEEDS_ATTENTION : ''),
            options: [
                ...PROJECT_HEALTHS.map(health => ({ value: health, label: t(projectHealthLabelKeys[health]) })),
                { value: HEALTH_NEEDS_ATTENTION, label: t('surfaces.projectsPage.atRiskOrOffTrack') },
            ],
        },
        {
            id: 'owner',
            label: t('surfaces.projectsPage.owner'),
            value: filters.owner,
            options: [{ value: NONE_VALUE, label: t('surfaces.projectsPage.noOwner') }, ...ownerOptions],
        },
        {
            id: 'initiative',
            label: t('surfaces.projectsPage.initiative'),
            value: filters.initiative,
            options: [
                { value: NONE_VALUE, label: t('surfaces.projectsPage.noInitiative') },
                ...initiatives.map(initiative => ({ value: String(initiative.id), label: initiative.name })),
            ],
        },
    ];

    const changeFilter = (id: string, value: string) => {
        if (id === 'health') {
            // "At risk or off track" is the at-risk count's condition; a single health replaces it.
            const needsAttention = value === HEALTH_NEEDS_ATTENTION;
            updateFilters({
                [PORTFOLIO_PARAMS.health]: needsAttention ? null : value || null,
                [PORTFOLIO_PARAMS.attention]: needsAttention ? 'at_risk' : null,
            });
            return;
        }
        updateFilters({ [FILTER_PARAM[id]]: value || null });
    };

    const deleteInitiativeMutation = useMutation({
        mutationFn: (initiativeId: number) => projectService.deleteInitiative(initiativeId),
        meta: { success: (_data, initiativeId) => feedbackMessage(t, 'deleted', 'initiative', initiatives.find(item => item.id === initiativeId)?.name) } satisfies MutationFeedbackMeta,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['initiatives'] });
            queryClient.invalidateQueries({ queryKey: ['projects'] });
            setInitiativeError(null);
        },
        onError: (err: unknown) => {
            setInitiativeError(getApiErrorMessage(err, t('queryFeedback.fallback')));
        },
    });

    const handleDeleteInitiative = (initiative: Initiative) => {
        const projectCount = projectCountByInitiative.get(initiative.id) ?? 0;
        requestConfirmation({
            title: t('actions.delete'),
            description: (
                <>
                    <strong>{initiative.name}</strong>
                    {projectCount > 0 && (
                        <> · {t('surfaces.projectsPage.initiativeProjectCount', { count: projectCount })}</>
                    )}
                </>
            ),
            confirmLabel: t('actions.delete'),
            cancelLabel: t('actions.cancel'),
            closeLabel: t('actions.close'),
            onConfirm: () => deleteInitiativeMutation.mutateAsync(initiative.id),
        });
    };
    const editInitiativeById = (initiativeId: number) => {
        const initiative = initiativesById.get(initiativeId);
        if (initiative) setEditingInitiative(initiative);
    };
    const deleteInitiativeById = (initiativeId: number) => {
        const initiative = initiativesById.get(initiativeId);
        if (initiative && !deleteInitiativeMutation.isPending) handleDeleteInitiative(initiative);
    };

    const activePreset: WindowPreset | '' = !timelineWindow.from && !timelineWindow.to
        ? 'fit'
        : WINDOW_PRESETS.find(preset => {
            const [start, end] = preset.range();
            return timelineWindow.from === inputDate(start) && timelineWindow.to === inputDate(end);
        })?.value ?? '';
    const choosePreset = (value: WindowPreset) => {
        const preset = WINDOW_PRESETS.find(candidate => candidate.value === value);
        if (!preset) {
            updateParams({ [PORTFOLIO_PARAMS.from]: null, [PORTFOLIO_PARAMS.to]: null });
            return;
        }
        const [start, end] = preset.range();
        updateParams({ [PORTFOLIO_PARAMS.from]: inputDate(start), [PORTFOLIO_PARAMS.to]: inputDate(end) });
    };

    const closeProjectEditor = () => { setIsCreating(false); setEditingProject(null); };
    const closeInitiativeEditor = () => { setIsCreatingInitiative(false); setEditingInitiative(null); };

    const exceptionButton = (pressed: boolean, onClick: () => void, label: string, risk = false) => (
        <button data-page-chrome-control="button" type="button" className={clsx('projects-exception', risk && 'is-risk')}
            aria-pressed={pressed} onClick={onClick}>
            {risk && <AlertTriangle aria-hidden="true" className="h-4 w-4" />}
            {label}
        </button>
    );

    const headerMeta = projectsData && projects.length > 0 ? (
        <div className="projects-header-meta">
            <p className="projects-workspace-facts">
                {t('surfaces.projectsPage.portfolioSummary', { active: activeProjectCount, total: projects.length })}
                {hasActiveProjectFilters && (
                    <span aria-live="polite">
                        {' · '}
                        {t('surfaces.projectsPage.showingProjects', { shown: filteredProjects.length, total: projects.length })}
                    </span>
                )}
            </p>
            <div className="projects-exceptions" role="group" aria-label={t('surfaces.projectsPage.portfolioExceptions')}>
                {atRiskProjectCount > 0
                    ? exceptionButton(
                        filters.attention === 'at_risk',
                        () => changeFilter('health', filters.attention === 'at_risk' ? '' : HEALTH_NEEDS_ATTENTION),
                        t('surfaces.projectsPage.atRiskCount', { count: atRiskProjectCount }),
                        true,
                    )
                    : unassessedProjectCount > 0
                        ? exceptionButton(
                            filters.health === 'unknown',
                            () => changeFilter('health', filters.health === 'unknown' ? '' : 'unknown'),
                            t('surfaces.projectsPage.healthNotAssessed', { count: unassessedProjectCount }),
                        )
                        : <span className="projects-exception is-clear">{t('surfaces.projectsPage.noRiskFlags')}</span>}
                {unassignedProjectCount > 0 && exceptionButton(
                    filters.initiative === NONE_VALUE,
                    () => updateFilters({ [PORTFOLIO_PARAMS.initiative]: filters.initiative === NONE_VALUE ? null : NONE_VALUE }),
                    t('surfaces.projectsPage.unassignedCount', { count: unassignedProjectCount }),
                )}
                {activeSavedView && (
                    <span className="projects-saved-view">
                        {t('surfaces.projectsPage.savedView')}: {activeSavedView.name}
                    </span>
                )}
            </div>
        </div>
    ) : undefined;

    return (
        <PageLayout variant={view === 'roadmap' ? 'wide' : 'default'}>
            <PageHeader
                title={t('surfaces.projectsPage.projects')}
                purpose={t('surfaces.projectsPage.purpose')}
                meta={headerMeta}
                primaryAction={projectsData && !hasPortfolio ? undefined : (
                    <Button onClick={() => setIsCreating(true)}>
                        <Plus aria-hidden="true" className="mr-2 h-4 w-4" />
                        {t('surfaces.projectsPage.newProject')}
                    </Button>
                )}
                secondaryActions={(
                    <Button variant="secondary" onClick={() => setIsCreatingInitiative(true)}>
                        <Plus aria-hidden="true" className="mr-2 h-4 w-4" />
                        {t('surfaces.projectsPage.newInitiative')}
                    </Button>
                )}
            />

            {savedViewError && <QueryErrorState error={savedViewError} onRetry={() => { void refetchSavedView(); }} />}

            {isLoading && !projectsData && <QueryLoadingState message={t('surfaces.projectsPage.loadingProjects')} />}
            {projectsError && !projectsData && <QueryErrorState error={projectsError} onRetry={() => { void refetchProjects(); }} />}
            {projectsError && projectsData && (
                <QueryStaleState message={t('surfaces.projectsPage.staleProjects')} onRetry={() => { void refetchProjects(); }} />
            )}
            {initiativesLoading && !initiativesData && projectsData && <QueryLoadingState message={t('surfaces.projectsPage.loadingInitiatives')} />}
            {initiativesError && !initiativesData && <QueryErrorState error={initiativesError} onRetry={() => { void refetchInitiatives(); }} />}
            {initiativesError && initiativesData && (
                <QueryStaleState message={t('surfaces.projectsPage.staleInitiatives')} onRetry={() => { void refetchInitiatives(); }} />
            )}
            {initiativeError && (
                <div role="alert" className="rounded-md bg-feedback-danger-muted p-3 text-sm text-feedback-danger-foreground">
                    {initiativeError}
                </div>
            )}

            {projectsData && (
                <section className="projects-workspace" aria-labelledby="projects-workspace-title">
                    <h2 id="projects-workspace-title" className="sr-only">{t('surfaces.projectsPage.projectPortfolio')}</h2>

                    {hasPortfolio && (
                        <PageToolbar
                            label={t('surfaces.projectsPage.projectFilters')}
                            search={(
                                <div className="relative">
                                    <Search aria-hidden="true" className="pointer-events-none absolute left-3 top-1/2 z-10 h-4 w-4 -translate-y-1/2 text-content-tertiary" />
                                    <Input
                                        type="search"
                                        aria-label={t('surfaces.projectsPage.searchProjects')}
                                        value={filters.search}
                                        onChange={event => updateFilters({ [PORTFOLIO_PARAMS.search]: event.target.value || null })}
                                        placeholder={t('surfaces.projectsPage.searchProjects')}
                                        className="pl-9"
                                    />
                                </div>
                            )}
                            filters={(
                                <FilterBar
                                    filters={filterBarFilters}
                                    onChange={changeFilter}
                                    onClear={clearProjectFilters}
                                />
                            )}
                            viewSwitch={(
                                <ViewSwitch<PortfolioView>
                                    label={t('surfaces.projectsPage.viewSwitch')}
                                    value={view}
                                    onChange={next => updateParams({ [PORTFOLIO_PARAMS.view]: next === 'roadmap' ? 'roadmap' : null })}
                                    options={[
                                        { value: 'list', label: t('surfaces.projectsPage.viewList'), icon: <List aria-hidden="true" className="h-4 w-4" /> },
                                        { value: 'roadmap', label: t('surfaces.projectsPage.viewRoadmap'), icon: <MapIcon aria-hidden="true" className="h-4 w-4" /> },
                                    ]}
                                />
                            )}
                            viewOptions={view === 'roadmap' ? (
                                <SegmentedControl<WindowPreset>
                                    label={t('surfaces.roadmapPage.windowPresets')}
                                    value={activePreset as WindowPreset}
                                    onChange={choosePreset}
                                    options={[
                                        ...WINDOW_PRESETS.map(preset => ({ value: preset.value, label: t(preset.labelKey) })),
                                        { value: 'fit' as const, label: t('surfaces.roadmapPage.presetFit') },
                                    ]}
                                />
                            ) : undefined}
                        />
                    )}

                    {!hasPortfolio && (
                        <TableFrame className="py-16 text-center">
                            <InlineEmptyState
                                className="mx-auto max-w-xl"
                                icon={<FolderOpen className="h-5 w-5" />}
                                title={t('surfaces.projectsPage.noProjectsFound')}
                                description={t('surfaces.projectsPage.createAProjectToGroupTaskWork')}
                                actions={(
                                    <Button onClick={() => setIsCreating(true)}>
                                        <Plus aria-hidden="true" className="mr-2 h-4 w-4" />
                                        {t('surfaces.projectsPage.newProject')}
                                    </Button>
                                )}
                            />
                        </TableFrame>
                    )}

                    {hasPortfolio && !showViews && (
                        <TableFrame className="py-16 text-center">
                            <InlineEmptyState
                                className="mx-auto max-w-xl"
                                icon={<Search className="h-5 w-5" />}
                                title={t('surfaces.projectsPage.noProjectsMatchFilters')}
                                description={t('surfaces.projectsPage.adjustOrClearProjectFilters')}
                                actions={hasActiveProjectFilters ? (
                                    <Button onClick={clearProjectFilters}>
                                        {t('surfaces.projectsPage.clearFilters')}
                                    </Button>
                                ) : undefined}
                            />
                        </TableFrame>
                    )}

                    {showViews && view === 'roadmap' && (
                        <RoadmapView
                            projects={filteredProjects}
                            initiatives={initiatives}
                            includeEmptyGroups={!filtersActive}
                            window={timelineWindow}
                            onResetWindow={() => choosePreset('fit')}
                            onEditInitiative={editInitiativeById}
                            onDeleteInitiative={deleteInitiativeById}
                        />
                    )}

                    {showViews && view === 'list' && (
                        <>
                            {portfolioSummariesLoading && (
                                <div
                                    aria-busy="true"
                                    aria-live="polite"
                                    className="flex items-center gap-2 rounded-md border border-border bg-surface-muted px-3 py-2 text-sm text-content-secondary"
                                    role="status"
                                >
                                    <LoaderCircle aria-hidden="true" className="h-4 w-4 animate-spin text-action" />
                                    {t('surfaces.projectsPage.loadingPortfolioSummaries')}
                                </div>
                            )}
                            {portfolioSummariesError && (
                                <QueryStaleState
                                    message={t('surfaces.projectsPage.portfolioSummariesUnavailable')}
                                    onRetry={() => { void refetchPortfolioSummaries(); }}
                                />
                            )}
                            <TableFrame className="projects-table">
                                {/* Focusable, so the table can be scrolled with the keyboard when it does not fit. Relative, so
                                    screen-reader-only labels inside stay within it instead of widening the page. */}
                                {/* eslint-disable-next-line jsx-a11y/no-noninteractive-tabindex -- a scrollable region must be reachable by keyboard to scroll it. */}
                                <div aria-busy={portfolioSummariesLoading} className="relative overflow-x-auto" tabIndex={0} role="region" aria-label={t('surfaces.projectsPage.projectsTable')}>
                                    <table className="w-full min-w-[860px]">
                                        <thead className="bg-surface-muted">
                                            <tr className="border-b border-border text-left text-xs font-medium text-content-secondary">
                                                {SORT_COLUMNS.map(column => (
                                                    <th key={column.key} scope="col" className={clsx('px-3 py-3', column.key === 'name' && 'pl-6', column.center && 'text-center')}
                                                        aria-sort={sort.key === column.key ? (sort.descending ? 'descending' : 'ascending') : undefined}>
                                                        <button data-page-chrome-control="button" type="button" onClick={() => toggleSort(column.key)}
                                                            className="inline-flex items-center gap-1 font-medium hover:text-content-primary focus:outline-none focus-visible:ring-2 focus-visible:ring-focus">
                                                            {t(column.labelKey)}
                                                            <span aria-hidden="true">{sort.key === column.key ? (sort.descending ? '↓' : '↑') : ''}</span>
                                                        </button>
                                                    </th>
                                                ))}
                                                <th scope="col" className="sticky right-0 w-12 bg-surface-muted px-2 py-3"><span className="sr-only">{t('surfaces.projectsPage.actions')}</span></th>
                                            </tr>
                                        </thead>
                                        {listGroups.map(group => {
                                            const initiative = group.initiative;
                                            const manageable = initiative ? initiativesById.has(initiative.id) : false;
                                            return (
                                                <tbody key={group.key} className="projects-group">
                                                    <tr className="projects-group-row">
                                                        <th scope="rowgroup" colSpan={SORT_COLUMNS.length + 1} className="px-3 py-2 text-left font-normal">
                                                            <InitiativeGroupHeader
                                                                initiative={initiative}
                                                                projectCount={group.items.length}
                                                                onEdit={initiative && manageable ? () => editInitiativeById(initiative.id) : undefined}
                                                                onDelete={initiative && manageable ? () => deleteInitiativeById(initiative.id) : undefined}
                                                            />
                                                        </th>
                                                    </tr>
                                                    {group.items.length === 0 && (
                                                        <tr className="border-b border-border-subtle">
                                                            <td colSpan={SORT_COLUMNS.length + 1} className="py-3 pl-6 pr-3 text-sm text-content-secondary">
                                                                {t('surfaces.projectsPage.noProjectsInInitiative')}
                                                            </td>
                                                        </tr>
                                                    )}
                                                    {group.items.map(project => (
                                                        <ProjectRow
                                                            key={project.id}
                                                            isSummaryLoading={portfolioSummariesLoading}
                                                            project={project}
                                                            summary={portfolioSummariesByProject.get(project.id)}
                                                            onEdit={setEditingProject}
                                                        />
                                                    ))}
                                                </tbody>
                                            );
                                        })}
                                    </table>
                                </div>
                            </TableFrame>
                        </>
                    )}
                </section>
            )}

            <SlideOverDrawer
                open={Boolean(isCreating || editingProject)}
                title={editingProject ? t('surfaces.projectsPage.editProject') : t('surfaces.projectsPage.createProject')}
                closeLabel={t('actions.close')}
                onClose={closeProjectEditor}
            >
                <div className="p-5">
                    {(isCreating || editingProject) && (
                        <ProjectForm
                            initialData={editingProject || undefined}
                            onSuccess={(project) => {
                                const created = !editingProject;
                                closeProjectEditor();
                                if (created) navigate(`/projects/${project.id}`);
                            }}
                            onCancel={closeProjectEditor}
                        />
                    )}
                </div>
            </SlideOverDrawer>

            <SlideOverDrawer
                open={Boolean(isCreatingInitiative || editingInitiative)}
                title={editingInitiative ? t('surfaces.projectsPage.editInitiative') : t('surfaces.projectsPage.createInitiative')}
                closeLabel={t('actions.close')}
                onClose={closeInitiativeEditor}
            >
                <div className="p-5">
                    {(isCreatingInitiative || editingInitiative) && (
                        <InitiativeForm
                            initialData={editingInitiative || undefined}
                            onSuccess={closeInitiativeEditor}
                            onCancel={closeInitiativeEditor}
                        />
                    )}
                </div>
            </SlideOverDrawer>
            {confirmationDialog}
        </PageLayout>
    );
};

export default ProjectsPage;

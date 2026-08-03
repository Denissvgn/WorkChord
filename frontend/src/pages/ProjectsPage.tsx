import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { Link, useNavigate, useSearchParams } from 'react-router-dom';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import {
    AlertTriangle,
    ChevronDown,
    FolderOpen,
    LoaderCircle,
    Plus,
    Search,
    Target,
} from 'lucide-react';
import clsx from 'clsx';
import { Button } from '../components/common/Button';
import { Input } from '../components/common/Input';
import { Modal } from '../components/common/Modal';
import { useConfirmDialog } from '../components/common/useConfirmDialog';
import { QueryErrorState, QueryLoadingState, QueryStaleState } from '../components/feedback/QueryState';
import { InitiativeForm } from '../components/projects/InitiativeForm';
import { ProjectForm } from '../components/projects/ProjectForm';
import { projectStatusBadgeClassName } from '../components/projects/projectStatusStyles';
import { InlineEmptyState, PageHeader, PageLayout, TableFrame } from '../components/ui';
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

const healthClassName = (health: string) => {
    switch (health) {
        case 'on_track':
            return 'bg-feedback-success-muted text-feedback-success-foreground border-feedback-success-border';
        case 'at_risk':
            return 'bg-feedback-warning-muted text-feedback-warning-foreground border-feedback-warning-border';
        case 'off_track':
            return 'bg-feedback-danger-muted text-feedback-danger-foreground border-feedback-danger-border';
        default:
            return 'bg-surface-muted text-content-primary border-border';
    }
};

const riskLabelKeys: Record<string, string> = {
    unknown: 'surfaces.projectsPage.unknown',
    on_track: 'surfaces.projectsPage.onTrack',
    at_risk: 'surfaces.projectsPage.atRisk',
    off_track: 'surfaces.projectsPage.offTrack',
};

const riskClassName = (risk: string) => {
    switch (risk) {
        case 'on_track':
            return 'bg-feedback-success-muted text-feedback-success-foreground border-feedback-success-border';
        case 'at_risk':
            return 'bg-feedback-warning-muted text-feedback-warning-foreground border-feedback-warning-border';
        case 'off_track':
            return 'bg-feedback-danger-muted text-feedback-danger-foreground border-feedback-danger-border';
        default:
            return 'bg-surface-muted text-content-primary border-border';
    }
};

const formatEffortDays = (value: number | undefined, language: string) => new Intl.NumberFormat(language, {
    style: 'unit',
    unit: 'day',
    unitDisplay: 'narrow',
    maximumFractionDigits: 1,
}).format(value ?? 0);

const projectFiltersFromSavedView = (view: SavedView) => {
    const raw = view.filters_json;
    const status: ProjectStatus | '' = typeof raw.status === 'string' && raw.status in projectStatusLabelKeys
        ? raw.status as ProjectStatus
        : '';
    const health: ProjectHealth | '' = typeof raw.health === 'string' && raw.health in projectHealthLabelKeys
        ? raw.health as ProjectHealth
        : '';

    return {
        search: typeof raw.search === 'string' ? raw.search : '',
        status,
        health,
    };
};

const ProjectSummaryCells = ({
    isLoading,
    summary,
}: {
    isLoading: boolean;
    summary?: ProjectPortfolioSummary;
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
                {[0, 1, 2].map(cell => (
                    <td key={cell} className="px-4 py-3 text-center text-content-tertiary">—</td>
                ))}
            </>
        );
    }

    return (
        <>
            <td className="px-4 py-3 text-center">
                <span className="font-medium text-content-primary">{summary?.total_tasks ?? 0}</span>
                <span className="ml-1 text-xs text-content-secondary">
                    / {summary?.completed_tasks ?? 0} {t('surfaces.projectsPage.done')}
                </span>
            </td>
            <td className="px-4 py-3 text-center">
                <span className="font-medium text-content-primary">
                    {formatEffortDays(summary?.remaining_effort_days, i18n.language)}
                </span>
                <span className="ml-1 text-xs text-content-secondary">
                    / {formatEffortDays(summary?.total_effort_days, i18n.language)}
                </span>
            </td>
            <td className="px-4 py-3">
                <div className="flex justify-center gap-2">
                    {summary && (
                        <span className={clsx('inline-flex items-center rounded-full border px-2 py-0.5 text-xs font-medium', riskClassName(summary.target_date_risk))}>
                            {t(riskLabelKeys[summary.target_date_risk])}
                        </span>
                    )}
                    {(summary?.blocked_tasks ?? 0) > 0 && (
                        <span className="inline-flex items-center rounded-full bg-feedback-warning-muted px-2 py-0.5 text-xs text-feedback-warning-foreground">
                            <AlertTriangle aria-hidden="true" className="mr-1 h-3 w-3" />
                            <span aria-hidden="true">{summary?.blocked_tasks}</span>
                            <span className="sr-only">
                                {t('surfaces.projectsPage.blockedTaskCount', {
                                    count: summary?.blocked_tasks,
                                })}
                            </span>
                        </span>
                    )}
                    {(summary?.overdue_tasks ?? 0) > 0 && (
                        <span className="inline-flex items-center rounded-full bg-feedback-danger-muted px-2 py-0.5 text-xs text-feedback-danger-foreground">
                            <Target aria-hidden="true" className="mr-1 h-3 w-3" />
                            <span aria-hidden="true">{summary?.overdue_tasks}</span>
                            <span className="sr-only">
                                {t('surfaces.projectsPage.overdueTaskCount', {
                                    count: summary?.overdue_tasks,
                                })}
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
    return (
        <tr className="border-b border-border-subtle hover:bg-surface-muted">
            <td className="px-4 py-3">
                <Link to={`/projects/${project.id}`} className="font-medium text-content-primary hover:text-action">
                    {project.name}
                </Link>
                {project.description && (
                    <p className="mt-1 max-w-md truncate text-xs text-content-secondary">{project.description}</p>
                )}
            </td>
            <td className="px-4 py-3">
                {project.initiative ? (
                    <span className="inline-flex max-w-[180px] items-center truncate rounded-full border border-action bg-action-muted px-2 py-0.5 text-xs font-medium text-action">
                        {project.initiative.name}
                    </span>
                ) : (
                    <span className="text-sm text-content-tertiary">{t('surfaces.projectsPage.unassigned')}</span>
                )}
            </td>
            <td className="px-4 py-3">
                <span className={clsx('rounded-full border px-2 py-0.5 text-xs font-medium', projectStatusBadgeClassName(project.status))}>
                    {t(projectStatusLabelKeys[project.status])}
                </span>
            </td>
            <td className="px-4 py-3">
                <span className={clsx('rounded-full border px-2 py-0.5 text-xs font-medium', healthClassName(project.health))}>
                    {t(projectHealthLabelKeys[project.health])}
                </span>
            </td>
            <td className="px-4 py-3 text-sm text-content-secondary">
                {formatPortfolioOwnerLabel(project.owner_profile, project.owner, project.owner_id, '—')}
            </td>
            <td className="px-4 py-3 text-sm text-content-secondary">{formatDate(project.target_date)}</td>
            <ProjectSummaryCells isLoading={isSummaryLoading} summary={summary} />
            <td className="px-4 py-3 text-right">
                <Button variant="ghost" size="sm" onClick={() => onEdit(project)}>
                    {t('surfaces.projectsPage.edit')}
                </Button>
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
    const [search, setSearch] = useState('');
    const [statusFilter, setStatusFilter] = useState<ProjectStatus | ''>('');
    const [healthFilter, setHealthFilter] = useState<ProjectHealth | ''>('');
    const requestedSavedViewId = Number(searchParams.get('view')) || null;
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

    const clearRequestedViewParam = useCallback(() => {
        if (!searchParams.has('view')) return;
        const nextParams = new URLSearchParams(searchParams);
        nextParams.delete('view');
        appliedSavedViewIdRef.current = null;
        setSearchParams(nextParams, { replace: true });
    }, [searchParams, setSearchParams]);

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
        const filters = projectFiltersFromSavedView(requestedSavedView);
        const timeoutId = window.setTimeout(() => {
            setSearch(filters.search);
            setStatusFilter(filters.status);
            setHealthFilter(filters.health);
        }, 0);

        return () => window.clearTimeout(timeoutId);
    }, [requestedSavedView, requestedSavedViewId]);

    const activeSavedView = requestedSavedViewId !== null && requestedSavedView?.view_type === 'projects'
        ? requestedSavedView
        : null;

    const filteredProjects = useMemo(() => {
        const normalizedSearch = search.trim().toLowerCase();
        return projects.filter(project => {
            if (normalizedSearch && !project.name.toLowerCase().includes(normalizedSearch)) {
                return false;
            }
            if (statusFilter && project.status !== statusFilter) {
                return false;
            }
            if (healthFilter && project.health !== healthFilter) {
                return false;
            }
            return true;
        });
    }, [projects, search, statusFilter, healthFilter]);
    const hasActiveProjectFilters = Boolean(
        search.trim()
        || statusFilter
        || healthFilter
        || activeSavedView,
    );

    const clearProjectFilters = () => {
        setSearch('');
        setStatusFilter('');
        setHealthFilter('');
        clearRequestedViewParam();
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
    const unassignedProjectCount = projects.filter(project => !project.initiative_id).length;

    const deleteInitiativeMutation = useMutation({
        mutationFn: (initiativeId: number) => projectService.deleteInitiative(initiativeId),
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

    return (
        <PageLayout>
            <PageHeader
                title={t('surfaces.projectsPage.projects')}
                subtitle={t('surfaces.projectsPage.planAndTrackWorkAcrossIterations')}
                actions={projectsData && projects.length === 0 ? undefined : (
                    <Button onClick={() => setIsCreating(true)}>
                        <Plus aria-hidden="true" className="mr-2 h-4 w-4" />
                        {t('surfaces.projectsPage.newProject')}
                    </Button>
                )}
            />

            {savedViewError && <QueryErrorState error={savedViewError} onRetry={() => { void refetchSavedView(); }} />}

            {isLoading && !projectsData && <QueryLoadingState message={t('surfaces.projectsPage.loadingProjects')} />}
            {projectsError && !projectsData && <QueryErrorState error={projectsError} onRetry={() => { void refetchProjects(); }} />}
            {projectsError && projectsData && (
                <QueryStaleState message={t('surfaces.projectsPage.staleProjects')} onRetry={() => { void refetchProjects(); }} />
            )}

            {projectsData && (
                <section className="projects-workspace" aria-labelledby="projects-workspace-title">
                    <div className="projects-workspace-head">
                        <div>
                            <h2 id="projects-workspace-title" className="projects-workspace-title">
                                {t('surfaces.projectsPage.projectPortfolio')}
                            </h2>
                            <p className="projects-workspace-facts">
                                {t('surfaces.projectsPage.portfolioSummary', {
                                    active: activeProjectCount,
                                    total: projects.length,
                                })}
                                {hasActiveProjectFilters && (
                                    <span aria-live="polite">
                                        {' · '}
                                        {t('surfaces.projectsPage.showingProjects', {
                                            shown: filteredProjects.length,
                                            total: projects.length,
                                        })}
                                    </span>
                                )}
                            </p>
                        </div>
                        {projects.length > 0 && (
                            <div
                                className="projects-exceptions"
                                aria-label={t('surfaces.projectsPage.portfolioExceptions')}
                            >
                                {atRiskProjectCount > 0 ? (
                                    <span className="projects-exception is-risk">
                                        <AlertTriangle aria-hidden="true" className="h-4 w-4" />
                                        {t('surfaces.projectsPage.atRiskCount', { count: atRiskProjectCount })}
                                    </span>
                                ) : (
                                    <span className="projects-exception is-clear">
                                        {t('surfaces.projectsPage.noRiskFlags')}
                                    </span>
                                )}
                                {unassignedProjectCount > 0 && (
                                    <span className="projects-exception">
                                        {t('surfaces.projectsPage.unassignedCount', { count: unassignedProjectCount })}
                                    </span>
                                )}
                            </div>
                        )}
                    </div>

                    {projects.length > 0 && (
                        <>
                            <div
                                className="projects-filter-toolbar"
                                role="search"
                                aria-label={t('surfaces.projectsPage.projectFilters')}
                            >
                                <div className="projects-filter-search relative">
                                    <Search aria-hidden="true" className="pointer-events-none absolute left-3 top-1/2 h-4 w-4 -translate-y-1/2 text-content-tertiary" />
                                    <Input
                                        aria-label={t('surfaces.projectsPage.searchProjects')}
                                        value={search}
                                        onChange={event => {
                                            clearRequestedViewParam();
                                            setSearch(event.target.value);
                                        }}
                                        placeholder={t('surfaces.projectsPage.searchProjects')}
                                        className="pl-9"
                                    />
                                </div>
                                <select
                                    aria-label={t('surfaces.projectsPage.statusFilterLabel')}
                                    value={statusFilter}
                                    onChange={event => {
                                        clearRequestedViewParam();
                                        setStatusFilter(event.target.value as ProjectStatus | '');
                                    }}
                                    className="input"
                                >
                                    <option value="">{t('surfaces.projectsPage.allStatuses')}</option>
                                    {Object.entries(projectStatusLabelKeys).map(([value, labelKey]) => (
                                        <option key={value} value={value}>{t(labelKey)}</option>
                                    ))}
                                </select>
                                <select
                                    aria-label={t('surfaces.projectsPage.healthFilterLabel')}
                                    value={healthFilter}
                                    onChange={event => {
                                        clearRequestedViewParam();
                                        setHealthFilter(event.target.value as ProjectHealth | '');
                                    }}
                                    className="input"
                                >
                                    <option value="">{t('surfaces.projectsPage.allHealth')}</option>
                                    {Object.entries(projectHealthLabelKeys).map(([value, labelKey]) => (
                                        <option key={value} value={value}>{t(labelKey)}</option>
                                    ))}
                                </select>
                                {hasActiveProjectFilters && (
                                    <Button variant="ghost" size="sm" onClick={clearProjectFilters}>
                                        {t('surfaces.projectsPage.clearFilters')}
                                    </Button>
                                )}
                            </div>
                            {activeSavedView && (
                                <div className="projects-saved-view">
                                    {t('surfaces.projectsPage.savedView')}: {activeSavedView.name}
                                </div>
                            )}
                        </>
                    )}

                    {projects.length > 0 && portfolioSummariesLoading && (
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
                    {projects.length > 0 && portfolioSummariesError && (
                        <QueryStaleState
                            message={t('surfaces.projectsPage.portfolioSummariesUnavailable')}
                            onRetry={() => { void refetchPortfolioSummaries(); }}
                        />
                    )}

                    <TableFrame className="projects-table">
                        <div aria-busy={portfolioSummariesLoading} className="overflow-x-auto">
                            <table className="w-full min-w-[1080px]">
                                <thead className="bg-surface-muted">
                                    <tr className="border-b border-border text-left text-xs font-medium uppercase tracking-wide text-content-secondary">
                                        <th className="px-4 py-3">{t('surfaces.projectsPage.project')}</th>
                                        <th className="px-4 py-3">{t('surfaces.projectsPage.initiative')}</th>
                                        <th className="px-4 py-3">{t('surfaces.projectsPage.status')}</th>
                                        <th className="px-4 py-3">{t('surfaces.projectsPage.health')}</th>
                                        <th className="px-4 py-3">{t('surfaces.projectsPage.owner')}</th>
                                        <th className="px-4 py-3">{t('surfaces.projectsPage.target')}</th>
                                        <th className="px-4 py-3 text-center">{t('surfaces.projectsPage.tasks')}</th>
                                        <th className="px-4 py-3 text-center">{t('surfaces.projectsPage.effort')}</th>
                                        <th className="px-4 py-3 text-center">{t('surfaces.projectsPage.signals')}</th>
                                        <th className="px-4 py-3 text-right">{t('surfaces.projectsPage.actions')}</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {filteredProjects.map(project => (
                                        <ProjectRow
                                            key={project.id}
                                            isSummaryLoading={portfolioSummariesLoading}
                                            project={project}
                                            summary={portfolioSummariesByProject.get(project.id)}
                                            onEdit={setEditingProject}
                                        />
                                    ))}
                                </tbody>
                            </table>
                        </div>

                        {projects.length > 0 && filteredProjects.length === 0 && (
                            <div className="py-16 text-center">
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
                            </div>
                        )}

                        {projects.length === 0 && (
                            <div className="py-16 text-center">
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
                            </div>
                        )}
                    </TableFrame>
                </section>
            )}

            <details className="projects-initiatives">
                <summary>
                    <span className="projects-initiatives-summary">
                        <ChevronDown aria-hidden="true" className="h-4 w-4" />
                        <span>
                            <strong>{t('surfaces.projectsPage.initiatives')}</strong>
                            <small>{t('surfaces.projectsPage.groupRelatedProjectsAroundStrategicGoals')}</small>
                        </span>
                        {initiativesError && !initiativesData ? (
                            <span className="projects-initiatives-state is-error">
                                {t('surfaces.projectsPage.initiativesUnavailable')}
                            </span>
                        ) : (
                            <span className="projects-initiatives-state tnum">{initiatives.length}</span>
                        )}
                    </span>
                </summary>
                <div className="projects-initiatives-content">
                    <div className="projects-initiatives-actions">
                        <Button variant="secondary" size="sm" onClick={() => setIsCreatingInitiative(true)}>
                            <Plus aria-hidden="true" className="mr-2 h-4 w-4" />
                            {t('surfaces.projectsPage.newInitiative')}
                        </Button>
                    </div>

                    {initiativeError && (
                        <div className="rounded-md bg-feedback-danger-muted p-3 text-sm text-feedback-danger-foreground">
                            {initiativeError}
                        </div>
                    )}

                    {initiativesLoading && !initiativesData && <QueryLoadingState message={t('surfaces.projectsPage.loadingInitiatives')} />}
                    {initiativesError && !initiativesData && <QueryErrorState error={initiativesError} onRetry={() => { void refetchInitiatives(); }} />}
                    {initiativesError && initiativesData && (
                        <QueryStaleState message={t('surfaces.projectsPage.staleInitiatives')} onRetry={() => { void refetchInitiatives(); }} />
                    )}
                    {initiativesData && (
                        <div className="projects-initiatives-table overflow-x-auto">
                            <table className="w-full min-w-[760px]">
                                <thead className="bg-surface-muted">
                                    <tr className="border-b border-border text-left text-xs font-medium uppercase tracking-wide text-content-secondary">
                                        <th className="px-3 py-2">{t('surfaces.projectsPage.initiative')}</th>
                                        <th className="px-3 py-2">{t('surfaces.projectsPage.health')}</th>
                                        <th className="px-3 py-2">{t('surfaces.projectsPage.owner')}</th>
                                        <th className="px-3 py-2">{t('surfaces.projectsPage.target')}</th>
                                        <th className="px-3 py-2 text-center">{t('surfaces.projectsPage.projects')}</th>
                                        <th className="px-3 py-2 text-right">{t('surfaces.projectsPage.actions')}</th>
                                    </tr>
                                </thead>
                                <tbody>
                                    {initiatives.map(initiative => (
                                        <tr key={initiative.id} className="border-b border-border-subtle hover:bg-surface-muted">
                                            <td className="px-3 py-3">
                                                <div className="font-medium text-content-primary">{initiative.name}</div>
                                                {initiative.description && (
                                                    <p className="mt-1 max-w-md truncate text-xs text-content-secondary">
                                                        {initiative.description}
                                                    </p>
                                                )}
                                            </td>
                                            <td className="px-3 py-3">
                                                <span className={clsx('rounded-full border px-2 py-0.5 text-xs font-medium', healthClassName(initiative.health))}>
                                                    {t(projectHealthLabelKeys[initiative.health])}
                                                </span>
                                            </td>
                                            <td className="px-3 py-3 text-sm text-content-secondary">
                                                {formatPortfolioOwnerLabel(initiative.owner_profile, initiative.owner, initiative.owner_id)}
                                            </td>
                                            <td className="px-3 py-3 text-sm text-content-secondary">{formatDate(initiative.target_date)}</td>
                                            <td className="px-3 py-3 text-center text-sm font-medium text-content-primary">
                                                {projectCountByInitiative.get(initiative.id) ?? 0}
                                            </td>
                                            <td className="px-3 py-3 text-right">
                                                <div className="flex justify-end gap-2">
                                                    <Button variant="ghost" size="sm" onClick={() => setEditingInitiative(initiative)}>
                                                        {t('surfaces.projectsPage.edit')}
                                                    </Button>
                                                    <Button
                                                        variant="danger"
                                                        size="sm"
                                                        onClick={() => handleDeleteInitiative(initiative)}
                                                        disabled={deleteInitiativeMutation.isPending}
                                                    >
                                                        {t('surfaces.projectsPage.delete')}
                                                    </Button>
                                                </div>
                                            </td>
                                        </tr>
                                    ))}
                                </tbody>
                            </table>
                            {!initiativesLoading && initiatives.length === 0 && (
                                <div className="py-8 text-center text-sm text-content-secondary">
                                    {t('surfaces.projectsPage.noInitiativesYetCreateOneToGroupProjectsOnTheRoadmap')}
                                </div>
                            )}
                        </div>
                    )}
                </div>
            </details>

            <Modal
                open={Boolean(isCreating || editingProject)}
                title={editingProject ? t('surfaces.projectsPage.editProject') : t('surfaces.projectsPage.createProject')}
                closeLabel={t('actions.close')}
                onClose={() => { setIsCreating(false); setEditingProject(null); }}
            >
                {(isCreating || editingProject) && (
                        <ProjectForm
                            initialData={editingProject || undefined}
                            onSuccess={(project) => {
                                setIsCreating(false);
                                setEditingProject(null);
                                if (!editingProject) {
                                    navigate(`/projects/${project.id}`);
                                }
                            }}
                            onCancel={() => {
                                setIsCreating(false);
                                setEditingProject(null);
                            }}
                        />
                )}
            </Modal>

            <Modal
                open={Boolean(isCreatingInitiative || editingInitiative)}
                title={editingInitiative ? t('surfaces.projectsPage.editInitiative') : t('surfaces.projectsPage.createInitiative')}
                closeLabel={t('actions.close')}
                onClose={() => { setIsCreatingInitiative(false); setEditingInitiative(null); }}
                className="max-w-xl"
            >
                {(isCreatingInitiative || editingInitiative) && (
                    <InitiativeForm
                        initialData={editingInitiative || undefined}
                        onSuccess={() => {
                            setIsCreatingInitiative(false);
                            setEditingInitiative(null);
                        }}
                        onCancel={() => {
                            setIsCreatingInitiative(false);
                            setEditingInitiative(null);
                        }}
                    />
                )}
            </Modal>
            {confirmationDialog}
        </PageLayout>
    );
};

export default ProjectsPage;

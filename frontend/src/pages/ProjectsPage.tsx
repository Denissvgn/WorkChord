import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { Link, useNavigate, useSearchParams } from 'react-router-dom';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import {
    Activity,
    AlertTriangle,
    FolderOpen,
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
import { InlineEmptyState, MetricGrid, PageHeader, PageLayout, TableFrame } from '../components/ui';
import { projectService } from '../services/projectService';
import { savedViewService } from '../services/savedViewService';
import { getApiErrorMessage } from '../utils/apiError';
import { formatPortfolioOwnerLabel } from '../utils/teamMemberLabels';
import { formatDate } from '../utils/formatDate';
import type { SavedView } from '../types/savedView';
import type { Initiative, Project, ProjectHealth, ProjectStatus, ProjectSummary } from '../types/project';
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

const statusClassName = (status: string) => {
    switch (status) {
        case 'active':
            return 'bg-action-muted text-action border-action';
        case 'completed':
            return 'bg-feedback-success-muted text-feedback-success-foreground border-feedback-success-border';
        case 'paused':
            return 'bg-feedback-warning-muted text-feedback-warning-foreground border-feedback-warning-border';
        case 'canceled':
            return 'bg-feedback-danger-muted text-feedback-danger-foreground border-feedback-danger-border';
        case 'proposed':
            return 'bg-feedback-purple-muted text-feedback-purple-foreground border-feedback-purple-border';
        default:
            return 'bg-surface-muted text-content-primary border-border';
    }
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

const formatNumber = (value?: number) => (value ?? 0).toFixed(1).replace(/\.0$/, '');

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

const ProjectSummaryCells = ({ projectId }: { projectId: number }) => {
    const { t } = useTranslation();
    const { data: summary, error, isLoading, refetch } = useQuery<ProjectSummary>({
        queryKey: ['projectSummary', projectId],
        queryFn: () => projectService.getSummary(projectId),
        staleTime: 30000,
    });

    if (isLoading) {
        return <td className="px-4 py-3" colSpan={3}><QueryLoadingState message={t('surfaces.projectsPage.loadingSummary')} /></td>;
    }

    if (error) {
        return (
            <td className="px-4 py-3" colSpan={3}>
                <QueryErrorState
                    error={error}
                    fallback={t('surfaces.projectsPage.summaryLoadFailed')}
                    onRetry={() => void refetch()}
                />
            </td>
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
                <span className="font-medium text-content-primary">{formatNumber(summary?.remaining_effort_days)}d</span>
                <span className="ml-1 text-xs text-content-secondary">
                    / {formatNumber(summary?.total_effort_days)}d
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
                            <AlertTriangle className="mr-1 h-3 w-3" />
                            {summary?.blocked_tasks}
                        </span>
                    )}
                    {(summary?.overdue_tasks ?? 0) > 0 && (
                        <span className="inline-flex items-center rounded-full bg-feedback-danger-muted px-2 py-0.5 text-xs text-feedback-danger-foreground">
                            <Target className="mr-1 h-3 w-3" />
                            {summary?.overdue_tasks}
                        </span>
                    )}
                </div>
            </td>
        </>
    );
};

const ProjectRow = ({ project, onEdit }: { project: Project; onEdit: (project: Project) => void }) => {
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
                <span className={clsx('rounded-full border px-2 py-0.5 text-xs font-medium', statusClassName(project.status))}>
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
            <ProjectSummaryCells projectId={project.id} />
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

    const { data: requestedSavedView, error: savedViewError, refetch: refetchSavedView } = useQuery({
        queryKey: ['saved-view', requestedSavedViewId],
        queryFn: () => savedViewService.getById(requestedSavedViewId as number),
        enabled: Boolean(requestedSavedViewId),
    });
    const projects = useMemo(() => projectsData ?? [], [projectsData]);
    const initiatives = useMemo(() => initiativesData ?? [], [initiativesData]);

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
            description: <><strong>{initiative.name}</strong>{projectCount > 0 && <> · {projectCount} {t('surfaces.projectsPage.projects')}</>}</>,
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
                actions={(
                    <button className="btn primary" onClick={() => setIsCreating(true)}>
                    + {t('surfaces.projectsPage.newProject')}
                    </button>
                )}
            />

            {savedViewError && <QueryErrorState error={savedViewError} onRetry={() => { void refetchSavedView(); }} />}

            {isLoading && !projectsData && <QueryLoadingState message={t('surfaces.projectsPage.loadingProjects')} />}
            {projectsError && !projectsData && <QueryErrorState error={projectsError} onRetry={() => { void refetchProjects(); }} />}
            {projectsError && projectsData && (
                <QueryStaleState message={t('surfaces.projectsPage.staleProjects')} onRetry={() => { void refetchProjects(); }} />
            )}

            {projectsData && (
            <MetricGrid>
                <div className="kpi"><div className="kpi-lbl">{t('surfaces.projectsPage.total')}</div><div className="kpi-val tnum">{projects.length}</div></div>
                <div className="kpi"><div className="kpi-lbl">{t('surfaces.projectsPage.active')}</div><div className="kpi-val tnum">{activeProjectCount}</div></div>
                <div className="kpi"><div className="kpi-lbl">{t('surfaces.projectsPage.atRisk')}</div><div className="kpi-val tnum">{atRiskProjectCount}</div></div>
                <div className="kpi"><div className="kpi-lbl">{t('surfaces.projectsPage.unassigned')}</div><div className="kpi-val tnum">{unassignedProjectCount}</div></div>
            </MetricGrid>
            )}

            <div className="card">
                <div className="card-head">
                    <h3>{t('surfaces.projectsPage.initiatives')}</h3>
                    <span className="sub">{t('surfaces.projectsPage.groupRelatedProjectsAroundStrategicGoals')}</span>
                    <button className="btn sm" onClick={() => setIsCreatingInitiative(true)}>
                        + {t('surfaces.projectsPage.newInitiative')}
                    </button>
                </div>

                {initiativeError && (
                    <div className="mt-3 rounded-md bg-feedback-danger-muted p-3 text-sm text-feedback-danger-foreground">
                        {initiativeError}
                    </div>
                )}

                {initiativesLoading && !initiativesData && <QueryLoadingState message={t('surfaces.projectsPage.loadingInitiatives')} />}
                {initiativesError && !initiativesData && <QueryErrorState error={initiativesError} onRetry={() => { void refetchInitiatives(); }} />}
                {initiativesError && initiativesData && (
                    <QueryStaleState message={t('surfaces.projectsPage.staleInitiatives')} onRetry={() => { void refetchInitiatives(); }} />
                )}
                {initiativesData && (
                <div className="mt-4 overflow-x-auto">
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

            {projectsData && (
            <>
            <div className="card">
                <div className="card-head"><h3>{t('surfaces.projectsPage.projectFilters')}</h3></div>
                <div className="card-pad">
                <div className="wc-form-grid">
                    <div className="relative">
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
                </div>
                {activeSavedView && (
                    <div className="mt-3 inline-flex items-center rounded-full bg-action-muted px-3 py-1 text-xs font-medium text-action">
                        {t('surfaces.projectsPage.savedView')}: {activeSavedView.name}
                    </div>
                )}
                </div>
            </div>

            <TableFrame>
                <div className="overflow-x-auto">
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
                                    project={project}
                                    onEdit={setEditingProject}
                                />
                            ))}
                        </tbody>
                    </table>
                </div>

                {!isLoading && filteredProjects.length === 0 && (
                    <div className="py-16 text-center">
                        <InlineEmptyState
                            className="mx-auto max-w-xl"
                            icon={<FolderOpen className="h-5 w-5" />}
                            title={t('surfaces.projectsPage.noProjectsFound')}
                            description={t('surfaces.projectsPage.createAProjectToGroupTaskWork')}
                            actions={(
                                <Button onClick={() => setIsCreating(true)}>
                                    <Plus className="mr-2 h-4 w-4" />
                                    {t('surfaces.projectsPage.newProject')}
                                </Button>
                            )}
                        />
                    </div>
                )}

                {isLoading && (
                    <div className="py-16 text-center text-content-secondary">
                        <Activity className="mx-auto mb-2 h-5 w-5 animate-pulse" />
                        {t('surfaces.projectsPage.loadingProjects')}
                    </div>
                )}
            </TableFrame>
            </>
            )}

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

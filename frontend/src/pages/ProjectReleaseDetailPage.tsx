import { useState } from 'react';
import { useNavigate, useParams } from 'react-router-dom';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import {
    CalendarDays,
    CheckCircle2,
    Clock,
    Edit,
    FolderOpen,
    Package,
    Tag,
} from 'lucide-react';
import clsx from 'clsx';
import { Button } from '../components/common/Button';
import { Modal } from '../components/common/Modal';
import { QueryErrorState } from '../components/feedback/QueryState';
import { ReleaseForm } from '../components/releases/ReleaseForm';
import { MetricGrid, PageHeader, PageLayout } from '../components/ui';
import { projectService } from '../services/projectService';
import { releaseService } from '../services/releaseService';
import { getApiErrorMessage } from '../utils/apiError';
import { formatDate, formatDateTime } from '../utils/formatDate';
import type { Release, ReleaseStatus, ReleaseTaskSummary } from '../types/release';
import { isTaskStatus, pillToneClassName, STATUS_TONE } from '../components/ui/tone';
import { Breadcrumbs } from '../components/layout/Breadcrumbs';

const releaseStatusLabelKeys: Record<ReleaseStatus, string> = {
    planned: 'surfaces.releaseDetail.statuses.planned',
    building: 'surfaces.releaseDetail.statuses.building',
    shipped: 'surfaces.releaseDetail.statuses.shipped',
    canceled: 'surfaces.releaseDetail.statuses.canceled',
};

const releaseStatusTone = (status: ReleaseStatus | string): 'gray' | 'blue' | 'green' | 'red' => {
    switch (status) {
        case 'building':
            return 'blue';
        case 'shipped':
            return 'green';
        case 'canceled':
            return 'red';
        default:
            return 'gray';
    }
};

const MetadataRow = ({
    label,
    value,
}: {
    label: string;
    value: React.ReactNode;
}) => (
    <div className="flex items-center justify-between gap-3 text-sm">
        <span className="text-content-secondary">{label}</span>
        <span className="text-right font-medium text-content-primary">{value}</span>
    </div>
);

const ReleaseTaskList = ({ tasks }: { tasks: ReleaseTaskSummary[] }) => {
    const { t } = useTranslation();
    if (tasks.length === 0) {
        return (
            <div className="rounded-lg border border-dashed border-border bg-surface-muted py-10 text-center text-content-secondary">
                {t('surfaces.releaseDetail.noTasksLinkedToThisRelease')}
            </div>
        );
    }

    return (
        <div className="divide-y divide-border-subtle rounded-lg border border-border">
            {tasks.map(task => (
                <div key={task.id} className="flex flex-wrap items-center gap-3 px-4 py-3">
                    <CheckCircle2 className={clsx(
                        'h-5 w-5',
                        task.status === 'closed' ? 'text-feedback-success' : 'text-content-tertiary',
                    )} />
                    <div className="min-w-0 flex-1">
                        <p className="truncate font-medium text-content-primary">{task.title}</p>
                        <p className="text-xs text-content-secondary">{t('surfaces.releaseDetail.taskNumber', { id: task.id })}</p>
                    </div>
                    <span className={clsx(
                        'rounded-full border px-2 py-0.5 text-xs font-medium',
                        isTaskStatus(task.status) ? pillToneClassName[STATUS_TONE[task.status]] : pillToneClassName.gray,
                    )}>
                        {isTaskStatus(task.status) ? t(`statuses.${task.status}`) : task.status}
                    </span>
                </div>
            ))}
        </div>
    );
};

const ProjectReleaseDetailPage = () => {
    const { projectId, releaseId } = useParams();
    const navigate = useNavigate();
    const { t } = useTranslation();
    const queryClient = useQueryClient();
    const numericProjectId = Number(projectId);
    const numericReleaseId = Number(releaseId);
    const [isEditing, setIsEditing] = useState(false);
    const [shipError, setShipError] = useState<string | null>(null);

    const projectEnabled = Number.isInteger(numericProjectId) && numericProjectId > 0;
    const releaseEnabled = Number.isInteger(numericReleaseId) && numericReleaseId > 0;

    const { data: project, error: projectError, refetch: refetchProject } = useQuery({
        queryKey: ['project', numericProjectId],
        queryFn: () => projectService.getById(numericProjectId),
        enabled: projectEnabled,
    });

    const {
        data: release,
        isLoading,
        isError,
        error,
        refetch: refetchRelease,
    } = useQuery({
        queryKey: ['release', numericReleaseId],
        queryFn: () => releaseService.getById(numericReleaseId),
        enabled: releaseEnabled,
    });

    const markShippedMutation = useMutation({
        mutationFn: () => releaseService.update(numericReleaseId, {
            status: 'shipped',
            shipped_at: new Date().toISOString(),
        }),
        onSuccess: (updatedRelease) => {
            setShipError(null);
            queryClient.setQueryData(['release', updatedRelease.id], updatedRelease);
            queryClient.invalidateQueries({ queryKey: ['release', updatedRelease.id] });
            queryClient.invalidateQueries({ queryKey: ['projectReleases', updatedRelease.project_id] });
            updatedRelease.tasks.forEach(task => {
                queryClient.invalidateQueries({ queryKey: ['task-timeline', task.id] });
            });
        },
        onError: (err: unknown) => {
            setShipError(getApiErrorMessage(err, t('surfaces.releaseDetail.markShippedFailed')));
        },
    });

    if (projectError) return <QueryErrorState error={projectError} onRetry={() => void refetchProject()} />;

    if (!projectEnabled || !releaseEnabled) {
        return (
            <div className="py-20 text-center">
                <h1 className="text-xl font-semibold text-content-primary">{t('surfaces.releaseDetail.releaseNotFound')}</h1>
                <Button className="mt-4" onClick={() => navigate('/projects')}>{t('surfaces.releaseDetail.backToProjects')}</Button>
            </div>
        );
    }

    if (isLoading) {
        return (
            <div className="py-20 text-center text-content-secondary">
                <Package className="mx-auto mb-2 h-5 w-5 animate-pulse" />
                {t('surfaces.releaseDetail.loadingRelease')}
            </div>
        );
    }

    if (!release || isError) {
        if (isError) return <QueryErrorState error={error} onRetry={() => void refetchRelease()} />;
        return (
            <div className="py-20 text-center">
                <FolderOpen className="mx-auto h-10 w-10 text-content-tertiary" />
                <h1 className="mt-3 text-xl font-semibold text-content-primary">{t('surfaces.releaseDetail.releaseNotFound')}</h1>
                <Button className="mt-4" onClick={() => navigate(`/projects/${numericProjectId}`)}>
                    {t('surfaces.releaseDetail.backToProject')}
                </Button>
            </div>
        );
    }

    const releaseProjectId = release.project_id || numericProjectId;

    return (
        <PageLayout>
            <Breadcrumbs items={[
                { label: t('breadcrumbs.projects'), path: '/projects' },
                { label: project?.name ?? t('surfaces.releaseDetail.projectFallback'), path: `/projects/${releaseProjectId}` },
                { label: release.name },
            ]} />

            <PageHeader
                title={release.name}
                subtitle={release.description}
                eyebrow={(
                    <div className="row wrap" style={{gap:8, marginBottom:6}}>
                        <span className={`pill ${releaseStatusTone(release.status) === 'green' ? 'done' : releaseStatusTone(release.status) === 'blue' ? 'accent' : releaseStatusTone(release.status) === 'red' ? 'blocked' : 'opt'}`}>
                            <span className="pdot"/>{t(releaseStatusLabelKeys[release.status])}
                        </span>
                    </div>
                )}
                meta={(
                    <div className="row wrap" style={{gap:12}}>
                        <span><CalendarDays className="inline h-3.5 w-3.5 mr-1"/>{formatDate(release.target_date)}</span>
                        {release.version && <span><Tag className="inline h-3.5 w-3.5 mr-1"/>{release.version}</span>}
                    </div>
                )}
                actions={(
                    <>
                    {release.status !== 'shipped' && (
                        <button className="btn primary" disabled={markShippedMutation.isPending} onClick={() => markShippedMutation.mutate()}>
                            <CheckCircle2 className="h-4 w-4"/> {t('surfaces.releaseDetail.markShipped')}
                        </button>
                    )}
                    <button className="btn" onClick={() => setIsEditing(true)}>
                        <Edit className="h-4 w-4"/> {t('surfaces.releaseDetail.edit')}
                    </button>
                    </>
                )}
            />
            <MetricGrid>
                <div className="kpi"><div className="kpi-lbl">{t('surfaces.releaseDetail.linkedTasks')}</div><div className="kpi-val tnum">{release.tasks.length}</div></div>
                <div className="kpi"><div className="kpi-lbl">{t('surfaces.releaseDetail.status')}</div><div className="kpi-val" style={{fontSize:16}}>{t(releaseStatusLabelKeys[release.status])}</div></div>
                <div className="kpi"><div className="kpi-lbl">{t('surfaces.releaseDetail.shipped')}</div><div className="kpi-val" style={{fontSize:16}}>{formatDate(release.shipped_at)}</div></div>
                <div className="kpi"><div className="kpi-lbl">{t('surfaces.releaseDetail.environment')}</div><div className="kpi-val" style={{fontSize:16}}>{release.environment || '—'}</div></div>
            </MetricGrid>

            {shipError && (
                <div className="flex items-start justify-between gap-3 rounded-md bg-feedback-danger-muted p-3 text-sm text-feedback-danger-foreground">
                    <span>{shipError}</span>
                    <button
                        type="button"
                        className="text-xs font-medium text-feedback-danger-foreground hover:underline"
                        onClick={() => setShipError(null)}
                    >
                        {t('surfaces.releaseDetail.dismiss')}
                    </button>
                </div>
            )}

            <div className="wc-content-rail">
                <div className="wc-panel-stack">
                    <div className="card">
                        <div className="card-head">
                            <h3>{t('surfaces.releaseDetail.linkedTasks')}</h3>
                            <span className="sub">{t('surfaces.releaseDetail.taskCount', { count: release.tasks.length })}</span>
                        </div>
                        <div className="card-pad">
                            <ReleaseTaskList tasks={release.tasks}/>
                        </div>
                    </div>
                </div>
                <aside className="sticky-rail">
                    <div className="card">
                        <div className="card-head"><h3>{t('surfaces.releaseDetail.releaseMetadata')}</h3></div>
                        <div className="card-pad" style={{display:'flex', flexDirection:'column', gap:10}}>
                            <MetadataRow label={t('surfaces.releaseDetail.target')} value={<span><CalendarDays className="inline h-3.5 w-3.5 mr-1"/>{formatDate(release.target_date)}</span>}/>
                            <MetadataRow label={t('surfaces.releaseDetail.shipped')} value={<span><Clock className="inline h-3.5 w-3.5 mr-1"/>{formatDateTime(release.shipped_at)}</span>}/>
                            <MetadataRow label={t('surfaces.releaseDetail.version')} value={release.version || '—'}/>
                            <MetadataRow label={t('surfaces.releaseDetail.environment')} value={release.environment || '—'}/>
                            <MetadataRow label={t('surfaces.releaseDetail.updated')} value={formatDateTime(release.updated_at)}/>
                        </div>
                    </div>
                    <div className="card card-pad">
                        <h3 style={{fontSize:12.5, fontWeight:600, margin:'0 0 8px'}}>{t('surfaces.releaseDetail.attachOrDetach')}</h3>
                        <p className="muted" style={{fontSize:12, marginBottom:12}}>
                            {t('surfaces.releaseDetail.useEditToChangeReleaseFieldsAndReplaceTheLinkedTaskSet')}
                        </p>
                        <button className="btn" style={{width:'100%'}} onClick={() => setIsEditing(true)}>
                            {t('surfaces.releaseDetail.editLinkedTasks')}
                        </button>
                    </div>
                </aside>
            </div>

            <Modal open={isEditing} title={t('surfaces.releaseDetail.editRelease')} closeLabel={t('actions.close')} onClose={() => setIsEditing(false)} className="max-w-3xl">
                {isEditing && (
                    <ReleaseForm
                        projectId={release.project_id}
                        initialData={release as Release}
                        onSuccess={() => setIsEditing(false)}
                        onCancel={() => setIsEditing(false)}
                    />
                )}
            </Modal>
        </PageLayout>
    );
};

export default ProjectReleaseDetailPage;

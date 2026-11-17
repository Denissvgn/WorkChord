import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import clsx from 'clsx';
import {
    Activity,
    Edit,
    Send,
    Trash2
} from 'lucide-react';
import type { FormEvent } from 'react';
import { useEffect, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { Link, useNavigate, useParams, useSearchParams } from 'react-router-dom';
import { Button } from '../components/common/Button';
import { ConfirmDialog } from '../components/common/ConfirmDialog';
import { QueryErrorState } from '../components/feedback/QueryState';
import { useToast } from '../components/feedback/toast';
import { Breadcrumbs } from '../components/layout/Breadcrumbs';
import { MilestoneFormDrawer } from '../components/projects/MilestoneFormDrawer';
import { PostUpdateDrawer } from '../components/projects/PostUpdateDrawer';
import { buildMilestonePayload, createEmptyMilestoneForm, createEmptyUpdateForm, createMilestoneFormFromRecord, type MilestoneEditorState, type MilestoneFormState, nullableTrimmedText, type ProjectUpdateErrorStore, type ProjectUpdateFormState, type ProjectUpdateFormStore } from '../components/projects/projectDetailShared';
import { ProjectForm } from '../components/projects/ProjectForm';
import { ProjectHeaderFields } from '../components/projects/ProjectHeaderFields';
import { ProjectIterationsTab } from '../components/projects/ProjectIterationsTab';
import { ProjectReleasesTab } from '../components/projects/ProjectReleasesTab';
import { ProjectRequestsTab } from '../components/projects/ProjectRequestsTab';
import { ProjectSummaryTab } from '../components/projects/ProjectSummaryTab';
import { ProjectTasksTab } from '../components/projects/ProjectTasksTab';
import { ProjectUpdatesTab } from '../components/projects/ProjectUpdatesTab';
import { ReleaseForm } from '../components/releases/ReleaseForm';
import {
    PageHeader,
    PageLayout,
    SlideOverDrawer
} from '../components/ui';
import type { MutationFeedbackMeta } from '../features/mutationFeedback';
import { feedbackMessage } from '../features/mutationFeedback';
import { planningInputService, type ObservedPlanningInput } from '../services/planningInputService';
import { projectService } from '../services/projectService';
import { releaseService } from '../services/releaseService';
import type {
    Project, ProjectMilestone,
    ProjectMilestoneCreateRequest, ProjectMilestoneUpdateRequest
} from '../types/project';
import { getApiErrorMessage, getApiErrorStatus, normalizeApiError } from '../utils/apiError';


const ProjectDetailPage = () => {
    const { projectId } = useParams();
    const navigate = useNavigate();
    const { t } = useTranslation();
    const queryClient = useQueryClient();
    const numericProjectId = Number(projectId);
    // The roadmap links here with ?action=edit or ?action=add-milestone.
    const [searchParams, setSearchParams] = useSearchParams();
    const projectTabs = ['summary', 'tasks', 'iterations', 'releases', 'requests', 'updates'] as const;
    const activeTab = projectTabs.find(tab => tab === searchParams.get('tab')) ?? 'summary';
    const tabSearch = (tab: typeof projectTabs[number]) => {
        const next = new URLSearchParams(searchParams);
        next.delete('action');
        next.set('tab', tab);
        return `?${next}`;
    };
    const requestedAction = searchParams.get('action');
    const [isEditing, setIsEditing] = useState(requestedAction === 'edit');
    const [showCreateRelease, setShowCreateRelease] = useState(false);
    const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
    const [showDetachConfirm, setShowDetachConfirm] = useState(false);
    const [deleteContext, setDeleteContext] = useState<ObservedPlanningInput<Project> | null>(null);
    const [deleteError, setDeleteError] = useState<string | null>(null);
    const [milestoneEditor, setMilestoneEditor] = useState<MilestoneEditorState | null>(null);
    const [deleteMilestoneTarget, setDeleteMilestoneTarget] = useState<ProjectMilestone | null>(null);
    const [milestoneActionError, setMilestoneActionError] = useState<string | null>(null);
    const [updateFormStore, setUpdateFormStore] = useState<ProjectUpdateFormStore>(() => ({
        projectId: null,
        form: createEmptyUpdateForm('unknown'),
    }));
    const [updateErrorStore, setUpdateErrorStore] = useState<ProjectUpdateErrorStore>({
        projectId: null,
        message: null,
    });
    const [postUpdateOpen, setPostUpdateOpen] = useState(false);
    const toast = useToast();

    const enabled = Number.isInteger(numericProjectId) && numericProjectId > 0;

    const { data: project, isLoading: isProjectLoading, error: projectError, refetch: refetchProject } = useQuery({
        queryKey: ['project', numericProjectId],
        queryFn: () => projectService.getById(numericProjectId),
        enabled,
    });

    const { data: summary, error: summaryError, refetch: refetchSummary } = useQuery({
        queryKey: ['projectSummary', numericProjectId],
        queryFn: () => projectService.getSummary(numericProjectId),
        enabled,
    });

    const { data: projectMilestones = [], isLoading: areMilestonesLoading, error: milestonesError, refetch: refetchMilestones } = useQuery({
        queryKey: ['projectMilestones', numericProjectId],
        queryFn: () => projectService.getMilestones(numericProjectId),
        enabled,
    });

    const { data: tasks = [], isLoading: areTasksLoading, error: tasksError, refetch: refetchTasks } = useQuery({
        queryKey: ['projectTasks', numericProjectId],
        queryFn: () => projectService.getTasks(numericProjectId),
        enabled,
    });

    const { data: projectUpdates = [], isLoading: areUpdatesLoading, error: updatesError, refetch: refetchUpdates } = useQuery({
        queryKey: ['projectUpdates', numericProjectId],
        queryFn: () => projectService.getUpdates(numericProjectId),
        enabled,
    });

    const { data: projectReleases = [], isLoading: areReleasesLoading, error: releasesError, refetch: refetchReleases } = useQuery({
        queryKey: ['projectReleases', numericProjectId],
        queryFn: () => releaseService.getForProject(numericProjectId),
        enabled,
    });

    const { data: projectIterations = [], isLoading: areProjectIterationsLoading, error: iterationsError, refetch: refetchIterations } = useQuery({
        queryKey: ['projectIterations', numericProjectId],
        queryFn: () => projectService.getIterations(numericProjectId),
        enabled,
    });

    const updateForm = updateFormStore.projectId === numericProjectId
        ? updateFormStore.form
        : createEmptyUpdateForm(project?.health ?? 'unknown');
    const updateError = updateErrorStore.projectId === numericProjectId
        ? updateErrorStore.message
        : null;

    const invalidateAfterDelete = () => {
        queryClient.invalidateQueries({ queryKey: ['projects'] });
        queryClient.invalidateQueries({ queryKey: ['project', numericProjectId] });
        queryClient.invalidateQueries({ queryKey: ['projectSummary', numericProjectId] });
        queryClient.invalidateQueries({ queryKey: ['projectTasks', numericProjectId] });
        queryClient.invalidateQueries({ queryKey: ['projectReleases', numericProjectId] });
        queryClient.invalidateQueries({ queryKey: ['projectIterations', numericProjectId] });
        queryClient.invalidateQueries({ queryKey: ['tasks'] });
        queryClient.invalidateQueries({ queryKey: ['gantt'] });
    };

    const invalidateProjectRequestLinks = () => {
        queryClient.invalidateQueries({ queryKey: ['projects'] });
        queryClient.invalidateQueries({ queryKey: ['project', numericProjectId] });
        queryClient.invalidateQueries({ queryKey: ['projectSummary', numericProjectId] });
    };

    const invalidateProjectMilestones = () => {
        queryClient.invalidateQueries({ queryKey: ['projects'] });
        queryClient.invalidateQueries({ queryKey: ['project', numericProjectId] });
        queryClient.invalidateQueries({ queryKey: ['projectMilestones'] });
        queryClient.invalidateQueries({ queryKey: ['projectSummary', numericProjectId] });
        queryClient.invalidateQueries({ queryKey: ['projectTasks', numericProjectId] });
        queryClient.invalidateQueries({ queryKey: ['tasks'] });
        queryClient.invalidateQueries({ queryKey: ['gantt'] });
    };

    const observeDelete = async (open = true) => {
        try {
            const observed = await planningInputService.readInitial<Project>('project', numericProjectId);
            setDeleteContext(observed); setDeleteError(null);
            if(open) setShowDeleteConfirm(true);
        } catch(cause) { setDeleteError(getApiErrorMessage(cause, t('surfaces.projectDetail.deleteProjectFailed'))); }
    };

    const deleteMutation = useMutation({
        mutationFn: (detachTasks: boolean) => projectService.delete(numericProjectId, deleteContext!.expected_revisions, detachTasks),
        meta: { success: () => feedbackMessage(t, 'deleted', 'project', project?.name) } satisfies MutationFeedbackMeta,
        onSuccess: () => {
            invalidateAfterDelete();
            navigate('/projects');
        },
        onError: (err: unknown) => {
            if (getApiErrorStatus(err) === 409 && normalizeApiError(err, '').code === 'project_has_tasks') {
                setShowDeleteConfirm(false);
                setShowDetachConfirm(true);
                setDeleteError(null);
            } else {
                setDeleteError(getApiErrorMessage(err, t('surfaces.projectDetail.deleteProjectFailed')));
            }
        },
    });

    const createMilestoneMutation = useMutation({
        mutationFn: (data: ProjectMilestoneCreateRequest) => projectService.createMilestone(numericProjectId, data),
        meta: {
            success: data => feedbackMessage(t, 'created', 'milestone', (data as ProjectMilestone).name),
            // A milestone just created can be removed again.
            undo: data => ({ run: () => projectService.deleteMilestone(numericProjectId, (data as ProjectMilestone).id) }),
        } satisfies MutationFeedbackMeta,
        onSuccess: () => {
            setMilestoneEditor(null);
            setMilestoneActionError(null);
            invalidateProjectMilestones();
        },
        onError: (err: unknown) => {
            setMilestoneEditor(previous => previous
                ? { ...previous, error: getApiErrorMessage(err, t('surfaces.projectDetail.createMilestoneFailed')) }
                : previous);
        },
    });

    const updateMilestoneMutation = useMutation({
        mutationFn: ({ milestoneId, data }: { milestoneId: number; data: ProjectMilestoneUpdateRequest }) => (
            projectService.updateMilestone(numericProjectId, milestoneId, data)
        ),
        meta: { success: data => feedbackMessage(t, 'saved', 'milestone', (data as ProjectMilestone).name) } satisfies MutationFeedbackMeta,
        onSuccess: () => {
            setMilestoneEditor(null);
            setMilestoneActionError(null);
            invalidateProjectMilestones();
        },
        onError: (err: unknown) => {
            const message = getApiErrorMessage(err, t('surfaces.projectDetail.updateMilestoneFailed'));
            setMilestoneEditor(previous => previous ? { ...previous, error: message } : previous);
            setMilestoneActionError(message);
        },
    });

    const deleteMilestoneMutation = useMutation({
        mutationFn: (milestoneId: number) => projectService.deleteMilestone(numericProjectId, milestoneId),
        meta: { success: () => feedbackMessage(t, 'deleted', 'milestone', deleteMilestoneTarget?.name) } satisfies MutationFeedbackMeta,
        onSuccess: () => {
            setDeleteMilestoneTarget(null);
            setMilestoneActionError(null);
            invalidateProjectMilestones();
        },
        onError: (err: unknown) => {
            setMilestoneActionError(getApiErrorMessage(err, t('surfaces.projectDetail.deleteMilestoneFailed')));
        },
    });

    const reorderMilestoneMutation = useMutation({
        mutationFn: async ({ milestoneId, direction }: { milestoneId: number; direction: -1 | 1 }) => {
            const currentIndex = projectMilestones.findIndex(milestone => milestone.id === milestoneId);
            const nextIndex = currentIndex + direction;
            if (currentIndex < 0 || nextIndex < 0 || nextIndex >= projectMilestones.length) return;

            const reordered = [...projectMilestones];
            [reordered[currentIndex], reordered[nextIndex]] = [reordered[nextIndex], reordered[currentIndex]];
            await Promise.all(reordered.map((milestone, index) => (
                projectService.updateMilestone(
                    numericProjectId,
                    milestone.id,
                    { sort_order: (index + 1) * 10 },
                )
            )));
        },
        onSuccess: () => {
            setMilestoneActionError(null);
            invalidateProjectMilestones();
        },
        onError: (err: unknown) => {
            setMilestoneActionError(getApiErrorMessage(err, t('surfaces.projectDetail.reorderMilestonesFailed')));
        },
    });

    const createUpdateMutation = useMutation({
        mutationFn: () => projectService.createUpdate(numericProjectId, {
            health: updateForm.health,
            summary: updateForm.summary.trim(),
            progress_text: nullableTrimmedText(updateForm.progress_text),
            risks_text: nullableTrimmedText(updateForm.risks_text),
            decisions_text: nullableTrimmedText(updateForm.decisions_text),
            next_steps_text: nullableTrimmedText(updateForm.next_steps_text),
        }),
        onSuccess: (update) => {
            setUpdateFormStore({
                projectId: numericProjectId,
                form: createEmptyUpdateForm(update.health),
            });
            setUpdateErrorStore({ projectId: numericProjectId, message: null });
            queryClient.invalidateQueries({ queryKey: ['projects'] });
            queryClient.invalidateQueries({ queryKey: ['project', numericProjectId] });
            queryClient.invalidateQueries({ queryKey: ['projectSummary', numericProjectId] });
            queryClient.invalidateQueries({ queryKey: ['projectUpdates', numericProjectId] });
            setPostUpdateOpen(false);
            toast.success(t('surfaces.projectDetail.updatePosted'));
        },
        onError: (err: unknown) => {
            setUpdateErrorStore({
                projectId: numericProjectId,
                message: getApiErrorMessage(err, t('surfaces.projectDetail.postUpdateFailed')),
            });
        },
    });

    const handleCreateUpdate = (event: FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        if(!updateForm.summary.trim() || createUpdateMutation.isPending) return;
        setUpdateErrorStore({ projectId: numericProjectId, message: null });
        createUpdateMutation.mutate();
    };

    const setUpdateField = <K extends keyof ProjectUpdateFormState>(
        field: K,
        value: ProjectUpdateFormState[K],
    ) => {
        setUpdateFormStore(previous => {
            const currentForm = previous.projectId === numericProjectId
                ? previous.form
                : createEmptyUpdateForm(project?.health ?? 'unknown');

            return {
                projectId: numericProjectId,
                form: { ...currentForm, [field]: value },
            };
        });
        if(updateError) {
            setUpdateErrorStore({ projectId: numericProjectId, message: null });
        }
    };

    const nextMilestoneSortOrder = projectMilestones.length
        ? Math.max(...projectMilestones.map(milestone => milestone.sort_order)) + 10
        : 10;

    const openCreateMilestone = () => {
        setMilestoneActionError(null);
        setMilestoneEditor({
            mode: 'create',
            milestone: null,
            form: createEmptyMilestoneForm(nextMilestoneSortOrder),
            error: null,
        });
    };

    const [handledAction, setHandledAction] = useState<string | null>(null);
    if(requestedAction && handledAction !== requestedAction) {
        setHandledAction(requestedAction);
        if(requestedAction === 'edit') setIsEditing(true);
        if(requestedAction === 'add-milestone') openCreateMilestone();
    }
    if(!requestedAction && handledAction) setHandledAction(null);
    useEffect(() => {
        if(!requestedAction) return;
        const next = new URLSearchParams(searchParams);
        next.delete('action');
        if(requestedAction === 'add-milestone') next.set('tab', 'summary');
        setSearchParams(next, { replace: true });
    }, [requestedAction, searchParams, setSearchParams]);

    const openEditMilestone = (milestone: ProjectMilestone) => {
        setMilestoneActionError(null);
        setMilestoneEditor({
            mode: 'edit',
            milestone,
            form: createMilestoneFormFromRecord(milestone),
            error: null,
        });
    };

    const setMilestoneField = <K extends keyof MilestoneFormState>(
        field: K,
        value: MilestoneFormState[K],
    ) => {
        setMilestoneEditor(previous => previous
            ? {
                ...previous,
                form: { ...previous.form, [field]: value },
                error: null,
            }
            : previous);
    };

    const handleSaveMilestone = (event: FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        if(!milestoneEditor || !milestoneEditor.form.name.trim()) return;

        const payload = buildMilestonePayload(milestoneEditor.form);
        if(milestoneEditor.mode === 'create') {
            createMilestoneMutation.mutate(payload as ProjectMilestoneCreateRequest);
            return;
        }

        if(milestoneEditor.milestone) {
            updateMilestoneMutation.mutate({
                milestoneId: milestoneEditor.milestone.id,
                data: payload,
            });
        }
    };

    const completeMilestone = (milestone: ProjectMilestone) => {
        updateMilestoneMutation.mutate({
            milestoneId: milestone.id,
            data: { status: 'completed' },
        });
    };

    const cancelMilestone = (milestone: ProjectMilestone) => {
        updateMilestoneMutation.mutate({
            milestoneId: milestone.id,
            data: { status: 'canceled', completed_at: null },
        });
    };

    const isMilestoneActionPending = (
        createMilestoneMutation.isPending
        || updateMilestoneMutation.isPending
        || deleteMilestoneMutation.isPending
        || reorderMilestoneMutation.isPending
    );

    if(!enabled) {
        return <PageLayout><PageHeader title={t('surfaces.projectDetail.projectNotFound')} purpose={t('surfaces.projectDetail.missingPurpose')} primaryAction={<Button onClick={() => navigate('/projects')}>{t('surfaces.projectDetail.backToProjects')}</Button>} /></PageLayout>;
    }

    if(isProjectLoading) {
        return (
            <div className="py-20 text-center text-content-secondary">
                <Activity className="mx-auto mb-2 h-5 w-5 animate-pulse" />
                {t('surfaces.projectDetail.loadingProject')}
            </div>
        );
    }

    const projectQueryError = projectError
        ?? summaryError
        ?? milestonesError
        ?? tasksError
        ?? updatesError
        ?? releasesError
        ?? iterationsError;

    if(projectQueryError) {
        return (
            <QueryErrorState
                error={projectQueryError}
                onRetry={() => {
                    void refetchProject();
                    void refetchSummary();
                    void refetchMilestones();
                    void refetchTasks();
                    void refetchUpdates();
                    void refetchReleases();
                    void refetchIterations();
                }}
            />
        );
    }

    if(!project) {
        return <PageLayout><PageHeader title={t('surfaces.projectDetail.projectNotFound')} purpose={t('surfaces.projectDetail.missingPurpose')} primaryAction={<Button onClick={() => navigate('/projects')}>{t('surfaces.projectDetail.backToProjects')}</Button>} /></PageLayout>;
    }

    return (
        <PageLayout>
            <Breadcrumbs items={[
                { label: t('breadcrumbs.projects'), path: '/projects' },
                { label: project.name },
            ]} />

            <PageHeader
                title={project.name}
                purpose={t('projectTabs.purpose')}
                meta={<ProjectHeaderFields key={project.id} project={project} />}
                primaryAction={<Button onClick={() => setPostUpdateOpen(true)}><Send className="mr-2 h-4 w-4" />{t('surfaces.projectDetail.postUpdate')}</Button>}
                secondaryActions={<Button variant="secondary" onClick={() => setIsEditing(true)}><Edit className="mr-2 h-4 w-4" />{t('surfaces.projectDetail.edit')}</Button>}
                overflowItems={[{ label: t('surfaces.projectDetail.deleteProject'), icon: <Trash2 className="h-3.5 w-3.5" />, tone: 'danger', onSelect: () => void observeDelete() }]}
            />
            {deleteError && !showDeleteConfirm && !showDetachConfirm && <p role="alert" className="text-feedback-danger-foreground">{deleteError}</p>}
            <div aria-label={t('projectTabs.navigation')} className="flex flex-wrap gap-1 border-b border-border" role="tablist" tabIndex={-1} onKeyDown={event => {
                const offset = event.key === 'ArrowRight' ? 1 : event.key === 'ArrowLeft' ? -1 : 0;
                if(!offset && event.key !== 'Home' && event.key !== 'End') return;
                event.preventDefault();
                const index = event.key === 'Home' ? 0 : event.key === 'End' ? projectTabs.length - 1 : (projectTabs.indexOf(activeTab) + offset + projectTabs.length) % projectTabs.length;
                const tab = projectTabs[index];
                setSearchParams(tabSearch(tab));
                document.getElementById(`project-tab-${tab}`)?.focus();
            }}>
                {projectTabs.map(tab => (
                    <Link key={tab} id={`project-tab-${tab}`} role="tab" tabIndex={activeTab === tab ? 0 : -1} aria-selected={activeTab === tab}
                        aria-controls={`project-panel-${tab}`} to={{ search: tabSearch(tab) }}
                        className={clsx('border-b-2 px-4 py-3 text-sm font-medium focus-visible:outline focus-visible:outline-2 focus-visible:outline-action', activeTab === tab ? 'border-action text-action' : 'border-transparent text-content-secondary hover:bg-surface-muted')}
                    >{t(`projectTabs.${tab}`)}</Link>
                ))}
            </div>
            <div role="tabpanel" id={`project-panel-${activeTab}`} aria-labelledby={`project-tab-${activeTab}`}>
                {activeTab === 'summary' && <ProjectSummaryTab project={project} summary={summary} updates={projectUpdates} onPostUpdate={() => setPostUpdateOpen(true)} milestones={{
                    milestones: projectMilestones, groups: summary?.milestone_groups ?? [], isLoading: areMilestonesLoading,
                    isActionPending: isMilestoneActionPending, actionError: milestoneActionError, onCreate: openCreateMilestone,
                    onEdit: openEditMilestone, onComplete: completeMilestone, onCancel: cancelMilestone,
                    onDelete: setDeleteMilestoneTarget, onMove: (milestoneId, direction) => reorderMilestoneMutation.mutate({ milestoneId, direction }),
                }} />}
                {activeTab === 'tasks' && <ProjectTasksTab projectId={numericProjectId} tasks={tasks} summary={summary} isLoading={areTasksLoading} />}
                {activeTab === 'iterations' && <ProjectIterationsTab projectId={numericProjectId} projectName={project.name} iterations={projectIterations} isLoading={areProjectIterationsLoading} />}
                {activeTab === 'releases' && <ProjectReleasesTab releases={projectReleases} isLoading={areReleasesLoading} onCreate={() => setShowCreateRelease(true)} />}
                {activeTab === 'requests' && <ProjectRequestsTab projectId={numericProjectId} count={summary?.request_count ?? 0} onChanged={invalidateProjectRequestLinks} />}
                {activeTab === 'updates' && <ProjectUpdatesTab projectId={numericProjectId} updates={projectUpdates} isLoading={areUpdatesLoading} />}
            </div>


            <PostUpdateDrawer
                open={postUpdateOpen}
                onClose={() => setPostUpdateOpen(false)}
                form={updateForm}
                error={updateError}
                isPending={createUpdateMutation.isPending}
                setField={setUpdateField}
                onSubmit={handleCreateUpdate}
                onDismissError={() => setUpdateErrorStore({ projectId: numericProjectId, message: null })}
                summaryIsBlank={!updateForm.summary.trim()}
                projectName={project.name}
            />

            <SlideOverDrawer open={showCreateRelease} title={t('surfaces.projectDetail.createRelease')} closeLabel={t('actions.close')} onClose={() => setShowCreateRelease(false)} className="max-w-3xl">
                <div className="p-5">{showCreateRelease && (
                    <ReleaseForm
                        projectId={numericProjectId}
                        onSuccess={(release) => {
                            setShowCreateRelease(false);
                            navigate(`/projects/${numericProjectId}/releases/${release.id}`);
                        }}
                        onCancel={() => setShowCreateRelease(false)}
                    />
                )}</div>
            </SlideOverDrawer>

            <SlideOverDrawer open={isEditing} title={t('surfaces.projectDetail.editProject')} closeLabel={t('actions.close')} onClose={() => setIsEditing(false)}>
                <div className="p-5">{isEditing && (
                    <ProjectForm
                        initialData={project}
                        onSuccess={() => setIsEditing(false)}
                        onCancel={() => setIsEditing(false)}
                    />
                )}</div>
            </SlideOverDrawer>

            {milestoneEditor && (
                <MilestoneFormDrawer
                    mode={milestoneEditor.mode}
                    form={milestoneEditor.form}
                    error={milestoneEditor.error}
                    isSaving={createMilestoneMutation.isPending || updateMilestoneMutation.isPending}
                    onChange={setMilestoneField}
                    onSubmit={handleSaveMilestone}
                    onCancel={() => setMilestoneEditor(null)}
                />
            )}

            <ConfirmDialog
                open={deleteMilestoneTarget !== null}
                title={t('surfaces.projectDetail.deleteMilestone')}
                description={<strong>{deleteMilestoneTarget?.name}</strong>}
                confirmLabel={t('surfaces.projectDetail.deleteMilestone')}
                cancelLabel={t('surfaces.projectDetail.cancel')}
                closeLabel={t('actions.close')}
                pending={deleteMilestoneMutation.isPending}
                onCancel={() => setDeleteMilestoneTarget(null)}
                onConfirm={() => { if(deleteMilestoneTarget) deleteMilestoneMutation.mutate(deleteMilestoneTarget.id); }}
            />

            <ConfirmDialog
                open={showDeleteConfirm && deleteContext?.resource_id === numericProjectId}
                title={t('surfaces.projectDetail.deleteProjectText')}
                description={<><strong>{project.name}</strong>{deleteError && <span role="alert" className="mt-2 block text-feedback-danger-foreground">{deleteError}<Button type="button" variant="secondary" disabled={deleteMutation.isPending} onClick={() => void observeDelete(false)}>{t('planningInput.reviewAgain')}</Button></span>}</>}
                confirmLabel={t('surfaces.projectDetail.delete')}
                cancelLabel={t('surfaces.projectDetail.cancel')}
                closeLabel={t('actions.close')}
                pending={deleteMutation.isPending}
                onCancel={() => setShowDeleteConfirm(false)}
                onConfirm={() => { if(deleteContext?.resource_id === numericProjectId) deleteMutation.mutate(false); }}
            />

            <ConfirmDialog
                open={showDetachConfirm && deleteContext?.resource_id === numericProjectId}
                title={t('surfaces.projectDetail.detachTasks')}
                description={<>{t('surfaces.projectDetail.detachDescription', { project: deleteContext?.resource.name ?? project.name })}{deleteError && <span role="alert">{deleteError}<Button type="button" variant="secondary" disabled={deleteMutation.isPending} onClick={() => void observeDelete(false)}>{t('planningInput.reviewAgain')}</Button></span>}</>}
                confirmLabel={t('surfaces.projectDetail.detachAndDelete')}
                cancelLabel={t('surfaces.projectDetail.cancel')}
                closeLabel={t('actions.close')}
                pending={deleteMutation.isPending}
                onCancel={() => setShowDetachConfirm(false)}
                onConfirm={() => { if(deleteContext?.resource_id === numericProjectId) deleteMutation.mutate(true); }}
            />
        </PageLayout>
    );
};

export default ProjectDetailPage;

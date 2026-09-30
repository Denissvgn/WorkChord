import { DeliveryDependencies } from './DeliveryDependencies';
import { PersonCapacity } from './PersonCapacity';
import { TaskDiscussion } from './TaskDiscussion';
import { useCallback, useEffect, useId, useMemo, useState } from 'react';
import { useMutation, useQueryClient, useQuery } from '@tanstack/react-query';
import { Inbox, Save, Sparkles } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { Button } from '../common/Button';
import { ConfirmDialog } from '../common/ConfirmDialog';
import { QueryErrorState } from '../feedback/QueryState';
import { Input } from '../common/Input';
import { CollapsibleSection } from '../common/CollapsibleSection';
import { LabelSelector } from '../labels/LabelSelector';
import { taskService } from '../../services/taskService';
import { templateService } from '../../services/templateService';
import { triageService } from '../../services/triageService';
import { teamService } from '../../services/teamService';
import { projectService } from '../../services/projectService';
import { iterationService } from '../../services/iterationService';
import { TaskDependencySelector } from './TaskDependencySelector';
import { TaskAgentReadinessBadge } from './TaskAgentReadinessBadge';
import { StatusChangeControl } from './StatusChangeControl';
import { TaskBriefEditor } from './TaskBriefEditor';
import { TaskWorkPanel } from './TaskWorkPanel';
import { emptyTaskBrief, newCriterion } from './taskEditorContract';
import { TaskTimelinePanel } from './TaskTimelinePanel';
import { AssigneeRecommendationsPanel } from '../team/AssigneeRecommendationsPanel';
import { getApiErrorMessage } from '../../utils/apiError';
import {
    getPayloadBoolean,
    getPayloadString,
    mergeLabels,
} from '../../utils/templateDefaults';
import type { GroundedAISuggestionResponse, TaskAISuggestRequest, TaskCreate, Task } from '../../types/task';
import type { WorkTemplate } from '../../types/template';
import type { TriageItemCreate } from '../../types/triage';
import { templateDisplay } from '../../i18n/seedDisplay';
import {
    buildTaskEditorDefaults,
    mapTaskEditorServerError,
    toTaskCreate,
    toTaskUpdate,
    validateTaskEditor,
    type TaskConflictMetadata,
    type TaskEditorValues,
} from './taskEditorContract';
import type { TaskUpdate } from '../../types/task';
import { formatDate } from '../../utils/formatDate';
import { useIdentity } from '../../features/identity/identityContext';
import { readTaskDraft, writeTaskDraft, removeTaskDraft } from './taskDraftStorage';

interface TaskFormProps {
    iterationId: number | null;
    initialData?: Task;
    parentId?: number | null;
    parentPriority?: number;
    parentProjectId?: number | null;
    parentMilestoneId?: number | null;
    onSuccess: () => void;
    onCancel: () => void;
    mode?: 'direct' | 'sandbox';
    onSaveSandbox?: (update: TaskUpdate) => void;
    onDirtyChange?: (dirty: boolean) => void;
    onPendingChange?: (pending: boolean) => void;
    onDiscardReady?: (handler: (() => void) | null) => void;
    confirmUnsavedOnCancel?: boolean;
}

export const TaskForm = ({
    iterationId: requestedIterationId,
    initialData,
    parentId,
    parentPriority,
    parentProjectId,
    parentMilestoneId,
    onSuccess,
    onCancel,
    mode = 'direct',
    onSaveSandbox,
    onDirtyChange,
    onPendingChange,
    onDiscardReady,
    confirmUnsavedOnCancel = true,
}: TaskFormProps) => {
    const { t } = useTranslation();
    const formId = useId();
    const identity = useIdentity();
    const [currentTask, setCurrentTask] = useState(initialData);
    const iterationId = currentTask ? currentTask.iteration_id : requestedIterationId;
    const sessionUnavailable = identity?.identity?.mode === "managed" && !identity.identity.authenticated;
    const draftScope = identity?.identity?.principal?.id ?? (identity?.identity?.mode === 'trusted_local' ? 'local' : null);
    const draftKey = draftScope === null ? null : `workchord-draft:${draftScope}:${mode}:${iterationId}:${parentProjectId ?? initialData?.project_id ?? "none"}:${initialData?.id ?? `new-${parentId ?? 'root'}`}`;
    const queryClient = useQueryClient();
    const [error, setError] = useState<string | null>(null);
    const [statusMessage, setStatusMessage] = useState<string | null>(null);
    const [aiContext, setAiContext] = useState('');
    const [aiSuggestion, setAiSuggestion] = useState<GroundedAISuggestionResponse | null>(null);
    const [selectedTemplateId, setSelectedTemplateId] = useState('');
    const [conflict, setConflict] = useState<TaskConflictMetadata | null>(null);
    const [conflictTask, setConflictTask] = useState<Task | null>(null);
    const [isRefreshing, setIsRefreshing] = useState(false);
    const [statusPending, setStatusPending] = useState(false);
    const [workDirty, setWorkDirty] = useState(false);
    const [discussionDirty, setDiscussionDirty] = useState(false);
    const [showAssistant, setShowAssistant] = useState(false);
    const [showDiscardWarning, setShowDiscardWarning] = useState(false);
    const canApplyTemplates = !currentTask && mode === 'direct';
    const canSendToTriage = !currentTask && !parentId && mode === 'direct';
    const initialValues = useMemo(() => buildTaskEditorDefaults({
        task: initialData,
        parentId,
        parentPriority,
        parentProjectId,
        parentMilestoneId,
    }), [initialData, parentId, parentPriority, parentProjectId, parentMilestoneId]);
    const [recoveredDraft] = useState(() => readTaskDraft(draftKey, initialValues));
    const [formData, setFormData] = useState<TaskEditorValues>(() => recoveredDraft ?? initialValues);
    const [baseline, setBaseline] = useState<TaskEditorValues>(() => initialValues);
    const isDirty = JSON.stringify(formData) !== JSON.stringify(baseline);
    const clearDraft = useCallback(() => removeTaskDraft(draftKey, true), [draftKey]);
    useEffect(() => {
        onDiscardReady?.(clearDraft);
        return () => onDiscardReady?.(null);
    }, [onDiscardReady, clearDraft]);
    useEffect(() => {
        if (isDirty) writeTaskDraft(draftKey, formData);
        else removeTaskDraft(draftKey);
    }, [draftKey, formData, isDirty]);

    useEffect(() => {
        onDirtyChange?.(isDirty || workDirty || discussionDirty);
    }, [isDirty, workDirty, discussionDirty, onDirtyChange]);

    // Fetch team for assignee dropdown
    const { data: teamMembers, error: teamError, refetch: refetchTeam } = useQuery({
        queryKey: ['team', iterationId],
        queryFn: () => teamService.getByIteration(iterationId!),
        enabled: iterationId !== null,
    });

    const { data: iteration, error: iterationError, refetch: refetchIteration } = useQuery({
        queryKey: ['iteration', iterationId],
        queryFn: () => iterationService.getById(iterationId!),
        enabled: iterationId !== null,
    });

    const { data: projects = [], error: projectsError, refetch: refetchProjects } = useQuery({
        queryKey: ['projects'],
        queryFn: projectService.getAll,
    });

    const dayHours = currentTask?.nominal_day_hours ?? iteration?.nominal_day_hours ?? 8;
    const scopedProjectId = iteration?.project_id ?? null;
    const scopedProject = iteration?.project ?? null;
    const effectiveProjectId = scopedProjectId ?? formData.project_id ?? null;

    const selectedProjectId = effectiveProjectId;
    const owners = useQuery({
        queryKey: ['taskOwnerOptions', selectedProjectId], queryFn: () => taskService.ownerOptions(selectedProjectId ?? undefined),
        enabled: selectedProjectId !== null || Boolean(iteration && iteration.project_id === null),
        // feedback-policy: query loading,error,retry,empty
    });
    const { data: projectMilestones = [], isFetched: milestonesFetched, error: milestonesError, refetch: refetchMilestones } = useQuery({
        queryKey: ['projectMilestones', selectedProjectId],
        queryFn: () => projectService.getMilestones(selectedProjectId!),
        enabled: selectedProjectId !== null,
    });
    const milestoneBelongsToSelectedProject = !formData.milestone_id
        || !milestonesFetched
        || projectMilestones.some(milestone => milestone.id === formData.milestone_id);
    const effectiveMilestoneId = effectiveProjectId && milestoneBelongsToSelectedProject
        ? formData.milestone_id ?? null
        : null;

    const { data: taskTemplates = [], error: templatesError, refetch: refetchTemplates } = useQuery({
        queryKey: ['templates', 'task'],
        queryFn: () => templateService.getAll({ template_type: 'task' }),
        enabled: canApplyTemplates,
    });

    const invalidateTaskProjectQueries = () => {
        queryClient.invalidateQueries({ queryKey: ['tasks', iterationId] });
        queryClient.invalidateQueries({ queryKey: ['taskEditor'] });
        queryClient.invalidateQueries({ queryKey: ['taskContext'] });
        queryClient.invalidateQueries({ queryKey: ['workload'] });
        queryClient.invalidateQueries({ queryKey: ['gantt'] });
        queryClient.invalidateQueries({ queryKey: ['projects'] });
        queryClient.invalidateQueries({ queryKey: ['projectSummary'] });
        queryClient.invalidateQueries({ queryKey: ['projectTasks'] });
    };

    const createMutation = useMutation({
        mutationFn: (data: TaskCreate) => taskService.create(iterationId, { ...data, expected_revision: iteration?.revision }),
        onSuccess: () => {
            clearDraft();
            invalidateTaskProjectQueries();
            onSuccess();
        },
        onError: (err: unknown) => {
            setError(getApiErrorMessage(err, t('surfaces.taskForm.createFailed')));
        },
    });

    const createTriageMutation = useMutation({
        mutationFn: (data: TriageItemCreate) => triageService.create(data),
        onSuccess: () => {
            clearDraft();
            queryClient.invalidateQueries({ queryKey: ['triage'] });
            onSuccess();
        },
        onError: (err: unknown) => {
            setError(getApiErrorMessage(err, t('surfaces.taskForm.createTriageFailed')));
        },
    });

    const updateMutation = useMutation({
        mutationFn: (data: TaskUpdate) => taskService.update(currentTask!.id, data),
        onSuccess: () => {
            clearDraft();
            invalidateTaskProjectQueries();
            onSuccess();
        },
        onError: (err: unknown) => {
            const mapped = mapTaskEditorServerError(err, t('taskEditor.updateFailed'));
            if (mapped.kind === 'version-conflict') {
                setConflict(mapped.currentTask);
                void taskService.getById(currentTask!.id).then(setConflictTask).catch(() => setConflictTask(null));
                setError(null);
                return;
            }
            setError(mapped.message);
        },
    });
    const isSubmitting = createMutation.isPending || updateMutation.isPending || createTriageMutation.isPending || statusPending || isRefreshing;
    useEffect(() => { onPendingChange?.(isSubmitting); }, [isSubmitting, onPendingChange]);

    const handleStatusPending = useCallback((value: boolean) => {
        if (value) onPendingChange?.(true);
        setStatusPending(value);
    }, [onPendingChange]);

    const reloadCurrentTask = async () => {
        if (!currentTask || isSubmitting) return;
        setIsRefreshing(true);
        onPendingChange?.(true);
        try {
            const latest = await taskService.getById(currentTask.id);
            const latestValues = buildTaskEditorDefaults({ task: latest });
            setCurrentTask(latest);
            setFormData(latestValues);
            setBaseline(latestValues);
            setConflict(null);
            setError(null);
            setStatusMessage(t('taskEditor.reloaded'));
            invalidateTaskProjectQueries();
        } catch (err: unknown) {
            setError(getApiErrorMessage(err, t('taskEditor.reloadFailed')));
        } finally { setIsRefreshing(false); }
    };

    const compareCurrentTask = async () => {
        if (!currentTask || isSubmitting) return;
        setIsRefreshing(true);
        onPendingChange?.(true);
        try {
            const latest = await taskService.getById(currentTask.id);
            setCurrentTask(latest);
            setBaseline(buildTaskEditorDefaults({ task: latest }));
            setFormData(values => ({ ...values, expected_version: latest.version,
                brief: values.brief ? { ...values.brief, acceptance_criteria: values.brief.acceptance_criteria.map(criterion => ({ ...criterion,
                    revision: latest.brief?.acceptance_criteria.find(current => current.id === criterion.id)?.revision ?? 1 })) } : null }));
            setConflict(null);
            setStatusMessage(t('taskEditor.reapplyReady'));
        } catch (cause) { setError(getApiErrorMessage(cause, t('taskEditor.reloadFailed'))); }
        finally { setIsRefreshing(false); }
    };

    const buildAISuggestPayload = (): TaskAISuggestRequest => ({
        brief: formData.brief,
        title: formData.title,
        description: formData.description ?? null,
        priority: formData.priority,
        effort_days: formData.effort_days,
        effort_hours: formData.effort_hours,
        assignee_id: formData.assignee_id ?? null,
        project_id: effectiveProjectId,
        milestone_id: effectiveMilestoneId,
        parent_id: formData.parent_id ?? null,
        depends_on: formData.depends_on ?? [],
        tags: formData.tags ?? [],
        is_optional: formData.is_optional ?? false,
        is_deferred: formData.is_deferred ?? false,
        min_start_date: formData.min_start_date ?? null,
        max_end_date: formData.max_end_date ?? null,
        source: formData.source ?? null,
        source_url: formData.source_url ?? null,
        external_key: formData.external_key ?? null,
        template_id: selectedTemplateId ? Number(selectedTemplateId) : null,
        user_context: aiContext.trim() || null,
        extra_context: {
            project_name: effectiveProjectId
                ? projects.find(project => project.id === effectiveProjectId)?.name ?? scopedProject?.name
                : null,
        },
    });

    const aiSuggestMutation = useMutation({
        mutationFn: () => taskService.suggestWithAI(buildAISuggestPayload(), currentTask?.id),
        onMutate: () => {
            setError(null);
            setStatusMessage(null);
            setAiSuggestion(null);
        },
        onSuccess: (data) => {
            setAiSuggestion(data);
            setStatusMessage(t('taskAi.generated'));
        },
        onError: (err: unknown) => {
            setError(getApiErrorMessage(err, t('taskAi.generateFailed')));
        },
    });

    const appendAcceptanceCriteria = (criteria: string[]) => {
        if (!criteria.length) return;
        setFormData(prev => ({ ...prev, brief: { ...(prev.brief ?? { ...emptyTaskBrief(), context: prev.description }),
            acceptance_criteria: [...(prev.brief?.acceptance_criteria ?? []), ...criteria.map(text => newCriterion(text))] } }));
        setStatusMessage(t('taskAi.criteriaAppended'));
    };

    const applyTaskTemplate = (template: WorkTemplate) => {
        const display = templateDisplay(template);
        const canonical = template.default_payload.brief as import('../../types/task').TaskBrief | undefined;
        setFormData(prev => {
            const effortDays = template.default_effort_days ?? prev.effort_days;
            const source = getPayloadString(template.default_payload, 'source', prev.source ?? null);

            return {
                ...prev,
                title: display.default_title ?? prev.title,
                brief: canonical ? { ...structuredClone(canonical), acceptance_criteria: canonical.acceptance_criteria.map(criterion => ({
                    ...criterion, id: newCriterion().id, revision: 1,
                })) } : { ...emptyTaskBrief(),
                    goal: display.default_title ?? prev.title,
                    context: display.default_description ?? prev.description,
                    acceptance_criteria: display.default_checklist.map(text => newCriterion(text)) },
                priority: template.default_priority ?? prev.priority,
                effort_days: effortDays,
                estimate_provenance: template.default_effort_days != null ? "assumed" : prev.estimate_provenance,
                effort_hours: template.default_effort_days != null
                    ? template.default_effort_days * dayHours
                    : prev.effort_hours,
                tags: mergeLabels(prev.tags ?? [], template.default_labels),
                is_optional: getPayloadBoolean(
                    template.default_payload,
                    'is_optional',
                    prev.is_optional ?? false,
                ),
                is_deferred: getPayloadBoolean(
                    template.default_payload,
                    'is_deferred',
                    prev.is_deferred ?? false,
                ),
                source,
            };
        });
    };

    const handleTemplateSelect = (templateId: string) => {
        setSelectedTemplateId(templateId);
        const template = taskTemplates.find(candidate => String(candidate.id) === templateId);
        if (template) {
            applyTaskTemplate(template);
        }
    };

    const handleProjectChange = (projectId: number | null) => {
        setFormData(prev => ({
            ...prev,
            project_id: projectId,
            milestone_id: projectId === prev.project_id ? prev.milestone_id : null,
        }));
    };

    const handleSubmit = (e: React.FormEvent) => {
        e.preventDefault();
        if (isSubmitting || workDirty || discussionDirty) return;
        setError(null);
        setConflict(null);
        const values = {
            ...formData,
            project_id: effectiveProjectId,
            milestone_id: effectiveMilestoneId,
        };
        if (iterationId === null && effectiveProjectId === null) { setError(t('domain.projectRequired')); return; }
        const assigneeIds = teamMembers
            ? new Set(teamMembers.map(member => member.id))
            : undefined;
        const validationIssue = validateTaskEditor(values, assigneeIds)[0];
        if (validationIssue) {
            setError(t(`taskEditor.validation.${validationIssue.code}`));
            return;
        }

        if (mode === 'sandbox' && currentTask && onSaveSandbox) {
            onSaveSandbox(toTaskUpdate(values, { includeStatus: true }));
            setBaseline(values);
            onSuccess();
        } else if (currentTask) {
            const update = toTaskUpdate(values);
            if (currentTask.detail_context?.dependencies.has_more) delete update.depends_on;
            if (currentTask.is_composite) {
                delete update.priority;
                delete update.effort_days;
                delete update.effort_hours;
                delete update.assignee_id;
                delete update.status;
            }
            onPendingChange?.(true);
            updateMutation.mutate(update);
        } else {
            onPendingChange?.(true);
            createMutation.mutate(toTaskCreate(values));
        }
    };

    const handleCancel = () => {
        if (isSubmitting) return;
        if (confirmUnsavedOnCancel && (isDirty || workDirty || discussionDirty)) {
            setShowDiscardWarning(true);
            return;
        }
        onCancel();
    };

    const handleSendToTriage = () => {
        const title = formData.title.trim();
        if (!title) {
            setError(t('taskEditor.validation.titleRequired'));
            return;
        }

        const assigneeHint = teamMembers?.find(member => member.id === formData.assignee_id)?.name ?? null;
        setError(null);
        createTriageMutation.mutate({
            title,
            description: formData.brief ? undefined : formData.description?.trim() || null,
            metadata_json: formData.brief ? { task_brief: formData.brief } : {},
            source: 'task_form',
            priority_hint: Number.isFinite(formData.priority) ? formData.priority : null,
            assignee_hint: assigneeHint,
            project_hint_id: effectiveProjectId,
            iteration_hint_id: iterationId,
            labels: formData.tags ?? [],
        });
    };

    const optionQueryError = teamError
        ?? iterationError
        ?? projectsError
        ?? milestonesError
        ?? templatesError;

    return (
        <form onSubmit={handleSubmit} className="task-form space-y-6">
            {sessionUnavailable && <div role="alert" className="space-y-2 rounded-md border border-feedback-warning-border bg-feedback-warning-muted p-3 text-sm text-feedback-warning-foreground">
                <p>{t('identity.expired')}</p>
                <a className="inline-flex min-h-11 items-center font-semibold underline" href={`/api/auth/login?return_to=${encodeURIComponent(window.location.pathname + window.location.search)}`}>{t('identity.signIn')}</a>
            </div>}
            {optionQueryError && (
                <QueryErrorState
                    error={optionQueryError}
                    fallback={t('queryFeedback.optionLoadFailed')}
                    onRetry={() => {
                        void refetchTeam();
                        void refetchIteration();
                        void refetchProjects();
                        void refetchMilestones();
                        void refetchTemplates();
                    }}
                />
            )}
            {error && (
                <div role="alert" className="bg-feedback-danger-muted text-feedback-danger-foreground p-3 rounded-md text-sm">
                    {error}
                </div>
            )}
            {conflict && (
                <div role="alert" className="space-y-2 rounded-md border border-feedback-warning-border bg-feedback-warning-muted p-3 text-sm text-feedback-warning-foreground">
                    <div className="font-semibold">{t('taskEditor.conflictTitle')}</div>
                    <p>
                        {t('taskEditor.conflictBody', {
                            title: conflict.title,
                            version: conflict.version,
                        })}
                    </p>
                    {conflictTask && <details><summary className="cursor-pointer font-medium">{t('taskEditor.compareCurrent')}</summary>
                        <dl className="mt-2 space-y-2"><dt>{t('surfaces.taskForm.description')}</dt>
                            <dd className="max-h-40 overflow-auto whitespace-pre-wrap break-words">{conflictTask.description || '—'}</dd>
                            <dt>{t('statusChange.currentStatus')}</dt><dd>{t(`statuses.${conflictTask.status}`)}</dd>
                        </dl></details>}
                    <Button type="button" size="sm" variant="secondary" onClick={compareCurrentTask} disabled={isSubmitting || workDirty || discussionDirty} isLoading={isRefreshing}>{t('taskEditor.keepDraftWithCurrentVersion')}</Button>
                    <Button type="button" size="sm" variant="secondary" onClick={reloadCurrentTask} disabled={isSubmitting || workDirty || discussionDirty}>
                        {t('taskEditor.reload')}
                    </Button>
                </div>
            )}
            <ConfirmDialog
                open={showDiscardWarning}
                title={t('taskEditor.unsavedTitle')}
                description={t('taskEditor.unsavedBody')}
                confirmLabel={t('taskEditor.discard')}
                cancelLabel={t('taskEditor.keepEditing')}
                closeLabel={t('actions.close')}
                tone="warning"
                onCancel={() => setShowDiscardWarning(false)}
                onConfirm={() => { if (!isSubmitting) { clearDraft(); onCancel(); } }}
            />
            {recoveredDraft && <p role="status" className="rounded-md bg-feedback-info-muted p-3 text-sm text-feedback-info-foreground">{t('taskEditor.recoveredDraft')}</p>}
            {statusMessage && (
                <div className="bg-action-muted text-action p-3 rounded-md text-sm">
                    {statusMessage}
                </div>
            )}

            {/* Template selector (only for new tasks) */}
            {canApplyTemplates && taskTemplates.length > 0 && (
                <div>
                    <label htmlFor={`${formId}-template`} className="block text-sm font-medium text-content-primary mb-1">{t('surfaces.taskForm.template')}</label>
                    <select id={`${formId}-template`}
                        value={selectedTemplateId}
                        onChange={event => handleTemplateSelect(event.target.value)}
                        className="w-full px-3 py-2 border border-border-strong rounded-md shadow-sm focus:outline-none focus:ring-1 focus:ring-focus bg-surface-card"
                    >
                        <option value="">{t('surfaces.taskForm.noTemplate')}</option>
                        {taskTemplates.map(template => (
                            <option key={template.id} value={template.id}>
                                {templateDisplay(template).name}
                            </option>
                        ))}
                    </select>
                </div>
            )}

            {/* Agent readiness badge (only for existing tasks) */}
            {currentTask && mode === 'direct' && (
                currentTask.tags.includes('agent') && !currentTask.agent_readiness.blocker_codes?.includes('execution_context_required') && <TaskAgentReadinessBadge readiness={currentTask.agent_readiness} mode="panel" />
            )}

            <fieldset disabled={workDirty || discussionDirty || isSubmitting} className="contents">
            {/* === ESSENTIAL SECTION (always visible) === */}

            {/* Title - required */}
            <Input
                label={t('surfaces.taskForm.taskTitle')}
                value={formData.title}
                onChange={e => setFormData({ ...formData, title: e.target.value })}
                required
            />

            <div>
                <label className="field-lbl" htmlFor={`${formId}-owner`}>{t('domain.owner')}</label>
                {owners.isLoading && <p className="text-sm text-content-secondary">{t('common.loading')}</p>}
                {owners.isError && <QueryErrorState error={owners.error} fallback={t('queryFeedback.optionLoadFailed')} onRetry={() => void owners.refetch()} />}
                <select id={`${formId}-owner`} className="input w-full" value={formData.owner_profile_id ?? ''}
                    onChange={event => setFormData(values => ({ ...values, owner_profile_id: event.target.value ? Number(event.target.value) : null }))}>
                    <option value="">{t('domain.unassignedOwner')}</option>
                    {currentTask?.owner && !owners.data?.items.some(owner => owner.id === currentTask.owner!.id) && <option value={currentTask.owner.id}>{currentTask.owner.name}</option>}
                    {(owners.data?.items ?? []).map(owner => <option key={owner.id} value={owner.id}>{owner.name}</option>)}
                </select>
                <p className="mt-1 text-sm text-content-secondary">{t('domain.ownerHelp')}</p>
                {formData.owner_profile_id && <PersonCapacity key={formData.owner_profile_id} profileId={formData.owner_profile_id} startDate={iteration?.start_date} endDate={iteration?.end_date} />}
            </div>

            {/* Priority + Assignee */}
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
                <Input
 disabled={Boolean(currentTask?.is_composite)}                    type="number"
                    label={t('surfaces.taskForm.priority')}
                    value={formData.priority}
                    onChange={e => setFormData({ ...formData, priority: parseInt(e.target.value) })}
                    min="1"
                    max="10"
                />

                <div>
                    <label htmlFor={`${formId}-assignee`} className="block text-sm font-medium text-content-primary mb-1">{t('surfaces.taskForm.assignee')}</label>
                    <select
 disabled={Boolean(currentTask?.is_composite) || iterationId === null}                        id={`${formId}-assignee`}
                        value={formData.assignee_id || ''}
                        onChange={e => setFormData({ ...formData, assignee_id: e.target.value ? parseInt(e.target.value) : null })}
                        className="w-full px-3 py-2 border border-border-strong rounded-md shadow-sm focus:outline-none focus:ring-1 focus:ring-focus bg-surface-card"
                    >
                        <option value="">{t('surfaces.taskForm.unassigned')}</option>
                        {teamMembers?.map(member => (
                            <option key={member.id} value={member.id}>
                                {member.name} ({member.position})
                            </option>
                        ))}
                    </select>
                </div>
            </div>

            {/* Assignee recommendations (only for existing) */}
            {currentTask && iterationId !== null && <CollapsibleSection title={t('assigneeRecommendations.title')}>
                <AssigneeRecommendationsPanel
                    targetType="task"
                    taskId={currentTask.id}
                    selectedAssigneeId={formData.assignee_id ?? null}
                    onSelectAssignee={teamMemberId => setFormData({ ...formData, assignee_id: teamMemberId })}
                />
            </CollapsibleSection>}

            {/* Project */}
            <div>
                <label htmlFor={`${formId}-project`} className="block text-sm font-medium text-content-primary mb-1">{t('surfaces.taskForm.project')}</label>
                {scopedProjectId !== null ? (
                    <input id={`${formId}-project`} readOnly value={scopedProject?.name ?? t('surfaces.taskForm.projectNumber', { id: scopedProjectId })}
                        className="w-full px-3 py-2 border border-border-strong rounded-md shadow-sm bg-surface-muted text-content-primary" />
                ) : (
                    <select id={`${formId}-project`}
                        value={formData.project_id ?? ''}
                        onChange={e => handleProjectChange(e.target.value ? parseInt(e.target.value) : null)}
                        className="w-full px-3 py-2 border border-border-strong rounded-md shadow-sm focus:outline-none focus:ring-1 focus:ring-focus bg-surface-card"
                    >
                        <option value="">{t('surfaces.taskForm.noProject')}</option>
                        {projects.map(project => (
                            <option key={project.id} value={project.id}>
                                {project.name}
                            </option>
                        ))}
                    </select>
                )}
            </div>

                {/* Effort Days + Hours */}
                <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
                    <Input
                        type="number"
                        label={t('surfaces.taskForm.effortDays')}
                        value={formData.effort_days ?? ''}
                        step="0.1"
                        disabled={Boolean(currentTask?.is_composite || currentTask?.children?.length)}
                        title={currentTask?.children?.length ? t('surfaces.taskForm.calculatedFromSubtasks') : t('surfaces.taskForm.enterEffortDays')}
                        onChange={e => {
                            const days = e.target.value === "" ? null : parseFloat(e.target.value);
                            setFormData({
                                ...formData,
                                effort_days: days,
                                effort_hours: days === null ? null : days * dayHours,
                                estimate_provenance: days === null ? "unknown" : "estimated"
                            });
                        }}
                    />
                    <Input
                        type="number"
                        label={t('surfaces.taskForm.effortHours')}
                        value={formData.effort_hours ?? ''}
                        step="0.5"
                        disabled={Boolean(currentTask?.is_composite || currentTask?.children?.length)}
                        title={currentTask?.children?.length ? t('surfaces.taskForm.calculatedFromSubtasks') : t('surfaces.taskForm.enterEffortHours')}
                        onChange={e => {
                            const hours = e.target.value === "" ? null : parseFloat(e.target.value);
                            setFormData({
                                ...formData,
                                effort_hours: hours,
                                effort_days: hours === null ? null : hours / dayHours,
                                estimate_provenance: hours === null ? "unknown" : "estimated"
                            });
                        }}
                    />
                </div>

                <p className="text-sm text-content-secondary">{t("domain.estimateHelp", { hours: dayHours })}</p>
            <p className="text-sm text-content-secondary">{t(iterationId === null ? 'teamwork.inBacklog' : 'teamwork.inIteration')}{currentTask?.baseline_start_date ? ` · ${currentTask.baseline_start_date} – ${currentTask.baseline_end_date}` : ''}</p>
            {currentTask && <details><summary className="cursor-pointer text-sm font-medium">{t('teamwork.executionDates')}</summary><dl className="grid grid-cols-1 gap-2 rounded-md border border-border p-3 text-sm sm:grid-cols-2">
                <div><dt className="text-content-secondary">{t('workMetrics.baseline')}</dt><dd>{currentTask.baseline_start_date ?? '—'} → {currentTask.baseline_end_date ?? '—'}</dd></div>
                <div><dt className="text-content-secondary">{t('workMetrics.forecast')}</dt><dd>{currentTask.start_date ?? '—'} → {currentTask.end_date ?? '—'}</dd></div>
                <div><dt className="text-content-secondary">{t('workMetrics.actualStart')}</dt><dd>{currentTask.started_at ? new Date(currentTask.started_at).toLocaleString() : '—'}</dd></div>
                <div><dt className="text-content-secondary">{t('workMetrics.actualResolve')}</dt><dd>{currentTask.resolved_at ? new Date(currentTask.resolved_at).toLocaleString() : '—'}</dd></div>
                <div><dt className="text-content-secondary">{t('workMetrics.actualAccept')}</dt><dd>{currentTask.accepted_at ? new Date(currentTask.accepted_at).toLocaleString() : '—'}</dd></div>
            </dl></details>}

            {formData.brief ? <TaskBriefEditor value={formData.brief} disabled={isSubmitting || workDirty || discussionDirty}
                onChange={brief => setFormData(values => ({ ...values, brief }))} /> : <div className="space-y-3">
                <label htmlFor={`${formId}-description`} className="field-lbl">{t('surfaces.taskForm.description')}</label>
                <textarea id={`${formId}-description`} className="input min-h-24 w-full" value={formData.description}
                    onChange={event => setFormData(values => ({ ...values, description: event.target.value }))} />
                {currentTask && <Button type="button" variant="secondary" size="sm" disabled={isSubmitting || isDirty}
                    onClick={async () => {
                        setIsRefreshing(true);
                        try {
                            const preview = await taskService.convertBrief(currentTask.id, currentTask.version, false);
                            setFormData(values => ({ ...values, brief: preview.brief }));
                            setStatusMessage([t('domain.conversionDraft'), ...preview.notes].join(' '));
                        } catch (cause) { setError(getApiErrorMessage(cause, t('domain.saveFailed'))); }
                        finally { setIsRefreshing(false); }
                    }}>{t('domain.convertBrief')}</Button>}
            </div>}
            {currentTask?.legacy_description && <details className="text-sm text-content-secondary">
                <summary className="cursor-pointer">{t('domain.originalDescription')}</summary>
                <pre className="mt-2 whitespace-pre-wrap break-words font-sans">{currentTask.legacy_description}</pre>
            </details>}
            {mode === 'direct' && <Button type="button" variant="ghost" size="sm" aria-expanded={showAssistant} onClick={() => setShowAssistant(value => !value)}>{t('teamwork.optionalAssistant')}</Button>}
            {/* AI assistance intentionally stays outside sandbox drafts. */}
            {mode === 'direct' && showAssistant && (
            <section className="rounded-md border border-feedback-purple-border bg-feedback-purple-muted p-4 space-y-3">
                <div className="flex flex-col gap-2 sm:flex-row sm:items-start sm:justify-between">
                    <div>
                        <h3 className="flex items-center gap-2 text-sm font-semibold text-feedback-purple-foreground">
                            <Sparkles className="h-4 w-4" />
                            {t('taskAi.title')}
                        </h3>
                        <p className="text-xs text-feedback-purple-foreground">
                            {t('taskAi.description')}
                        </p>
                    </div>
                    <Button
                        type="button"
                        variant="secondary"
                        size="sm"
                        onClick={() => aiSuggestMutation.mutate()}
                        isLoading={aiSuggestMutation.isPending}
                        disabled={!formData.title.trim() && !formData.description?.trim()}
                    >
                        <Sparkles className="mr-2 h-4 w-4" />
                        {t('taskAi.generate')}
                    </Button>
                </div>
                <div>
                    <label htmlFor={`${formId}-ai-context`} className="mb-1 block text-xs font-medium text-feedback-purple-foreground">{t('taskAi.contextLabel')}</label>
                    <textarea
                        id={`${formId}-ai-context`}
                        value={aiContext}
                        onChange={event => setAiContext(event.target.value)}
                        placeholder={t('taskAi.contextPlaceholder')}
                        className="min-h-[70px] w-full rounded-md border border-feedback-purple-border bg-surface-card px-3 py-2 text-sm shadow-sm focus:border-action focus:outline-none focus:ring-1 focus:ring-focus"
                    />
                </div>
                {aiSuggestion && (
                    <div className="space-y-3 rounded-md border border-feedback-purple-border bg-surface-card p-3">
                        <div className="flex flex-wrap items-center gap-2">
                            <span className="rounded-full bg-feedback-purple-muted px-2 py-0.5 text-xs font-semibold text-feedback-purple-foreground">
                                {t('taskAi.suggested')}
                            </span>
                            <span className="rounded-full bg-surface-subtle px-2 py-0.5 text-xs text-content-primary">
                                {aiSuggestion.provider || t('taskAi.providerFallback')} / {aiSuggestion.model || t('taskAi.modelFallback')}
                            </span>
                            {aiSuggestion.language && (
                                <span className="rounded-full bg-status-active-muted px-2 py-0.5 text-xs text-action">
                                    {t('taskAi.language')}: {t(`common.language.${aiSuggestion.language}`)}
                                </span>
                            )}
                            {aiSuggestion.is_fallback && (
                                <span className="rounded-full bg-feedback-warning-muted px-2 py-0.5 text-xs font-medium text-feedback-warning-foreground">
                                    {t('taskAi.fallback')}
                                </span>
                            )}
                            {aiSuggestion.is_truncated && (
                                <span className="rounded-full bg-feedback-danger-muted px-2 py-0.5 text-xs font-medium text-feedback-danger-foreground">
                                    {t('taskAi.truncated')}
                                </span>
                            )}
                        </div>
                        {aiSuggestion.warnings.length > 0 && (
                            <div className="rounded-md border border-feedback-warning-border bg-feedback-warning-muted px-3 py-2 text-xs text-feedback-warning-foreground">
                                {aiSuggestion.warnings.map(warning => (
                                    <div key={warning}>{warning}</div>
                                ))}
                            </div>
                        )}
                        {aiSuggestion.suggested_title && (
                            <div>
                                <div className="text-xs font-semibold uppercase text-content-secondary">{t('taskAi.titleSection')}</div>
                                <div className="text-sm text-content-primary">{aiSuggestion.suggested_title}</div>
                            </div>
                        )}
                        {aiSuggestion.suggested_description && (
                            <div>
                                <div className="text-xs font-semibold uppercase text-content-secondary">{t('taskAi.descriptionSection')}</div>
                                <div className="whitespace-pre-wrap text-sm text-content-primary">{aiSuggestion.suggested_description}</div>
                            </div>
                        )}
                        {aiSuggestion.acceptance_criteria.length > 0 && (
                            <div>
                                <div className="text-xs font-semibold uppercase text-content-secondary">{t('taskAi.acceptanceCriteria')}</div>
                                <ul className="mt-1 list-disc space-y-1 pl-5 text-sm text-content-primary">
                                    {aiSuggestion.acceptance_criteria.map(item => <li key={item}>{item}</li>)}
                                </ul>
                            </div>
                        )}
                        {aiSuggestion.implementation_notes.length > 0 && (
                            <div>
                                <div className="text-xs font-semibold uppercase text-content-secondary">{t('taskAi.notes')}</div>
                                <ul className="mt-1 list-disc space-y-1 pl-5 text-sm text-content-primary">
                                    {aiSuggestion.implementation_notes.map(item => <li key={item}>{item}</li>)}
                                </ul>
                            </div>
                        )}
                        {aiSuggestion.risks.length > 0 && (
                            <div>
                                <div className="text-xs font-semibold uppercase text-content-secondary">{t('taskAi.risks')}</div>
                                <ul className="mt-1 list-disc space-y-1 pl-5 text-sm text-content-primary">
                                    {aiSuggestion.risks.map(item => <li key={item}>{item}</li>)}
                                </ul>
                            </div>
                        )}
                        {aiSuggestion.open_questions.length > 0 && (
                            <div>
                                <div className="text-xs font-semibold uppercase text-content-secondary">{t('taskAi.openQuestions')}</div>
                                <ul className="mt-1 list-disc space-y-1 pl-5 text-sm text-content-primary">
                                    {aiSuggestion.open_questions.map(item => <li key={item}>{item}</li>)}
                                </ul>
                            </div>
                        )}
                        {aiSuggestion.ungrounded_suggestions.length > 0 && (
                            <div>
                                <div className="text-xs font-semibold uppercase text-content-secondary">{t('taskAi.ungroundedSuggestions')}</div>
                                <ul className="mt-1 list-disc space-y-1 pl-5 text-sm text-content-primary">
                                    {aiSuggestion.ungrounded_suggestions.map(item => <li key={item}>{item}</li>)}
                                </ul>
                            </div>
                        )}
                        {aiSuggestion.grounded_facts.length > 0 && (
                            <div className="text-xs text-content-secondary">
                                {t('taskAi.groundedFacts')}: {aiSuggestion.grounded_facts.map(fact => fact.source).join(', ')}
                            </div>
                        )}
                        <div className="flex flex-wrap gap-2 border-t pt-3">
                            <Button
                                type="button"
                                size="sm"
                                variant="secondary"
                                disabled={!aiSuggestion.suggested_title}
                                onClick={() => {
                                    if (aiSuggestion.suggested_title) {
                                        setFormData(prev => ({ ...prev, title: aiSuggestion.suggested_title || prev.title }));
                                        setStatusMessage(t('taskAi.titleApplied'));
                                    }
                                }}
                            >
                                {t('taskAi.applyTitle')}
                            </Button>
                            <Button
                                type="button"
                                size="sm"
                                variant="secondary"
                                disabled={!aiSuggestion.suggested_description}
                                onClick={() => {
                                    setFormData(prev => ({ ...prev, ...(prev.brief ? { brief: { ...prev.brief, context: aiSuggestion.suggested_description } } : { description: aiSuggestion.suggested_description }) }));
                                    setStatusMessage(t('taskAi.descriptionApplied'));
                                }}
                            >
                                {t('taskAi.applyDescription')}
                            </Button>
                            <Button
                                type="button"
                                size="sm"
                                variant="secondary"
                                disabled={aiSuggestion.acceptance_criteria.length === 0}
                                onClick={() => appendAcceptanceCriteria(aiSuggestion.acceptance_criteria)}
                            >
                                {t('taskAi.appendCriteria')}
                            </Button>
                            <Button type="button" size="sm" variant="ghost" onClick={() => setAiSuggestion(null)}>
                                {t('taskAi.dismiss')}
                            </Button>
                        </div>
                    </div>
                )}
            </section>
            )}

            {/* === COLLAPSIBLE: DATES & EFFORT === */}
            <CollapsibleSection title={t('taskForm.datesEffort')}>
                {/* Milestone */}
                <div>
                    <label htmlFor={`${formId}-milestone`} className="block text-sm font-medium text-content-primary mb-1">{t('surfaces.taskForm.milestone')}</label>
                    <select id={`${formId}-milestone`}
                        value={effectiveMilestoneId ?? ''}
                        onChange={e => setFormData({ ...formData, milestone_id: e.target.value ? parseInt(e.target.value) : null })}
                        disabled={!effectiveProjectId}
                        className="w-full px-3 py-2 border border-border-strong rounded-md shadow-sm focus:outline-none focus:ring-1 focus:ring-focus bg-surface-card disabled:bg-surface-muted disabled:text-content-secondary"
                    >
                        <option value="">{t('surfaces.taskForm.noMilestone')}</option>
                        {projectMilestones.map(milestone => (
                            <option key={milestone.id} value={milestone.id}>
                                {milestone.name}
                                {milestone.target_date ? ` (${formatDate(milestone.target_date)})` : ''}
                            </option>
                        ))}
                    </select>
                </div>

                {/* Date constraints */}
                <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
                    <div>
                        <label htmlFor={`${formId}-min-start`} className="block text-sm font-medium text-content-primary mb-1">{t('surfaces.taskForm.minStartDate')}</label>
                        <input id={`${formId}-min-start`}
                            type="date"
                            value={formData.min_start_date || ''}
                            onChange={e => setFormData({ ...formData, min_start_date: e.target.value || null })}
                            className="w-full px-3 py-2 border border-border-strong rounded-md shadow-sm focus:outline-none focus:ring-1 focus:ring-focus"
                        />
                    </div>
                    <div>
                        <label htmlFor={`${formId}-max-end`} className="block text-sm font-medium text-content-primary mb-1">{t('surfaces.taskForm.maxEndDate')}</label>
                        <input id={`${formId}-max-end`}
                            type="date"
                            value={formData.max_end_date || ''}
                            onChange={e => setFormData({ ...formData, max_end_date: e.target.value || null })}
                            className="w-full px-3 py-2 border border-border-strong rounded-md shadow-sm focus:outline-none focus:ring-1 focus:ring-focus"
                        />
                    </div>
                </div>
            </CollapsibleSection>

            {/* === COLLAPSIBLE: ADVANCED OPTIONS === */}
            <CollapsibleSection title={t('taskForm.advancedOptions')}>
                {mode === 'sandbox' && currentTask && (
                    <div>
                        <label htmlFor={`${formId}-sandbox-status`} className="block text-sm font-medium text-content-primary mb-1">
                            {t('taskEditor.status')}
                        </label>
                        <select id={`${formId}-sandbox-status`}
                            value={formData.status}
                            onChange={event => setFormData({
                                ...formData,
                                status: event.target.value as Task['status'],
                            })}
                            className="w-full px-3 py-2 border border-border-strong rounded-md shadow-sm focus:outline-none focus:ring-1 focus:ring-focus bg-surface-card"
                        >
                            <option value="planned">{t('statuses.planned')}</option>
                            <option value="active">{t('statuses.active')}</option>
                            <option value="resolved">{t('statuses.resolved')}</option>
                            <option value="closed">{t('statuses.closed')}</option>
                        </select>
                    </div>
                )}

                {/* Dependencies */}
                <div>
                    <label className="block text-sm font-medium text-content-primary mb-1">{t('surfaces.taskForm.dependencies')}</label>
                    <div className="border border-border-strong rounded-md p-2 max-h-32 overflow-y-auto bg-surface-muted">
                        {currentTask?.detail_context?.dependencies.has_more ? <p className="text-sm text-content-secondary">{t('domain.boundedDependencies')}</p> : <TaskDependencySelector
                        projectId={effectiveProjectId}
                            iterationId={iterationId}
                            currentTaskId={currentTask?.id}
                            selectedIds={formData.depends_on}
                            onChange={(ids) => setFormData({ ...formData, depends_on: ids })}
                        />}
                    </div>
                </div>

                {/* Task flags */}
                <div className="grid grid-cols-1 gap-2 sm:grid-cols-2 sm:gap-4">
                    <label className="flex min-h-11 cursor-pointer items-center gap-2">
                        <input
                            type="checkbox"
                            checked={formData.is_optional}
                            onChange={e => setFormData({ ...formData, is_optional: e.target.checked })}
                            className="w-4 h-4 rounded border-border-strong text-action focus:ring-focus"
                        />
                        <span className="text-sm font-medium text-content-primary">{t('surfaces.taskForm.optionalTask')}</span>
                    </label>
                    <label className="flex min-h-11 cursor-pointer items-center gap-2">
                        <input
                            type="checkbox"
                            checked={formData.is_deferred}
                            onChange={e => setFormData({ ...formData, is_deferred: e.target.checked })}
                            className="w-4 h-4 rounded border-border-strong text-content-secondary focus:ring-focus"
                        />
                        <span className="text-sm font-medium text-content-primary">{t('surfaces.taskForm.deferred')}</span>
                    </label>
                </div>

                {/* Tags */}
                <LabelSelector
                    label={t('surfaces.taskForm.tags')}
                    value={formData.tags ?? []}
                    onChange={tags => setFormData({ ...formData, tags })}
                    placeholder={t('surfaces.taskForm.newTag')}
                />
            </CollapsibleSection>

            {/* === STATUS & TIMELINE (only for existing tasks) === */}
            {currentTask && <div className="flex flex-wrap gap-2 text-sm" role="status">
                {currentTask.is_accepted ? <span className="text-feedback-success">{t('workStatus.accepted')}</span>
                    : currentTask.status === 'resolved' ? <span className="text-content-secondary">{t('workStatus.awaitingAcceptance')}</span>
                    : currentTask.acceptance_unknown ? <span className="text-content-secondary">{t('workStatus.acceptanceUnknown')}</span> : null}
                {currentTask.is_overdue && <span className="text-feedback-danger">{t('workStatus.overdueDelivery')}</span>}
                {currentTask.is_iteration_overflow && <span className="text-feedback-warning-foreground">{t('workStatus.iterationOverflow')}</span>}
            </div>}
            {currentTask && iterationId !== null && mode === 'direct' && (
                <div className="border-t pt-4">
                    <label className="block text-sm font-medium text-content-primary mb-2">{t('surfaces.taskForm.statusManagement')}</label>
                    {iterationId !== null && <fieldset disabled={isDirty || workDirty || discussionDirty || isSubmitting}><StatusChangeControl
                        onPendingChange={handleStatusPending}
                        task={currentTask}
                        iterationId={iterationId}
                        onStatusChanged={async () => {
                            const latest = await taskService.getById(currentTask.id);
                            setCurrentTask(latest);
                            setFormData(values => ({ ...values, status: latest.status, expected_version: latest.version }));
                            setBaseline(values => ({ ...values, status: latest.status, expected_version: latest.version }));
                            invalidateTaskProjectQueries();
                        }}
                    /></fieldset>}
                </div>
            )}

            </fieldset>
            {currentTask && mode === 'direct' && <TaskWorkPanel key={`${currentTask.id}:${currentTask.version}`} task={currentTask}
                draftKey={draftKey} disabled={isDirty || discussionDirty || isSubmitting} onDirty={setWorkDirty} onPending={handleStatusPending}
                onReload={() => void reloadCurrentTask()}
                onUpdated={latest => {
                    const values = buildTaskEditorDefaults({ task: latest });
                    setCurrentTask(latest); setFormData(values); setBaseline(values); setStatusPending(false);
                    invalidateTaskProjectQueries();
                }} />}
            {currentTask && mode === 'direct' && <DeliveryDependencies task={currentTask} disabled={isDirty || workDirty || discussionDirty || isSubmitting}
                onPending={handleStatusPending} onUpdated={latest => {
                    const values = buildTaskEditorDefaults({ task: latest }); setCurrentTask(latest); setFormData(values); setBaseline(values); invalidateTaskProjectQueries();
                }} />}
            {currentTask && mode === 'direct' && <TaskDiscussion taskId={currentTask.id} draftKey={draftKey} disabled={isSubmitting}
                onDirty={setDiscussionDirty} onPending={handleStatusPending} />}
            {currentTask && mode === 'direct' && <CollapsibleSection title={t('taskTimeline.title', { defaultValue: t('domain.history') })}><TaskTimelinePanel task={currentTask} /></CollapsibleSection>}

            {/* === ACTION BUTTONS === */}
            <div className="flex flex-col items-stretch gap-2 border-t pt-4 sm:flex-row sm:items-center sm:justify-between">
                {canSendToTriage ? (
                    <Button
                        type="button"
                        variant="secondary"
                        className="w-full sm:w-auto"
                        onClick={handleSendToTriage}
                        isLoading={createTriageMutation.isPending}
                        disabled={isSubmitting || workDirty || discussionDirty}
                    >
                        <Inbox className="w-4 h-4 mr-2" />
                        {t('surfaces.taskForm.sendToTriage')}
                    </Button>
                ) : (
                    <div />
                )}
                <div className="flex flex-col gap-2 sm:flex-row sm:justify-end">
                    <Button
                        type="button"
                        variant="ghost"
                        className="w-full sm:w-auto"
                        onClick={handleCancel}
                    >
                        {t('surfaces.taskForm.cancel')}
                    </Button>
                    <Button
                        type="submit"
                        className="w-full sm:w-auto"
                        isLoading={createMutation.isPending || updateMutation.isPending}
                        disabled={isSubmitting || workDirty || discussionDirty || sessionUnavailable || Boolean(conflict)}
                    >
                        <Save className="w-4 h-4 mr-2" />
                        {mode === 'sandbox'
                            ? t('taskEditor.saveSandbox')
                            : currentTask
                                ? t('taskEditor.updateTask')
                                : t('taskEditor.createTask')}
                    </Button>
                </div>
            </div>
        </form>
    );
};

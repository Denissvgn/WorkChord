import { useEffect, useMemo, useState } from 'react';
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
import { TaskTimelinePanel } from './TaskTimelinePanel';
import { AssigneeRecommendationsPanel } from '../team/AssigneeRecommendationsPanel';
import { getApiErrorMessage } from '../../utils/apiError';
import {
    appendChecklistToDescription,
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

interface TaskFormProps {
    iterationId: number;
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
    confirmUnsavedOnCancel?: boolean;
}

export const TaskForm = ({
    iterationId,
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
    confirmUnsavedOnCancel = true,
}: TaskFormProps) => {
    const { t } = useTranslation();
    const queryClient = useQueryClient();
    const [error, setError] = useState<string | null>(null);
    const [statusMessage, setStatusMessage] = useState<string | null>(null);
    const [aiContext, setAiContext] = useState('');
    const [aiSuggestion, setAiSuggestion] = useState<GroundedAISuggestionResponse | null>(null);
    const [selectedTemplateId, setSelectedTemplateId] = useState('');
    const [currentTask, setCurrentTask] = useState(initialData);
    const [conflict, setConflict] = useState<TaskConflictMetadata | null>(null);
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
    const [formData, setFormData] = useState<TaskEditorValues>(() => initialValues);
    const [baseline, setBaseline] = useState<TaskEditorValues>(() => initialValues);
    const isDirty = JSON.stringify(formData) !== JSON.stringify(baseline);

    useEffect(() => {
        onDirtyChange?.(isDirty);
    }, [isDirty, onDirtyChange]);

    // Fetch team for assignee dropdown
    const { data: teamMembers, error: teamError, refetch: refetchTeam } = useQuery({
        queryKey: ['team', iterationId],
        queryFn: () => teamService.getByIteration(iterationId),
    });

    const { data: iteration, error: iterationError, refetch: refetchIteration } = useQuery({
        queryKey: ['iteration', iterationId],
        queryFn: () => iterationService.getById(iterationId),
    });

    const { data: projects = [], error: projectsError, refetch: refetchProjects } = useQuery({
        queryKey: ['projects'],
        queryFn: projectService.getAll,
    });

    const scopedProjectId = iteration?.project_id ?? null;
    const scopedProject = iteration?.project ?? null;
    const effectiveProjectId = scopedProjectId ?? formData.project_id ?? null;

    const selectedProjectId = effectiveProjectId;
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
        queryClient.invalidateQueries({ queryKey: ['workload'] });
        queryClient.invalidateQueries({ queryKey: ['gantt'] });
        queryClient.invalidateQueries({ queryKey: ['projects'] });
        queryClient.invalidateQueries({ queryKey: ['projectSummary'] });
        queryClient.invalidateQueries({ queryKey: ['projectTasks'] });
    };

    const createMutation = useMutation({
        mutationFn: (data: TaskCreate) => taskService.create(iterationId, data),
        onSuccess: () => {
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
            invalidateTaskProjectQueries();
            onSuccess();
        },
        onError: (err: unknown) => {
            const mapped = mapTaskEditorServerError(err, t('taskEditor.updateFailed'));
            if (mapped.kind === 'version-conflict') {
                setConflict(mapped.currentTask);
                setError(null);
                return;
            }
            setError(mapped.message);
        },
    });

    const reloadCurrentTask = async () => {
        if (!currentTask) return;
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
        }
    };

    const buildAISuggestPayload = (): TaskAISuggestRequest => ({
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
        const block = [
            `${t('taskAi.acceptanceCriteria')}:`,
            ...criteria.map(item => `- ${item}`),
        ].join('\n');
        setFormData(prev => ({
            ...prev,
            description: [prev.description?.trim(), block].filter(Boolean).join('\n\n'),
        }));
        setStatusMessage(t('taskAi.criteriaAppended'));
    };

    const applyTaskTemplate = (template: WorkTemplate) => {
        const display = templateDisplay(template);
        setFormData(prev => {
            const effortDays = template.default_effort_days ?? prev.effort_days;
            const source = getPayloadString(template.default_payload, 'source', prev.source ?? null);

            return {
                ...prev,
                title: display.default_title ?? prev.title,
                description: appendChecklistToDescription(
                    display.default_description ?? prev.description,
                    display.default_checklist,
                ),
                priority: template.default_priority ?? prev.priority,
                effort_days: effortDays,
                effort_hours: template.default_effort_days != null
                    ? effortDays * 8
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
        setError(null);
        setConflict(null);
        const values = {
            ...formData,
            project_id: effectiveProjectId,
            milestone_id: effectiveMilestoneId,
        };
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
            updateMutation.mutate(toTaskUpdate(values));
        } else {
            createMutation.mutate(toTaskCreate(values));
        }
    };

    const handleCancel = () => {
        if (confirmUnsavedOnCancel && isDirty) {
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
            description: formData.description?.trim() || null,
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
                    <Button type="button" size="sm" variant="secondary" onClick={reloadCurrentTask}>
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
                onConfirm={onCancel}
            />
            {statusMessage && (
                <div className="bg-action-muted text-action p-3 rounded-md text-sm">
                    {statusMessage}
                </div>
            )}

            {/* Template selector (only for new tasks) */}
            {canApplyTemplates && taskTemplates.length > 0 && (
                <div>
                    <label className="block text-sm font-medium text-content-primary mb-1">{t('surfaces.taskForm.template')}</label>
                    <select
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
                <TaskAgentReadinessBadge readiness={currentTask.agent_readiness} mode="panel" />
            )}

            {/* === ESSENTIAL SECTION (always visible) === */}

            {/* Title - required */}
            <Input
                label={t('surfaces.taskForm.taskTitle')}
                value={formData.title}
                onChange={e => setFormData({ ...formData, title: e.target.value })}
                required
            />

            {/* Description */}
            <div>
                <label className="block text-sm font-medium text-content-primary mb-1">{t('surfaces.taskForm.description')}</label>
                <textarea
                    className="w-full px-3 py-2 border border-border-strong rounded-md shadow-sm focus:outline-none focus:ring-1 focus:ring-focus min-h-[100px]"
                    value={formData.description || ''}
                    onChange={e => setFormData({ ...formData, description: e.target.value })}
                />
            </div>

            {/* Priority + Assignee */}
            <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
                <Input
                    type="number"
                    label={t('surfaces.taskForm.priority')}
                    value={formData.priority}
                    onChange={e => setFormData({ ...formData, priority: parseInt(e.target.value) })}
                    min="1"
                    max="10"
                />

                <div>
                    <label htmlFor="task-assignee" className="block text-sm font-medium text-content-primary mb-1">{t('surfaces.taskForm.assignee')}</label>
                    <select
                        id="task-assignee"
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
            {currentTask && (
                <AssigneeRecommendationsPanel
                    targetType="task"
                    taskId={currentTask.id}
                    selectedAssigneeId={formData.assignee_id ?? null}
                    onSelectAssignee={teamMemberId => setFormData({ ...formData, assignee_id: teamMemberId })}
                />
            )}

            {/* Project */}
            <div>
                <label className="block text-sm font-medium text-content-primary mb-1">{t('surfaces.taskForm.project')}</label>
                {scopedProjectId !== null ? (
                    <div className="w-full px-3 py-2 border border-border-strong rounded-md shadow-sm bg-surface-muted text-content-primary">
                        {scopedProject?.name ?? t('surfaces.taskForm.projectNumber', { id: scopedProjectId })}
                    </div>
                ) : (
                    <select
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

            {/* AI assistance intentionally stays outside sandbox drafts. */}
            {mode === 'direct' && (
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
                    <label htmlFor="task-ai-context" className="mb-1 block text-xs font-medium text-feedback-purple-foreground">{t('taskAi.contextLabel')}</label>
                    <textarea
                        id="task-ai-context"
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
                                    setFormData(prev => ({ ...prev, description: aiSuggestion.suggested_description }));
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
                    <label className="block text-sm font-medium text-content-primary mb-1">{t('surfaces.taskForm.milestone')}</label>
                    <select
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

                {/* Effort Days + Hours */}
                <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
                    <Input
                        type="number"
                        label={t('surfaces.taskForm.effortDays')}
                        value={formData.effort_days}
                        step="0.1"
                        disabled={Boolean(currentTask?.children?.length)}
                        title={currentTask?.children?.length ? t('surfaces.taskForm.calculatedFromSubtasks') : t('surfaces.taskForm.enterEffortDays')}
                        onChange={e => {
                            const days = parseFloat(e.target.value);
                            setFormData({
                                ...formData,
                                effort_days: days,
                                effort_hours: days * 8
                            });
                        }}
                    />
                    <Input
                        type="number"
                        label={t('surfaces.taskForm.effortHours')}
                        value={formData.effort_hours}
                        step="0.5"
                        disabled={Boolean(currentTask?.children?.length)}
                        title={currentTask?.children?.length ? t('surfaces.taskForm.calculatedFromSubtasks') : t('surfaces.taskForm.enterEffortHours')}
                        onChange={e => {
                            const hours = parseFloat(e.target.value);
                            setFormData({
                                ...formData,
                                effort_hours: hours,
                                effort_days: hours / 8
                            });
                        }}
                    />
                </div>

                {/* Date constraints */}
                <div className="grid grid-cols-1 gap-4 sm:grid-cols-2">
                    <div>
                        <label className="block text-sm font-medium text-content-primary mb-1">{t('surfaces.taskForm.minStartDate')}</label>
                        <input
                            type="date"
                            value={formData.min_start_date || ''}
                            onChange={e => setFormData({ ...formData, min_start_date: e.target.value || null })}
                            className="w-full px-3 py-2 border border-border-strong rounded-md shadow-sm focus:outline-none focus:ring-1 focus:ring-focus"
                        />
                    </div>
                    <div>
                        <label className="block text-sm font-medium text-content-primary mb-1">{t('surfaces.taskForm.maxEndDate')}</label>
                        <input
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
                        <label className="block text-sm font-medium text-content-primary mb-1">
                            {t('taskEditor.status')}
                        </label>
                        <select
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
                        <TaskDependencySelector
                            iterationId={iterationId}
                            currentTaskId={currentTask?.id}
                            selectedIds={formData.depends_on}
                            onChange={(ids) => setFormData({ ...formData, depends_on: ids })}
                        />
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
            {currentTask && mode === 'direct' && (
                <div className="border-t pt-4">
                    <label className="block text-sm font-medium text-content-primary mb-2">{t('surfaces.taskForm.statusManagement')}</label>
                    <StatusChangeControl
                        task={currentTask}
                        iterationId={iterationId}
                        onStatusChanged={onSuccess}
                    />
                </div>
            )}

            {currentTask && mode === 'direct' && (
                <TaskTimelinePanel task={currentTask} />
            )}

            {/* === ACTION BUTTONS === */}
            <div className="flex flex-col items-stretch gap-2 border-t pt-4 sm:flex-row sm:items-center sm:justify-between">
                {canSendToTriage ? (
                    <Button
                        type="button"
                        variant="secondary"
                        className="w-full sm:w-auto"
                        onClick={handleSendToTriage}
                        isLoading={createTriageMutation.isPending}
                        disabled={createMutation.isPending || updateMutation.isPending}
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
                        disabled={createTriageMutation.isPending}
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

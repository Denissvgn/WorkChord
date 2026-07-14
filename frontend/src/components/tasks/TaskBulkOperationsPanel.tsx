import i18n from '../../i18n/i18n';
import { useMemo, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { Bot, CheckCircle2, ClipboardCheck, Trash2, XCircle } from 'lucide-react';
import { Button } from '../common/Button';
import { taskService } from '../../services/taskService';
import { teamService } from '../../services/teamService';
import { projectService } from '../../services/projectService';
import { iterationService } from '../../services/iterationService';
import { getApiErrorMessage } from '../../utils/apiError';
import { QueryErrorState, QueryLoadingState } from '../feedback/QueryState';
import type {
    Task,
    TaskBulkAction,
    TaskBulkOperationRequest,
    TaskBulkOperationResponse,
    TaskBulkOperationResult,
    TaskStatus,
} from '../../types/task';

const t = i18n.t.bind(i18n);

interface TaskBulkOperationsPanelProps {
    iterationId: number;
    selectedTasks: Task[];
    selectedTaskIds: number[];
    onClearSelection: () => void;
    onApplied: () => void;
}

const ACTION_OPTIONS: { value: TaskBulkAction; labelKey: string }[] = [
    { value: 'set_assignee', labelKey: 'setAssignee' },
    { value: 'clear_assignee', labelKey: 'clearAssignee' },
    { value: 'auto_assign', labelKey: 'autoAssign' },
    { value: 'set_project', labelKey: 'setProject' },
    { value: 'clear_project', labelKey: 'clearProject' },
    { value: 'set_milestone', labelKey: 'setMilestone' },
    { value: 'clear_milestone', labelKey: 'clearMilestone' },
    { value: 'set_priority', labelKey: 'setPriority' },
    { value: 'add_labels', labelKey: 'addLabels' },
    { value: 'remove_labels', labelKey: 'removeLabels' },
    { value: 'set_flags', labelKey: 'setFlags' },
    { value: 'change_status', labelKey: 'changeStatus' },
    { value: 'delete', labelKey: 'delete' },
];

const STATUS_OPTIONS: TaskStatus[] = ['planned', 'active', 'resolved', 'closed'];

const formatValue = (value: unknown): string => {
    if (value === null || value === undefined || value === '') return t('surfaces.taskBulk.none');
    if (Array.isArray(value)) return value.length ? value.join(', ') : t('surfaces.taskBulk.none');
    if (typeof value === 'boolean') return value ? t('surfaces.taskBulk.yes') : t('surfaces.taskBulk.no');
    return String(value);
};

const changeLines = (result: TaskBulkOperationResult) => {
    return Object.entries(result.changes || {}).map(([field, value]) => {
        if (value && typeof value === 'object' && 'old' in value && 'new' in value) {
            const change = value as { old: unknown; new: unknown };
            return `${field}: ${formatValue(change.old)} -> ${formatValue(change.new)}`;
        }
        return `${field}: ${formatValue(value)}`;
    });
};

export const TaskBulkOperationsPanel = ({
    iterationId,
    selectedTasks,
    selectedTaskIds,
    onClearSelection,
    onApplied,
}: TaskBulkOperationsPanelProps) => {
    useTranslation();
    const queryClient = useQueryClient();
    const [action, setAction] = useState<TaskBulkAction>('set_assignee');
    const [assigneeId, setAssigneeId] = useState('');
    const [projectId, setProjectId] = useState('');
    const [milestoneId, setMilestoneId] = useState('');
    const [priority, setPriority] = useState('5');
    const [labelsText, setLabelsText] = useState('');
    const [status, setStatus] = useState<TaskStatus>('active');
    const [reason, setReason] = useState('');
    const [isOptional, setIsOptional] = useState('');
    const [isDeferred, setIsDeferred] = useState('');
    const [minConfidence, setMinConfidence] = useState('0.5');
    const [preview, setPreview] = useState<TaskBulkOperationResponse | null>(null);
    const [previewAction, setPreviewAction] = useState<TaskBulkAction | null>(null);
    const [error, setError] = useState<string | null>(null);

    const taskNameById = useMemo(() => {
        const map = new Map<number, string>();
        selectedTasks.forEach(task => map.set(task.id, task.title));
        return map;
    }, [selectedTasks]);

    const teamQuery = useQuery({
        queryKey: ['team', iterationId],
        queryFn: () => teamService.getByIteration(iterationId),
    });

    const projectsQuery = useQuery({
        queryKey: ['projects'],
        queryFn: () => projectService.getAll(),
    });

    const iterationQuery = useQuery({
        queryKey: ['iteration', iterationId],
        queryFn: () => iterationService.getById(iterationId),
    });
    const teamMembers = teamQuery.data ?? [];
    const projects = projectsQuery.data ?? [];
    const iteration = iterationQuery.data;

    const scopedProjectId = iteration?.project_id ?? null;
    const scopedProject = iteration?.project ?? null;
    const actionOptions = useMemo(
        () => ACTION_OPTIONS.filter(option => scopedProjectId === null || option.value !== 'clear_project'),
        [scopedProjectId],
    );
    const effectiveAction: TaskBulkAction = scopedProjectId !== null && action === 'clear_project'
        ? 'set_project'
        : action;

    const selectedProjectId = scopedProjectId ?? (projectId ? Number(projectId) : null);
    const milestonesQuery = useQuery({
        queryKey: ['projectMilestones', selectedProjectId],
        queryFn: () => projectService.getMilestones(selectedProjectId!),
        enabled: Boolean(selectedProjectId),
    });
    const milestones = milestonesQuery.data ?? [];
    const optionQueries = [teamQuery, projectsQuery, iterationQuery, milestonesQuery];
    const optionError = optionQueries.find(query => query.isError)?.error;
    const optionsLoading = optionQueries.some(query => query.isLoading);

    const buildPayload = (): Record<string, unknown> => {
        const labels = labelsText
            .split(/[\n,]/)
            .map(label => label.trim())
            .filter(Boolean);

        switch (effectiveAction) {
            case 'set_assignee':
                return { assignee_id: assigneeId ? Number(assigneeId) : undefined };
            case 'auto_assign':
                return { min_confidence: Number(minConfidence || 0.5) };
            case 'set_project': {
                const payload: Record<string, unknown> = {
                    project_id: scopedProjectId ?? (projectId ? Number(projectId) : undefined),
                };
                if (milestoneId) payload.milestone_id = Number(milestoneId);
                return payload;
            }
            case 'set_milestone':
                return { milestone_id: milestoneId ? Number(milestoneId) : undefined };
            case 'set_priority':
                return { priority: Number(priority) };
            case 'add_labels':
            case 'remove_labels':
                return { labels };
            case 'set_flags': {
                const payload: Record<string, unknown> = {};
                if (isOptional) payload.is_optional = isOptional === 'true';
                if (isDeferred) payload.is_deferred = isDeferred === 'true';
                return payload;
            }
            case 'change_status':
                return { status, reason: reason.trim() || undefined };
            default:
                return {};
        }
    };

    const mutation = useMutation({
        mutationFn: (request: TaskBulkOperationRequest) => taskService.runBulkOperation(request),
        onSuccess: async (response, variables) => {
            setPreview(response);
            setPreviewAction(response.dry_run ? variables.action : null);
            setError(null);
            if (!response.dry_run) {
                await queryClient.invalidateQueries({ queryKey: ['tasks', iterationId] });
                await queryClient.invalidateQueries({ queryKey: ['workload'] });
                await queryClient.invalidateQueries({ queryKey: ['gantt'] });
                await queryClient.invalidateQueries({ queryKey: ['projects'] });
                await queryClient.invalidateQueries({ queryKey: ['projectSummary'] });
                await queryClient.invalidateQueries({ queryKey: ['saved-view-dashboard-cards'] });
                onApplied();
            }
        },
        onError: (err: unknown) => {
            setError(getApiErrorMessage(err, t('surfaces.taskBulk.failedToRun')));
        },
    });

    const run = (dryRun: boolean) => {
        setError(null);
        if (effectiveAction === 'set_assignee') {
            const selectedAssigneeId = assigneeId ? Number(assigneeId) : null;
            if (selectedAssigneeId === null) {
                setError(t('surfaces.taskBulk.chooseIterationMember'));
                return;
            }
            if (!teamMembers.some(member => member.id === selectedAssigneeId)) {
                setError(t('surfaces.taskBulk.assigneeOutsideIteration'));
                return;
            }
        }
        if (scopedProjectId !== null && effectiveAction === 'clear_project') {
            setError(t('surfaces.taskBulk.projectCannotBeCleared'));
            return;
        }
        mutation.mutate({
            task_ids: selectedTaskIds,
            action: effectiveAction,
            payload: buildPayload(),
            dry_run: dryRun,
        });
    };

    const canApply = preview?.dry_run === true
        && previewAction === effectiveAction
        && selectedTaskIds.length > 0
        && !mutation.isPending;

    return (
        <div data-testid="task-bulk-operations" className="border border-feedback-indigo-border bg-feedback-indigo-muted rounded-lg p-3 space-y-3">
            {optionsLoading && <QueryLoadingState className="min-h-16 py-3" />}
            {optionError && (
                <QueryErrorState
                    error={optionError}
                    fallback={t('queryFeedback.optionLoadFailed')}
                    onRetry={() => optionQueries.forEach(query => void query.refetch())}
                />
            )}
            <div className="flex flex-wrap items-center justify-between gap-3">
                <div className="flex items-center gap-2 text-sm text-feedback-indigo-foreground">
                    <ClipboardCheck className="w-4 h-4" />
                    <span><strong>{selectedTaskIds.length}</strong>{t('surfaces.taskBulk.selected')}</span>
                </div>
                <div className="flex flex-wrap items-center gap-2">
                    <select
                        value={effectiveAction}
                        onChange={event => {
                            setAction(event.target.value as TaskBulkAction);
                            setPreview(null);
                            setPreviewAction(null);
                        }}
                        className="text-sm border border-feedback-indigo-border rounded-md px-2 py-1 bg-surface-card"
                    >
                        {actionOptions.map(option => (
                            <option key={option.value} value={option.value}>{t(`surfaces.taskBulk.actions.${option.labelKey}`)}</option>
                        ))}
                    </select>
                    <Button size="sm" variant="secondary" onClick={onClearSelection}>
                        {t('surfaces.taskBulk.clearSelection')}
                    </Button>
                </div>
            </div>

            <div className="grid grid-cols-1 md:grid-cols-3 gap-2">
                {effectiveAction === 'set_assignee' && (
                    <select value={assigneeId} onChange={event => setAssigneeId(event.target.value)} className="text-sm border rounded-md px-2 py-2 bg-surface-card">
                        <option value="">{t('surfaces.taskBulk.chooseAssignee')}</option>
                        {teamMembers.map(member => (
                            <option key={member.id} value={member.id}>{member.name}</option>
                        ))}
                    </select>
                )}

                {effectiveAction === 'auto_assign' && (
                    <label className="text-sm text-content-primary">
                        {t('surfaces.taskBulk.minConfidence')}
                        <input
                            type="number"
                            min="0"
                            max="1"
                            step="0.05"
                            value={minConfidence}
                            onChange={event => setMinConfidence(event.target.value)}
                            className="mt-1 w-full border rounded-md px-2 py-2"
                        />
                    </label>
                )}

                {(effectiveAction === 'set_project' || effectiveAction === 'set_milestone') && scopedProjectId !== null && (
                    <div className="text-sm border border-border rounded-md px-2 py-2 bg-surface-muted text-content-primary">
                        {scopedProject?.name ?? `Project #${scopedProjectId}`}
                    </div>
                )}

                {(effectiveAction === 'set_project' || effectiveAction === 'set_milestone') && scopedProjectId === null && (
                    <select value={projectId} onChange={event => { setProjectId(event.target.value); setMilestoneId(''); }} className="text-sm border rounded-md px-2 py-2 bg-surface-card">
                        <option value="">{t('surfaces.taskBulk.chooseProject')}</option>
                        {projects.map(project => (
                            <option key={project.id} value={project.id}>{project.name}</option>
                        ))}
                    </select>
                )}

                {effectiveAction === 'set_project' && (
                    <select value={milestoneId} onChange={event => setMilestoneId(event.target.value)} className="text-sm border rounded-md px-2 py-2 bg-surface-card" disabled={!selectedProjectId}>
                        <option value="">{t('surfaces.taskBulk.leaveMilestoneUnchangedUnlessIncompatible')}</option>
                        {milestones.map(milestone => (
                            <option key={milestone.id} value={milestone.id}>{milestone.name}</option>
                        ))}
                    </select>
                )}

                {effectiveAction === 'set_milestone' && (
                    <select value={milestoneId} onChange={event => setMilestoneId(event.target.value)} className="text-sm border rounded-md px-2 py-2 bg-surface-card" disabled={!selectedProjectId}>
                        <option value="">{t('surfaces.taskBulk.chooseMilestone')}</option>
                        {milestones.map(milestone => (
                            <option key={milestone.id} value={milestone.id}>{milestone.name}</option>
                        ))}
                    </select>
                )}

                {effectiveAction === 'set_priority' && (
                    <input type="number" min="1" max="10" value={priority} onChange={event => setPriority(event.target.value)} className="text-sm border rounded-md px-2 py-2" />
                )}

                {(effectiveAction === 'add_labels' || effectiveAction === 'remove_labels') && (
                    <input
                        value={labelsText}
                        onChange={event => setLabelsText(event.target.value)}
                        placeholder={t('surfaces.taskBulk.labelsCommaSeparated')}
                        className="text-sm border rounded-md px-2 py-2 md:col-span-2"
                    />
                )}

                {effectiveAction === 'set_flags' && (
                    <>
                        <select value={isOptional} onChange={event => setIsOptional(event.target.value)} className="text-sm border rounded-md px-2 py-2 bg-surface-card">
                            <option value="">{t('surfaces.taskBulk.optionalUnchanged')}</option>
                            <option value="true">{t('surfaces.taskBulk.setOptional')}</option>
                            <option value="false">{t('surfaces.taskBulk.clearOptional')}</option>
                        </select>
                        <select value={isDeferred} onChange={event => setIsDeferred(event.target.value)} className="text-sm border rounded-md px-2 py-2 bg-surface-card">
                            <option value="">{t('surfaces.taskBulk.deferredUnchanged')}</option>
                            <option value="true">{t('surfaces.taskBulk.setDeferred')}</option>
                            <option value="false">{t('surfaces.taskBulk.clearDeferred')}</option>
                        </select>
                    </>
                )}

                {effectiveAction === 'change_status' && (
                    <>
                        <select value={status} onChange={event => setStatus(event.target.value as TaskStatus)} className="text-sm border rounded-md px-2 py-2 bg-surface-card">
                            {STATUS_OPTIONS.map(item => <option key={item} value={item}>{item}</option>)}
                        </select>
                        <input value={reason} onChange={event => setReason(event.target.value)} placeholder={t('surfaces.taskBulk.reasonOptional')} className="text-sm border rounded-md px-2 py-2" />
                    </>
                )}
            </div>

            {error && <div className="text-sm text-feedback-danger-foreground bg-feedback-danger-muted border border-feedback-danger-border rounded-md px-3 py-2">{error}</div>}

            <div className="flex flex-wrap items-center gap-2">
                <Button size="sm" variant="primary" onClick={() => run(true)} isLoading={mutation.isPending && preview?.dry_run !== false} disabled={selectedTaskIds.length === 0 || optionsLoading || Boolean(optionError)}>
                    {t('surfaces.taskBulk.preview')}
                </Button>
                <Button size="sm" variant={effectiveAction === 'delete' ? 'danger' : 'secondary'} onClick={() => run(false)} isLoading={mutation.isPending && preview?.dry_run === false} disabled={!canApply}>
                    {t('surfaces.taskBulk.applyPreview')}
                </Button>
            </div>

            {preview && (
                <div className="bg-surface-card border border-feedback-indigo-border rounded-md">
                    <div className="flex items-center justify-between px-3 py-2 border-b text-sm">
                        <span>
                            {t(preview.dry_run ? 'surfaces.taskBulk.preview' : 'surfaces.taskBulk.applied')}: {t('surfaces.taskBulk.resultSummary', { succeeded: preview.succeeded_count, failed: preview.failed_count })}
                        </span>
                    </div>
                    <div className="max-h-72 overflow-y-auto divide-y">
                        {preview.results.map(result => (
                            <div key={result.task_id} className="px-3 py-2 text-sm">
                                <div className="flex items-center gap-2">
                                    {result.outcome === 'failed' ? (
                                        <XCircle className="w-4 h-4 text-feedback-danger" />
                                    ) : (
                                        <CheckCircle2 className="w-4 h-4 text-feedback-success" />
                                    )}
                                    <span className="font-medium">{taskNameById.get(result.task_id) || t('surfaces.taskBulk.taskNumber', { id: result.task_id })}</span>
                                    <span className="text-xs text-content-secondary">{result.outcome}</span>
                                </div>
                                {result.error && <div className="mt-1 text-feedback-danger-foreground">{result.error}</div>}
                                {result.warnings.map((warning, index) => (
                                    <div key={index} className="mt-1 text-feedback-warning-foreground">{warning}</div>
                                ))}
                                {result.assignee_recommendation && (
                                    <div className="mt-1 flex items-center gap-1 text-xs text-action">
                                        <Bot className="w-3 h-3" />
                                        {result.assignee_recommendation.name} ({Math.round(result.assignee_recommendation.confidence * 100)}%): {result.assignee_recommendation.rationale}
                                    </div>
                                )}
                                {changeLines(result).map((line, index) => (
                                    <div key={index} className="mt-1 text-xs text-content-secondary">{line}</div>
                                ))}
                            </div>
                        ))}
                    </div>
                </div>
            )}

            {effectiveAction === 'delete' && (
                <div className="flex items-center gap-2 text-xs text-feedback-danger-foreground">
                    <Trash2 className="w-3 h-3" />
                    {t('surfaces.taskBulk.deleteRemovesSelectedTasksAndTheirSubtasksAfterPreviewIsApplied')}
                </div>
            )}
        </div>
    );
};

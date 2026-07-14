import { useState, useEffect, useMemo, useCallback, useRef } from 'react';
import { useQuery, useMutation, useQueryClient } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { Link } from 'react-router-dom';
import { GanttChart } from '../components/gantt/GanttChart';
import { ScheduleExplanationDetails } from '../components/gantt/ScheduleExplanationDetails';
import { TaskEditModal } from '../components/gantt/TaskEditModal';
import { iterationService } from '../services/iterationService';
import { ganttService } from '../services/ganttService';
import { taskService } from '../services/taskService';
import { Button } from '../components/common/Button';
import { ConfirmDialog } from '../components/common/ConfirmDialog';
import { Modal } from '../components/common/Modal';
import { FullscreenWorkspace } from '../components/common/FullscreenWorkspace';
import { Sparkles, Maximize2, Minimize2, FlaskConical, Undo2, Check, History } from 'lucide-react';
import { useIterationStore } from '../store/iterationStore';
import { IterationSelector } from '../components/iteration/IterationSelector';
import { PageHeader, PageLayout } from '../components/ui';
import type { ExplainScheduleResponse, GanttTask } from '../types/gantt';
import type { TaskBatchUpdateItem, TaskUpdate } from '../types/task';
import { getApiErrorMessage } from '../utils/apiError';
import clsx from 'clsx';
import { useToast } from '../components/feedback/toast';
import { snapshotService } from '../services/snapshotService';
import type { IterationSnapshot } from '../services/snapshotService';
import { getAdminAccessErrorMessage, hasAdminApiKey } from '../utils/adminAccess';
import { formatDateTime } from '../utils/formatDate';

const DECISION_COUNT_LABELS = [
    { key: 'scheduled', labelKey: 'gantt.decisionCounts.scheduled' },
    { key: 'delayed', labelKey: 'gantt.decisionCounts.delayed' },
    { key: 'reordered', labelKey: 'gantt.decisionCounts.reordered' },
    { key: 'overdue', labelKey: 'gantt.decisionCounts.overdue' },
] as const;

const applySandboxChanges = (tasks: GanttTask[], changes: Record<number, Partial<GanttTask>>): GanttTask[] => {
    return tasks.map(task => {
        let updated = { ...task };
        if (changes[task.id]) {
            updated = {
                ...updated,
                ...changes[task.id],
                isSandboxModified: true,
            };
        }
        if (task.children && task.children.length > 0) {
            updated.children = applySandboxChanges(task.children, changes);
        }
        return updated;
    });
};

// Server preview tasks already carry the applied edits; re-mark edited ids so
// the chart keeps highlighting them.
const markSandboxModified = (tasks: GanttTask[], changes: Record<number, Partial<GanttTask>>): GanttTask[] => {
    return tasks.map(task => ({
        ...task,
        ...(changes[task.id] ? { isSandboxModified: true } : {}),
        children: task.children && task.children.length > 0
            ? markSandboxModified(task.children, changes)
            : task.children,
    }));
};

const GanttPage = () => {
    const queryClient = useQueryClient();
    const { t } = useTranslation();
    const toast = useToast();
    const { selectedIterationId, setSelectedIterationId } = useIterationStore();
    const [explanation, setExplanation] = useState<{ iterationId: number; data: ExplainScheduleResponse } | null>(null);
    const [explanationError, setExplanationError] = useState<{ iterationId: number; message: string } | null>(null);
    const [isFullScreen, setIsFullScreen] = useState(false);
    const [editingExplanationTask, setEditingExplanationTask] = useState<GanttTask | null>(null);
    const [snapshotsOpen, setSnapshotsOpen] = useState(false);
    const [restoreTarget, setRestoreTarget] = useState<IterationSnapshot | null>(null);
    const [restoreError, setRestoreError] = useState<string | null>(null);
    const latestExplainIterationRef = useRef<number | null>(null);
    const fullscreenExitRef = useRef<HTMLButtonElement>(null);

    // Sandbox state
    const [sandboxMode, setSandboxMode] = useState(false);
    const [sandboxChanges, setSandboxChanges] = useState<Record<number, Partial<GanttTask>>>({});

    const { data: iterations, isLoading: iterationsLoading, isError: iterationsError, refetch: refetchIterations } = useQuery({
        queryKey: ['iterations'],
        queryFn: iterationService.getAll,
    });

    const { data: ganttTasks, isLoading: isGanttLoading, isError: ganttError, error: ganttQueryError, refetch: refetchGantt } = useQuery({
        queryKey: ['gantt', selectedIterationId],
        queryFn: () => ganttService.getChart(selectedIterationId),
        enabled: selectedIterationId > 0,
    });

    const snapshotsQuery = useQuery({
        queryKey: ['snapshots', selectedIterationId],
        queryFn: () => snapshotService.list(selectedIterationId),
        enabled: snapshotsOpen && selectedIterationId > 0,
    });

    const restoreMutation = useMutation({
        mutationFn: (snapshot: IterationSnapshot) => snapshotService.restore(selectedIterationId, snapshot.filename),
        onSuccess: async response => {
            await Promise.all([
                queryClient.invalidateQueries({ queryKey: ['snapshots', selectedIterationId] }),
                queryClient.invalidateQueries({ queryKey: ['tasks', selectedIterationId] }),
                queryClient.invalidateQueries({ queryKey: ['team', selectedIterationId] }),
                queryClient.invalidateQueries({ queryKey: ['gantt', selectedIterationId] }),
                queryClient.invalidateQueries({ queryKey: ['workload'] }),
                queryClient.invalidateQueries({ queryKey: ['projectTasks'] }),
                queryClient.invalidateQueries({ queryKey: ['projectSummary'] }),
                queryClient.invalidateQueries({ queryKey: ['projects'] }),
            ]);
            setRestoreTarget(null);
            setRestoreError(null);
            toast.success(t('snapshots.restoreSuccess', { snapshot: response.pre_restore_snapshot }));
        },
        onError: error => {
            setRestoreError(getAdminAccessErrorMessage(error, {
                missingOrInvalid: t('settings.adminAccessMissingOrInvalid'),
                backendNotConfigured: t('settings.adminAccessBackendNotConfigured'),
                fallback: t('snapshots.restoreFailed'),
            }));
        },
    });

    const currentIteration = iterations?.find(i => i.id === selectedIterationId);

    const originalTaskLookup = useMemo(() => {
        const lookup = new Map<number, GanttTask>();
        const visit = (task: GanttTask) => {
            lookup.set(task.id, task);
            task.children?.forEach(visit);
        };
        ganttTasks?.tasks?.forEach(visit);
        return lookup;
    }, [ganttTasks]);

    const sandboxChangeCount = Object.keys(sandboxChanges).length;

    // The exact payload a later "Apply changes" batch-update would send;
    // shared with the preview so the dry-run exercises the same contract.
    const buildBatchTasks = useCallback((): TaskBatchUpdateItem[] => {
        return Object.entries(sandboxChanges).map(([taskIdStr, changes]) => {
            const taskId = Number(taskIdStr);
            const originalTask = originalTaskLookup.get(taskId);
            const updatePayload: TaskUpdate = changes.sandbox_update ?? {
                title: changes.title !== undefined ? changes.title : originalTask?.title,
                description: changes.description !== undefined ? changes.description : originalTask?.description,
                project_id: changes.project_id !== undefined ? changes.project_id : originalTask?.project_id,
                priority: changes.priority !== undefined ? Number(changes.priority) : originalTask?.priority,
                effort_days: changes.effort_days !== undefined ? Number(changes.effort_days) : originalTask?.effort_days,
                effort_hours: changes.effort_hours !== undefined ? Number(changes.effort_hours) : originalTask?.effort_hours,
                assignee_id: changes.assignee !== undefined ? (changes.assignee ? Number(changes.assignee.id) : null) : originalTask?.assignee?.id,
                milestone_id: changes.milestone_id !== undefined ? (changes.milestone_id ? Number(changes.milestone_id) : null) : originalTask?.milestone_id,
                is_optional: changes.is_optional !== undefined ? changes.is_optional : originalTask?.is_optional,
                is_deferred: changes.is_deferred !== undefined ? changes.is_deferred : originalTask?.is_deferred,
                tags: changes.tags !== undefined ? changes.tags : originalTask?.tags,
                depends_on: changes.dependencies !== undefined ? changes.dependencies : originalTask?.dependencies,
                min_start_date: changes.min_start_date !== undefined ? (changes.min_start_date || null) : originalTask?.min_start_date,
                max_end_date: changes.max_end_date !== undefined ? (changes.max_end_date || null) : originalTask?.max_end_date,
            };
            if (changes.status) {
                updatePayload.status = changes.status;
            }
            return {
                task_id: taskId,
                expected_version: updatePayload.expected_version ?? changes.version ?? originalTask?.version,
                update: updatePayload,
                status_reason: changes.status ? t('gantt.sandboxStatusReason') : undefined,
            };
        });
    }, [sandboxChanges, originalTaskLookup, t]);

    // Dry-run the sandbox edits through the real backend scheduler so the
    // preview always matches what applying them would produce.
    const schedulePreviewQuery = useQuery({
        queryKey: ['gantt-schedule-preview', selectedIterationId, sandboxChanges],
        queryFn: () => ganttService.previewSchedule(selectedIterationId, buildBatchTasks()),
        enabled: sandboxMode && selectedIterationId > 0 && sandboxChangeCount > 0,
        staleTime: Infinity,
        retry: false,
    });

    const { sandboxedTasks, currentSimulationError } = useMemo(() => {
        if (!ganttTasks?.tasks) return { sandboxedTasks: [] as GanttTask[], currentSimulationError: null as string | null };
        if (!sandboxMode || sandboxChangeCount === 0) {
            return { sandboxedTasks: ganttTasks.tasks, currentSimulationError: null };
        }
        if (schedulePreviewQuery.data) {
            return {
                sandboxedTasks: markSandboxModified(schedulePreviewQuery.data.tasks, sandboxChanges),
                currentSimulationError: null,
            };
        }
        // Preview pending or failed: show local edits without projected dates.
        const tasksWithChanges = applySandboxChanges(ganttTasks.tasks, sandboxChanges);
        const errMsg = schedulePreviewQuery.isError
            ? getApiErrorMessage(schedulePreviewQuery.error, t('gantt.simulationWarning'))
            : null;
        return { sandboxedTasks: tasksWithChanges, currentSimulationError: errMsg };
    }, [
        ganttTasks,
        sandboxMode,
        sandboxChanges,
        sandboxChangeCount,
        schedulePreviewQuery.data,
        schedulePreviewQuery.isError,
        schedulePreviewQuery.error,
        t,
    ]);

    const taskLookup = useMemo(() => {
        const lookup = new Map<number, GanttTask>();
        const visit = (task: GanttTask) => {
            lookup.set(task.id, task);
            task.children?.forEach(visit);
        };
        sandboxedTasks.forEach(visit);
        return lookup;
    }, [sandboxedTasks]);

    const canExplainSchedule = selectedIterationId > 0 && Boolean(currentIteration);
    const visibleExplanation = explanation?.iterationId === selectedIterationId ? explanation.data : null;
    const visibleExplanationError = explanationError?.iterationId === selectedIterationId ? explanationError.message : null;
    const visibleEditingTask = editingExplanationTask ? taskLookup.get(editingExplanationTask.id) || null : null;

    const handleSaveSandbox = (taskId: number, changes: Partial<GanttTask>) => {
        setSandboxChanges(prev => ({
            ...prev,
            [taskId]: {
                ...prev[taskId],
                ...changes,
            }
        }));
    };

    const applySandboxMutation = useMutation({
        mutationFn: async () => {
            await taskService.batchUpdate(selectedIterationId, { tasks: buildBatchTasks() });
        },
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['gantt', selectedIterationId] });
            queryClient.invalidateQueries({ queryKey: ['tasks', selectedIterationId] });
            queryClient.invalidateQueries({ queryKey: ['projectTasks'] });
            queryClient.invalidateQueries({ queryKey: ['projectSummary'] });
            queryClient.invalidateQueries({ queryKey: ['projects'] });
            setSandboxChanges({});
            setSandboxMode(false);
            toast.success(t('feedback.ganttApplySuccess'));
        },
        onError: (err: unknown) => {
            toast.error(getApiErrorMessage(err, t('feedback.ganttApplyFailed')));
        }
    });

    const explainMutation = useMutation({
        mutationFn: (iterationId: number) => ganttService.explainSchedule(iterationId),
        onMutate: (iterationId) => {
            latestExplainIterationRef.current = iterationId;
            setExplanation(null);
            setExplanationError(null);
        },
        onSuccess: (data, iterationId) => {
            if (latestExplainIterationRef.current !== iterationId) return;
            setExplanation({ iterationId, data });
            setExplanationError(null);
        },
        onError: (error: unknown, iterationId) => {
            if (latestExplainIterationRef.current !== iterationId) return;
            setExplanation(null);
            setExplanationError({
                iterationId,
                message: getApiErrorMessage(error, t('gantt.explanationFailed')),
            });
        },
    });

    const decisionCounts = DECISION_COUNT_LABELS.map(({ key, labelKey }) => ({
        key,
        label: t(labelKey),
        count: visibleExplanation?.decisions.filter(decision => decision.decision_type === key).length ?? 0,
    }));
    const hasExplanationDetails = Boolean(
        visibleExplanation && (
            visibleExplanation.decisions.length > 0 ||
            visibleExplanation.workload_analysis.issues.length > 0
        )
    );

    useEffect(() => {
        if (iterations && iterations.length > 0) {
            const iterationExists = iterations.some(i => i.id === selectedIterationId);
            if (selectedIterationId === 0 || !iterationExists) {
                setSelectedIterationId(iterations[0].id);
            }
        }
    }, [iterations, selectedIterationId, setSelectedIterationId]);

    if (iterationsLoading) return <div className="p-6 text-content-secondary">{t('queryFeedback.loading')}</div>;
    if (iterationsError) return <div role="alert" className="rounded-md border border-feedback-danger-border bg-feedback-danger-muted p-4 text-feedback-danger-foreground"><p>{t('queryFeedback.fallback')}</p><Button className="mt-3" variant="secondary" onClick={() => void refetchIterations()}>{t('queryFeedback.retry')}</Button></div>;
    if (!iterations || iterations.length === 0) {
        return (
            <PageLayout>
                <PageHeader title={t('gantt.title')} subtitle={t('gantt.noIterationsBody')} />
                <div className="empty">
                    <h4>{t('gantt.noIterationsTitle')}</h4>
                    <p>{t('gantt.noIterationsBody')}</p>
                    <div className="empty-actions">
                        <a href="/iterations" className="btn primary">{t('gantt.goToIterations')}</a>
                    </div>
                </div>
            </PageLayout>
        );
    }

    return (
        <FullscreenWorkspace
            open={isFullScreen}
            onClose={() => setIsFullScreen(false)}
            ariaLabel={t('gantt.fullScreenLabel')}
            className="contents"
            fullscreenClassName="bg-surface-muted"
            initialFocusRef={fullscreenExitRef}
        >
        <PageLayout variant="workbench" className="flex h-full min-h-0 flex-col gap-4 overflow-hidden px-3 py-3 sm:px-4 sm:py-4">
            <div className="wc-page-head shrink-0" data-testid="page-header" style={{padding:'0 4px'}}>
                <div>
                    <div className="row" style={{gap:8, marginBottom:2}}>
                        <h1 className="wc-page-title" style={{fontSize:18}}>{t('gantt.title')}</h1>
                        {sandboxMode && <span className="pill warn"><span className="pdot"/>{t('gantt.sandboxActive')}</span>}
                        {currentIteration && <span className="muted" style={{fontSize:12}}>{currentIteration.name}</span>}
                    </div>
                    <div className="wc-page-sub">{t('gantt.description')}</div>
                </div>
                <div className="row" style={{flexWrap:'wrap', gap:6}}>
                    <IterationSelector
                        className="min-w-0 sm:min-w-60"
                        onChange={() => {
                            latestExplainIterationRef.current = null;
                            setExplanation(null);
                            setExplanationError(null);
                            setEditingExplanationTask(null);
                            setSandboxChanges({});
                            setSandboxMode(false);
                        }}
                    />
                    <Button
                        variant="secondary"
                        onClick={() => setSnapshotsOpen(true)}
                        disabled={selectedIterationId <= 0}
                    >
                        <History className="mr-2 h-4 w-4" />
                        {t('snapshots.open')}
                    </Button>
                    <Button
                        variant={sandboxMode ? "primary" : "secondary"}
                        onClick={() => { if (sandboxMode) setSandboxChanges({}); setSandboxMode(!sandboxMode); }}
                        className={clsx("justify-center transition-all duration-300", sandboxMode && "bg-feedback-warning hover:bg-feedback-warning/90 text-feedback-warning-emphasis")}
                        title={t('gantt.sandboxTooltip')}
                    >
                        <FlaskConical className="w-4 h-4 mr-2"/>
                        {sandboxMode ? t('gantt.exitSandbox') : t('gantt.sandboxMode')}
                    </Button>
                    <Button
                        variant="secondary"
                        onClick={() => explainMutation.mutate(selectedIterationId)}
                        isLoading={explainMutation.isPending}
                        disabled={!canExplainSchedule || sandboxMode}
                        className="justify-center"
                    >
                        <Sparkles className="w-4 h-4 mr-2 text-feedback-purple"/>{t('gantt.explainSchedule')}
                    </Button>
                    <Button ref={isFullScreen ? fullscreenExitRef : undefined} variant="ghost" onClick={() => setIsFullScreen(!isFullScreen)}
                        aria-label={isFullScreen ? t('actions.exitFullScreen') : t('actions.enterFullScreen')}
                        title={isFullScreen ? t('actions.exitFullScreen') : t('actions.enterFullScreen')} className="shrink-0">
                        {isFullScreen ? <Minimize2 aria-hidden="true" className="w-5 h-5"/> : <Maximize2 aria-hidden="true" className="w-5 h-5"/>}
                    </Button>
                </div>
            </div>

            {sandboxMode && (
                <div className="bg-feedback-warning-muted border border-feedback-warning-border rounded-lg p-4 animate-in fade-in slide-in-from-top-2 shrink-0 shadow-sm flex flex-col sm:flex-row sm:items-center sm:justify-between gap-4">
                    <div className="flex items-start gap-3">
                        <div className="p-2 bg-feedback-warning-muted-hover text-feedback-warning-foreground rounded-lg shrink-0">
                            <FlaskConical className="w-5 h-5 animate-pulse text-feedback-warning-foreground" />
                        </div>
                        <div>
                            <h3 className="font-semibold text-feedback-warning-foreground font-sans">{t('gantt.sandboxActive')}</h3>
                            <p className="mt-0.5 text-sm text-feedback-warning-foreground font-sans">
                                {t('gantt.sandboxBody')}
                                {Object.keys(sandboxChanges).length > 0 ? (
                                    <span className="font-bold ml-1 text-feedback-warning-foreground">
                                        {t('gantt.pendingModifications', { count: Object.keys(sandboxChanges).length })}
                                    </span>
                                ) : ` ${t('gantt.noEditsYet')}`}
                            </p>
                        </div>
                    </div>
                    <div className="flex items-center gap-2 self-end sm:self-center">
                        <Button
                            variant="secondary"
                            onClick={() => {
                                setSandboxChanges({});
                            }}
                            disabled={Object.keys(sandboxChanges).length === 0}
                            className="text-feedback-warning-foreground border-feedback-warning-border hover:bg-feedback-warning-muted-hover/50"
                        >
                            <Undo2 className="w-4 h-4 mr-2" /> {t('gantt.discardEdits')}
                        </Button>
                        <Button
                            onClick={() => applySandboxMutation.mutate()}
                            isLoading={applySandboxMutation.isPending}
                            disabled={Object.keys(sandboxChanges).length === 0}
                            className="bg-feedback-success hover:bg-feedback-success/90 text-feedback-success-emphasis ring-feedback-success"
                        >
                            <Check className="w-4 h-4 mr-2" /> {t('gantt.applyChanges')}
                        </Button>
                    </div>
                </div>
            )}

            {sandboxMode && currentSimulationError && (
                <div className="bg-feedback-danger-muted border border-feedback-danger-border rounded-lg p-4 animate-in fade-in slide-in-from-top-2 shrink-0">
                    <div className="flex items-start gap-3">
                        <span className="text-xl shrink-0">⚠️</span>
                        <div>
                            <h3 className="font-semibold text-feedback-danger-foreground font-sans">{t('gantt.simulationWarning')}</h3>
                            <p className="mt-0.5 text-sm text-feedback-danger-foreground font-sans">{currentSimulationError}</p>
                        </div>
                    </div>
                </div>
            )}

            {visibleExplanationError && (
                <div className="bg-feedback-danger-muted border border-feedback-danger-border rounded-lg p-4 animate-in fade-in slide-in-from-top-2 shrink-0">
                    <div className="flex justify-between items-start gap-4">
                        <div>
                            <h3 className="font-semibold text-feedback-danger-foreground">{t('gantt.explanationFailed')}</h3>
                            <p className="mt-1 text-sm text-feedback-danger-foreground">{visibleExplanationError}</p>
                        </div>
                        <button
                            onClick={() => setExplanationError(null)}
                            className="text-sm text-feedback-danger-foreground hover:underline"
                        >
                            {t('actions.close')}
                        </button>
                    </div>
                </div>
            )}

            {visibleExplanation && sandboxMode && (
                <div className="bg-feedback-purple-muted border border-feedback-purple-border rounded-lg p-4 animate-in fade-in shrink-0 text-sm text-feedback-purple-foreground">
                    {t('gantt.aiDisabledInSandbox')}
                </div>
            )}

            {visibleExplanation && !sandboxMode && (
                <div className="bg-feedback-purple-muted border border-feedback-purple-border rounded-lg p-4 animate-in fade-in slide-in-from-top-2 shrink-0">
                    <div className="flex justify-between items-start mb-2">
                        <h3 className="font-semibold text-feedback-purple-foreground flex items-center gap-2">
                            <Sparkles className="w-4 h-4" /> {t('gantt.aiExplanation')}
                        </h3>
                        <button onClick={() => setExplanation(null)} className="text-feedback-purple-foreground hover:underline">{t('actions.close')}</button>
                    </div>
                    <div className="space-y-3 text-sm text-feedback-purple-foreground">
                        <p className="leading-relaxed text-feedback-purple-foreground">{visibleExplanation.summary}</p>

                        <div className="flex flex-wrap items-center gap-2">
                            {(visibleExplanation.provider || visibleExplanation.model) && (
                                <span className="rounded-full bg-surface-card/80 px-2.5 py-1 text-xs text-feedback-purple-foreground ring-1 ring-feedback-purple-border">
                                    {visibleExplanation.provider || t('gantt.providerFallback')} / {visibleExplanation.model || t('gantt.modelFallback')}
                                </span>
                            )}
                            {visibleExplanation.language && (
                                <span className="rounded-full bg-surface-card/80 px-2.5 py-1 text-xs text-feedback-purple-foreground ring-1 ring-feedback-purple-border">
                                    {t('gantt.language')}: {visibleExplanation.language.toUpperCase()}
                                </span>
                            )}
                            {visibleExplanation.is_fallback && (
                                <span className="rounded-full bg-feedback-warning-muted-hover px-2.5 py-1 text-xs font-medium text-feedback-warning-foreground">
                                    {t('gantt.fallback')}
                                </span>
                            )}
                            {visibleExplanation.is_truncated && (
                                <span className="rounded-full bg-feedback-danger-muted-hover px-2.5 py-1 text-xs font-medium text-feedback-danger-foreground">
                                    {t('gantt.truncated')}
                                </span>
                            )}
                            <span className={clsx(
                                'rounded-full px-2.5 py-1 text-xs font-medium',
                                visibleExplanation.workload_analysis.balanced
                                    ? 'bg-feedback-success-muted-hover text-feedback-success-foreground'
                                    : 'bg-feedback-warning-muted-hover text-feedback-warning-foreground'
                            )}>
                                {visibleExplanation.workload_analysis.balanced ? t('gantt.workloadBalanced') : t('gantt.workloadNeedsReview')}
                            </span>
                            {decisionCounts.map(item => (
                                <span key={item.key} className="rounded-full bg-surface-card/80 px-2.5 py-1 text-xs text-feedback-purple-foreground ring-1 ring-feedback-purple-border">
                                    {item.label}: {item.count}
                                </span>
                            ))}
                        </div>

                        {(visibleExplanation.warnings?.length ?? 0) > 0 && (
                            <div className="rounded-md border border-feedback-warning-border bg-feedback-warning-muted px-3 py-2 text-xs text-feedback-warning-foreground">
                                {visibleExplanation.warnings?.map(warning => (
                                    <div key={warning}>{warning}</div>
                                ))}
                            </div>
                        )}

                        {visibleExplanation.workload_analysis.issues.length > 0 && (
                            <div>
                                <h4 className="mb-1 font-medium text-feedback-purple-foreground">{t('gantt.workloadWarnings')}</h4>
                                <ul className="list-disc space-y-1 pl-5 text-feedback-purple-foreground">
                                    {visibleExplanation.workload_analysis.issues.map((issue, index) => (
                                        <li key={`${issue}-${index}`}>{issue}</li>
                                    ))}
                                </ul>
                            </div>
                        )}

                        {!hasExplanationDetails && (
                            <p className="text-feedback-purple-foreground">{t('gantt.noExplanationDetails')}</p>
                        )}

                        <ScheduleExplanationDetails
                            decisions={visibleExplanation.decisions}
                            taskLookup={taskLookup}
                            memberVacations={ganttTasks?.member_vacations || {}}
                            workloadBalanced={visibleExplanation.workload_analysis.balanced}
                            workloadIssues={visibleExplanation.workload_analysis.issues}
                            onOpenTask={setEditingExplanationTask}
                        />
                    </div>
                </div>
            )}

            {ganttError ? (
                <div role="alert" className="rounded-md border border-feedback-danger-border bg-feedback-danger-muted p-4 text-feedback-danger-foreground">
                    <p>{getApiErrorMessage(ganttQueryError, t('queryFeedback.fallback'))}</p>
                    <Button className="mt-3" variant="secondary" onClick={() => void refetchGantt()}>{t('queryFeedback.retry')}</Button>
                </div>
            ) : isGanttLoading ? (
                <div className="flex-1 bg-surface-card rounded-lg shadow overflow-hidden animate-pulse">
                    {/* Toolbar skeleton */}
                    <div className="flex justify-between items-center p-4 border-b border-border">
                        <div className="h-6 w-40 bg-surface-hover rounded" />
                        <div className="flex gap-2">
                            <div className="h-9 w-32 bg-surface-hover rounded" />
                            <div className="h-9 w-24 bg-surface-hover rounded" />
                            <div className="h-9 w-36 bg-surface-hover rounded" />
                        </div>
                    </div>
                    {/* Chart skeleton */}
                    <div className="p-4 space-y-1">
                        {/* Header row */}
                        <div className="flex gap-px mb-2">
                            <div className="w-72 h-10 bg-surface-subtle rounded" />
                            <div className="flex-1 h-10 bg-surface-muted rounded" />
                        </div>
                        {/* Task rows */}
                        {[...Array(10)].map((_, i) => (
                            <div key={i} className="flex gap-px">
                                <div className="w-72 h-12 bg-surface-subtle rounded" />
                                <div className="flex-1 h-12 bg-surface-muted rounded relative overflow-hidden">
                                    <div
                                        className="absolute h-6 top-3 bg-surface-hover rounded"
                                        style={{
                                            left: `${10 + i * 5}%`,
                                            width: `${20 + (i % 3) * 10}%`
                                        }}
                                    />
                                </div>
                            </div>
                        ))}
                    </div>
                </div>
            ) : selectedIterationId > 0 && currentIteration && ganttTasks ? (
                <div className="flex-1 min-h-0 overflow-hidden rounded-lg shadow ring-1 ring-overlay/5">
                    <GanttChart
                        iterationId={selectedIterationId}
                        startDate={currentIteration.start_date}
                        endDate={currentIteration.end_date}
                        tasks={sandboxedTasks}
                        weekends={ganttTasks.weekends || []}
                        holidays={ganttTasks.holidays || []}
                        memberVacations={ganttTasks.member_vacations || {}}
                        sandboxMode={sandboxMode}
                        onSaveSandbox={handleSaveSandbox}
                    />
                </div>
            ) : (
                <div className="text-center py-12 text-content-tertiary bg-surface-muted rounded-lg">
                    {t('surfaces.ganttPage.selectAnIterationToViewTheGanttChart')}
                </div>
            )}

            <Modal open={snapshotsOpen} title={t('snapshots.title')} closeLabel={t('actions.close')} onClose={() => { if (!restoreMutation.isPending) setSnapshotsOpen(false); }} closeDisabled={restoreMutation.isPending}>
                {snapshotsQuery.isLoading && <p className="text-content-secondary">{t('snapshots.loading')}</p>}
                {snapshotsQuery.isError && (
                    <div role="alert" className="rounded-md border border-feedback-danger-border bg-feedback-danger-muted p-4 text-feedback-danger-foreground">
                        <p>{getApiErrorMessage(snapshotsQuery.error, t('snapshots.listFailed'))}</p>
                        <Button className="mt-3" variant="secondary" onClick={() => void snapshotsQuery.refetch()}>{t('queryFeedback.retry')}</Button>
                    </div>
                )}
                {snapshotsQuery.isSuccess && snapshotsQuery.data.length === 0 && <p className="text-content-secondary">{t('snapshots.empty')}</p>}
                {snapshotsQuery.data && snapshotsQuery.data.length > 0 && (
                    <ul className="space-y-3">
                        {snapshotsQuery.data.map(snapshot => (
                            <li key={snapshot.filename} className="flex items-center justify-between gap-4 rounded-md border border-border p-3">
                                <div className="min-w-0">
                                    <p className="truncate font-medium text-content-primary">{snapshot.filename}</p>
                                    <p className="text-sm text-content-secondary">{snapshot.created_at ? t('snapshots.created', { date: formatDateTime(snapshot.created_at) }) : t('common.unknown')}</p>
                                    <p className="text-sm text-content-secondary">{t('snapshots.reason', { reason: snapshot.reason })}</p>
                                </div>
                                <Button variant="danger" disabled={!hasAdminApiKey()} onClick={() => { setRestoreError(null); setRestoreTarget(snapshot); }}>{t('snapshots.restore')}</Button>
                            </li>
                        ))}
                    </ul>
                )}
                {!hasAdminApiKey() && (
                    <div className="mt-4 rounded-md border border-feedback-warning-border bg-feedback-warning-muted p-3 text-sm text-feedback-warning-foreground">
                        <p>{t('snapshots.adminRequired')}</p>
                        <Link className="mt-2 inline-block font-medium underline" to="/settings">{t('snapshots.goToSettings')}</Link>
                    </div>
                )}
            </Modal>

            <ConfirmDialog
                open={restoreTarget !== null}
                title={t('snapshots.restoreTitle')}
                description={<>{t('snapshots.restoreBody')}{restoreError && <span role="alert" className="mt-2 block text-feedback-danger-foreground">{restoreError}</span>}</>}
                confirmLabel={t('snapshots.restore')}
                cancelLabel={t('actions.cancel')}
                closeLabel={t('actions.close')}
                pending={restoreMutation.isPending}
                onCancel={() => { setRestoreTarget(null); setRestoreError(null); }}
                onConfirm={() => { if (restoreTarget && hasAdminApiKey()) restoreMutation.mutate(restoreTarget); }}
            />

            <TaskEditModal
                task={visibleEditingTask}
                iterationId={selectedIterationId}
                isOpen={!!visibleEditingTask}
                onClose={() => setEditingExplanationTask(null)}
                sandboxMode={sandboxMode}
                onSaveSandbox={handleSaveSandbox}
            />
        </PageLayout>
        </FullscreenWorkspace>
    );
};

export default GanttPage;

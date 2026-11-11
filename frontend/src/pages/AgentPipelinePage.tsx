import { useMemo, useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { Link, useSearchParams } from 'react-router-dom';
import {
    CheckCircle2,
    User,
    Calendar,
    Folder,
    RefreshCw,
    Terminal,
    Search,
    Clock,
    AlertTriangle
} from 'lucide-react';
import { agentService } from '../services/agentService';
import type { AgentModelTrustState, TaskTimelineItem } from '../types/agent';
import type { Task, TaskStatus } from '../types/task';
import { PageHeader, PageLayout } from '../components/ui';
import { SlideOverDrawer } from '../components/ui/SlideOverDrawer';
import { QueryEmptyState, QueryErrorState, QueryLoadingState, QueryStaleState } from '../components/feedback/QueryState';
import { AdminAccessGate } from '../components/settings/AdminAccessGate';
import { useAdminAccess, useKeylessReader } from '../hooks/useAdminAccess';
import { useAgentAccess } from '../hooks/useAgentAccess';
import { getApiErrorStatus } from '../utils/apiError';
import { protectedQueryRetry } from '../utils/protectedQueries';
import { formatDateTime } from '../utils/formatDate';
import { TaskRoutingPanel } from '../components/agent/TaskRoutingPanel';
import clsx from 'clsx';

const EMPTY_PIPELINE = {
    needs_definition: [],
    ready_to_assign: [],
    assigned_waiting: [],
    start_ready: [],
    executing: [],
    verification_required: [],
    recovery_required: [],
} satisfies Record<keyof import('../types/agent').AgentPipeline, Task[]>;

const TIMELINE_ITEM_LABELS: Record<TaskTimelineItem['item_type'], string> = {
    task_event: 'taskEvent',
    status_log: 'statusChange',
    agent_run: 'agentRun',
    agent_run_event: 'runEvent',
};

/** Stages that wait on a planning decision rather than on an agent. */
const HUMAN_GATED_STAGES: ReadonlySet<string> = new Set(['needs_definition', 'ready_to_assign', 'recovery_required']);
/** The action a row offers in each stage; all open the task's detail with routing and recovery. */
const STAGE_ACTION_KEYS: Partial<Record<string, string>> = {
    needs_definition: 'agentPipeline.actions.define',
    ready_to_assign: 'agentPipeline.actions.assign',
    recovery_required: 'agentPipeline.actions.recover',
    verification_required: 'agentPipeline.actions.review',
};

const RUN_STATUSES = new Set(['running', 'succeeded', 'failed', 'canceled']);
const MODEL_TRUST_STATES = new Set<AgentModelTrustState>([
    'matched',
    'mismatch',
    'unreported',
    'unverifiable',
]);
const TASK_STATUSES = new Set<TaskStatus>(['planned', 'active', 'resolved', 'closed']);

const safeRunStatus = (value?: string | null) => (
    value && RUN_STATUSES.has(value) ? value : 'unknown'
);

const safeModelTrustState = (value?: string | null) => (
    value && MODEL_TRUST_STATES.has(value as AgentModelTrustState)
        ? value as AgentModelTrustState
        : 'unknown'
);

const safeTaskStatus = (value: string) => (
    TASK_STATUSES.has(value as TaskStatus) ? value as TaskStatus : null
);

const safeTimelineItemLabel = (value: string) => (
    Object.prototype.hasOwnProperty.call(TIMELINE_ITEM_LABELS, value)
        ? TIMELINE_ITEM_LABELS[value as TaskTimelineItem['item_type']]
        : 'unknown'
);

export default function AgentPipelinePage() {
    const { t } = useTranslation();
    const { hasAdminKey } = useAdminAccess();
    const { hasAgentKey } = useAgentAccess();
    const hasProtectedAccess = hasAdminKey || hasAgentKey;
    // The board is a view of work, readable on the same rule as Tasks; run logs keep the key.
    const keylessReader = useKeylessReader();
    const canReadBoard = hasProtectedAccess || keylessReader.workViews;
    const [selectedTaskId, setSelectedTaskId] = useState<number | null>(null);
    const [searchParams, setSearchParams] = useSearchParams();
    const [searchQuery, setSearchQuery] = useState('');
    const [projectFilter, setProjectFilter] = useState('');
    const [agentFilter, setAgentFilter] = useState('');

    // Query pipeline tasks
    const {
        data: pipelineData,
        refetch,
        isFetching,
        isPending: pipelinePending,
        isError: pipelineIsError,
        error: pipelineError,
    } = useQuery({
        queryKey: ['agent-pipeline'],
        queryFn: agentService.getPipeline,
        enabled: canReadBoard,
        retry: protectedQueryRetry,
        refetchInterval: canReadBoard ? 5000 : false, // short-poll every 5 seconds for board
    });
    const pipelineErrorStatus = getApiErrorStatus(pipelineError);
    const pipelineAuthorizationFailed = pipelineIsError
        && (pipelineErrorStatus === 401 || pipelineErrorStatus === 403);
    const usablePipelineData = pipelineAuthorizationFailed ? undefined : pipelineData;
    const pipeline = usablePipelineData ?? EMPTY_PIPELINE;
    const allTasks = useMemo(() => {
        return [
            ...pipeline.needs_definition,
            ...pipeline.ready_to_assign,
            ...pipeline.assigned_waiting,
            ...pipeline.start_ready,
            ...pipeline.executing,
            ...pipeline.verification_required,
            ...pipeline.recovery_required,
        ];
    }, [pipeline]);
    const selectedTask = selectedTaskId === null
        ? null
        : allTasks.find(task => task.id === selectedTaskId) ?? null;

    // Query task timeline
    const { data: timelineData, error: timelineError, refetch: refetchTimeline } = useQuery({
        queryKey: ['task-timeline', selectedTask?.id],
        queryFn: () => selectedTask ? agentService.getTaskTimeline(selectedTask.id) : null,
        enabled: canReadBoard && !!selectedTask,
        retry: protectedQueryRetry,
        refetchInterval: canReadBoard && selectedTask ? 3000 : false, // short-poll every 3 seconds for active log console
    });

    // Extract active run id for the selected task if it's currently executing/running
    const activeRunId = useMemo(() => {
        if (!timelineData?.items) return null;
        // Search timeline for the latest agent_run that is either running or completed
        const runs = timelineData.items.filter(item => item.item_type === 'agent_run');
        if (runs.length === 0) return null;
        // Find if the latest run has a run_id
        const latestDoc = runs[runs.length - 1];
        const runId = latestDoc.payload.run_id;
        return typeof runId === 'number' ? runId : null;
    }, [timelineData]);

    // Query active agent run details for deep log inspection
    const { data: runDetail, error: runError, refetch: refetchRun } = useQuery({
        queryKey: ['agent-run-detail', activeRunId],
        queryFn: () => activeRunId ? agentService.getRunDetail(activeRunId) : null,
        enabled: hasProtectedAccess && !!activeRunId,
        retry: protectedQueryRetry,
        refetchInterval: hasProtectedAccess && activeRunId ? 3000 : false, // short-poll logs dynamically
    });

    // Unique options for dropdown filters
    const projectOptions = useMemo(() => {
        const set = new Set<string>();
        allTasks.forEach(t => {
            if (t.project?.name) set.add(t.project.name);
        });
        return Array.from(set).sort();
    }, [allTasks]);

    const agentOptions = useMemo(() => {
        const set = new Set<string>();
        allTasks.forEach(t => {
            if (t.claimed_by?.display_name) set.add(t.claimed_by.display_name);
            else if (t.assignee?.name) set.add(t.assignee.name);
        });
        return Array.from(set).sort();
    }, [allTasks]);

    // Filter mapping helper
    const filterAndSegment = (tasks: Task[]) => {
        return tasks.filter(task => {
            const matchesQuery = searchQuery === '' ||
                task.title.toLowerCase().includes(searchQuery.toLowerCase()) ||
                (task.description || '').toLowerCase().includes(searchQuery.toLowerCase());

            const matchesProject = projectFilter === '' ||
                (task.project?.name === projectFilter);

            const matchesAgent = agentFilter === '' ||
                (task.claimed_by?.display_name === agentFilter) ||
                (task.assignee?.name === agentFilter);

            return matchesQuery && matchesProject && matchesAgent;
        });
    };

    const columns = [
        {
            id: 'needs_definition' as const,
            title: t('agentPipeline.columns.needs_definition.title'),
            color: 'text-feedback-warning-foreground',
            bgColor: 'bg-feedback-warning-muted border-feedback-warning-border',
            tasks: filterAndSegment(pipeline.needs_definition),
            description: t('agentPipeline.columns.needs_definition.description')
        },
        {
            id: 'ready_to_assign' as const,
            title: t('agentPipeline.columns.ready_to_assign.title'),
            color: 'text-feedback-info-foreground',
            bgColor: 'bg-feedback-info-muted border-feedback-info-border',
            tasks: filterAndSegment(pipeline.ready_to_assign),
            description: t('agentPipeline.columns.ready_to_assign.description')
        },
        {
            id: 'assigned_waiting' as const,
            title: t('agentPipeline.columns.assigned_waiting.title'),
            color: 'text-content-secondary',
            bgColor: 'bg-surface-muted border-border',
            tasks: filterAndSegment(pipeline.assigned_waiting),
            description: t('agentPipeline.columns.assigned_waiting.description')
        },
        {
            id: 'start_ready' as const,
            title: t('agentPipeline.columns.start_ready.title'),
            color: 'text-feedback-indigo-foreground',
            bgColor: 'bg-feedback-indigo-muted border-feedback-indigo-border',
            tasks: filterAndSegment(pipeline.start_ready),
            description: t('agentPipeline.columns.start_ready.description')
        },
        {
            id: 'executing' as const,
            title: t('agentPipeline.columns.executing.title'),
            color: 'text-action-muted-foreground',
            bgColor: 'bg-action-muted border-action',
            tasks: filterAndSegment(pipeline.executing),
            description: t('agentPipeline.columns.executing.description')
        },
        {
            id: 'verification_required' as const,
            title: t('agentPipeline.columns.verification_required.title'),
            color: 'text-feedback-success-foreground',
            bgColor: 'bg-feedback-success-muted border-feedback-success-border',
            tasks: filterAndSegment(pipeline.verification_required),
            description: t('agentPipeline.columns.verification_required.description')
        },
        {
            id: 'recovery_required' as const,
            title: t('agentPipeline.columns.recovery_required.title'),
            color: 'text-feedback-danger-foreground',
            bgColor: 'bg-feedback-danger-muted border-feedback-danger-border',
            tasks: filterAndSegment(pipeline.recovery_required),
            description: t('agentPipeline.columns.recovery_required.description')
        }
    ];
    // The selected stage lives in the URL; by default the first stage that holds work.
    const requestedStage = searchParams.get('stage');
    const activeStage = columns.find(column => column.id === requestedStage)
        ?? columns.find(column => column.tasks.length > 0) ?? columns[0];
    const setStageParam = (stage: string) => setSearchParams(previous => {
        const next = new URLSearchParams(previous);
        next.set('stage', stage);
        return next;
    }, { replace: true });
    const filteredTaskCount = columns.reduce(
        (count, column) => count + column.tasks.length,
        0,
    );
    const runStatus = safeRunStatus(runDetail?.status);
    const modelTrustState = safeModelTrustState(runDetail?.model_trust_state);
    const modelBindingEvidence = runDetail
        && typeof runDetail.model_binding_id === 'number'
        && typeof runDetail.model_binding_revision === 'number'
        ? {
            id: runDetail.model_binding_id,
            revision: runDetail.model_binding_revision,
        }
        : null;
    const externalReferenceCount = runDetail
        ? (runDetail.commit_url ? 1 : 0)
            + (runDetail.pr_url ? 1 : 0)
            + (Array.isArray(runDetail.artifact_links) ? runDetail.artifact_links.length : 0)
        : 0;

    return (
        <PageLayout testId="agent-pipeline-page">
            <PageHeader
                title={t('agentPipeline.title')}
                subtitle={t('agentPipeline.description')}
                actions={canReadBoard ? (
                    <button className="btn" onClick={() => refetch()} disabled={isFetching}>
                    <RefreshCw className={clsx("h-4 w-4", isFetching && "animate-spin")}/>
                    {isFetching ? t('actions.refreshing') : t('actions.refresh')}
                    </button>
                ) : null}
            />
            {!canReadBoard && (
                <AdminAccessGate>
                    <span />
                </AdminAccessGate>
            )}
            {canReadBoard && !hasProtectedAccess && (
                <p className="rounded-md border border-border bg-surface-muted px-4 py-3 text-sm text-content-secondary">{t('agentPipeline.runLogsNeedKey')}</p>
            )}
            {canReadBoard && pipelinePending && !usablePipelineData && (
                <QueryLoadingState message={t('agentPipeline.loading')} />
            )}
            {canReadBoard && pipelineIsError && !usablePipelineData && (
                <QueryErrorState
                    error={pipelineError}
                    message={t('agentPipeline.pipelineUnavailable')}
                    onRetry={() => { void refetch(); }}
                />
            )}
            {canReadBoard && pipelineIsError && usablePipelineData && (
                <QueryStaleState message={t('agentPipeline.staleWarning')} onRetry={() => { void refetch(); }} />
            )}
            {canReadBoard && usablePipelineData && allTasks.length === 0 && (
                <QueryEmptyState
                    title={t('agentPipeline.emptyTitle')}
                    description={t('agentPipeline.emptyDescription')}
                />
            )}
            {canReadBoard && usablePipelineData && allTasks.length > 0 && (
            <>

            {/* Filter bar */}
            <div className="wc-toolbar">
                <div className="relative">
                    <Search className="absolute left-3 top-3 h-4 w-4 text-content-secondary" />
                    <input
                        type="text"
                        aria-label={t('agentPipeline.searchLabel')}
                        placeholder={t('agentPipeline.searchPlaceholder')}
                        value={searchQuery}
                        onChange={(e) => setSearchQuery(e.target.value)}
                        className="input with-leading-icon"
                    />
                </div>

                <div>
                    <select
                        aria-label={t('agentPipeline.filterByProject')}
                        value={projectFilter}
                        onChange={(e) => setProjectFilter(e.target.value)}
                        className="input"
                    >
                        <option value="">{t('agentPipeline.allProjects')}</option>
                        {projectOptions.map(p => (
                            <option key={p} value={p}>{p}</option>
                        ))}
                    </select>
                </div>

                <div>
                    <select
                        aria-label={t('agentPipeline.filterByAgent')}
                        value={agentFilter}
                        onChange={(e) => setAgentFilter(e.target.value)}
                        className="input"
                    >
                        <option value="">{t('agentPipeline.allAgents')}</option>
                        {agentOptions.map(a => (
                            <option key={a} value={a}>{a}</option>
                        ))}
                    </select>
                </div>

                <div className="text-right flex items-center justify-end text-xs text-content-secondary">
                    {t('agentPipeline.showingActiveTasks', { count: filteredTaskCount })}
                </div>
            </div>

            {/* One strip, left to right: the stages a task moves through. */}
            <nav aria-label={t('agentPipeline.stagesLabel')} className="overflow-x-auto">
                <ol className="flex min-w-max gap-1 xl:grid xl:min-w-0 xl:grid-cols-7">
                    {columns.map((column, index) => (
                        <li key={column.id} className="flex items-stretch">
                            <button
                                type="button"
                                aria-pressed={column.id === activeStage.id}
                                onClick={() => setStageParam(column.id)}
                                data-testid={`column-${column.id}`}
                                className={clsx(
                                    'flex min-h-16 w-full min-w-36 flex-col items-start gap-1 rounded-md border px-3 py-2 text-left text-sm focus:outline-none focus-visible:ring-2 focus-visible:ring-focus',
                                    column.id === activeStage.id ? 'border-action bg-action-muted' : 'border-border bg-surface-card hover:bg-surface-hover',
                                )}
                            >
                                <span className="flex w-full items-center justify-between gap-2">
                                    <span className="font-semibold text-content-primary">{column.title}</span>
                                    <span className="tabular-nums text-content-secondary">{column.tasks.length}</span>
                                </span>
                                {HUMAN_GATED_STAGES.has(column.id) && (
                                    <span className="rounded-full bg-feedback-warning-muted px-2 py-0.5 text-xs text-feedback-warning-foreground">{t('agentPipeline.needsDecision')}</span>
                                )}
                            </button>
                            {index < columns.length - 1 && <span aria-hidden="true" className="hidden self-center px-0.5 text-content-tertiary xl:hidden">›</span>}
                        </li>
                    ))}
                </ol>
            </nav>

            <section aria-labelledby="pipeline-stage-title" className="card card-pad space-y-3">
                <div>
                    <h3 id="pipeline-stage-title" className="text-base font-semibold">{t('agentPipeline.stageHeading', { stage: activeStage.title, count: activeStage.tasks.length })}</h3>
                    <p className="text-sm text-content-secondary">{activeStage.description}</p>
                    {HUMAN_GATED_STAGES.has(activeStage.id) && <p className="mt-1 text-sm text-feedback-warning-foreground">{t(`agentPipeline.decisionHelp.${activeStage.id}`)}</p>}
                </div>
                {activeStage.tasks.length === 0 ? (
                    <p className="text-sm text-content-secondary">{t('agentPipeline.noTasksInState')}</p>
                ) : (
                    <ul className="divide-y divide-border-subtle">
                        {activeStage.tasks.map(task => {
                            // Why the task is here, in full: its blockers, or what the stage means.
                            const reasons = task.agent_readiness?.blockers?.length ? task.agent_readiness.blockers.join(' · ') : activeStage.description;
                            const effort = task.effort_days === null || task.effort_days === undefined
                                ? t('agentPipeline.estimateUnknown')
                                : t('agentPipeline.effort', { days: t('units.daysCompact', { count: task.effort_days }) });
                            return (
                                <li key={task.id} className="flex flex-wrap items-start justify-between gap-3 py-3">
                                    <div className="min-w-0 flex-1 space-y-1">
                                        <button type="button" onClick={() => setSelectedTaskId(task.id)} data-testid={`task-card-${task.id}`}
                                            aria-label={t('agentPipeline.inspectTask', { title: task.title, state: activeStage.title })}
                                            className="break-words text-left font-medium text-action hover:underline focus:outline-none focus-visible:ring-2 focus-visible:ring-focus">
                                            {t('agentPipeline.taskNumber', { id: task.id })} · {task.title}
                                        </button>
                                        <p className="text-sm text-content-primary">{t('agentPipeline.reason', { reason: reasons })}</p>
                                        <p className="flex flex-wrap gap-x-3 text-xs text-content-secondary">
                                            {task.project && <span className="inline-flex items-center gap-1"><Folder aria-hidden="true" className="h-3.5 w-3.5" />{task.project.name}</span>}
                                            <span className="inline-flex items-center gap-1"><Calendar aria-hidden="true" className="h-3.5 w-3.5" />{effort}</span>
                                            {task.claimed_by
                                                ? <span className="inline-flex items-center gap-1"><User aria-hidden="true" className="h-3.5 w-3.5" />{t('agentPipeline.claimed', { name: task.claimed_by.display_name })}</span>
                                                : task.assignee ? <span className="inline-flex items-center gap-1"><User aria-hidden="true" className="h-3.5 w-3.5" />{task.assignee.name}</span> : null}
                                            {task.priority === 1 && <span className="rounded bg-feedback-danger-muted px-1 font-semibold text-feedback-danger-foreground">{t('agentPipeline.urgent')}</span>}
                                        </p>
                                    </div>
                                    <div className="flex shrink-0 flex-wrap gap-2">
                                        <Link to={`/tasks?task=${task.id}`} className="btn sm">{t('agentPipeline.openTask')}</Link>
                                        <button type="button" className="btn sm primary" onClick={() => setSelectedTaskId(task.id)}>
                                            {t(STAGE_ACTION_KEYS[activeStage.id] ?? 'agentPipeline.inspect')}
                                        </button>
                                    </div>
                                </li>
                            );
                        })}
                    </ul>
                )}
            </section>

            {/* Slide-over Detail & Console panel */}
                {selectedTask && (
                    <SlideOverDrawer
                        open
                        title={selectedTask.title}
                        subtitle={t('agentPipeline.taskNumber', { id: selectedTask.id })}
                        ariaLabel={selectedTask.title}
                        closeLabel={t('agentPipeline.closePanel')}
                        onClose={() => setSelectedTaskId(null)}
                        className="max-w-7xl"
                    >
                        <div className="flex h-full flex-col overflow-hidden md:flex-row" data-testid="pipeline-detail-panel">

                            {/* Left Pane: Task Fields & Timeline list */}
                            <div className="w-full md:w-1/2 p-6 overflow-y-auto border-r border-border flex flex-col gap-6 pt-16">
                                <div>
                                    <span className="text-xs font-semibold text-feedback-indigo font-mono">
                                        {t('agentPipeline.taskNumber', { id: selectedTask.id })}
                                    </span>
                                    <h2 className="text-xl font-bold text-content-primary mt-1 font-sans">
                                        {selectedTask.title}
                                    </h2>
                                    <p className="text-sm text-content-secondary mt-2 leading-relaxed bg-surface-muted p-3 rounded-lg border border-border/50 whitespace-pre-wrap font-sans">
                                        {selectedTask.description || t('agentPipeline.noDescription')}
                                    </p>
                                </div>

                                {/* Metadata fields */}
                                <div className="grid grid-cols-2 gap-4 rounded-xl border border-border p-4 bg-surface-muted/40 text-sm">
                                    <div>
                                        <p className="text-xs text-content-secondary font-semibold">{t('agentPipeline.priority')}</p>
                                        <p className="font-semibold text-content-primary mt-0.5">{t('agentPipeline.priorityValue', { priority: selectedTask.priority })}</p>
                                    </div>
                                    <div>
                                        <p className="text-xs text-content-secondary font-semibold">{t('agentPipeline.status')}</p>
                                        <p className="font-semibold text-content-primary mt-0.5">
                                            {safeTaskStatus(selectedTask.status)
                                                ? t(`statuses.${selectedTask.status}`)
                                                : t('common.unknown')}
                                        </p>
                                    </div>
                                    <div>
                                        <p className="text-xs text-content-secondary font-semibold">{t('agentPipeline.effortDays')}</p>
                                        <p className="font-semibold text-content-primary mt-0.5">{selectedTask.effort_days == null ? t('agentPipeline.estimateUnknown') : t('units.days', { count: selectedTask.effort_days })}</p>
                                    </div>
                                    <div>
                                        <p className="text-xs text-content-secondary font-semibold">{t('agentPipeline.project')}</p>
                                        <p className="font-semibold text-content-primary mt-0.5 truncate">{selectedTask.project?.name || t('common.unassigned')}</p>
                                    </div>
                                </div>

                                <TaskRoutingPanel
                                    task={selectedTask}
                                    onAssigned={() => { void refetch(); }}
                                />

                                {/* Combined Timeline */}
                                <div className="flex-1 flex flex-col gap-3">
                                    <h3 className="font-bold text-sm text-content-primary font-sans flex items-center gap-2">
                                        <Clock className="h-4 w-4 text-feedback-indigo" />
                                        {t('agentPipeline.auditTimeline')}
                                    </h3>

                                    {Boolean(timelineError) && (
                                        <QueryErrorState
                                            error={timelineError}
                                            message={t('agentPipeline.timelineUnavailable')}
                                            onRetry={() => { void refetchTimeline(); }}
                                        />
                                    )}
                                    <div className="flex-1 space-y-4 border-l-2 border-border ml-2 pl-4 py-2 mt-2 overflow-y-auto max-h-[300px]">
                                        {!timelineData?.items || timelineData.items.length === 0 ? (
                                            <p className="text-xs text-content-secondary">{t('agentPipeline.noTimeline')}</p>
                                        ) : (
                                            timelineData.items.map((item, idx) => {
                                                const timestampStr = formatDateTime(item.timestamp);
                                                const itemLabel = safeTimelineItemLabel(item.item_type);
                                                return (
                                                    <div key={idx} className="relative flex flex-col gap-0.5">
                                                        {/* Dot indicator */}
                                                        <div className="absolute -left-[21px] top-1.5 h-2 w-2 rounded-full border border-surface-card bg-border" />

                                                        <div className="flex items-center gap-2 text-xs font-semibold text-content-primary">
                                                            <span className="uppercase text-wc-micro bg-surface-muted px-1.5 py-0.5 rounded text-content-secondary font-mono">
                                                                {t(`agentPipeline.timelineItemTypes.${itemLabel}`)}
                                                            </span>
                                                            <span>{t('agentPipeline.timelineEntry')}</span>
                                                            <span className="text-wc-micro text-content-tertiary ml-auto font-mono">{timestampStr}</span>
                                                        </div>

                                                        <p className="text-xs text-content-secondary pl-1 font-sans">
                                                            {t('agentPipeline.timelineDetailsWithheld')}
                                                        </p>
                                                    </div>
                                                );
                                            })
                                        )}
                                    </div>
                                </div>
                            </div>

                            {/* Right pane: the run log for the selected task */}
                            <div className="w-full md:w-1/2 bg-surface-muted text-content-primary p-6 flex flex-col gap-4 select-text pt-16 h-full border-t md:border-t-0 md:border-l border-border">
                                {Boolean(runError) && (
                                    <QueryErrorState
                                        error={runError}
                                        message={t('agentPipeline.runUnavailable')}
                                        onRetry={() => { void refetchRun(); }}
                                    />
                                )}
                                <div className="flex items-center justify-between border-b border-border pb-3">
                                    <div className="flex items-center gap-2">
                                        <Terminal className="h-5 w-5 text-content-primary" />
                                        <span className="font-bold text-sm text-content-primary">{t('agentPipeline.consoleTitle')}</span>
                                    </div>
                                    <span className={clsx(
                                        "rounded-full px-2 py-0.5 text-wc-micro font-boldr",
                                        runDetail?.status === 'succeeded' ? "bg-feedback-success-muted text-feedback-success-foreground border border-feedback-success-border" :
                                        runDetail?.status === 'failed' ? "bg-feedback-danger-muted text-feedback-danger-foreground border border-feedback-danger-border" :
                                        runDetail?.status === 'running' ? "bg-feedback-info-muted text-feedback-info-foreground border border-feedback-info-border animate-pulse" :
                                        "bg-surface-card text-content-secondary border border-border"
                                    )}>
                                        {runDetail
                                            ? t(`agentPipeline.runStatuses.${runStatus}`)
                                            : t('agentPipeline.noActiveRun')}
                                    </span>
                                </div>

                                {/* Only bounded, non-secret run metadata is rendered in this operator view. */}
                                {runDetail && (
                                    <div className="grid grid-cols-2 gap-2 text-wc-micro p-3 rounded-lg bg-surface-card border border-border text-content-secondary">
                                        <div>
                                            <span className="text-content-tertiary font-semibold block">{t('agentPipeline.runIdentifier')}</span>
                                            <span className="text-content-primary font-semibold">#{activeRunId}</span>
                                        </div>
                                        <div>
                                            <span className="text-content-tertiary font-semibold block">{t('agentPipeline.eventCount')}</span>
                                            <span className="text-content-primary font-semibold">{runDetail.events?.length ?? 0}</span>
                                        </div>
                                        <div>
                                            <span className="text-content-tertiary font-semibold block">{t('agentPipeline.modelBindingEvidence')}</span>
                                            <span className="text-content-primary font-semibold">
                                                {modelBindingEvidence
                                                    ? t('agentPipeline.modelBindingEvidenceValue', modelBindingEvidence)
                                                    : t('agentPipeline.notReported')}
                                            </span>
                                        </div>
                                        <div>
                                            <span className="text-content-tertiary font-semibold block">{t('agentPipeline.modelTrust')}</span>
                                            <span className="text-content-primary font-semibold">
                                                {t(`agentPipeline.modelTrustStates.${modelTrustState}`)}
                                            </span>
                                        </div>
                                        <p className="col-span-2 border-t border-border/50 pt-2 text-content-tertiary" role="note">
                                            {t('agentPipeline.sensitiveRunFieldsWithheld')}
                                        </p>
                                        {externalReferenceCount > 0 && (
                                            <p className="col-span-2 text-content-tertiary" role="note">
                                                {t('agentPipeline.externalReferencesWithheld', {
                                                    count: externalReferenceCount,
                                                })}
                                            </p>
                                        )}
                                    </div>
                                )}

                                {/* Console lines Area */}
                                <div className="flex-1 bg-surface-card rounded-lg border border-border p-4 overflow-y-auto text-xs flex flex-col gap-2 shadow-inner min-h-[300px]">
                                    {!runDetail?.events || runDetail.events.length === 0 ? (
                                        <div className="flex-1 flex flex-col items-center justify-center text-center text-content-tertiary select-none py-16 gap-2">
                                            <Terminal className="h-8 w-8 opacity-40 animate-pulse" />
                                            <p className="text-xs">{t('agentPipeline.consoleOffline')}</p>
                                        </div>
                                    ) : (
                                        runDetail.events.map((evt) => {
                                            const time = formatDateTime(evt.created_at);
                                            return (
                                                <div key={evt.id} className="flex flex-col gap-1 hover:bg-surface-muted/50 py-1 px-1 rounded transition-colors group">
                                                    <div className="flex items-start gap-2">
                                                        <span className="text-content-tertiary select-none shrink-0 font-mono">[{time}]</span>
                                                        <span className="text-content-secondary select-none shrink-0 font-semibold text-wc-micro mt-0.5">
                                                            {t('agentPipeline.runEvent')}
                                                        </span>
                                                        <span className="text-content-primary break-words flex-1 font-mono font-medium leading-relaxed font-sans">
                                                            {t('agentPipeline.runEventDetailsWithheld')}
                                                        </span>
                                                    </div>
                                                </div>
                                            );
                                        })
                                    )}

                                    {/* Append running cursor if active */}
                                    {runStatus === 'running' && (
                                        <div className="flex items-center gap-1.5 text-content-secondary text-wc-micro animate-pulse py-1 font-semibold pl-1">
                                            <span className="h-1.5 w-1.5 rounded-full bg-action animate-ping" />
                                            <span>{t('agentPipeline.streaming')}</span>
                                        </div>
                                    )}

                                    {/* Output failed indicator */}
                                    {runStatus === 'failed' && (
                                        <div className="mt-4 p-3 bg-feedback-danger-muted border border-feedback-danger-border rounded-md flex items-start gap-2.5 text-feedback-danger-foreground">
                                            <AlertTriangle className="h-4.5 w-4.5 shrink-0 text-feedback-danger mt-0.5" />
                                            <div className="flex flex-col font-mono text-wc-micro">
                                                <span className="font-bold text-feedback-danger-foreground">{t('agentPipeline.outcomeFailed')}</span>
                                                <p className="text-feedback-danger-foreground mt-1 whitespace-pre-wrap">{t('agentPipeline.failureDetailsWithheld')}</p>
                                            </div>
                                        </div>
                                    )}

                                    {/* Succeeded summary indicator */}
                                    {runStatus === 'succeeded' && (
                                        <div className="mt-4 p-3 bg-feedback-success-muted border border-feedback-success-border rounded-md flex items-start gap-2.5 text-feedback-success-foreground">
                                            <CheckCircle2 className="h-4.5 w-4.5 shrink-0 text-feedback-success mt-0.5" />
                                            <div className="flex flex-col font-mono text-wc-micro">
                                                <span className="font-bold text-feedback-success-foreground">{t('agentPipeline.outcomeSuccess')}</span>
                                                <p className="text-feedback-success-foreground mt-1 whitespace-pre-wrap">{t('agentPipeline.successDetailsWithheld')}</p>
                                            </div>
                                        </div>
                                    )}
                                </div>
                            </div>
                        </div>
                    </SlideOverDrawer>
                )}
            </>
            )}
        </PageLayout>
    );
}

import { useState, useMemo } from 'react';
import { useQuery } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { motion } from 'framer-motion';
import {
    CheckCircle2,
    User,
    Calendar,
    Folder,
    RefreshCw,
    Terminal,
    ExternalLink,
    Search,
    Clock,
    AlertTriangle
} from 'lucide-react';
import { agentService } from '../services/agentService';
import type { Task } from '../types/task';
import { safeExternalHref } from '../utils/safeUrl';
import { MetricGrid, PageHeader, PageLayout } from '../components/ui';
import { SlideOverDrawer } from '../components/ui/SlideOverDrawer';
import { QueryEmptyState, QueryErrorState, QueryLoadingState, QueryStaleState } from '../components/feedback/QueryState';
import { AdminAccessGate } from '../components/settings/AdminAccessGate';
import { useAdminAccess } from '../hooks/useAdminAccess';
import { protectedQueryRetry } from '../utils/protectedQueries';
import { formatDateTime } from '../utils/formatDate';
import clsx from 'clsx';

const EMPTY_PIPELINE = {
    needs_definition: [],
    ready_for_agent: [],
    definition_ready_unassigned: [],
    assigned_waiting: [],
    start_ready: [],
    executing: [],
    verification_required: [],
    recovery_required: [],
} satisfies Record<keyof import('../types/agent').AgentPipeline, Task[]>;

export default function AgentPipelinePage() {
    const { t } = useTranslation();
    const { hasAdminKey } = useAdminAccess();
    const [selectedTask, setSelectedTask] = useState<Task | null>(null);
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
        enabled: hasAdminKey,
        retry: protectedQueryRetry,
        refetchInterval: hasAdminKey ? 5000 : false, // short-poll every 5 seconds for board
    });
    const pipeline = pipelineData ?? EMPTY_PIPELINE;

    // Query task timeline
    const { data: timelineData, error: timelineError, refetch: refetchTimeline } = useQuery({
        queryKey: ['task-timeline', selectedTask?.id],
        queryFn: () => selectedTask ? agentService.getTaskTimeline(selectedTask.id) : null,
        enabled: hasAdminKey && !!selectedTask,
        retry: protectedQueryRetry,
        refetchInterval: hasAdminKey && selectedTask ? 3000 : false, // short-poll every 3 seconds for active log console
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
        enabled: hasAdminKey && !!activeRunId,
        retry: protectedQueryRetry,
        refetchInterval: hasAdminKey && activeRunId ? 3000 : false, // short-poll logs dynamically
    });

    // Unique options for dropdown filters
    const allTasks = useMemo(() => {
        return [
            ...pipeline.needs_definition,
            ...pipeline.ready_for_agent,
            ...pipeline.assigned_waiting,
            ...pipeline.start_ready,
            ...pipeline.executing,
            ...pipeline.verification_required,
            ...pipeline.recovery_required,
        ];
    }, [pipeline]);

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
            id: 'ready_for_agent' as const,
            title: t('agentPipeline.columns.ready_for_agent.title'),
            color: 'text-action',
            bgColor: 'bg-action-muted border-action',
            tasks: filterAndSegment(pipeline.ready_for_agent),
            description: t('agentPipeline.columns.ready_for_agent.description')
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
    const filteredTaskCount = columns.reduce(
        (count, column) => count + column.tasks.length,
        0,
    );

    return (
        <PageLayout testId="agent-pipeline-page">
            <PageHeader
                title={t('agentPipeline.title')}
                subtitle={t('agentPipeline.description')}
                actions={hasAdminKey ? (
                    <button className="btn" onClick={() => refetch()} disabled={isFetching}>
                    <RefreshCw className={clsx("h-4 w-4", isFetching && "animate-spin")}/>
                    {isFetching ? t('actions.refreshing') : t('actions.refresh')}
                    </button>
                ) : null}
            />
            {!hasAdminKey && (
                <AdminAccessGate>
                    <span />
                </AdminAccessGate>
            )}
            {hasAdminKey && pipelinePending && !pipelineData && (
                <QueryLoadingState message={t('agentPipeline.loading')} />
            )}
            {hasAdminKey && pipelineIsError && !pipelineData && (
                <QueryErrorState error={pipelineError} onRetry={() => { void refetch(); }} />
            )}
            {hasAdminKey && pipelineIsError && pipelineData && (
                <QueryStaleState message={t('agentPipeline.staleWarning')} onRetry={() => { void refetch(); }} />
            )}
            {hasAdminKey && pipelineData && allTasks.length === 0 && (
                <QueryEmptyState
                    title={t('agentPipeline.emptyTitle')}
                    description={t('agentPipeline.emptyDescription')}
                />
            )}
            {hasAdminKey && pipelineData && allTasks.length > 0 && (
            <>
            <MetricGrid columns={6}>
                <div className="kpi"><div className="kpi-lbl">{t('agentPipeline.columns.needs_definition.title')}</div><div className="kpi-val tnum">{pipeline.needs_definition.length}</div></div>
                <div className="kpi"><div className="kpi-lbl">{t('agentPipeline.columns.ready_for_agent.title')}</div><div className="kpi-val tnum">{pipeline.ready_for_agent.length}</div></div>
                <div className="kpi"><div className="kpi-lbl">{t('agentPipeline.columns.verification_required.title')}</div><div className="kpi-val tnum">{pipeline.verification_required.length}</div></div>
                <div className="kpi"><div className="kpi-lbl">{t('agentPipeline.columns.start_ready.title')}</div><div className="kpi-val tnum">{pipeline.start_ready.length}</div></div>
                <div className="kpi"><div className="kpi-lbl">{t('agentPipeline.columns.executing.title')}</div><div className="kpi-val tnum">{pipeline.executing.length}</div></div>
                <div className="kpi"><div className="kpi-lbl">{t('agentPipeline.columns.recovery_required.title')}</div><div className="kpi-val tnum">{pipeline.recovery_required.length}</div></div>
            </MetricGrid>

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

            {/* Board Columns */}
            <div className="grid grid-cols-1 gap-6 md:grid-cols-2 xl:grid-cols-3 2xl:grid-cols-4">
                {columns.map(column => (
                    <div
                        key={column.id}
                        className="flex flex-col rounded-xl border border-border bg-surface-card p-4 shadow-sm min-h-[500px]"
                        data-testid={`column-${column.id}`}
                    >
                        {/* Column Header */}
                        <div className="pb-3 border-b border-border mb-4">
                            <div className="flex items-center justify-between">
                                <h3 className="font-semibold text-sm text-content-primary font-sans flex items-center gap-2">
                                    <span className={column.color}>•</span>
                                    <span>{column.title}</span>
                                </h3>
                                <span className="rounded-full bg-surface-muted px-2.5 py-0.5 text-xs font-medium text-content-secondary">
                                    {column.tasks.length}
                                </span>
                            </div>
                            <p className="text-xs text-content-secondary mt-1 leading-snug">
                                {column.description}
                            </p>
                        </div>

                        {/* Column Cards */}
                        <div className="flex-1 flex flex-col gap-3 overflow-y-auto">
                            {column.tasks.length === 0 ? (
                                <div className="flex flex-col items-center justify-center py-12 px-4 rounded-lg border border-dashed border-border text-center">
                                    <p className="text-xs text-content-secondary">{t('agentPipeline.noTasksInState')}</p>
                                </div>
                            ) : (
                                column.tasks.map(task => {
                                    const latestEvent = task.agent_readiness?.blockers?.[0] || t('agentPipeline.stateUpdated', 'State updated');
                                    return (
                                        <motion.button
                                            key={task.id}
                                            type="button"
                                            layoutId={`card-${task.id}`}
                                            onClick={() => setSelectedTask(task)}
                                            aria-label={t('agentPipeline.inspectTask', { title: task.title, state: column.title })}
                                            className="group flex w-full flex-col gap-2 rounded-lg border border-border bg-surface-muted p-3 text-left shadow-xs hover:border-feedback-indigo-border hover:shadow-md cursor-pointer transition-all duration-150 focus-visible:outline-none focus-visible:ring-2 focus-visible:ring-action focus-visible:ring-offset-2"
                                            data-testid={`task-card-${task.id}`}
                                        >
                                            <div className="flex items-start justify-between gap-2">
                                                <span className="text-[10px] uppercase tracking-wider font-semibold text-feedback-indigo">
                                                    {t('agentPipeline.taskNumber', { id: task.id })}
                                                </span>
                                                {task.priority === 1 && (
                                                    <span className="rounded bg-feedback-danger-muted px-1 text-[9px] font-bold text-feedback-danger-foreground">
                                                        {t('agentPipeline.urgent')}
                                                    </span>
                                                )}
                                            </div>

                                            <h4 className="font-medium text-sm text-content-primary leading-tight group-hover:text-feedback-indigo-foreground transition-colors">
                                                {task.title}
                                            </h4>

                                            {/* Micro fields */}
                                            <div className="flex flex-col gap-1.5 mt-1 border-t border-border/50 pt-2 text-xs text-content-secondary">
                                                {task.project && (
                                                    <div className="flex items-center gap-1">
                                                        <Folder className="h-3.5 w-3.5 shrink-0" />
                                                        <span className="truncate">{task.project.name}</span>
                                                    </div>
                                                )}
                                                <div className="flex items-center gap-1">
                                                    <Calendar className="h-3.5 w-3.5 shrink-0" />
                                                    <span>{t('agentPipeline.effort', { days: t('units.daysCompact', { count: task.effort_days }) })}</span>
                                                </div>
                                                {task.claimed_by ? (
                                                    <div className="flex items-center gap-1 text-feedback-indigo-foreground font-medium font-sans">
                                                        <User className="h-3.5 w-3.5 shrink-0" />
                                                        <span className="truncate">{t('agentPipeline.claimed', { name: task.claimed_by.display_name })}</span>
                                                    </div>
                                                ) : task.assignee ? (
                                                    <div className="flex items-center gap-1">
                                                        <User className="h-3.5 w-3.5 shrink-0" />
                                                        <span className="truncate">{task.assignee.name}</span>
                                                    </div>
                                                ) : null}
                                            </div>

                                            {/* Footer hint */}
                                            <div className="mt-1 flex items-center justify-between text-[10px] text-content-secondary bg-surface-card px-2 py-1 rounded">
                                                <span className="truncate max-w-[120px]">{latestEvent}</span>
                                                <span className="shrink-0 text-content-tertiary">{t('agentPipeline.inspect')}</span>
                                            </div>
                                        </motion.button>
                                    );
                                })
                            )}
                        </div>
                    </div>
                ))}
            </div>

            {/* Slide-over Detail & Console panel */}
                {selectedTask && (
                    <SlideOverDrawer
                        open
                        title={selectedTask.title}
                        subtitle={t('agentPipeline.taskNumber', { id: selectedTask.id })}
                        ariaLabel={selectedTask.title}
                        closeLabel={t('agentPipeline.closePanel')}
                        onClose={() => setSelectedTask(null)}
                        className="max-w-5xl"
                    >
                        <div className="flex h-full flex-col overflow-hidden md:flex-row" data-testid="pipeline-detail-panel">

                            {/* Left Pane: Task Fields & Timeline list */}
                            <div className="w-full md:w-1/2 p-6 overflow-y-auto border-r border-border flex flex-col gap-6 pt-16">
                                <div>
                                    <span className="text-xs uppercase tracking-wider font-semibold text-feedback-indigo font-mono">
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
                                        <p className="text-xs text-content-secondary uppercase tracking-wider font-semibold">{t('agentPipeline.priority')}</p>
                                        <p className="font-semibold text-content-primary mt-0.5">{t('agentPipeline.priorityValue', { priority: selectedTask.priority })}</p>
                                    </div>
                                    <div>
                                        <p className="text-xs text-content-secondary uppercase tracking-wider font-semibold">{t('agentPipeline.status')}</p>
                                        <p className="font-semibold text-content-primary uppercase mt-0.5">
                                            {t(`statuses.${selectedTask.status}`, { defaultValue: selectedTask.status })}
                                        </p>
                                    </div>
                                    <div>
                                        <p className="text-xs text-content-secondary uppercase tracking-wider font-semibold">{t('agentPipeline.effortDays')}</p>
                                        <p className="font-semibold text-content-primary mt-0.5">{t('units.days', { count: selectedTask.effort_days })}</p>
                                    </div>
                                    <div>
                                        <p className="text-xs text-content-secondary uppercase tracking-wider font-semibold">{t('agentPipeline.project')}</p>
                                        <p className="font-semibold text-content-primary mt-0.5 truncate">{selectedTask.project?.name || t('common.unassigned')}</p>
                                    </div>
                                </div>

                                {/* Combined Timeline */}
                                <div className="flex-1 flex flex-col gap-3">
                                    <h3 className="font-bold text-sm text-content-primary font-sans flex items-center gap-2">
                                        <Clock className="h-4 w-4 text-feedback-indigo" />
                                        {t('agentPipeline.auditTimeline')}
                                    </h3>

                                    {Boolean(timelineError) && (
                                        <QueryErrorState error={timelineError} onRetry={() => { void refetchTimeline(); }} />
                                    )}
                                    <div className="flex-1 space-y-4 border-l-2 border-border ml-2 pl-4 py-2 mt-2 overflow-y-auto max-h-[300px]">
                                        {!timelineData?.items || timelineData.items.length === 0 ? (
                                            <p className="text-xs text-content-secondary">{t('agentPipeline.noTimeline')}</p>
                                        ) : (
                                            timelineData.items.map((item, idx) => {
                                                const timestampStr = formatDateTime(item.timestamp);
                                                const reason = typeof item.payload.reason === 'string' ? item.payload.reason : null;
                                                const summary = typeof item.payload.summary === 'string' ? item.payload.summary : null;
                                                return (
                                                    <div key={idx} className="relative flex flex-col gap-0.5">
                                                        {/* Dot indicator */}
                                                        <div className="absolute -left-[21px] top-1.5 h-2 w-2 rounded-full border border-surface-card bg-border" />

                                                        <div className="flex items-center gap-2 text-xs font-semibold text-content-primary">
                                                            <span className="uppercase text-[10px] bg-surface-muted px-1.5 py-0.5 rounded text-content-secondary font-mono">
                                                                {item.item_type}
                                                            </span>
                                                            <span>{item.title}</span>
                                                            <span className="text-[10px] text-content-tertiary ml-auto font-mono">{timestampStr}</span>
                                                        </div>

                                                        {reason && (
                                                            <p className="text-xs text-content-secondary pl-1 italic font-sans">
                                                                &ldquo;{reason}&rdquo;
                                                            </p>
                                                        )}
                                                        {summary && (
                                                            <p className="text-xs text-content-secondary pl-1 font-sans">
                                                                {t('agentPipeline.summary', { summary })}
                                                            </p>
                                                        )}
                                                    </div>
                                                );
                                            })
                                        )}
                                    </div>
                                </div>
                            </div>

                            {/* Right Pane: rich darkness monospace Console Log Terminal */}
                            <div className="w-full md:w-1/2 bg-terminal-surface text-terminal-primary p-6 flex flex-col gap-4 font-mono select-text pt-16 h-full border-t md:border-t-0 md:border-l border-terminal-border">
                                {Boolean(runError) && (
                                    <QueryErrorState error={runError} onRetry={() => { void refetchRun(); }} />
                                )}
                                <div className="flex items-center justify-between border-b border-terminal-border pb-3">
                                    <div className="flex items-center gap-2">
                                        <Terminal className="h-5 w-5 text-terminal-primary" />
                                        <span className="font-bold text-sm tracking-wide text-terminal-primary">{t('agentPipeline.consoleTitle')}</span>
                                    </div>
                                    <span className={clsx(
                                        "rounded-full px-2 py-0.5 text-[10px] uppercase font-bold tracking-wider",
                                        runDetail?.status === 'succeeded' ? "bg-feedback-success-muted text-feedback-success-foreground border border-feedback-success-border" :
                                        runDetail?.status === 'failed' ? "bg-feedback-danger-muted text-feedback-danger-foreground border border-feedback-danger-border" :
                                        runDetail?.status === 'running' ? "bg-feedback-info-muted text-feedback-info-foreground border border-feedback-info-border animate-pulse" :
                                        "bg-terminal-canvas text-terminal-secondary border border-terminal-border"
                                    )}>
                                        {runDetail?.status
                                            ? t(`agentPipeline.runStatuses.${runDetail.status}`, { defaultValue: runDetail.status })
                                            : t('agentPipeline.noActiveRun')}
                                    </span>
                                </div>

                                {/* Active Run Metadata (Model, tool name, artifact links) */}
                                {runDetail && (
                                    <div className="grid grid-cols-2 gap-2 text-[11px] p-3 rounded-lg bg-terminal-canvas border border-terminal-border text-terminal-secondary">
                                        <div>
                                            <span className="text-terminal-muted font-semibold uppercase tracking-wider block">{t('agentPipeline.modelTarget')}</span>
                                            <span className="text-terminal-primary font-semibold">{runDetail.model || t('common.unknown')}</span>
                                        </div>
                                        <div>
                                            <span className="text-terminal-muted font-semibold uppercase tracking-wider block">{t('agentPipeline.currentTool')}</span>
                                            <span className="text-terminal-primary font-semibold">{runDetail.tool_name || t('common.unassigned')}</span>
                                        </div>
                                        {runDetail.commit_url && (
                                            <div className="col-span-2 border-t border-terminal-border/50 pt-1.5 mt-1.5 flex items-center justify-between">
                                                <span className="text-terminal-muted">{t('agentPipeline.githubCommit')}</span>
                                                <a href={safeExternalHref(runDetail.commit_url)} target="_blank" rel="noopener noreferrer" className="text-terminal-primary hover:text-terminal-secondary hover:underline flex items-center gap-1">
                                                    {t('agentPipeline.openCommit')} <ExternalLink className="h-3 w-3" />
                                                </a>
                                            </div>
                                        )}
                                        {runDetail.pr_url && (
                                            <div className="col-span-2 border-t border-terminal-border/50 pt-1 flex items-center justify-between">
                                                <span className="text-terminal-muted">{t('agentPipeline.pullRequest')}</span>
                                                <a href={safeExternalHref(runDetail.pr_url)} target="_blank" rel="noopener noreferrer" className="text-terminal-primary hover:text-terminal-secondary hover:underline flex items-center gap-1">
                                                    {t('agentPipeline.reviewPr')} <ExternalLink className="h-3 w-3" />
                                                </a>
                                            </div>
                                        )}
                                        {runDetail.artifact_links && runDetail.artifact_links.length > 0 && (
                                            <div className="col-span-2 border-t border-terminal-border/50 pt-1 text-terminal-secondary">
                                                <span className="text-terminal-muted font-semibold block uppercase tracking-wider">{t('agentPipeline.producedArtifacts')}</span>
                                                <ul className="list-disc pl-4 space-y-1 mt-1 text-[10px]">
                                                    {runDetail.artifact_links.map((link, idx) => (
                                                        <li key={idx}>
                                                            <a href={safeExternalHref(link)} target="_blank" rel="noopener noreferrer" className="text-terminal-primary hover:text-terminal-secondary hover:underline break-all">
                                                                {link}
                                                            </a>
                                                        </li>
                                                    ))}
                                                </ul>
                                            </div>
                                        )}
                                    </div>
                                )}

                                {/* Console lines Area */}
                                <div className="flex-1 bg-terminal-canvas rounded-lg border border-terminal-border p-4 overflow-y-auto text-xs flex flex-col gap-2 shadow-inner min-h-[300px]">
                                    {!runDetail?.events || runDetail.events.length === 0 ? (
                                        <div className="flex-1 flex flex-col items-center justify-center text-center text-terminal-muted select-none py-16 gap-2">
                                            <Terminal className="h-8 w-8 opacity-40 animate-pulse" />
                                            <p className="text-xs">{t('agentPipeline.consoleOffline')}</p>
                                        </div>
                                    ) : (
                                        runDetail.events.map((evt) => {
                                            const time = formatDateTime(evt.created_at);
                                            return (
                                                <div key={evt.id} className="flex flex-col gap-1 hover:bg-terminal-surface/50 py-1 px-1 rounded transition-colors group">
                                                    <div className="flex items-start gap-2">
                                                        <span className="text-terminal-muted select-none shrink-0 font-mono">[{time}]</span>
                                                        <span className="text-terminal-secondary select-none shrink-0 font-semibold uppercase tracking-wider text-[10px] mt-0.5">
                                                            {evt.event_type}
                                                        </span>
                                                        <span className="text-terminal-primary break-words flex-1 font-mono font-medium leading-relaxed font-sans">
                                                            {evt.message}
                                                        </span>
                                                    </div>
                                                    {evt.payload && Object.keys(evt.payload).length > 0 && (
                                                        <pre className="text-[10px] text-terminal-secondary bg-terminal-surface/20 p-2 rounded border border-terminal-border pl-8 overflow-x-auto whitespace-pre-wrap break-all">
                                                            {JSON.stringify(evt.payload, null, 2)}
                                                        </pre>
                                                    )}
                                                </div>
                                            );
                                        })
                                    )}

                                    {/* Append running cursor if active */}
                                    {runDetail?.status === 'running' && (
                                        <div className="flex items-center gap-1.5 text-terminal-secondary text-[11px] animate-pulse py-1 font-semibold pl-1">
                                            <span className="h-1.5 w-1.5 rounded-full bg-terminal-primary animate-ping" />
                                            <span>{t('agentPipeline.streaming')}</span>
                                        </div>
                                    )}

                                    {/* Output failed indicator */}
                                    {runDetail?.status === 'failed' && (
                                        <div className="mt-4 p-3 bg-feedback-danger-muted border border-feedback-danger-border rounded-md flex items-start gap-2.5 text-feedback-danger-foreground">
                                            <AlertTriangle className="h-4.5 w-4.5 shrink-0 text-feedback-danger mt-0.5" />
                                            <div className="flex flex-col font-mono text-[11px]">
                                                <span className="font-bold text-feedback-danger-foreground">{t('agentPipeline.outcomeFailed')}</span>
                                                <p className="text-feedback-danger-foreground mt-1 whitespace-pre-wrap">{runDetail.error || t('agentPipeline.unknownRuntimeError')}</p>
                                            </div>
                                        </div>
                                    )}

                                    {/* Succeeded summary indicator */}
                                    {runDetail?.status === 'succeeded' && (
                                        <div className="mt-4 p-3 bg-feedback-success-muted border border-feedback-success-border rounded-md flex items-start gap-2.5 text-feedback-success-foreground">
                                            <CheckCircle2 className="h-4.5 w-4.5 shrink-0 text-feedback-success mt-0.5" />
                                            <div className="flex flex-col font-mono text-[11px]">
                                                <span className="font-bold text-feedback-success-foreground">{t('agentPipeline.outcomeSuccess')}</span>
                                                <p className="text-feedback-success-foreground mt-1 whitespace-pre-wrap">{runDetail.summary || t('agentPipeline.successSummary')}</p>
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

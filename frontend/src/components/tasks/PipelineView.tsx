import { TaskAssigneeDisplay } from './TaskAssigneeDisplay';
import { useTranslation } from 'react-i18next';
import { useSearchParams } from 'react-router-dom';
import { Calendar, Folder } from 'lucide-react';
import clsx from 'clsx';
import type { Task } from '../../types/task';
import { priorityChipClassName } from '../ui/tone';
import { AdminAccessGate } from '../settings/AdminAccessGate';
import { QueryErrorState, QueryLoadingState, QueryStaleState } from '../feedback/QueryState';
import { InlineEmptyState } from '../ui/InlineEmptyState';
import { Button } from '../common/Button';
import { NextStepEmptyState } from '../../features/firstRun/NextStepEmptyState';
import { firstRunPlanHref } from '../../features/firstRun/firstRunSteps';
import { useScopeLink } from '../../features/scope/useScopeLink';
import { usePipeline } from './usePipeline';
import { taskMatchesFilters } from '../../utils/taskFilters';
import { pipelineTasksInScope } from '../../features/overview/overviewSignals';
import type { TaskFilters } from './TaskFiltersBar';
import type { LabelGroup } from '../../types/label';
import type { ScopeIteration, ScopeProject } from '../../features/scope/workScope';

/** Stages that wait on a planning decision rather than on an agent. */
const HUMAN_GATED_STAGES: ReadonlySet<string> = new Set(['needs_definition', 'ready_to_assign', 'recovery_required']);
/** The action a row offers in each stage; all open the task's detail with routing and recovery. */
const STAGE_ACTION_KEYS: Partial<Record<string, string>> = {
    needs_definition: 'agentPipeline.actions.define',
    ready_to_assign: 'agentPipeline.actions.assign',
    recovery_required: 'agentPipeline.actions.recover',
    verification_required: 'agentPipeline.actions.review',
};

export function PipelineView({ query, project, iteration, search, agent, filters, labelGroups, onOpenTask, hasActiveFilters = false, onClearFilters }: {
    query: ReturnType<typeof usePipeline>;
    project: ScopeProject | undefined;
    iteration: ScopeIteration | undefined;
    search: string;
    agent: string;
    filters: TaskFilters;
    labelGroups: LabelGroup[];
    onOpenTask: (task: Task) => void;
    hasActiveFilters?: boolean;
    onClearFilters?: () => void;
}) {
    const scopeLink = useScopeLink();
    const { t } = useTranslation();
    const [params, setParams] = useSearchParams();
    const { pipeline, canRead, usableData, isPending, isError, error, refetch } = query;
    const filterAndSegment = (tasks: Task[]) => pipelineTasksInScope(tasks, project, iteration).filter(task => (
        (!agent || task.claimed_by?.display_name === agent || task.assignee?.name === agent)
        && (!search || `${task.title} ${task.description ?? ''}`.toLowerCase().includes(search.toLowerCase()))
        && taskMatchesFilters(task, filters, labelGroups)
    ));
    const columns = [
        {
            id: 'needs_definition' as const,
            title: t('agentPipeline.columns.needs_definition.title'),
            tasks: filterAndSegment(pipeline.needs_definition),
            description: t('agentPipeline.columns.needs_definition.description')
        },
        {
            id: 'ready_to_assign' as const,
            title: t('agentPipeline.columns.ready_to_assign.title'),
            tasks: filterAndSegment(pipeline.ready_to_assign),
            description: t('agentPipeline.columns.ready_to_assign.description')
        },
        {
            id: 'assigned_waiting' as const,
            title: t('agentPipeline.columns.assigned_waiting.title'),
            tasks: filterAndSegment(pipeline.assigned_waiting),
            description: t('agentPipeline.columns.assigned_waiting.description')
        },
        {
            id: 'start_ready' as const,
            title: t('agentPipeline.columns.start_ready.title'),
            tasks: filterAndSegment(pipeline.start_ready),
            description: t('agentPipeline.columns.start_ready.description')
        },
        {
            id: 'executing' as const,
            title: t('agentPipeline.columns.executing.title'),
            tasks: filterAndSegment(pipeline.executing),
            description: t('agentPipeline.columns.executing.description')
        },
        {
            id: 'verification_required' as const,
            title: t('agentPipeline.columns.verification_required.title'),
            tasks: filterAndSegment(pipeline.verification_required),
            description: t('agentPipeline.columns.verification_required.description')
        },
        {
            id: 'recovery_required' as const,
            title: t('agentPipeline.columns.recovery_required.title'),
            tasks: filterAndSegment(pipeline.recovery_required),
            description: t('agentPipeline.columns.recovery_required.description')
        }
    ];
    // The selected stage lives in the URL; by default the first stage that holds work.
    const requestedStage = params.get('stage');
    const activeStage = columns.find(column => column.id === requestedStage)
        ?? columns.find(column => column.tasks.length > 0) ?? columns[0];
    const setStageParam = (stage: string) => setParams(previous => {
        const next = new URLSearchParams(previous);
        next.set('stage', stage);
        return next;
    }, { replace: true });
    const filteredTaskCount = columns.reduce(
        (count, column) => count + column.tasks.length,
        0,
    );
    // Nothing visible: the stage's list gives way to the empty state, with one action. Clear filters when filters hide
    // the work; otherwise (no agent work at all yet) the first-run step that brings work in. The stage strip stays.
    const showEmpty = usableData && filteredTaskCount === 0;
    const noAgentWork = Object.values(pipeline).every(tasks => tasks.length === 0);
    const emptyState = noAgentWork || !hasActiveFilters || !onClearFilters ? (
        <NextStepEmptyState
            title={t('agentPipeline.emptyTitle')}
            description={t('emptyStates.pipeline.body')}
            fallback={{ label: t('firstRun.steps.tasks.title'), to: scopeLink(firstRunPlanHref('work')) }}
        />
    ) : (
        <InlineEmptyState
            headingLevel={2}
            title={t('emptyStates.filtered.title')}
            description={t('emptyStates.filtered.body')}
            actions={<Button variant="secondary" onClick={onClearFilters}>{t('emptyStates.filtered.clear')}</Button>}
        />
    );
    if (!canRead) return <AdminAccessGate><span /></AdminAccessGate>;
    if (isPending && !usableData) return <QueryLoadingState message={t('agentPipeline.loading')} />;
    if (isError && !usableData) return <QueryErrorState error={error} message={t('agentPipeline.pipelineUnavailable')} onRetry={() => { void refetch(); }} />;

    return <div className="space-y-4" data-testid="pipeline-view">
        {isError && usableData && <QueryStaleState message={t('agentPipeline.staleWarning')} onRetry={() => { void refetch(); }} />}
        <p className="text-xs text-content-secondary" role="status">{t('agentPipeline.showingActiveTasks', { count: filteredTaskCount })}</p>
            {/* One strip, left to right: the stages a task moves through. */}
            <nav aria-label={t('agentPipeline.stagesLabel')} className="overflow-x-auto">
                <ol className="flex min-w-max gap-1 xl:grid xl:min-w-0 xl:grid-cols-7">
                    {columns.map((column, index) => (
                        <li key={column.id} className="flex items-stretch">
                            <button
                                data-page-chrome-control="button" type="button"
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

            {showEmpty ? emptyState : (
            <section aria-labelledby="pipeline-stage-title" className="card card-pad space-y-3">
                <div>
                    <h2 id="pipeline-stage-title" className="text-base font-semibold">{t('agentPipeline.stageHeading', { stage: activeStage.title, count: activeStage.tasks.length })}</h2>
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
                                        <button data-page-chrome-control="button" type="button" onClick={() => onOpenTask(task)} data-testid={`task-card-${task.id}`}
                                            aria-label={t('agentPipeline.inspectTask', { title: task.title, state: activeStage.title })}
                                            className="break-words text-left font-medium text-action hover:underline focus:outline-none focus-visible:ring-2 focus-visible:ring-focus">
                                            {t('agentPipeline.taskNumber', { id: task.id })} · {task.title}
                                        </button>
                                        <p className="text-sm text-content-primary">{t('agentPipeline.reason', { reason: reasons })}</p>
                                        <p className="flex flex-wrap gap-x-3 text-xs text-content-secondary">
                                            {task.project && <span className="inline-flex items-center gap-1"><Folder aria-hidden="true" className="h-3.5 w-3.5" />{task.project.name}</span>}
                                            <span className="inline-flex items-center gap-1"><Calendar aria-hidden="true" className="h-3.5 w-3.5" />{effort}</span>
                                            <TaskAssigneeDisplay task={task} iterationId={task.iteration_id} />
                                            {task.priority === 1 && <span className={`rounded px-1 ${priorityChipClassName(task.priority)}`}>{t('agentPipeline.urgent')}</span>}
                                        </p>
                                    </div>
                                    <div className="flex shrink-0 flex-wrap gap-2">
                                        <button data-page-chrome-control="button" type="button" className="btn sm" onClick={() => onOpenTask(task)}>{t('agentPipeline.openTask')}</button>
                                        <button data-page-chrome-control="button" type="button" className="btn sm" onClick={() => onOpenTask(task)}>
                                            {t(STAGE_ACTION_KEYS[activeStage.id] ?? 'agentPipeline.inspect')}
                                        </button>
                                    </div>
                                </li>
                            );
                        })}
                    </ul>
                )}
            </section>
            )}
    </div>;
}

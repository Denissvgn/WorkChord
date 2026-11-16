import { useMemo } from 'react';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { CheckCircle2, Clock, Terminal, AlertTriangle } from 'lucide-react';
import clsx from 'clsx';
import { agentService } from '../../services/agentService';
import type { AgentModelTrustState, TaskTimelineItem } from '../../types/agent';
import type { Task } from '../../types/task';
import { useAdminAccess } from '../../hooks/useAdminAccess';
import { useAgentAccess } from '../../hooks/useAgentAccess';
import { protectedQueryRetry } from '../../utils/protectedQueries';
import { getApiErrorStatus } from '../../utils/apiError';
import { formatDateTime } from '../../utils/formatDate';
import { QueryErrorState } from '../feedback/QueryState';
import { TaskRoutingPanel } from '../agent/TaskRoutingPanel';

const TIMELINE_ITEM_LABELS: Record<TaskTimelineItem['item_type'], string> = {
    task_event: 'taskEvent',
    status_log: 'statusChange',
    agent_run: 'agentRun',
    agent_run_event: 'runEvent',
};

const RUN_STATUSES = new Set(['running', 'succeeded', 'failed', 'canceled']);
const MODEL_TRUST_STATES = new Set<AgentModelTrustState>([
    'matched',
    'mismatch',
    'unreported',
    'unverifiable',
]);


const safeRunStatus = (value?: string | null) => (
    value && RUN_STATUSES.has(value) ? value : 'unknown'
);

const safeModelTrustState = (value?: string | null) => (
    value && MODEL_TRUST_STATES.has(value as AgentModelTrustState)
        ? value as AgentModelTrustState
        : 'unknown'
);

const safeTimelineItemLabel = (value: string) => (
    Object.prototype.hasOwnProperty.call(TIMELINE_ITEM_LABELS, value)
        ? TIMELINE_ITEM_LABELS[value as TaskTimelineItem['item_type']]
        : 'unknown'
);

export function PipelineTaskEvidence({ task: selectedTask }: { task: Task }) {
    const { t } = useTranslation();
    const { hasAdminKey } = useAdminAccess();
    const { hasAgentKey } = useAgentAccess();
    const hasProtectedAccess = hasAdminKey || hasAgentKey;
    const queryClient = useQueryClient();
    // feedback-policy: query loading,error,retry,empty - optional evidence uses an empty placeholder and explicit error/retry feedback.
    const { data: cachedTimelineData, error: timelineError, refetch: refetchTimeline } = useQuery({
        queryKey: ['task-timeline', selectedTask?.id],
        queryFn: () => selectedTask ? agentService.getTaskTimeline(selectedTask.id) : null,
        enabled: hasProtectedAccess && !!selectedTask,
        retry: protectedQueryRetry,
        refetchInterval: hasProtectedAccess && selectedTask ? 3000 : false, // short-poll every 3 seconds for active log console
    });
    const timelineStatus = getApiErrorStatus(timelineError);
    const timelineData = hasProtectedAccess && timelineStatus !== 401 && timelineStatus !== 403
        ? cachedTimelineData : undefined;

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

    // feedback-policy: query loading,error,retry,empty - optional run evidence uses offline feedback and explicit error/retry feedback.
    const { data: cachedRunDetail, error: runError, refetch: refetchRun } = useQuery({
        queryKey: ['agent-run-detail', activeRunId],
        queryFn: () => activeRunId ? agentService.getRunDetail(activeRunId) : null,
        enabled: hasProtectedAccess && !!activeRunId,
        retry: protectedQueryRetry,
        refetchInterval: hasProtectedAccess && activeRunId ? 3000 : false, // short-poll logs dynamically
    });
    const runErrorStatus = getApiErrorStatus(runError);
    const runDetail = hasProtectedAccess && activeRunId && runErrorStatus !== 401 && runErrorStatus !== 403
        ? cachedRunDetail : undefined;

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

    return <div className="space-y-6">
        <TaskRoutingPanel task={selectedTask} onAssigned={() => { void queryClient.invalidateQueries({ queryKey: ['agent-pipeline'] }); }} />
        {hasProtectedAccess && <details className="space-y-4">
            <summary className="cursor-pointer text-sm font-medium text-content-primary">{t('agentPipeline.consoleTitle')}</summary>
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
                            <div className="flex flex-col gap-4 select-text">
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
        </details>}
    </div>;
}

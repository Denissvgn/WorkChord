import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { taskService } from '../services/taskService';
import { iterationService } from '../services/iterationService';
import { WorkMetricsLine } from '../components/tasks/WorkMetricsLine';
import { TaskStatusFlow } from '../components/analytics/TaskStatusFlow';
import { ExecutionUsagePanel } from '../components/analytics/ExecutionUsagePanel';
import { Select } from '../components/common/Select';
import { DeliveryAnalytics } from '../components/analytics/DeliveryAnalytics';
import { OnTrackSummary } from '../components/analytics/OnTrackSummary';
import { StatusDistribution } from '../components/analytics/StatusDistribution';
import { SavedViewDashboardCards } from '../components/dashboard/SavedViewDashboardCards';
import { PageHeader, PageLayout, PageToolbar } from '../components/ui';
import { QueryErrorState } from '../components/feedback/QueryState';
import { useWorkScope } from '../features/scope/useWorkScope';
import type { TaskStatusLog } from '../types/task';

interface HistoryGroup { taskTitle: string; logs: TaskStatusLog[]; }

const AnalyticsPage = () => {
    const { iteration } = useWorkScope();
    const [days, setDays] = useState(30);
    const selectedIterationId = typeof iteration === 'number' ? iteration : 0;
    const { t } = useTranslation();


    // feedback-policy: query loading,error,retry,empty
    const {
        data: history,
        error: historyError,
        isError: isHistoryError,
        isLoading: isLoadingHistory,
        refetch: refetchHistory,
    } = useQuery({
        queryKey: ['iteration-history', selectedIterationId],
        queryFn: () => taskService.getIterationHistory(selectedIterationId),
        enabled: selectedIterationId > 0,
    });

    // feedback-policy: query loading,error,retry,empty
    const summaryQuery = useQuery({ queryKey: ['iterationSummary', selectedIterationId],
        queryFn: () => iterationService.getSummary(selectedIterationId), enabled: selectedIterationId > 0 });

    const groupedHistory = history?.reduce<Record<number, HistoryGroup>>((acc, log) => {
        if (!acc[log.task_id]) acc[log.task_id] = { taskTitle: log.task_title || `Task #${log.task_id}`, logs: [] };
        acc[log.task_id].logs.push(log);
        return acc;
    }, {});

    const summary = summaryQuery.data;
    return (
        <PageLayout>
            <PageHeader title={t('analytics.title')} purpose={t('analytics.purpose')} />
            <PageToolbar label={t('analytics.title')} viewOptions={<Select label={t('deliveryAnalytics.window')} value={days} onChange={event => setDays(Number(event.target.value))}>
                {[30, 90, 180, 366].map(value => <option key={value} value={value}>{t('deliveryAnalytics.days', { count: value })}</option>)}
            </Select>} />
            {selectedIterationId === 0 && <p>{t('analytics.selectIteration')}</p>}

            {summaryQuery.isLoading && <p role="status">{t('common.loading')}</p>}
            {summaryQuery.isError && <QueryErrorState error={summaryQuery.error} onRetry={() => { void summaryQuery.refetch(); }} />}
            {summary && <div className="space-y-5">
                <OnTrackSummary summary={summary} />
                <StatusDistribution summary={summary} />
                <WorkMetricsLine metrics={summary} scope={{ iteration_id: selectedIterationId }} />
            </div>}

            <DeliveryAnalytics days={days} />
            {selectedIterationId > 0 ? <ExecutionUsagePanel key={selectedIterationId + "-" + days} scope={{ iteration_id: selectedIterationId, lookback_days: days }} /> :
                <section aria-labelledby="usage-title"><h2 id="usage-title" className="font-semibold">{t('executionUsage.title')}</h2><p>{t('deliveryAnalytics.unavailableScope')}</p></section>}
            {selectedIterationId > 0 && <SavedViewDashboardCards iterationId={selectedIterationId} title={t('analytics.savedViewDashboard')}/>}

            {isHistoryError && (
                <QueryErrorState error={historyError} onRetry={() => { void refetchHistory(); }} />
            )}

            {selectedIterationId > 0 && <section className="card" aria-labelledby="task-lifecycle-title">
                <div className="card-head"><h2 id="task-lifecycle-title">{t('analytics.taskLifecycle')}</h2></div>
                <div className="card-pad">
                    {isLoadingHistory ? (
                        <p role="status" className="muted py-8 text-center">{t('analytics.loadingHistory')}</p>
                    ) : isHistoryError ? null : groupedHistory && Object.keys(groupedHistory).length > 0 ? (
                        <div className="space-y-5">
                            {Object.entries(groupedHistory).map(([taskId, group]) => (
                                <TaskStatusFlow key={taskId} taskId={Number(taskId)} title={group.taskTitle} logs={group.logs} />
                            ))}
                        </div>
                    ) : (
                        <p className="muted py-8 text-center">{t('analytics.noTransitions')}</p>
                    )}
                </div>
            </section>}
        </PageLayout>
    );
};

export default AnalyticsPage;

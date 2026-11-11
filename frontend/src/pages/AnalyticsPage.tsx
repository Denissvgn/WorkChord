import { useQuery } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { taskService } from '../services/taskService';
import { iterationService } from '../services/iterationService';
import { WorkMetricsLine } from '../components/tasks/WorkMetricsLine';
import { TaskStatusFlow } from '../components/analytics/TaskStatusFlow';
import { DeliveryAnalytics } from '../components/analytics/DeliveryAnalytics';
import { OnTrackSummary } from '../components/analytics/OnTrackSummary';
import { StatusDistribution } from '../components/analytics/StatusDistribution';
import { SavedViewDashboardCards } from '../components/dashboard/SavedViewDashboardCards';
import { PageHeader, PageLayout } from '../components/ui';
import { QueryErrorState } from '../components/feedback/QueryState';
import { useIterationStore } from '../store/iterationStore';
import { formatDate } from '../utils/formatDate';
import type { TaskStatusLog } from '../types/task';

interface HistoryGroup { taskTitle: string; logs: TaskStatusLog[]; }

const AnalyticsPage = () => {
    const { selectedIterationId } = useIterationStore();
    const { t, i18n } = useTranslation();
    const locale = i18n.resolvedLanguage ?? i18n.language;

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

    if (selectedIterationId === 0) {
        return (
            <PageLayout>
                <PageHeader title={t('analytics.title')} subtitle={t('analytics.selectIteration')} />
                <DeliveryAnalytics />
            </PageLayout>
        );
    }

    const summary = summaryQuery.data;
    // The subtitle names the scope the page answers for.
    const subtitle = summary
        ? t('analytics.scope', { name: summary.name, start: formatDate(summary.start_date, locale), end: formatDate(summary.end_date, locale) })
        : t('analytics.scopeLoading');

    return (
        <PageLayout>
            <PageHeader title={t('analytics.title')} subtitle={subtitle} />

            {summaryQuery.isLoading && <p role="status">{t('common.loading')}</p>}
            {summaryQuery.isError && <QueryErrorState error={summaryQuery.error} onRetry={() => { void summaryQuery.refetch(); }} />}
            {summary && <div className="space-y-5">
                <OnTrackSummary summary={summary} />
                <StatusDistribution summary={summary} />
                <WorkMetricsLine metrics={summary} scope={{ iteration_id: selectedIterationId }} />
            </div>}

            <DeliveryAnalytics iterationId={selectedIterationId} />
            <SavedViewDashboardCards iterationId={selectedIterationId} title={t('analytics.savedViewDashboard')}/>

            {isHistoryError && (
                <QueryErrorState error={historyError} onRetry={() => { void refetchHistory(); }} />
            )}

            <section className="card" aria-labelledby="task-lifecycle-title">
                <div className="card-head"><h3 id="task-lifecycle-title">{t('analytics.taskLifecycle')}</h3></div>
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
            </section>
        </PageLayout>
    );
};

export default AnalyticsPage;

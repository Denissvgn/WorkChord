import { useQuery } from '@tanstack/react-query';
import { useNavigate } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { taskService } from '../services/taskService';
import { NotificationsPanel } from '../components/notifications/NotificationsPanel';
import { TaskStatusFlow } from '../components/analytics/TaskStatusFlow';
import { SavedViewDashboardCards } from '../components/dashboard/SavedViewDashboardCards';
import { PageHeader, PageLayout } from '../components/ui';
import { QueryErrorState } from '../components/feedback/QueryState';
import { useIterationStore } from '../store/iterationStore';
import type { TaskStatusLog } from '../types/task';

interface HistoryGroup { taskTitle: string; logs: TaskStatusLog[]; }

const AnalyticsPage = () => {
    const { selectedIterationId } = useIterationStore();
    const navigate = useNavigate();
    const { t } = useTranslation();

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

    const groupedHistory = history?.reduce<Record<number, HistoryGroup>>((acc, log) => {
        if (!acc[log.task_id]) acc[log.task_id] = { taskTitle: log.task_title || `Task #${log.task_id}`, logs: [] };
        acc[log.task_id].logs.push(log);
        return acc;
    }, {});

    if (selectedIterationId === 0) {
        return (
            <PageLayout>
                <PageHeader
                    title={t('analytics.title')}
                    subtitle={t('analytics.selectIteration')}
                    actions={<button className="btn" onClick={() => navigate('/')}>{t('actions.backToTasks')}</button>}
                />
            </PageLayout>
        );
    }

    return (
        <PageLayout>
            <PageHeader
                title={t('analytics.title')}
                subtitle={t('analytics.taskLifecycle')}
                actions={<button className="btn" onClick={() => navigate('/')}>{t('actions.backToTasks')}</button>}
            />

            <SavedViewDashboardCards iterationId={selectedIterationId} title={t('analytics.savedViewDashboard')}/>

            {isHistoryError && (
                <QueryErrorState error={historyError} onRetry={() => { void refetchHistory(); }} />
            )}

            <div className="wc-content-rail">
                <div>
                    <div className="card">
                        <div className="card-head"><h3>{t('analytics.taskLifecycle')}</h3></div>
                        <div className="card-pad">
                            {isLoadingHistory ? (
                                <div className="muted" style={{textAlign:'center', padding:32}}>{t('analytics.loadingHistory')}</div>
                            ) : isHistoryError ? null : groupedHistory && Object.keys(groupedHistory).length > 0 ? (
                                <div style={{display:'flex', flexDirection:'column', gap:16}}>
                                    {Object.entries(groupedHistory).map(([taskId, group]) => (
                                        <div key={taskId} style={{border:'1px solid var(--border)', borderRadius:'var(--r-md)', padding:14, background:'var(--panel-2)'}}>
                                            <div style={{fontWeight:500, marginBottom:10, display:'flex', alignItems:'center', gap:8}}>
                                                <span style={{width:8, height:8, borderRadius:'50%', background:'var(--accent)', display:'inline-block'}}/>
                                                {group.taskTitle}
                                            </div>
                                            <TaskStatusFlow logs={group.logs}/>
                                        </div>
                                    ))}
                                </div>
                            ) : (
                                <div className="muted" style={{textAlign:'center', padding:32}}>{t('analytics.noTransitions')}</div>
                            )}
                        </div>
                    </div>
                </div>
                <aside className="sticky-rail">
                    <NotificationsPanel iterationId={selectedIterationId} className="w-full h-full border-0"/>
                </aside>
            </div>
        </PageLayout>
    );
};

export default AnalyticsPage;

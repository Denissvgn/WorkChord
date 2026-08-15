import React, { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { taskService } from '../../services/taskService';
import { AlertCircle, History, CheckCircle } from 'lucide-react';
import clsx from 'clsx';
import { formatDate, formatDateTime } from '../../utils/formatDate';
import { QueryErrorState } from '../feedback/QueryState';

interface NotificationsPanelProps {
    iterationId: number;
    className?: string;
}

type Tab = 'history' | 'overdue';

export const NotificationsPanel: React.FC<NotificationsPanelProps> = ({ iterationId, className }) => {
    const [activeTab, setActiveTab] = useState<Tab>('history');
    const { t, i18n } = useTranslation();

    const historyQuery = useQuery({
        queryKey: ['iteration-history', iterationId],
        queryFn: () => taskService.getIterationHistory(iterationId),
        refetchInterval: 30000 // Refresh every 30s
    });

    const overdueQuery = useQuery({
        queryKey: ['iteration-overdue', iterationId],
        queryFn: () => taskService.getOverdueTasks(iterationId),
        refetchInterval: 60000
    });
    const { data: history, isLoading: isLoadingHistory } = historyQuery;
    const { data: overdueTasks, isLoading: isLoadingOverdue } = overdueQuery;

    const statusLabel = (status: string) => t(`statuses.${status}`, status);

    return (
        <div className={clsx("bg-surface-card border-l border-border flex flex-col h-full w-80", className)}>
            <div className="p-4 border-b border-border">
                <h3 className="font-semibold text-lg mb-4 flex items-center gap-2">
                    <History className="w-5 h-5" />
                    {t('notifications.title')}
                </h3>

                <div className="flex space-x-1 bg-surface-subtle p-1 rounded-lg">
                    <button
                        onClick={() => setActiveTab('history')}
                        className={clsx(
                            "flex-1 py-1 px-3 text-sm font-medium rounded-md transition-colors",
                            activeTab === 'history'
                                ? "bg-surface-card text-content-primary shadow-sm"
                                : "text-content-secondary hover:text-content-primary hover:bg-surface-hover"
                        )}
                    >
                        {t('notifications.history')}
                    </button>
                    <button
                        onClick={() => setActiveTab('overdue')}
                        className={clsx(
                            "flex-1 py-1 px-3 text-sm font-medium rounded-md transition-colors flex items-center justify-center gap-1",
                            activeTab === 'overdue'
                                ? "bg-surface-card text-content-primary shadow-sm"
                                : "text-content-secondary hover:text-content-primary hover:bg-surface-hover"
                        )}
                    >
                        {t('notifications.overdue')}
                        {overdueTasks && overdueTasks.length > 0 && (
                            <span className="bg-feedback-danger text-feedback-danger-emphasis text-xs px-1.5 rounded-full">
                                {overdueTasks.length}
                            </span>
                        )}
                    </button>
                </div>
            </div>

            <div className="flex-1 overflow-y-auto p-4">
                {activeTab === 'history' && (
                    <div className="space-y-4">
                        {historyQuery.isError ? (
                            <QueryErrorState error={historyQuery.error} onRetry={() => void historyQuery.refetch()} />
                        ) : isLoadingHistory ? (
                            <div className="text-center text-content-secondary py-4">{t('common.loading')}</div>
                        ) : history && history.length > 0 ? (
                            history.map((log) => (
                                <div key={log.id} className="text-sm border-b border-border-subtle pb-3 last:border-0 relative pl-4">
                                    <div className="absolute left-0 top-1 w-1.5 h-1.5 rounded-full bg-border-strong"></div>
                                    <div className="font-medium text-content-primary mb-1 line-clamp-2">
                                        {log.task_title || `Task #${log.task_id}`}
                                    </div>
                                    <div className="flex items-center gap-2 text-xs text-content-secondary mb-1">
                                        <span>{statusLabel(log.from_status)}</span>
                                        <span>→</span>
                                        <span className={clsx(
                                            "font-medium",
                                            log.to_status === 'active' && "text-action",
                                            log.to_status === 'resolved' && "text-feedback-success-foreground",
                                            log.to_status === 'closed' && "text-content-secondary"
                                        )}>
                                            {statusLabel(log.to_status)}
                                        </span>
                                    </div>
                                    <div className="text-xs text-content-tertiary flex justify-between items-center">
                                        <span>{formatDateTime(log.changed_at, i18n.language)}</span>
                                        <span>{log.triggered_by === 'auto' ? t('notifications.auto') : t('notifications.user')}</span>
                                    </div>
                                    {log.reason && (
                                        <div className="mt-1 text-xs text-content-secondary bg-surface-muted p-1.5 rounded">
                                            {log.reason}
                                        </div>
                                    )}
                                </div>
                            ))
                        ) : (
                            <div className="text-center text-content-tertiary py-8 text-sm">
                                {t('notifications.emptyHistory')}
                            </div>
                        )}
                    </div>
                )}

                {activeTab === 'overdue' && (
                    <div className="space-y-3">
                        {overdueQuery.isError ? (
                            <QueryErrorState error={overdueQuery.error} onRetry={() => void overdueQuery.refetch()} />
                        ) : isLoadingOverdue ? (
                            <div className="text-center text-content-secondary py-4">{t('common.loading')}</div>
                        ) : overdueTasks && overdueTasks.length > 0 ? (
                            overdueTasks.map((task) => (
                                <div key={task.id} className="p-3 bg-feedback-danger-muted border border-feedback-danger-border rounded-lg">
                                    <div className="flex items-start gap-2 mb-1">
                                        <AlertCircle className="w-4 h-4 text-feedback-danger flex-shrink-0 mt-0.5" />
                                        <div className="font-medium text-feedback-danger-foreground text-sm line-clamp-2">
                                            {task.title}
                                        </div>
                                    </div>
                                    <div className="ml-6 text-xs text-feedback-danger-foreground">
                                        {task.assignee ? (
                                            <div className="mb-1">{t('notifications.assigneeShort')} {task.assignee.name}</div>
                                        ) : (
                                            <div className="mb-1">{t('common.unassigned')}</div>
                                        )}
                                        <div>
                                            {t('notifications.start')} {formatDate(task.start_date, i18n.language)}
                                        </div>
                                    </div>
                                </div>
                            ))
                        ) : (
                            <div className="text-center text-content-secondary py-8 flex flex-col items-center">
                                <CheckCircle className="w-8 h-8 text-feedback-success mb-2 opacity-50" />
                                <span className="text-sm">{t('notifications.noOverdue')}</span>
                            </div>
                        )}
                    </div>
                )}
            </div>
        </div>
    );
};

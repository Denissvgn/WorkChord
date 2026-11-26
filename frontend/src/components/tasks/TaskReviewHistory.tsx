import { useQuery } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { taskService } from '../../services/taskService';
import type { Task } from '../../types/task';
import { formatDateTime } from '../../utils/formatDate';
import { QueryErrorState } from '../feedback/QueryState';

/** Every recorded review of the task, newest first. An owner override is labelled, never shown as an independent review. */
export const TaskReviewHistory = ({ task }: { task: Task }) => {
    const { t } = useTranslation();
    // feedback-policy: query loading,error,retry,empty
    const reviews = useQuery({ queryKey: ['taskReviews', task.id, task.version], queryFn: () => taskService.reviews(task.id, { limit: 100 }) });
    if (reviews.isError) return <QueryErrorState error={reviews.error} fallback={t('domain.reviewHistoryFailed')} onRetry={() => void reviews.refetch()} />;
    if (reviews.isLoading) return <p role="status" className="text-sm text-content-secondary">{t('common.loading')}</p>;
    const items = [...(reviews.data ?? [])].reverse();
    if (items.length === 0) return null;
    return <section className="space-y-2" aria-label={t('domain.reviewHistory')}>
        <h4 className="font-medium text-content-primary">{t('domain.reviewHistory')}</h4>
        <ul className="space-y-2 text-sm">{items.map(item => {
            const override = item.kind === 'owner_override';
            return <li key={item.id} className="space-y-0.5">
                <p className="flex flex-wrap items-center gap-2">
                    <span className="font-medium text-content-primary">{item.verdict === 'accept' ? t('domain.reviewAccepted') : t('domain.reviewRejected')}</span>
                    {override && <span className="rounded border border-feedback-warning-foreground px-1.5 text-xs text-feedback-warning-foreground">{t('domain.ownerOverrideLabel')}</span>}
                    <span className="text-content-secondary">{formatDateTime(item.created_at)}</span>
                </p>
                {override && <p className="text-content-secondary">{t('domain.ownerOverrideNote')}</p>}
                {item.reason && <p className="text-content-primary">{t('domain.reviewReason')}: {item.reason}</p>}
            </li>;
        })}</ul>
    </section>;
};

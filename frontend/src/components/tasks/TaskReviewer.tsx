import { useTranslation } from 'react-i18next';
import type { Task } from '../../types/task';
import { useTaskReviewer } from './useTaskReviewer';
import { QueryErrorState } from '../feedback/QueryState';

/** Who reviews submitted work: the agent with the live review assignment, or any authorized person. */
export const TaskReviewer = ({ task }: { task: Task }) => {
    const { t } = useTranslation();
    // feedback-policy: query loading,error,retry,empty
    const detail = useTaskReviewer(task);
    if (task.status !== 'resolved') return null;
    if (detail.isError) {
        return <QueryErrorState error={detail.error} fallback={t('domain.reviewerLoadFailed')} onRetry={() => void detail.refetch()} />;
    }
    if (detail.isLoading) return <p role="status" className="text-sm text-content-secondary">{t('common.loading')}</p>;
    const name = detail.data?.reviewer_name;
    return <p className="text-sm text-content-secondary">
        <span className="font-medium text-content-primary">{t('domain.reviewer')}:</span>{' '}
        {name ?? t('domain.reviewerAnyone')}
    </p>;
};

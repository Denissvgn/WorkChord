import { useQuery } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { iterationService } from '../../services/iterationService';
import { planningNavigationSummaryKey } from '../../features/planningMasters/usePlanningNavigationSummary';
import { formatDecimal } from '../../utils/workNumbers';

/** One labelled capacity bar per iteration: planned hours against capacity, tasks, and whether a schedule exists. */
export const IterationCapacityLine = ({ iterationId }: { iterationId: number }) => {
    const { t, i18n } = useTranslation();
    const locale = i18n.resolvedLanguage ?? i18n.language;
    // feedback-policy: query loading,error,retry,empty - the card says when its capacity line is unavailable.
    const readiness = useQuery({
        queryKey: planningNavigationSummaryKey(iterationId),
        queryFn: () => iterationService.getPlanningReadiness(iterationId),
        staleTime: 60000,
    });
    if (readiness.isLoading) return <p role="status" className="text-sm text-content-secondary">{t('common.loading')}</p>;
    if (readiness.isError || !readiness.data) {
        return <p className="text-sm text-content-secondary">{t('iterations.capacityUnavailable')} <button type="button" className="underline" onClick={() => void readiness.refetch()}>{t('queryFeedback.retry')}</button></p>;
    }
    const data = readiness.data;
    const capacity = data.team_capacity_hours;
    const planned = data.planned_hours ?? 0;
    const hours = (value: number) => formatDecimal(value, locale) ?? '0';
    const scale = Math.max(capacity, planned, 1);
    const over = capacity > 0 && planned > capacity;
    return (
        <div className="space-y-1">
            {capacity > 0 ? (
                <div className="relative h-2.5 rounded-full bg-surface-subtle" aria-hidden="true">
                    <span className="absolute inset-y-0 left-0 rounded-full border border-feedback-success-border bg-feedback-success-muted" style={{ width: `${capacity / scale * 100}%` }} />
                    <span className={`absolute inset-y-0 left-0 rounded-full ${over ? 'bg-feedback-danger' : 'bg-action'}`} style={{ width: `${Math.min(100, planned / scale * 100)}%` }} />
                </div>
            ) : null}
            <p className={`text-sm ${over ? 'text-feedback-danger-foreground' : 'text-content-secondary'}`}>
                {capacity > 0
                    ? t('iterations.capacityLine', { planned: hours(planned), capacity: hours(capacity) })
                    : t('iterations.capacityLineUnknown', { planned: hours(planned) })}
                {' · '}{t('iterations.taskCount', { count: data.task_count })}
                {' · '}{t(data.has_schedule ? 'iterations.scheduleSaved' : 'iterations.noSchedule')}
            </p>
        </div>
    );
};

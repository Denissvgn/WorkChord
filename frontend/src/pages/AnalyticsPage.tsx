import { useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { iterationService } from '../services/iterationService';
import { WorkMetricsLine } from '../components/tasks/WorkMetricsLine';
import { ExecutionUsagePanel } from '../components/analytics/ExecutionUsagePanel';
import { Select } from '../components/common/Select';
import { DeliveryAnalytics } from '../components/analytics/DeliveryAnalytics';
import { OnTrackSummary } from '../components/analytics/OnTrackSummary';
import { StatusDistribution } from '../components/analytics/StatusDistribution';
import { PageHeader, PageLayout, PageToolbar } from '../components/ui';
import { NextStepEmptyState } from '../features/firstRun/NextStepEmptyState';
import { firstRunPlanHref } from '../features/firstRun/firstRunSteps';
import { useScopeLink } from '../features/scope/useScopeLink';
import { QueryErrorState } from '../components/feedback/QueryState';
import { useWorkScope } from '../features/scope/useWorkScope';


const AnalyticsPage = () => {
    const { iteration } = useWorkScope();
    const [days, setDays] = useState(30);
    const selectedIterationId = typeof iteration === 'number' ? iteration : 0;
    const { t } = useTranslation();
    const scopeLink = useScopeLink();


    // feedback-policy: query loading,error,retry,empty
    const summaryQuery = useQuery({ queryKey: ['iterationSummary', selectedIterationId],
        queryFn: () => iterationService.getSummary(selectedIterationId), enabled: selectedIterationId > 0 });

    const summary = summaryQuery.data;
    return (
        <PageLayout>
            <PageHeader title={t('analytics.title')} purpose={t('analytics.purpose')} />
            <PageToolbar label={t('analytics.title')} viewOptions={<Select label={t('deliveryAnalytics.window')} value={days} onChange={event => setDays(Number(event.target.value))}>
                {[30, 90, 180, 366].map(value => <option key={value} value={value}>{t('deliveryAnalytics.days', { count: value })}</option>)}
            </Select>} />
            {selectedIterationId === 0 && (
                <NextStepEmptyState title={t('emptyStates.analytics.title')} description={t('emptyStates.analytics.body')} fallback={{ label: t('firstRun.steps.iteration.title'), to: scopeLink(firstRunPlanHref('iteration')) }} />
            )}

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
        </PageLayout>
    );
};

export default AnalyticsPage;

import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { PlanShareSection } from './PlanShareSection';
import { QueryErrorState, QueryLoadingState } from '../feedback/QueryState';
import { usePlanScheduleWorkloads } from '../../features/planningMasters/usePlanScheduleWorkloads';
import { scheduleLeaves } from '../../features/planningMasters/scheduleEvidence';
import { withPlanReturn } from '../../features/planningMasters/planningReturn';
import { hasDeliverySignal, isFinished } from '../../features/planningMasters/planningTaskIssues';
import { useScopeLink } from '../../features/scope/useScopeLink';
import type { GanttResponse } from '../../types/gantt';
import type { Iteration } from '../../types/iteration';
import type { TeamMember } from '../../types/team';
import { formatDate } from '../../utils/formatDate';

export const PlanReviewSection = ({ iteration, members, gantt, riskCount }: {
    iteration: Iteration; members: TeamMember[]; gantt?: GanttResponse; riskCount: number;
}) => {
    const { t, i18n } = useTranslation();
    const scopeLink = useScopeLink();
    const workloads = usePlanScheduleWorkloads(iteration.id, members);
    const tasks = scheduleLeaves(gantt?.tasks ?? []);
    const afterEnd = tasks.filter(task => task.end_date && task.end_date > iteration.end_date);
    const undated = tasks.filter(task => task.status === 'planned' && (!task.start_date || !task.end_date));
    const signals = tasks.filter(task => !isFinished(task) && hasDeliverySignal(task));
    const overloaded = (workloads.data ?? []).filter(row => row.allocated_hours !== undefined && row.capacity_hours !== undefined && row.allocated_hours > row.capacity_hours);
    const href = (params: Record<string, string>) => scopeLink(withPlanReturn('/tasks', 'review', params));
    const riskLink = (label: string, count: number, to: string) => <div className={count > 0 ? 'exception' : undefined}>
        <dt>{label}</dt><dd>{count > 0 ? <Link className="plan-evidence-link" to={to} aria-label={`${label}: ${count}`}>{count}</Link> : count}</dd>
    </div>;
    return <div className="space-y-4">
        <section className="plan-checkpoint-evidence" aria-label={t('planSchedule.risks')}>
            <h3>{t('planSchedule.risks')}</h3>
            <p className="text-sm text-content-secondary mb-3">{t('plan.status.risksToAcknowledge', { count: riskCount })}</p>
            <dl>
                {riskLink(t('planSchedule.afterEnd', { date: formatDate(iteration.end_date, i18n.language) }), afterEnd.length, href({ overflow: 'true' }))}
                {riskLink(t('planSchedule.withoutDates'), undated.length, href({ planningIssue: 'unscheduled' }))}
                {riskLink(t('plan.page.atRisk'), signals.length, href({ planningIssue: 'at-risk' }))}
            </dl>
        </section>
        {workloads.isLoading ? <QueryLoadingState message={t('planSchedule.loadingCapacity')} />
            : workloads.isError ? <QueryErrorState error={workloads.error} fallback={t('planSchedule.capacityFailed')} onRetry={() => void workloads.refetch()} />
                : <section className="plan-checkpoint-evidence" aria-label={t('planSchedule.overCapacity')}>
                    <h3>{t('planSchedule.overCapacity')}</h3>
                    {overloaded.length ? <ul className="plan-schedule-reasons">{overloaded.map(row => <li key={row.team_member_id}>
                        <Link className="underline" to={href({ assignee: String(row.team_member_id) })}>{row.name}</Link>
                    </li>)}</ul> : <p className="text-sm text-content-secondary py-3">{t('planSchedule.noneOverCapacity')}</p>}
                </section>}
        {Boolean(gantt?.schedule_result?.capacity_issues?.length) && <section aria-label={t('planSchedule.capacityIssues')}>
            <h3 className="text-sm font-semibold">{t('planSchedule.capacityIssues')}</h3>
            <ul className="plan-schedule-reasons">{gantt!.schedule_result!.capacity_issues!.map((issue, index) => <li key={index}>{issue.message}</li>)}</ul>
        </section>}
        <PlanShareSection iterationId={iteration.id} />
        <Link className="btn secondary" to={scopeLink(withPlanReturn('/gantt', 'review'))}>{t('planSchedule.openGantt')}</Link>
    </div>;
};

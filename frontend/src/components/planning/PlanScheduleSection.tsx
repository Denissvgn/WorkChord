import { ButtonLink } from '../common/ButtonLink';
import { useState } from 'react';
import { useQueryClient } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { Button } from '../common/Button';
import { QueryErrorState, QueryLoadingState } from '../feedback/QueryState';
import { ganttService } from '../../services/ganttService';
import { usePlanScheduleWorkloads } from '../../features/planningMasters/usePlanScheduleWorkloads';
import { withPlanReturn } from '../../features/planningMasters/planningReturn';
import { useScopeLink } from '../../features/scope/useScopeLink';
import type { GanttResponse, SchedulePreviewResponse } from '../../types/gantt';
import { scheduleLeaves } from '../../features/planningMasters/scheduleEvidence';
import type { Iteration } from '../../types/iteration';
import type { Task } from '../../types/task';
import type { TeamMember } from '../../types/team';
import { formatDate } from '../../utils/formatDate';
import { formatDecimal } from '../../utils/workNumbers';
import { getApiErrorMessage, getApiErrorStatus } from '../../utils/apiError';

type ListedTask = Pick<Task, 'id' | 'start_date' | 'end_date' | 'is_deferred' | 'effective_is_deferred'> & { children?: ListedTask[] };

/**
 * Sorts the iteration's tasks into deferred and scheduled work. Deferred tasks are backlog work: they stay in list
 * views and never count in schedule checks. A subtask of a deferred task is deferred too. Works on a nested tree and
 * on a flattened list that keeps each task's subtasks.
 */
const sortByDeferral = (tasks: ListedTask[]) => {
    const deferred = new Set<number>();
    const scheduled = new Map<number, ListedTask>();
    const visit = (task: ListedTask, inherited: boolean) => {
        const isDeferred = inherited || Boolean(task.effective_is_deferred ?? task.is_deferred);
        if (isDeferred) deferred.add(task.id); else scheduled.set(task.id, task);
        task.children?.forEach(child => visit(child, isDeferred));
    };
    tasks.forEach(task => visit(task, false));
    deferred.forEach(id => scheduled.delete(id));
    return { deferred, scheduled: [...scheduled.values()] };
};

/**
 * Whether every task that is not deferred has its own start and end dates, whatever its status: finished and active
 * tasks alike, and a parent task as well as each of its subtasks. A parent task without its own dates fails the check
 * even when all its subtasks are dated.
 */
const everyTaskHasDates = (scheduled: ListedTask[]): boolean => (
    scheduled.length > 0 && scheduled.every(task => Boolean(task.start_date && task.end_date))
);

export const PlanScheduleSection = ({ iteration, members, gantt, tasks: iterationTasks, done }: {
    /** The iteration's tasks from the task list, flattened, deferred tasks included; this section leaves those out. */
    iteration: Iteration; members: TeamMember[]; gantt?: GanttResponse; tasks: Task[]; done: boolean;
}) => {
    const { t, i18n } = useTranslation();
    const client = useQueryClient();
    const scopeLink = useScopeLink();
    const workloads = usePlanScheduleWorkloads(iteration.id, members);
    const [preview, setPreview] = useState<SchedulePreviewResponse | null>(null);
    const [pending, setPending] = useState<'calculate' | 'apply' | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [applied, setApplied] = useState(false);
    const refresh = () => Promise.all(['gantt', 'tasks', 'team', 'iterations', 'planning-navigation-summary', 'workload',
        'plan-schedule-workloads', 'projectSummary', 'projects'].map(key => client.invalidateQueries({ queryKey: [key] })));
    const calculate = async () => {
        setPending('calculate'); setError(null); setPreview(null); setApplied(false);
        try {
            setPreview(await ganttService.previewSchedule(iteration.id, [], gantt?.iteration.revision ?? iteration.revision));
        } catch (cause) {
            setError(getApiErrorMessage(cause, t('planSchedule.calculateFailed')));
            if (getApiErrorStatus(cause) === 409) await refresh();
        }
        finally { setPending(null); }
    };
    const apply = async () => {
        if (!preview) return;
        setPending('apply'); setError(null);
        try {
            const result = await ganttService.schedule(iteration.id, preview.input_revision, preview.input_planning_revision);
            if (!result.success) throw new Error(t('planSchedule.applyFailed'));
            setApplied(true); setPreview(null);
            await refresh();
        } catch (cause) {
            setError(getApiErrorMessage(cause, t('planSchedule.applyFailed')));
            setPreview(null);
            await refresh();
        } finally { setPending(null); }
    };
    const tasks = preview?.tasks ?? gantt?.tasks ?? [];
    const ends = scheduleLeaves(tasks).flatMap(task => task.end_date ? [task.end_date] : []);
    const finish = ends.sort().at(-1);
    const result = preview?.schedule_result ?? gantt?.schedule_result;
    // The iteration's task list is the authority: the Gantt response and the schedule preview leave out or misreport
    // deferred tasks, and an unsaved preview changes no task's dates.
    const { deferred, scheduled } = sortByDeferral(iterationTasks);
    const everyTaskDated = everyTaskHasDates(scheduled);
    const unscheduled = (result?.unscheduled ?? []).filter(task => task.reason !== 'deferred' && !deferred.has(task.task_id));
    const showResult = preview !== null || done || Boolean(result);
    return <div className="space-y-4">
        <p className="text-sm text-content-secondary">{t('planSchedule.datesAreCalculated')}</p>
        <div className="flex flex-wrap items-center gap-2">
            <Button variant={!preview && !done ? 'primary' : 'secondary'} disabled={pending !== null} isLoading={pending === 'calculate'} onClick={() => void calculate()}>
                {t('planSchedule.calculate')}
            </Button>
            {preview && <Button variant="primary" disabled={pending !== null || preview.schedule_result?.success === false} isLoading={pending === 'apply'} onClick={() => void apply()}>{t('planSchedule.apply')}</Button>}
            <ButtonLink  to={scopeLink(withPlanReturn('/gantt', 'schedule'))} variant="secondary">{t('planSchedule.openGantt')}</ButtonLink>
        </div>
        {error && <p role="alert" className="text-sm text-feedback-danger-foreground">{error}</p>}
        {applied && <p role="status" className="text-sm text-content-secondary">{t('planSchedule.applied')}</p>}
        {showResult && <>
            <section className="plan-checkpoint-evidence" aria-label={t('planSchedule.result')}>
                <h3>{t(preview ? 'planSchedule.preview' : 'planSchedule.saved')}</h3>
                <dl>
                    <div className={finish && finish > iteration.end_date ? 'exception' : undefined}><dt>{t('planSchedule.calculatedEnd')}</dt><dd>{finish ? formatDate(finish, i18n.language) : t('plan.master.notAvailable')}</dd></div>
                    <div><dt>{t('planSchedule.iterationEnd')}</dt><dd>{formatDate(iteration.end_date, i18n.language)}</dd></div>
                </dl>
            </section>
            {workloads.isLoading ? <QueryLoadingState message={t('planSchedule.loadingCapacity')} />
                : workloads.isError ? <QueryErrorState error={workloads.error} fallback={t('planSchedule.capacityFailed')} onRetry={() => void workloads.refetch()} />
                    : <div className="overflow-x-auto"><table className="plan-schedule-loads">
                        <caption>{t('planSchedule.hoursAgainstCapacity')}</caption>
                        <thead><tr><th scope="col">{t('planWork.row')}</th><th scope="col">{t('planSchedule.hours')}</th><th scope="col">{t('planWork.capacity')}</th></tr></thead>
                        <tbody>{(workloads.data ?? []).map(row => <tr key={row.team_member_id}>
                            <th scope="row">{row.name}</th>
                            <td className={row.allocated_hours !== undefined && row.capacity_hours !== undefined && row.allocated_hours > row.capacity_hours ? 'text-feedback-warning-foreground' : undefined}>{row.allocated_hours === undefined ? t('plan.master.unknown') : t('capacity.hourValue', { hours: formatDecimal(row.allocated_hours, i18n.language) })}</td>
                            <td>{row.capacity_hours === undefined ? t('plan.master.unknown') : t('capacity.hourValue', { hours: formatDecimal(row.capacity_hours, i18n.language) })}</td>
                        </tr>)}</tbody>
                    </table>{members.length === 0 && <p className="text-sm text-content-secondary">{t('plan.status.noPeople')}</p>}</div>}
            <section aria-label={t('planSchedule.withoutDates')} className="space-y-2">
                <h3 className="text-sm font-semibold">{t('planSchedule.withoutDates')}</h3>
                {everyTaskDated ? <p className="text-sm text-content-secondary">{t('planSchedule.allDated')}</p>
                    : unscheduled.length ? <ul className="plan-schedule-reasons">{unscheduled.map(task => <li key={task.task_id}>
                    <Link className="underline" to={scopeLink(withPlanReturn('/tasks', 'schedule', { task: String(task.task_id) }))}>{task.task_title}</Link>
                    <p>{task.message}</p>
                </li>)}</ul> : <p className="text-sm text-content-secondary">{t('planSchedule.calculateForReasons')}</p>}
            </section>
        </>}
    </div>;
};

import type { TFunction } from 'i18next';
import type { Task } from '../../types/task';
import { isOutsideDateLimits } from './planningTaskIssues';

type RiskFields = Pick<Task, 'is_overdue' | 'is_delayed' | 'is_outside_constraints'>
    & Partial<Pick<Task, 'start_date' | 'end_date' | 'min_start_date' | 'max_end_date' | 'actual_start_date' | 'baseline_start_date'>>;

/** Why a task counts as an at-risk signal, in the words Plan and the Tasks list share. */
export const atRiskReasons = (task: RiskFields, t: TFunction): string[] => {
    // The server judges both cases against the planned start: the baseline start when one exists, otherwise
    // the current start. An unstarted task can therefore be late while its current start is still ahead, so
    // the reason names the planned start rather than the current one; the Gantt payload carries no baseline.
    const startedLate = Boolean(task.actual_start_date);
    return [
        ...(task.is_overdue ? [t('planSchedule.riskOverdue')] : []),
        ...(task.is_delayed ? [t(startedLate ? 'planSchedule.riskStartedLate' : 'planSchedule.riskNotStartedByPlannedStart')] : []),
        ...(isOutsideDateLimits(task) ? [t('planSchedule.riskOutsideLimits')] : []),
    ];
};

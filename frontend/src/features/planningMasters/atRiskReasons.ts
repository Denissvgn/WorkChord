import type { Task } from '../../types/task';
import { isOutsideDateLimits } from './planningTaskIssues';

type Translate = (key: string) => string;

type RiskFields = Pick<Task, 'is_overdue' | 'is_delayed' | 'is_outside_constraints'>
    & Partial<Pick<Task, 'start_date' | 'end_date' | 'min_start_date' | 'max_end_date' | 'actual_start_date' | 'baseline_start_date'>>;

/** Why a task counts as an at-risk signal, in the words Plan and the Tasks list share. */
export const atRiskReasons = (task: RiskFields, t: Translate): string[] => {
    const plannedStart = task.baseline_start_date ?? task.start_date;
    const startedLate = Boolean(task.actual_start_date && plannedStart && task.actual_start_date > plannedStart);
    return [
        ...(task.is_overdue ? [t('planSchedule.riskOverdue')] : []),
        ...(task.is_delayed ? [t(startedLate ? 'planSchedule.riskStartedLate' : 'planSchedule.riskStartsBeforeToday')] : []),
        ...(isOutsideDateLimits(task) ? [t('planSchedule.riskOutsideLimits')] : []),
    ];
};

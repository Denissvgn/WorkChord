import type { Task } from '../../types/task';

type Translate = (key: string) => string;

/** Why a task counts as an at-risk signal, in the words Plan and the Tasks list share. */
export const atRiskReasons = (
    task: Pick<Task, 'is_overdue' | 'is_delayed' | 'is_outside_constraints'>,
    t: Translate,
): string[] => [
    ...(task.is_overdue ? [t('planSchedule.riskOverdue')] : []),
    ...(task.is_delayed ? [t('planSchedule.riskStartsBeforeToday')] : []),
    ...(task.is_outside_constraints ? [t('planSchedule.riskOutsideLimits')] : []),
];

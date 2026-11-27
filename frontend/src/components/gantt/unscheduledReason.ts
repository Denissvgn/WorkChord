import type { TFunction } from 'i18next';
import type { KeptDatesTask, UnscheduledTask } from '../../types/gantt';

/** The translated reason a schedule run left a task unplaced, naming any postponed work it waits on. */
export const unscheduledReasonText = (t: TFunction, item: UnscheduledTask | KeptDatesTask): string => t(
    `gantt.unscheduled.reasons.${item.reason}`,
    {
        defaultValue: item.message,
        tasks: (item.waiting_on ?? []).map(task => `"${task.task_title}" (#${task.task_id})`).join(', '),
    },
);

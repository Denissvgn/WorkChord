import type { TFunction } from 'i18next';
import type { KeptDatesTask, UnscheduledTask } from '../../types/gantt';

/** The translated reason a schedule run left a task unplaced, naming any postponed work it waits on. */
export const unscheduledReasonText = (t: TFunction, item: UnscheduledTask | KeptDatesTask): string => {
    const waitingOn = item.waiting_on ?? [];
    // Without the names the translated text would read wrongly; the server's message names the wait.
    if (item.reason === 'predecessor_postponed' && waitingOn.length === 0) return item.message;
    return t(`gantt.unscheduled.reasons.${item.reason}`, {
        defaultValue: item.message,
        tasks: waitingOn.map(task => `"${task.task_title}" (#${task.task_id})`).join(', '),
    });
};

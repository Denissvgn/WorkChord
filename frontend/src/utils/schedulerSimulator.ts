import type { GanttTask } from '../types/gantt';

/**
 * Client-side scheduler simulation.
 * Recalculates task start/end dates based on priority, effort, assignee capacity,
 * weekends, holidays, and vacations, matching the backend scheduler logic.
 */
export function simulateSchedule(
    tasks: GanttTask[],
    startDateStr: string,
    endDateStr: string,
    weekends: string[],
    holidays: string[],
    memberVacations: Record<number, string[]>
): GanttTask[] {
    const startLimit = new Date(startDateStr);
    const endLimit = new Date(endDateStr);

    const weekendSet = new Set(weekends);
    const holidaySet = new Set(holidays);
    const vacationMap = new Map<number, Set<string>>();
    Object.entries(memberVacations).forEach(([memberId, dates]) => {
        vacationMap.set(Number(memberId), new Set(dates));
    });

    const formatDate = (d: Date): string => {
        const year = d.getFullYear();
        const month = String(d.getMonth() + 1).padStart(2, '0');
        const day = String(d.getDate()).padStart(2, '0');
        return `${year}-${month}-${day}`;
    };

    const isWorkingDay = (dateStr: string, memberId?: number): boolean => {
        if (weekendSet.has(dateStr)) return false;
        if (holidaySet.has(dateStr)) return false;
        if (memberId && vacationMap.get(memberId)?.has(dateStr)) return false;
        return true;
    };

    const addDays = (d: Date, days: number): Date => {
        const result = new Date(d);
        result.setDate(result.getDate() + days);
        return result;
    };

    const findNextWorkingDay = (earliestStart: Date, memberId?: number): Date => {
        let curr = new Date(earliestStart);
        // Safety boundary to avoid infinite loop (limit scheduling search up to 1 year)
        const limit = addDays(endLimit, 365);
        while (curr <= limit) {
            const dateStr = formatDate(curr);
            if (isWorkingDay(dateStr, memberId)) {
                return curr;
            }
            curr = addDays(curr, 1);
        }
        return earliestStart;
    };

    const allocateDates = (startDate: Date, effortDays: number, memberId?: number): { start: Date; end: Date } => {
        let current = findNextWorkingDay(startDate, memberId);
        const start = new Date(current);
        let allocatedDays = 0;

        while (allocatedDays < effortDays) {
            const dateStr = formatDate(current);
            if (isWorkingDay(dateStr, memberId)) {
                allocatedDays++;
                if (allocatedDays === effortDays) {
                    break;
                }
            }
            current = addDays(current, 1);
        }
        return { start, end: current };
    };

    const allLeafTasks: GanttTask[] = [];
    const lockedTasks: GanttTask[] = [];
    const plannedTasks: GanttTask[] = [];

    const collectLeafTasks = (task: GanttTask) => {
        if (!task.children || task.children.length === 0) {
            allLeafTasks.push(task);
            if (task.status !== 'planned') {
                lockedTasks.push(task);
            } else {
                plannedTasks.push(task);
            }
        } else {
            task.children.forEach(collectLeafTasks);
        }
    };
    tasks.forEach(collectLeafTasks);

    const calculatedDates = new Map<number, { start_date: string; end_date: string }>();

    // Lock in existing dates for non-planned tasks
    lockedTasks.forEach(task => {
        if (task.start_date && task.end_date) {
            calculatedDates.set(task.id, {
                start_date: task.start_date,
                end_date: task.end_date
            });
        }
    });

    const getTaskEarliestStart = (task: GanttTask): Date => {
        let base = new Date(startLimit);

        if (task.min_start_date) {
            const minStart = new Date(task.min_start_date);
            if (minStart > base) {
                base = minStart;
            }
        }

        if (task.dependencies && task.dependencies.length > 0) {
            task.dependencies.forEach(depId => {
                const depDates = calculatedDates.get(depId);
                if (depDates && depDates.end_date) {
                    const depEndNextDay = addDays(new Date(depDates.end_date), 1);
                    if (depEndNextDay > base) {
                        base = depEndNextDay;
                    }
                }
            });
        }

        return base;
    };

    const assigneeLastEnd = new Map<number, Date>();
    lockedTasks.forEach(task => {
        if (task.assignee?.id && task.end_date) {
            const currentLast = assigneeLastEnd.get(task.assignee.id);
            const taskEnd = new Date(task.end_date);
            if (!currentLast || taskEnd > currentLast) {
                assigneeLastEnd.set(task.assignee.id, taskEnd);
            }
        }
    });

    // Sort planned tasks by priority (lower priority number = scheduled first), then effort_days
    const sortedPlanned = [...plannedTasks].sort((a, b) => {
        const aOpt = a.is_optional ? 1 : 0;
        const bOpt = b.is_optional ? 1 : 0;
        if (aOpt !== bOpt) return aOpt - bOpt;

        const aPri = Number(a.priority) || 5;
        const bPri = Number(b.priority) || 5;
        if (aPri !== bPri) return aPri - bPri;

        const aEff = Number(a.effort_days) || 1;
        const bEff = Number(b.effort_days) || 1;
        return aEff - bEff;
    });

    const scheduledIds = new Set<number>();
    const schedulingInProgress = new Set<number>();

    const scheduleTask = (task: GanttTask) => {
        if (scheduledIds.has(task.id)) return;
        if (schedulingInProgress.has(task.id)) {
            return; // Cycle protection
        }
        schedulingInProgress.add(task.id);

        if (task.dependencies) {
            task.dependencies.forEach(depId => {
                const depTask = plannedTasks.find(t => t.id === depId);
                if (depTask) {
                    scheduleTask(depTask);
                }
            });
        }

        let earliestStart = getTaskEarliestStart(task);
        const memberId = task.assignee?.id;

        if (memberId && assigneeLastEnd.has(memberId)) {
            const prevEnd = assigneeLastEnd.get(memberId)!;
            const nextDay = addDays(prevEnd, 1);
            if (nextDay > earliestStart) {
                earliestStart = nextDay;
            }
        }

        const effort = Number(task.effort_days) || 1;
        const { start, end } = allocateDates(earliestStart, effort, memberId);

        calculatedDates.set(task.id, {
            start_date: formatDate(start),
            end_date: formatDate(end)
        });

        if (memberId) {
            const currentLast = assigneeLastEnd.get(memberId);
            if (!currentLast || end > currentLast) {
                assigneeLastEnd.set(memberId, end);
            }
        }

        scheduledIds.add(task.id);
        schedulingInProgress.delete(task.id);
    };

    sortedPlanned.forEach(scheduleTask);

    const updateTaskTree = (task: GanttTask): GanttTask => {
        const updated = { ...task };
        if (task.children && task.children.length > 0) {
            const updatedChildren = task.children.map(updateTaskTree);
            updated.children = updatedChildren;

            let minStart: Date | null = null;
            let maxEnd: Date | null = null;
            let totalProgress = 0;

            updatedChildren.forEach(child => {
                if (child.start_date) {
                    const d = new Date(child.start_date);
                    if (!minStart || d < minStart) minStart = d;
                }
                if (child.end_date) {
                    const d = new Date(child.end_date);
                    if (!maxEnd || d > maxEnd) maxEnd = d;
                }
                totalProgress += child.progress || 0;
            });

            updated.start_date = minStart ? formatDate(minStart) : task.start_date;
            updated.end_date = maxEnd ? formatDate(maxEnd) : task.end_date;
            updated.progress = updatedChildren.length > 0 ? totalProgress / updatedChildren.length : 0;
        } else {
            const dates = calculatedDates.get(task.id);
            if (dates) {
                updated.start_date = dates.start_date;
                updated.end_date = dates.end_date;
            }
        }
        return updated;
    };

    return tasks.map(updateTaskTree);
}

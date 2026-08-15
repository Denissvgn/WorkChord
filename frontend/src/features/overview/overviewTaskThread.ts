export const OVERVIEW_TASK_PARAM = 'task';
export const OVERVIEW_TASK_ORIGIN_PARAM = 'from';
export const OVERVIEW_TASK_ORIGIN = 'overview';
export const OVERVIEW_TASK_RETURN_PARAM = 'returnTask';
export const OVERVIEW_TASK_THREAD_PARAM = 'thread';

export const OVERVIEW_TASK_THREAD_SOURCES = ['attention', 'work-now'] as const;
export type OverviewTaskThreadSource = typeof OVERVIEW_TASK_THREAD_SOURCES[number];

export const positiveTaskId = (value: string | null): number | null => {
    const taskId = Number(value);
    return Number.isInteger(taskId) && taskId > 0 ? taskId : null;
};

export const overviewTaskThreadSource = (
    value: string | null,
): OverviewTaskThreadSource | null => (
    value && OVERVIEW_TASK_THREAD_SOURCES.includes(value as OverviewTaskThreadSource)
        ? value as OverviewTaskThreadSource
        : null
);

export const overviewTaskReturnFocusId = (taskId: number) => (
    `overview-task-${taskId}`
);

export const overviewTaskDrawerHref = (
    taskId: number,
    source: OverviewTaskThreadSource,
) => {
    const search = new URLSearchParams({
        layout: 'board',
        [OVERVIEW_TASK_PARAM]: String(taskId),
        [OVERVIEW_TASK_ORIGIN_PARAM]: OVERVIEW_TASK_ORIGIN,
        [OVERVIEW_TASK_RETURN_PARAM]: String(taskId),
        [OVERVIEW_TASK_THREAD_PARAM]: source,
    });
    return `/tasks?${search.toString()}`;
};

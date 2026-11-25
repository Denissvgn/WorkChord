import { useCallback, useState } from 'react';

/**
 * What a person was doing in the task view's panels. The view remounts whenever the task version
 * changes, so the drawer holds this for as long as it is open. It is memory only: it ends with the drawer.
 */
export interface TaskViewSession { prerequisitesOpen: boolean; branchConflict: boolean; catchUpDone: boolean }
export type TaskViewSessionUpdate = (patch: Partial<TaskViewSession>) => void;

export const EMPTY_TASK_VIEW_SESSION: TaskViewSession = { prerequisitesOpen: false, branchConflict: false, catchUpDone: false };

/** Session state keyed by the signed-in person and task, so it never carries to another person or task. */
export const useTaskViewSession = (scope: string | null) => {
    const [stored, setStored] = useState<{ scope: string | null; value: TaskViewSession }>({ scope, value: EMPTY_TASK_VIEW_SESSION });
    const session = stored.scope === scope ? stored.value : EMPTY_TASK_VIEW_SESSION;
    const update = useCallback<TaskViewSessionUpdate>(patch => setStored(current => ({
        scope, value: { ...(current.scope === scope ? current.value : EMPTY_TASK_VIEW_SESSION), ...patch },
    })), [scope]);
    return [session, update] as const;
};

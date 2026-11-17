import { taskService } from '../../services/taskService';
import type { TaskReference } from '../../types/task';

/** The largest page the task lookup serves. */
const PAGE_SIZE = 100;
/** More pages than this would make Overview slow; it reports the backlog as unavailable instead. */
const MAX_PAGES = 50;

/**
 * Every task of one project's backlog, or of every project's with no project given. Overview counts the whole backlog, so it reads every
 * page; a backlog too large to read in full fails instead of showing a partial count.
 */
export const loadProjectBacklog = async (projectId: number | null): Promise<TaskReference[]> => {
    const items: TaskReference[] = [];
    let afterId = 0;
    for (let page = 0; page < MAX_PAGES; page += 1) {
        const result = await taskService.lookup({ ...(projectId === null ? {} : { project_id: projectId }), backlog_only: true, after_id: afterId, limit: PAGE_SIZE });
        items.push(...result.items);
        if (!result.has_more || result.next_after_id === null) return items;
        afterId = result.next_after_id;
    }
    throw new Error('The backlog is too large to count here. Open it in Tasks.');
};

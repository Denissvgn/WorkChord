import type { TFunction } from 'i18next';
import type { TaskReference } from '../../types/task';

/** The same task identity and project context in every global search result. */
export const taskSearchResultCopy = (task: TaskReference, t: TFunction) => ({
    label: `#${task.id} · ${task.title}`,
    description: `${task.project_name ?? t('teamwork.workspace')} · ${task.iteration_name ?? t('teamwork.backlog')} · ${t(`statuses.${task.status}`)}`,
});

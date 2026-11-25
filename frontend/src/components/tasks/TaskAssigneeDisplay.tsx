import { Bot, User } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import type { Task } from '../../types/task';
import type { GanttTask } from '../../types/gantt';
import { AGENT_DISPATCH_LABEL_KEY } from '../../features/agentDispatch';
import { useTaskAssigneeDisplay } from './useTaskAssigneeDisplay';

/** The same capacity identity and dispatch line used by the task row, with its Reviewer beside it. */
export const TaskAssigneeDisplay = ({ task, iterationId, bar = false, durationDays }: { task: Task | GanttTask; iterationId: number | null; bar?: boolean; durationDays?: number }) => {
    const { t } = useTranslation();
    const { dispatch, reviewer, kind } = useTaskAssigneeDisplay(task, iterationId);
    const Icon = kind === 'agent' ? Bot : User;
    return <span data-task-people={task.id} className={`inline-flex min-w-0 items-start gap-3 text-xs ${bar ? 'max-w-full rounded bg-surface-card px-1 text-content-primary' : 'text-content-secondary'}`}>
        <span data-assignee-cell="" className="flex min-w-0 flex-col">
            <span className="flex min-w-0 items-center gap-1">
                <Icon aria-hidden="true" className="h-3.5 w-3.5 shrink-0" />
                <span className="truncate" title={task.assignee?.name ?? t('common.unassigned')}><span className="sr-only">{t('taskList.assignee')}: </span>{task.assignee?.name ?? t('common.unassigned')}</span>
                {durationDays !== undefined && <span className="shrink-0">· {t('units.daysCompact', { count: durationDays })}</span>}
            </span>
            {dispatch && <span data-agent-dispatch={dispatch} className="truncate pl-4.5 text-wc-micro" title={t(AGENT_DISPATCH_LABEL_KEY[dispatch])}>{t(AGENT_DISPATCH_LABEL_KEY[dispatch])}</span>}
        </span>
        {reviewer && <span data-reviewer-cell="" className="min-w-0 truncate" title={reviewer.name ? t('taskList.reviewerName', { name: reviewer.name }) : t('taskList.reviewerAnyoneTitle')}>
            {reviewer.name ? t('taskList.reviewerName', { name: reviewer.name }) : t('taskList.reviewerAnyone')}
        </span>}
    </span>;
};

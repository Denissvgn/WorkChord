import {
    CheckCircle2,
    Plus
} from 'lucide-react';
import { useState } from 'react';
import { useTranslation } from 'react-i18next';
import { Link, useNavigate } from 'react-router-dom';
import { Button } from '../common/Button';
import { ProjectTaskTree } from './ProjectTaskTree';
import { GuardedTaskDrawer } from '../tasks/GuardedTaskDrawer';
import type { Task } from '../../types/task';

import {
    InlineEmptyState,
    SectionCard,
    StatusSegmentStrip
} from '../ui';
import { STATUS_TONE } from '../ui/tone';
import { useScopeLink } from '../../features/scope/useScopeLink';

export const ProjectTasksTab = ({ tasks, summary, projectId: numericProjectId, isLoading: areTasksLoading }: {
    tasks: Task[]; summary?: import('../../types/project').ProjectSummary; projectId: number; isLoading: boolean;
}) => {
    const { t } = useTranslation();
    const navigate = useNavigate();
    const scopeLink = useScopeLink();
    const [newBacklogTask, setNewBacklogTask] = useState(false);
    const PROJECT_TASK_PREVIEW = 10;
    const statusCounts = summary?.status_counts || {};
    // The first ten root tasks, grouped by status in working order; the rest open in Tasks.
    const groupedPreview = (['active', 'planned', 'resolved', 'closed'] as const).reduce<{ status: Task['status']; total: number; tasks: Task[] }[]>((groups, status) => {
        const inStatus = tasks.filter(task => task.status === status);
        const shown = groups.reduce((count, group) => count + group.tasks.length, 0);
        const take = inStatus.slice(0, Math.max(0, PROJECT_TASK_PREVIEW - shown));
        return inStatus.length > 0 && take.length > 0 ? [...groups, { status, total: inStatus.length, tasks: take }] : groups;
    }, []);
    return (
        <SectionCard
            icon={<CheckCircle2 className="h-4 w-4 text-action" />}
            title={t('surfaces.projectDetail.linkedTasks')}
            count={<span className="text-xs text-content-secondary">· {tasks.length} {t('surfaces.projectDetail.rootTasks')}</span>}
            actions={(
                <div className="flex flex-wrap gap-2">
                    <Button variant="secondary" size="sm" onClick={() => setNewBacklogTask(true)}>{t('projectTabs.newTask')}</Button>
                    <Button variant="secondary" size="sm" onClick={() => navigate(scopeLink(`/tasks?layout=list&project=${numericProjectId}`, { project: numericProjectId }))}>{t('projectTabs.openTasks')}</Button>
                </div>
            )}
        >

            {newBacklogTask && <GuardedTaskDrawer title={t('projectTabs.newTask')} closeLabel={t('common.close')}
                iterationId={null} parentProjectId={numericProjectId} onClose={() => setNewBacklogTask(false)} />}
            <StatusSegmentStrip
                className="mb-4"
                segments={[
                    { key: 'planned', label: t('statuses.planned'), value: statusCounts.planned ?? 0, tone: STATUS_TONE.planned },
                    { key: 'active', label: t('statuses.active'), value: statusCounts.active ?? 0, tone: STATUS_TONE.active },
                    { key: 'resolved', label: t('statuses.resolved'), value: statusCounts.resolved ?? 0, tone: STATUS_TONE.resolved },
                    { key: 'closed', label: t('statuses.closed'), value: statusCounts.closed ?? 0, tone: STATUS_TONE.closed },
                ]}
            />

            {areTasksLoading ? (
                <div className="py-8 text-center text-sm text-content-secondary">{t('surfaces.projectDetail.loadingTasks')}</div>
            ) : tasks.length === 0 ? (
                <InlineEmptyState
                    title={t('surfaces.projectDetail.noTasksLinkedYet')}
                    actions={(
                        <>
                            <Button size="sm" variant="secondary" onClick={() => setNewBacklogTask(true)}>
                                <Plus className="mr-1.5 h-3.5 w-3.5" />
                                {t('surfaces.projectDetail.createTask')}
                            </Button>
                            <Button size="sm" variant="outline" onClick={() => navigate('/triage')}>
                                {t('surfaces.projectDetail.pullFromTriage')}
                            </Button>
                        </>
                    )}
                />
            ) : (
                <>
                    <ProjectTaskTree dependencyTasks={tasks} sections={groupedPreview.map(group => ({
                        key: group.status, heading: `${t(`statuses.${group.status}`)} · ${group.total}`, tasks: group.tasks,
                    }))} />
                    {tasks.length > PROJECT_TASK_PREVIEW && (
                        <Link className="btn sm secondary" to={scopeLink(`/tasks?project=${numericProjectId}`, { project: numericProjectId })}>
                            {t('surfaces.projectDetail.viewAllTasks', { count: tasks.length })}
                        </Link>
                    )}
                </>
            )}
        </SectionCard>
    );
};

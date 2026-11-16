import clsx from 'clsx';
import {
    ArrowDown,
    ArrowUp,
    CheckCircle2,
    Edit,
    Plus,
    Target,
    Trash2,
    XCircle
} from 'lucide-react';
import { Button } from '../common/Button';

import {
    projectStatusBadgeClassName
} from './projectStatusStyles';
import {
    SectionCard
} from '../ui';
import type {
    ProjectMilestone,
    ProjectMilestoneTaskGroup
} from '../../types/project';
import { formatDate } from '../../utils/formatDate';

import { formatNumber, milestoneStatusLabelKeys, t } from './projectDetailShared';
export const MilestonesSection = ({
    milestones,
    groups,
    isLoading,
    isActionPending,
    actionError,
    onCreate,
    onEdit,
    onComplete,
    onCancel,
    onDelete,
    onMove,
}: {
    milestones: ProjectMilestone[];
    groups: ProjectMilestoneTaskGroup[];
    isLoading: boolean;
    isActionPending: boolean;
    actionError: string | null;
    onCreate: () => void;
    onEdit: (milestone: ProjectMilestone) => void;
    onComplete: (milestone: ProjectMilestone) => void;
    onCancel: (milestone: ProjectMilestone) => void;
    onDelete: (milestone: ProjectMilestone) => void;
    onMove: (milestoneId: number, direction: -1 | 1) => void;
}) => {
    const groupsByMilestoneId = new Map<number, ProjectMilestoneTaskGroup>();
    for(const group of groups) {
        if(group.milestone_id !== null && group.milestone_id !== undefined) {
            groupsByMilestoneId.set(group.milestone_id, group);
        }
    }
    const unassignedGroup = groups.find(group => group.milestone_id === null || group.milestone_id === undefined);

    return (
        <SectionCard
            icon={<Target className="h-4 w-4 text-feedback-indigo" />}
            title={t('surfaces.projectDetail.projectMilestones')}
            count={<span className="rounded-full bg-surface-subtle px-1.5 text-wc-micro font-bold tabular-nums text-content-secondary">{milestones.length}</span>}
            actions={(
                <Button size="sm" variant="secondary" onClick={onCreate}>
                    <Plus className="mr-2 h-4 w-4" />
                    {t('surfaces.projectDetail.newMilestone')}
                </Button>
            )}
            testId="project-milestones-section"
        >
            {actionError && (
                <div className="mb-4 rounded-md bg-feedback-danger-muted p-3 text-sm text-feedback-danger-foreground">
                    {actionError}
                </div>
            )}

            {isLoading ? (
                <div className="rounded-md bg-surface-muted p-4 text-sm text-content-secondary">
                    {t('surfaces.projectDetail.loadingMilestones')}
                </div>
            ) : milestones.length === 0 ? (
                <div className="rounded-md bg-surface-muted p-4 text-sm text-content-secondary">
                    {t('surfaces.projectDetail.noMilestonesYet')}
                </div>
            ) : (
                <div className="divide-y divide-border-subtle rounded-md border border-border">
                    {milestones.map((milestone, index) => {
                        const group = groupsByMilestoneId.get(milestone.id);
                        const isFirst = index === 0;
                        const isLast = index === milestones.length - 1;

                        return (
                            <div key={milestone.id} className="px-4 py-4" data-testid="milestone-row">
                                <div className="flex flex-wrap items-start justify-between gap-4">
                                    <div className="min-w-0">
                                        <div className="flex flex-wrap items-center gap-2">
                                            <h3 className="font-semibold text-content-primary">{milestone.name}</h3>
                                            <span className={clsx('rounded-full border px-2 py-0.5 text-xs font-medium', projectStatusBadgeClassName(milestone.status))}>
                                                {t(milestoneStatusLabelKeys[milestone.status])}
                                            </span>
                                            <span className="rounded-full border border-border bg-surface-muted px-2 py-0.5 text-xs text-content-secondary">
                                                {t('surfaces.projectDetail.orderNumber', { order: milestone.sort_order })}
                                            </span>
                                        </div>
                                        {milestone.description && (
                                            <p className="mt-1 text-sm text-content-secondary">{milestone.description}</p>
                                        )}
                                        <p className="mt-2 text-xs text-content-secondary">
                                            {t('surfaces.projectDetail.targetValue', { date: formatDate(milestone.target_date) })}
                                            {' '}· {t('surfaces.projectDetail.completedValue', { date: formatDate(milestone.completed_at) })}
                                            {' '}· {t('surfaces.projectDetail.taskCount', { count: group?.task_count ?? 0 })}
                                            {' '}· {t('surfaces.projectDetail.percentDone', { percent: formatNumber(group?.completion_percent) })}
                                        </p>
                                    </div>
                                    <div className="flex flex-wrap items-center justify-end gap-2">
                                        <Button
                                            type="button"
                                            size="sm"
                                            variant="outline"
                                            aria-label={t('surfaces.projectDetail.moveMilestoneUp', { name: milestone.name })}
                                            title={t('surfaces.projectDetail.moveUp')}
                                            disabled={isActionPending || isFirst}
                                            onClick={() => onMove(milestone.id, -1)}
                                        >
                                            <ArrowUp className="mr-1 h-4 w-4" />
                                            {t('surfaces.projectDetail.up')}
                                        </Button>
                                        <Button
                                            type="button"
                                            size="sm"
                                            variant="outline"
                                            aria-label={t('surfaces.projectDetail.moveMilestoneDown', { name: milestone.name })}
                                            title={t('surfaces.projectDetail.moveDown')}
                                            disabled={isActionPending || isLast}
                                            onClick={() => onMove(milestone.id, 1)}
                                        >
                                            <ArrowDown className="mr-1 h-4 w-4" />
                                            {t('surfaces.projectDetail.down')}
                                        </Button>
                                        {milestone.status !== 'completed' && (
                                            <Button
                                                type="button"
                                                size="sm"
                                                variant="secondary"
                                                disabled={isActionPending}
                                                onClick={() => onComplete(milestone)}
                                            >
                                                <CheckCircle2 className="mr-1 h-4 w-4" />
                                                {t('surfaces.projectDetail.complete')}
                                            </Button>
                                        )}
                                        {milestone.status !== 'canceled' && (
                                            <Button
                                                type="button"
                                                size="sm"
                                                variant="secondary"
                                                disabled={isActionPending}
                                                onClick={() => onCancel(milestone)}
                                            >
                                                <XCircle className="mr-1 h-4 w-4" />
                                                {t('surfaces.projectDetail.cancel')}
                                            </Button>
                                        )}
                                        <Button
                                            type="button"
                                            size="sm"
                                            variant="outline"
                                            disabled={isActionPending}
                                            onClick={() => onEdit(milestone)}
                                        >
                                            <Edit className="mr-1 h-4 w-4" />
                                            {t('surfaces.projectDetail.edit')}
                                        </Button>
                                        <Button
                                            type="button"
                                            size="sm"
                                            variant="danger"
                                            disabled={isActionPending}
                                            onClick={() => onDelete(milestone)}
                                        >
                                            <Trash2 className="mr-1 h-4 w-4" />
                                            {t('surfaces.projectDetail.delete')}
                                        </Button>
                                    </div>
                                </div>
                                {group && (
                                    <div className="mt-3 h-2 rounded-full bg-surface-subtle">
                                        <div
                                            className="h-2 rounded-full bg-action"
                                            style={{ width: `${Math.min(100, Math.max(0, group.completion_percent))}%` }}
                                        />
                                    </div>
                                )}
                            </div>
                        );
                    })}
                </div>
            )}

            {unassignedGroup && (
                <div className="mt-4 rounded-md border border-dashed border-border-strong bg-surface-muted p-3 text-sm text-content-secondary">
                    {t('surfaces.projectDetail.unassignedMilestoneTasks', { count: unassignedGroup.task_count })}
                </div>
            )}
        </SectionCard>
    );
};


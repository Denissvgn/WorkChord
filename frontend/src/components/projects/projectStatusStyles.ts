import type { ProjectMilestoneStatus, ProjectStatus } from '../../types/project';
import {
    toneBorderClassName,
    wcPillClass,
    type PillTone,
} from '../ui/tone';

export type ProjectRecordStatus = ProjectStatus | ProjectMilestoneStatus;

const projectRecordStatusTone: Record<ProjectStatus, PillTone> = {
    proposed: 'gray',
    planned: 'gray',
    active: 'blue',
    paused: 'gray',
    completed: 'green',
    canceled: 'purple',
};

export const projectStatusBadgeClassName = (status: ProjectRecordStatus) => (
    toneBorderClassName[projectRecordStatusTone[status]]
);

export const projectStatusPillClassName = (status: ProjectRecordStatus) => (
    wcPillClass[projectRecordStatusTone[status]]
);

/** The health badge colours shared by project rows and initiative headers. */
export const projectHealthBadgeClassName = (health: string) => {
    switch (health) {
        case 'on_track':
            return 'border-feedback-success-border bg-feedback-success-muted text-feedback-success-foreground';
        case 'at_risk':
            return 'border-feedback-warning-border bg-feedback-warning-muted text-feedback-warning-foreground';
        case 'off_track':
            return 'border-feedback-danger-border bg-feedback-danger-muted text-feedback-danger-foreground';
        default:
            return 'border-border bg-surface-muted text-content-primary';
    }
};

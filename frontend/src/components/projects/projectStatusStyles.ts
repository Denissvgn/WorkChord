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

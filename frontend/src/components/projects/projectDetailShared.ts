import i18n from '../../i18n/i18n';


import type {
    ProjectHealth,
    ProjectMilestone,
    ProjectMilestoneCreateRequest,
    ProjectMilestoneStatus,
    ProjectMilestoneUpdateRequest,
    ProjectStatus,
    ProjectTargetDateRisk,
    ProjectUpdateEntry,
    ProjectUpdateFreshness
} from '../../types/project';
import type { ReleaseStatus } from '../../types/release';
import { formatDecimal } from '../../utils/workNumbers';

export const t = i18n.t.bind(i18n);

export const projectStatusLabelKeys: Record<ProjectStatus, string> = {
    proposed: 'surfaces.projectDetail.projectStatuses.proposed',
    planned: 'surfaces.projectDetail.projectStatuses.planned',
    active: 'surfaces.projectDetail.projectStatuses.active',
    paused: 'surfaces.projectDetail.projectStatuses.paused',
    completed: 'surfaces.projectDetail.projectStatuses.completed',
    canceled: 'surfaces.projectDetail.projectStatuses.canceled',
};

export const milestoneStatusLabelKeys: Record<ProjectMilestoneStatus, string> = {
    planned: 'surfaces.projectDetail.milestoneStatuses.planned',
    active: 'surfaces.projectDetail.milestoneStatuses.active',
    completed: 'surfaces.projectDetail.milestoneStatuses.completed',
    canceled: 'surfaces.projectDetail.milestoneStatuses.canceled',
};

export const healthLabelKeys: Record<ProjectHealth, string> = {
    unknown: 'surfaces.projectDetail.healths.unknown',
    on_track: 'surfaces.projectDetail.healths.onTrack',
    at_risk: 'surfaces.projectDetail.healths.atRisk',
    off_track: 'surfaces.projectDetail.healths.offTrack',
};

export const riskLabelKeys: Record<ProjectTargetDateRisk, string> = {
    unknown: 'surfaces.projectDetail.healths.unknown',
    on_track: 'surfaces.projectDetail.healths.onTrack',
    at_risk: 'surfaces.projectDetail.healths.atRisk',
    off_track: 'surfaces.projectDetail.healths.offTrack',
};

export const updateFreshnessLabelKeys: Record<ProjectUpdateFreshness, string> = {
    fresh: 'surfaces.projectDetail.freshness.fresh',
    stale: 'surfaces.projectDetail.freshness.stale',
    missing: 'surfaces.projectDetail.freshness.missing',
    not_required: 'surfaces.projectDetail.freshness.notRequired',
};

export const releaseStatusLabelKeys: Record<ReleaseStatus, string> = {
    planned: 'surfaces.projectDetail.releaseStatuses.planned',
    building: 'surfaces.projectDetail.releaseStatuses.building',
    shipped: 'surfaces.projectDetail.releaseStatuses.shipped',
    canceled: 'surfaces.projectDetail.releaseStatuses.canceled',
};

export const releaseBadgeClassName = (status: ReleaseStatus | string) => {
    switch(status) {
        case 'building':
            return 'bg-action-muted text-action border-action';
        case 'shipped':
            return 'bg-feedback-success-muted text-feedback-success-foreground border-feedback-success-border';
        case 'canceled':
            return 'bg-feedback-danger-muted text-feedback-danger-foreground border-feedback-danger-border';
        default:
            return 'bg-surface-muted text-content-primary border-border';
    }
};

export const riskTone = (risk?: string): 'gray' | 'green' | 'yellow' | 'red' => {
    switch(risk) {
        case 'on_track':
            return 'green';
        case 'at_risk':
            return 'yellow';
        case 'off_track':
            return 'red';
        default:
            return 'gray';
    }
};

export const formatNumber = (value?: number) => formatDecimal(value ?? 0, i18n.language) ?? '0';

export type ProjectUpdateFormState = {
    health: ProjectHealth;
    summary: string;
    progress_text: string;
    risks_text: string;
    decisions_text: string;
    next_steps_text: string;
};

export type ProjectUpdateFormStore = {
    projectId: number | null;
    form: ProjectUpdateFormState;
};

export type ProjectUpdateErrorStore = {
    projectId: number | null;
    message: string | null;
};

export type MilestoneFormState = {
    name: string;
    description: string;
    target_date: string;
    completed_at: string;
    sort_order: string;
    status: ProjectMilestoneStatus;
};

export type MilestoneEditorState = {
    mode: 'create' | 'edit';
    milestone: ProjectMilestone | null;
    form: MilestoneFormState;
    error: string | null;
};

export const createEmptyUpdateForm = (health: ProjectHealth): ProjectUpdateFormState => ({
    health,
    summary: '',
    progress_text: '',
    risks_text: '',
    decisions_text: '',
    next_steps_text: '',
});

export const nullableTrimmedText = (value: string) => {
    const trimmed = value.trim();
    return trimmed.length > 0 ? trimmed : null;
};

export const toDateInputValue = (value?: string | null) => value ? value.slice(0, 10) : '';
export const toDateTimeInputValue = (value?: string | null) => value ? value.slice(0, 16) : '';

export const createEmptyMilestoneForm = (sortOrder = 0): MilestoneFormState => ({
    name: '',
    description: '',
    target_date: '',
    completed_at: '',
    sort_order: String(sortOrder),
    status: 'planned',
});

export const createMilestoneFormFromRecord = (milestone: ProjectMilestone): MilestoneFormState => ({
    name: milestone.name,
    description: milestone.description ?? '',
    target_date: toDateInputValue(milestone.target_date),
    completed_at: toDateTimeInputValue(milestone.completed_at),
    sort_order: String(milestone.sort_order),
    status: milestone.status,
});

export const buildMilestonePayload = (form: MilestoneFormState): ProjectMilestoneCreateRequest | ProjectMilestoneUpdateRequest => {
    const sortOrder = Number.parseInt(form.sort_order, 10);
    return {
        name: form.name.trim(),
        description: nullableTrimmedText(form.description),
        target_date: form.target_date || null,
        completed_at: form.completed_at || null,
        sort_order: Number.isFinite(sortOrder) ? sortOrder : 0,
        status: form.status,
    };
};

export const formatUpdateAge = (days?: number | null) => {
    if(days === null || days === undefined) return null;
    if(days <= 0) return t('surfaces.projectDetail.updatedToday');
    if(days === 1) return t('surfaces.projectDetail.updatedYesterday');
    return t('surfaces.projectDetail.daysSinceUpdate', { count: days });
};

export const updateDetailFields = (update: ProjectUpdateEntry) => ([
    { label: t('surfaces.projectDetail.progress'), value: update.progress_text },
    { label: t('surfaces.projectDetail.risks'), value: update.risks_text },
    { label: t('surfaces.projectDetail.decisions'), value: update.decisions_text },
    { label: t('surfaces.projectDetail.nextSteps'), value: update.next_steps_text },
]).filter(field => Boolean(field.value?.trim()));

export const updateFreshnessMessage = (
    freshness: ProjectUpdateFreshness,
    daysSinceLatestUpdate?: number | null,
    thresholdDays = 7,
) => {
    if(freshness === 'missing') {
        return t('surfaces.projectDetail.noUpdateExpectedEvery', { count: thresholdDays });
    }
    if(freshness === 'stale') {
        return t('surfaces.projectDetail.daysSinceLatestUpdate', { count: daysSinceLatestUpdate ?? thresholdDays });
    }
    return null;
};

export const textareaClassName = 'w-full rounded-md border border-border-strong px-3 py-2 text-sm shadow-sm focus:border-action focus:outline-none focus:ring-1 focus:ring-focus disabled:bg-surface-muted disabled:text-content-secondary';

export const healthToTone = (health: ProjectHealth): 'gray' | 'green' | 'yellow' | 'red' => {
    switch(health) {
        case 'on_track': return 'green';
        case 'at_risk': return 'yellow';
        case 'off_track': return 'red';
        default: return 'gray';
    }
};

export const healthDotClass = (health: ProjectHealth) => {
    switch(health) {
        case 'on_track': return 'bg-feedback-success';
        case 'at_risk': return 'bg-feedback-warning';
        case 'off_track': return 'bg-feedback-danger';
        default: return 'bg-content-tertiary';
    }
};


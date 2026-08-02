import i18n from '../i18n/i18n';
import { useState } from 'react';
import type { FormEvent } from 'react';
import { Link, useNavigate, useParams } from 'react-router-dom';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import {
    Activity,
    AlertTriangle,
    ArrowDown,
    ArrowUp,
    CalendarDays,
    CheckCircle2,
    ChevronRight,
    Edit,
    FolderOpen,
    History,
    MessageSquare,
    Package,
    Plus,
    Send,
    Target,
    Trash2,
    User,
    XCircle,
} from 'lucide-react';
import clsx from 'clsx';
import { Button } from '../components/common/Button';
import { ConfirmDialog } from '../components/common/ConfirmDialog';
import { Modal } from '../components/common/Modal';
import { QueryErrorState } from '../components/feedback/QueryState';
import { Breadcrumbs } from '../components/layout/Breadcrumbs';
import { ProjectForm } from '../components/projects/ProjectForm';
import { ProjectIterationsSection } from '../components/projects/ProjectIterationsSection';
import { ProjectTaskTree } from '../components/projects/ProjectTaskTree';
import { RequestSourceLinksPanel } from '../components/requestSources/RequestSourceLinksPanel';
import { ReleaseForm } from '../components/releases/ReleaseForm';
import { projectService } from '../services/projectService';
import { releaseService } from '../services/releaseService';
import { getApiErrorMessage, getApiErrorStatus } from '../utils/apiError';
import { formatPortfolioOwnerLabel } from '../utils/teamMemberLabels';
import { formatDate, formatDateTime } from '../utils/formatDate';
import type {
    ProjectHealth,
    ProjectMilestone,
    ProjectMilestoneCreateRequest,
    ProjectMilestoneStatus,
    ProjectMilestoneTaskGroup,
    ProjectMilestoneUpdateRequest,
    ProjectStatus,
    ProjectTargetDateRisk,
    ProjectUpdateEntry,
    ProjectUpdateFreshness,
} from '../types/project';
import type { Release, ReleaseStatus } from '../types/release';
import {
    InlineEmptyState,
    OverflowMenu,
    MetricGrid,
    PageHeader,
    PageLayout,
    Pill,
    SectionCard,
    SlideOverDrawer,
    StatusSegmentStrip,
    StickyRail,
} from '../components/ui';
import { STATUS_TONE } from '../components/ui/tone';

const t = i18n.t.bind(i18n);

const projectStatusLabelKeys: Record<ProjectStatus, string> = {
    proposed: 'surfaces.projectDetail.projectStatuses.proposed',
    planned: 'surfaces.projectDetail.projectStatuses.planned',
    active: 'surfaces.projectDetail.projectStatuses.active',
    paused: 'surfaces.projectDetail.projectStatuses.paused',
    completed: 'surfaces.projectDetail.projectStatuses.completed',
    canceled: 'surfaces.projectDetail.projectStatuses.canceled',
};

const milestoneStatusLabelKeys: Record<ProjectMilestoneStatus, string> = {
    planned: 'surfaces.projectDetail.milestoneStatuses.planned',
    active: 'surfaces.projectDetail.milestoneStatuses.active',
    completed: 'surfaces.projectDetail.milestoneStatuses.completed',
    canceled: 'surfaces.projectDetail.milestoneStatuses.canceled',
};

const healthLabelKeys: Record<ProjectHealth, string> = {
    unknown: 'surfaces.projectDetail.healths.unknown',
    on_track: 'surfaces.projectDetail.healths.onTrack',
    at_risk: 'surfaces.projectDetail.healths.atRisk',
    off_track: 'surfaces.projectDetail.healths.offTrack',
};

const riskLabelKeys: Record<ProjectTargetDateRisk, string> = {
    unknown: 'surfaces.projectDetail.healths.unknown',
    on_track: 'surfaces.projectDetail.healths.onTrack',
    at_risk: 'surfaces.projectDetail.healths.atRisk',
    off_track: 'surfaces.projectDetail.healths.offTrack',
};

const updateFreshnessLabelKeys: Record<ProjectUpdateFreshness, string> = {
    fresh: 'surfaces.projectDetail.freshness.fresh',
    stale: 'surfaces.projectDetail.freshness.stale',
    missing: 'surfaces.projectDetail.freshness.missing',
    not_required: 'surfaces.projectDetail.freshness.notRequired',
};

const releaseStatusLabelKeys: Record<ReleaseStatus, string> = {
    planned: 'surfaces.projectDetail.releaseStatuses.planned',
    building: 'surfaces.projectDetail.releaseStatuses.building',
    shipped: 'surfaces.projectDetail.releaseStatuses.shipped',
    canceled: 'surfaces.projectDetail.releaseStatuses.canceled',
};

const badgeClassName = (value: string) => {
    switch (value) {
        case 'active':
        case 'on_track':
            return 'bg-action-muted text-action border-action';
        case 'completed':
        case 'closed':
            return 'bg-feedback-success-muted text-feedback-success-foreground border-feedback-success-border';
        case 'paused':
        case 'at_risk':
            return 'bg-feedback-warning-muted text-feedback-warning-foreground border-feedback-warning-border';
        case 'canceled':
        case 'off_track':
            return 'bg-feedback-danger-muted text-feedback-danger-foreground border-feedback-danger-border';
        case 'proposed':
            return 'bg-feedback-purple-muted text-feedback-purple-foreground border-feedback-purple-border';
        default:
            return 'bg-surface-muted text-content-primary border-border';
    }
};

const releaseBadgeClassName = (status: ReleaseStatus | string) => {
    switch (status) {
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

const riskTone = (risk?: string): 'gray' | 'green' | 'yellow' | 'red' => {
    switch (risk) {
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

const formatNumber = (value?: number) => (value ?? 0).toFixed(1).replace(/\.0$/, '');

type ProjectUpdateFormState = {
    health: ProjectHealth;
    summary: string;
    progress_text: string;
    risks_text: string;
    decisions_text: string;
    next_steps_text: string;
};

type ProjectUpdateFormStore = {
    projectId: number | null;
    form: ProjectUpdateFormState;
};

type ProjectUpdateErrorStore = {
    projectId: number | null;
    message: string | null;
};

type MilestoneFormState = {
    name: string;
    description: string;
    target_date: string;
    completed_at: string;
    sort_order: string;
    status: ProjectMilestoneStatus;
};

type MilestoneEditorState = {
    mode: 'create' | 'edit';
    milestone: ProjectMilestone | null;
    form: MilestoneFormState;
    error: string | null;
};

const createEmptyUpdateForm = (health: ProjectHealth): ProjectUpdateFormState => ({
    health,
    summary: '',
    progress_text: '',
    risks_text: '',
    decisions_text: '',
    next_steps_text: '',
});

const nullableTrimmedText = (value: string) => {
    const trimmed = value.trim();
    return trimmed.length > 0 ? trimmed : null;
};

const toDateInputValue = (value?: string | null) => value ? value.slice(0, 10) : '';
const toDateTimeInputValue = (value?: string | null) => value ? value.slice(0, 16) : '';

const createEmptyMilestoneForm = (sortOrder = 0): MilestoneFormState => ({
    name: '',
    description: '',
    target_date: '',
    completed_at: '',
    sort_order: String(sortOrder),
    status: 'planned',
});

const createMilestoneFormFromRecord = (milestone: ProjectMilestone): MilestoneFormState => ({
    name: milestone.name,
    description: milestone.description ?? '',
    target_date: toDateInputValue(milestone.target_date),
    completed_at: toDateTimeInputValue(milestone.completed_at),
    sort_order: String(milestone.sort_order),
    status: milestone.status,
});

const buildMilestonePayload = (form: MilestoneFormState): ProjectMilestoneCreateRequest | ProjectMilestoneUpdateRequest => {
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

const formatUpdateAge = (days?: number | null) => {
    if (days === null || days === undefined) return null;
    if (days <= 0) return t('surfaces.projectDetail.updatedToday');
    if (days === 1) return t('surfaces.projectDetail.updatedYesterday');
    return t('surfaces.projectDetail.daysSinceUpdate', { count: days });
};

const updateDetailFields = (update: ProjectUpdateEntry) => ([
    { label: t('surfaces.projectDetail.progress'), value: update.progress_text },
    { label: t('surfaces.projectDetail.risks'), value: update.risks_text },
    { label: t('surfaces.projectDetail.decisions'), value: update.decisions_text },
    { label: t('surfaces.projectDetail.nextSteps'), value: update.next_steps_text },
]).filter(field => Boolean(field.value?.trim()));

const updateFreshnessMessage = (
    freshness: ProjectUpdateFreshness,
    daysSinceLatestUpdate?: number | null,
    thresholdDays = 7,
) => {
    if (freshness === 'missing') {
        return t('surfaces.projectDetail.noUpdateExpectedEvery', { count: thresholdDays });
    }
    if (freshness === 'stale') {
        return t('surfaces.projectDetail.daysSinceLatestUpdate', { count: daysSinceLatestUpdate ?? thresholdDays });
    }
    return null;
};

const textareaClassName = 'w-full rounded-md border border-border-strong px-3 py-2 text-sm shadow-sm focus:border-action focus:outline-none focus:ring-1 focus:ring-focus disabled:bg-surface-muted disabled:text-content-secondary';

const MilestonesSection = ({
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
    for (const group of groups) {
        if (group.milestone_id !== null && group.milestone_id !== undefined) {
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
                <Button size="sm" onClick={onCreate}>
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
                                            <span className={clsx('rounded-full border px-2 py-0.5 text-xs font-medium', badgeClassName(milestone.status))}>
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

const MilestoneFormModal = ({
    mode,
    form,
    error,
    isSaving,
    onChange,
    onSubmit,
    onCancel,
}: {
    mode: 'create' | 'edit';
    form: MilestoneFormState;
    error: string | null;
    isSaving: boolean;
    onChange: <K extends keyof MilestoneFormState>(field: K, value: MilestoneFormState[K]) => void;
    onSubmit: (event: FormEvent<HTMLFormElement>) => void;
    onCancel: () => void;
}) => (
    <Modal
        open
        title={mode === 'create' ? t('surfaces.projectDetail.createMilestone') : t('surfaces.projectDetail.editMilestone')}
        closeLabel={t('actions.close')}
        onClose={onCancel}
    >
        <form className="space-y-4" onSubmit={onSubmit}>
            {error && (
                <div className="rounded-md bg-feedback-danger-muted p-3 text-sm text-feedback-danger-foreground">
                    {error}
                </div>
            )}

            <div className="grid grid-cols-1 gap-4 md:grid-cols-2">
                <label className="block text-sm font-medium text-content-primary" htmlFor="milestone-name">
                    {t('surfaces.projectDetail.milestoneName')}
                    <input
                        id="milestone-name"
                        value={form.name}
                        onChange={event => onChange('name', event.target.value)}
                        className="mt-1 w-full rounded-md border border-border-strong px-3 py-2 text-sm shadow-sm focus:border-action focus:outline-none focus:ring-1 focus:ring-focus"
                        maxLength={255}
                        required
                    />
                </label>
                <label className="block text-sm font-medium text-content-primary" htmlFor="milestone-status">
                    {t('surfaces.projectDetail.status')}
                    <select
                        id="milestone-status"
                        value={form.status}
                        onChange={event => onChange('status', event.target.value as ProjectMilestoneStatus)}
                        className="mt-1 w-full rounded-md border border-border-strong bg-surface-card px-3 py-2 text-sm shadow-sm focus:border-action focus:outline-none focus:ring-1 focus:ring-focus"
                    >
                        {Object.entries(milestoneStatusLabelKeys).map(([value, labelKey]) => (
                            <option key={value} value={value}>{t(labelKey)}</option>
                        ))}
                    </select>
                </label>
                <label className="block text-sm font-medium text-content-primary" htmlFor="milestone-target-date">
                    {t('surfaces.projectDetail.targetDate')}
                    <input
                        id="milestone-target-date"
                        type="date"
                        value={form.target_date}
                        onChange={event => onChange('target_date', event.target.value)}
                        className="mt-1 w-full rounded-md border border-border-strong px-3 py-2 text-sm shadow-sm focus:border-action focus:outline-none focus:ring-1 focus:ring-focus"
                    />
                </label>
                <label className="block text-sm font-medium text-content-primary" htmlFor="milestone-completed-at">
                    {t('surfaces.projectDetail.completedAt')}
                    <input
                        id="milestone-completed-at"
                        type="datetime-local"
                        value={form.completed_at}
                        onChange={event => onChange('completed_at', event.target.value)}
                        className="mt-1 w-full rounded-md border border-border-strong px-3 py-2 text-sm shadow-sm focus:border-action focus:outline-none focus:ring-1 focus:ring-focus"
                    />
                </label>
                <label className="block text-sm font-medium text-content-primary" htmlFor="milestone-sort-order">
                    {t('surfaces.projectDetail.sortOrder')}
                    <input
                        id="milestone-sort-order"
                        type="number"
                        value={form.sort_order}
                        onChange={event => onChange('sort_order', event.target.value)}
                        className="mt-1 w-full rounded-md border border-border-strong px-3 py-2 text-sm shadow-sm focus:border-action focus:outline-none focus:ring-1 focus:ring-focus"
                    />
                </label>
            </div>

            <label className="block text-sm font-medium text-content-primary" htmlFor="milestone-description">
                {t('surfaces.projectDetail.description')}
                <textarea
                    id="milestone-description"
                    value={form.description}
                    onChange={event => onChange('description', event.target.value)}
                    className={clsx('mt-1', textareaClassName)}
                    rows={3}
                />
            </label>

            <div className="flex justify-end gap-3">
                <Button type="button" variant="secondary" onClick={onCancel}>{t('surfaces.projectDetail.cancel')}</Button>
                <Button type="submit" isLoading={isSaving} disabled={!form.name.trim()}>
                    {mode === 'create' ? t('surfaces.projectDetail.createMilestone') : t('surfaces.projectDetail.saveMilestone')}
                </Button>
            </div>
        </form>
    </Modal>
);

const ReleaseList = ({
    releases,
    emptyText,
}: {
    releases: Release[];
    emptyText: string;
}) => {
    if (releases.length === 0) {
        return (
            <div className="rounded-md bg-surface-muted p-4 text-sm text-content-secondary">
                {emptyText}
            </div>
        );
    }

    return (
        <div className="divide-y divide-border-subtle rounded-md border border-border">
            {releases.map(release => (
                <Link
                    key={release.id}
                    to={`/projects/${release.project_id}/releases/${release.id}`}
                    className={clsx(
                        'block px-4 py-3 hover:bg-surface-muted',
                        release.status === 'canceled' && 'bg-surface-muted text-content-secondary'
                    )}
                >
                    <div className="flex flex-wrap items-center justify-between gap-3">
                        <div className="min-w-0">
                            <div className="flex flex-wrap items-center gap-2">
                                <span className="truncate font-medium text-content-primary">{release.name}</span>
                                <span className={clsx('rounded-full border px-2 py-0.5 text-xs font-medium', releaseBadgeClassName(release.status))}>
                                    {t(releaseStatusLabelKeys[release.status])}
                                </span>
                                {release.version && (
                                    <span className="rounded-full bg-surface-subtle px-2 py-0.5 text-xs text-content-secondary">
                                        {release.version}
                                    </span>
                                )}
                            </div>
                            <p className="mt-1 text-xs text-content-secondary">
                                {t('surfaces.projectDetail.linkedTaskCount', { count: release.tasks.length })}
                                {' '}· {t('surfaces.projectDetail.targetValue', { date: formatDate(release.target_date) })}
                                {release.shipped_at ? ` · ${t('surfaces.projectDetail.shippedValue', { date: formatDate(release.shipped_at) })}` : ''}
                            </p>
                        </div>
                        <span className="text-xs font-medium text-action">{t('surfaces.projectDetail.open')}</span>
                    </div>
                </Link>
            ))}
        </div>
    );
};

const ProjectReleasesSection = ({
    releases,
    isLoading,
    onCreate,
}: {
    releases: Release[];
    isLoading: boolean;
    onCreate: () => void;
}) => {
    const upcoming = releases.filter(release => (
        release.status === 'planned' || release.status === 'building'
    ));
    const shipped = releases.filter(release => release.status === 'shipped');
    const canceled = releases.filter(release => release.status === 'canceled');

    return (
        <SectionCard
            icon={<Package className="h-4 w-4 text-action" />}
            title={t('surfaces.projectDetail.releases')}
            count={<span className="rounded-full bg-surface-subtle px-1.5 text-wc-micro font-bold tabular-nums text-content-secondary">{releases.length}</span>}
            actions={(
                <Button size="sm" onClick={onCreate}>
                    <Plus className="mr-2 h-4 w-4" />
                    {t('surfaces.projectDetail.newRelease')}
                </Button>
            )}
        >
            {isLoading ? (
                <div className="rounded-md bg-surface-muted p-4 text-sm text-content-secondary">
                    {t('surfaces.projectDetail.loadingReleases')}
                </div>
            ) : releases.length === 0 ? (
                <div className="rounded-md bg-surface-muted p-4 text-sm text-content-secondary">
                    {t('surfaces.projectDetail.noReleasesYet')}
                </div>
            ) : (
                <div className="grid grid-cols-1 gap-4 lg:grid-cols-2">
                    <div>
                        <h3 className="mb-2 text-sm font-semibold text-content-primary">{t('surfaces.projectDetail.upcoming')}</h3>
                        <ReleaseList releases={upcoming} emptyText={t('surfaces.projectDetail.noUpcomingReleases')} />
                    </div>
                    <div>
                        <h3 className="mb-2 text-sm font-semibold text-content-primary">{t('surfaces.projectDetail.shipped')}</h3>
                        <ReleaseList releases={shipped} emptyText={t('surfaces.projectDetail.noShippedReleases')} />
                    </div>
                    {canceled.length > 0 && (
                        <div className="lg:col-span-2">
                            <h3 className="mb-2 text-sm font-semibold text-content-primary">{t('surfaces.projectDetail.canceled')}</h3>
                            <ReleaseList releases={canceled} emptyText={t('surfaces.projectDetail.noCanceledReleases')} />
                        </div>
                    )}
                </div>
            )}
        </SectionCard>
    );
};

const healthToTone = (health: ProjectHealth): 'gray' | 'green' | 'yellow' | 'red' => {
    switch (health) {
        case 'on_track': return 'green';
        case 'at_risk': return 'yellow';
        case 'off_track': return 'red';
        default: return 'gray';
    }
};

const healthDotClass = (health: ProjectHealth) => {
    switch (health) {
        case 'on_track': return 'bg-feedback-success';
        case 'at_risk': return 'bg-feedback-warning';
        case 'off_track': return 'bg-feedback-danger';
        default: return 'bg-content-tertiary';
    }
};

const PostUpdateDrawer = ({
    open,
    onClose,
    form,
    error,
    isPending,
    setField,
    onSubmit,
    onDismissError,
    summaryIsBlank,
    projectName,
}: {
    open: boolean;
    onClose: () => void;
    form: ProjectUpdateFormState;
    error: string | null;
    isPending: boolean;
    setField: <K extends keyof ProjectUpdateFormState>(field: K, value: ProjectUpdateFormState[K]) => void;
    onSubmit: (event: FormEvent<HTMLFormElement>) => void;
    onDismissError: () => void;
    summaryIsBlank: boolean;
    projectName: string;
}) => {
    return (
        <SlideOverDrawer
            open={open}
            onClose={onClose}
            ariaLabel={t('surfaces.projectDetail.postStatusUpdate')}
            title={t('surfaces.projectDetail.postStatusUpdate')}
            subtitle={(
                <>
                    {t('surfaces.projectDetail.visibleToSubscribersOf')} <span className="font-medium text-content-primary">{projectName}</span>
                </>
            )}
            icon={<Send className="h-4 w-4" />}
        >
            <form className="flex min-h-full flex-col overflow-hidden" onSubmit={onSubmit}>
                <div className="flex-1 space-y-4 overflow-y-auto p-5">
                    {error && (
                        <div className="flex items-start justify-between gap-3 rounded-md bg-feedback-danger-muted p-3 text-sm text-feedback-danger-foreground">
                            <div className="flex gap-2">
                                <AlertTriangle className="mt-0.5 h-4 w-4 flex-shrink-0" />
                                <span>{error}</span>
                            </div>
                            <button
                                type="button"
                                className="bg-transparent p-0 text-xs font-medium text-feedback-danger-foreground hover:underline"
                                onClick={onDismissError}
                            >
                                {t('surfaces.projectDetail.dismiss')}
                            </button>
                        </div>
                    )}

                    <div>
                        <label className="mb-1.5 block text-xs font-semibold text-content-primary" htmlFor="drawer-health">
                            {t('surfaces.projectDetail.health')} <span className="text-feedback-danger">*</span>
                        </label>
                        <div className="grid grid-cols-3 gap-2">
                            {(Object.entries(healthLabelKeys) as [ProjectHealth, string][]).filter(([k]) => k !== 'unknown').map(([value, labelKey]) => {
                                const active = form.health === value;
                                const tone = healthToTone(value);
                                const dot = healthDotClass(value);
                                const activeCls: Record<string, string> = {
                                    green:  'border-feedback-success-border bg-feedback-success-muted text-feedback-success-foreground',
                                    yellow: 'border-feedback-warning-border bg-feedback-warning-muted text-feedback-warning-foreground',
                                    red:    'border-feedback-danger-border bg-feedback-danger-muted text-feedback-danger-foreground',
                                    gray:   'border-border bg-surface-muted text-content-primary',
                                };
                                return (
                                    <button
                                        key={value}
                                        type="button"
                                        onClick={() => setField('health', value)}
                                        className={clsx(
                                            'inline-flex h-9 items-center gap-2 rounded-md border px-3 text-sm transition-colors',
                                            active ? clsx(activeCls[tone], 'font-semibold') : 'border-border bg-surface-card text-content-primary hover:bg-surface-muted',
                                        )}
                                    >
                                        <span className={clsx('h-2 w-2 rounded-full', dot)} />
                                        {t(labelKey)}
                                    </button>
                                );
                            })}
                        </div>
                    </div>

                    <div>
                        <div className="mb-1.5 flex items-baseline justify-between">
                            <label className="text-xs font-semibold text-content-primary" htmlFor="drawer-summary">{t('surfaces.projectDetail.summary')}</label>
                            <span className="text-wc-micro text-content-tertiary">{t('surfaces.projectDetail.oneLineStakeholdersWillSkim')}</span>
                        </div>
                        <input
                            id="drawer-summary"
                            value={form.summary}
                            onChange={event => setField('summary', event.target.value)}
                            placeholder={t('surfaces.projectDetail.eGSpecLandedEngKickoffTuesday')}
                            className="w-full rounded-md border border-border-strong px-3 py-2 text-sm shadow-sm focus:border-action focus:outline-none focus:ring-1 focus:ring-focus"
                            maxLength={500}
                        />
                    </div>

                    <div className="grid grid-cols-1 gap-3 md:grid-cols-2">
                        <div>
                            <label className="mb-1.5 block text-xs font-semibold text-content-primary" htmlFor="drawer-progress">{t('surfaces.projectDetail.progress')}</label>
                            <textarea
                                id="drawer-progress"
                                value={form.progress_text}
                                onChange={event => setField('progress_text', event.target.value)}
                                placeholder={t('surfaces.projectDetail.whatMovedThisWeek')}
                                className={textareaClassName}
                                rows={3}
                            />
                        </div>
                        <div>
                            <label className="mb-1.5 block text-xs font-semibold text-content-primary" htmlFor="drawer-risks">{t('surfaces.projectDetail.risks')}</label>
                            <textarea
                                id="drawer-risks"
                                value={form.risks_text}
                                onChange={event => setField('risks_text', event.target.value)}
                                placeholder={t('surfaces.projectDetail.whatMightSlip')}
                                className={textareaClassName}
                                rows={3}
                            />
                        </div>
                        <div>
                            <label className="mb-1.5 block text-xs font-semibold text-content-primary" htmlFor="drawer-decisions">{t('surfaces.projectDetail.decisions')}</label>
                            <textarea
                                id="drawer-decisions"
                                value={form.decisions_text}
                                onChange={event => setField('decisions_text', event.target.value)}
                                placeholder={t('surfaces.projectDetail.anythingNewLockedIn')}
                                className={textareaClassName}
                                rows={3}
                            />
                        </div>
                        <div>
                            <label className="mb-1.5 block text-xs font-semibold text-content-primary" htmlFor="drawer-next">{t('surfaces.projectDetail.nextSteps')}</label>
                            <textarea
                                id="drawer-next"
                                value={form.next_steps_text}
                                onChange={event => setField('next_steps_text', event.target.value)}
                                placeholder={t('surfaces.projectDetail.whatSNext')}
                                className={textareaClassName}
                                rows={3}
                            />
                        </div>
                    </div>
                </div>

                <footer className="flex items-center justify-end gap-2 border-t border-border-subtle p-4">
                    <Button type="button" variant="secondary" onClick={onClose}>{t('surfaces.projectDetail.cancel')}</Button>
                    <Button type="submit" isLoading={isPending} disabled={summaryIsBlank}>
                        {!isPending && <Send className="mr-2 h-4 w-4" />}
                        {t('surfaces.projectDetail.postUpdate')}
                    </Button>
                </footer>
            </form>
        </SlideOverDrawer>
    );
};
const ProjectDetailPage = () => {
    const { projectId } = useParams();
    const navigate = useNavigate();
    const { t } = useTranslation();
    const queryClient = useQueryClient();
    const numericProjectId = Number(projectId);
    const [isEditing, setIsEditing] = useState(false);
    const [showCreateRelease, setShowCreateRelease] = useState(false);
    const [showDeleteConfirm, setShowDeleteConfirm] = useState(false);
    const [showDetachConfirm, setShowDetachConfirm] = useState(false);
    const [deleteError, setDeleteError] = useState<string | null>(null);
    const [milestoneEditor, setMilestoneEditor] = useState<MilestoneEditorState | null>(null);
    const [deleteMilestoneTarget, setDeleteMilestoneTarget] = useState<ProjectMilestone | null>(null);
    const [milestoneActionError, setMilestoneActionError] = useState<string | null>(null);
    const [updateFormStore, setUpdateFormStore] = useState<ProjectUpdateFormStore>(() => ({
        projectId: null,
        form: createEmptyUpdateForm('unknown'),
    }));
    const [updateErrorStore, setUpdateErrorStore] = useState<ProjectUpdateErrorStore>({
        projectId: null,
        message: null,
    });
    const [postUpdateOpen, setPostUpdateOpen] = useState(false);
    const [historyOpen, setHistoryOpen] = useState(false);

    const enabled = Number.isInteger(numericProjectId) && numericProjectId > 0;

    const { data: project, isLoading: isProjectLoading, error: projectError, refetch: refetchProject } = useQuery({
        queryKey: ['project', numericProjectId],
        queryFn: () => projectService.getById(numericProjectId),
        enabled,
    });

    const { data: summary, error: summaryError, refetch: refetchSummary } = useQuery({
        queryKey: ['projectSummary', numericProjectId],
        queryFn: () => projectService.getSummary(numericProjectId),
        enabled,
    });

    const { data: projectMilestones = [], isLoading: areMilestonesLoading, error: milestonesError, refetch: refetchMilestones } = useQuery({
        queryKey: ['projectMilestones', numericProjectId],
        queryFn: () => projectService.getMilestones(numericProjectId),
        enabled,
    });

    const { data: tasks = [], isLoading: areTasksLoading, error: tasksError, refetch: refetchTasks } = useQuery({
        queryKey: ['projectTasks', numericProjectId],
        queryFn: () => projectService.getTasks(numericProjectId),
        enabled,
    });

    const { data: projectUpdates = [], isLoading: areUpdatesLoading, error: updatesError, refetch: refetchUpdates } = useQuery({
        queryKey: ['projectUpdates', numericProjectId],
        queryFn: () => projectService.getUpdates(numericProjectId),
        enabled,
    });

    const { data: projectReleases = [], isLoading: areReleasesLoading, error: releasesError, refetch: refetchReleases } = useQuery({
        queryKey: ['projectReleases', numericProjectId],
        queryFn: () => releaseService.getForProject(numericProjectId),
        enabled,
    });

    const { data: projectIterations = [], isLoading: areProjectIterationsLoading, error: iterationsError, refetch: refetchIterations } = useQuery({
        queryKey: ['projectIterations', numericProjectId],
        queryFn: () => projectService.getIterations(numericProjectId),
        enabled,
    });

    const updateForm = updateFormStore.projectId === numericProjectId
        ? updateFormStore.form
        : createEmptyUpdateForm(project?.health ?? 'unknown');
    const updateError = updateErrorStore.projectId === numericProjectId
        ? updateErrorStore.message
        : null;

    const invalidateAfterDelete = () => {
        queryClient.invalidateQueries({ queryKey: ['projects'] });
        queryClient.invalidateQueries({ queryKey: ['project', numericProjectId] });
        queryClient.invalidateQueries({ queryKey: ['projectSummary', numericProjectId] });
        queryClient.invalidateQueries({ queryKey: ['projectTasks', numericProjectId] });
        queryClient.invalidateQueries({ queryKey: ['projectReleases', numericProjectId] });
        queryClient.invalidateQueries({ queryKey: ['projectIterations', numericProjectId] });
        queryClient.invalidateQueries({ queryKey: ['tasks'] });
        queryClient.invalidateQueries({ queryKey: ['gantt'] });
    };

    const invalidateProjectRequestLinks = () => {
        queryClient.invalidateQueries({ queryKey: ['projects'] });
        queryClient.invalidateQueries({ queryKey: ['project', numericProjectId] });
        queryClient.invalidateQueries({ queryKey: ['projectSummary', numericProjectId] });
    };

    const invalidateProjectMilestones = () => {
        queryClient.invalidateQueries({ queryKey: ['projects'] });
        queryClient.invalidateQueries({ queryKey: ['project', numericProjectId] });
        queryClient.invalidateQueries({ queryKey: ['projectMilestones', numericProjectId] });
        queryClient.invalidateQueries({ queryKey: ['projectSummary', numericProjectId] });
        queryClient.invalidateQueries({ queryKey: ['projectTasks', numericProjectId] });
        queryClient.invalidateQueries({ queryKey: ['tasks'] });
        queryClient.invalidateQueries({ queryKey: ['gantt'] });
    };

    const deleteMutation = useMutation({
        mutationFn: (detachTasks: boolean) => projectService.delete(numericProjectId, detachTasks),
        onSuccess: () => {
            invalidateAfterDelete();
            navigate('/projects');
        },
        onError: (err: unknown) => {
            if (getApiErrorStatus(err) === 409) {
                setShowDeleteConfirm(false);
                setShowDetachConfirm(true);
                setDeleteError(null);
            } else {
                setDeleteError(getApiErrorMessage(err, t('surfaces.projectDetail.deleteProjectFailed')));
            }
        },
    });

    const createMilestoneMutation = useMutation({
        mutationFn: (data: ProjectMilestoneCreateRequest) => projectService.createMilestone(numericProjectId, data),
        onSuccess: () => {
            setMilestoneEditor(null);
            setMilestoneActionError(null);
            invalidateProjectMilestones();
        },
        onError: (err: unknown) => {
            setMilestoneEditor(previous => previous
                ? { ...previous, error: getApiErrorMessage(err, t('surfaces.projectDetail.createMilestoneFailed')) }
                : previous);
        },
    });

    const updateMilestoneMutation = useMutation({
        mutationFn: ({ milestoneId, data }: { milestoneId: number; data: ProjectMilestoneUpdateRequest }) => (
            projectService.updateMilestone(numericProjectId, milestoneId, data)
        ),
        onSuccess: () => {
            setMilestoneEditor(null);
            setMilestoneActionError(null);
            invalidateProjectMilestones();
        },
        onError: (err: unknown) => {
            const message = getApiErrorMessage(err, t('surfaces.projectDetail.updateMilestoneFailed'));
            setMilestoneEditor(previous => previous ? { ...previous, error: message } : previous);
            setMilestoneActionError(message);
        },
    });

    const deleteMilestoneMutation = useMutation({
        mutationFn: (milestoneId: number) => projectService.deleteMilestone(numericProjectId, milestoneId),
        onSuccess: () => {
            setDeleteMilestoneTarget(null);
            setMilestoneActionError(null);
            invalidateProjectMilestones();
        },
        onError: (err: unknown) => {
            setMilestoneActionError(getApiErrorMessage(err, t('surfaces.projectDetail.deleteMilestoneFailed')));
        },
    });

    const reorderMilestoneMutation = useMutation({
        mutationFn: async ({ milestoneId, direction }: { milestoneId: number; direction: -1 | 1 }) => {
            const currentIndex = projectMilestones.findIndex(milestone => milestone.id === milestoneId);
            const nextIndex = currentIndex + direction;
            if (currentIndex < 0 || nextIndex < 0 || nextIndex >= projectMilestones.length) return;

            const reordered = [...projectMilestones];
            [reordered[currentIndex], reordered[nextIndex]] = [reordered[nextIndex], reordered[currentIndex]];
            await Promise.all(reordered.map((milestone, index) => (
                projectService.updateMilestone(
                    numericProjectId,
                    milestone.id,
                    { sort_order: (index + 1) * 10 },
                )
            )));
        },
        onSuccess: () => {
            setMilestoneActionError(null);
            invalidateProjectMilestones();
        },
        onError: (err: unknown) => {
            setMilestoneActionError(getApiErrorMessage(err, t('surfaces.projectDetail.reorderMilestonesFailed')));
        },
    });

    const createUpdateMutation = useMutation({
        mutationFn: () => projectService.createUpdate(numericProjectId, {
            health: updateForm.health,
            summary: updateForm.summary.trim(),
            progress_text: nullableTrimmedText(updateForm.progress_text),
            risks_text: nullableTrimmedText(updateForm.risks_text),
            decisions_text: nullableTrimmedText(updateForm.decisions_text),
            next_steps_text: nullableTrimmedText(updateForm.next_steps_text),
        }),
        onSuccess: (update) => {
            setUpdateFormStore({
                projectId: numericProjectId,
                form: createEmptyUpdateForm(update.health),
            });
            setUpdateErrorStore({ projectId: numericProjectId, message: null });
            queryClient.invalidateQueries({ queryKey: ['projects'] });
            queryClient.invalidateQueries({ queryKey: ['project', numericProjectId] });
            queryClient.invalidateQueries({ queryKey: ['projectSummary', numericProjectId] });
            queryClient.invalidateQueries({ queryKey: ['projectUpdates', numericProjectId] });
        },
        onError: (err: unknown) => {
            setUpdateErrorStore({
                projectId: numericProjectId,
                message: getApiErrorMessage(err, t('surfaces.projectDetail.postUpdateFailed')),
            });
        },
    });

    const handleCreateUpdate = (event: FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        if (!updateForm.summary.trim() || createUpdateMutation.isPending) return;
        setUpdateErrorStore({ projectId: numericProjectId, message: null });
        createUpdateMutation.mutate();
    };

    const setUpdateField = <K extends keyof ProjectUpdateFormState>(
        field: K,
        value: ProjectUpdateFormState[K],
    ) => {
        setUpdateFormStore(previous => {
            const currentForm = previous.projectId === numericProjectId
                ? previous.form
                : createEmptyUpdateForm(project?.health ?? 'unknown');

            return {
                projectId: numericProjectId,
                form: { ...currentForm, [field]: value },
            };
        });
        if (updateError) {
            setUpdateErrorStore({ projectId: numericProjectId, message: null });
        }
    };

    const nextMilestoneSortOrder = projectMilestones.length
        ? Math.max(...projectMilestones.map(milestone => milestone.sort_order)) + 10
        : 10;

    const openCreateMilestone = () => {
        setMilestoneActionError(null);
        setMilestoneEditor({
            mode: 'create',
            milestone: null,
            form: createEmptyMilestoneForm(nextMilestoneSortOrder),
            error: null,
        });
    };

    const openEditMilestone = (milestone: ProjectMilestone) => {
        setMilestoneActionError(null);
        setMilestoneEditor({
            mode: 'edit',
            milestone,
            form: createMilestoneFormFromRecord(milestone),
            error: null,
        });
    };

    const setMilestoneField = <K extends keyof MilestoneFormState>(
        field: K,
        value: MilestoneFormState[K],
    ) => {
        setMilestoneEditor(previous => previous
            ? {
                ...previous,
                form: { ...previous.form, [field]: value },
                error: null,
            }
            : previous);
    };

    const handleSaveMilestone = (event: FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        if (!milestoneEditor || !milestoneEditor.form.name.trim()) return;

        const payload = buildMilestonePayload(milestoneEditor.form);
        if (milestoneEditor.mode === 'create') {
            createMilestoneMutation.mutate(payload as ProjectMilestoneCreateRequest);
            return;
        }

        if (milestoneEditor.milestone) {
            updateMilestoneMutation.mutate({
                milestoneId: milestoneEditor.milestone.id,
                data: payload,
            });
        }
    };

    const completeMilestone = (milestone: ProjectMilestone) => {
        updateMilestoneMutation.mutate({
            milestoneId: milestone.id,
            data: { status: 'completed' },
        });
    };

    const cancelMilestone = (milestone: ProjectMilestone) => {
        updateMilestoneMutation.mutate({
            milestoneId: milestone.id,
            data: { status: 'canceled', completed_at: null },
        });
    };

    const isMilestoneActionPending = (
        createMilestoneMutation.isPending
        || updateMilestoneMutation.isPending
        || deleteMilestoneMutation.isPending
        || reorderMilestoneMutation.isPending
    );

    if (!enabled) {
        return (
            <div className="py-20 text-center">
                <h1 className="text-xl font-semibold text-content-primary">{t('surfaces.projectDetail.projectNotFound')}</h1>
                <Button className="mt-4" onClick={() => navigate('/projects')}>{t('surfaces.projectDetail.backToProjects')}</Button>
            </div>
        );
    }

    if (isProjectLoading) {
        return (
            <div className="py-20 text-center text-content-secondary">
                <Activity className="mx-auto mb-2 h-5 w-5 animate-pulse" />
                {t('surfaces.projectDetail.loadingProject')}
            </div>
        );
    }

    const projectQueryError = projectError
        ?? summaryError
        ?? milestonesError
        ?? tasksError
        ?? updatesError
        ?? releasesError
        ?? iterationsError;

    if (projectQueryError) {
        return (
            <QueryErrorState
                error={projectQueryError}
                onRetry={() => {
                    void refetchProject();
                    void refetchSummary();
                    void refetchMilestones();
                    void refetchTasks();
                    void refetchUpdates();
                    void refetchReleases();
                    void refetchIterations();
                }}
            />
        );
    }

    if (!project) {
        return (
            <div className="py-20 text-center">
                <FolderOpen className="mx-auto h-10 w-10 text-content-tertiary" />
                <h1 className="mt-3 text-xl font-semibold text-content-primary">{t('surfaces.projectDetail.projectNotFound')}</h1>
                <Button className="mt-4" onClick={() => navigate('/projects')}>{t('surfaces.projectDetail.backToProjects')}</Button>
            </div>
        );
    }

    const completionText = summary
        ? `${summary.completed_tasks}/${summary.total_tasks}`
        : '0/0';
    const statusCounts = summary?.status_counts || {};
    const latestUpdate = summary?.latest_update ?? projectUpdates[0] ?? null;
    const latestUpdateAge = summary?.latest_update
        ? formatUpdateAge(summary.days_since_latest_update)
        : null;
    const updateSummaryIsBlank = updateForm.summary.trim().length === 0;
    const freshnessWarning = summary
        ? updateFreshnessMessage(
            summary.update_freshness,
            summary.days_since_latest_update,
            summary.stale_update_threshold_days,
        )
        : null;

    const projectHealth: ProjectHealth = project?.health ?? 'unknown';
    const projectStatus = project?.status ?? 'planned';
    const completionPercent = Math.min(100, Math.max(0, summary?.completion_percent ?? 0));

    return (
        <PageLayout>
            <Breadcrumbs items={[
                { label: t('breadcrumbs.projects'), path: '/projects' },
                { label: project.name },
            ]} />

            <PageHeader
                title={project.name}
                subtitle={project.description}
                meta={(
                    <>
                        <span className="pill opt"><span className="pdot"/>{t(projectStatusLabelKeys[projectStatus])}</span>
                        <span className={`pill ${healthToTone(projectHealth) === 'green' ? 'done' : healthToTone(projectHealth) === 'yellow' ? 'warn' : healthToTone(projectHealth) === 'red' ? 'blocked' : 'opt'}`}>
                            <span className="pdot"/>{t(healthLabelKeys[projectHealth])}
                        </span>
                        {summary && (
                            <span className={`pill ${summary.update_freshness === 'fresh' ? 'done' : summary.update_freshness === 'stale' ? 'warn' : summary.update_freshness === 'missing' ? 'blocked' : 'opt'}`}>
                                <span className="pdot"/>{t(updateFreshnessLabelKeys[summary.update_freshness])}{latestUpdateAge ? ` · ${latestUpdateAge.toLowerCase()}` : ''}
                            </span>
                        )}
                        <span><CalendarDays className="inline h-3.5 w-3.5 mr-1"/>
                            {formatDate(project.start_date)} – {formatDate(project.target_date)}
                            {typeof summary?.days_until_target === 'number' && ` · ${summary.days_until_target}d left`}
                        </span>
                        <span><User className="inline h-3.5 w-3.5 mr-1"/>
                            {formatPortfolioOwnerLabel(project.owner_profile, project.owner, project.owner_id, '—')}
                        </span>
                    </>
                )}
                actions={(
                    <>
                    <Button onClick={() => setPostUpdateOpen(true)}>
                        <Send className="mr-2 h-4 w-4"/>{t('surfaces.projectDetail.postUpdate')}
                    </Button>
                    <Button variant="secondary" onClick={() => setIsEditing(true)}>
                        <Edit className="mr-2 h-4 w-4"/>{t('surfaces.projectDetail.edit')}
                    </Button>
                    <OverflowMenu label={t('surfaces.projectDetail.projectActions')} items={[{
                        label: t('surfaces.projectDetail.deleteProject'),
                        icon: <Trash2 className="h-3.5 w-3.5"/>,
                        tone: 'danger',
                        onSelect: () => setShowDeleteConfirm(true),
                    }]}/>
                    </>
                )}
            />

            {/* Progress bar */}
            <div>
                <div style={{display:'flex', justifyContent:'space-between', fontSize:11.5, color:'var(--ink-3)', marginBottom:6}}>
                    <span style={{fontWeight:500, color:'var(--ink)'}}>{t('surfaces.projectDetail.completion')}</span>
                    <span className="tnum">{completionText} {t('surfaces.projectDetail.tasks')} · <b style={{color:'var(--ink)'}}>{formatNumber(summary?.completion_percent)}%</b></span>
                </div>
                <div style={{height:6, background:'var(--panel-3)', borderRadius:999, overflow:'hidden'}}>
                    <div style={{height:'100%', width:`${completionPercent}%`, background:'var(--done)', borderRadius:999}}/>
                </div>
            </div>

            <MetricGrid>
                <div className="kpi"><div className="kpi-lbl">{t('surfaces.projectDetail.active')}</div><div className="kpi-val tnum">{summary?.active_tasks ?? 0}</div></div>
                <div className="kpi"><div className="kpi-lbl">{t('surfaces.projectDetail.blocked')}</div><div className="kpi-val tnum">{summary?.blocked_tasks ?? 0}</div></div>
                <div className="kpi"><div className="kpi-lbl">{t('surfaces.projectDetail.overdue')}</div><div className="kpi-val tnum">{summary?.overdue_tasks ?? 0}</div></div>
                <div className="kpi"><div className="kpi-lbl">{t('surfaces.projectDetail.requests')}</div><div className="kpi-val tnum">{summary?.request_count ?? 0}</div></div>
            </MetricGrid>

            {/* ── Two-column workspace: main content + sticky right rail ─── */}
            <div className="wc-content-rail">
                <div className="wc-panel-stack">
                    {/* Latest Update — content-sized, no more 200px void */}
                    <SectionCard
                        icon={<MessageSquare className="h-4 w-4 text-action" />}
                        title={t('surfaces.projectDetail.latestUpdate')}
                        actions={latestUpdate && (
                            <span className="text-xs tabular-nums text-content-secondary">{formatDateTime(latestUpdate.created_at)}</span>
                        )}
                    >
                        {freshnessWarning && (
                            <div className="mb-3 flex gap-2 rounded-md bg-feedback-warning-muted p-3 text-sm text-feedback-warning-foreground">
                                <AlertTriangle className="mt-0.5 h-4 w-4 flex-shrink-0" />
                                <span>{freshnessWarning}</span>
                            </div>
                        )}

                        {latestUpdate ? (
                            <div className="border-l-2 border-border pl-4">
                                <div className="mb-2 flex flex-wrap items-center gap-2">
                                    <Pill tone={healthToTone(latestUpdate.health)} icon={<span className={clsx('h-1.5 w-1.5 rounded-full', healthDotClass(latestUpdate.health))} />}>
                                        {t(healthLabelKeys[latestUpdate.health])}
                                    </Pill>
                                    {latestUpdateAge && <span className="text-xs text-content-secondary">{latestUpdateAge}</span>}
                                </div>
                                <p className="text-sm font-medium text-content-primary">{latestUpdate.summary}</p>
                                {updateDetailFields(latestUpdate).length > 0 && (
                                    <div className="mt-3 grid grid-cols-1 gap-3 text-xs md:grid-cols-4">
                                        {updateDetailFields(latestUpdate).map(field => (
                                            <div key={field.label}>
                                                <p className="text-wc-micro font-semibold uppercase tracking-wide text-content-tertiary">{field.label}</p>
                                                <p className="mt-0.5 text-content-primary">{field.value}</p>
                                            </div>
                                        ))}
                                    </div>
                                )}
                            </div>
                        ) : (
                            <InlineEmptyState
                                title={t('surfaces.projectDetail.noProjectUpdatesYet')}
                                actions={(
                                    <Button size="sm" onClick={() => setPostUpdateOpen(true)}>
                                        <Send className="mr-1.5 h-3.5 w-3.5" />
                                        {t('surfaces.projectDetail.postFirstUpdate')}
                                    </Button>
                                )}
                            />
                        )}
                    </SectionCard>

                    {/* Releases */}
                    <ProjectReleasesSection
                        releases={projectReleases}
                        isLoading={areReleasesLoading}
                        onCreate={() => setShowCreateRelease(true)}
                    />

                    <ProjectIterationsSection
                        projectId={numericProjectId}
                        projectName={project.name}
                        iterations={projectIterations}
                        isLoading={areProjectIterationsLoading}
                    />

                    {/* Milestones */}
                    <MilestonesSection
                        milestones={projectMilestones}
                        groups={summary?.milestone_groups ?? []}
                        isLoading={areMilestonesLoading}
                        isActionPending={isMilestoneActionPending}
                        actionError={milestoneActionError}
                        onCreate={openCreateMilestone}
                        onEdit={openEditMilestone}
                        onComplete={completeMilestone}
                        onCancel={cancelMilestone}
                        onDelete={setDeleteMilestoneTarget}
                        onMove={(milestoneId, direction) => reorderMilestoneMutation.mutate({ milestoneId, direction })}
                    />

                    {/* Project Requests */}
                    <RequestSourceLinksPanel
                        targetType="project"
                        targetId={numericProjectId}
                        initialCount={summary?.request_count ?? 0}
                        title={t('surfaces.projectDetail.projectRequests')}
                        onChanged={invalidateProjectRequestLinks}
                    />

                    {/* Linked Tasks (Status Counts folded in as the scope strip) */}
                    <SectionCard
                        icon={<CheckCircle2 className="h-4 w-4 text-action" />}
                        title={t('surfaces.projectDetail.linkedTasks')}
                        count={<span className="text-xs text-content-secondary">· {tasks.length} {t('surfaces.projectDetail.rootTasks')}</span>}
                        actions={(
                            <Button variant="secondary" size="sm" onClick={() => navigate('/tasks')}>
                                {t('surfaces.projectDetail.openTaskBoard')}
                            </Button>
                        )}
                    >

                        {/* Status segments — moved from a standalone "Status Counts" card to here, where they actually scope the list below */}
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
                                    <Button size="sm" onClick={() => navigate('/tasks')}>
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
                            <ProjectTaskTree tasks={tasks} />
                        )}
                    </SectionCard>

                    {/* Update History — collapsed by default */}
                    <div className="rounded-xl border border-border bg-surface-card shadow-sm">
                        <button
                            type="button"
                            onClick={() => setHistoryOpen(open => !open)}
                            className="flex w-full items-center gap-2 px-5 py-3.5 text-left"
                            aria-expanded={historyOpen}
                        >
                            <History className="h-4 w-4 text-content-secondary" />
                            <h2 className="text-base font-semibold tracking-tight text-content-primary">{t('surfaces.projectDetail.updateHistory')}</h2>
                            <span className="rounded-full bg-surface-subtle px-1.5 text-wc-micro font-bold tabular-nums text-content-secondary">{projectUpdates.length}</span>
                            <div className="flex-1" />
                            <span className="text-xs text-content-secondary">{t('surfaces.projectDetail.newestFirst')}</span>
                            <ChevronRight className={clsx('h-4 w-4 text-content-tertiary transition-transform', historyOpen && 'rotate-90')} />
                        </button>
                        {historyOpen && (
                            <div className="border-t border-border-subtle px-5 py-4">
                                {areUpdatesLoading ? (
                                    <div className="py-8 text-center text-sm text-content-secondary">{t('surfaces.projectDetail.loadingUpdates')}</div>
                                ) : projectUpdates.length === 0 ? (
                                    <div className="rounded-md bg-surface-muted p-4 text-sm text-content-secondary">{t('surfaces.projectDetail.noProjectUpdatesYet')}</div>
                                ) : (
                                    <ol className="relative space-y-4 pl-5 before:absolute before:bottom-1 before:left-1.5 before:top-1.5 before:w-px before:bg-surface-hover">
                                        {projectUpdates.map(update => {
                                            const details = updateDetailFields(update);
                                            return (
                                                <li key={update.id} className="relative">
                                                    <span className={clsx('absolute -left-[18px] top-1 h-3 w-3 rounded-full ring-4 ring-surface-card', healthDotClass(update.health))} />
                                                    <div className="flex flex-wrap items-center gap-2">
                                                        <Pill tone={healthToTone(update.health)} icon={<span className={clsx('h-1.5 w-1.5 rounded-full', healthDotClass(update.health))} />}>
                                                            {t(healthLabelKeys[update.health])}
                                                        </Pill>
                                                        <span className="text-xs tabular-nums text-content-secondary">{formatDateTime(update.created_at)}</span>
                                                    </div>
                                                    <p className="mt-1.5 text-sm font-medium text-content-primary">{update.summary}</p>
                                                    {details.length > 0 && (
                                                        <div className="mt-2 grid grid-cols-1 gap-2 text-sm md:grid-cols-2">
                                                            {details.map(field => (
                                                                <div key={field.label}>
                                                                    <span className="text-xs font-semibold uppercase tracking-wide text-content-secondary">{field.label}: </span>
                                                                    <span className="text-content-primary">{field.value}</span>
                                                                </div>
                                                            ))}
                                                        </div>
                                                    )}
                                                </li>
                                            );
                                        })}
                                    </ol>
                                )}
                            </div>
                        )}
                    </div>
                </div>

                {/* ── Sticky right rail: facts at a glance ─────────────────── */}
                <StickyRail>
                    {/* Date risk */}
                    <div className="rounded-xl border border-border bg-surface-card p-5 shadow-sm">
                        <div className="mb-3 flex items-center gap-2">
                            <AlertTriangle className="h-4 w-4 text-content-secondary" />
                            <h2 className="text-sm font-semibold tracking-tight text-content-primary">{t('surfaces.projectDetail.targetDateRisk')}</h2>
                            <div className="flex-1" />
                            <Pill tone={riskTone(summary?.target_date_risk)}>{t(riskLabelKeys[summary?.target_date_risk || 'unknown'])}</Pill>
                        </div>
                        <div className="space-y-2 text-sm">
                            <div className="flex items-baseline justify-between">
                                <span className="text-content-secondary">{t('surfaces.projectDetail.daysUntilTarget')}</span>
                                <span className="font-semibold tabular-nums text-content-primary">{summary?.days_until_target ?? '—'}</span>
                            </div>
                            <div className="flex items-baseline justify-between">
                                <span className="text-content-secondary">{t('surfaces.projectDetail.slip')}</span>
                                <span className="font-semibold tabular-nums text-content-primary">{summary?.target_date_slip_days ?? 0}d</span>
                            </div>
                            <div className="flex items-baseline justify-between">
                                <span className="text-content-secondary">{t('surfaces.projectDetail.taskRange')}</span>
                                <span className="font-medium tabular-nums text-content-primary">
                                    {formatDate(summary?.task_start_date)} – {formatDate(summary?.task_end_date)}
                                </span>
                            </div>
                        </div>
                        {summary?.target_date_risk_reason && (
                            <p className="mt-3 rounded-md bg-surface-muted p-3 text-xs text-content-secondary">
                                {summary.target_date_risk_reason}
                            </p>
                        )}
                    </div>

                    {/* Effort */}
                    <div className="rounded-xl border border-border bg-surface-card p-5 shadow-sm">
                        <div className="mb-3 flex items-center gap-2">
                            <Activity className="h-4 w-4 text-content-secondary" />
                            <h2 className="text-sm font-semibold tracking-tight text-content-primary">{t('surfaces.projectDetail.effort')}</h2>
                        </div>
                        <div className="space-y-3">
                            <div>
                                <div className="mb-1 flex justify-between text-sm">
                                    <span className="text-content-secondary">{t('surfaces.projectDetail.remaining')}</span>
                                    <span className="font-semibold tabular-nums text-content-primary">{formatNumber(summary?.remaining_effort_days)}d</span>
                                </div>
                                <div className="h-1.5 overflow-hidden rounded-full bg-surface-subtle">
                                    <div
                                        className="h-full rounded-full bg-action"
                                        style={{
                                            width: `${summary?.total_effort_days
                                                ? Math.min(100, (summary.remaining_effort_days / summary.total_effort_days) * 100)
                                                : 0}%`,
                                        }}
                                    />
                                </div>
                            </div>
                            <div className="flex justify-between text-sm">
                                <span className="text-content-secondary">{t('surfaces.projectDetail.total')}</span>
                                <span className="font-medium tabular-nums text-content-primary">{formatNumber(summary?.total_effort_days)}d</span>
                            </div>
                        </div>
                    </div>

                </StickyRail>
            </div>

            {/* ── Drawer + modals (modals unchanged) ─────────────────────── */}
            <PostUpdateDrawer
                open={postUpdateOpen}
                onClose={() => setPostUpdateOpen(false)}
                form={updateForm}
                error={updateError}
                isPending={createUpdateMutation.isPending}
                setField={setUpdateField}
                onSubmit={(event) => { handleCreateUpdate(event); if (!updateSummaryIsBlank) setPostUpdateOpen(false); }}
                onDismissError={() => setUpdateErrorStore({ projectId: numericProjectId, message: null })}
                summaryIsBlank={updateSummaryIsBlank}
                projectName={project.name}
            />

            <Modal open={showCreateRelease} title={t('surfaces.projectDetail.createRelease')} closeLabel={t('actions.close')} onClose={() => setShowCreateRelease(false)} className="max-w-3xl">
                {showCreateRelease && (
                        <ReleaseForm
                            projectId={numericProjectId}
                            onSuccess={(release) => {
                                setShowCreateRelease(false);
                                navigate(`/projects/${numericProjectId}/releases/${release.id}`);
                            }}
                            onCancel={() => setShowCreateRelease(false)}
                        />
                )}
            </Modal>

            <Modal open={isEditing} title={t('surfaces.projectDetail.editProject')} closeLabel={t('actions.close')} onClose={() => setIsEditing(false)}>
                {isEditing && (
                        <ProjectForm
                            initialData={project}
                            onSuccess={() => setIsEditing(false)}
                            onCancel={() => setIsEditing(false)}
                        />
                )}
            </Modal>

            {milestoneEditor && (
                <MilestoneFormModal
                    mode={milestoneEditor.mode}
                    form={milestoneEditor.form}
                    error={milestoneEditor.error}
                    isSaving={createMilestoneMutation.isPending || updateMilestoneMutation.isPending}
                    onChange={setMilestoneField}
                    onSubmit={handleSaveMilestone}
                    onCancel={() => setMilestoneEditor(null)}
                />
            )}

            <ConfirmDialog
                open={deleteMilestoneTarget !== null}
                title={t('surfaces.projectDetail.deleteMilestone')}
                description={<strong>{deleteMilestoneTarget?.name}</strong>}
                confirmLabel={t('surfaces.projectDetail.deleteMilestone')}
                cancelLabel={t('surfaces.projectDetail.cancel')}
                closeLabel={t('actions.close')}
                pending={deleteMilestoneMutation.isPending}
                onCancel={() => setDeleteMilestoneTarget(null)}
                onConfirm={() => { if (deleteMilestoneTarget) deleteMilestoneMutation.mutate(deleteMilestoneTarget.id); }}
            />

            <ConfirmDialog
                open={showDeleteConfirm}
                title={t('surfaces.projectDetail.deleteProjectText')}
                description={<><strong>{project.name}</strong>{deleteError && <span role="alert" className="mt-2 block text-feedback-danger-foreground">{deleteError}</span>}</>}
                confirmLabel={t('surfaces.projectDetail.delete')}
                cancelLabel={t('surfaces.projectDetail.cancel')}
                closeLabel={t('actions.close')}
                pending={deleteMutation.isPending}
                onCancel={() => setShowDeleteConfirm(false)}
                onConfirm={() => deleteMutation.mutate(false)}
            />

            <ConfirmDialog
                open={showDetachConfirm}
                title={t('surfaces.projectDetail.detachTasks')}
                description={t('surfaces.projectDetail.detachDescription', { project: project.name })}
                confirmLabel={t('surfaces.projectDetail.detachAndDelete')}
                cancelLabel={t('surfaces.projectDetail.cancel')}
                closeLabel={t('actions.close')}
                pending={deleteMutation.isPending}
                onCancel={() => setShowDetachConfirm(false)}
                onConfirm={() => deleteMutation.mutate(true)}
            />
        </PageLayout>
    );
};

export default ProjectDetailPage;

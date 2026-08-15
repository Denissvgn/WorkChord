import { useEffect, useId, useMemo, useState } from 'react';
import { Link } from 'react-router-dom';
import { useInfiniteQuery, useQuery } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import {
    addDays,
    compareAsc,
    differenceInCalendarDays,
    eachMonthOfInterval,
    format,
    parseISO,
    startOfMonth,
} from 'date-fns';
import {
    FolderOpen,
    ListFilter,
    Map as MapIcon,
    RotateCcw,
    X,
} from 'lucide-react';
import clsx from 'clsx';
import { Button } from '../components/common/Button';
import { QueryErrorState, QueryStaleState } from '../components/feedback/QueryState';
import { FormGrid, InlineEmptyState, InlineField, SlideOverDrawer } from '../components/ui';
import { PlanningWorkbenchFrame } from '../components/planning/PlanningWorkbenchFrame';
import { projectStatusBadgeClassName } from '../components/projects/projectStatusStyles';
import { projectService } from '../services/projectService';
import { formatPortfolioOwnerLabel } from '../utils/teamMemberLabels';
import { formatDate } from '../utils/formatDate';
import i18n from '../i18n/i18n';
import { dateFnsLocale } from '../i18n/dateLocale';
import type {
    Initiative,
    Project,
    ProjectHealth,
    ProjectMilestone,
    ProjectMilestoneStatus,
    ProjectStatus,
} from '../types/project';

type RoadmapMarker = {
    milestone: ProjectMilestone;
    date: Date;
};

type RoadmapRow = {
    project: Project;
    milestones: ProjectMilestone[];
    markers: RoadmapMarker[];
    startDate: Date | null;
    endDate: Date | null;
    spanSource: 'project' | 'single-project-date' | 'milestones' | 'none';
    isUnscheduled: boolean;
};

type DateRange = {
    start: Date;
    end: Date;
};

type InitiativeGroupInfo = Pick<
    Initiative,
    'id' | 'name' | 'owner_id' | 'owner' | 'owner_profile_id' | 'owner_profile' | 'health' | 'target_date'
>;

type RoadmapGroup = {
    key: string;
    initiative: InitiativeGroupInfo | null;
    rows: RoadmapRow[];
};

type RoadmapFilterDescriptor = {
    id: 'status' | 'health' | 'owner' | 'initiative' | 'dates';
    label: string;
    remove: () => void;
};

const t = i18n.t.bind(i18n);

const projectStatusLabelKeys: Record<ProjectStatus, string> = {
    proposed: 'surfaces.roadmapPage.proposed',
    planned: 'surfaces.roadmapPage.planned',
    active: 'surfaces.roadmapPage.active',
    paused: 'surfaces.roadmapPage.paused',
    completed: 'surfaces.roadmapPage.completedStatus',
    canceled: 'surfaces.roadmapPage.canceled',
};

const projectHealthLabelKeys: Record<ProjectHealth, string> = {
    unknown: 'surfaces.roadmapPage.unknown',
    on_track: 'surfaces.roadmapPage.onTrack',
    at_risk: 'surfaces.roadmapPage.atRisk',
    off_track: 'surfaces.roadmapPage.offTrack',
};

const milestoneStatusLabelKeys: Record<ProjectMilestoneStatus, string> = {
    planned: 'surfaces.roadmapPage.planned',
    active: 'surfaces.roadmapPage.active',
    completed: 'surfaces.roadmapPage.milestoneComplete',
    canceled: 'surfaces.roadmapPage.milestoneCanceled',
};

const healthClassName = (health: ProjectHealth) => {
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

const barClassName = (health: ProjectHealth) => {
    switch (health) {
        case 'on_track':
            return 'bg-feedback-success';
        case 'at_risk':
            return 'bg-feedback-warning';
        case 'off_track':
            return 'bg-feedback-danger';
        default:
            return 'bg-status-planned';
    }
};

const markerClassName = (status: ProjectMilestoneStatus) => {
    switch (status) {
        case 'active':
            return 'border-status-active bg-status-active';
        case 'completed':
            return 'border-status-resolved bg-status-resolved';
        case 'canceled':
            return 'border-status-closed bg-status-closed';
        default:
            return 'border-status-planned bg-status-planned';
    }
};

const parseDate = (value?: string | null) => {
    if (!value) return null;
    const parsed = parseISO(value);
    return Number.isNaN(parsed.getTime()) ? null : parsed;
};

const formatInputDate = (date: Date) => format(date, 'yyyy-MM-dd');

const minDate = (dates: Date[]) => dates.reduce((earliest, date) => compareAsc(date, earliest) < 0 ? date : earliest);
const maxDate = (dates: Date[]) => dates.reduce((latest, date) => compareAsc(date, latest) > 0 ? date : latest);
const clamp = (value: number, min: number, max: number) => Math.min(max, Math.max(min, value));

const compareProjectRows = (a: RoadmapRow, b: RoadmapRow) => {
    const sortOrderDelta = a.project.sort_order - b.project.sort_order;
    if (sortOrderDelta !== 0) return sortOrderDelta;

    const aTarget = parseDate(a.project.target_date);
    const bTarget = parseDate(b.project.target_date);
    if (aTarget && bTarget) {
        const targetDelta = compareAsc(aTarget, bTarget);
        if (targetDelta !== 0) return targetDelta;
    }
    if (aTarget && !bTarget) return -1;
    if (!aTarget && bTarget) return 1;

    return a.project.name.localeCompare(b.project.name);
};

const compareMilestones = (a: ProjectMilestone, b: ProjectMilestone) => {
    const sortOrderDelta = a.sort_order - b.sort_order;
    if (sortOrderDelta !== 0) return sortOrderDelta;

    const aTarget = parseDate(a.target_date);
    const bTarget = parseDate(b.target_date);
    if (aTarget && bTarget) {
        const targetDelta = compareAsc(aTarget, bTarget);
        if (targetDelta !== 0) return targetDelta;
    }
    if (aTarget && !bTarget) return -1;
    if (!aTarget && bTarget) return 1;

    return a.name.localeCompare(b.name);
};

const compareInitiatives = (a: InitiativeGroupInfo, b: InitiativeGroupInfo) => {
    const aTarget = parseDate(a.target_date);
    const bTarget = parseDate(b.target_date);
    if (aTarget && bTarget) {
        const targetDelta = compareAsc(aTarget, bTarget);
        if (targetDelta !== 0) return targetDelta;
    }
    if (aTarget && !bTarget) return -1;
    if (!aTarget && bTarget) return 1;

    const nameDelta = a.name.localeCompare(b.name);
    if (nameDelta !== 0) return nameDelta;

    return a.id - b.id;
};

const buildRoadmapGroups = (
    rows: RoadmapRow[],
    initiativesById: Map<number, Initiative>,
): RoadmapGroup[] => {
    const groups = new Map<string, RoadmapGroup>();

    rows.forEach(row => {
        const initiativeId = row.project.initiative_id;
        const initiative = initiativeId
            ? initiativesById.get(initiativeId) ?? row.project.initiative ?? {
                id: initiativeId,
                name: `Initiative #${initiativeId}`,
                owner_id: null,
                owner: null,
                owner_profile_id: null,
                owner_profile: null,
                health: 'unknown' as ProjectHealth,
                target_date: null,
            }
            : null;
        const key = initiative ? `initiative-${initiative.id}` : 'unassigned';

        if (!groups.has(key)) {
            groups.set(key, {
                key,
                initiative,
                rows: [],
            });
        }
        groups.get(key)!.rows.push(row);
    });

    const initiativeGroups = Array.from(groups.values())
        .filter(group => group.initiative)
        .sort((a, b) => compareInitiatives(a.initiative!, b.initiative!));
    const unassignedGroup = groups.get('unassigned');

    return unassignedGroup ? [...initiativeGroups, unassignedGroup] : initiativeGroups;
};

const ownerFilterKeyForProject = (project: Project) => {
    if (project.owner_profile_id) {
        return `profile:${project.owner_profile_id}`;
    }
    if (project.owner_id) {
        return `member:${project.owner_id}`;
    }
    return null;
};

const buildRoadmapRows = (projects: Project[], milestonesByProject: Map<number, ProjectMilestone[]>): RoadmapRow[] => {
    return projects.map((project): RoadmapRow => {
        const milestones = [...(milestonesByProject.get(project.id) ?? [])].sort(compareMilestones);
        const markers = milestones
            .map(milestone => {
                const date = parseDate(milestone.target_date);
                return date ? { milestone, date } : null;
            })
            .filter((marker): marker is RoadmapMarker => Boolean(marker))
            .sort((a, b) => (
                compareAsc(a.date, b.date)
                || compareMilestones(a.milestone, b.milestone)
            ));

        const projectStart = parseDate(project.start_date);
        const projectTarget = parseDate(project.target_date);
        const projectDates = [projectStart, projectTarget].filter((date): date is Date => Boolean(date));

        if (projectStart && projectTarget) {
            return {
                project,
                milestones,
                markers,
                startDate: minDate(projectDates),
                endDate: maxDate(projectDates),
                spanSource: 'project',
                isUnscheduled: false,
            };
        }

        if (projectDates.length === 1) {
            return {
                project,
                milestones,
                markers,
                startDate: projectDates[0],
                endDate: projectDates[0],
                spanSource: 'single-project-date',
                isUnscheduled: false,
            };
        }

        if (markers.length > 0) {
            const markerDates = markers.map(marker => marker.date);
            return {
                project,
                milestones,
                markers,
                startDate: minDate(markerDates),
                endDate: maxDate(markerDates),
                spanSource: 'milestones',
                isUnscheduled: false,
            };
        }

        return {
            project,
            milestones,
            markers,
            startDate: null,
            endDate: null,
            spanSource: 'none',
            isUnscheduled: true,
        };
    }).sort(compareProjectRows);
};

const deriveDefaultRange = (rows: RoadmapRow[]): DateRange => {
    const dates = rows.flatMap(row => [
        row.startDate,
        row.endDate,
        ...row.markers.map(marker => marker.date),
    ]).filter((date): date is Date => Boolean(date));

    if (dates.length === 0) {
        const today = new Date();
        return {
            start: addDays(today, -30),
            end: addDays(today, 90),
        };
    }

    return {
        start: addDays(minDate(dates), -14),
        end: addDays(maxDate(dates), 14),
    };
};

const rangeOverlaps = (row: RoadmapRow, range: DateRange) => {
    const rowOverlaps = row.startDate && row.endDate &&
        compareAsc(row.endDate, range.start) >= 0 &&
        compareAsc(row.startDate, range.end) <= 0;

    if (rowOverlaps) return true;

    return row.markers.some(marker =>
        compareAsc(marker.date, range.start) >= 0 &&
        compareAsc(marker.date, range.end) <= 0
    );
};

const MilestoneMarker = ({
    marker,
    position,
}: {
    marker: RoadmapMarker;
    position: number;
}) => {
    const { milestone } = marker;
    const detailsId = useId();
    const [expanded, setExpanded] = useState(false);

    return (
        <div
            className="group absolute top-1/2 z-20 -translate-x-1/2 -translate-y-1/2"
            style={{ left: `${position}%` }}
            onBlur={event => {
                if (!event.currentTarget.contains(event.relatedTarget as Node | null)) {
                    setExpanded(false);
                }
            }}
        >
            <button
                type="button"
                className="roadmap-marker-target relative rounded-sm focus:outline-none focus:ring-2 focus:ring-focus focus:ring-offset-2"
                aria-label={`${milestone.name}, ${t(milestoneStatusLabelKeys[milestone.status])}, ${formatDate(milestone.target_date)}`}
                aria-controls={detailsId}
                aria-expanded={expanded}
                onClick={() => setExpanded(value => !value)}
                onKeyDown={event => {
                    if (event.key === 'Escape') {
                        event.stopPropagation();
                        setExpanded(false);
                    }
                }}
            >
                <span className={clsx('absolute left-1/2 top-1/2 block h-3.5 w-3.5 -translate-x-1/2 -translate-y-1/2 rotate-45 border-2 shadow-sm', markerClassName(milestone.status))} />
            </button>
            <span className="pointer-events-none absolute left-4 top-1/2 hidden max-w-[150px] -translate-y-1/2 truncate rounded bg-surface-card/90 px-1.5 py-0.5 text-wc-micro font-medium text-content-primary shadow-sm ring-1 ring-border md:block">
                {milestone.name}
            </span>
            <div
                id={detailsId}
                className={clsx(
                    'pointer-events-none absolute left-1/2 top-7 w-72 -translate-x-1/2 rounded-md border border-border bg-surface-card p-3 text-left shadow-lg',
                    expanded ? 'block' : 'hidden group-hover:block',
                )}
            >
                <div className="flex items-start justify-between gap-3">
                    <div>
                        <p className="font-semibold text-content-primary">{milestone.name}</p>
                        <p className="mt-1 text-xs text-content-secondary">{formatDate(milestone.target_date)}</p>
                    </div>
                    <span className={clsx('rounded-full border px-2 py-0.5 text-wc-micro font-medium', projectStatusBadgeClassName(milestone.status))}>
                        {t(milestoneStatusLabelKeys[milestone.status])}
                    </span>
                </div>
                {milestone.description && (
                    <p className="mt-2 text-sm text-content-secondary">{milestone.description}</p>
                )}
                <dl className="mt-3 grid grid-cols-2 gap-2 text-xs">
                    <div>
                        <dt className="font-medium text-content-secondary">{t('surfaces.roadmapPage.target')}</dt>
                        <dd className="text-content-primary">{formatDate(milestone.target_date)}</dd>
                    </div>
                    <div>
                        <dt className="font-medium text-content-secondary">{t('surfaces.roadmapPage.completed')}</dt>
                        <dd className="text-content-primary">{formatDate(milestone.completed_at)}</dd>
                    </div>
                </dl>
            </div>
        </div>
    );
};

/* eslint-disable jsx-a11y/no-noninteractive-tabindex -- The horizontal timeline must be keyboard-scrollable. */
const RoadmapTimeline = ({
    groups,
    range,
}: {
    groups: RoadmapGroup[];
    range: DateRange;
}) => {
    const { i18n: activeI18n } = useTranslation();
    const normalizedRange = compareAsc(range.start, range.end) <= 0
        ? range
        : { start: range.end, end: range.start };
    const totalDays = Math.max(1, differenceInCalendarDays(normalizedRange.end, normalizedRange.start) + 1);
    const dayWidth = totalDays > 365 ? 4 : totalDays > 180 ? 7 : totalDays > 90 ? 10 : 16;
    const timelineWidth = Math.max(960, totalDays * dayWidth);
    const months = eachMonthOfInterval({
        start: startOfMonth(normalizedRange.start),
        end: normalizedRange.end,
    });
    const denominator = Math.max(1, totalDays - 1);
    const positionForDate = (date: Date) => clamp(
        (differenceInCalendarDays(date, normalizedRange.start) / denominator) * 100,
        0,
        100,
    );

    return (
        <div
            aria-label={t('surfaces.roadmapPage.timelineScrollLabel')}
            className="roadmap-timeline-scroll overflow-x-auto rounded-lg border border-border bg-surface-card"
            role="region"
            tabIndex={0}
        >
            <div style={{ width: `calc(${timelineWidth}px + var(--roadmap-project-rail-width))` }}>
                <div
                    className="grid border-b border-border bg-surface-muted"
                    style={{ gridTemplateColumns: 'var(--roadmap-project-rail-width) 1fr' }}
                >
                    <div className="roadmap-project-rail is-header border-r border-border px-4 py-3">
                        <p className="text-xs font-semibold uppercase text-content-secondary">{t('surfaces.roadmapPage.project')}</p>
                        <p className="roadmap-timeline-range mt-1 text-sm text-content-secondary">
                            {formatDate(normalizedRange.start)} {t('surfaces.roadmapPage.toText')} {formatDate(normalizedRange.end)}
                        </p>
                    </div>
                    <div className="relative h-16">
                        {months.map(month => (
                            <div
                                key={month.toISOString()}
                                className="absolute top-0 h-full border-l border-border px-2 py-3"
                                style={{ left: `${positionForDate(month)}%` }}
                            >
                                <span className="whitespace-nowrap text-xs font-medium text-content-secondary">
                                    {format(month, 'MMM yyyy', { locale: dateFnsLocale(activeI18n.language) })}
                                </span>
                            </div>
                        ))}
                    </div>
                </div>

                <div className="relative">
                    <div
                        aria-hidden="true"
                        className="pointer-events-none absolute inset-y-0 right-0"
                        style={{ left: 'var(--roadmap-project-rail-width)' }}
                    >
                        {months.map(month => (
                            <div
                                key={`grid-${month.toISOString()}`}
                                className="absolute top-0 h-full border-l border-border-subtle"
                                style={{ left: `${positionForDate(month)}%` }}
                            />
                        ))}
                    </div>
                    <div className="relative">
                        {groups.map(group => {
                        const initiative = group.initiative;
                        const groupHeadingId = `roadmap-timeline-${group.key}`;

                        return (
                            <section key={group.key} aria-labelledby={groupHeadingId}>
                                <div
                                    className="roadmap-timeline-group grid border-b border-border"
                                    style={{ gridTemplateColumns: 'var(--roadmap-project-rail-width) 1fr' }}
                                >
                                    <div className="roadmap-project-rail is-group border-r border-border px-4 py-3">
                                        <div className="flex flex-wrap items-center gap-2">
                                            <h3 id={groupHeadingId} className="font-semibold text-content-primary">
                                                {initiative ? initiative.name : t('surfaces.roadmapPage.unassigned')}
                                            </h3>
                                            {initiative ? (
                                                <span className={clsx('rounded-full border px-2 py-0.5 text-wc-micro font-medium', healthClassName(initiative.health))}>
                                                    {t(projectHealthLabelKeys[initiative.health])}
                                                </span>
                                            ) : (
                                                <span className="rounded-full border border-border bg-surface-card px-2 py-0.5 text-wc-micro font-medium text-content-secondary">
                                                    {t('surfaces.roadmapPage.noInitiative')}
                                                </span>
                                            )}
                                        </div>
                                        <p className="roadmap-timeline-group-meta mt-1 truncate text-xs text-content-secondary">
                                            {initiative
                                                ? `${formatPortfolioOwnerLabel(initiative.owner_profile, initiative.owner, initiative.owner_id, t('surfaces.roadmapPage.unassignedOwner'))} · ${t('surfaces.roadmapPage.target')} ${formatDate(initiative.target_date)}`
                                                : t('surfaces.roadmapPage.projectsWithoutAnInitiativeAssignment')}
                                        </p>
                                    </div>
                                    <div className="roadmap-timeline-group-track relative flex items-center px-4">
                                        <span className="relative rounded-full border border-border bg-surface-card px-2 py-0.5 text-xs font-medium text-content-secondary">
                                            {t('surfaces.roadmapPage.projectCount', { count: group.rows.length })}
                                        </span>
                                    </div>
                                </div>

                                <div className="divide-y divide-border-subtle">
                                    {group.rows.map(row => {
                                        const start = row.startDate ?? normalizedRange.start;
                                        const end = row.endDate ?? start;
                                        const startPosition = positionForDate(start);
                                        const endPosition = positionForDate(end);
                                        const width = Math.max(0, endPosition - startPosition);

                                        return (
                                            <div
                                                key={row.project.id}
                                                className="roadmap-timeline-row grid min-h-[88px] hover:bg-surface-muted"
                                                style={{ gridTemplateColumns: 'var(--roadmap-project-rail-width) 1fr' }}
                                            >
                                                <div className="roadmap-project-rail border-r border-border px-4 py-4">
                                                    <Link
                                                        to={`/projects/${row.project.id}`}
                                                        className="font-medium text-content-primary hover:text-action"
                                                    >
                                                        {row.project.name}
                                                    </Link>
                                                    <p className="sr-only">
                                                        {t('surfaces.roadmapPage.scheduledSpan', {
                                                            start: formatDate(formatInputDate(start)),
                                                            end: formatDate(formatInputDate(end)),
                                                        })}
                                                    </p>
                                                    <div className="mt-2 flex flex-wrap items-center gap-2">
                                                        <span className={clsx('rounded-full border px-2 py-0.5 text-xs font-medium', projectStatusBadgeClassName(row.project.status))}>
                                                            {t(projectStatusLabelKeys[row.project.status])}
                                                        </span>
                                                        <span className={clsx('rounded-full border px-2 py-0.5 text-xs font-medium', healthClassName(row.project.health))}>
                                                            {t(projectHealthLabelKeys[row.project.health])}
                                                        </span>
                                                    </div>
                                                    <p className="roadmap-project-span-source mt-2 text-xs text-content-secondary">
                                                        {row.spanSource === 'project' && t('surfaces.roadmapPage.projectDates')}
                                                        {row.spanSource === 'single-project-date' && t('surfaces.roadmapPage.singleProjectDate')}
                                                        {row.spanSource === 'milestones' && t('surfaces.roadmapPage.milestoneDerivedRange')}
                                                    </p>
                                                </div>
                                                <div className="relative min-h-[88px] px-6">
                                                    <div
                                                        aria-hidden="true"
                                                        className={clsx('absolute top-9 h-3 rounded-full shadow-sm', barClassName(row.project.health))}
                                                        style={{
                                                            left: `${startPosition}%`,
                                                            width: `max(18px, ${width}%)`,
                                                        }}
                                                    />
                                                    {row.markers
                                                        .filter(marker => (
                                                            compareAsc(marker.date, normalizedRange.start) >= 0
                                                            && compareAsc(marker.date, normalizedRange.end) <= 0
                                                        ))
                                                        .map(marker => (
                                                            <MilestoneMarker
                                                                key={marker.milestone.id}
                                                                marker={marker}
                                                                position={positionForDate(marker.date)}
                                                            />
                                                        ))}
                                                </div>
                                            </div>
                                        );
                                    })}
                                </div>
                            </section>
                        );
                        })}
                    </div>
                </div>
            </div>
        </div>
    );
};
/* eslint-enable jsx-a11y/no-noninteractive-tabindex */

const RoadmapGroupHeader = ({ group }: { group: RoadmapGroup }) => {
    const initiative = group.initiative;

    return (
        <div className="flex flex-col gap-3 rounded-lg border border-border bg-surface-card p-4 sm:flex-row sm:items-center sm:justify-between">
            <div>
                <div className="flex flex-wrap items-center gap-2">
                    <h3 className="text-base font-semibold text-content-primary">
                        {initiative ? initiative.name : t('surfaces.roadmapPage.unassigned')}
                    </h3>
                    {initiative ? (
                        <span className={clsx('rounded-full border px-2 py-0.5 text-xs font-medium', healthClassName(initiative.health))}>
                            {t(projectHealthLabelKeys[initiative.health])}
                        </span>
                    ) : (
                        <span className="rounded-full border border-border bg-surface-muted px-2 py-0.5 text-xs font-medium text-content-secondary">
                            {t('surfaces.roadmapPage.noInitiative')}
                        </span>
                    )}
                </div>
                <p className="mt-1 text-sm text-content-secondary">
                    {initiative
                        ? `${formatPortfolioOwnerLabel(initiative.owner_profile, initiative.owner, initiative.owner_id, t('surfaces.roadmapPage.unassignedOwner'))} - ${t('surfaces.roadmapPage.target')} ${formatDate(initiative.target_date)}`
                        : t('surfaces.roadmapPage.projectsWithoutAnInitiativeAssignment')}
                </p>
            </div>
            <span className="w-fit rounded-full bg-surface-subtle px-2.5 py-1 text-xs font-medium text-content-secondary">
                {t('surfaces.roadmapPage.projectCount', { count: group.rows.length })}
            </span>
        </div>
    );
};

const UnscheduledProjects = ({ groups }: { groups: RoadmapGroup[] }) => {
    const projectCount = groups.reduce((total, group) => total + group.rows.length, 0);
    if (projectCount === 0) return null;

    return (
        <section className="rounded-lg border border-border bg-surface-card p-4">
            <div className="flex items-center justify-between gap-3">
                <div>
                    <h2 className="text-lg font-semibold text-content-primary">{t('surfaces.roadmapPage.unscheduled')}</h2>
                    <p className="text-sm text-content-secondary">{t('surfaces.roadmapPage.projectsWithoutProjectDatesOrDatedMilestones')}</p>
                </div>
                <span className="rounded-full bg-surface-subtle px-2.5 py-1 text-xs font-medium text-content-secondary">
                    {projectCount}
                </span>
            </div>
            <div className="mt-4 space-y-5">
                {groups.map(group => (
                    <div key={group.key}>
                        <RoadmapGroupHeader group={group} />
                        <div className="mt-3 grid gap-3 md:grid-cols-2 xl:grid-cols-3">
                            {group.rows.map(row => (
                                <Link
                                    key={row.project.id}
                                    to={`/projects/${row.project.id}`}
                                    className="rounded-md border border-border px-3 py-3 hover:border-action hover:bg-action-muted"
                                >
                                    <div className="flex items-start justify-between gap-3">
                                        <div className="min-w-0">
                                            <p className="truncate font-medium text-content-primary">{row.project.name}</p>
                                            <p className="mt-1 text-xs text-content-secondary">
                                                {t('surfaces.roadmapPage.milestoneCount', { count: row.milestones.length })}, {t('surfaces.roadmapPage.noDatedMarkers')}
                                            </p>
                                        </div>
                                        <span className={clsx('shrink-0 rounded-full border px-2 py-0.5 text-xs font-medium', healthClassName(row.project.health))}>
                                            {t(projectHealthLabelKeys[row.project.health])}
                                        </span>
                                    </div>
                                </Link>
                            ))}
                        </div>
                    </div>
                ))}
            </div>
        </section>
    );
};

const TimelineGroups = ({ groups, range }: { groups: RoadmapGroup[]; range: DateRange }) => {
    if (groups.length === 0) return null;

    return (
        <section className="space-y-4">
            <div className="flex items-center justify-between gap-3">
                <div>
                    <h2 className="text-lg font-semibold text-content-primary">{t('surfaces.roadmapPage.timeline')}</h2>
                    <p className="text-sm text-content-secondary">
                        {t('surfaces.roadmapPage.initiativeGroupsContainProjectBarsAndMilestoneMarkers')}
                    </p>
                </div>
            </div>
            <RoadmapTimeline groups={groups} range={range} />
        </section>
    );
};

const RoadmapPage = () => {
    const { t } = useTranslation();
    const [statusFilter, setStatusFilter] = useState<ProjectStatus | ''>('');
    const [healthFilter, setHealthFilter] = useState<ProjectHealth | ''>('');
    const [ownerFilter, setOwnerFilter] = useState('');
    const [initiativeFilter, setInitiativeFilter] = useState('');
    const [dateFrom, setDateFrom] = useState('');
    const [dateTo, setDateTo] = useState('');
    const [filtersOpen, setFiltersOpen] = useState(false);

    const {
        data: projects = [],
        error: projectsError,
        isError: isProjectsError,
        isLoading: isProjectsLoading,
        refetch: refetchProjects,
    } = useQuery({
        queryKey: ['projects'],
        queryFn: projectService.getAll,
    });

    const {
        data: initiatives = [],
        error: initiativesError,
        isError: isInitiativesError,
        isLoading: isInitiativesLoading,
        refetch: refetchInitiatives,
    } = useQuery({
        queryKey: ['initiatives'],
        queryFn: projectService.getInitiatives,
    });

    const {
        data: milestonePages,
        error: milestonesError,
        fetchNextPage,
        hasNextPage,
        isFetchNextPageError,
        isFetchingNextPage,
        isLoading: isMilestonesLoading,
        refetch: refetchMilestones,
    } = useInfiniteQuery({
        queryKey: ['projectMilestones', 'portfolio'],
        queryFn: ({ pageParam }) => projectService.getRoadmapMilestones(pageParam),
        initialPageParam: null as number | null,
        getNextPageParam: lastPage => lastPage.next_cursor ?? undefined,
        staleTime: 30000,
    });

    useEffect(() => {
        if (hasNextPage && !isFetchingNextPage && !isFetchNextPageError) {
            void fetchNextPage();
        }
    }, [fetchNextPage, hasNextPage, isFetchNextPageError, isFetchingNextPage]);

    const portfolioMilestones = useMemo(
        () => milestonePages?.pages.flatMap(page => page.items) ?? [],
        [milestonePages],
    );
    const milestonesByProject = useMemo(() => {
        const map = new Map<number, ProjectMilestone[]>();
        projects.forEach(project => {
            map.set(project.id, []);
        });
        portfolioMilestones.forEach(milestone => {
            map.get(milestone.project_id)?.push(milestone);
        });
        map.forEach(projectMilestones => {
            projectMilestones.sort(compareMilestones);
        });
        return map;
    }, [portfolioMilestones, projects]);

    const rows = useMemo(() => buildRoadmapRows(projects, milestonesByProject), [projects, milestonesByProject]);
    const initiativesById = useMemo(() => {
        const map = new Map<number, Initiative>();
        initiatives.forEach(initiative => {
            map.set(initiative.id, initiative);
        });
        return map;
    }, [initiatives]);

    const ownerOptions = useMemo(() => {
        const owners = new Map<string, string>();
        let hasUnassigned = false;
        projects.forEach(project => {
            const ownerKey = ownerFilterKeyForProject(project);
            if (ownerKey) {
                owners.set(
                    ownerKey,
                    formatPortfolioOwnerLabel(project.owner_profile, project.owner, project.owner_id),
                );
            }
            else {
                hasUnassigned = true;
            }
        });

        return {
            owners: Array.from(owners, ([id, label]) => ({ id, label }))
                .sort((a, b) => a.label.localeCompare(b.label) || a.id.localeCompare(b.id)),
            hasUnassigned,
        };
    }, [projects]);

    const metadataFilteredRows = useMemo(() => rows.filter(row => {
        if (statusFilter && row.project.status !== statusFilter) return false;
        if (healthFilter && row.project.health !== healthFilter) return false;
        const ownerKey = ownerFilterKeyForProject(row.project);
        if (ownerFilter === 'unassigned' && ownerKey) return false;
        if (ownerFilter && ownerFilter !== 'unassigned' && ownerKey !== ownerFilter) return false;
        if (initiativeFilter === 'unassigned' && row.project.initiative_id) return false;
        if (
            initiativeFilter &&
            initiativeFilter !== 'unassigned' &&
            row.project.initiative_id !== Number(initiativeFilter)
        ) return false;
        return true;
    }), [rows, statusFilter, healthFilter, ownerFilter, initiativeFilter]);

    const defaultRange = useMemo(() => deriveDefaultRange(metadataFilteredRows), [metadataFilteredRows]);
    const effectiveRange = useMemo(() => {
        const start = parseDate(dateFrom) ?? defaultRange.start;
        const end = parseDate(dateTo) ?? defaultRange.end;
        return compareAsc(start, end) <= 0 ? { start, end } : { start: end, end: start };
    }, [dateFrom, dateTo, defaultRange]);
    const activeFilterDescriptors = useMemo<RoadmapFilterDescriptor[]>(() => {
        const descriptors: RoadmapFilterDescriptor[] = [];
        if (statusFilter) {
            descriptors.push({
                id: 'status',
                label: t('surfaces.roadmapPage.statusFilterValue', {
                    value: t(projectStatusLabelKeys[statusFilter]),
                }),
                remove: () => setStatusFilter(''),
            });
        }
        if (healthFilter) {
            descriptors.push({
                id: 'health',
                label: t('surfaces.roadmapPage.healthFilterValue', {
                    value: t(projectHealthLabelKeys[healthFilter]),
                }),
                remove: () => setHealthFilter(''),
            });
        }
        if (ownerFilter) {
            const ownerLabel = ownerFilter === 'unassigned'
                ? t('surfaces.roadmapPage.unassigned')
                : ownerOptions.owners.find(owner => owner.id === ownerFilter)?.label ?? ownerFilter;
            descriptors.push({
                id: 'owner',
                label: t('surfaces.roadmapPage.ownerFilterValue', { value: ownerLabel }),
                remove: () => setOwnerFilter(''),
            });
        }
        if (initiativeFilter) {
            const initiativeLabel = initiativeFilter === 'unassigned'
                ? t('surfaces.roadmapPage.unassigned')
                : initiatives.find(initiative => initiative.id === Number(initiativeFilter))?.name ?? initiativeFilter;
            descriptors.push({
                id: 'initiative',
                label: t('surfaces.roadmapPage.initiativeFilterValue', { value: initiativeLabel }),
                remove: () => setInitiativeFilter(''),
            });
        }
        if (dateFrom || dateTo) {
            descriptors.push({
                id: 'dates',
                label: t('surfaces.roadmapPage.dateFilterValue', {
                    start: formatDate(effectiveRange.start),
                    end: formatDate(effectiveRange.end),
                }),
                remove: () => {
                    setDateFrom('');
                    setDateTo('');
                },
            });
        }
        return descriptors;
    }, [
        dateFrom,
        dateTo,
        effectiveRange,
        healthFilter,
        initiativeFilter,
        initiatives,
        ownerFilter,
        ownerOptions.owners,
        statusFilter,
        t,
    ]);

    const datedRows = useMemo(
        () => metadataFilteredRows.filter(row => !row.isUnscheduled && rangeOverlaps(row, effectiveRange)),
        [metadataFilteredRows, effectiveRange],
    );
    const hasMilestoneDataError = Boolean(milestonesError || isFetchNextPageError);
    const milestoneDataComplete = Boolean(milestonePages)
        && !hasNextPage
        && !isFetchingNextPage
        && !hasMilestoneDataError;
    const unscheduledRows = useMemo(
        () => milestoneDataComplete
            ? metadataFilteredRows.filter(row => row.isUnscheduled)
            : [],
        [metadataFilteredRows, milestoneDataComplete],
    );
    const schedulePendingCount = milestoneDataComplete
        ? 0
        : metadataFilteredRows.filter(row => row.isUnscheduled).length;
    const datedGroups = useMemo(
        () => buildRoadmapGroups(datedRows, initiativesById),
        [datedRows, initiativesById],
    );
    const unscheduledGroups = useMemo(
        () => buildRoadmapGroups(unscheduledRows, initiativesById),
        [unscheduledRows, initiativesById],
    );

    const isLoading = isProjectsLoading || isInitiativesLoading;
    const hasQueryError = isProjectsError || isInitiativesError;
    const totalMilestones = portfolioMilestones.length;
    const visibleRowsCount = metadataFilteredRows.length;
    const milestoneFactValue = milestoneDataComplete
        ? totalMilestones
        : hasMilestoneDataError && totalMilestones === 0
            ? t('surfaces.roadmapPage.unavailable')
            : t('surfaces.roadmapPage.loadedMilestones', { count: totalMilestones });
    const activeFilterCount = activeFilterDescriptors.length;
    const visibleFilterDescriptors = activeFilterDescriptors.slice(0, 3);
    const hiddenFilterCount = Math.max(0, activeFilterCount - visibleFilterDescriptors.length);
    const noRowsMatchFilters = metadataFilteredRows.length === 0
        || (milestoneDataComplete && datedRows.length + unscheduledRows.length === 0);
    const noLoadedRowsMatchDateWindow = !milestoneDataComplete
        && metadataFilteredRows.length > 0
        && Boolean(dateFrom || dateTo)
        && datedRows.length === 0;

    const resetDateRange = () => {
        setDateFrom('');
        setDateTo('');
    };

    const clearRoadmapFilters = () => {
        setStatusFilter('');
        setHealthFilter('');
        setOwnerFilter('');
        setInitiativeFilter('');
        resetDateRange();
    };

    return (
        <>
            <PlanningWorkbenchFrame
                className="roadmap-page"
                variant="wide"
                title={t('surfaces.roadmapPage.roadmap')}
                description={t('surfaces.roadmapPage.portfolioTimelineForProjectsAndMilestoneCommitments')}
                facts={!isLoading && !hasQueryError ? [
                    {
                        id: 'visible-projects',
                        label: t('surfaces.roadmapPage.visibleProjects'),
                        value: visibleRowsCount,
                    },
                    {
                        id: 'milestones',
                        label: t('surfaces.roadmapPage.milestones'),
                        value: milestoneFactValue,
                    },
                    {
                        id: 'timeline-window',
                        label: t('surfaces.roadmapPage.timelineWindow'),
                        value: `${formatDate(effectiveRange.start)} – ${formatDate(effectiveRange.end)}`,
                    },
                ] : []}
                secondaryActions={(
                    <>
                        {!isLoading && !hasQueryError && projects.length > 0 && (
                            <Button
                                type="button"
                                variant="outline"
                                aria-expanded={filtersOpen}
                                aria-haspopup="dialog"
                                aria-label={activeFilterCount > 0
                                    ? t('surfaces.roadmapPage.filtersActive', { count: activeFilterCount })
                                    : t('surfaces.roadmapPage.filters')}
                                onClick={() => setFiltersOpen(true)}
                            >
                                <ListFilter aria-hidden="true" className="h-4 w-4" />
                                <span>{t('surfaces.roadmapPage.filters')}</span>
                                {activeFilterCount > 0 && (
                                    <span aria-hidden="true" className="roadmap-filter-trigger-count">
                                        {activeFilterCount}
                                    </span>
                                )}
                            </Button>
                        )}
                        <Link className="btn" to="/projects">
                            <FolderOpen aria-hidden="true" className="h-4 w-4" />
                            {t('surfaces.roadmapPage.projects')}
                        </Link>
                    </>
                )}
                state={(hasQueryError || isLoading) ? (
                    <>
                        {hasQueryError && (
                            <QueryErrorState
                                error={projectsError ?? initiativesError}
                                onRetry={() => {
                                    void refetchProjects();
                                    void refetchInitiatives();
                                }}
                            />
                        )}
                        {isLoading && !hasQueryError && (
                            <div className="banner muted" role="status">
                                {t('surfaces.roadmapPage.loadingRoadmap')}
                            </div>
                        )}
                    </>
                ) : undefined}
            >
                {!isLoading && !hasQueryError && (
                    <>
                        {(isMilestonesLoading || isFetchingNextPage) && projects.length > 0 && (
                            <div className="banner muted" role="status">
                                {t('surfaces.roadmapPage.loadingMilestoneMarkers')}
                            </div>
                        )}
                        {hasMilestoneDataError && projects.length > 0 && (
                            <QueryStaleState
                                message={totalMilestones > 0
                                    ? t('surfaces.roadmapPage.milestoneMarkersIncomplete', {
                                        count: totalMilestones,
                                    })
                                    : t('surfaces.roadmapPage.milestoneMarkersUnavailable', {
                                        count: schedulePendingCount,
                                    })}
                                onRetry={() => {
                                    if (isFetchNextPageError && hasNextPage) {
                                        void fetchNextPage();
                                        return;
                                    }
                                    void refetchMilestones();
                                }}
                            />
                        )}
                        {activeFilterCount > 0 && projects.length > 0 && (
                            <div
                                aria-label={t('surfaces.roadmapPage.activeFilters')}
                                className="roadmap-active-filters"
                                role="group"
                            >
                                <span className="roadmap-active-filters-label">
                                    {t('surfaces.roadmapPage.activeFilters')}
                                </span>
                                <div className="roadmap-active-filter-list">
                                    {visibleFilterDescriptors.map(filter => (
                                        <button
                                            key={filter.id}
                                            aria-label={t('surfaces.roadmapPage.removeFilter', {
                                                filter: filter.label,
                                            })}
                                            className="roadmap-active-filter-chip"
                                            onClick={filter.remove}
                                            type="button"
                                        >
                                            <span>{filter.label}</span>
                                            <X aria-hidden="true" className="h-3.5 w-3.5" />
                                        </button>
                                    ))}
                                    {hiddenFilterCount > 0 && (
                                        <button
                                            aria-label={t('surfaces.roadmapPage.openRemainingFilters', {
                                                count: hiddenFilterCount,
                                            })}
                                            className="roadmap-active-filter-more"
                                            onClick={() => setFiltersOpen(true)}
                                            type="button"
                                        >
                                            {t('surfaces.roadmapPage.moreFilters', {
                                                count: hiddenFilterCount,
                                            })}
                                        </button>
                                    )}
                                </div>
                            </div>
                        )}
                        {projects.length === 0 && (
                            <InlineEmptyState
                                icon={<FolderOpen className="h-5 w-5" />}
                                title={t('surfaces.roadmapPage.noProjectsYet')}
                                description={t('surfaces.roadmapPage.createProjectsFirstThenAddMilestonesForRoadmapMarkers')}
                                actions={<Link className="btn" to="/projects">{t('surfaces.roadmapPage.openProjects')}</Link>}
                            />
                        )}

                        {projects.length > 0 && noRowsMatchFilters && (
                            <InlineEmptyState
                                icon={<MapIcon className="h-5 w-5" />}
                                title={t('surfaces.roadmapPage.noRoadmapRowsMatchTheFilters')}
                                description={t('surfaces.roadmapPage.adjustStatusHealthOwnerOrDateRangeToBringRowsBackIntoView')}
                                actions={activeFilterCount > 0 ? (
                                    <Button type="button" onClick={clearRoadmapFilters}>
                                        {t('surfaces.roadmapPage.clearFilters')}
                                    </Button>
                                ) : undefined}
                            />
                        )}

                        {projects.length > 0 && noLoadedRowsMatchDateWindow && (
                            <InlineEmptyState
                                icon={<MapIcon className="h-5 w-5" />}
                                title={t('surfaces.roadmapPage.noLoadedRowsMatchDateWindow')}
                                description={t('surfaces.roadmapPage.loadedRowsIncomplete')}
                                actions={(
                                    <Button type="button" onClick={resetDateRange}>
                                        {t('surfaces.roadmapPage.useDerivedRange')}
                                    </Button>
                                )}
                            />
                        )}

                        <TimelineGroups groups={datedGroups} range={effectiveRange} />
                        <UnscheduledProjects groups={unscheduledGroups} />
                    </>
                )}
            </PlanningWorkbenchFrame>

            <SlideOverDrawer
                open={filtersOpen && !isLoading && !hasQueryError && projects.length > 0}
                title={t('surfaces.roadmapPage.filters')}
                subtitle={t('surfaces.roadmapPage.filtersDescription')}
                icon={<ListFilter aria-hidden="true" className="h-4 w-4" />}
                onClose={() => setFiltersOpen(false)}
                footer={(
                    <Button
                        className="w-full"
                        type="button"
                        variant="secondary"
                        onClick={clearRoadmapFilters}
                        disabled={activeFilterCount === 0}
                    >
                        {t('surfaces.roadmapPage.clearFilters')}
                    </Button>
                )}
            >
                <div className="roadmap-filter-drawer-content">
                    <fieldset className="roadmap-filter-section">
                        <legend>{t('surfaces.roadmapPage.projectAttributes')}</legend>
                        <FormGrid className="roadmap-filter-drawer-grid">
                            <InlineField label={t('surfaces.roadmapPage.status')}>
                                <select
                                    value={statusFilter}
                                    onChange={event => setStatusFilter(event.target.value as ProjectStatus | '')}
                                    className="input"
                                >
                                    <option value="">{t('surfaces.roadmapPage.allStatuses')}</option>
                                    {Object.entries(projectStatusLabelKeys).map(([value, labelKey]) => (
                                        <option key={value} value={value}>{t(labelKey)}</option>
                                    ))}
                                </select>
                            </InlineField>
                            <InlineField label={t('surfaces.roadmapPage.health')}>
                                <select
                                    value={healthFilter}
                                    onChange={event => setHealthFilter(event.target.value as ProjectHealth | '')}
                                    className="input"
                                >
                                    <option value="">{t('surfaces.roadmapPage.allHealth')}</option>
                                    {Object.entries(projectHealthLabelKeys).map(([value, labelKey]) => (
                                        <option key={value} value={value}>{t(labelKey)}</option>
                                    ))}
                                </select>
                            </InlineField>
                            <InlineField label={t('surfaces.roadmapPage.owner')}>
                                <select
                                    value={ownerFilter}
                                    onChange={event => setOwnerFilter(event.target.value)}
                                    className="input"
                                >
                                    <option value="">{t('surfaces.roadmapPage.allOwners')}</option>
                                    {ownerOptions.hasUnassigned && <option value="unassigned">{t('surfaces.roadmapPage.unassigned')}</option>}
                                    {ownerOptions.owners.map(owner => (
                                        <option key={owner.id} value={owner.id}>{owner.label}</option>
                                    ))}
                                </select>
                            </InlineField>
                            <InlineField label={t('surfaces.roadmapPage.initiative')}>
                                <select
                                    value={initiativeFilter}
                                    onChange={event => setInitiativeFilter(event.target.value)}
                                    className="input"
                                >
                                    <option value="">{t('surfaces.roadmapPage.allInitiatives')}</option>
                                    <option value="unassigned">{t('surfaces.roadmapPage.unassigned')}</option>
                                    {initiatives.map(initiative => (
                                        <option key={initiative.id} value={initiative.id}>
                                            {initiative.name}
                                        </option>
                                    ))}
                                </select>
                            </InlineField>
                        </FormGrid>
                    </fieldset>

                    <fieldset className="roadmap-filter-section">
                        <legend>{t('surfaces.roadmapPage.dateWindow')}</legend>
                        <FormGrid className="roadmap-filter-drawer-grid">
                            <InlineField label={t('surfaces.roadmapPage.from')}>
                                <input
                                    type="date"
                                    value={dateFrom || formatInputDate(defaultRange.start)}
                                    onChange={event => setDateFrom(event.target.value)}
                                    className="input"
                                />
                            </InlineField>
                            <InlineField label={t('surfaces.roadmapPage.to')}>
                                <input
                                    type="date"
                                    value={dateTo || formatInputDate(defaultRange.end)}
                                    onChange={event => setDateTo(event.target.value)}
                                    className="input"
                                />
                            </InlineField>
                        </FormGrid>
                        <div className="roadmap-filter-date-reset">
                            <p className="field-hint">
                                {t('surfaces.roadmapPage.derivedRange')}: {formatDate(defaultRange.start)} {t('surfaces.roadmapPage.toText')} {formatDate(defaultRange.end)}
                            </p>
                            <Button
                                type="button"
                                variant="ghost"
                                size="sm"
                                onClick={resetDateRange}
                                disabled={!dateFrom && !dateTo}
                            >
                                <RotateCcw aria-hidden="true" className="h-4 w-4" />
                                {t('surfaces.roadmapPage.useDerivedRange')}
                            </Button>
                        </div>
                    </fieldset>
                </div>
            </SlideOverDrawer>
        </>
    );
};

export default RoadmapPage;

import { useId, useMemo, useState } from 'react';
import { Link } from 'react-router-dom';
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
import { Map as MapIcon, Plus } from 'lucide-react';
import clsx from 'clsx';
import { Button } from '../common/Button';
import { LiveWindowStatus } from '../feedback/LiveWindowStatus';
import { QueryStaleState } from '../feedback/QueryState';
import { InlineEmptyState } from '../ui';
import { useLiveWindow } from '../../features/useLiveWindow';
import { dateFnsLocale } from '../../i18n/dateLocale';
import { projectService } from '../../services/projectService';
import { formatDate } from '../../utils/formatDate';
import type {
    Initiative,
    Project,
    ProjectHealth,
    ProjectMilestone,
    ProjectMilestoneStatus,
    ProjectStatus,
} from '../../types/project';
import { AddMilestoneModal } from './AddMilestoneModal';
import { InitiativeGroupHeader } from './InitiativeGroupHeader';
import { groupByInitiative, type InitiativeGroup } from './projectPortfolio';
import { projectHealthBadgeClassName, projectStatusBadgeClassName } from './projectStatusStyles';
import { SetDatesPopover } from './SetDatesPopover';

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

const compareByOrderDateName = (
    a: { sort_order: number; target_date?: string | null; name: string },
    b: { sort_order: number; target_date?: string | null; name: string },
) => {
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

const buildRoadmapRows = (projects: Project[], milestonesByProject: Map<number, ProjectMilestone[]>): RoadmapRow[] => (
    projects.map((project): RoadmapRow => {
        const milestones = [...(milestonesByProject.get(project.id) ?? [])].sort(compareByOrderDateName);
        const markers = milestones
            .map(milestone => {
                const date = parseDate(milestone.target_date);
                return date ? { milestone, date } : null;
            })
            .filter((marker): marker is RoadmapMarker => Boolean(marker))
            .sort((a, b) => compareAsc(a.date, b.date) || compareByOrderDateName(a.milestone, b.milestone));

        const projectStart = parseDate(project.start_date);
        const projectTarget = parseDate(project.target_date);
        const projectDates = [projectStart, projectTarget].filter((date): date is Date => Boolean(date));
        const base = { project, milestones, markers };

        if (projectStart && projectTarget) {
            return { ...base, startDate: minDate(projectDates), endDate: maxDate(projectDates), spanSource: 'project', isUnscheduled: false };
        }
        if (projectDates.length === 1) {
            return { ...base, startDate: projectDates[0], endDate: projectDates[0], spanSource: 'single-project-date', isUnscheduled: false };
        }
        if (markers.length > 0) {
            const markerDates = markers.map(marker => marker.date);
            return { ...base, startDate: minDate(markerDates), endDate: maxDate(markerDates), spanSource: 'milestones', isUnscheduled: false };
        }
        return { ...base, startDate: null, endDate: null, spanSource: 'none', isUnscheduled: true };
    }).sort((a, b) => compareByOrderDateName(a.project, b.project))
);

const deriveDefaultRange = (rows: RoadmapRow[]): DateRange => {
    const dates = rows.flatMap(row => [
        row.startDate,
        row.endDate,
        ...row.markers.map(marker => marker.date),
    ]).filter((date): date is Date => Boolean(date));

    if (dates.length === 0) {
        const today = new Date();
        return { start: addDays(today, -30), end: addDays(today, 90) };
    }
    return { start: addDays(minDate(dates), -14), end: addDays(maxDate(dates), 14) };
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

const MilestoneMarker = ({ marker, position }: { marker: RoadmapMarker; position: number }) => {
    const { t } = useTranslation();
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
                data-page-chrome-control="button"
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

const GRID_COLUMNS = { gridTemplateColumns: 'var(--roadmap-project-rail-width) 1fr' };

/* eslint-disable jsx-a11y/no-noninteractive-tabindex -- The horizontal timeline must be keyboard-scrollable. */
const RoadmapTimeline = ({
    groups,
    range,
    initiativesById,
    onEditInitiative,
    onDeleteInitiative,
    onAddMilestone,
}: {
    groups: InitiativeGroup<RoadmapRow>[];
    range: DateRange;
    initiativesById: Map<number, Initiative>;
    onEditInitiative: (initiativeId: number) => void;
    onDeleteInitiative: (initiativeId: number) => void;
    onAddMilestone: (project: Project) => void;
}) => {
    const { t, i18n } = useTranslation();
    const totalDays = Math.max(1, differenceInCalendarDays(range.end, range.start) + 1);
    const dayWidth = totalDays > 365 ? 4 : totalDays > 180 ? 7 : totalDays > 90 ? 10 : 16;
    const timelineWidth = Math.max(960, totalDays * dayWidth);
    const months = eachMonthOfInterval({ start: startOfMonth(range.start), end: range.end });
    const denominator = Math.max(1, totalDays - 1);
    const positionForDate = (date: Date) => clamp(
        (differenceInCalendarDays(date, range.start) / denominator) * 100,
        0,
        100,
    );
    const today = new Date();
    const todayInRange = compareAsc(today, range.start) >= 0 && compareAsc(today, range.end) <= 0;

    return (
        <div
            aria-label={t('surfaces.roadmapPage.timelineScrollLabel')}
            className="roadmap-timeline-scroll overflow-x-auto rounded-lg border border-border bg-surface-card"
            role="region"
            tabIndex={0}
        >
            <div style={{ width: `calc(${timelineWidth}px + var(--roadmap-project-rail-width))` }}>
                <div className="grid border-b border-border bg-surface-muted" style={GRID_COLUMNS}>
                    <div className="roadmap-project-rail is-header border-r border-border px-4 py-3">
                        <p className="text-xs font-semibold uppercase text-content-secondary">{t('surfaces.roadmapPage.project')}</p>
                        <p className="roadmap-timeline-range mt-1 text-sm text-content-secondary">
                            {formatDate(range.start)} {t('surfaces.roadmapPage.toText')} {formatDate(range.end)}
                        </p>
                    </div>
                    <div className="relative h-16">
                        {todayInRange && (
                            <span className="absolute bottom-1 z-10 -translate-x-1/2 rounded bg-action px-1.5 py-0.5 text-wc-micro font-semibold text-action-foreground"
                                style={{ left: `${positionForDate(today)}%` }}>
                                {t('surfaces.roadmapPage.today')}
                            </span>
                        )}
                        {/* A month that starts before the window has no label; it would sit on top of the next one. */}
                        {months.filter(month => months.length === 1 || compareAsc(month, range.start) >= 0).map(month => (
                            <div
                                key={month.toISOString()}
                                className="absolute top-0 h-full border-l border-border px-2 py-3"
                                style={{ left: `${positionForDate(month)}%` }}
                            >
                                <span className="whitespace-nowrap text-xs font-medium text-content-secondary">
                                    {format(month, 'MMM yyyy', { locale: dateFnsLocale(i18n.language) })}
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
                        {todayInRange && (
                            <div className="absolute top-0 z-10 h-full w-0.5 bg-action" style={{ left: `${positionForDate(today)}%` }} />
                        )}
                    </div>
                    <div className="relative">
                        {groups.map(group => {
                            const initiative = group.initiative;
                            const groupHeadingId = `roadmap-timeline-${group.key}`;
                            const manageable = initiative ? initiativesById.has(initiative.id) : false;

                            return (
                                <section key={group.key} aria-labelledby={groupHeadingId}>
                                    <div className="roadmap-timeline-group grid border-b border-border" style={GRID_COLUMNS}>
                                        <div className="roadmap-project-rail is-group border-r border-border px-4 py-3">
                                            <InitiativeGroupHeader
                                                initiative={initiative}
                                                projectCount={group.items.length}
                                                headingLevel={3}
                                                headingId={groupHeadingId}
                                                onEdit={initiative && manageable ? () => onEditInitiative(initiative.id) : undefined}
                                                onDelete={initiative && manageable ? () => onDeleteInitiative(initiative.id) : undefined}
                                            />
                                        </div>
                                        <div className="roadmap-timeline-group-track relative" />
                                    </div>

                                    <div className="divide-y divide-border-subtle">
                                        {group.items.length === 0 && (
                                            <div className="grid" style={GRID_COLUMNS}>
                                                <p className="roadmap-project-rail border-r border-border px-4 py-3 text-sm text-content-secondary">
                                                    {t('surfaces.projectsPage.noProjectsInInitiative')}
                                                </p>
                                                <div />
                                            </div>
                                        )}
                                        {group.items.map(row => {
                                            const start = row.startDate ?? range.start;
                                            const end = row.endDate ?? start;
                                            const startPosition = positionForDate(start);
                                            const endPosition = positionForDate(end);
                                            const width = Math.max(0, endPosition - startPosition);

                                            return (
                                                <div
                                                    key={row.project.id}
                                                    className="roadmap-timeline-row grid min-h-[88px] hover:bg-surface-muted"
                                                    style={GRID_COLUMNS}
                                                >
                                                    <div className="roadmap-project-rail border-r border-border px-4 py-4">
                                                        <Link
                                                            to={`/projects/${row.project.id}`}
                                                            className="font-medium text-content-primary hover:text-action"
                                                        >
                                                            {row.project.name}
                                                        </Link>
                                                        {!row.isUnscheduled && (
                                                            <p className="sr-only">
                                                                {t('surfaces.roadmapPage.scheduledSpan', {
                                                                    start: formatDate(formatInputDate(start)),
                                                                    end: formatDate(formatInputDate(end)),
                                                                })}
                                                            </p>
                                                        )}
                                                        <div className="mt-2 flex flex-wrap items-center gap-2">
                                                            <span className={clsx('rounded-full border px-2 py-0.5 text-xs font-medium', projectStatusBadgeClassName(row.project.status))}>
                                                                {t(projectStatusLabelKeys[row.project.status])}
                                                            </span>
                                                            <span className={clsx('rounded-full border px-2 py-0.5 text-xs font-medium', projectHealthBadgeClassName(row.project.health))}>
                                                                {t('surfaces.roadmapPage.healthLabel', { health: t(projectHealthLabelKeys[row.project.health]) })}
                                                            </span>
                                                        </div>
                                                        <p className="roadmap-project-span-source mt-2 text-xs text-content-secondary">
                                                            {row.spanSource === 'project' && t('surfaces.roadmapPage.projectDates')}
                                                            {row.spanSource === 'single-project-date' && t('surfaces.roadmapPage.singleProjectDate')}
                                                            {row.spanSource === 'milestones' && t('surfaces.roadmapPage.milestoneDerivedRange')}
                                                        </p>
                                                    </div>
                                                    {row.isUnscheduled ? (
                                                        <div className="roadmap-undated-track">
                                                            <span className="roadmap-undated-note">{t('surfaces.projectsPage.noDatesYet')}</span>
                                                            <SetDatesPopover project={row.project} />
                                                            <Button variant="ghost" size="sm" onClick={() => onAddMilestone(row.project)}>
                                                                <Plus aria-hidden="true" className="h-3.5 w-3.5" />
                                                                {t('surfaces.projectsPage.addMilestone')}
                                                            </Button>
                                                        </div>
                                                    ) : (
                                                        <div className="relative min-h-[88px] px-6">
                                                            <div
                                                                aria-hidden="true"
                                                                className={clsx('absolute top-9 h-3 rounded-full shadow-sm', barClassName(row.project.health))}
                                                                style={{ left: `${startPosition}%`, width: `max(18px, ${width}%)` }}
                                                            />
                                                            {row.markers
                                                                .filter(marker => (
                                                                    compareAsc(marker.date, range.start) >= 0
                                                                    && compareAsc(marker.date, range.end) <= 0
                                                                ))
                                                                .map(marker => (
                                                                    <MilestoneMarker
                                                                        key={marker.milestone.id}
                                                                        marker={marker}
                                                                        position={positionForDate(marker.date)}
                                                                    />
                                                                ))}
                                                        </div>
                                                    )}
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

/**
 * The Roadmap view of Projects: the filtered projects on one date axis, under
 * the same initiative groups as the list. It reads project start and target
 * dates and milestone target dates; a project with neither can be dated here.
 */
export const RoadmapView = ({
    projects,
    initiatives,
    includeEmptyGroups,
    window: timelineWindow,
    onResetWindow,
    onEditInitiative,
    onDeleteInitiative,
}: {
    /** The projects left after the page's search and filters. */
    projects: Project[];
    initiatives: Initiative[];
    includeEmptyGroups: boolean;
    /** The window set by a preset, as `yyyy-MM-dd`; empty values fit the projects. */
    window: { from: string; to: string };
    onResetWindow: () => void;
    onEditInitiative: (initiativeId: number) => void;
    onDeleteInitiative: (initiativeId: number) => void;
}) => {
    const { t } = useTranslation();
    const [milestoneProject, setMilestoneProject] = useState<Project | null>(null);

    // feedback-policy: query loading,error,retry,empty - bars from project dates show at once; markers load in pages with a status line, a stale-state retry and load more.
    const milestoneWindow = useLiveWindow({
        queryKey: ['projectMilestones', 'portfolio'],
        queryFn: ({ pageParam }) => projectService.getRoadmapMilestones(pageParam),
        initialPageParam: null as number | null,
        getNextPageParam: lastPage => lastPage.next_cursor ?? undefined,
        staleTime: 30000,
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
    } = milestoneWindow;

    const portfolioMilestones = useMemo(
        () => milestonePages?.pages.flatMap(page => page.items) ?? [],
        [milestonePages],
    );
    const milestonesByProject = useMemo(() => {
        const map = new Map<number, ProjectMilestone[]>();
        portfolioMilestones.forEach(milestone => {
            const list = map.get(milestone.project_id) ?? [];
            list.push(milestone);
            map.set(milestone.project_id, list);
        });
        return map;
    }, [portfolioMilestones]);
    const initiativesById = useMemo(() => new Map(initiatives.map(initiative => [initiative.id, initiative])), [initiatives]);

    const rows = useMemo(() => buildRoadmapRows(projects, milestonesByProject), [projects, milestonesByProject]);
    const defaultRange = useMemo(() => deriveDefaultRange(rows), [rows]);
    const range = useMemo(() => {
        const start = parseDate(timelineWindow.from) ?? defaultRange.start;
        const end = parseDate(timelineWindow.to) ?? defaultRange.end;
        return compareAsc(start, end) <= 0 ? { start, end } : { start: end, end: start };
    }, [timelineWindow.from, timelineWindow.to, defaultRange]);
    const windowSet = Boolean(timelineWindow.from || timelineWindow.to);

    const visibleRows = useMemo(
        () => rows.filter(row => row.isUnscheduled || rangeOverlaps(row, range)),
        [rows, range],
    );
    const groups = useMemo(
        () => groupByInitiative(visibleRows, row => row.project, initiatives, includeEmptyGroups && !windowSet),
        [visibleRows, initiatives, includeEmptyGroups, windowSet],
    );

    const hasMilestoneDataError = Boolean(milestonesError || isFetchNextPageError);
    const milestoneDataComplete = Boolean(milestonePages)
        && !hasNextPage
        && !milestoneWindow.outsideWindow
        && !isFetchingNextPage
        && !hasMilestoneDataError;
    const totalMilestones = portfolioMilestones.length;
    const undatedCount = rows.filter(row => row.isUnscheduled).length;
    const nothingInWindow = rows.length > 0 && visibleRows.length === 0;

    return (
        <section className="space-y-3" aria-labelledby="roadmap-timeline-title">
            <div className="flex flex-wrap items-baseline justify-between gap-x-4 gap-y-1">
                <h2 id="roadmap-timeline-title" className="text-lg font-semibold text-content-primary">{t('surfaces.roadmapPage.timeline')}</h2>
                <ul aria-label={t('surfaces.roadmapPage.milestoneLegend')} className="flex flex-wrap gap-x-4 gap-y-1 text-xs text-content-secondary">
                    {(['planned', 'active', 'completed', 'canceled'] as const).map(status => (
                        <li key={status} className="flex items-center gap-1.5">
                            <span aria-hidden="true" className={clsx('inline-block h-2.5 w-2.5 rotate-45 border-2', markerClassName(status))} />
                            {t(milestoneStatusLabelKeys[status])}
                        </li>
                    ))}
                    <li className="flex items-center gap-1.5"><span aria-hidden="true" className="inline-block h-3 w-0.5 bg-action" />{t('surfaces.roadmapPage.today')}</li>
                </ul>
            </div>

            <LiveWindowStatus window={milestoneWindow} />
            {hasNextPage && (
                <Button type="button" variant="secondary" disabled={isFetchingNextPage} onClick={() => void fetchNextPage()}>
                    {t('teamwork.loadMore')}
                </Button>
            )}
            {(isMilestonesLoading || isFetchingNextPage) && (
                <div className="banner muted" role="status">
                    {t('surfaces.roadmapPage.loadingMilestoneMarkers')}
                </div>
            )}
            {hasMilestoneDataError && (
                <QueryStaleState
                    message={totalMilestones > 0
                        ? t('surfaces.roadmapPage.milestoneMarkersIncomplete', { count: totalMilestones })
                        : t('surfaces.roadmapPage.milestoneMarkersUnavailable', { count: undatedCount })}
                    onRetry={() => {
                        if (isFetchNextPageError && hasNextPage) {
                            void fetchNextPage();
                            return;
                        }
                        void refetchMilestones();
                    }}
                />
            )}

            {nothingInWindow ? (
                <InlineEmptyState
                    icon={<MapIcon className="h-5 w-5" />}
                    title={milestoneDataComplete
                        ? t('surfaces.projectsPage.noProjectsInWindow')
                        : t('surfaces.roadmapPage.noLoadedRowsMatchDateWindow')}
                    description={milestoneDataComplete ? undefined : t('surfaces.roadmapPage.loadedRowsIncomplete')}
                    actions={(
                        <Button type="button" variant="secondary" onClick={onResetWindow}>
                            {t('surfaces.roadmapPage.presetFit')}
                        </Button>
                    )}
                />
            ) : (
                <RoadmapTimeline
                    groups={groups}
                    range={range}
                    initiativesById={initiativesById}
                    onEditInitiative={onEditInitiative}
                    onDeleteInitiative={onDeleteInitiative}
                    onAddMilestone={setMilestoneProject}
                />
            )}

            {milestoneProject && (
                <AddMilestoneModal project={milestoneProject} onClose={() => setMilestoneProject(null)} />
            )}
        </section>
    );
};

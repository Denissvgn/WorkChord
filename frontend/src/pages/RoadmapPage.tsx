import { useMemo, useState } from 'react';
import { Link } from 'react-router-dom';
import { useQueries, useQuery } from '@tanstack/react-query';
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
    Map as MapIcon,
    RotateCcw,
} from 'lucide-react';
import clsx from 'clsx';
import { Button } from '../components/common/Button';
import { QueryErrorState } from '../components/feedback/QueryState';
import { FormGrid, InlineEmptyState, InlineField, MetricGrid, PageHeader, PageLayout } from '../components/ui';
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

const statusClassName = (status: ProjectStatus | ProjectMilestoneStatus) => {
    switch (status) {
        case 'active':
            return 'border-action bg-action-muted text-action';
        case 'completed':
            return 'border-feedback-success-border bg-feedback-success-muted text-feedback-success-foreground';
        case 'paused':
            return 'border-feedback-warning-border bg-feedback-warning-muted text-feedback-warning-foreground';
        case 'canceled':
            return 'border-feedback-danger-border bg-feedback-danger-muted text-feedback-danger-foreground';
        case 'proposed':
            return 'border-feedback-purple-border bg-feedback-purple-muted text-feedback-purple-foreground';
        default:
            return 'border-border bg-surface-muted text-content-primary';
    }
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
            return 'bg-action';
    }
};

const markerClassName = (status: ProjectMilestoneStatus) => {
    switch (status) {
        case 'active':
            return 'border-action bg-action';
        case 'completed':
            return 'border-feedback-success bg-feedback-success';
        case 'canceled':
            return 'border-feedback-danger bg-feedback-danger';
        default:
            return 'border-border-strong bg-surface-card';
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
            .filter((marker): marker is RoadmapMarker => Boolean(marker));

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

    return (
        <div
            className="group absolute top-1/2 z-20 -translate-x-1/2 -translate-y-1/2"
            style={{ left: `${position}%` }}
        >
            <button
            type="button"
            className="relative h-5 w-5 rounded-sm focus:outline-none focus:ring-2 focus:ring-focus focus:ring-offset-2"
            aria-label={`${milestone.name}, ${t(milestoneStatusLabelKeys[milestone.status])}, ${formatDate(milestone.target_date)}`}
            >
                <span className={clsx('absolute left-1/2 top-1/2 block h-3.5 w-3.5 -translate-x-1/2 -translate-y-1/2 rotate-45 border-2 shadow-sm', markerClassName(milestone.status))} />
            </button>
            <span className="pointer-events-none absolute left-4 top-1/2 hidden max-w-[150px] -translate-y-1/2 truncate rounded bg-surface-card/90 px-1.5 py-0.5 text-[11px] font-medium text-content-primary shadow-sm ring-1 ring-border md:block">
                {milestone.name}
            </span>
            <div className="pointer-events-none absolute left-1/2 top-7 hidden w-72 -translate-x-1/2 rounded-md border border-border bg-surface-card p-3 text-left shadow-lg group-hover:block group-focus-within:block">
                <div className="flex items-start justify-between gap-3">
                    <div>
                        <p className="font-semibold text-content-primary">{milestone.name}</p>
                        <p className="mt-1 text-xs text-content-secondary">{formatDate(milestone.target_date)}</p>
                    </div>
                    <span className={clsx('rounded-full border px-2 py-0.5 text-[11px] font-medium', statusClassName(milestone.status))}>
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

const RoadmapTimeline = ({
    rows,
    range,
}: {
    rows: RoadmapRow[];
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
        <div className="overflow-x-auto rounded-lg border border-border bg-surface-card">
            <div style={{ width: timelineWidth + 280 }}>
                <div className="grid border-b border-border bg-surface-muted" style={{ gridTemplateColumns: '280px 1fr' }}>
                    <div className="border-r border-border px-4 py-3">
                        <p className="text-xs font-semibold uppercase text-content-secondary">{t('surfaces.roadmapPage.project')}</p>
                        <p className="mt-1 text-sm text-content-secondary">
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

                <div className="divide-y divide-border-subtle">
                    {rows.map(row => {
                        const start = row.startDate ?? normalizedRange.start;
                        const end = row.endDate ?? start;
                        const startPosition = positionForDate(start);
                        const endPosition = positionForDate(end);
                        const width = Math.max(0, endPosition - startPosition);

                        return (
                            <div
                                key={row.project.id}
                                className="grid min-h-[88px] hover:bg-surface-muted"
                                style={{ gridTemplateColumns: '280px 1fr' }}
                            >
                                <div className="border-r border-border px-4 py-4">
                                    <Link
                                        to={`/projects/${row.project.id}`}
                                        className="font-medium text-content-primary hover:text-action"
                                    >
                                        {row.project.name}
                                    </Link>
                                    <div className="mt-2 flex flex-wrap items-center gap-2">
                                        <span className={clsx('rounded-full border px-2 py-0.5 text-xs font-medium', statusClassName(row.project.status))}>
                                            {t(projectStatusLabelKeys[row.project.status])}
                                        </span>
                                        <span className={clsx('rounded-full border px-2 py-0.5 text-xs font-medium', healthClassName(row.project.health))}>
                                            {t(projectHealthLabelKeys[row.project.health])}
                                        </span>
                                    </div>
                                    <p className="mt-2 text-xs text-content-secondary">
                                        {row.spanSource === 'project' && t('surfaces.roadmapPage.projectDates')}
                                        {row.spanSource === 'single-project-date' && t('surfaces.roadmapPage.singleProjectDate')}
                                        {row.spanSource === 'milestones' && t('surfaces.roadmapPage.milestoneDerivedRange')}
                                    </p>
                                </div>
                                <div className="relative min-h-[88px] px-6">
                                    {months.map(month => (
                                        <div
                                            key={`${row.project.id}-${month.toISOString()}`}
                                            className="absolute top-0 h-full border-l border-border-subtle"
                                            style={{ left: `${positionForDate(month)}%` }}
                                        />
                                    ))}
                                    <div
                                        className={clsx('absolute top-9 h-3 rounded-full shadow-sm', barClassName(row.project.health))}
                                        style={{
                                            left: `${startPosition}%`,
                                            width: `max(18px, ${width}%)`,
                                        }}
                                    />
                                    {row.markers.map(marker => (
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
            </div>
        </div>
    );
};

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
            {groups.map(group => (
                <div key={group.key} className="space-y-3">
                    <RoadmapGroupHeader group={group} />
                    <RoadmapTimeline rows={group.rows} range={range} />
                </div>
            ))}
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

    const milestoneQueries = useQueries({
        queries: projects.map(project => ({
            queryKey: ['projectMilestones', project.id],
            queryFn: () => projectService.getMilestones(project.id),
            staleTime: 30000,
        })),
    });

    const milestonesByProject = useMemo(() => {
        const map = new Map<number, ProjectMilestone[]>();
        projects.forEach((project, index) => {
            map.set(project.id, milestoneQueries[index]?.data ?? []);
        });
        return map;
    }, [projects, milestoneQueries]);

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

    const datedRows = useMemo(
        () => metadataFilteredRows.filter(row => !row.isUnscheduled && rangeOverlaps(row, effectiveRange)),
        [metadataFilteredRows, effectiveRange],
    );
    const unscheduledRows = useMemo(
        () => metadataFilteredRows.filter(row => row.isUnscheduled),
        [metadataFilteredRows],
    );
    const datedGroups = useMemo(
        () => buildRoadmapGroups(datedRows, initiativesById),
        [datedRows, initiativesById],
    );
    const unscheduledGroups = useMemo(
        () => buildRoadmapGroups(unscheduledRows, initiativesById),
        [unscheduledRows, initiativesById],
    );

    const isMilestonesLoading = milestoneQueries.some(query => query.isLoading);
    const failedMilestoneQueries = milestoneQueries.filter(query => query.isError);
    const isLoading = isProjectsLoading || isMilestonesLoading || isInitiativesLoading;
    const hasQueryError = isProjectsError || isInitiativesError || failedMilestoneQueries.length > 0;
    const totalMilestones = rows.reduce((total, row) => total + row.milestones.length, 0);
    const visibleRowsCount = datedRows.length + unscheduledRows.length;

    const resetDateRange = () => {
        setDateFrom(formatInputDate(defaultRange.start));
        setDateTo(formatInputDate(defaultRange.end));
    };

    return (
        <PageLayout className="roadmap-page">
            <PageHeader
                title={t('surfaces.roadmapPage.roadmap')}
                subtitle={t('surfaces.roadmapPage.portfolioTimelineForProjectsAndMilestoneCommitments')}
                actions={<Link to="/projects"><button className="btn"><FolderOpen className="inline h-4 w-4"/>{t('surfaces.roadmapPage.projects')}</button></Link>}
            />

            {hasQueryError && (
                <QueryErrorState
                    error={projectsError ?? initiativesError ?? failedMilestoneQueries[0]?.error}
                    title={failedMilestoneQueries.length > 0 ? t('surfaces.roadmapPage.milestones') : undefined}
                    onRetry={() => {
                        void refetchProjects();
                        void refetchInitiatives();
                        milestoneQueries.forEach(query => { void query.refetch(); });
                    }}
                />
            )}

            <MetricGrid columns={3}>
                <div className="kpi"><div className="kpi-lbl">{t('surfaces.roadmapPage.visibleProjects')}</div><div className="kpi-val tnum">{visibleRowsCount}</div></div>
                <div className="kpi"><div className="kpi-lbl">{t('surfaces.roadmapPage.milestones')}</div><div className="kpi-val tnum">{totalMilestones}</div></div>
                <div className="kpi"><div className="kpi-lbl">{t('surfaces.roadmapPage.timelineWindow')}</div><div className="kpi-val" style={{fontSize:13}}>{formatDate(effectiveRange.start)} – {formatDate(effectiveRange.end)}</div></div>
            </MetricGrid>

            <div className="card">
                <div className="card-head"><h3>{t('surfaces.roadmapPage.filters')}</h3></div>
                <div className="card-pad">
                    <FormGrid className="roadmap-filter-grid">
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
                        <Button type="button" variant="outline" onClick={resetDateRange} className="roadmap-filter-reset">
                            <RotateCcw className="h-4 w-4" />
                            {t('surfaces.roadmapPage.reset')}
                        </Button>
                    </FormGrid>
                    <p className="field-hint roadmap-filter-hint">
                        {t('surfaces.roadmapPage.derivedRange')}: {formatDate(defaultRange.start)} {t('surfaces.roadmapPage.toText')} {formatDate(defaultRange.end)}
                    </p>
                </div>
            </div>

            {isLoading && (
                <div className="banner muted" style={{justifyContent:'center'}}>{t('surfaces.roadmapPage.loadingRoadmap')}</div>
            )}

            {!isLoading && !hasQueryError && projects.length === 0 && (
                <InlineEmptyState
                    icon={<FolderOpen className="h-5 w-5" />}
                    title={t('surfaces.roadmapPage.noProjectsYet')}
                    description={t('surfaces.roadmapPage.createProjectsFirstThenAddMilestonesForRoadmapMarkers')}
                    actions={<Link to="/projects"><button className="btn">{t('surfaces.roadmapPage.openProjects')}</button></Link>}
                />
            )}

            {!isLoading && !hasQueryError && projects.length > 0 && visibleRowsCount === 0 && (
                <InlineEmptyState
                    icon={<MapIcon className="h-5 w-5" />}
                    title={t('surfaces.roadmapPage.noRoadmapRowsMatchTheFilters')}
                    description={t('surfaces.roadmapPage.adjustStatusHealthOwnerOrDateRangeToBringRowsBackIntoView')}
                />
            )}

            {!isLoading && !hasQueryError && <TimelineGroups groups={datedGroups} range={effectiveRange} />}

            {!isLoading && !hasQueryError && <UnscheduledProjects groups={unscheduledGroups} />}
        </PageLayout>
    );
};

export default RoadmapPage;

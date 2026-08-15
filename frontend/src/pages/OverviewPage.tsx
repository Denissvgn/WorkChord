import { useEffect, useMemo, useRef, useState } from 'react';
import type { ReactNode } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import type { TFunction } from 'i18next';
import { formatDate } from '../utils/formatDate';
import clsx from 'clsx';
import {
    Activity,
    AlertTriangle,
    ArrowRight,
    Bookmark,
    Calendar,
    CheckCircle2,
    ChevronDown,
    Clock,
    FolderOpen,
    Inbox,
    ListTodo,
    RefreshCw,
    Target,
    User,
    Zap,
} from 'lucide-react';
import { STEP_DEFS } from '../features/planningMasters/masters';
import { usePlanningReadiness } from '../features/planningMasters/usePlanningReadiness';
import type { PlanningQueryFeedback } from '../features/planningMasters/usePlanningReadiness';
import type { LucideIcon } from 'lucide-react';
import { iterationService } from '../services/iterationService';
import { projectService } from '../services/projectService';
import { QueryErrorState, QueryLoadingState } from '../components/feedback/QueryState';
import { InlineEmptyState, PageHeader, PageLayout, SectionCard } from '../components/ui';
import { Button } from '../components/common/Button';
import type { ProjectSummary, ProjectTargetDateRisk, ProjectUpdateFreshness } from '../types/project';
import type { Task, TaskStatus } from '../types/task';
import type { Iteration } from '../types/iteration';
import type { PillTone } from '../components/ui/tone';
import { STATUS_TONE, toneVar, toneSoftVar } from '../components/ui/tone';
import { selectWorkNowTasks } from '../utils/selectWorkNowTasks';
import { getApiErrorStatus } from '../utils/apiError';
import {
    overviewTaskDrawerHref,
    overviewTaskReturnFocusId,
} from '../features/overview/overviewTaskThread';
import {
    rankAttentionItems,
    rankAttentionTaskCandidates,
    type AttentionKind,
    type AttentionSeverity,
} from '../features/overview/attentionRanking';

type CapacityException = {
    id: number;
    name: string;
    position: string;
    allocatedDays: number;
    capacityDays: number;
    utilizationPercent: number;
    tone: PillTone;
};

type AttentionItem = {
    id: string;
    kind: AttentionKind;
    severity: AttentionSeverity;
    urgency: number;
    magnitude: number;
    tone: PillTone;
    icon: LucideIcon;
    title: string;
    meta: string;
    to: string;
    actionLabel: string;
};

type OverviewDataSource = {
    id: string;
    label: string;
    enabled: boolean;
    hasData: boolean;
    hasUsableData: boolean;
    dataUpdatedAt: number;
    isLoading: boolean;
    isFetching: boolean;
    isError: boolean;
    error: unknown;
    refetch: () => Promise<unknown>;
};

type DirectQueryFeedback = {
    data: unknown;
    dataUpdatedAt: number;
    error: unknown;
    isLoading: boolean;
    isFetching: boolean;
    isError: boolean;
    refetch: () => Promise<unknown>;
};

type OverviewLocationState = {
    returnFocusId?: string;
};

const MS_PER_DAY = 24 * 60 * 60 * 1000;
const HOURS_PER_DAY = 8;
const CAPACITY_WARNING_PERCENT = 85;
const PACE_WARNING_POINTS = 15;
const ITERATION_DETAILS_ID = 'overview-iteration-details';
const WORK_NOW_TITLE_ID = 'overview-work-now-title';
const doneStatuses = new Set<TaskStatus>(['resolved', 'closed']);
const invalidCachedStatuses = new Set([401, 403, 404]);
const operationalAttentionIds = new Set(['overdue', 'unassigned', 'intake']);
const commitmentAttentionIds = new Set(['project-risk', 'project-update', 'pace']);

const hasUsableCachedData = (
    hasData: boolean,
    isError: boolean,
    error: unknown,
) => (
    hasData
    && !(isError && invalidCachedStatuses.has(getApiErrorStatus(error) ?? 0))
);

const planningDataSource = (
    id: string,
    label: string,
    query: PlanningQueryFeedback,
): OverviewDataSource => ({
    id,
    label,
    enabled: query.enabled,
    hasData: query.hasData,
    hasUsableData: hasUsableCachedData(query.hasData, query.isError, query.error),
    dataUpdatedAt: query.dataUpdatedAt,
    isLoading: query.isLoading,
    isFetching: query.isFetching,
    isError: query.isError,
    error: query.error,
    refetch: query.refetch,
});

const directDataSource = (
    id: string,
    label: string,
    query: DirectQueryFeedback,
    enabled: boolean,
): OverviewDataSource => {
    const hasData = query.data !== undefined;
    return {
        id,
        label,
        enabled,
        hasData,
        hasUsableData: hasUsableCachedData(hasData, query.isError, query.error),
        dataUpdatedAt: query.dataUpdatedAt,
        isLoading: query.isLoading,
        isFetching: query.isFetching,
        isError: query.isError,
        error: query.error,
        refetch: query.refetch,
    };
};

const refetchSucceeded = (result: unknown) => (
    typeof result !== 'object'
    || result === null
    || !('isError' in result)
    || (result as { isError?: unknown }).isError !== true
);

const formatConfirmationTime = (timestamp: number, locale: string) => {
    if (!timestamp) return null;
    return new Intl.DateTimeFormat(locale, {
        hour: 'numeric',
        minute: '2-digit',
    }).format(new Date(timestamp));
};

const parseIsoDate = (value?: string | null) => {
    if (!value) return null;
    const timestamp = Date.parse(`${value}T00:00:00`);
    return Number.isNaN(timestamp) ? null : timestamp;
};

const formatNumber = (value: number, locale: string, digits = 1) => (
    new Intl.NumberFormat(locale, {
        maximumFractionDigits: digits,
    }).format(value)
);

const initialsFor = (name?: string | null) => {
    if (!name) return '?';
    const parts = name.trim().split(/\s+/).slice(0, 2);
    return parts.map(part => part[0]?.toUpperCase() ?? '').join('') || '?';
};

const iterationProgress = (iteration?: Iteration | null) => {
    if (!iteration) return { dayNo: 0, daysLeft: 0, percent: 0 };

    const workingDays = Math.max(1, iteration.working_days || 1);
    const start = parseIsoDate(iteration.start_date);
    const end = parseIsoDate(iteration.end_date);
    const today = parseIsoDate(new Date().toISOString().slice(0, 10));

    if (start === null || end === null || today === null || end < start) {
        return { dayNo: 1, daysLeft: Math.max(0, workingDays - 1), percent: Math.min(100, 100 / workingDays) };
    }

    const totalCalendarDays = Math.max(1, Math.round((end - start) / MS_PER_DAY) + 1);
    const elapsedCalendarDays = Math.min(
        totalCalendarDays,
        Math.max(1, Math.round((today - start) / MS_PER_DAY) + 1),
    );
    const dayNo = Math.min(workingDays, Math.max(1, Math.ceil((elapsedCalendarDays / totalCalendarDays) * workingDays)));

    return {
        dayNo,
        daysLeft: Math.max(0, workingDays - dayNo),
        percent: Math.min(100, (dayNo / workingDays) * 100),
    };
};

const riskTone = (risk?: ProjectTargetDateRisk | null): PillTone => {
    if (risk === 'off_track') return 'red';
    if (risk === 'at_risk') return 'yellow';
    if (risk === 'on_track') return 'green';
    return 'gray';
};

const freshnessTone = (freshness?: ProjectUpdateFreshness | null): PillTone => {
    if (freshness === 'missing') return 'red';
    if (freshness === 'stale') return 'yellow';
    if (freshness === 'fresh') return 'green';
    return 'gray';
};

const paceUrgency = (elapsedPercent: number) => {
    if (elapsedPercent >= 80) return 3;
    if (elapsedPercent >= 50) return 2;
    return 1;
};

const OverviewPage = () => {
    const { t } = useTranslation();
    const location = useLocation();
    const navigate = useNavigate();
    const [retryPending, setRetryPending] = useState(false);
    const [recoveryAnnouncement, setRecoveryAnnouncement] = useState('');
    const [iterationDetailsOpen, setIterationDetailsOpen] = useState(false);
    const pageTitleRef = useRef<HTMLSpanElement>(null);
    const iterationDetailsSummaryRef = useRef<HTMLElement | null>(null);
    const focusIterationDetailsOnOpenRef = useRef(false);
    const {
        selectedIterationId,
        iterations,
        currentIteration: selectedIteration,
        teamMembers,
        allTasks,
        readinessData: planR,
        ready: planReady,
        nextId: planNextId,
        queryStates,
    } = usePlanningReadiness({ autoSelectFirst: true, includeInbox: true });

    const iterationSummaryQuery = useQuery({
        queryKey: ['iterationSummary', selectedIterationId],
        queryFn: () => iterationService.getSummary(selectedIterationId),
        enabled: selectedIterationId > 0,
    });
    const hasUsableIterationSummary = hasUsableCachedData(
        iterationSummaryQuery.data !== undefined,
        iterationSummaryQuery.isError,
        iterationSummaryQuery.error,
    );
    const iterationSummary = hasUsableIterationSummary
        ? iterationSummaryQuery.data
        : undefined;
    const scopedProject = selectedIteration
        ? selectedIteration.project === undefined
            ? iterationSummary?.project ?? null
            : selectedIteration.project
        : iterationSummary?.project ?? null;
    const scopedProjectId = selectedIteration
        ? selectedIteration.project_id === undefined
            ? scopedProject?.id ?? iterationSummary?.project_id ?? null
            : selectedIteration.project_id
        : scopedProject?.id ?? iterationSummary?.project_id ?? null;

    const linkedProjectSummaryQuery = useQuery({
        queryKey: ['projectSummary', scopedProjectId],
        queryFn: () => projectService.getSummary(scopedProjectId as number),
        enabled: Boolean(scopedProjectId),
        staleTime: 30000,
    });
    const hasUsableProjectSummary = hasUsableCachedData(
        linkedProjectSummaryQuery.data !== undefined,
        linkedProjectSummaryQuery.isError,
        linkedProjectSummaryQuery.error,
    );
    const linkedProjectSummary = hasUsableProjectSummary
        ? linkedProjectSummaryQuery.data
        : undefined;

    const iterationsSource = planningDataSource(
        'iterations',
        t('overview.dataStatus.sources.iterations'),
        queryStates.iterations,
    );
    const teamSource = planningDataSource(
        'team',
        t('overview.dataStatus.sources.team'),
        queryStates.team,
    );
    const tasksSource = planningDataSource(
        'tasks',
        t('overview.dataStatus.sources.tasks'),
        queryStates.tasks,
    );
    const ganttSource = planningDataSource(
        'gantt',
        t('overview.dataStatus.sources.gantt'),
        queryStates.gantt,
    );
    const inboxSource = planningDataSource(
        'inbox',
        t('overview.dataStatus.sources.inbox'),
        queryStates.inbox,
    );
    const iterationSummarySource = directDataSource(
        'iteration-summary',
        t('overview.dataStatus.sources.iterationSummary'),
        iterationSummaryQuery,
        selectedIterationId > 0,
    );
    const projectSummarySource = directDataSource(
        'project-summary',
        t('overview.dataStatus.sources.projectSummary'),
        linkedProjectSummaryQuery,
        Boolean(scopedProjectId),
    );
    const dataSources = [
        iterationsSource,
        teamSource,
        tasksSource,
        ganttSource,
        inboxSource,
        iterationSummarySource,
        projectSummarySource,
    ];
    const dataIssues = dataSources.filter(source => source.enabled && source.isError);
    const tasksDataAvailable = tasksSource.hasUsableData;
    const planningDataAvailable = [teamSource, tasksSource, ganttSource, inboxSource]
        .filter(source => source.enabled)
        .every(source => source.hasUsableData);
    const decisionSignalsAvailable = (
        planningDataAvailable
        && (!projectSummarySource.enabled || projectSummarySource.hasUsableData)
    );
    const decisionSignalsLoading = [
        teamSource,
        tasksSource,
        ganttSource,
        inboxSource,
        projectSummarySource,
    ].some(source => (
        source.enabled
        && source.isLoading
        && !source.hasUsableData
    ));
    const deliveryDataAvailable = iterationSummarySource.hasUsableData || tasksDataAvailable;

    const completedTasks = tasksDataAvailable
        ? allTasks.filter(task => doneStatuses.has(task.status)).length
        : null;
    const openTaskList = useMemo(
        () => tasksDataAvailable
            ? allTasks.filter(task => !doneStatuses.has(task.status))
            : [],
        [allTasks, tasksDataAvailable],
    );
    const overdueTaskList = useMemo(
        () => rankAttentionTaskCandidates(
            openTaskList.filter(task => task.is_overdue),
        ),
        [openTaskList],
    );
    const unassignedTaskList = useMemo(
        () => rankAttentionTaskCandidates(
            openTaskList.filter(task => !task.assignee),
        ),
        [openTaskList],
    );
    const totalEffortDays = tasksDataAvailable
        ? allTasks.reduce((sum, task) => sum + (task.effort_days || 0), 0)
        : null;
    const completedEffortDays = tasksDataAvailable
        ? allTasks
            .filter(task => doneStatuses.has(task.status))
            .reduce((sum, task) => sum + (task.effort_days || 0), 0)
        : null;

    const totalTasks = iterationSummarySource.hasUsableData
        ? iterationSummary?.total_tasks ?? null
        : tasksDataAvailable
            ? allTasks.length
            : null;
    const shippedTasks = iterationSummarySource.hasUsableData
        ? iterationSummary?.completed_tasks ?? null
        : completedTasks;
    const progress = selectedIteration ? iterationProgress(selectedIteration) : { dayNo: 0, daysLeft: 0, percent: 0 };
    const completionPercent = totalTasks !== null && shippedTasks !== null
        ? totalTasks > 0
            ? (shippedTasks / totalTasks) * 100
            : 0
        : null;
    const effortCompletionPercent = (
        totalEffortDays !== null
        && completedEffortDays !== null
        && totalEffortDays > 0
    )
        ? (completedEffortDays / totalEffortDays) * 100
        : null;
    const paceGapPoints = effortCompletionPercent === null
        ? 0
        : Math.max(0, Math.round(progress.percent - effortCompletionPercent));
    const capacityExceptions = useMemo<CapacityException[]>(() => {
        if (!planningDataAvailable) return [];
        return teamMembers.flatMap<CapacityException>(member => {
            const capacityDays = member.capacity_hours / HOURS_PER_DAY;
            const allocatedDays = member.planned_hours / HOURS_PER_DAY;
            const utilizationPercent = capacityDays > 0
                ? (allocatedDays / capacityDays) * 100
                : allocatedDays > 0
                    ? 100
                    : 0;
            if (
                allocatedDays <= 0
                || (allocatedDays <= capacityDays && utilizationPercent < CAPACITY_WARNING_PERCENT)
            ) {
                return [];
            }
            return [{
                id: member.id,
                name: member.name,
                position: member.position,
                allocatedDays,
                capacityDays,
                utilizationPercent,
                tone: allocatedDays > capacityDays ? 'red' : 'yellow',
            }];
        }).sort((left, right) => (
            Number(right.tone === 'red') - Number(left.tone === 'red')
            || right.utilizationPercent - left.utilizationPercent
            || left.id - right.id
        ));
    }, [planningDataAvailable, teamMembers]);

    const attentionItems = useMemo<AttentionItem[]>(() => {
        const items: AttentionItem[] = [];
        if (tasksDataAvailable && overdueTaskList.length > 0) {
            items.push({
                id: 'overdue',
                kind: 'overdue',
                severity: 'critical',
                urgency: 4,
                magnitude: overdueTaskList.length,
                tone: 'red',
                icon: Clock,
                title: t('overview.attention.overdueTitle', { count: overdueTaskList.length }),
                meta: t('overview.attention.overdueMeta'),
                to: overviewTaskDrawerHref(overdueTaskList[0].id, 'attention'),
                actionLabel: t('overview.focus.reviewTasks'),
            });
        }
        if (
            projectSummarySource.hasUsableData
            && (linkedProjectSummary?.target_date_risk === 'at_risk'
                || linkedProjectSummary?.target_date_risk === 'off_track')
        ) {
            items.push({
                id: 'project-risk',
                kind: 'project-risk',
                severity: linkedProjectSummary.target_date_risk === 'off_track'
                    ? 'critical'
                    : 'warning',
                urgency: linkedProjectSummary.target_date_risk === 'off_track' ? 4 : 3,
                magnitude: 1,
                tone: riskTone(linkedProjectSummary.target_date_risk),
                icon: AlertTriangle,
                title: t('overview.attention.projectRiskTitle'),
                meta: linkedProjectSummary.target_date_risk_reason || t(`overview.riskLabels.${linkedProjectSummary.target_date_risk}`),
                to: scopedProjectId ? `/projects/${scopedProjectId}` : '/projects',
                actionLabel: t('overview.focus.openProject'),
            });
        }
        if (tasksDataAvailable && unassignedTaskList.length > 0) {
            items.push({
                id: 'unassigned',
                kind: 'unassigned',
                severity: 'advisory',
                urgency: unassignedTaskList.some(task => task.status === 'active') ? 2 : 1,
                magnitude: unassignedTaskList.length,
                tone: 'gray',
                icon: User,
                title: t('overview.attention.unassignedTitle', { count: unassignedTaskList.length }),
                meta: unassignedTaskList[0]?.title ?? t('common.unassigned'),
                to: overviewTaskDrawerHref(unassignedTaskList[0].id, 'attention'),
                actionLabel: t('overview.focus.reviewTasks'),
            });
        }
        if (inboxSource.hasUsableData && planR.inboxCount > 0) {
            items.push({
                id: 'intake',
                kind: 'intake',
                severity: 'warning',
                urgency: 1,
                magnitude: planR.inboxCount,
                tone: 'yellow',
                icon: Inbox,
                title: t('overview.attention.intakeTitle', { count: planR.inboxCount }),
                meta: t('overview.attention.intakeMeta'),
                to: '/triage',
                actionLabel: t('overview.focus.reviewIntake'),
            });
        }
        if (
            projectSummarySource.hasUsableData
            && linkedProjectSummary?.is_update_stale
            && (
                linkedProjectSummary.update_freshness === 'missing'
                || linkedProjectSummary.update_freshness === 'stale'
            )
        ) {
            items.push({
                id: 'project-update',
                kind: 'project-update',
                severity: linkedProjectSummary.update_freshness === 'missing'
                    ? 'critical'
                    : 'warning',
                urgency: linkedProjectSummary.update_freshness === 'missing' ? 2 : 1,
                magnitude: 1,
                tone: freshnessTone(linkedProjectSummary.update_freshness),
                icon: Bookmark,
                title: t('overview.attention.projectUpdateTitle'),
                meta: updateFreshnessText(linkedProjectSummary, t),
                to: scopedProjectId ? `/projects/${scopedProjectId}` : '/projects',
                actionLabel: t('overview.focus.openProject'),
            });
        }
        if (
            tasksDataAvailable
            && effortCompletionPercent !== null
            && paceGapPoints >= PACE_WARNING_POINTS
        ) {
            items.push({
                id: 'pace',
                kind: 'pace',
                severity: paceGapPoints >= 30 ? 'critical' : 'warning',
                urgency: paceUrgency(progress.percent),
                magnitude: paceGapPoints,
                tone: paceGapPoints >= 30 ? 'red' : 'yellow',
                icon: Activity,
                title: t('overview.attention.paceBehindTitle', { count: paceGapPoints }),
                meta: t('overview.attention.paceBehindMeta', {
                    completed: Math.round(effortCompletionPercent),
                    elapsed: Math.round(progress.percent),
                }),
                to: '/gantt',
                actionLabel: t('overview.focus.reviewSchedule'),
            });
        }
        return rankAttentionItems(items);
    }, [
        effortCompletionPercent,
        inboxSource.hasUsableData,
        linkedProjectSummary,
        overdueTaskList,
        paceGapPoints,
        planR.inboxCount,
        progress.percent,
        projectSummarySource.hasUsableData,
        scopedProjectId,
        t,
        tasksDataAvailable,
        unassignedTaskList,
    ]);
    const remainingAttentionItems = attentionItems.slice(1);
    const otherExceptionItems = remainingAttentionItems.filter(item => (
        operationalAttentionIds.has(item.id)
    ));
    const commitmentHealthItems = remainingAttentionItems.filter(item => (
        commitmentAttentionIds.has(item.id)
    ));
    const hasOtherExceptions = otherExceptionItems.length > 0 || capacityExceptions.length > 0;
    const hasCommitmentHealth = commitmentHealthItems.length > 0;
    const hasIterationDetails = hasOtherExceptions || hasCommitmentHealth;
    const remainingExceptionCount = (
        remainingAttentionItems.length
        + capacityExceptions.length
    );
    const needsPlanning = planningDataAvailable && planReady.pct < 100;
    const hasTrustedFocus = attentionItems.length > 0 || needsPlanning || decisionSignalsAvailable;
    const showFocusPanel = hasTrustedFocus || decisionSignalsLoading;
    const showDeliverySnapshot = hasTrustedFocus || deliveryDataAvailable || decisionSignalsLoading;

    const description = selectedIteration
        ? scopedProject
            ? t('overview.scopedDescription', { project: scopedProject.name })
            : t('overview.independentDescription')
        : t('overview.description');
    const isResolvingIteration = (
        iterationsSource.hasUsableData
        && iterations.length > 0
        && selectedIteration === null
    );
    const isOverviewLoading = (
        (!iterationsSource.hasUsableData && iterationsSource.isLoading)
        || isResolvingIteration
    );
    const hasBlockingIterationError = (
        iterationsSource.isError
        && !iterationsSource.hasUsableData
    );
    const showOverviewContent = (
        !isOverviewLoading
        && !hasBlockingIterationError
        && selectedIteration !== null
    );
    const returnFocusId = (
        location.state as OverviewLocationState | null
    )?.returnFocusId;

    useEffect(() => {
        if (!iterationDetailsOpen || !focusIterationDetailsOnOpenRef.current) return;
        focusIterationDetailsOnOpenRef.current = false;
        const summary = iterationDetailsSummaryRef.current;
        summary?.scrollIntoView?.({ block: 'nearest', behavior: 'auto' });
        summary?.focus({ preventScroll: true });
    }, [iterationDetailsOpen]);

    useEffect(() => {
        if (hasIterationDetails || !iterationDetailsOpen) return;
        setIterationDetailsOpen(false);
    }, [hasIterationDetails, iterationDetailsOpen]);

    const revealIterationDetails = () => {
        if (iterationDetailsOpen) {
            const summary = iterationDetailsSummaryRef.current;
            summary?.scrollIntoView?.({ block: 'nearest', behavior: 'auto' });
            summary?.focus({ preventScroll: true });
            return;
        }
        focusIterationDetailsOnOpenRef.current = true;
        setIterationDetailsOpen(true);
    };

    useEffect(() => {
        if (!returnFocusId || isOverviewLoading || !showOverviewContent) return;

        const focusTarget = document.getElementById(returnFocusId)
            ?? pageTitleRef.current;
        focusTarget?.focus();
        navigate(
            {
                pathname: location.pathname,
                search: location.search,
                hash: location.hash,
            },
            { replace: true, state: null },
        );
    }, [
        allTasks.length,
        isOverviewLoading,
        location.hash,
        location.pathname,
        location.search,
        navigate,
        returnFocusId,
        showOverviewContent,
    ]);

    const retryDataIssues = async () => {
        if (retryPending) return;
        const failedSources = dataIssues.filter(source => !source.isFetching);
        if (failedSources.length === 0) return;
        setRecoveryAnnouncement('');
        setRetryPending(true);
        let recovered = false;
        try {
            const results = await Promise.allSettled(
                failedSources.map(source => source.refetch()),
            );
            recovered = results.every(result => (
                result.status === 'fulfilled'
                && refetchSucceeded(result.value)
            ));
        } finally {
            setRetryPending(false);
            if (recovered) {
                setRecoveryAnnouncement(t('overview.dataStatus.updated'));
                pageTitleRef.current?.focus();
            }
        }
    };
    const retryPlanningPeriods = async () => {
        if (iterationsSource.isFetching) return;
        setRecoveryAnnouncement('');
        try {
            const result = await iterationsSource.refetch();
            if (refetchSucceeded(result)) {
                setRecoveryAnnouncement(t('overview.dataStatus.updated'));
                pageTitleRef.current?.focus();
            }
        } catch {
            // Query feedback remains in place and owns the next recovery attempt.
        }
    };

    return (
        <PageLayout>
            <PageHeader
                title={(
                    <span
                        ref={pageTitleRef}
                        className="overview-page-title-focus"
                        tabIndex={-1}
                    >
                        {t('overview.title')}
                    </span>
                )}
                subtitle={description}
                meta={selectedIteration && (
                    <>
                        {scopedProject ? (
                            <Link to={`/projects/${scopedProject.id}`} className="overview-project-link">
                                <FolderOpen aria-hidden="true" className="h-3.5 w-3.5" />
                                <span>{scopedProject.name}</span>
                            </Link>
                        ) : (
                            <span>{t('overview.independentIteration')}</span>
                        )}
                        <span><Calendar aria-hidden="true" className="inline h-3.5 w-3.5 mr-1"/>{formatDate(selectedIteration.start_date)} – {formatDate(selectedIteration.end_date)}</span>
                        <span><Zap aria-hidden="true" className="inline h-3.5 w-3.5 mr-1"/>{iterationPhase(progress.dayNo, selectedIteration.working_days, t)}</span>
                        <span><Clock aria-hidden="true" className="inline h-3.5 w-3.5 mr-1"/>{t('overview.daysLeft', { count: progress.daysLeft })}</span>
                    </>
                )}
            />
            {recoveryAnnouncement && (
                <p className="sr-only" role="status" aria-atomic="true">
                    {recoveryAnnouncement}
                </p>
            )}

            {isOverviewLoading && (
                <QueryLoadingState
                    className="overview-state-loading"
                    message={t('overview.dataStatus.loadingOverview')}
                />
            )}
            {hasBlockingIterationError && (
                <div className="overview-blocking-state">
                    <QueryErrorState
                        error={iterationsSource.error}
                        isRetrying={iterationsSource.isFetching}
                        title={t('overview.dataStatus.planningPeriodsUnavailableTitle')}
                        message={t('overview.dataStatus.planningPeriodsUnavailableBody')}
                        onRetry={() => { void retryPlanningPeriods(); }}
                    />
                    <Link to="/settings?tab=about" className="btn secondary sm">
                        {t('overview.dataStatus.checkSystemStatus')}
                        <ArrowRight aria-hidden="true" className="h-3.5 w-3.5" />
                    </Link>
                </div>
            )}

            {!isOverviewLoading
                && !hasBlockingIterationError
                && iterationsSource.hasUsableData
                && iterations.length === 0
                && selectedIteration === null
                && (
                <section className="empty overview-empty" aria-labelledby="overview-empty-title">
                    <h2 id="overview-empty-title">{t('overview.noIterationTitle')}</h2>
                    <p>{t('overview.noIterationBody')}</p>
                    <div className="empty-actions">
                        <Link className="btn primary" to="/plan">
                            <Calendar aria-hidden="true" className="h-4 w-4" />
                            {t('overview.setUpPlanningPeriod')}
                        </Link>
                    </div>
                </section>
                )}

            {showOverviewContent && (
                <>
                    {dataIssues.length > 0 && (
                        <OverviewDataStatus
                            issues={dataIssues}
                            retrying={
                                retryPending
                                || dataIssues.some(source => source.isFetching)
                            }
                            onRetry={() => { void retryDataIssues(); }}
                        />
                    )}

                    <div className="wc-panel-stack">
                        <div
                            className={clsx(
                                'overview-thread-flow',
                                showFocusPanel && 'has-thread has-focus-panel',
                            )}
                        >
                            {showFocusPanel && (
                                <div className="overview-focus-frame" aria-hidden="true" />
                            )}
                            {showFocusPanel && (
                                <div className="overview-thread-stop is-focus">
                                    {hasTrustedFocus ? (
                                        <OverviewFocusPanel
                                            attentionItems={attentionItems}
                                            planReady={planReady}
                                            planNextId={planNextId}
                                            remainingExceptionCount={remainingExceptionCount}
                                            iterationDetailsOpen={iterationDetailsOpen}
                                            onRevealIterationDetails={revealIterationDetails}
                                        />
                                    ) : (
                                        <QueryLoadingState
                                            className="overview-state-loading"
                                            message={t('overview.dataStatus.loadingSignals')}
                                        />
                                    )}
                                </div>
                            )}
                            <div className="overview-thread-stop is-work">
                                <WorkNowPreview
                                    tasks={allTasks}
                                    isProjectScoped={Boolean(scopedProject)}
                                    dataAvailable={tasksDataAvailable}
                                    dataLoading={tasksSource.isLoading && !tasksSource.hasUsableData}
                                />
                            </div>
                            {showDeliverySnapshot && (
                                <OverviewDeliverySnapshot
                                    planReady={planReady}
                                    completionPercent={completionPercent}
                                    shippedTasks={shippedTasks}
                                    totalTasks={totalTasks}
                                    planningDataAvailable={planningDataAvailable}
                                    deliveryDataAvailable={deliveryDataAvailable}
                                    progress={progress}
                                    workingDays={selectedIteration.working_days}
                                />
                            )}
                        </div>

                        {hasIterationDetails && (
                            <details
                                id={ITERATION_DETAILS_ID}
                                className="overview-details"
                                open={iterationDetailsOpen}
                                onToggle={event => {
                                    setIterationDetailsOpen(event.currentTarget.open);
                                }}
                            >
                                <summary ref={iterationDetailsSummaryRef} tabIndex={0}>
                                    <span>
                                        <strong>{t('overview.focus.detailsSummary')}</strong>
                                        <small>{t('overview.focus.detailsHint')}</small>
                                    </span>
                                    <ChevronDown
                                        aria-hidden="true"
                                        className="overview-details-toggle h-4 w-4"
                                    />
                                </summary>
                                <div
                                    className={clsx(
                                        'overview-details-grid',
                                        hasOtherExceptions !== hasCommitmentHealth && 'is-single',
                                    )}
                                >
                                    {hasOtherExceptions && (
                                        <OtherExceptionsCluster
                                            items={otherExceptionItems}
                                            capacityExceptions={capacityExceptions}
                                        />
                                    )}
                                    {hasCommitmentHealth && (
                                        <CommitmentHealthCluster items={commitmentHealthItems} />
                                    )}
                                </div>
                            </details>
                        )}
                    </div>
                </>
            )}
        </PageLayout>
    );
};

const OverviewDataStatus = ({
    issues,
    retrying,
    onRetry,
}: {
    issues: OverviewDataSource[];
    retrying: boolean;
    onRetry: () => void;
}) => {
    const { t, i18n } = useTranslation();
    const hasUnavailable = issues.some(source => !source.hasUsableData);
    const hasStale = issues.some(source => source.hasUsableData);
    const bodyKey = hasUnavailable && hasStale
        ? 'overview.dataStatus.partialBody'
        : hasUnavailable
            ? 'overview.dataStatus.unavailableBody'
            : 'overview.dataStatus.staleBody';
    const titleKey = hasUnavailable && hasStale
        ? 'overview.dataStatus.partialTitle'
        : hasUnavailable
            ? 'overview.dataStatus.unavailableTitle'
            : 'overview.dataStatus.staleTitle';

    return (
        <section
            className={clsx('overview-data-status', hasUnavailable && 'has-unavailable')}
            role={hasUnavailable ? 'alert' : 'status'}
            aria-live={hasUnavailable ? 'assertive' : 'polite'}
            aria-busy={retrying || undefined}
        >
            <AlertTriangle aria-hidden="true" className="overview-data-status-icon h-5 w-5" />
            <div className="overview-data-status-content">
                <h2>{t(titleKey)}</h2>
                <p>{t(bodyKey)}</p>
                <ul aria-label={t('overview.dataStatus.affectedSources')}>
                    {issues.map(source => {
                        const confirmedTime = source.hasUsableData
                            ? formatConfirmationTime(
                                source.dataUpdatedAt,
                                i18n.resolvedLanguage ?? i18n.language,
                            )
                            : null;
                        return (
                            <li key={source.id}>
                                <span>{source.label}</span>
                                <strong>
                                    {source.hasUsableData
                                        ? confirmedTime
                                            ? t('overview.dataStatus.lastConfirmedAt', {
                                                time: confirmedTime,
                                            })
                                            : t('overview.dataStatus.lastConfirmed')
                                        : t('overview.dataStatus.unavailable')}
                                </strong>
                            </li>
                        );
                    })}
                </ul>
            </div>
            <div className="overview-data-status-actions">
                <Button
                    type="button"
                    variant="secondary"
                    size="sm"
                    isLoading={retrying}
                    aria-label={retrying
                        ? t('overview.dataStatus.retrying')
                        : undefined}
                    onClick={onRetry}
                >
                    {!retrying && <RefreshCw aria-hidden="true" className="h-3.5 w-3.5" />}
                    {t('overview.dataStatus.retryAffected')}
                </Button>
                <Link to="/settings?tab=about" className="btn ghost sm">
                    {t('overview.dataStatus.checkSystemStatus')}
                </Link>
            </div>
        </section>
    );
};

const OverviewUnavailableState = ({ loading = false }: { loading?: boolean }) => {
    const { t } = useTranslation();
    return (
        <div
            className={clsx('overview-section-unavailable', loading && 'is-loading')}
            role="status"
            aria-busy={loading || undefined}
        >
            {loading ? (
                <RefreshCw aria-hidden="true" className="h-4 w-4 animate-spin" />
            ) : (
                <AlertTriangle aria-hidden="true" className="h-4 w-4" />
            )}
            <span>
                {loading
                    ? t('overview.dataStatus.sectionLoading')
                    : t('overview.dataStatus.sectionUnavailable')}
            </span>
        </div>
    );
};

interface OverviewFocusPanelProps {
    attentionItems: AttentionItem[];
    planReady: { done: number; total: number; pct: number };
    planNextId: string;
    remainingExceptionCount: number;
    iterationDetailsOpen: boolean;
    onRevealIterationDetails: () => void;
}

const OverviewFocusPanel = ({
    attentionItems,
    planReady,
    planNextId,
    remainingExceptionCount,
    iterationDetailsOpen,
    onRevealIterationDetails,
}: OverviewFocusPanelProps) => {
    const { t } = useTranslation();
    const topAttention = attentionItems[0];
    const needsPlanning = planReady.pct < 100;
    const nextDef = STEP_DEFS.find(step => step.id === planNextId);
    const tone: PillTone = topAttention?.tone
        ?? (needsPlanning ? 'indigo' : 'green');
    const FocusIcon = topAttention?.icon
        ?? (needsPlanning ? Target : CheckCircle2);
    const title = topAttention?.title ?? (
        needsPlanning
            ? t('overview.focus.planIncompleteTitle')
            : t('overview.focus.planReadyTitle')
    );
    const meta = topAttention?.meta ?? (
        needsPlanning
            ? t('overview.focus.planIncompleteMeta', {
                done: planReady.done,
                total: planReady.total,
                step: nextDef ? t(`plan.steps.${nextDef.id}.title`) : t('nav.planning'),
            })
            : t('overview.focus.planReadyMeta')
    );
    const actionLabel = topAttention?.actionLabel ?? (
        needsPlanning
            ? t('overview.focus.continuePlanning')
            : t('overview.focus.reviewPlan')
    );
    const actionTo = topAttention?.to
        ?? '/plan/master';

    return (
        <section className="overview-focus" aria-labelledby="overview-focus-title">
            <div className="overview-focus-main">
                <div className="overview-focus-heading">
                    <span className="overview-focus-icon" style={pillBoxStyle(tone)}>
                        <FocusIcon aria-hidden="true" className="h-5 w-5" />
                    </span>
                    <div>
                        <h2 id="overview-focus-title">{title}</h2>
                        <p>{meta}</p>
                    </div>
                </div>

                <div className="overview-focus-action">
                    <Link to={actionTo} className="btn primary">
                        {actionLabel}
                        <ArrowRight aria-hidden="true" className="h-4 w-4" />
                    </Link>
                    {remainingExceptionCount > 0 && (
                        <Button
                            type="button"
                            variant="ghost"
                            size="sm"
                            className="overview-focus-more-exceptions"
                            aria-controls={ITERATION_DETAILS_ID}
                            aria-expanded={iterationDetailsOpen}
                            onClick={onRevealIterationDetails}
                        >
                            {t('overview.focus.reviewRemainingExceptions', {
                                count: remainingExceptionCount,
                            })}
                            <ChevronDown aria-hidden="true" className="h-3.5 w-3.5" />
                        </Button>
                    )}
                </div>
            </div>
        </section>
    );
};

interface OverviewDeliverySnapshotProps {
    planReady: { done: number; total: number; pct: number };
    completionPercent: number | null;
    shippedTasks: number | null;
    totalTasks: number | null;
    planningDataAvailable: boolean;
    deliveryDataAvailable: boolean;
    progress: { dayNo: number; daysLeft: number; percent: number };
    workingDays: number;
}

const OverviewDeliverySnapshot = ({
    planReady,
    completionPercent,
    shippedTasks,
    totalTasks,
    planningDataAvailable,
    deliveryDataAvailable,
    progress,
    workingDays,
}: OverviewDeliverySnapshotProps) => {
    const { t } = useTranslation();
    const completion = completionPercent === null
        ? null
        : Math.max(0, Math.min(100, Math.round(completionPercent)));
    const completionValueText = (
        completion !== null
        && shippedTasks !== null
        && totalTasks !== null
    )
        ? t('overview.focus.deliveryProgressValue', {
            percent: completion,
            completed: shippedTasks,
            total: totalTasks,
            count: totalTasks,
        })
        : undefined;

    return (
        <div className="overview-focus-progress">
            <div className="overview-focus-progress-head">
                <span>{t('overview.focus.deliveryProgress')}</span>
                <strong className="tnum">
                    {deliveryDataAvailable && completion !== null
                        ? `${completion}%`
                        : t('overview.dataStatus.valueUnavailable')}
                </strong>
            </div>
            {deliveryDataAvailable && completion !== null ? (
                <div
                    className="overview-focus-track"
                    role="progressbar"
                    aria-label={t('overview.focus.deliveryProgress')}
                    aria-valuemin={0}
                    aria-valuemax={100}
                    aria-valuenow={completion}
                    aria-valuetext={completionValueText}
                >
                    <span style={{width: `${completion}%`}} />
                </div>
            ) : (
                <div
                    className="overview-focus-track is-unavailable"
                    aria-label={t('overview.dataStatus.deliveryProgressUnavailable')}
                    role="img"
                />
            )}
            <dl className="overview-focus-facts">
                <div>
                    <dt>{t('overview.focus.planReadiness')}</dt>
                    <dd>
                        {planningDataAvailable
                            ? t('plan.hub.stepsComplete', {
                                done: planReady.done,
                                total: planReady.total,
                            })
                            : t('overview.dataStatus.valueUnavailable')}
                    </dd>
                </div>
                <div>
                    <dt>{t('overview.focus.tasksShipped')}</dt>
                    <dd>
                        {deliveryDataAvailable
                            && shippedTasks !== null
                            && totalTasks !== null
                            ? t('overview.tasksShipped', {
                                completed: shippedTasks,
                                total: totalTasks,
                                count: totalTasks,
                            })
                            : t('overview.dataStatus.valueUnavailable')}
                    </dd>
                </div>
                <div>
                    <dt>{t('overview.focus.iterationDay')}</dt>
                    <dd>{t('overview.dayOf', { day: progress.dayNo, total: workingDays })}</dd>
                </div>
            </dl>
        </div>
    );
};

const AttentionItemList = ({ items }: { items: AttentionItem[] }) => (
    <ul className="overview-exception-list">
        {items.map(item => {
            const Icon = item.icon;
            return (
                <li key={item.id}>
                    <Link to={item.to} className="overview-exception-link">
                        <span
                            className="overview-exception-icon"
                            style={pillBoxStyle(item.tone)}
                        >
                            <Icon aria-hidden="true" className="h-4 w-4" />
                        </span>
                        <span className="overview-exception-copy">
                            <strong>{item.title}</strong>
                            <span>{item.meta}</span>
                        </span>
                        <span className="overview-exception-action">
                            <span>{item.actionLabel}</span>
                            <ArrowRight aria-hidden="true" className="h-3.5 w-3.5" />
                        </span>
                    </Link>
                </li>
            );
        })}
    </ul>
);

const OverviewDetailCluster = ({
    id,
    icon,
    title,
    description,
    children,
}: {
    id: string;
    icon: ReactNode;
    title: ReactNode;
    description: ReactNode;
    children: ReactNode;
}) => (
    <section className="overview-detail-cluster" aria-labelledby={id}>
        <header className="overview-detail-cluster-head">
            <span className="overview-detail-cluster-icon">{icon}</span>
            <div>
                <h2 id={id}>{title}</h2>
                <p>{description}</p>
            </div>
        </header>
        <div className="overview-detail-cluster-body">{children}</div>
    </section>
);

const OtherExceptionsCluster = ({
    items,
    capacityExceptions,
}: {
    items: AttentionItem[];
    capacityExceptions: CapacityException[];
}) => {
    const { t, i18n } = useTranslation();
    const numberLocale = i18n.resolvedLanguage ?? i18n.language;

    return (
        <OverviewDetailCluster
            id="overview-other-exceptions"
            icon={<AlertTriangle aria-hidden="true" className="h-4 w-4" />}
            title={t('overview.details.otherExceptionsTitle')}
            description={t('overview.details.otherExceptionsDescription')}
        >
            {items.length > 0 && <AttentionItemList items={items} />}
            {capacityExceptions.length > 0 && (
                <div className={clsx('overview-capacity-exceptions', items.length > 0 && 'has-divider')}>
                    <h3>{t('overview.details.capacityWarnings')}</h3>
                    <ul className="overview-exception-list">
                        {capacityExceptions.map(exception => (
                            <li key={exception.id}>
                                <Link to="/team" className="overview-exception-link">
                                    <span
                                        className="overview-exception-icon"
                                        style={pillBoxStyle(exception.tone)}
                                    >
                                        <User aria-hidden="true" className="h-4 w-4" />
                                    </span>
                                    <span className="overview-exception-copy">
                                        <strong>{exception.name}</strong>
                                        <span>
                                            {exception.allocatedDays > exception.capacityDays
                                                ? t('overview.details.capacityOver', {
                                                    allocated: formatNumber(exception.allocatedDays, numberLocale),
                                                    capacity: formatNumber(exception.capacityDays, numberLocale),
                                                })
                                                : t('overview.details.capacityNear', {
                                                    percent: Math.round(exception.utilizationPercent),
                                                })}
                                        </span>
                                    </span>
                                    <span className="overview-exception-action">
                                        <span>{t('overview.focus.reviewTeam')}</span>
                                        <ArrowRight aria-hidden="true" className="h-3.5 w-3.5" />
                                    </span>
                                </Link>
                            </li>
                        ))}
                    </ul>
                </div>
            )}
        </OverviewDetailCluster>
    );
};

const CommitmentHealthCluster = ({ items }: { items: AttentionItem[] }) => {
    const { t } = useTranslation();
    return (
        <OverviewDetailCluster
            id="overview-commitment-health"
            icon={<Target aria-hidden="true" className="h-4 w-4" />}
            title={t('overview.details.commitmentHealthTitle')}
            description={t('overview.details.commitmentHealthDescription')}
        >
            <AttentionItemList items={items} />
        </OverviewDetailCluster>
    );
};

const WorkNowPreview = ({
    tasks,
    isProjectScoped,
    dataAvailable,
    dataLoading,
}: {
    tasks: Task[];
    isProjectScoped: boolean;
    dataAvailable: boolean;
    dataLoading: boolean;
}) => {
    const { t } = useTranslation();
    const openTaskCount = tasks.filter(task => !doneStatuses.has(task.status)).length;
    const visibleTasks = selectWorkNowTasks(tasks);
    const remainingTaskCount = Math.max(0, openTaskCount - visibleTasks.length);
    const hasConfirmedNoTasks = dataAvailable && tasks.length === 0;
    const hasConfirmedAllTasksComplete = (
        dataAvailable
        && tasks.length > 0
        && openTaskCount === 0
    );
    const shouldCreateTask = hasConfirmedNoTasks || hasConfirmedAllTasksComplete;
    const taskBoardPath = shouldCreateTask ? '/tasks?create=1' : '/tasks';
    const taskBoardLabel = hasConfirmedNoTasks
        ? t('overview.addFirstTask')
        : hasConfirmedAllTasksComplete
            ? t('overview.addTask')
            : t('overview.openTaskBoard');

    return (
        <SectionCard
            className="overview-work-now"
            headingLevel={2}
            headingId={WORK_NOW_TITLE_ID}
            icon={<ListTodo className="h-5 w-5 text-action" />}
            title={t('overview.workNow')}
            description={t('overview.workNowDescription')}
            actions={(
                <Link to={taskBoardPath} className="btn ghost sm">
                    {taskBoardLabel}
                    <ArrowRight aria-hidden="true" className="h-3.5 w-3.5" />
                </Link>
            )}
        >
            {!dataAvailable ? (
                <OverviewUnavailableState loading={dataLoading} />
            ) : visibleTasks.length === 0 ? (
                <InlineEmptyState>
                    {hasConfirmedNoTasks
                        ? t('overview.noWorkNowFirstUse')
                        : t('overview.noWorkNow')}
                </InlineEmptyState>
            ) : (
                <>
                    <ul className="divide-y divide-border-subtle overflow-hidden rounded-lg border border-border-subtle">
                        {visibleTasks.map(task => (
                            <TaskRow key={task.id} task={task} showProject={!isProjectScoped} />
                        ))}
                    </ul>
                    {remainingTaskCount > 0 && (
                        <p className="overview-work-now-summary">
                            {t('overview.workNowRemaining', { count: remainingTaskCount })}
                        </p>
                    )}
                </>
            )}
        </SectionCard>
    );
};

const TaskRow = ({ task, showProject }: { task: Task; showProject: boolean }) => {
    const { t, i18n } = useTranslation();
    const numberLocale = i18n.resolvedLanguage ?? i18n.language;
    const status = t(`statuses.${task.status}`);
    const tone = STATUS_TONE[task.status];

    return (
        <li>
            <Link
                id={overviewTaskReturnFocusId(task.id)}
                className="overview-task-row flex min-w-0 items-center gap-3 px-3 py-2.5"
                to={overviewTaskDrawerHref(task.id, 'work-now')}
                aria-label={t('overview.thread.openTask', { title: task.title })}
            >
                <div className="overview-task-copy min-w-0 flex-1">
                    <div className="overview-task-title text-sm font-medium text-content-primary">{task.title}</div>
                    <div className="mt-0.5 flex min-w-0 items-center gap-2 text-xs text-content-secondary">
                        <span className="inline-flex shrink-0 items-center gap-1.5 font-medium">
                            <span
                                aria-hidden="true"
                                className="h-1.5 w-1.5 shrink-0 rounded-full"
                                style={dotStyle(tone)}
                            />
                            <span>{status}</span>
                        </span>
                        {showProject && task.project && (
                            <span className="truncate">{task.project.name}</span>
                        )}
                    </div>
                </div>
                <div className="overview-task-metadata flex shrink-0 items-center gap-3">
                    {task.is_overdue && (
                        <span className="inline-flex h-5 shrink-0 items-center gap-1 rounded bg-feedback-danger-muted px-1.5 text-wc-micro font-semibold text-feedback-danger-foreground">
                            <Clock aria-hidden="true" className="h-3 w-3" />
                            {t('taskList.overdue')}
                        </span>
                    )}
                    <span className="w-10 shrink-0 text-right text-xs tabular-nums text-content-secondary">
                        {t('units.daysCompact', {
                            count: formatNumber(task.effort_days || 0, numberLocale),
                        })}
                    </span>
                    {task.assignee ? (
                        <span
                            title={task.assignee.name}
                            role="img"
                            aria-label={task.assignee.name}
                            className="grid h-7 w-7 shrink-0 place-items-center rounded-full bg-status-active-muted text-wc-micro font-bold text-action"
                        >
                            <span aria-hidden="true">{initialsFor(task.assignee.name)}</span>
                        </span>
                    ) : (
                        <span
                            title={t('common.unassigned')}
                            role="img"
                            aria-label={t('common.unassigned')}
                            className="grid h-7 w-7 shrink-0 place-items-center rounded-full border border-dashed border-border-strong bg-surface-card text-content-tertiary"
                        >
                            <User aria-hidden="true" className="h-3.5 w-3.5" />
                        </span>
                    )}
                    <ArrowRight
                        aria-hidden="true"
                        className="overview-task-open-icon h-4 w-4 shrink-0"
                    />
                </div>
            </Link>
        </li>
    );
};

const updateFreshnessText = (summary: ProjectSummary, t: TFunction) => {
    if (summary.update_freshness === 'not_required') return t('overview.freshnessLabels.not_required');
    if (summary.days_since_latest_update === null || summary.days_since_latest_update === undefined) {
        return t('overview.noUpdatePosted');
    }
    if (summary.days_since_latest_update <= 0) return t('overview.updatedToday');
    if (summary.days_since_latest_update === 1) return t('overview.updatedYesterday');
    return t('overview.daysSinceUpdate', { count: summary.days_since_latest_update });
};

const iterationPhase = (dayNo: number, workingDays: number, t: TFunction) => {
    if (dayNo <= 1) return t('overview.phase.start');
    if (dayNo >= workingDays) return t('overview.phase.closeout');
    const ratio = dayNo / Math.max(1, workingDays);
    if (ratio < 0.5) return t('overview.phase.early');
    if (ratio < 0.8) return t('overview.phase.middle');
    return t('overview.phase.final');
};

// Inline style for soft-tinted "pill box" elements (badges, icon tiles).
const pillBoxStyle = (tone: PillTone) => ({
    background: toneSoftVar[tone],
    color: toneVar[tone],
});

// Background colour (WorkChord token) for dots and progress fills.
const dotStyle = (tone: PillTone) => ({ background: toneVar[tone] });

export default OverviewPage;

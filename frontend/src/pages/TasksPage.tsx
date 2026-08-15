import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { useQuery } from '@tanstack/react-query';
import { Link, useSearchParams } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import {
    AlertTriangle,
    Bookmark,
    LayoutGrid,
    List,
    ListFilter,
    Maximize2,
    Minimize2,
    Plus,
    Upload,
    Waypoints,
    X,
} from 'lucide-react';
import { motion } from 'framer-motion';
import { Button } from '../components/common/Button';
import { Modal } from '../components/common/Modal';
import { FullscreenWorkspace } from '../components/common/FullscreenWorkspace';
import { QueryErrorState, QueryLoadingState } from '../components/feedback/QueryState';
import { TaskList } from '../components/tasks/TaskList';
import type { SortKey, TaskMode } from '../components/tasks/TaskList';
import { KanbanBoard } from '../components/tasks/KanbanBoard/KanbanBoard';
import { TaskForm } from '../components/tasks/TaskForm';
import { TaskEditorDrawer } from '../components/tasks/TaskEditorDrawer';
import { ImportTasksModal } from '../components/tasks/ImportTasksModal';
import { TaskFiltersBar } from '../components/tasks/TaskFiltersBar';
import type { TaskFilters } from '../components/tasks/TaskFiltersBar';
import { SavedViewsControl } from '../components/tasks/SavedViewsControl';
import { defaultFilters } from '../utils/taskFilterDefaults';
import { iterationService } from '../services/iterationService';
import { useIterationStore } from '../store/iterationStore';
import { IterationSelector } from '../components/iteration/IterationSelector';
import { OverflowMenu, PageHeader, PageLayout, SlideOverDrawer } from '../components/ui';
import type { SavedView } from '../types/savedView';
import { savedViewService } from '../services/savedViewService';
import { savedViewDisplay } from '../i18n/seedDisplay';
import clsx from 'clsx';
import { PlanReturnBar } from '../components/planning/PlanReturnBar';
import { OverviewTaskReturnBar } from '../components/overview/OverviewTaskReturnBar';
import { taskService } from '../services/taskService';
import {
    OVERVIEW_TASK_ORIGIN,
    OVERVIEW_TASK_ORIGIN_PARAM,
    OVERVIEW_TASK_PARAM,
    OVERVIEW_TASK_RETURN_PARAM,
    OVERVIEW_TASK_THREAD_PARAM,
    overviewTaskThreadSource,
    positiveTaskId,
} from '../features/overview/overviewTaskThread';
import {
    PLANNING_ITERATION_PARAM,
    PLANNING_TASK_ISSUE_PARAM,
    parsePlanningIterationId,
    parsePlanningTaskIssue,
} from '../features/planningMasters/planningTaskIssues';
import type {
    PlanningTaskIssue,
} from '../features/planningMasters/planningTaskIssues';

type ViewMode = 'list' | 'board';
const SORT_KEYS: SortKey[] = ['priority', 'sort_order', 'status', 'title'];
const PLANNING_ISSUE_COPY_KEYS: Record<
    PlanningTaskIssue,
    { title: string; body: string }
> = {
    unassigned: {
        title: 'tasks.planningIssueUnassignedTitle',
        body: 'tasks.planningIssueUnassignedBody',
    },
    'missing-effort': {
        title: 'tasks.planningIssueMissingEffortTitle',
        body: 'tasks.planningIssueMissingEffortBody',
    },
    any: {
        title: 'tasks.planningIssueAnyTitle',
        body: 'tasks.planningIssueAnyBody',
    },
};

const stringListFromValue = (value: unknown) => (
    Array.isArray(value) && value.every(item => typeof item === 'string') ? value : []
);

const nullableNumberFromValue = (value: unknown) => (
    typeof value === 'number' || value === null ? value : null
);

const nullableBooleanFromValue = (value: unknown) => (
    typeof value === 'boolean' || value === null ? value : null
);

const stringFromValue = (value: unknown) => (
    typeof value === 'string' ? value : ''
);

const nullableStringFromValue = (value: unknown) => (
    typeof value === 'string' || value === null ? value : null
);

const filtersFromSavedView = (view: SavedView): TaskFilters => {
    const raw = view.filters_json;
    return {
        ...defaultFilters,
        planningIssue: parsePlanningTaskIssue(raw.planningIssue),
        assigneeId: nullableNumberFromValue(raw.assigneeId),
        projectId: nullableNumberFromValue(raw.projectId),
        priority: nullableNumberFromValue(raw.priority),
        status: nullableStringFromValue(raw.status),
        hasDependency: nullableBooleanFromValue(raw.hasDependency),
        isOverdue: nullableBooleanFromValue(raw.isOverdue),
        agentReady: nullableBooleanFromValue(raw.agentReady),
        startDateFrom: stringFromValue(raw.startDateFrom),
        startDateTo: stringFromValue(raw.startDateTo),
        endDateFrom: stringFromValue(raw.endDateFrom),
        endDateTo: stringFromValue(raw.endDateTo),
        labelSlugs: stringListFromValue(raw.labelSlugs),
        labelGroupKeys: stringListFromValue(raw.labelGroupKeys),
    };
};

const sortKeyFromSavedView = (view: SavedView): SortKey | null => {
    const sortKey = view.sort_json.sortKey;
    return typeof sortKey === 'string' && SORT_KEYS.includes(sortKey as SortKey)
        ? sortKey as SortKey
        : null;
};

const TasksPage = () => {
    const [searchParams, setSearchParams] = useSearchParams();
    const { selectedIterationId, setSelectedIterationId } = useIterationStore();
    const [isCreating, setIsCreating] = useState(false);
    const [isImporting, setIsImporting] = useState(false);
    const [filters, setFilters] = useState<TaskFilters>(defaultFilters);
    const [sortKey, setSortKey] = useState<SortKey>('priority');
    const [selectedSavedViewId, setSelectedSavedViewId] = useState<number | null>(null);
    const [viewMode, setViewMode] = useState<ViewMode>('list');
    const [isFullScreen, setIsFullScreen] = useState(false);
    const [isFiltersOpen, setIsFiltersOpen] = useState(false);
    const appliedRequestedViewIdRef = useRef<number | null>(null);
    const overviewReturnActionRef = useRef<HTMLAnchorElement>(null);
    const requestedTaskId = positiveTaskId(searchParams.get(OVERVIEW_TASK_PARAM));
    const returnTaskId = positiveTaskId(
        searchParams.get(OVERVIEW_TASK_RETURN_PARAM),
    ) ?? requestedTaskId;
    const taskThreadSource = overviewTaskThreadSource(
        searchParams.get(OVERVIEW_TASK_THREAD_PARAM),
    );
    const isFromOverview = (
        searchParams.get(OVERVIEW_TASK_ORIGIN_PARAM) === OVERVIEW_TASK_ORIGIN
    );
    const focusedTaskContextId = requestedTaskId
        ?? (isFromOverview ? returnTaskId : null);
    const requestedSavedViewId = Number(searchParams.get('view')) || null;
    const createTaskRequested = searchParams.get('create') === '1';
    const filtersRequested = searchParams.get('panel') === 'filters';
    const fullscreenRequested = searchParams.get('fullscreen') === '1';
    const manualSortRequested = searchParams.get('sort') === 'manual';
    const requestedLayout = searchParams.get('layout');
    const requestedTaskMode = searchParams.get('mode');
    const rawPlanningIssue = searchParams.get(PLANNING_TASK_ISSUE_PARAM);
    const requestedPlanningIssue = parsePlanningTaskIssue(rawPlanningIssue);
    const rawPlanningIterationId = searchParams.get(PLANNING_ITERATION_PARAM);
    const requestedPlanningIterationId = parsePlanningIterationId(
        rawPlanningIterationId,
    );
    const taskMode: TaskMode | null = requestedTaskMode === 'bulk' || requestedTaskMode === 'merge'
        ? requestedTaskMode
        : null;
    const isCreateModalOpen = requestedTaskId === null
        && (isCreating || (createTaskRequested && selectedIterationId > 0));
    const { t } = useTranslation();
    const activeFilterCount =
        Number(filters.planningIssue !== null) +
        Number(filters.assigneeId !== null) +
        Number(filters.projectId !== null) +
        Number(filters.priority !== null) +
        Number(filters.status !== null) +
        Number(filters.hasDependency !== null) +
        Number(filters.isOverdue !== null) +
        Number(filters.agentReady !== null) +
        Number(Boolean(filters.startDateFrom)) +
        Number(Boolean(filters.startDateTo)) +
        Number(Boolean(filters.endDateFrom)) +
        Number(Boolean(filters.endDateTo)) +
        filters.labelSlugs.length +
        filters.labelGroupKeys.length;
    const planningIssueCopy = filters.planningIssue
        ? PLANNING_ISSUE_COPY_KEYS[filters.planningIssue]
        : null;

    const setTaskContextParam = useCallback((key: string, value: string | null) => {
        const nextSearchParams = new URLSearchParams(searchParams);
        if (value === null) nextSearchParams.delete(key);
        else nextSearchParams.set(key, value);
        setSearchParams(nextSearchParams, { replace: true });
    }, [searchParams, setSearchParams]);

    const openFilters = useCallback(() => {
        setIsFiltersOpen(true);
        setTaskContextParam('panel', 'filters');
    }, [setTaskContextParam]);

    const closeFilters = useCallback(() => {
        setIsFiltersOpen(false);
        setTaskContextParam('panel', null);
    }, [setTaskContextParam]);

    const changeViewMode = useCallback((layout: ViewMode) => {
        setViewMode(layout);
        setTaskContextParam('layout', layout === 'list' ? null : layout);
    }, [setTaskContextParam]);

    const enterFullscreen = useCallback(() => {
        setIsFullScreen(true);
        setTaskContextParam('fullscreen', '1');
    }, [setTaskContextParam]);

    const exitFullscreen = useCallback(() => {
        setIsFullScreen(false);
        setTaskContextParam('fullscreen', null);
    }, [setTaskContextParam]);

    const { data: iterations, isLoading: iterationsLoading, error: iterationsError, refetch: refetchIterations } = useQuery({
        queryKey: ['iterations'],
        queryFn: iterationService.getAll,
    });
    // feedback-policy: query loading,error,retry,empty - URL context stays
    // explicit while the task drawer owns loading, retry, and empty handling.
    const focusedTaskQuery = useQuery({
        queryKey: ['task', focusedTaskContextId],
        queryFn: () => taskService.getById(focusedTaskContextId as number),
        enabled: focusedTaskContextId !== null,
    });
    // feedback-policy: query loading,error,retry,empty - URL context stays explicit; the drawer owns retry and empty management.
    const {
        data: savedViews = [],
        isLoading: savedViewsLoading,
        error: savedViewsError,
    } = useQuery({
        queryKey: ['saved-views', 'tasks'],
        queryFn: () => savedViewService.getAll({ view_type: 'tasks' }),
    });
    const selectedSavedView = useMemo(
        () => savedViews.find(view => view.id === selectedSavedViewId) ?? null,
        [savedViews, selectedSavedViewId],
    );
    const requestedSavedView = useMemo(
        () => savedViews.find(view => view.id === requestedSavedViewId) ?? null,
        [requestedSavedViewId, savedViews],
    );
    const requestedSavedViewMissing = Boolean(
        requestedSavedViewId
        && !savedViewsLoading
        && !savedViewsError
        && (!requestedSavedView || !requestedSavedView.is_valid),
    );
    const requestedSavedViewLoadFailed = Boolean(
        requestedSavedViewId && savedViewsError,
    );

    useEffect(() => {
        if (!iterations || iterations.length === 0) return;

        if (rawPlanningIterationId !== null) {
            const requestedIterationExists = (
                requestedPlanningIterationId !== null
                && iterations.some(iteration => (
                    iteration.id === requestedPlanningIterationId
                ))
            );
            if (requestedIterationExists) {
                if (selectedIterationId !== requestedPlanningIterationId) {
                    setSelectedIterationId(requestedPlanningIterationId);
                }
                return;
            }

            const nextSearchParams = new URLSearchParams(searchParams);
            nextSearchParams.delete(PLANNING_ITERATION_PARAM);
            nextSearchParams.delete(PLANNING_TASK_ISSUE_PARAM);
            setSearchParams(nextSearchParams, { replace: true });
        }

        const iterationExists = iterations.some(i => i.id === selectedIterationId);
        if (selectedIterationId === 0 || !iterationExists) {
            setSelectedIterationId(iterations[0].id);
        }
    }, [
        iterations,
        rawPlanningIterationId,
        requestedPlanningIterationId,
        searchParams,
        selectedIterationId,
        setSearchParams,
        setSelectedIterationId,
    ]);

    useEffect(() => {
        if (rawPlanningIssue !== null && requestedPlanningIssue === null) {
            const nextSearchParams = new URLSearchParams(searchParams);
            nextSearchParams.delete(PLANNING_TASK_ISSUE_PARAM);
            setSearchParams(nextSearchParams, { replace: true });
            return;
        }

        if (requestedPlanningIssue) {
            if (requestedSavedViewId) {
                const nextSearchParams = new URLSearchParams(searchParams);
                nextSearchParams.delete('view');
                setSearchParams(nextSearchParams, { replace: true });
            }
            appliedRequestedViewIdRef.current = null;
            setSelectedSavedViewId(null);
            setFilters(current => (
                current.planningIssue === requestedPlanningIssue
                    ? current
                    : { ...current, planningIssue: requestedPlanningIssue }
            ));
            return;
        }

        if (!requestedSavedViewId) {
            setFilters(current => (
                current.planningIssue === null
                    ? current
                    : { ...current, planningIssue: null }
            ));
        }
    }, [
        rawPlanningIssue,
        requestedPlanningIssue,
        requestedSavedViewId,
        searchParams,
        setSearchParams,
    ]);

    useEffect(() => {
        const focusedTask = focusedTaskQuery.data;
        if (
            !focusedTask
            || focusedTask.iteration_id === selectedIterationId
            || !iterations?.some(iteration => iteration.id === focusedTask.iteration_id)
        ) {
            return;
        }
        setSelectedIterationId(focusedTask.iteration_id);
    }, [
        focusedTaskQuery.data,
        iterations,
        selectedIterationId,
        setSelectedIterationId,
    ]);

    useEffect(() => {
        setIsFiltersOpen(filtersRequested);
    }, [filtersRequested]);

    useEffect(() => {
        setIsFullScreen(fullscreenRequested);
    }, [fullscreenRequested]);

    useEffect(() => {
        setViewMode(requestedLayout === 'board' ? 'board' : 'list');
    }, [requestedLayout]);

    useEffect(() => {
        if (!manualSortRequested) return;
        setSortKey('sort_order');
        const nextSearchParams = new URLSearchParams(searchParams);
        nextSearchParams.delete('sort');
        setSearchParams(nextSearchParams, { replace: true });
    }, [manualSortRequested, searchParams, setSearchParams]);

    const closeTaskCreator = useCallback(() => {
        setIsCreating(false);
        if (!createTaskRequested) return;

        const nextSearchParams = new URLSearchParams(searchParams);
        nextSearchParams.delete('create');
        setSearchParams(nextSearchParams, { replace: true });
    }, [createTaskRequested, searchParams, setSearchParams]);

    const closeFocusedTask = useCallback(() => {
        const nextSearchParams = new URLSearchParams(searchParams);
        nextSearchParams.delete(OVERVIEW_TASK_PARAM);
        nextSearchParams.delete(OVERVIEW_TASK_THREAD_PARAM);
        setSearchParams(nextSearchParams, { replace: true });
    }, [searchParams, setSearchParams]);

    const applySavedView = useCallback((view: SavedView) => {
        setFilters(filtersFromSavedView(view));
        const savedSortKey = sortKeyFromSavedView(view);
        if (savedSortKey) {
            setSortKey(savedSortKey);
        }
    }, []);

    const selectSavedView = useCallback((viewId: number | null) => {
        setSelectedSavedViewId(viewId);
        const nextSearchParams = new URLSearchParams(searchParams);
        if (viewId) {
            nextSearchParams.set('view', String(viewId));
            nextSearchParams.delete(PLANNING_TASK_ISSUE_PARAM);
        } else {
            nextSearchParams.delete('view');
        }
        setSearchParams(nextSearchParams, { replace: true });
    }, [searchParams, setSearchParams]);

    const clearViewContext = useCallback(() => {
        setFilters(defaultFilters);
        setSortKey('priority');
        appliedRequestedViewIdRef.current = null;
        setSelectedSavedViewId(null);
        const nextSearchParams = new URLSearchParams(searchParams);
        nextSearchParams.delete('view');
        nextSearchParams.delete(PLANNING_TASK_ISSUE_PARAM);
        setSearchParams(nextSearchParams, { replace: true });
    }, [searchParams, setSearchParams]);

    const changeFilters = useCallback((nextFilters: TaskFilters) => {
        const planningIssueChanged = (
            nextFilters.planningIssue !== filters.planningIssue
        );
        setFilters(nextFilters);
        if (!planningIssueChanged) return;

        appliedRequestedViewIdRef.current = null;
        setSelectedSavedViewId(null);
        const nextSearchParams = new URLSearchParams(searchParams);
        nextSearchParams.delete('view');
        if (nextFilters.planningIssue) {
            nextSearchParams.set(
                PLANNING_TASK_ISSUE_PARAM,
                nextFilters.planningIssue,
            );
        } else {
            nextSearchParams.delete(PLANNING_TASK_ISSUE_PARAM);
        }
        setSearchParams(nextSearchParams, { replace: true });
    }, [filters.planningIssue, searchParams, setSearchParams]);

    const clearIterationViewContext = useCallback(() => {
        setFilters(defaultFilters);
        setSortKey('priority');
        appliedRequestedViewIdRef.current = null;
        setSelectedSavedViewId(null);
        const nextSearchParams = new URLSearchParams(searchParams);
        nextSearchParams.delete('view');
        nextSearchParams.delete(PLANNING_TASK_ISSUE_PARAM);
        nextSearchParams.delete(PLANNING_ITERATION_PARAM);
        setSearchParams(nextSearchParams, { replace: true });
    }, [searchParams, setSearchParams]);

    useEffect(() => {
        if (!requestedSavedViewId) {
            if (appliedRequestedViewIdRef.current === null) return undefined;
            const clearTimer = window.setTimeout(() => {
                appliedRequestedViewIdRef.current = null;
                setSelectedSavedViewId(null);
                setFilters(defaultFilters);
                setSortKey('priority');
            }, 0);
            return () => window.clearTimeout(clearTimer);
        }
        if (
            appliedRequestedViewIdRef.current === requestedSavedViewId
            || !requestedSavedView?.is_valid
        ) {
            return undefined;
        }

        const applyTimer = window.setTimeout(() => {
            appliedRequestedViewIdRef.current = requestedSavedViewId;
            setSelectedSavedViewId(requestedSavedView.id);
            applySavedView(requestedSavedView);
        }, 0);
        return () => window.clearTimeout(applyTimer);
    }, [applySavedView, requestedSavedView, requestedSavedViewId]);

    if (iterationsLoading) {
        return <QueryLoadingState message={t('queryFeedback.loading')} />;
    }

    if (iterationsError) {
        return <QueryErrorState error={iterationsError} onRetry={() => void refetchIterations()} />;
    }

    if (!iterations || iterations.length === 0) {
        return (
            <PageLayout>
                <PageHeader
                    title={t('tasks.title')}
                    subtitle={t('tasks.noIterationsBody')}
                    actions={(
                        <Link to="/iterations" className="btn primary">
                            {t('tasks.goToIterations')}
                        </Link>
                    )}
                />
                <PlanReturnBar />
                <div className="empty">
                    <h4>{t('tasks.noIterationsTitle')}</h4>
                    <p>{t('tasks.noIterationsBody')}</p>
                </div>
            </PageLayout>
        );
    }

    return (
        <PageLayout variant="workbench" className="wc-workbench-flush tasks-workbench">
            {/* Main Content Area */}
            <div className="tasks-workbench-shell flex-1 min-w-0 flex flex-col h-full overflow-hidden">
                <PlanReturnBar />
                <OverviewTaskReturnBar
                    active={isFromOverview}
                    taskId={returnTaskId}
                    taskTitle={focusedTaskQuery.data?.title}
                    returnActionRef={overviewReturnActionRef}
                />
                <div className="tasks-workbench-header-wrap flex-shrink-0 px-4 pt-4 pb-3">
                    <div className="wc-page-head tasks-workbench-header" data-testid="page-header">
                        <div className="tasks-workbench-heading">
                            <h1 className="wc-page-title">{t('tasks.title')}</h1>
                            <div className="wc-page-sub">{t('tasks.description')}</div>
                        </div>
                        <div className="row tasks-header-actions">
                        <IterationSelector
                            className="tasks-iteration-selector"
                            onChange={clearIterationViewContext}
                        />
                        <OverflowMenu
                            className="tasks-overflow-trigger"
                            label={t('actions.moreActions')}
                            items={[
                                {
                                    label: t('actions.import'),
                                    icon: <Upload className="h-4 w-4" aria-hidden="true" />,
                                    onSelect: () => setIsImporting(true),
                                    disabled: selectedIterationId === 0,
                                },
                                {
                                    label: t('actions.enterFullScreen'),
                                    icon: <Maximize2 className="h-4 w-4" aria-hidden="true" />,
                                    onSelect: enterFullscreen,
                                },
                            ]}
                        />
                        <div className="tasks-primary-slot">
                            <Button
                                className="tasks-primary-action"
                                onClick={() => setIsCreating(true)}
                                disabled={isCreating || selectedIterationId === 0}
                            >
                                <Plus className="h-4 w-4" aria-hidden="true" />
                                {t('tasks.newTask')}
                            </Button>
                        </div>
                        </div>
                    </div>
                </div>

                {selectedIterationId > 0 && (
                    <div className="tasks-context-wrap flex-shrink-0 px-6 pb-3">
                        <section
                            className={clsx(
                                'tasks-view-context border-y px-1 py-2.5 text-sm',
                                requestedSavedViewMissing || requestedSavedViewLoadFailed
                                    ? 'border-feedback-warning-border bg-feedback-warning-muted'
                                    : 'border-border-subtle',
                            )}
                            aria-label={t('tasks.viewContext')}
                        >
                            <div className="tasks-view-context-copy flex min-w-0 items-center gap-2">
                                {requestedSavedViewMissing || requestedSavedViewLoadFailed ? (
                                    <AlertTriangle
                                        className="h-4 w-4 shrink-0 text-feedback-warning-foreground"
                                        aria-hidden="true"
                                    />
                                ) : (
                                    <Bookmark
                                        className="h-4 w-4 shrink-0 text-action"
                                        aria-hidden="true"
                                    />
                                )}
                                <div className="min-w-0">
                                    <div className="truncate font-medium text-content-primary">
                                        {requestedSavedViewLoadFailed
                                            ? t('tasks.savedViewsLoadFailed')
                                            : requestedSavedViewMissing
                                                ? t('tasks.savedViewUnavailable')
                                                : requestedSavedViewId && savedViewsLoading
                                                    ? t('tasks.loadingSavedView')
                                            : selectedSavedView
                                                ? savedViewDisplay(selectedSavedView).name
                                                : planningIssueCopy
                                                    ? t(planningIssueCopy.title)
                                                    : activeFilterCount > 0
                                                        ? t('tasks.customView')
                                                        : t('tasks.allTasks')}
                                    </div>
                                    <div className="text-xs text-content-secondary">
                                        {requestedSavedViewLoadFailed
                                            ? t('tasks.savedViewsLoadFailedBody')
                                            : requestedSavedViewMissing
                                                ? t('tasks.savedViewUnavailableBody')
                                                : requestedSavedViewId && savedViewsLoading
                                                    ? t('tasks.loadingSavedViewBody')
                                            : !selectedSavedView && planningIssueCopy
                                                ? t(planningIssueCopy.body)
                                                : activeFilterCount > 0
                                                    ? t('tasks.activeFilterCount', { count: activeFilterCount })
                                                    : t('tasks.noActiveFilters')}
                                    </div>
                                </div>
                            </div>
                            <div className="tasks-context-actions flex flex-wrap items-center gap-2">
                                {(activeFilterCount > 0 || selectedSavedViewId || requestedSavedViewId) && (
                                    <Button
                                        className="tasks-clear-view"
                                        variant="ghost"
                                        size="sm"
                                        aria-label={t('tasks.clearView')}
                                        onClick={clearViewContext}
                                    >
                                        <X className="mr-1 h-4 w-4" aria-hidden="true" />
                                        <span>{t('tasks.clearView')}</span>
                                    </Button>
                                )}
                                <Button
                                    variant={activeFilterCount > 0 ? 'secondary' : 'outline'}
                                    size="sm"
                                    onClick={openFilters}
                                    aria-expanded={isFiltersOpen}
                                >
                                    <ListFilter className="mr-1 h-4 w-4" aria-hidden="true" />
                                    {t('taskFilters.filters')}
                                    {activeFilterCount > 0 && (
                                        <span className="ml-1 rounded-full bg-surface-card/80 px-1.5 py-0.5 text-xs tabular-nums">
                                            {activeFilterCount}
                                        </span>
                                    )}
                                </Button>
                            </div>
                            <div className="tasks-view-switcher flex w-fit bg-surface-subtle p-1 rounded-lg" role="group" aria-label={t('tasks.title')}>
                            <button
                                type="button"
                                onClick={() => changeViewMode('list')}
                                aria-pressed={viewMode === 'list'}
                                className={clsx(
                                    "relative px-3 py-1.5 rounded-md text-sm font-medium transition-colors flex items-center gap-2",
                                    viewMode === 'list' ? "text-content-primary" : "text-content-secondary hover:text-content-primary"
                                )}
                            >
                                {viewMode === 'list' && (
                                    <motion.div
                                        layoutId="view-tab"
                                        className="absolute inset-0 bg-surface-card shadow-sm rounded-md"
                                        initial={false}
                                        transition={{ duration: 0.18, ease: [0.16, 1, 0.3, 1] }}
                                    />
                                )}
                                <span className="relative z-10 flex items-center gap-2">
                                    <List className="w-4 h-4" />
                                    {t('tasks.list')}
                                </span>
                            </button>
                            <button
                                type="button"
                                onClick={() => changeViewMode('board')}
                                aria-pressed={viewMode === 'board'}
                                className={clsx(
                                    "relative px-3 py-1.5 rounded-md text-sm font-medium transition-colors flex items-center gap-2",
                                    viewMode === 'board' ? "text-content-primary" : "text-content-secondary hover:text-content-primary"
                                )}
                            >
                                {viewMode === 'board' && (
                                    <motion.div
                                        layoutId="view-tab"
                                        className="absolute inset-0 bg-surface-card shadow-sm rounded-md"
                                        initial={false}
                                        transition={{ duration: 0.18, ease: [0.16, 1, 0.3, 1] }}
                                    />
                                )}
                                <span className="relative z-10 flex items-center gap-2">
                                    <LayoutGrid className="w-4 h-4" />
                                    {t('tasks.board')}
                                </span>
                            </button>
                            </div>
                        </section>
                    </div>
                )}

                <SlideOverDrawer
                    open={isFiltersOpen && requestedTaskId === null}
                    title={t('taskFilters.filters')}
                    icon={<ListFilter className="h-4 w-4" aria-hidden="true" />}
                    onClose={closeFilters}
                >
                    {selectedIterationId > 0 && (
                        <>
                            <TaskFiltersBar
                                iterationId={selectedIterationId}
                                filters={filters}
                                onFiltersChange={changeFilters}
                            />
                            <section className="border-t border-border px-4 py-4">
                                <h2 className="mb-3 text-sm font-semibold text-content-primary">{t('surfaces.savedViews.savedViews')}</h2>
                                <SavedViewsControl
                                    filters={filters}
                                    sortKey={sortKey}
                                    selectedViewId={selectedSavedViewId}
                                    onSelectedViewIdChange={viewId => {
                                        if (viewId === null) {
                                            clearViewContext();
                                            return;
                                        }
                                        selectSavedView(viewId);
                                    }}
                                    onApplyView={applySavedView}
                                />
                            </section>
                        </>
                    )}
                </SlideOverDrawer>

                <TaskEditorDrawer
                    taskId={requestedTaskId}
                    open={requestedTaskId !== null}
                    onClose={closeFocusedTask}
                    title={task => task?.title ?? (
                        isFromOverview && requestedTaskId !== null
                            ? t('taskEditor.taskCode', { id: requestedTaskId })
                            : t('taskEditor.editTask')
                    )}
                    subtitle={isFromOverview
                        ? t(
                            taskThreadSource === 'attention'
                                ? 'overview.thread.drawerAttention'
                                : 'overview.thread.drawerWorkNow',
                        )
                        : undefined}
                    icon={isFromOverview
                        ? <Waypoints aria-hidden="true" className="h-4 w-4" />
                        : undefined}
                    className={clsx(
                        'max-w-2xl',
                        isFromOverview && 'overview-task-drawer',
                    )}
                    restoreFocusRef={isFromOverview
                        ? overviewReturnActionRef
                        : undefined}
                />

                {selectedIterationId > 0 && (
                    <FullscreenWorkspace
                        open={isFullScreen}
                        onClose={exitFullscreen}
                        ariaLabel={t('tasks.fullScreenLabel')}
                        className="tasks-workbench-content flex-1 overflow-hidden relative"
                    >
                        {isFullScreen && (
                            <div className="flex justify-between items-center px-6 py-4 flex-shrink-0 border-b border-border-subtle">
                                <div>
                                    <h2 className="text-2xl font-bold text-content-primary">
                                        {viewMode === 'list' ? t('tasks.taskList') : t('tasks.boardView')}
                                    </h2>
                                    <p className="text-content-secondary text-sm">{t('tasks.focusMode')}</p>
                                </div>
                                <Button variant="ghost" onClick={exitFullscreen}>
                                    <Minimize2 className="w-5 h-5 mr-2" /> {t('actions.exitFullScreen')}
                                </Button>
                            </div>
                        )}

                        {viewMode === 'list' ? (
                            <div className="h-full overflow-y-auto">
                                <div className={clsx(
                                    'tasks-list-content',
                                    isFullScreen ? 'p-6' : 'px-6 pb-6',
                                )}>
                                    <TaskList
                                        iterationId={selectedIterationId}
                                        filters={filters}
                                        sortKey={sortKey}
                                        onSortKeyChange={setSortKey}
                                        hasActiveFilters={activeFilterCount > 0}
                                        activeViewName={selectedSavedView
                                            ? savedViewDisplay(selectedSavedView).name
                                            : planningIssueCopy
                                                ? t(planningIssueCopy.title)
                                                : undefined}
                                        onClearFilters={clearViewContext}
                                        onCreateTask={() => setIsCreating(true)}
                                        requestedMode={taskMode}
                                        onModeChange={mode => setTaskContextParam('mode', mode)}
                                    />
                                </div>
                            </div>
                        ) : (
                            <div className="h-full overflow-hidden">
                                <KanbanBoard iterationId={selectedIterationId} filters={filters} />
                            </div>
                        )}
                    </FullscreenWorkspace>
                )}
            </div>

            <Modal open={isCreateModalOpen} title={t('tasks.createNewTask')} closeLabel={t('actions.close')} onClose={closeTaskCreator}>
                {isCreateModalOpen && (
                        <TaskForm
                            iterationId={selectedIterationId}
                            onSuccess={closeTaskCreator}
                            onCancel={closeTaskCreator}
                        />
                )}
            </Modal>

            {isImporting && (
                <ImportTasksModal
                    iterationId={selectedIterationId}
                    onClose={() => setIsImporting(false)}
                />
            )}
        </PageLayout>
    );
};

export default TasksPage;

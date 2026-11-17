import { filtersFromSavedView, sortKeyFromSavedView } from '../features/savedViews/taskViewState';
import {
    activeFilterCount as countActiveFilters,
    filtersFromSearchParams,
    groupByStatusFromSearchParams,
    searchParamsNameView,
    sortKeyFromSearchParams,
    TASK_CLEARED_VIEW_PARAM,
    TASK_FILTER_PARAMS,
    TASK_GROUP_PARAM,
    TASK_SORT_PARAM,
    writeClearedViewMarker,
    writeFiltersToSearchParams,
    writeSortKeyToSearchParams,
} from '../features/savedViews/taskViewParams';
import { PipelineView } from '../components/tasks/PipelineView';
import { PipelineTaskEvidence } from '../components/tasks/PipelineTaskEvidence';
import { usePipeline } from '../components/tasks/usePipeline';
import { labelService } from '../services/labelService';
import { BacklogPanel } from '../components/tasks/BacklogPanel';
import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import type { ReactNode } from 'react';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { Link, useLocation, useSearchParams } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import {
    AlertTriangle,
    Bot,
    FileText,
    LayoutGrid,
    List,
    Maximize2,
    Minimize2,
    Plus,
    Search,
    Upload,
    Waypoints,
    X,
} from 'lucide-react';
import { Button } from '../components/common/Button';
import { Input } from '../components/common/Input';
import { FullscreenWorkspace } from '../components/common/FullscreenWorkspace';
import { QueryErrorState, QueryLoadingState } from '../components/feedback/QueryState';
import { TaskList } from '../components/tasks/TaskList';
import type { SortKey, TaskMode } from '../components/tasks/TaskList';
import { KanbanBoard } from '../components/tasks/KanbanBoard/KanbanBoard';
import { GuardedTaskModal } from '../components/tasks/GuardedTaskModal';
import { TaskEditorDrawer } from '../components/tasks/TaskEditorDrawer';
import { QuickCapture } from '../components/tasks/QuickCapture';
import { ImportTasksModal } from '../components/tasks/ImportTasksModal';
import { TaskFiltersBar } from '../components/tasks/TaskFiltersBar';
import { TaskTextEditorModal } from '../components/tasks/TaskTextEditorModal';
import { TaskViewOptions } from '../components/tasks/TaskViewOptions';
import { TASK_PART_PARAM } from '../components/tasks/TaskReadView';
import type { Task } from '../types/task';
import type { TaskFilters } from '../components/tasks/TaskFiltersBar';
import { SavedViewPicker } from '../components/tasks/SavedViewsControl';
import { useSavedViewManager } from '../components/tasks/useSavedViewManager';
import { defaultFilters } from '../utils/taskFilterDefaults';
import { iterationService } from '../services/iterationService';
import { useWorkScope } from '../features/scope/useWorkScope';
import { urlNamesIteration } from '../features/scope/namedIteration';
import { useLinkScope, useScopeLink } from '../features/scope/useScopeLink';
import { resolveWorkScope, type ScopeIteration as ScopeIterationValue } from '../features/scope/workScope';
import { PageHeader, PageLayout, PageToolbar, ViewSwitch } from '../components/ui';
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
import { PLANNING_RETURN_STEP_PARAM } from '../features/planningMasters/planningReturn';

type ViewMode = 'list' | 'board' | 'pipeline';
const VIEW_PARAM = 'view';
const SEARCH_PARAM = 'q';

const viewModeFromParam = (value: string | null): ViewMode => (
    value === 'board' || value === 'pipeline' ? value : 'list'
);

/** Conditions another page applied on the way here, such as Plan handing over its scheduling gaps. */
const handedOverFilters = (params: URLSearchParams): Partial<TaskFilters> => {
    const planningIssue = parsePlanningTaskIssue(params.get(PLANNING_TASK_ISSUE_PARAM));
    const fromPlan = params.has(PLANNING_RETURN_STEP_PARAM) || params.has(PLANNING_ITERATION_PARAM);
    return planningIssue && fromPlan ? { planningIssue } : {};
};

/** Shows the view's filters and order in `params`, or no filters for All tasks. */
const writeViewToSearchParams = (params: URLSearchParams, view: SavedView | null) => {
    writeFiltersToSearchParams(params, view ? filtersFromSavedView(view) : defaultFilters);
    writeSortKeyToSearchParams(params, (view && sortKeyFromSavedView(view)) ?? 'priority');
    params.delete(TASK_CLEARED_VIEW_PARAM);
    if (view) params.set(VIEW_PARAM, String(view.id));
    else params.delete(VIEW_PARAM);
    return params;
};

const TasksPage = () => {
    const [searchParams, setSearchParams] = useSearchParams();
    const { search: locationSearch } = useLocation();
    const { project, iteration, setIteration } = useWorkScope();
    const selectedIterationId = typeof iteration === 'number' ? iteration : 0;
    const isBacklog = iteration === 'backlog';
    const scopeLink = useScopeLink();
    const linkedScope = useLinkScope();
    // Older links open the backlog with ?scope=backlog; the scope now says so with iteration=backlog.
    const legacyBacklogRequested = searchParams.get('scope') === 'backlog';
    const isBacklogView = isBacklog || legacyBacklogRequested;
    const [isCreating, setIsCreating] = useState(false);
    const [createTitle, setCreateTitle] = useState('');
    const [isImporting, setIsImporting] = useState(false);
    const [isTextEditorOpen, setIsTextEditorOpen] = useState(false);
    // The view, its filters, order, grouping, search and layout all live in the URL.
    const filters = useMemo(() => filtersFromSearchParams(searchParams), [searchParams]);
    const sortKey = useMemo(() => sortKeyFromSearchParams(searchParams), [searchParams]);
    const groupByStatus = groupByStatusFromSearchParams(searchParams);
    const searchText = searchParams.get(SEARCH_PARAM) ?? '';
    const [systemFilters] = useState(() => handedOverFilters(searchParams));
    const appliedRequestedViewIdRef = useRef<number | null>(null);
    const appliedPlanningIterationRef = useRef<string | null>(null);
    // The iteration this page chose itself; a scope change to it keeps the filters and view.
    const appliedScopeChangeRef = useRef<number | null>(null);
    const shownIterationRef = useRef<ScopeIterationValue | undefined>(iteration);
    // The task opened by the URL, and whether it may still move the scope to its iteration.
    const taskScopeMoveRef = useRef<{ taskId: number; pending: boolean } | null>(null);
    const overviewReturnActionRef = useRef<HTMLAnchorElement>(null);
    const toolbarRef = useRef<HTMLDivElement>(null);
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
    // The return bar names the task Overview opened; it is not scope, so it never moves the scope.
    const focusedTaskContextId = requestedTaskId
        ?? (isFromOverview ? returnTaskId : null);
    const iterationNamedByUrl = urlNamesIteration(locationSearch) || legacyBacklogRequested;
    const requestedSavedViewId = Number(searchParams.get(VIEW_PARAM)) || null;
    const createTaskRequested = searchParams.get('create') === '1';
    const filtersRequested = searchParams.get('panel') === 'filters';
    const isFullScreen = searchParams.get('fullscreen') === '1';
    const viewMode = viewModeFromParam(searchParams.get('layout'));
    const pipelineQuery = usePipeline(viewMode === 'pipeline');
    const agentFilter = searchParams.get('agent') ?? '';
    // feedback-policy: query loading,error,retry,empty - TaskFiltersBar reports option errors and retry.
    const { data: pipelineLabelGroups = [] } = useQuery({ queryKey: ['label-groups'], queryFn: () => labelService.getGroups(), enabled: viewMode === 'pipeline' });
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
    // On the Backlog a new task goes to the scope's project with no iteration; All projects names no project.
    const backlogProjectId = isBacklogView && typeof project === 'number' ? project : null;
    const canCreateTask = isBacklogView ? backlogProjectId !== null : selectedIterationId > 0;
    const isCreateModalOpen = requestedTaskId === null
        && (isCreating || (createTaskRequested && canCreateTask));
    const queryClient = useQueryClient();
    const { t } = useTranslation();
    const activeFilterCount = countActiveFilters(filters);

    const updateSearchParams = useCallback((change: (next: URLSearchParams) => void) => {
        const nextSearchParams = new URLSearchParams(searchParams);
        change(nextSearchParams);
        setSearchParams(nextSearchParams, { replace: true });
    }, [searchParams, setSearchParams]);

    const setTaskContextParam = useCallback((key: string, value: string | null) => {
        updateSearchParams(next => {
            if (value === null) next.delete(key);
            else next.set(key, value);
        });
    }, [updateSearchParams]);

    const changeViewMode = useCallback((layout: ViewMode) => {
        setTaskContextParam('layout', layout === 'list' ? null : layout);
    }, [setTaskContextParam]);

    const enterFullscreen = useCallback(() => {
        setTaskContextParam('fullscreen', '1');
    }, [setTaskContextParam]);

    const exitFullscreen = useCallback(() => {
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

    const changeFilters = useCallback((nextFilters: TaskFilters) => {
        updateSearchParams(next => writeClearedViewMarker(writeFiltersToSearchParams(next, nextFilters), next.has(VIEW_PARAM)));
    }, [updateSearchParams]);

    const changeSortKey = useCallback((nextSortKey: SortKey) => {
        updateSearchParams(next => writeClearedViewMarker(writeSortKeyToSearchParams(next, nextSortKey), next.has(VIEW_PARAM)));
    }, [updateSearchParams]);

    const changeGrouping = useCallback((grouped: boolean) => {
        setTaskContextParam(TASK_GROUP_PARAM, grouped ? null : 'none');
    }, [setTaskContextParam]);

    const changeSearch = useCallback((value: string) => {
        setTaskContextParam(SEARCH_PARAM, value ? value.slice(0, 200) : null);
    }, [setTaskContextParam]);

    const showSavedView = useCallback((view: SavedView | null) => {
        appliedRequestedViewIdRef.current = view?.id ?? null;
        updateSearchParams(next => writeViewToSearchParams(next, view));
    }, [updateSearchParams]);

    const clearViewContext = useCallback(() => {
        showSavedView(null);
    }, [showSavedView]);

    // The empty list's Clear filters removes every condition that hides tasks: the view's filters and the search.
    const clearListConditions = useCallback(() => {
        appliedRequestedViewIdRef.current = null;
        updateSearchParams(next => {
            writeViewToSearchParams(next, null);
            next.delete(SEARCH_PARAM);
        });
    }, [updateSearchParams]);

    const savedViewManager = useSavedViewManager({
        filters,
        sortKey,
        systemFilters,
        selectedViewId: requestedSavedView?.is_valid ? requestedSavedView.id : null,
        onSelectedViewIdChange: viewId => {
            // A view just saved, duplicated or updated already shows these filters; only its name changes.
            if (viewId === null) {
                clearViewContext();
                return;
            }
            appliedRequestedViewIdRef.current = viewId;
            setTaskContextParam(VIEW_PARAM, String(viewId));
        },
        onApplyView: showSavedView,
    });

    // A link that names an iteration for planning opens the scope on it once; the scope bar then
    // changes it freely. A name that matches no iteration is dropped from the URL.
    useEffect(() => {
        if (!iterations || iterations.length === 0) return;
        if (rawPlanningIterationId === null) {
            appliedPlanningIterationRef.current = null;
            return;
        }
        if (appliedPlanningIterationRef.current === rawPlanningIterationId) return;
        appliedPlanningIterationRef.current = rawPlanningIterationId;

        const requestedIterationExists = (
            requestedPlanningIterationId !== null
            && iterations.some(item => item.id === requestedPlanningIterationId)
        );
        if (requestedIterationExists) {
            if (selectedIterationId !== requestedPlanningIterationId) {
                appliedScopeChangeRef.current = requestedPlanningIterationId;
                setIteration(requestedPlanningIterationId);
            }
            return;
        }

        updateSearchParams(next => {
            next.delete(PLANNING_ITERATION_PARAM);
            next.delete(PLANNING_TASK_ISSUE_PARAM);
        });
    }, [
        iterations,
        rawPlanningIterationId,
        requestedPlanningIterationId,
        selectedIterationId,
        setIteration,
        updateSearchParams,
    ]);

    useEffect(() => {
        if (!legacyBacklogRequested) return;
        updateSearchParams(next => {
            next.delete('scope');
            next.set('iteration', 'backlog');
        });
    }, [legacyBacklogRequested, updateSearchParams]);

    // Leaving the backlog opens the project's default iteration, else the default across projects.
    const iterationTasksScope = useMemo(() => {
        if (!iterations || iterations.length === 0) return undefined;
        const inProject = resolveWorkScope({ project: linkedScope.project }, {}, iterations);
        return inProject.iteration === 'backlog' ? resolveWorkScope({}, {}, iterations) : inProject;
    }, [iterations, linkedScope.project]);

    // A planning issue the page does not know is dropped from the URL.
    useEffect(() => {
        if (rawPlanningIssue === null || requestedPlanningIssue !== null) return;
        setTaskContextParam(PLANNING_TASK_ISSUE_PARAM, null);
    }, [rawPlanningIssue, requestedPlanningIssue, setTaskContextParam]);

    // The Filters command (?panel=filters) moves focus to the first filter in the toolbar.
    useEffect(() => {
        if (!filtersRequested || iterationsLoading) return;
        toolbarRef.current?.querySelector<HTMLElement>('.wc-page-toolbar-filters select, .wc-page-toolbar-filters input')?.focus();
        setTaskContextParam('panel', null);
    }, [filtersRequested, iterationsLoading, setTaskContextParam]);

    // The scope in the URL decides. A task opened by a URL that names no iteration moves the
    // scope to the task's iteration once; a link, a reload or a scope already chosen that names
    // an iteration (Backlog too) keeps it. The scope bar then changes the scope freely.
    useEffect(() => {
        if (requestedTaskId === null) {
            taskScopeMoveRef.current = null;
            return;
        }
        if (taskScopeMoveRef.current?.taskId !== requestedTaskId) {
            taskScopeMoveRef.current = { taskId: requestedTaskId, pending: !iterationNamedByUrl };
        }
        const move = taskScopeMoveRef.current;
        if (!move.pending) return;
        const focusedTask = focusedTaskQuery.data;
        if (!focusedTask || focusedTask.id !== requestedTaskId || !iterations) return;
        move.pending = false;
        if (
            focusedTask.iteration_id === null
            || focusedTask.iteration_id === selectedIterationId
            || !iterations.some(iteration => iteration.id === focusedTask.iteration_id)
        ) {
            return;
        }
        appliedScopeChangeRef.current = focusedTask.iteration_id;
        setIteration(focusedTask.iteration_id);
    }, [
        focusedTaskQuery.data,
        iterationNamedByUrl,
        iterations,
        requestedTaskId,
        selectedIterationId,
        setIteration,
    ]);

    const closeTaskCreator = useCallback(() => {
        setIsCreating(false);
        setCreateTitle('');
        if (isBacklogView) void queryClient.invalidateQueries({ queryKey: ['backlog'] });
        if (!createTaskRequested) return;
        setTaskContextParam('create', null);
    }, [createTaskRequested, isBacklogView, queryClient, setTaskContextParam]);

    const closeFocusedTask = useCallback(() => {
        updateSearchParams(next => {
            next.delete(OVERVIEW_TASK_PARAM);
            next.delete(OVERVIEW_TASK_THREAD_PARAM);
            next.delete(TASK_PART_PARAM);
        });
    }, [updateSearchParams]);
    // Opening a task puts it in the URL, so a refresh or a copied link reopens it.
    const openTask = useCallback((task: Task) => {
        const nextSearchParams = new URLSearchParams(searchParams);
        nextSearchParams.set(OVERVIEW_TASK_PARAM, String(task.id));
        nextSearchParams.delete(TASK_PART_PARAM);
        setSearchParams(nextSearchParams);
    }, [searchParams, setSearchParams]);

    // Another iteration in the scope bar starts with no filters, no search and no saved view.
    const clearIterationViewContext = useCallback(() => {
        appliedRequestedViewIdRef.current = null;
        updateSearchParams(next => {
            Object.values(TASK_FILTER_PARAMS).forEach(param => next.delete(param));
            next.delete(TASK_SORT_PARAM);
            next.delete(TASK_CLEARED_VIEW_PARAM);
            next.delete(VIEW_PARAM);
            next.delete(SEARCH_PARAM);
            next.delete(PLANNING_ITERATION_PARAM);
        });
    }, [updateSearchParams]);

    useEffect(() => {
        const previous = shownIterationRef.current;
        shownIterationRef.current = iteration;
        if (previous === undefined || previous === iteration) return;
        if (appliedScopeChangeRef.current === iteration) {
            appliedScopeChangeRef.current = null;
            return;
        }
        clearIterationViewContext();
    }, [clearIterationViewContext, iteration]);

    // A link that names only a saved view (?view=<id>) shows that view's filters and order once.
    // A link that also carries filters or an order shows those: it is the view as someone left it.
    useEffect(() => {
        if (!requestedSavedViewId) {
            appliedRequestedViewIdRef.current = null;
            return;
        }
        if (appliedRequestedViewIdRef.current === requestedSavedViewId || !requestedSavedView?.is_valid) return;
        appliedRequestedViewIdRef.current = requestedSavedViewId;
        if (searchParamsNameView(searchParams)) return;
        updateSearchParams(next => writeViewToSearchParams(next, requestedSavedView));
    }, [requestedSavedView, requestedSavedViewId, searchParams, updateSearchParams]);

    const header = (title: ReactNode, ready: boolean) => {
        const { modified, canMutateSelected, selectedView, statusMessage, statusIsError, unsavedConditions } = savedViewManager;
        const secondaryAction = ready && modified
            ? (canMutateSelected
                ? (
                    <Button variant="secondary" onClick={() => void savedViewManager.saveChanges()} isLoading={savedViewManager.isSaving}>
                        {t('teamwork.saveChanges')}
                    </Button>
                )
                : (
                    <Button variant="secondary" onClick={savedViewManager.openSaveAs}>
                        {t('teamwork.saveAs')}
                    </Button>
                ))
            : undefined;
        // A failed save is shown on its own line, so the Modified view notice never hides it.
        const modifiedNotice = ready && modified && (
            <p role="status" className="tasks-view-state">
                <span className="font-medium text-feedback-warning-foreground">{t('teamwork.modifiedView')}</span>
                {' · '}
                {t(selectedView ? 'tasks.modifiedViewHelp' : 'tasks.draftViewHelp')}
                {unsavedConditions && ` ${t('surfaces.savedViews.notSaved', { conditions: unsavedConditions })}`}
            </p>
        );
        const statusNote = statusMessage && (statusIsError
            ? <p role="alert" className="tasks-view-state is-error">{statusMessage}</p>
            : !modifiedNotice && <p role="status" className="tasks-view-state">{statusMessage}</p>);
        const meta = modifiedNotice || statusNote
            ? <>{modifiedNotice}{statusNote}</>
            : undefined;
        return (
            <PageHeader
                title={title}
                purpose={t('tasks.description')}
                meta={meta}
                primaryAction={(
                    <Button
                        className="tasks-primary-action"
                        onClick={() => setIsCreating(true)}
                        disabled={!ready || isCreating || !canCreateTask}
                    >
                        <Plus className="h-4 w-4" aria-hidden="true" />
                        {t('tasks.newTask')}
                    </Button>
                )}
                secondaryActions={secondaryAction}
                overflowItems={[
                    {
                        label: t('actions.import'),
                        icon: <Upload className="h-4 w-4" aria-hidden="true" />,
                        onSelect: () => setIsImporting(true),
                        disabled: !ready || selectedIterationId === 0,
                    },
                    {
                        label: t('taskFilters.textMode'),
                        icon: <FileText className="h-4 w-4" aria-hidden="true" />,
                        onSelect: () => setIsTextEditorOpen(true),
                        disabled: !ready || selectedIterationId === 0,
                    },
                    {
                        label: t('actions.enterFullScreen'),
                        icon: <Maximize2 className="h-4 w-4" aria-hidden="true" />,
                        onSelect: enterFullscreen,
                        disabled: !ready,
                    },
                ]}
            />
        );
    };

    if (iterationsLoading || iterationsError) {
        return (
            <PageLayout>
                {header(t('tasks.title'), false)}
                {iterationsLoading
                    ? <QueryLoadingState message={t('queryFeedback.loading')} />
                    : <QueryErrorState error={iterationsError} onRetry={() => void refetchIterations()} />}
            </PageLayout>
        );
    }

    const viewSwitch = <ViewSwitch<ViewMode>
        label={t('tasks.layout')}
        value={viewMode}
        onChange={changeViewMode}
        options={[
            { value: 'list', label: t('tasks.list'), icon: <List aria-hidden="true" className="h-4 w-4" /> },
            { value: 'board', label: t('tasks.board'), icon: <LayoutGrid aria-hidden="true" className="h-4 w-4" /> },
            { value: 'pipeline', label: t('tasks.pipeline'), icon: <Bot aria-hidden="true" className="h-4 w-4" /> },
        ]}
    />;

    const taskCreator = isCreateModalOpen && <GuardedTaskModal
        title={t('tasks.createNewTask')} closeLabel={t('actions.close')} onClose={closeTaskCreator}
        iterationId={isBacklogView ? null : selectedIterationId} parentProjectId={backlogProjectId}
        initialTitle={createTitle}
    />;

    if (viewMode !== 'pipeline' && (!iterations || iterations.length === 0 || isBacklogView)) {
        return <PageLayout>
            {/* Leaving the backlog changes only the scope, so it replaces this entry; Iterations is a new page. */}
            <PageHeader title={t('tasks.title')} purpose={t('teamwork.backlogHelp')}
                secondaryActions={<Link className="btn secondary" replace={iterationTasksScope !== undefined} to={iterationTasksScope ? scopeLink('/tasks', iterationTasksScope) : '/iterations'}>{t(iterations?.length ? 'teamwork.iterationTasks' : 'tasks.goToIterations')}</Link>} />
            <PageToolbar compact label={t('tasks.toolbar')} viewSwitch={viewSwitch} />
            <BacklogPanel />
            {taskCreator}
            <TaskEditorDrawer taskId={requestedTaskId} open={requestedTaskId !== null} onClose={closeFocusedTask}
                title={task => task?.title ?? t('taskEditor.editTask')} />
        </PageLayout>;
    }

    const viewName = savedViewManager.selectedView
        ? savedViewDisplay(savedViewManager.selectedView).name
        : t('tasks.allTasks');
    const viewNotice = requestedSavedViewLoadFailed
        ? { title: t('tasks.savedViewsLoadFailed'), body: t('tasks.savedViewsLoadFailedBody') }
        : requestedSavedViewMissing
            ? { title: t('tasks.savedViewUnavailable'), body: t('tasks.savedViewUnavailableBody') }
            : null;

    return (
        <PageLayout variant="workbench" className="wc-workbench-flush tasks-workbench">
            <div className="tasks-workbench-shell flex-1 min-w-0 flex flex-col h-full overflow-hidden">
                <PlanReturnBar />
                <OverviewTaskReturnBar
                    active={isFromOverview}
                    taskId={returnTaskId}
                    taskTitle={focusedTaskQuery.data?.title}
                    returnActionRef={overviewReturnActionRef}
                />
                <div className="tasks-workbench-header-wrap flex-shrink-0">
                    {header(<SavedViewPicker manager={savedViewManager} label={viewName} />, true)}
                </div>

                <div ref={toolbarRef} className="tasks-toolbar-wrap flex-shrink-0">
                    <PageToolbar
                        compact
                        label={t('tasks.toolbar')}
                        search={(
                            <div className="relative">
                                <Search aria-hidden="true" className="pointer-events-none absolute left-3 top-1/2 z-10 h-4 w-4 -translate-y-1/2 text-content-tertiary" />
                                <Input
                                    type="search"
                                    aria-label={t('tasks.searchList')}
                                    placeholder={t('tasks.searchPlaceholder')}
                                    value={searchText}
                                    maxLength={200}
                                    onChange={event => changeSearch(event.target.value)}
                                    className="pl-9"
                                />
                            </div>
                        )}
                        filters={(
                            <TaskFiltersBar
                                iterationId={selectedIterationId}
                                filters={filters}
                                onFiltersChange={changeFilters}
                                agentFilter={viewMode === 'pipeline' ? { value: agentFilter, options: pipelineQuery.agents, onChange: value => setTaskContextParam('agent', value || null) } : undefined}
                                hideProject={viewMode === 'pipeline'}
                                onClear={viewMode === 'pipeline' ? () => updateSearchParams(next => {
                                    writeClearedViewMarker(writeFiltersToSearchParams(next, defaultFilters), next.has(VIEW_PARAM));
                                    next.delete('agent');
                                }) : undefined}
                            />
                        )}
                        viewSwitch={viewSwitch}
                        viewOptions={viewMode === 'list' ? (
                            <TaskViewOptions
                                sortKey={sortKey}
                                onSortKeyChange={changeSortKey}
                                groupByStatus={groupByStatus}
                                onGroupByStatusChange={changeGrouping}
                            />
                        ) : undefined}
                    />
                    {viewMode === 'pipeline' && <p className="px-4 py-2 text-xs text-content-secondary">{t('agentPipeline.runLogsNeedKey')}</p>}
                    {requestedSavedViewId && savedViewsLoading && (
                        <p role="status" className="tasks-view-notice">{t('tasks.loadingSavedView')}</p>
                    )}
                    {viewNotice && (
                        <div role="status" className="tasks-view-notice is-warning">
                            <AlertTriangle className="h-4 w-4 shrink-0" aria-hidden="true" />
                            <span className="min-w-0 flex-1">
                                <strong className="font-medium">{viewNotice.title}</strong>
                                {' · '}
                                {viewNotice.body}
                            </span>
                            <Button variant="ghost" size="sm" onClick={clearViewContext}>
                                <X className="mr-1 h-4 w-4" aria-hidden="true" />
                                {t('tasks.clearView')}
                            </Button>
                        </div>
                    )}
                </div>

                <TaskEditorDrawer
                    beforeForm={viewMode === 'pipeline' ? task => task ? <PipelineTaskEvidence key={`${task.id}:${task.version}`} task={task} /> : null : undefined}
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

                {(selectedIterationId > 0 || viewMode === 'pipeline') && (
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
                                        {viewMode === 'pipeline' ? t('tasks.pipeline') : viewMode === 'board' ? t('tasks.boardView') : t('tasks.taskList')}
                                    </h2>
                                    <p className="text-content-secondary text-sm">{t('tasks.focusMode')}</p>
                                </div>
                                <Button variant="ghost" onClick={exitFullscreen}>
                                    <Minimize2 className="w-5 h-5 mr-2" /> {t('actions.exitFullScreen')}
                                </Button>
                            </div>
                        )}

                        {viewMode === 'list' && (
                            <div className="h-full overflow-y-auto">
                                <div className={clsx(
                                    'tasks-list-content',
                                    isFullScreen ? 'p-6' : 'px-4 pb-6',
                                )}>
                                    <TaskList
                                        iterationId={selectedIterationId}
                                        filters={filters}
                                        sortKey={sortKey}
                                        groupByStatus={groupByStatus}
                                        leadingRow={(
                                            <QuickCapture listRow target={{ kind: 'task', iterationId: selectedIterationId }}
                                                onExpand={title => { setCreateTitle(title); setIsCreating(true); }} />
                                        )}
                                        hasActiveFilters={activeFilterCount > 0 || searchText !== ''}
                                        activeViewName={savedViewManager.selectedView ? viewName : undefined}
                                        onClearFilters={clearListConditions}
                                        onCreateTask={() => setIsCreating(true)}
                                        requestedMode={taskMode}
                                        onModeChange={mode => setTaskContextParam('mode', mode)}
                                        preselectAllInBulk={taskMode === 'bulk' && filters.planningIssue === 'unassigned'}
                                        onOpenTask={openTask}
                                    />
                                </div>
                            </div>
                        )}
                        {viewMode === 'board' && (
                            <div className="h-full overflow-hidden">
                                <KanbanBoard iterationId={selectedIterationId} filters={filters} />
                            </div>
                        )}
                        {viewMode === 'pipeline' && (
                            <div className="h-full overflow-y-auto px-4 pb-6">
                                <PipelineView query={pipelineQuery} project={project} iteration={iteration}
                                    search={searchText} agent={agentFilter} filters={filters} labelGroups={pipelineLabelGroups}
                                    onOpenTask={openTask} />
                            </div>
                        )}
                    </FullscreenWorkspace>
                )}
            </div>

            {savedViewManager.dialogs}

            {taskCreator}

            {isImporting && (
                <ImportTasksModal
                    iterationId={selectedIterationId}
                    onClose={() => setIsImporting(false)}
                />
            )}

            {isTextEditorOpen && (
                <TaskTextEditorModal
                    iterationId={selectedIterationId}
                    onClose={() => setIsTextEditorOpen(false)}
                />
            )}
        </PageLayout>
    );
};

export default TasksPage;

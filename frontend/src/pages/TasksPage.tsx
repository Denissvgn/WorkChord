import { useCallback, useState, useEffect } from 'react';
import { useQuery } from '@tanstack/react-query';
import { useSearchParams } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { Plus, Upload, LayoutGrid, List, ListFilter, Maximize2, Minimize2 } from 'lucide-react';
import { motion } from 'framer-motion';
import { Button } from '../components/common/Button';
import { Modal } from '../components/common/Modal';
import { FullscreenWorkspace } from '../components/common/FullscreenWorkspace';
import { QueryErrorState, QueryLoadingState } from '../components/feedback/QueryState';
import { TaskList } from '../components/tasks/TaskList';
import { KanbanBoard } from '../components/tasks/KanbanBoard/KanbanBoard';
import { TaskForm } from '../components/tasks/TaskForm';
import { ImportTasksModal } from '../components/tasks/ImportTasksModal';
import { TaskFiltersBar } from '../components/tasks/TaskFiltersBar';
import type { TaskFilters } from '../components/tasks/TaskFiltersBar';
import { SavedViewsControl } from '../components/tasks/SavedViewsControl';
import type { SortKey } from '../components/tasks/TaskList';
import { defaultFilters } from '../utils/taskFilterDefaults';
import { iterationService } from '../services/iterationService';
import { useIterationStore } from '../store/iterationStore';
import { IterationSelector } from '../components/iteration/IterationSelector';
import { OverflowMenu, PageHeader, PageLayout, SlideOverDrawer } from '../components/ui';
import type { SavedView } from '../types/savedView';
import clsx from 'clsx';

type ViewMode = 'list' | 'board';
const SORT_KEYS: SortKey[] = ['priority', 'sort_order', 'status', 'title'];

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
    const requestedSavedViewId = Number(searchParams.get('view')) || null;
    const createTaskRequested = searchParams.get('create') === '1';
    const isCreateModalOpen = isCreating || (createTaskRequested && selectedIterationId > 0);
    const { t } = useTranslation();
    const activeFilterCount =
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

    const { data: iterations, isLoading: iterationsLoading, error: iterationsError, refetch: refetchIterations } = useQuery({
        queryKey: ['iterations'],
        queryFn: iterationService.getAll,
    });

    useEffect(() => {
        if (iterations && iterations.length > 0) {
            // Reset to first iteration if selected iteration doesn't exist
            const iterationExists = iterations.some(i => i.id === selectedIterationId);
            if (selectedIterationId === 0 || !iterationExists) {
                setSelectedIterationId(iterations[0].id);
            }
        }
    }, [iterations, selectedIterationId, setSelectedIterationId]);

    const closeTaskCreator = useCallback(() => {
        setIsCreating(false);
        if (!createTaskRequested) return;

        const nextSearchParams = new URLSearchParams(searchParams);
        nextSearchParams.delete('create');
        setSearchParams(nextSearchParams, { replace: true });
    }, [createTaskRequested, searchParams, setSearchParams]);

    const applySavedView = useCallback((view: SavedView) => {
        setFilters(filtersFromSavedView(view));
        const savedSortKey = sortKeyFromSavedView(view);
        if (savedSortKey) {
            setSortKey(savedSortKey);
        }
    }, []);

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
                    actions={<a href="/iterations" className="btn primary">{t('tasks.goToIterations')}</a>}
                />
                <div className="empty">
                    <h4>{t('tasks.noIterationsTitle')}</h4>
                    <p>{t('tasks.noIterationsBody')}</p>
                </div>
            </PageLayout>
        );
    }

    return (
        <PageLayout variant="workbench" className="wc-workbench-flush">
            {/* Main Content Area */}
            <div className="flex-1 min-w-0 flex flex-col h-full overflow-hidden">
                <div className="flex-shrink-0 px-4 pt-4 pb-3">
                    <div className="wc-page-head" data-testid="page-header" style={{marginBottom:0}}>
                        <div>
                            <h1 className="wc-page-title">{t('tasks.title')}</h1>
                            <div className="wc-page-sub">{t('tasks.description')}</div>
                        </div>
                        <div className="row" style={{flexWrap:'wrap', gap:6}}>
                        <IterationSelector
                            onChange={() => {
                                setFilters(defaultFilters);
                                setSortKey('priority');
                                setSelectedSavedViewId(null);
                            }}
                        />
                        <Button
                            variant={activeFilterCount > 0 ? 'secondary' : 'outline'}
                            onClick={() => setIsFiltersOpen(true)}
                            aria-expanded={isFiltersOpen}
                        >
                            <ListFilter className="w-4 h-4 mr-2" />
                            {t('taskFilters.filters')}
                            {activeFilterCount > 0 && (
                                <span className="ml-1 rounded-full bg-surface-card/80 px-1.5 py-0.5 text-xs tabular-nums">
                                    {activeFilterCount}
                                </span>
                            )}
                        </Button>
                        <OverflowMenu
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
                                    onSelect: () => setIsFullScreen(true),
                                },
                            ]}
                        />
                        <Button onClick={() => setIsCreating(true)} disabled={isCreating || selectedIterationId === 0}>
                            <Plus className="w-4 h-4 mr-2" />
                            {t('tasks.newTask')}
                        </Button>
                        </div>
                    </div>
                </div>

                {selectedIterationId > 0 && (
                    <div className="flex-shrink-0 px-6 pb-3">
                        <div className="flex w-fit bg-surface-subtle p-1 rounded-lg" role="group" aria-label={t('tasks.title')}>
                            <button
                                type="button"
                                onClick={() => setViewMode('list')}
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
                                        transition={{ type: "spring", bounce: 0.2, duration: 0.6 }}
                                    />
                                )}
                                <span className="relative z-10 flex items-center gap-2">
                                    <List className="w-4 h-4" />
                                    {t('tasks.list')}
                                </span>
                            </button>
                            <button
                                type="button"
                                onClick={() => setViewMode('board')}
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
                                        transition={{ type: "spring", bounce: 0.2, duration: 0.6 }}
                                    />
                                )}
                                <span className="relative z-10 flex items-center gap-2">
                                    <LayoutGrid className="w-4 h-4" />
                                    {t('tasks.board')}
                                </span>
                            </button>
                        </div>
                    </div>
                )}

                <div hidden>
                    <SavedViewsControl
                        filters={filters}
                        sortKey={sortKey}
                        selectedViewId={selectedSavedViewId}
                        requestedViewId={requestedSavedViewId}
                        onSelectedViewIdChange={setSelectedSavedViewId}
                        onApplyView={applySavedView}
                    />
                </div>

                <SlideOverDrawer
                    open={isFiltersOpen}
                    title={t('taskFilters.filters')}
                    icon={<ListFilter className="h-4 w-4" aria-hidden="true" />}
                    onClose={() => setIsFiltersOpen(false)}
                >
                    {selectedIterationId > 0 && (
                        <>
                            <TaskFiltersBar
                                iterationId={selectedIterationId}
                                filters={filters}
                                onFiltersChange={setFilters}
                            />
                            <section className="border-t border-border px-4 py-4">
                                <h2 className="mb-3 text-sm font-semibold text-content-primary">{t('surfaces.savedViews.savedViews')}</h2>
                                <SavedViewsControl
                                    filters={filters}
                                    sortKey={sortKey}
                                    selectedViewId={selectedSavedViewId}
                                    onSelectedViewIdChange={setSelectedSavedViewId}
                                    onApplyView={applySavedView}
                                />
                            </section>
                        </>
                    )}
                </SlideOverDrawer>

                {selectedIterationId > 0 && (
                    <FullscreenWorkspace
                        open={isFullScreen}
                        onClose={() => setIsFullScreen(false)}
                        ariaLabel={t('tasks.fullScreenLabel')}
                        className="flex-1 overflow-hidden relative"
                    >
                        {isFullScreen && (
                            <div className="flex justify-between items-center px-6 py-4 flex-shrink-0 border-b border-border-subtle">
                                <div>
                                    <h2 className="text-2xl font-bold text-content-primary">
                                        {viewMode === 'list' ? t('tasks.taskList') : t('tasks.boardView')}
                                    </h2>
                                    <p className="text-content-secondary text-sm">{t('tasks.focusMode')}</p>
                                </div>
                                <Button variant="ghost" onClick={() => setIsFullScreen(false)}>
                                    <Minimize2 className="w-5 h-5 mr-2" /> {t('actions.exitFullScreen')}
                                </Button>
                            </div>
                        )}

                        {viewMode === 'list' ? (
                            <div className="h-full overflow-y-auto">
                                <div className={clsx(isFullScreen ? "p-6" : "px-6 pb-6")}>
                                    <TaskList
                                        iterationId={selectedIterationId}
                                        filters={filters}
                                        sortKey={sortKey}
                                        onSortKeyChange={setSortKey}
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

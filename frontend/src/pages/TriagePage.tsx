import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import clsx from 'clsx';
import {
    AlertCircle,
    CheckCircle2,
    ExternalLink,
    Plus,
    X
} from 'lucide-react';
import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import { useTranslation } from 'react-i18next';
import { Link, useSearchParams } from 'react-router-dom';
import { Button } from '../components/common/Button';
import { QueryErrorState } from '../components/feedback/QueryState';
import { PageHeader, PageLayout } from '../components/ui';
import { firstRunPlanHref } from '../features/firstRun/firstRunSteps';
import type { MutationFeedbackMeta } from '../features/mutationFeedback';
import { feedbackMessage } from '../features/mutationFeedback';
import { useScopeLink } from '../features/scope/useScopeLink';
import { iterationService } from '../services/iterationService';
import { projectService } from '../services/projectService';
import { savedViewService } from '../services/savedViewService';
import { triageService } from '../services/triageService';
import { useIterationStore } from '../store/iterationStore';
import type {
    TriageActionRequest,
    TriageConvertToTaskRequest,
    TriageConvertToTaskResponse,
    TriageDuplicateRequest,
    TriageDuplicateSuggestion,
    TriageItem,
    TriageItemCreate,
    TriageItemStatus,
    TriageListParams,
    TriageSnoozeRequest
} from '../types/triage';

import { ConvertTriageDrawer } from '../components/triage/ConvertTriageDrawer';
import { CreateTriageDrawer } from '../components/triage/CreateTriageDrawer';
import { TriageActionModal } from '../components/triage/TriageActionModal';
import { TriageDetailPanel } from '../components/triage/TriageDetailPanel';
import { TriageList } from '../components/triage/TriageList';
import { TriageToolbar } from '../components/triage/TriageToolbar';
import { AGENT_SOURCE_LABEL_KEYS, getErrorMessage, getSourceLinkError, isDueSnoozed, makeLookup, toLocalDateTimeInputValue, triageFiltersFromSavedView, type DuplicateActionDefaults, type TriageLifecycleAction } from '../components/triage/triageUtils';
type ActionMutationInput =
    | { type: 'accept'; itemId: number; payload: TriageActionRequest }
    | { type: 'decline'; itemId: number; payload: TriageActionRequest }
    | { type: 'snooze'; itemId: number; payload: TriageSnoozeRequest }
    | { type: 'duplicate'; itemId: number; payload: TriageDuplicateRequest };

interface ConvertMutationInput {
    itemId: number;
    payload: TriageConvertToTaskRequest;
}

const TriagePage = () => {
    const { t } = useTranslation();
    const scopeLink = useScopeLink();
    const queryClient = useQueryClient();
    const [searchParams, setSearchParams] = useSearchParams();
    const { selectedIterationId } = useIterationStore();
    const [search, setSearch] = useState('');
    const [sourceFilter, setSourceFilter] = useState('');
    const [statusFilter, setStatusFilter] = useState<TriageItemStatus | ''>('');
    const [activeOnly, setActiveOnly] = useState(true);
    const [labelFilter, setLabelFilter] = useState('');
    const [selectedId, setSelectedId] = useState<number | null>(null);
    const [isCreating, setIsCreating] = useState(false);
    const [actionState, setActionState] = useState<{
        action: TriageLifecycleAction;
        item: TriageItem;
        defaultSnooze: string;
        defaultDuplicate?: DuplicateActionDefaults;
    } | null>(null);
    const [convertItem, setConvertItem] = useState<TriageItem | null>(null);
    const [conversionResult, setConversionResult] = useState<{ taskId: number; taskTitle: string; sourceLinkNote?: string | null } | null>(null);
    const requestedSavedViewId = Number(searchParams.get('view')) || null;
    const appliedSavedViewIdRef = useRef<number | null>(null);

    const { data: requestedSavedView, error: savedViewError, refetch: refetchSavedView } = useQuery({
        queryKey: ['saved-view', requestedSavedViewId],
        queryFn: () => savedViewService.getById(requestedSavedViewId as number),
        enabled: Boolean(requestedSavedViewId),
    });

    const clearRequestedViewParam = useCallback(() => {
        if (!searchParams.has('view')) return;
        const nextParams = new URLSearchParams(searchParams);
        nextParams.delete('view');
        appliedSavedViewIdRef.current = null;
        setSearchParams(nextParams, { replace: true });
    }, [searchParams, setSearchParams]);

    useEffect(() => {
        if (
            !requestedSavedViewId ||
            !requestedSavedView ||
            appliedSavedViewIdRef.current === requestedSavedViewId ||
            requestedSavedView.view_type !== 'triage' ||
            !requestedSavedView.is_valid
        ) {
            return;
        }

        appliedSavedViewIdRef.current = requestedSavedViewId;
        const filters = triageFiltersFromSavedView(requestedSavedView);
        const timeoutId = window.setTimeout(() => {
            setActiveOnly(filters.active);
            setStatusFilter(filters.status);
            setSearch(filters.q);
            setSourceFilter(filters.source);
            setLabelFilter('');
        }, 0);

        return () => window.clearTimeout(timeoutId);
    }, [requestedSavedView, requestedSavedViewId]);

    const activeSavedView = requestedSavedViewId !== null && requestedSavedView?.view_type === 'triage'
        ? requestedSavedView
        : null;

    const triageFilters = useMemo<TriageListParams>(() => {
        const filters: TriageListParams = { active: activeOnly, limit: 100 };
        if (statusFilter) filters.statuses = [statusFilter];
        if (search.trim()) filters.q = search.trim();
        if (sourceFilter) filters.source = sourceFilter;
        return filters;
    }, [activeOnly, search, sourceFilter, statusFilter]);

    const { data: triageItems = [], isLoading, error: listError, refetch: refetchTriageItems } = useQuery({
        queryKey: ['triage', triageFilters],
        queryFn: () => triageService.getAll(triageFilters),
    });

    const { data: allTriageItems = [], error: allTriageError, refetch: refetchAllTriage } = useQuery({
        queryKey: ['triage', 'all'],
        queryFn: () => triageService.getAll({ active: false, limit: 500 }),
    });

    const { data: iterations = [], error: iterationsError, refetch: refetchIterations } = useQuery({
        queryKey: ['iterations'],
        queryFn: iterationService.getAll,
    });
    const hasPlannableIterations = iterations.length > 0;

    const { data: projects = [], error: projectsError, refetch: refetchProjects } = useQuery({
        queryKey: ['projects'],
        queryFn: projectService.getAll,
    });

    const projectsById = useMemo(() => makeLookup(projects), [projects]);
    const iterationsById = useMemo(() => makeLookup(iterations), [iterations]);
    const visibleItems = useMemo(() => labelFilter ? triageItems.filter(item => item.labels.includes(labelFilter)) : triageItems, [triageItems, labelFilter]);
    const selectedItem = useMemo(() => visibleItems.find(item => item.id === selectedId) ?? visibleItems[0] ?? null, [selectedId, visibleItems]);
    const effectiveSelectedId = selectedItem?.id ?? null;
    const sources = useMemo(() => Array.from(new Set([
        ...Object.keys(AGENT_SOURCE_LABEL_KEYS),
        ...allTriageItems.map(item => item.source).filter((source): source is string => Boolean(source)),
    ])).sort(), [allTriageItems]);

    const dueSnoozedCount = useMemo(
        () => allTriageItems.filter(isDueSnoozed).length,
        [allTriageItems],
    );
    const activeFilterCount =
        Number(Boolean(search.trim())) +
        Number(Boolean(sourceFilter)) +
        Number(Boolean(statusFilter)) +
        Number(Boolean(labelFilter)) +
        Number(!activeOnly);
    const resetFilters = () => {
        clearRequestedViewParam();
        setSearch('');
        setSourceFilter('');
        setStatusFilter('');
        setLabelFilter('');
        setActiveOnly(true);
    };
    const [createTitle, setCreateTitle] = useState('');
    const startNewIntake = (title = '') => {
        createMutation.reset();
        setCreateTitle(title);
        setIsCreating(true);
    };

    const invalidateTriageQueries = () => {
        queryClient.invalidateQueries({ queryKey: ['triage'] });
    };

    const invalidateTaskProjectQueries = (iterationId: number | null, projectId?: number | null) => {
        invalidateTriageQueries();
        queryClient.invalidateQueries({ queryKey: ['tasks', iterationId] });
        queryClient.invalidateQueries({ queryKey: ['tasks'] });
        queryClient.invalidateQueries({ queryKey: ['workload'] });
        queryClient.invalidateQueries({ queryKey: ['gantt', iterationId] });
        queryClient.invalidateQueries({ queryKey: ['gantt'] });
        queryClient.invalidateQueries({ queryKey: ['projects'] });
        if (projectId) {
            queryClient.invalidateQueries({ queryKey: ['projectSummary', projectId] });
            queryClient.invalidateQueries({ queryKey: ['projectTasks', projectId] });
        } else {
            queryClient.invalidateQueries({ queryKey: ['projectSummary'] });
            queryClient.invalidateQueries({ queryKey: ['projectTasks'] });
        }
    };

    const createMutation = useMutation({
        mutationFn: (payload: TriageItemCreate) => triageService.create(payload),
        meta: { success: data => feedbackMessage(t, 'created', 'triageItem', (data as TriageItem).title) } satisfies MutationFeedbackMeta,
        onSuccess: item => {
            setIsCreating(false);
            setSelectedId(item.id);
            invalidateTriageQueries();
        },
    });

    const actionMutation = useMutation<TriageItem, unknown, ActionMutationInput>({
        meta: { success: (data, variables) => t(`feedback.triage_${(variables as ActionMutationInput).type}`, { name: (data as TriageItem).title }) } satisfies MutationFeedbackMeta,
        mutationFn: input => {
            switch (input.type) {
                case 'accept':
                    return triageService.accept(input.itemId, input.payload);
                case 'decline':
                    return triageService.decline(input.itemId, input.payload);
                case 'snooze':
                    return triageService.snooze(input.itemId, input.payload);
                case 'duplicate':
                    return triageService.markDuplicate(input.itemId, input.payload);
            }
        },
        onSuccess: (item, variables) => {
            setActionState(null);
            setSelectedId(item.id);
            invalidateTriageQueries();
            if (variables.type === 'duplicate' && variables.payload.duplicate_task_id) {
                queryClient.invalidateQueries({ queryKey: ['tasks'] });
                queryClient.invalidateQueries({ queryKey: ['projectSummary'] });
                queryClient.invalidateQueries({ queryKey: ['projectTasks'] });
                queryClient.invalidateQueries({ queryKey: ['request-source-links'] });
            }
        },
    });

    const convertMutation = useMutation<TriageConvertToTaskResponse, unknown, ConvertMutationInput>({
        mutationFn: input => triageService.convertToTask(input.itemId, input.payload),
        meta: { success: data => t('feedback.triageConverted', { name: (data as TriageConvertToTaskResponse).task.title }) } satisfies MutationFeedbackMeta,
        onSuccess: (response, variables) => {
            setConvertItem(null);
            setConversionResult({ taskId: response.task.id, taskTitle: response.task.title, sourceLinkNote: response.source_link?.message ?? null });
            setSelectedId(response.triage_item.id);
            invalidateTaskProjectQueries(variables.payload.iteration_id, variables.payload.project_id);
        },
    });

    const openAction = (
        action: TriageLifecycleAction,
        item: TriageItem,
        defaultDuplicate?: DuplicateActionDefaults,
    ) => {
        actionMutation.reset();
        setActionState({
            action,
            item,
            defaultSnooze: toLocalDateTimeInputValue(new Date(Date.now() + 24 * 60 * 60 * 1000)),
            defaultDuplicate,
        });
    };

    const openSuggestedDuplicate = (item: TriageItem, suggestion: TriageDuplicateSuggestion) => {
        openAction('duplicate', item, {
            targetType: suggestion.target_type === 'task' ? 'task' : 'triage',
            targetId: suggestion.target_id,
            title: suggestion.title,
            iterationId: suggestion.iteration_id,
        });
    };

    const openConvert = (item: TriageItem) => {
        if (!hasPlannableIterations) return;
        convertMutation.reset();
        setConvertItem(item);
    };

    const handleActionSubmit = (payload: TriageActionRequest | TriageSnoozeRequest | TriageDuplicateRequest) => {
        if (!actionState) return;
        if (actionState.action === 'accept' || actionState.action === 'decline') {
            actionMutation.mutate({
                type: actionState.action,
                itemId: actionState.item.id,
                payload: payload as TriageActionRequest,
            });
            return;
        }
        if (actionState.action === 'snooze' || actionState.action === 'clarify') {
            // Asking for clarification snoozes the item until the stated review
            // time, with the question as its reason, as the PM skill does.
            actionMutation.mutate({
                type: 'snooze',
                itemId: actionState.item.id,
                payload: payload as TriageSnoozeRequest,
            });
            return;
        }
        actionMutation.mutate({
            type: 'duplicate',
            itemId: actionState.item.id,
            payload: payload as TriageDuplicateRequest,
        });
    };

    const listErrorMessage = listError ? getErrorMessage(listError, t('surfaces.triagePage.loadFailed')) : null;
    const createSourceLinkError = createMutation.error ? getSourceLinkError(createMutation.error) : null;
    const createErrorMessage = createMutation.error && !createSourceLinkError ? getErrorMessage(createMutation.error, t('surfaces.triagePage.createFailed')) : null;
    const actionErrorMessage = actionMutation.error ? getErrorMessage(actionMutation.error, t('surfaces.triagePage.updateFailed')) : null;
    const convertErrorMessage = convertMutation.error ? getErrorMessage(convertMutation.error, t('surfaces.triagePage.convertFailed')) : null;
    const supportingQueryError = savedViewError ?? allTriageError ?? iterationsError ?? projectsError;

    return (
        <PageLayout variant="workbench">
            <PageHeader
                title={t('surfaces.triagePage.triageIntake')}
                purpose={t('surfaces.triagePage.reviewRawIntakeAndConvertAcceptedWorkIntoPlannedTasks')}
                primaryAction={(
                    <Button onClick={() => startNewIntake()}>
                        <Plus className="h-4 w-4" aria-hidden="true" />
                        {t('surfaces.triagePage.newIntake')}
                    </Button>
                )}
            />

            {dueSnoozedCount > 0 && (
                <div className="flex shrink-0 items-center gap-3 rounded-lg border border-feedback-warning-border bg-feedback-warning-muted px-4 py-3 text-sm text-feedback-warning-foreground">
                    <AlertCircle className="h-4 w-4 shrink-0" aria-hidden="true" />
                    <span className="font-medium tabular-nums">{dueSnoozedCount} {t('surfaces.triagePage.dueSnoozed')}</span>
                </div>
            )}

            {/* Conversion success banner */}
            {conversionResult && (
                <div className="flex items-center justify-between rounded-lg border border-feedback-success-border bg-feedback-success-muted p-3 text-sm text-feedback-success-foreground">
                    <div className="flex items-center gap-2">
                        <CheckCircle2 className="h-4 w-4" />
                        <span>{t('quickActions.taskCreated')}</span>
                        {conversionResult.sourceLinkNote && <span role="status">{conversionResult.sourceLinkNote}</span>}
                    </div>
                    <div className="flex items-center gap-2">
                        <Link
                            to={scopeLink(`/tasks?highlight=${conversionResult.taskId}`)}
                            className="inline-flex items-center gap-1 font-medium text-feedback-success-foreground hover:underline"
                        >
                            {t('quickActions.viewTask')} #{conversionResult.taskId}
                            <ExternalLink className="h-3 w-3" />
                        </Link>
                        <Button variant="ghost"
                            type="button"
                            onClick={() => setConversionResult(null)}
                            className="ml-2 rounded p-1 hover:bg-feedback-success-muted-hover"
                            aria-label={t('surfaces.triagePage.dismissConversionSuccess')} title={t('surfaces.triagePage.dismissConversionSuccess')}
                        >
                            <X className="h-4 w-4" aria-hidden="true" />
                        </Button>
                    </div>
                </div>
            )}

            <TriageToolbar search={search} source={sourceFilter} status={statusFilter} label={labelFilter} activeOnly={activeOnly}
                sources={sources} labels={Array.from(new Set(allTriageItems.flatMap(item => item.labels))).sort()}
                onSearch={value => { clearRequestedViewParam(); setSearch(value); }}
                onFilter={(id, value) => {
                    clearRequestedViewParam();
                    if (id === 'status') setStatusFilter(value as TriageItemStatus | '');
                    if (id === 'source') setSourceFilter(value);
                    if (id === 'label') setLabelFilter(value);
                }}
                onView={value => { clearRequestedViewParam(); setActiveOnly(value); }} onClear={resetFilters} />
            {activeSavedView && <p className="text-sm text-content-secondary">{t('surfaces.projectsPage.savedView')}: {activeSavedView.name}</p>}
            {supportingQueryError && <QueryErrorState error={supportingQueryError} fallback={t('queryFeedback.optionLoadFailed')}
                onRetry={() => { void refetchSavedView(); void refetchAllTriage(); void refetchIterations(); void refetchProjects(); }} />}

            {/* Conversion needs an iteration only once there is a request to convert; an empty page offers one step. */}
            {!hasPlannableIterations && visibleItems.length > 0 && (
                <div className="flex flex-wrap items-center justify-between gap-3 rounded-lg border border-feedback-warning-border bg-feedback-warning-muted px-4 py-3 text-sm text-feedback-warning-foreground">
                    <div className="flex min-w-0 items-start gap-2">
                        <AlertCircle className="mt-0.5 h-4 w-4 shrink-0" />
                        <div>
                            <p className="font-medium">{t('surfaces.triagePage.conversionRequiresAnIteration')}</p>
                            <p className="mt-0.5 text-feedback-warning-foreground">{t('surfaces.triagePage.intakeCanStayInTriageUntilPlanningCreatesARealTargetIteration')}</p>
                        </div>
                    </div>
                    <Link
                        to={firstRunPlanHref('iteration')}
                        className="inline-flex items-center rounded-md border border-feedback-warning-border bg-surface-card px-3 py-1.5 font-medium text-feedback-warning-foreground hover:bg-feedback-warning-muted-hover"
                    >
                        {t('surfaces.triagePage.createIteration')}
                    </Link>
                </div>
            )}

            <div className={clsx('grid min-h-0 flex-1 grid-cols-1 gap-4 overflow-y-auto lg:overflow-hidden', (visibleItems.length > 0 || selectedItem) && 'lg:grid-cols-[minmax(0,1fr)_360px] xl:grid-cols-[minmax(0,1fr)_420px]')}>
                <TriageList items={visibleItems} selectedId={effectiveSelectedId} projectsById={projectsById} iterationsById={iterationsById}
                    listErrorMessage={listErrorMessage} isLoading={isLoading} activeFilterCount={activeFilterCount}
                    onRetry={() => void refetchTriageItems()} onSelect={setSelectedId} onCreate={startNewIntake} onReset={resetFilters} />

                {(visibleItems.length > 0 || selectedItem) && <div className="min-h-[420px] lg:min-h-0">
                    <TriageDetailPanel
                        item={selectedItem}
                        projectsById={projectsById}
                        iterationsById={iterationsById}
                        canConvert={hasPlannableIterations}
                        onAction={openAction}
                        onMarkSuggestion={openSuggestedDuplicate}
                        onConvert={openConvert}
                        onRequestLinksChanged={invalidateTriageQueries}
                    />
                </div>}
            </div>

            {convertItem && hasPlannableIterations && <ConvertTriageDrawer
                key={`${convertItem.id}-${convertItem.iteration_hint_id || 0}-${iterations.length}-${selectedIterationId}`}
                item={convertItem} projects={projects} iterations={iterations} selectedIterationId={selectedIterationId}
                isSubmitting={convertMutation.isPending} error={convertErrorMessage}
                onSubmit={payload => convertMutation.mutate({ itemId: convertItem.id, payload })} onClose={() => setConvertItem(null)} />}
            {isCreating && (
                <CreateTriageDrawer
                    projects={projects}
                    iterations={iterations}
                    isSubmitting={createMutation.isPending}
                    error={createErrorMessage}
                    sourceUrlError={createSourceLinkError}
                    onSubmit={payload => createMutation.mutate(payload)}
                    onClose={() => setIsCreating(false)}
                    initialTitle={createTitle}
                />
            )}

            {actionState && (
                <TriageActionModal
                    key={`${actionState.action}-${actionState.item.id}-${actionState.defaultSnooze}-${actionState.defaultDuplicate?.targetType || 'none'}-${actionState.defaultDuplicate?.targetId || 0}`}
                    action={actionState.action}
                    item={actionState.item}
                    allTriageItems={allTriageItems}
                    iterations={iterations}
                    selectedIterationId={selectedIterationId}
                    defaultSnooze={actionState.defaultSnooze}
                    defaultDuplicate={actionState.defaultDuplicate}
                    isSubmitting={actionMutation.isPending}
                    error={actionErrorMessage}
                    onSubmit={handleActionSubmit}
                    onClose={() => setActionState(null)}
                />
            )}
        </PageLayout>
    );
};

export default TriagePage;

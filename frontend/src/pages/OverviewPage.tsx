import { useEffect, useMemo, useRef, useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useQueries, useQuery } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import {
    AlertTriangle,
    ArrowRight,
    Bot,
    CheckCircle2,
    Clock,
    ClipboardCheck,
    HelpCircle,
    ListTodo,
    Plus,
    RefreshCw,
    Target,
    User,
    UserPlus,
} from 'lucide-react';
import type { LucideIcon } from 'lucide-react';
import { formatDate } from '../utils/formatDate';
import { formatDecimal } from '../utils/workNumbers';
import { getApiErrorStatus } from '../utils/apiError';
import { taskService } from '../services/taskService';
import { iterationService } from '../services/iterationService';
import { QueryErrorState, QueryLoadingState, QueryStaleState } from '../components/feedback/QueryState';
import { PageHeader, PageLayout, SectionCard, SlideOverDrawer } from '../components/ui';
import type { PillTone } from '../components/ui/tone';
import { STATUS_TONE, toneSoftVar, toneVar } from '../components/ui/tone';
import { usePipeline } from '../components/tasks/usePipeline';
import type { Iteration } from '../types/iteration';
import type { Task } from '../types/task';
import { useWorkScope } from '../features/scope/useWorkScope';
import { useScopeLink } from '../features/scope/useScopeLink';
import type { ScopeIteration, ScopeProject } from '../features/scope/workScope';
import {
    planProgress,
    planningNavigationSummaryKey,
    usePlanningNavigationSummary,
} from '../features/planningMasters/usePlanningNavigationSummary';
import { isPlanningStepId } from '../features/planningMasters/planningReturn';
import {
    overviewTaskDrawerHref,
    overviewTaskReturnFocusId,
} from '../features/overview/overviewTaskThread';
import { loadProjectBacklog } from '../features/overview/overviewBacklog';
import { GetStartedPanel } from '../features/firstRun/GetStartedPanel';
import { NextStepEmptyState } from '../features/firstRun/NextStepEmptyState';
import { firstRunPlanHref } from '../features/firstRun/firstRunSteps';
import { useGetStarted } from '../features/firstRun/useGetStarted';
import {
    OVERVIEW_COUNT_LIST_PARAM,
    PIPELINE_STAGES,
    backlogRoots,
    daysLeftToLatestEnd,
    deliveryRisk,
    iterationsInView,
    listTasks,
    overviewCountListHref,
    parseOverviewCountList,
    pickAttention,
    pipelineStageHref,
    pipelineTasksInScope,
    selectWorkNow,
    taskListHref,
    type AttentionCandidate,
    type AttentionKind,
    type OverviewCountList,
    type PipelineStage,
} from '../features/overview/overviewSignals';

type OverviewLocationState = {
    returnFocusId?: string;
};

/**
 * Whether a source Overview needs has arrived. 'stale' means a refresh failed and the last
 * loaded result is shown; 'unavailable' means this person cannot read the source at all.
 */
type SourceState = 'loading' | 'failed' | 'stale' | 'ready' | 'unavailable';

type AttentionSource = 'tasks' | 'pipeline' | 'plan';

/** True when the source has a result to show, current or the last one loaded. */
const hasResult = (state: SourceState) => state === 'ready' || state === 'stale';

const queryState = (query: { data: unknown; isError: boolean }): SourceState => {
    if (query.data !== undefined) return query.isError ? 'stale' : 'ready';
    return query.isError ? 'failed' : 'loading';
};

/** The tasks Overview counts: one group per iteration in view, or the project's backlog. */
type TaskGroup = { iteration: Iteration | null; roots: Task[] };

/** A task in one of Overview's own lists, with the iteration it belongs to. */
type ListedTask = { task: Task; iteration: Iteration | null };

const ATTENTION_ID = 'overview-attention-title';
const WORK_NOW_TITLE_ID = 'overview-work-now-title';
const AGENTS_NOW_TITLE_ID = 'overview-agents-now-title';
const ON_TRACK_TITLE_ID = 'overview-on-track-title';

const localToday = () => {
    const now = new Date();
    const month = String(now.getMonth() + 1).padStart(2, '0');
    const day = String(now.getDate()).padStart(2, '0');
    return `${now.getFullYear()}-${month}-${day}`;
};

const initialsFor = (name?: string | null) => {
    if (!name) return '?';
    const parts = name.trim().split(/\s+/).slice(0, 2);
    return parts.map(part => part[0]?.toUpperCase() ?? '').join('') || '?';
};

const pillBoxStyle = (tone: PillTone) => ({ background: toneSoftVar[tone], color: toneVar[tone] });
const dotStyle = (tone: PillTone) => ({ background: toneVar[tone] });

const ATTENTION_LOOK: Record<AttentionKind, { tone: PillTone; icon: LucideIcon }> = {
    blocked: { tone: 'red', icon: AlertTriangle },
    reviews: { tone: 'yellow', icon: ClipboardCheck },
    'to-assign': { tone: 'yellow', icon: UserPlus },
    plan: { tone: 'indigo', icon: Target },
};

/** The combined state of several sources: any failure first, then loading, then a stale result. */
const combine = (states: SourceState[]): SourceState => {
    if (states.includes('failed')) return 'failed';
    if (states.includes('loading')) return 'loading';
    if (states.includes('stale')) return 'stale';
    return 'ready';
};

const OverviewPage = () => {
    const { t } = useTranslation();
    const scopeLink = useScopeLink();
    const location = useLocation();
    const navigate = useNavigate();
    const pageTitleRef = useRef<HTMLSpanElement>(null);
    const { project, iteration: scopeIteration } = useWorkScope();
    const navigation = usePlanningNavigationSummary();
    const getStarted = useGetStarted();
    const [today] = useState(localToday);

    const iterations = navigation.iterations;
    const isAllProjects = project === 'all';
    const backlogProject = !isAllProjects && scopeIteration === 'backlog' && typeof project === 'number' ? project : null;
    const isBacklog = backlogProject !== null;
    const viewIterations = useMemo(
        () => iterationsInView(iterations, project, scopeIteration, today),
        [iterations, project, scopeIteration, today],
    );
    /** The project links carry: one project, or All projects. */
    const linkProject: ScopeProject | undefined = isAllProjects ? 'all' : project;

    // feedback-policy: query loading,error,retry,empty - each section shows loading, retry and empty states.
    const taskQueries = useQueries({
        queries: viewIterations.map(item => ({
            queryKey: ['tasks', item.id],
            queryFn: () => taskService.getByIteration(item.id),
            staleTime: 60000,
        })),
    });
    // feedback-policy: query loading,error,retry,empty - the backlog sections share the task states.
    const backlogQuery = useQuery({
        queryKey: ['overview-backlog', backlogProject],
        queryFn: () => loadProjectBacklog(backlogProject as number),
        enabled: isBacklog,
        staleTime: 60000,
    });
    // feedback-policy: query loading,error,retry,empty - the attention item waits for every iteration's plan.
    const readinessQueries = useQueries({
        queries: viewIterations.map(item => ({
            queryKey: planningNavigationSummaryKey(item.id),
            queryFn: () => iterationService.getPlanningReadiness(item.id),
            staleTime: 60000,
        })),
    });
    const pipelineQuery = usePipeline(true);

    const tasksState: SourceState = isBacklog ? queryState(backlogQuery) : combine(taskQueries.map(queryState));
    const readinessState: SourceState = isBacklog ? 'unavailable' : combine(readinessQueries.map(queryState));
    const pipelineStatus = getApiErrorStatus(pipelineQuery.error);
    const pipelineState: SourceState = !pipelineQuery.canRead || (pipelineQuery.isError && (pipelineStatus === 401 || pipelineStatus === 403))
        ? 'unavailable'
        : queryState({ data: pipelineQuery.usableData, isError: pipelineQuery.isError });

    const groups: TaskGroup[] = isBacklog
        ? [{ iteration: null, roots: backlogRoots(backlogQuery.data ?? []) }]
        : viewIterations.map((item, index) => ({ iteration: item, roots: (taskQueries[index]?.data ?? []) as Task[] }));
    const allRoots = groups.flatMap(group => group.roots);

    const iterationLabel = (item: Iteration) => (
        isAllProjects && item.project?.name ? `${item.name} · ${item.project.name}` : item.name
    );
    const linkIn = (item: Iteration, to: string) => scopeLink(to, {
        project: isAllProjects ? 'all' : (item.project_id ?? 'all') as ScopeProject,
        iteration: item.id,
    });
    /** The scopes the pipeline counts cover: each iteration in view, or the backlog. */
    const pipelineScopes: { iteration: Iteration | null; value: ScopeIteration }[] = isBacklog
        ? [{ iteration: null, value: 'backlog' }]
        : viewIterations.map(item => ({ iteration: item, value: item.id }));

    // A task count opens a Tasks list when one list holds exactly that count: a single
    // iteration's filtered list. Otherwise Overview shows the list itself.
    const singleIteration = !isBacklog && viewIterations.length === 1 ? viewIterations[0] : null;
    const ownList = (list: OverviewCountList) => scopeLink(overviewCountListHref(list));

    const listedTasks = (list: OverviewCountList): ListedTask[] => groups.flatMap(group => (
        listTasks(group.roots, list).map(task => ({ task, iteration: group.iteration }))
    ));
    const taskCount = (list: OverviewCountList) => ({
        value: listedTasks(list).length,
        to: singleIteration ? linkIn(singleIteration, taskListHref(list)) : ownList(list),
    });
    // Stage counts are taken in the scope the pipeline view applies, the project and iteration
    // of the scope bar, so the stage they link to always holds that many tasks. With All
    // projects that is every project's work in the scope bar's iteration.
    const stageIteration = typeof scopeIteration === 'number'
        ? iterations.find(item => item.id === scopeIteration) ?? null
        : null;
    const stageCount = (stage: PipelineStage) => ({
        value: pipelineTasksInScope(pipelineQuery.pipeline[stage], linkProject, scopeIteration).length,
        to: scopeLink(pipelineStageHref(stage)),
    });

    // Each kind is counted per iteration, so the item and its link always name one list.
    const attentionState = combine([tasksState, pipelineState, readinessState].filter(state => state !== 'unavailable'));
    const candidates: AttentionCandidate[] = [];
    if (hasResult(attentionState)) {
        for (const group of groups) {
            candidates.push({ kind: 'blocked', count: listTasks(group.roots, 'blocked').length, iteration: group.iteration });
            // Backlog references carry no assignee, so tasks to assign are counted in iterations only.
            if (group.iteration) {
                candidates.push({ kind: 'to-assign', count: listTasks(group.roots, 'toAssign').length, iteration: group.iteration });
            }
        }
        if (hasResult(pipelineState)) {
            for (const scope of pipelineScopes) {
                candidates.push({
                    kind: 'reviews',
                    count: pipelineTasksInScope(pipelineQuery.pipeline.verification_required, linkProject, scope.value).length,
                    iteration: scope.iteration,
                });
            }
        }
        if (hasResult(readinessState)) {
            viewIterations.forEach((item, index) => {
                const { ready, nextId } = planProgress(item, iterations.length, readinessQueries[index]?.data);
                if (ready.done < ready.total) {
                    candidates.push({ kind: 'plan', count: ready.total - ready.done, iteration: item, plan: { ...ready, nextId } });
                }
            });
        }
    }
    const attention = pickAttention(candidates);
    const sourcesIn = (state: SourceState) => ([
        ['tasks', tasksState],
        ['pipeline', pipelineState],
        ['plan', readinessState],
    ] as const).filter(([, value]) => value === state).map(([source]) => source as AttentionSource);
    const unknownSources = sourcesIn('failed');
    const staleSources = sourcesIn('stale');

    const retryTasks = () => {
        if (isBacklog) void backlogQuery.refetch();
        taskQueries.forEach(query => { if (query.isError) void query.refetch(); });
    };
    const retryAttention = () => {
        if (tasksState === 'failed' || tasksState === 'stale') retryTasks();
        if (pipelineState === 'failed' || pipelineState === 'stale') void pipelineQuery.refetch();
        readinessQueries.forEach(query => { if (query.isError) void query.refetch(); });
    };

    const returnFocusId = (location.state as OverviewLocationState | null)?.returnFocusId;
    useEffect(() => {
        if (!returnFocusId || !hasResult(tasksState)) return;
        const focusTarget = document.getElementById(returnFocusId) ?? pageTitleRef.current;
        focusTarget?.focus();
        navigate(
            { pathname: location.pathname, search: location.search, hash: location.hash },
            { replace: true, state: null },
        );
    }, [location.hash, location.pathname, location.search, navigate, returnFocusId, tasksState]);

    const iterationsLoading = navigation.isIterationsLoading && iterations.length === 0;
    const iterationsFailed = navigation.isIterationsError;
    const hasNoIterations = !iterationsLoading && !iterationsFailed && iterations.length === 0;
    const scopeKnown = project !== undefined && scopeIteration !== undefined;
    const showContent = scopeKnown && !iterationsLoading && !iterationsFailed && (isBacklog || !hasNoIterations);

    const openList = parseOverviewCountList(new URLSearchParams(location.search).get(OVERVIEW_COUNT_LIST_PARAM));
    const closeList = () => {
        const params = new URLSearchParams(location.search);
        params.delete(OVERVIEW_COUNT_LIST_PARAM);
        const search = params.toString();
        navigate({ pathname: location.pathname, search: search ? `?${search}` : '' }, { replace: true });
    };

    const purpose = (() => {
        if (iterationsLoading || !scopeKnown) return t('overview.purpose.loading');
        if (isAllProjects) {
            if (viewIterations.length === 0) return t('overview.purpose.allProjectsNoneOpen');
            const start = viewIterations.map(item => item.start_date).sort()[0];
            const end = viewIterations.map(item => item.end_date).sort().at(-1);
            return t('overview.purpose.allProjects', {
                count: viewIterations.length,
                start: formatDate(start),
                end: formatDate(end),
            });
        }
        const projectName = iterations.find(item => item.project_id === project)?.project?.name;
        if (isBacklog) return t('overview.purpose.backlog', { project: projectName ?? t('overview.purpose.thisProject') });
        const item = viewIterations[0];
        if (!item) return t('overview.purpose.loading');
        const dates = { iteration: item.name, start: formatDate(item.start_date), end: formatDate(item.end_date) };
        return item.project?.name
            ? t('overview.purpose.iteration', { project: item.project.name, ...dates })
            : t('overview.purpose.independentIteration', dates);
    })();

    const listLabel = (list: OverviewCountList) => t(`overview.list.labels.${list}`);
    const listReady = openList !== null && hasResult(tasksState);

    return (
        <PageLayout>
            <PageHeader
                title={(
                    <span ref={pageTitleRef} className="overview-page-title-focus" tabIndex={-1}>
                        {t('overview.title')}
                    </span>
                )}
                purpose={purpose}
                primaryAction={(
                    // While Get started shows, its next step is the page's one primary action.
                    <Link to={scopeLink('/tasks?create=1')} className={getStarted.visible ? 'btn secondary' : 'btn primary'}>
                        <Plus aria-hidden="true" className="h-4 w-4" />
                        {t('tasks.newTask')}
                    </Link>
                )}
            />

            {/* The Get started panel comes first, above everything else on the page. */}
            <div className="overview-first-run" data-testid="overview-first-run-slot">
                {getStarted.visible && <GetStartedPanel progress={getStarted.progress} />}
            </div>

            {iterationsLoading && (
                <QueryLoadingState className="overview-state-loading" message={t('overview.dataStatus.loadingOverview')} />
            )}
            {iterationsFailed && (
                <QueryErrorState
                    title={t('overview.dataStatus.planningPeriodsUnavailableTitle')}
                    message={t('overview.dataStatus.planningPeriodsUnavailableBody')}
                    isRetrying={navigation.isIterationsFetching}
                    onRetry={() => { void navigation.refetch(); }}
                />
            )}
            {/* Get started already names the next step, so the empty state would repeat it. */}
            {hasNoIterations && !isBacklog && !getStarted.visible && (
                <SectionCard>
                    <NextStepEmptyState
                        title={t('emptyStates.overview.iterationTitle')}
                        description={t('emptyStates.overview.iterationBody')}
                        fallback={{ label: t('overview.setUpPlanningPeriod'), to: scopeLink(firstRunPlanHref('iteration')) }}
                    />
                </SectionCard>
            )}

            {/* A workspace with no tasks at all gets the page's one next step; sections below stay plain text. */}
            {showContent && !hasNoIterations && !getStarted.visible && allRoots.length === 0 && hasResult(tasksState) && (
                <SectionCard>
                    <NextStepEmptyState
                        description={t(isBacklog ? 'overview.noWorkNowBacklog' : 'overview.noWorkNowFirstUse')}
                        fallback={{ label: t('overview.openTasks'), to: scopeLink('/tasks') }}
                    />
                </SectionCard>
            )}

            {showContent && (
                <>
                    <AttentionItem
                        state={attentionState}
                        candidate={attention}
                        unknownSources={unknownSources}
                        staleSources={staleSources}
                        onRetry={retryAttention}
                        backlog={isBacklog}
                        reviewsHidden={pipelineState === 'unavailable'}
                        multiIteration={isAllProjects}
                        iterationLabel={iterationLabel}
                        linkIn={linkIn}
                        ownList={ownList}
                    />

                    {isAllProjects && viewIterations.length === 0 && (
                        <p className="overview-note">{t('overview.noOpenIterations')}</p>
                    )}

                    <div className="overview-grid">
                        <WorkNow
                            roots={allRoots}
                            state={tasksState}
                            onRetry={retryTasks}
                            backlog={isBacklog}
                            showProject={isAllProjects}
                            showIteration={isAllProjects && viewIterations.length > 1}
                            iterations={viewIterations}
                        />
                        <div className="overview-side">
                            <AgentsNow
                                query={pipelineQuery}
                                stageCount={stageCount}
                                // With All projects the stages count the scope bar's iteration, so the section names it.
                                scopeName={isAllProjects
                                    ? (stageIteration ? iterationLabel(stageIteration) : t('overview.agentsNowBacklog'))
                                    : null}
                            />
                            <OnTrack
                                state={tasksState}
                                onRetry={retryTasks}
                                done={hasResult(tasksState) ? taskCount('done') : null}
                                total={hasResult(tasksState) ? taskCount('total') : null}
                                // Backlog references carry no schedule signals, and Backlog has no end date.
                                atRisk={hasResult(tasksState) && !isBacklog ? taskCount('atRisk') : null}
                                daysLeft={isBacklog ? null : daysLeftToLatestEnd(viewIterations, today)}
                                backlog={isBacklog}
                            />
                        </div>
                    </div>
                </>
            )}

            <SlideOverDrawer
                open={showContent && openList !== null}
                title={openList ? listLabel(openList) : ''}
                subtitle={purpose}
                onClose={closeList}
            >
                <div className="grid gap-3 p-5">
                    {openList && (listReady ? (
                        <CountList
                            items={listedTasks(openList)}
                            label={listLabel(openList)}
                            showIteration={!isBacklog && viewIterations.length > 1}
                            linkProject={linkProject}
                        />
                    ) : (
                        <QueryLoadingState message={t('overview.dataStatus.sectionLoading')} />
                    ))}
                </div>
            </SlideOverDrawer>
        </PageLayout>
    );
};

const AttentionItem = ({
    state,
    candidate,
    unknownSources,
    staleSources,
    onRetry,
    backlog,
    reviewsHidden,
    multiIteration,
    iterationLabel,
    linkIn,
    ownList,
}: {
    state: SourceState;
    candidate: AttentionCandidate | null;
    unknownSources: AttentionSource[];
    staleSources: AttentionSource[];
    onRetry: () => void;
    backlog: boolean;
    reviewsHidden: boolean;
    multiIteration: boolean;
    iterationLabel: (item: Iteration) => string;
    linkIn: (item: Iteration, to: string) => string;
    ownList: (list: OverviewCountList) => string;
}) => {
    const { t } = useTranslation();
    const scopeLink = useScopeLink();
    const sourceNames = (sources: AttentionSource[]) => sources.map(source => t(`overview.attentionItem.sources.${source}`)).join(', ');
    // A refresh failed: the item comes from the last loaded result, so it says so and offers a retry.
    const staleNote = state === 'stale' ? (
        <p className="overview-attention-stale" data-testid="overview-attention-stale">
            <span>{t('overview.attentionItem.staleMeta', { sources: sourceNames(staleSources) })}</span>
            <button type="button" className="btn ghost sm" onClick={onRetry}>
                <RefreshCw aria-hidden="true" className="h-3.5 w-3.5" />
                {t('overview.attentionItem.retry')}
            </button>
        </p>
    ) : null;

    if (state === 'failed') {
        // Without every source Overview cannot say what is most severe, or that nothing is.
        return (
            <section className="overview-attention is-clear" aria-labelledby={ATTENTION_ID} data-attention="unknown">
                <span className="overview-attention-icon" style={pillBoxStyle('gray')}>
                    <HelpCircle aria-hidden="true" className="h-5 w-5" />
                </span>
                <div className="overview-attention-copy">
                    <p className="overview-attention-label">{t('overview.needsYou')}</p>
                    <h2 id={ATTENTION_ID}>{t('overview.attentionItem.unknownTitle')}</h2>
                    <p>{t('overview.attentionItem.unknownMeta', { sources: sourceNames(unknownSources) })}</p>
                </div>
                <button type="button" className="btn secondary overview-attention-action" onClick={onRetry}>
                    <RefreshCw aria-hidden="true" className="h-4 w-4" />
                    {t('overview.attentionItem.retry')}
                </button>
            </section>
        );
    }

    if (state === 'loading' || !candidate) {
        const loading = state === 'loading';
        const stale = state === 'stale';
        const clearMeta = [
            t(backlog ? 'overview.attentionItem.clearMetaBacklog' : 'overview.attentionItem.clearMeta'),
            reviewsHidden ? t('overview.attentionItem.reviewsHidden') : null,
        ].filter(Boolean).join(' ');
        return (
            <section
                className="overview-attention is-clear"
                aria-labelledby={ATTENTION_ID}
                data-attention={loading ? 'loading' : stale ? 'stale-clear' : 'clear'}
            >
                <span className="overview-attention-icon" style={pillBoxStyle('gray')}>
                    <CheckCircle2 aria-hidden="true" className="h-5 w-5" />
                </span>
                <div className="overview-attention-copy">
                    <p className="overview-attention-label">{t('overview.needsYou')}</p>
                    <h2 id={ATTENTION_ID}>
                        {loading
                            ? t('overview.dataStatus.loadingSignals')
                            : t(stale ? 'overview.attentionItem.staleClearTitle' : 'overview.attentionItem.clearTitle')}
                    </h2>
                    {!loading && <p>{clearMeta}</p>}
                    {staleNote}
                </div>
            </section>
        );
    }

    const { kind, count, iteration } = candidate;
    const { tone, icon: Icon } = ATTENTION_LOOK[kind];
    const where = (to: string) => (iteration ? linkIn(iteration, to) : scopeLink(to));
    const plan = candidate.plan ?? { done: 0, total: 0, nextId: '' };
    const content: Record<AttentionKind, { title: string; meta: string; action: string; to: string }> = {
        blocked: {
            title: t('overview.attentionItem.blocked', { count }),
            meta: t('overview.attentionItem.blockedMeta'),
            action: t('overview.attentionItem.blockedAction'),
            // The Tasks backlog does not filter, so Overview lists the blocked backlog work itself.
            to: iteration ? where(taskListHref('blocked')) : ownList('blocked'),
        },
        reviews: {
            title: t('overview.attentionItem.reviews', { count }),
            meta: t('overview.attentionItem.reviewsMeta'),
            action: t('overview.attentionItem.reviewsAction'),
            to: where(pipelineStageHref('verification_required')),
        },
        'to-assign': {
            title: t('overview.attentionItem.toAssign', { count }),
            meta: t('overview.attentionItem.toAssignMeta'),
            action: t('overview.attentionItem.toAssignAction', { count }),
            to: where(taskListHref('toAssign', { mode: 'bulk' })),
        },
        plan: {
            title: t('overview.attentionItem.plan', { done: plan.done, total: plan.total }),
            meta: isPlanningStepId(plan.nextId)
                ? t('overview.attentionItem.planMeta', { step: t(`plan.steps.${plan.nextId}.title`) })
                : t('overview.attentionItem.planMetaGeneric'),
            action: t('overview.attentionItem.planAction'),
            to: where('/plan'),
        },
    };
    const item = content[kind];
    const meta = multiIteration && iteration
        ? t('overview.attentionItem.inIteration', { iteration: iterationLabel(iteration), meta: item.meta })
        : item.meta;

    return (
        <section className="overview-attention" aria-labelledby={ATTENTION_ID} data-attention={kind} data-stale={state === 'stale' || undefined}>
            <span className="overview-attention-icon" style={pillBoxStyle(tone)}>
                <Icon aria-hidden="true" className="h-5 w-5" />
            </span>
            <div className="overview-attention-copy">
                <p className="overview-attention-label">{t('overview.needsYou')}</p>
                <h2 id={ATTENTION_ID}>{item.title}</h2>
                <p>{meta}</p>
                {staleNote}
            </div>
            <Link to={item.to} className="btn secondary overview-attention-action">
                {item.action}
                <ArrowRight aria-hidden="true" className="h-4 w-4" />
            </Link>
        </section>
    );
};

/** A count that opens the list holding exactly that many tasks. */
const CountLink = ({ count, label, testId }: {
    count: { value: number; to: string };
    label: string;
    testId: string;
}) => (
    <Link to={count.to} className="overview-count-link" data-testid={testId} aria-label={`${label}: ${count.value}`}>
        {count.value}
    </Link>
);

const WorkNow = ({ roots, state, onRetry, backlog, showProject, showIteration, iterations }: {
    roots: Task[];
    state: SourceState;
    onRetry: () => void;
    backlog: boolean;
    showProject: boolean;
    showIteration: boolean;
    iterations: Iteration[];
}) => {
    const { t } = useTranslation();
    const scopeLink = useScopeLink();
    const { tasks, openCount } = selectWorkNow(roots);
    const remaining = Math.max(0, openCount - tasks.length);
    const iterationNames = new Map(iterations.map(item => [item.id, item.name]));
    const emptyText = backlog
        ? t('overview.noWorkNowBacklog')
        : roots.length === 0 ? t('overview.noWorkNowFirstUse') : t('overview.noWorkNow');

    return (
        <SectionCard
            className="overview-work-now"
            headingId={WORK_NOW_TITLE_ID}
            icon={<ListTodo aria-hidden="true" className="h-5 w-5 text-action" />}
            title={t('overview.workNow')}
            description={t(backlog ? 'overview.workNowBacklogDescription' : 'overview.workNowDescription')}
            actions={(
                <Link to={scopeLink('/tasks')} className="btn ghost sm">
                    {t('overview.openTasks')}
                    <ArrowRight aria-hidden="true" className="h-3.5 w-3.5" />
                </Link>
            )}
        >
            {state === 'stale' && (
                <QueryStaleState className="mb-3" message={t('overview.dataStatus.sectionStale')} onRetry={onRetry} />
            )}
            {state === 'failed' ? (
                <QueryErrorState message={t('overview.dataStatus.sectionUnavailable')} onRetry={onRetry} />
            ) : !hasResult(state) ? (
                <QueryLoadingState message={t('overview.dataStatus.sectionLoading')} />
            ) : tasks.length === 0 ? (
                <p className="overview-note">{emptyText}</p>
            ) : (
                <>
                    <ul className="overview-task-list">
                        {tasks.map(task => (
                            <TaskRow
                                key={task.id}
                                task={task}
                                // Backlog references carry no effort or assignee to show.
                                detailed={!backlog}
                                context={[
                                    showProject ? task.project?.name : null,
                                    showIteration && task.iteration_id ? iterationNames.get(task.iteration_id) : null,
                                ].filter((value): value is string => Boolean(value))}
                            />
                        ))}
                    </ul>
                    {remaining > 0 && (
                        <p className="overview-work-now-summary">{t('overview.workNowRemaining', { count: remaining })}</p>
                    )}
                </>
            )}
        </SectionCard>
    );
};

const RISK_TONE: Record<Exclude<ReturnType<typeof deliveryRisk>, null>, PillTone> = {
    overdue: 'red',
    'late-start': 'yellow',
    'outside-limits': 'yellow',
    blocked: 'red',
};

const TaskRow = ({ task, context, detailed }: { task: Task; context: string[]; detailed: boolean }) => {
    const { t, i18n } = useTranslation();
    const scopeLink = useScopeLink();
    const risk = deliveryRisk(task);
    const effort = task.effort_days === null || task.effort_days === undefined
        ? t('domain.unknownEstimate')
        : t('units.daysCompact', { count: formatDecimal(task.effort_days, i18n.resolvedLanguage ?? i18n.language, 1) ?? '' });

    return (
        <li>
            <Link
                id={overviewTaskReturnFocusId(task.id)}
                className="overview-task-row"
                to={scopeLink(overviewTaskDrawerHref(task.id, 'work-now'))}
                aria-label={t('overview.thread.openTask', { title: task.title })}
            >
                <span className="overview-task-copy">
                    <span className="overview-task-title">{task.title}</span>
                    <span className="overview-task-meta">
                        <span className="overview-task-status">
                            <span aria-hidden="true" className="overview-task-dot" style={dotStyle(STATUS_TONE[task.status])} />
                            {t(`statuses.${task.status}`)}
                        </span>
                        {context.map(value => <span key={value} className="truncate">{value}</span>)}
                    </span>
                </span>
                {risk && (
                    <span className="overview-task-risk" style={pillBoxStyle(RISK_TONE[risk])}>
                        {risk === 'overdue' && <Clock aria-hidden="true" className="h-3 w-3" />}
                        {t(`overview.deliveryRisk.${risk}`)}
                    </span>
                )}
                {detailed && <span className="overview-task-effort tnum">{effort}</span>}
                {detailed && (task.assignee ? (
                    <span title={task.assignee.name} role="img" aria-label={task.assignee.name} className="overview-task-avatar">
                        <span aria-hidden="true">{initialsFor(task.assignee.name)}</span>
                    </span>
                ) : (
                    <span title={t('common.unassigned')} role="img" aria-label={t('common.unassigned')} className="overview-task-avatar is-empty">
                        <User aria-hidden="true" className="h-3.5 w-3.5" />
                    </span>
                ))}
                <ArrowRight aria-hidden="true" className="overview-task-open-icon h-4 w-4" />
            </Link>
        </li>
    );
};

const AgentsNow = ({ query, stageCount, scopeName }: {
    query: ReturnType<typeof usePipeline>;
    stageCount: (stage: PipelineStage) => { value: number; to: string };
    /** The iteration the stages count when it is not the one the page names. */
    scopeName: string | null;
}) => {
    const { t } = useTranslation();
    const scopeLink = useScopeLink();
    const { canRead, usableData, isPending, isError, error, refetch } = query;

    return (
        <SectionCard
            className="overview-agents-now"
            headingId={AGENTS_NOW_TITLE_ID}
            icon={<Bot aria-hidden="true" className="h-5 w-5 text-action" />}
            title={t('overview.agentsNow')}
            description={scopeName
                ? t('overview.agentsNowScopeDescription', { scope: scopeName })
                : t('overview.agentsNowDescription')}
            actions={(
                <Link to={scopeLink('/tasks?layout=pipeline')} className="btn ghost sm">
                    {t('overview.openPipeline')}
                    <ArrowRight aria-hidden="true" className="h-3.5 w-3.5" />
                </Link>
            )}
        >
            {!canRead ? (
                <p className="overview-note">{t('overview.agentsNowLocked')}</p>
            ) : isError && !usableData ? (
                <QueryErrorState error={error} message={t('agentPipeline.pipelineUnavailable')} onRetry={() => { void refetch(); }} />
            ) : isPending && !usableData ? (
                <QueryLoadingState message={t('agentPipeline.loading')} />
            ) : (
                <>
                {isError && (
                    // A refresh failed: the counts are the last loaded ones.
                    <QueryStaleState className="mb-3" message={t('overview.dataStatus.sectionStale')} onRetry={() => { void refetch(); }} />
                )}
                <dl className="overview-stage-list">
                    {PIPELINE_STAGES.map(stage => {
                        const label = t(`agentPipeline.columns.${stage}.title`);
                        return (
                            <div key={stage}>
                                <dt>{label}</dt>
                                <dd className="tnum">
                                    <CountLink count={stageCount(stage)} label={label} testId={`overview-stage-${stage}`} />
                                </dd>
                            </div>
                        );
                    })}
                </dl>
                </>
            )}
        </SectionCard>
    );
};

const OnTrack = ({ state, onRetry, done, total, atRisk, daysLeft, backlog }: {
    state: SourceState;
    onRetry: () => void;
    done: { value: number; to: string } | null;
    total: { value: number; to: string } | null;
    /** Null where Overview cannot count it: Backlog work carries no schedule signals. */
    atRisk: { value: number; to: string } | null;
    /** Calendar days to the latest end in view; null without an iteration. */
    daysLeft: number | null;
    backlog: boolean;
}) => {
    const { t } = useTranslation();
    const doneLabel = t('overview.figures.done');
    const daysLabel = t('overview.figures.daysLeft');
    const atRiskLabel = t('overview.figures.atRisk');
    const notCounted = (testId: string) => (
        <span className="overview-count-value" data-testid={testId} aria-label={t('overview.figures.notCounted')}>—</span>
    );

    return (
        <SectionCard
            className="overview-on-track"
            headingId={ON_TRACK_TITLE_ID}
            icon={<Target aria-hidden="true" className="h-5 w-5 text-action" />}
            title={t('overview.onTrack')}
        >
            {state === 'stale' && (
                <QueryStaleState className="mb-3" message={t('overview.dataStatus.sectionStale')} onRetry={onRetry} />
            )}
            {state === 'failed' ? (
                <QueryErrorState message={t('overview.dataStatus.sectionUnavailable')} onRetry={onRetry} />
            ) : !hasResult(state) || !done || !total ? (
                <QueryLoadingState message={t('overview.dataStatus.sectionLoading')} />
            ) : (
                <div className="grid gap-3">
                    <dl className="overview-figures">
                        <div>
                            <dt>{doneLabel}</dt>
                            <dd className="tnum">
                                <CountLink count={done} label={doneLabel} testId="overview-figure-done" />
                                <span className="overview-figure-of">{t('overview.figures.of')}</span>
                                <CountLink count={total} label={t('overview.figures.allTasks')} testId="overview-figure-total" />
                            </dd>
                        </div>
                        <div>
                            <dt>{daysLabel}</dt>
                            <dd className="tnum">
                                {/* A number of days, not of tasks: there is no list to open. */}
                                {daysLeft === null
                                    ? notCounted('overview-figure-days-left')
                                    : <span className="overview-count-value" data-testid="overview-figure-days-left">{daysLeft}</span>}
                            </dd>
                        </div>
                        <div>
                            <dt>{atRiskLabel}</dt>
                            <dd className="tnum">
                                {atRisk
                                    ? <CountLink count={atRisk} label={atRiskLabel} testId="overview-figure-at-risk" />
                                    : notCounted('overview-figure-at-risk')}
                            </dd>
                        </div>
                    </dl>
                    {backlog && <p className="overview-note">{t('overview.figures.backlogNote')}</p>}
                </div>
            )}
        </SectionCard>
    );
};

/** One of Overview's own lists: exactly the tasks a count counts. */
const CountList = ({ items, label, showIteration, linkProject }: {
    items: ListedTask[];
    label: string;
    showIteration: boolean;
    linkProject: ScopeProject | undefined;
}) => {
    const { t } = useTranslation();
    const scopeLink = useScopeLink();

    if (items.length === 0) {
        return <p className="overview-note">{t('overview.list.empty')}</p>;
    }
    return (
        <>
            <p className="overview-note">{t('overview.list.count', { label, count: items.length })}</p>
            <ul className="overview-task-list" data-testid="overview-count-list">
                {items.map(({ task, iteration }) => (
                    <li key={task.id}>
                        <Link
                            className="overview-task-row"
                            to={scopeLink(`/tasks?task=${task.id}`, { project: linkProject, iteration: task.iteration_id ?? 'backlog' })}
                            aria-label={t('overview.list.openTask', { title: task.title })}
                        >
                            <span className="overview-task-copy">
                                <span className="overview-task-title">{task.title}</span>
                                <span className="overview-task-meta">
                                    <span className="overview-task-status">
                                        <span aria-hidden="true" className="overview-task-dot" style={dotStyle(STATUS_TONE[task.status])} />
                                        {t(`statuses.${task.status}`)}
                                    </span>
                                    {showIteration && iteration && <span className="truncate">{iteration.name}</span>}
                                    {task.project?.name && <span className="truncate">{task.project.name}</span>}
                                </span>
                            </span>
                            <ArrowRight aria-hidden="true" className="overview-task-open-icon h-4 w-4" />
                        </Link>
                    </li>
                ))}
            </ul>
        </>
    );
};

export default OverviewPage;

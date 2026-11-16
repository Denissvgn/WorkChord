import { useEffect, useMemo, useRef, useState } from 'react';
import { Link, useLocation, useNavigate } from 'react-router-dom';
import { useQueries } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import {
    AlertTriangle,
    ArrowRight,
    Bot,
    Calendar,
    CheckCircle2,
    Clock,
    ClipboardCheck,
    ListTodo,
    Plus,
    Target,
    User,
    UserPlus,
} from 'lucide-react';
import type { LucideIcon } from 'lucide-react';
import { formatDate } from '../utils/formatDate';
import { formatDecimal } from '../utils/workNumbers';
import { taskService } from '../services/taskService';
import { QueryErrorState, QueryLoadingState } from '../components/feedback/QueryState';
import { InlineEmptyState, PageHeader, PageLayout, SectionCard } from '../components/ui';
import type { PillTone } from '../components/ui/tone';
import { STATUS_TONE, toneSoftVar, toneVar } from '../components/ui/tone';
import { usePipeline } from '../components/tasks/usePipeline';
import type { Iteration } from '../types/iteration';
import type { Task } from '../types/task';
import { useWorkScope } from '../features/scope/useWorkScope';
import { useScopeLink } from '../features/scope/useScopeLink';
import type { ScopeProject } from '../features/scope/workScope';
import { usePlanningNavigationSummary } from '../features/planningMasters/usePlanningNavigationSummary';
import { isPlanningStepId } from '../features/planningMasters/planningReturn';
import {
    overviewTaskDrawerHref,
    overviewTaskReturnFocusId,
} from '../features/overview/overviewTaskThread';
import {
    PIPELINE_STAGES,
    deliveryRisk,
    iterationsInView,
    listTasks,
    pickAttention,
    pipelineStageHref,
    pipelineTasksInScope,
    selectWorkNow,
    taskListHref,
    workingDaysLeft,
    type AttentionCandidate,
    type AttentionKind,
    type OverviewTaskList,
    type PipelineStage,
} from '../features/overview/overviewSignals';

type OverviewLocationState = {
    returnFocusId?: string;
};

/** One iteration's share of a count, with the link to the list that holds it. */
type CountPart = {
    key: number;
    label: string;
    count: number;
    to: string;
};

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

const OverviewPage = () => {
    const { t } = useTranslation();
    const scopeLink = useScopeLink();
    const location = useLocation();
    const navigate = useNavigate();
    const pageTitleRef = useRef<HTMLSpanElement>(null);
    const { project, iteration: scopeIteration } = useWorkScope();
    const navigation = usePlanningNavigationSummary();
    const [today] = useState(localToday);

    const iterations = navigation.iterations;
    const viewIterations = useMemo(
        () => iterationsInView(iterations, project, scopeIteration, today),
        [iterations, project, scopeIteration, today],
    );
    const isAllProjects = project === 'all';

    // feedback-policy: query loading,error,retry,empty - each section shows loading, retry and empty states.
    const taskQueries = useQueries({
        queries: viewIterations.map(item => ({
            queryKey: ['tasks', item.id],
            queryFn: () => taskService.getByIteration(item.id),
            staleTime: 60000,
        })),
    });
    const tasksLoading = taskQueries.some(query => query.data === undefined && query.isLoading);
    const failedTaskQueries = taskQueries.filter(query => query.data === undefined && query.isError);
    const tasksAvailable = taskQueries.every(query => query.data !== undefined);
    const tasksByIteration = viewIterations.map((item, index) => ({
        iteration: item,
        roots: (taskQueries[index]?.data ?? []) as Task[],
    }));
    const allRoots = tasksByIteration.flatMap(entry => entry.roots);

    const pipelineQuery = usePipeline(true);
    const pipelineAvailable = pipelineQuery.usableData !== undefined;

    /** The parts of a count: one per iteration in view, each with its own list link. */
    const iterationLabel = (item: Iteration) => (
        isAllProjects && item.project?.name ? `${item.name} · ${item.project.name}` : item.name
    );
    const linkIn = (item: Iteration, to: string) => scopeLink(to, {
        project: isAllProjects ? 'all' : (item.project_id ?? 'all') as ScopeProject,
        iteration: item.id,
    });
    const listParts = (list: OverviewTaskList): CountPart[] => tasksByIteration.map(({ iteration: item, roots }) => ({
        key: item.id,
        label: iterationLabel(item),
        count: listTasks(roots, list).length,
        to: linkIn(item, taskListHref(list)),
    }));
    const stageParts = (stage: PipelineStage): CountPart[] => viewIterations.map(item => ({
        key: item.id,
        label: iterationLabel(item),
        count: pipelineTasksInScope(pipelineQuery.pipeline[stage], isAllProjects ? 'all' : project, item.id).length,
        to: linkIn(item, pipelineStageHref(stage)),
    }));

    const planKnown = navigation.isPlanProgressKnown && typeof scopeIteration === 'number';
    const planIteration = typeof scopeIteration === 'number'
        ? iterations.find(item => item.id === scopeIteration) ?? null
        : null;

    const candidates: AttentionCandidate[] = [];
    // Each kind is counted per iteration, so the item and its link always name one list.
    if (tasksAvailable) {
        for (const { iteration: item, roots } of tasksByIteration) {
            candidates.push({ kind: 'blocked', count: listTasks(roots, 'blocked').length, iteration: item });
            candidates.push({ kind: 'to-assign', count: listTasks(roots, 'toAssign').length, iteration: item });
        }
    }
    if (pipelineAvailable) {
        for (const item of viewIterations) {
            candidates.push({
                kind: 'reviews',
                count: pipelineTasksInScope(pipelineQuery.pipeline.verification_required, isAllProjects ? 'all' : project, item.id).length,
                iteration: item,
            });
        }
    }
    if (planKnown && navigation.ready.done < navigation.ready.total) {
        candidates.push({ kind: 'plan', count: navigation.ready.total - navigation.ready.done, iteration: planIteration });
    }
    const attention = pickAttention(candidates);

    const returnFocusId = (location.state as OverviewLocationState | null)?.returnFocusId;
    useEffect(() => {
        if (!returnFocusId || !tasksAvailable) return;
        const focusTarget = document.getElementById(returnFocusId) ?? pageTitleRef.current;
        focusTarget?.focus();
        navigate(
            { pathname: location.pathname, search: location.search, hash: location.hash },
            { replace: true, state: null },
        );
    }, [location.hash, location.pathname, location.search, navigate, returnFocusId, tasksAvailable]);

    const iterationsLoading = navigation.isIterationsLoading && iterations.length === 0;
    const iterationsFailed = navigation.isIterationsError;
    const hasNoIterations = !iterationsLoading && !iterationsFailed && iterations.length === 0;
    const isBacklog = !isAllProjects && scopeIteration === 'backlog';
    const scopeKnown = project !== undefined && scopeIteration !== undefined;
    const showContent = scopeKnown && !iterationsLoading && !iterationsFailed && !hasNoIterations && !isBacklog;

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

    const retryTasks = () => {
        failedTaskQueries.forEach(query => { void query.refetch(); });
    };

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
                    <Link to={scopeLink('/tasks?create=1')} className="btn primary">
                        <Plus aria-hidden="true" className="h-4 w-4" />
                        {t('tasks.newTask')}
                    </Link>
                )}
            />

            {/* The Get started panel takes this place, above everything else on the page. */}
            <div className="overview-first-run" data-testid="overview-first-run-slot" />

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
            {hasNoIterations && (
                <SectionCard>
                    <InlineEmptyState
                        title={t('overview.noIterationTitle')}
                        description={t('overview.noIterationBody')}
                        actions={(
                            <Link className="btn secondary" to={scopeLink('/plan')}>
                                <Calendar aria-hidden="true" className="h-4 w-4" />
                                {t('overview.setUpPlanningPeriod')}
                            </Link>
                        )}
                    />
                </SectionCard>
            )}
            {isBacklog && !iterationsLoading && !iterationsFailed && !hasNoIterations && (
                <SectionCard>
                    <InlineEmptyState
                        title={t('overview.backlogTitle')}
                        description={t('overview.backlogBody')}
                        actions={(
                            <Link className="btn secondary" to={scopeLink('/tasks')}>
                                {t('overview.openBacklog')}
                                <ArrowRight aria-hidden="true" className="h-4 w-4" />
                            </Link>
                        )}
                    />
                </SectionCard>
            )}

            {showContent && (
                <>
                    <AttentionItem
                        candidate={attention}
                        multiIteration={isAllProjects}
                        loading={tasksLoading}
                        plan={{ ...navigation.ready, nextId: navigation.nextId }}
                        iterationLabel={iterationLabel}
                        linkIn={linkIn}
                    />

                    {isAllProjects && viewIterations.length === 0 && (
                        <p className="overview-note">{t('overview.noOpenIterations')}</p>
                    )}

                    <div className="overview-grid">
                        <WorkNow
                            roots={allRoots}
                            loading={tasksLoading}
                            failed={failedTaskQueries.length > 0}
                            onRetry={retryTasks}
                            showProject={isAllProjects}
                            showIteration={isAllProjects && viewIterations.length > 1}
                            iterations={viewIterations}
                        />
                        <div className="overview-side">
                            <AgentsNow
                                query={pipelineQuery}
                                stageParts={stageParts}
                            />
                            <OnTrack
                                available={tasksAvailable}
                                loading={tasksLoading}
                                failed={failedTaskQueries.length > 0}
                                onRetry={retryTasks}
                                doneParts={tasksAvailable ? listParts('done') : []}
                                totalParts={tasksAvailable ? listParts('total') : []}
                                atRiskParts={tasksAvailable ? listParts('atRisk') : []}
                                dayParts={viewIterations.map(item => ({
                                    key: item.id,
                                    label: iterationLabel(item),
                                    count: workingDaysLeft(item, today),
                                    to: linkIn(item, '/gantt'),
                                }))}
                            />
                        </div>
                    </div>
                </>
            )}
        </PageLayout>
    );
};

const AttentionItem = ({
    candidate,
    multiIteration,
    loading,
    plan,
    iterationLabel,
    linkIn,
}: {
    candidate: AttentionCandidate | null;
    multiIteration: boolean;
    loading: boolean;
    plan: { done: number; total: number; nextId: string };
    iterationLabel: (item: Iteration) => string;
    linkIn: (item: Iteration, to: string) => string;
}) => {
    const { t } = useTranslation();
    const scopeLink = useScopeLink();

    if (!candidate || loading) {
        return (
            <section className="overview-attention is-clear" aria-labelledby={ATTENTION_ID}>
                <span className="overview-attention-icon" style={pillBoxStyle('gray')}>
                    <CheckCircle2 aria-hidden="true" className="h-5 w-5" />
                </span>
                <div className="overview-attention-copy">
                    <p className="overview-attention-label">{t('overview.needsYou')}</p>
                    <h2 id={ATTENTION_ID}>{loading ? t('overview.dataStatus.loadingSignals') : t('overview.attentionItem.clearTitle')}</h2>
                    {!loading && <p>{t('overview.attentionItem.clearMeta')}</p>}
                </div>
            </section>
        );
    }

    const { kind, count, iteration } = candidate;
    const { tone, icon: Icon } = ATTENTION_LOOK[kind];
    const where = (to: string) => (iteration ? linkIn(iteration, to) : scopeLink(to));
    const content: Record<AttentionKind, { title: string; meta: string; action: string; to: string }> = {
        blocked: {
            title: t('overview.attentionItem.blocked', { count }),
            meta: t('overview.attentionItem.blockedMeta'),
            action: t('overview.attentionItem.blockedAction'),
            to: where(taskListHref('blocked')),
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
            to: scopeLink('/plan'),
        },
    };
    const item = content[kind];
    const meta = multiIteration && iteration
        ? t('overview.attentionItem.inIteration', { iteration: iterationLabel(iteration), meta: item.meta })
        : item.meta;

    return (
        <section className="overview-attention" aria-labelledby={ATTENTION_ID} data-attention={kind}>
            <span className="overview-attention-icon" style={pillBoxStyle(tone)}>
                <Icon aria-hidden="true" className="h-5 w-5" />
            </span>
            <div className="overview-attention-copy">
                <p className="overview-attention-label">{t('overview.needsYou')}</p>
                <h2 id={ATTENTION_ID}>{item.title}</h2>
                <p>{meta}</p>
            </div>
            <Link to={item.to} className="btn secondary overview-attention-action">
                {item.action}
                <ArrowRight aria-hidden="true" className="h-4 w-4" />
            </Link>
        </section>
    );
};

/**
 * A count that opens what it counts. With several iterations in view each has its own
 * list, so the count opens a short breakdown with one link per iteration.
 */
const CountLink = ({ parts, value, label, testId }: {
    parts: CountPart[];
    /** The figure shown; a sum of the parts unless given. */
    value?: number;
    label: string;
    testId: string;
}) => {
    const { t } = useTranslation();
    const shown = value ?? parts.reduce((sum, part) => sum + part.count, 0);
    const nonEmpty = parts.filter(part => part.count > 0);
    const single = parts.length === 1 ? parts[0] : nonEmpty.length === 1 ? nonEmpty[0] : null;
    if (single) {
        return (
            <Link to={single.to} className="overview-count-link" data-testid={testId} aria-label={`${label}: ${shown}`}>
                {shown}
            </Link>
        );
    }
    if (nonEmpty.length === 0) {
        return <span className="overview-count-value" data-testid={testId}>{shown}</span>;
    }
    return (
        <details className="overview-count-breakdown" data-testid={testId}>
            <summary aria-label={t('overview.figures.openBreakdown', { label, count: shown })}>{shown}</summary>
            <ul>
                {nonEmpty.map(part => (
                    <li key={part.key}>
                        <Link to={part.to} className="overview-count-link" aria-label={`${label}, ${part.label}: ${part.count}`}>
                            <span>{part.label}</span>
                            <strong className="tnum">{part.count}</strong>
                        </Link>
                    </li>
                ))}
            </ul>
        </details>
    );
};

const WorkNow = ({ roots, loading, failed, onRetry, showProject, showIteration, iterations }: {
    roots: Task[];
    loading: boolean;
    failed: boolean;
    onRetry: () => void;
    showProject: boolean;
    showIteration: boolean;
    iterations: Iteration[];
}) => {
    const { t } = useTranslation();
    const scopeLink = useScopeLink();
    const { tasks, openCount } = selectWorkNow(roots);
    const remaining = Math.max(0, openCount - tasks.length);
    const iterationNames = new Map(iterations.map(item => [item.id, item.name]));

    return (
        <SectionCard
            className="overview-work-now"
            headingId={WORK_NOW_TITLE_ID}
            icon={<ListTodo aria-hidden="true" className="h-5 w-5 text-action" />}
            title={t('overview.workNow')}
            description={t('overview.workNowDescription')}
            actions={(
                <Link to={scopeLink('/tasks')} className="btn ghost sm">
                    {t('overview.openTasks')}
                    <ArrowRight aria-hidden="true" className="h-3.5 w-3.5" />
                </Link>
            )}
        >
            {failed ? (
                <QueryErrorState message={t('overview.dataStatus.sectionUnavailable')} onRetry={onRetry} />
            ) : loading ? (
                <QueryLoadingState message={t('overview.dataStatus.sectionLoading')} />
            ) : tasks.length === 0 ? (
                <InlineEmptyState>{roots.length === 0 ? t('overview.noWorkNowFirstUse') : t('overview.noWorkNow')}</InlineEmptyState>
            ) : (
                <>
                    <ul className="overview-task-list">
                        {tasks.map(task => (
                            <TaskRow
                                key={task.id}
                                task={task}
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

const TaskRow = ({ task, context }: { task: Task; context: string[] }) => {
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
                <span className="overview-task-effort tnum">{effort}</span>
                {task.assignee ? (
                    <span title={task.assignee.name} role="img" aria-label={task.assignee.name} className="overview-task-avatar">
                        <span aria-hidden="true">{initialsFor(task.assignee.name)}</span>
                    </span>
                ) : (
                    <span title={t('common.unassigned')} role="img" aria-label={t('common.unassigned')} className="overview-task-avatar is-empty">
                        <User aria-hidden="true" className="h-3.5 w-3.5" />
                    </span>
                )}
                <ArrowRight aria-hidden="true" className="overview-task-open-icon h-4 w-4" />
            </Link>
        </li>
    );
};

const AgentsNow = ({ query, stageParts }: {
    query: ReturnType<typeof usePipeline>;
    stageParts: (stage: PipelineStage) => CountPart[];
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
            description={t('overview.agentsNowDescription')}
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
                <dl className="overview-stage-list">
                    {PIPELINE_STAGES.map(stage => {
                        const label = t(`agentPipeline.columns.${stage}.title`);
                        return (
                            <div key={stage}>
                                <dt>{label}</dt>
                                <dd className="tnum">
                                    <CountLink parts={stageParts(stage)} label={label} testId={`overview-stage-${stage}`} />
                                </dd>
                            </div>
                        );
                    })}
                </dl>
            )}
        </SectionCard>
    );
};

const OnTrack = ({ available, loading, failed, onRetry, doneParts, totalParts, atRiskParts, dayParts }: {
    available: boolean;
    loading: boolean;
    failed: boolean;
    onRetry: () => void;
    doneParts: CountPart[];
    totalParts: CountPart[];
    atRiskParts: CountPart[];
    dayParts: CountPart[];
}) => {
    const { t } = useTranslation();
    const doneLabel = t('overview.figures.done');
    const daysLabel = t('overview.figures.daysLeft');
    const atRiskLabel = t('overview.figures.atRisk');
    const longestDays = dayParts.reduce((max, part) => Math.max(max, part.count), 0);

    return (
        <SectionCard
            className="overview-on-track"
            headingId={ON_TRACK_TITLE_ID}
            icon={<Target aria-hidden="true" className="h-5 w-5 text-action" />}
            title={t('overview.onTrack')}
        >
            {failed ? (
                <QueryErrorState message={t('overview.dataStatus.sectionUnavailable')} onRetry={onRetry} />
            ) : loading || !available ? (
                <QueryLoadingState message={t('overview.dataStatus.sectionLoading')} />
            ) : (
                <dl className="overview-figures">
                    <div>
                        <dt>{doneLabel}</dt>
                        <dd className="tnum">
                            <CountLink parts={doneParts} label={doneLabel} testId="overview-figure-done" />
                            <span className="overview-figure-of">{t('overview.figures.of')}</span>
                            <CountLink parts={totalParts} label={t('overview.figures.allTasks')} testId="overview-figure-total" />
                        </dd>
                    </div>
                    <div>
                        <dt>{daysLabel}</dt>
                        <dd className="tnum">
                            <CountLink parts={dayParts} value={longestDays} label={daysLabel} testId="overview-figure-days-left" />
                        </dd>
                    </div>
                    <div>
                        <dt>{atRiskLabel}</dt>
                        <dd className="tnum">
                            <CountLink parts={atRiskParts} label={atRiskLabel} testId="overview-figure-at-risk" />
                        </dd>
                    </div>
                </dl>
            )}
        </SectionCard>
    );
};

export default OverviewPage;

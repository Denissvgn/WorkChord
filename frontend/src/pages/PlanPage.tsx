import { ButtonLink } from '../components/common/ButtonLink';
import { useEffect, useRef, useState } from 'react';
import type { ReactNode } from 'react';
import { Link, useSearchParams } from 'react-router-dom';
import { ArrowRight, Check, ChevronDown, RefreshCw } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import clsx from 'clsx';
import { Button } from '../components/common/Button';
import { QueryErrorState, QueryLoadingState } from '../components/feedback/QueryState';
import { CapacitySection } from '../components/capacity/CapacitySection';
import { PlanIterationCheckpoint } from '../components/planning/PlanIterationCheckpoint';
import { PlanIterationDrawers } from '../components/planning/PlanIterationDrawers';
import { PlanScheduleSection } from '../components/planning/PlanScheduleSection';
import { PlanReviewSection } from '../components/planning/PlanReviewSection';
import { PlanWorkSection } from '../components/planning/PlanWorkSection';
import { PlanBlockersSection } from '../components/planning/PlanBlockersSection';
import { PageHeader, PageLayout } from '../components/ui';
import { NextStepEmptyState } from '../features/firstRun/NextStepEmptyState';
import { useFirstRunProgress } from '../features/firstRun/useFirstRunProgress';
import { firstRunPlanHref } from '../features/firstRun/firstRunSteps';
import {
    firstIncompleteCheckpoint,
    planCheckpointSections,
} from '../features/planningMasters/planCheckpoints';
import type { PlanCheckpointSection, PlanCheckpointState } from '../features/planningMasters/planCheckpoints';
import { checkpointEvidence, checkpointOwnerLink, readinessWithServerCounts } from '../features/planningMasters/planEvidence';
import {
    isPlanningStepId,
    PLAN_RETURNED_PARAM,
    PLANNING_STEP_IDS,
} from '../features/planningMasters/planningReturn';
import type { PlanningStepId } from '../features/planningMasters/planningReturn';
import { usePlanningReadiness } from '../features/planningMasters/usePlanningReadiness';
import { planProgress } from '../features/planningMasters/usePlanningNavigationSummary';
import type { PlanningQueryFeedback } from '../features/planningMasters/usePlanningReadiness';
import { useScopeLink } from '../features/scope/useScopeLink';
import { SetupReturnBar } from '../features/firstRun/SetupReturnBar';
import type { IterationPlanningReadinessSummary } from '../types/iteration';
import { formatDecimal } from '../utils/workNumbers';
import { formatDate } from '../utils/formatDate';

type Translate = ReturnType<typeof useTranslation>['t'];
type Readiness = ReturnType<typeof usePlanningReadiness>;

const STEP_PARAM = 'step';
const ITERATION_PARAM = 'iteration';

// Status hues for status; cobalt only for the next step; amber only where something needs doing.
// A waiting checkpoint stays neutral.
const STATE_PILL: Record<PlanCheckpointState, string> = {
    done: 'resolved',
    todo: 'accent',
    warn: 'warn',
    blocked: 'opt',
};

const SECTION_CLASS: Record<PlanCheckpointState, string> = {
    done: 'is-done',
    todo: 'is-next',
    warn: 'is-attention',
    blocked: 'is-waiting',
};

const stateLabel = (section: PlanCheckpointSection, t: Translate) => {
    if (section.state === 'done') return t('plan.page.state.done');
    if (section.state === 'warn') return t('plan.page.state.attention');
    if (section.state === 'blocked') {
        return t('plan.page.state.waiting', { number: PLANNING_STEP_IDS.indexOf(section.waitsFor ?? 'iteration') + 1 });
    }
    return t('plan.page.state.next');
};

/** The one-line result of a checkpoint, worded from the server's reason codes and counts. */
const checkpointResult = (
    section: PlanCheckpointSection,
    summary: IterationPlanningReadinessSummary | undefined,
    readiness: Readiness,
    t: Translate,
    language: string,
): string => {
    const { counts, state } = section;
    if (state === 'blocked') {
        return t('plan.page.waitingResult', { checkpoint: t(`plan.steps.${section.waitsFor ?? 'iteration'}.title`) });
    }
    switch (section.id) {
        case 'iteration': {
            const iteration = readiness.currentIteration;
            return iteration
                ? t('plan.status.periodReady', {
                    name: iteration.name,
                    start: formatDate(iteration.start_date, language),
                    end: formatDate(iteration.end_date, language),
                })
                : t('plan.page.noIterationResult');
        }
        case 'team': {
            if (!summary?.team_member_count) return t('plan.status.noPeople');
            const agents = summary?.team_agent_count ?? 0;
            const members = summary?.team_member_count ?? counts.people ?? 0;
            const capacity = summary?.team_capacity_hours ?? 0;
            const result = t('capacity.result', {
                people: t('capacity.people', { count: members - agents }),
                agents: t('capacity.agents', { count: agents }),
                hours: formatDecimal(capacity, language),
            });
            return state === 'warn'
                ? result + ' · ' + t('plan.status.peopleWithoutAllocation', { count: counts.people_without_capacity ?? 0 })
                : result;
        }
        case 'work':
            return state === 'done'
                ? t('plan.status.workReady', { count: counts.tasks ?? summary?.task_count ?? 0 })
                : t('plan.status.noTasks');
        case 'blockers': {
            if (state === 'done') return t('plan.status.noBlockers');
            const parts = [
                counts.unassigned_tasks ? t('plan.status.unassignedTasks', { count: counts.unassigned_tasks }) : null,
                counts.tasks_without_effort ? t('plan.status.tasksWithoutEffort', { count: counts.tasks_without_effort }) : null,
                counts.agent_working_no_capacity
                    ? t('plan.status.agentWorkingNoCapacity', { count: counts.agent_working_no_capacity })
                    : null,
            ].filter(Boolean);
            return parts.length > 0 ? parts.join(' · ') : t('plan.page.state.attention');
        }
        case 'schedule':
            return state === 'done' ? t('plan.status.scheduleBuilt') : t('plan.status.scheduleNotBuilt');
        default:
            return state === 'done'
                ? t('plan.status.planReady')
                : t('plan.status.risksToAcknowledge', { count: counts.risks ?? 0 });
    }
};

/** Evidence comes from the readiness response; the in-place capacity form also needs the iteration's team. */
const bodyQueries = (stepId: PlanningStepId, queryStates: Readiness['queryStates']): PlanningQueryFeedback[] => (
    stepId === 'team' ? [queryStates.team]
        : stepId === 'work' ? [queryStates.tasks]
            : stepId === 'blockers' ? [queryStates.tasks, queryStates.team]
                : stepId === 'schedule' || stepId === 'review' ? [queryStates.gantt, queryStates.team] : []
);

/** Today's body of a checkpoint: its evidence rows and the link to the page that owns the change. */
const CheckpointBody = ({
    section,
    readiness,
}: {
    section: PlanCheckpointSection;
    readiness: Readiness;
}) => {
    const { t, i18n } = useTranslation();
    const scopeLink = useScopeLink();
    const iterationId = readiness.currentIteration?.id ?? 0;

    if (section.state === 'blocked' && !(section.id === 'review' && readiness.gantt?.schedule_result)) {
        const waitsFor = section.waitsFor ?? 'iteration';
        return (
            <p className="plan-section-waiting">
                {t('plan.page.waitingBody', {
                    number: PLANNING_STEP_IDS.indexOf(waitsFor) + 1,
                    checkpoint: t(`plan.steps.${waitsFor}.title`),
                })}
            </p>
        );
    }

    if (section.id === 'iteration') {
        return <PlanIterationCheckpoint iteration={readiness.currentIteration} done={section.state === 'done'} />;
    }

    const queries = bodyQueries(section.id, readiness.queryStates).filter(query => query.enabled);
    const failed = queries.find(query => query.isBlockingError);
    if (failed) {
        const label = t(`plan.steps.${section.id}.title`);
        return (
            <QueryErrorState
                error={failed.error}
                title={t('plan.master.sectionUnavailableTitle', { section: label })}
                fallback={t('plan.master.sectionUnavailableBody', { section: label })}
                headingLevel={3}
                isRetrying={queries.some(query => query.isFetching)}
                onRetry={() => { void Promise.allSettled(queries.map(query => query.refetch())); }}
            />
        );
    }
    if (queries.some(query => query.isLoading && !query.hasData)) {
        return <QueryLoadingState message={t('plan.master.sectionLoading', { section: t(`plan.steps.${section.id}.title`) })} />;
    }

    const facts = readinessWithServerCounts(readiness.readinessData, readiness.planningSummary);
    const evidence = checkpointEvidence(section.id, facts, t, i18n.language, iterationId);
    const owner = checkpointOwnerLink(section.id, facts, t, iterationId);
    if (section.id === 'team' && readiness.currentIteration) {
        return <CapacitySection key={readiness.currentIteration.id} iteration={readiness.currentIteration}
            iterations={readiness.iterations} members={readiness.teamMembers} primary={section.state !== 'done'} />;
    }
    if (section.id === 'work' && readiness.currentIteration) {
        return <PlanWorkSection key={iterationId} iteration={readiness.currentIteration} tasks={readiness.planningLeafTasks}
            count={section.counts.tasks ?? readiness.planningSummary?.task_count ?? 0} />;
    }
    if (section.id === 'blockers' && readiness.currentIteration) {
        return <PlanBlockersSection key={iterationId} iterationId={iterationId} tasks={readiness.allTasks} members={readiness.teamMembers}
            unassignedCount={section.counts.unassigned_tasks ?? readiness.planningSummary?.tasks_without_assignee ?? 0}
            effortCount={section.counts.tasks_without_effort ?? readiness.planningSummary?.tasks_without_effort ?? 0} />;
    }
    if (section.id === 'schedule' && readiness.currentIteration) {
        return <PlanScheduleSection key={iterationId} iteration={readiness.currentIteration} members={readiness.teamMembers}
            gantt={readiness.gantt} done={section.state === 'done'} />;
    }
    if (section.id === 'review' && readiness.currentIteration) {
        return <PlanReviewSection key={iterationId} iteration={readiness.currentIteration} members={readiness.teamMembers}
            gantt={readiness.gantt} riskCount={section.counts.risks ?? readiness.planningSummary?.risk_count ?? 0} />;
    }
    // One primary action per page: the open, incomplete checkpoint's own action, done in place when it can be.
    const ownerIsPrimary = section.state !== 'done';

    return (
        <>
            <section className="plan-checkpoint-evidence" aria-labelledby={`plan-section-${section.id}-evidence`}>
                <h3 id={`plan-section-${section.id}-evidence`}>{t('plan.page.evidence')}</h3>
                <dl>
                    {evidence.map(item => (
                        <div key={item.label} className={item.exception ? 'exception' : undefined}>
                            <dt>{item.label}</dt>
                            <dd>
                                {item.href ? (
                                    <Link className="plan-evidence-link" to={scopeLink(item.href)} aria-label={item.actionLabel}>
                                        <span>{item.value}</span>
                                        <ArrowRight aria-hidden="true" size={13} />
                                    </Link>
                                ) : item.value}
                            </dd>
                        </div>
                    ))}
                </dl>
            </section>
            <div className="plan-section-owner">
                <ButtonLink to={scopeLink(owner.href)} variant={ownerIsPrimary ? 'primary' : 'secondary'}>
                    {owner.label}
                    <ArrowRight aria-hidden="true" size={14} />
                </ButtonLink>
            </div>
        </>
    );
};

const CheckpointSection = ({
    section,
    open,
    onToggle,
    result,
    children,
}: {
    section: PlanCheckpointSection;
    open: boolean;
    onToggle: () => void;
    result: string;
    children: ReactNode;
}) => {
    const { t } = useTranslation();
    const headingId = `plan-section-${section.id}-title`;
    const bodyId = `plan-section-${section.id}-body`;
    const statusId = `plan-section-${section.id}-status`;
    return (
        <li className={clsx('plan-section', SECTION_CLASS[section.state], open && 'is-open')} data-state={section.state}
            data-testid={`plan-section-${section.id}`}>
            <div className="plan-section-head">
                <span className="plan-section-number" aria-hidden="true">
                    {section.state === 'done' ? <Check size={13} strokeWidth={3} /> : section.number}
                </span>
                <h2 id={headingId} className="plan-section-title">
                    <Button variant="ghost" className="plan-section-toggle" aria-expanded={open} aria-controls={bodyId}
                        aria-describedby={statusId} onClick={onToggle}>
                        <span className="sr-only">{t('plan.page.checkpointNumber', { number: section.number })}: </span>
                        {t(`plan.steps.${section.id}.title`)}
                        <ChevronDown aria-hidden="true" size={15} className="plan-section-chevron" />
                    </Button>
                </h2>
                <p id={statusId} className="plan-section-status">
                    <span className={`pill ${STATE_PILL[section.state]}`}>
                        <span className="pdot" />
                        {stateLabel(section, t)}
                    </span>
                    <span className="plan-section-result">{result}</span>
                </p>
            </div>
            {open && (
                <div id={bodyId} className="plan-section-body" role="region" aria-labelledby={headingId}>
                    {children}
                </div>
            )}
        </li>
    );
};

const PlanCheckpoints = () => {
    const { t, i18n } = useTranslation();
    const [searchParams, setSearchParams] = useSearchParams();
    const readiness = usePlanningReadiness();
    const { currentIteration, hasCurrentIteration, planningSummary, queryStates, refetch, isFetching } = readiness;
    const scopeLink = useScopeLink();
    const setupProgress = useFirstRunProgress();
    const [refreshStatus, setRefreshStatus] = useState<'idle' | 'success' | 'error'>('idle');
    // Opening or closing a section by hand wins over the default for the rest of the visit to that
    // iteration; another iteration in scope starts again from its first incomplete checkpoint.
    const [openOverride, setOpenOverride] = useState<{ id: PlanningStepId | null; iterationId?: number } | null>(null);

    // A section kept in the link belongs to the iteration it was opened for. When the scope moves to
    // another iteration and the link still names that section, it is set aside, so the new iteration
    // opens on its first incomplete checkpoint. A section that arrives with the link, or together with
    // the new iteration, is kept.
    const linkStep = searchParams.get(STEP_PARAM);
    const scopeIteration = searchParams.get(ITERATION_PARAM);
    const [stepScope, setStepScope] = useState({ iteration: scopeIteration, step: linkStep, stale: false });
    if (stepScope.iteration !== scopeIteration || stepScope.step !== linkStep) {
        const iterationChanged = stepScope.iteration !== null && scopeIteration !== null
            && stepScope.iteration !== scopeIteration;
        const stale = linkStep !== null && linkStep === stepScope.step && (stepScope.stale || iterationChanged);
        setStepScope({ iteration: scopeIteration, step: linkStep, stale });
    }
    const requestedStep = stepScope.stale ? null : linkStep;
    useEffect(() => {
        if (!stepScope.stale) return;
        setSearchParams(previous => {
            const next = new URLSearchParams(previous);
            next.delete(STEP_PARAM);
            return next;
        }, { replace: true });
    }, [setSearchParams, stepScope.stale]);

    const sections = planCheckpointSections(planningSummary, { hasIteration: hasCurrentIteration });
    const defaultOpen = isPlanningStepId(requestedStep)
        ? requestedStep
        : sections ? firstIncompleteCheckpoint(sections) : null;
    const override = openOverride && openOverride.iterationId === currentIteration?.id ? openOverride : null;
    const openId = override ? override.id : defaultOpen;

    // Coming back from Tasks, Team or Gantt re-reads readiness; a section that is now done gives
    // way to the first incomplete one.
    const returned = searchParams.get(PLAN_RETURNED_PARAM) === '1';
    const returnStarted = useRef(false);
    const [returnSettled, setReturnSettled] = useState(false);
    const sectionsKnown = queryStates.iterations.hasData
        && (!hasCurrentIteration || planningSummary !== undefined);
    useEffect(() => {
        // Wait for the first read, so the re-read is of the iteration's own readiness.
        if (!returned || !sectionsKnown || returnStarted.current) return;
        returnStarted.current = true;
        void refetch().finally(() => setReturnSettled(true));
    }, [refetch, returned, sectionsKnown]);
    useEffect(() => {
        if (!returnSettled || isFetching || !sections) return;
        // eslint-disable-next-line react-hooks/set-state-in-effect -- runs once after the return re-read settles.
        setReturnSettled(false);
        const stepDone = sections.find(section => section.id === requestedStep)?.state === 'done';
        if (stepDone) setOpenOverride(null);
        setSearchParams(previous => {
            const next = new URLSearchParams(previous);
            next.delete(PLAN_RETURNED_PARAM);
            if (stepDone) next.delete(STEP_PARAM);
            return next;
        }, { replace: true });
    }, [isFetching, requestedStep, returnSettled, sections, setSearchParams]);

    const toggle = (id: PlanningStepId) => {
        const next = openId === id ? null : id;
        setOpenOverride({ id: next, iterationId: currentIteration?.id });
        if (next) {
            setSearchParams(previous => {
                const params = new URLSearchParams(previous);
                params.set(STEP_PARAM, next);
                return params;
            }, { replace: true });
        }
    };

    const refresh = async () => {
        if (isFetching) return;
        setRefreshStatus('idle');
        const results = await refetch();
        const failed = results.some(result => result.status === 'rejected'
            || Boolean((result.value as { isError?: boolean } | undefined)?.isError));
        setRefreshStatus(failed ? 'error' : 'success');
    };

    // With no iteration there is no readiness to read: the page offers the one next step and shows no
    // checkpoint states. Before a profile or project exists, that step alone.
    const noIteration = queryStates.iterations.hasData && !hasCurrentIteration;
    const setupFirst = noIteration && setupProgress.known && (setupProgress.nextId === 'profile' || setupProgress.nextId === 'project');
    const iterationIsNext = noIteration && setupProgress.known && setupProgress.nextId === 'iteration';
    // The server's own count; no count without a complete response.
    const progress = sections && hasCurrentIteration ? planProgress(currentIteration, planningSummary)?.ready ?? null : null;
    const header = (
        <PageHeader
            title={t('plan.title')}
            purpose={t('plan.page.purpose')}
            meta={(
                <span className="plan-page-meta">
                    <span>{currentIteration?.name ?? t('plan.page.noIteration')}</span>
                    {progress !== null && (
                        <span className="tnum">{t('plan.page.progress', { done: progress.done, total: progress.total })}</span>
                    )}
                    {refreshStatus !== 'idle' && (
                        <span role={refreshStatus === 'error' ? 'alert' : 'status'}>
                            {refreshStatus === 'error' ? t('plan.hub.refreshFailed') : t('plan.hub.refreshSucceeded')}
                        </span>
                    )}
                </span>
            )}
            secondaryActions={(
                <Button variant="secondary" onClick={() => { void refresh(); }} disabled={isFetching} aria-busy={isFetching}>
                    <RefreshCw aria-hidden="true" size={12} className={isFetching ? 'animate-spin' : undefined} />
                    {isFetching ? t('actions.refreshing') : t('plan.hub.refresh')}
                </Button>
            )}
        />
    );

    let content: ReactNode;
    if (queryStates.iterations.isLoading && !queryStates.iterations.hasData) {
        content = <QueryLoadingState message={t('plan.master.planningDataLoading')} />;
    } else if (queryStates.iterations.isBlockingError) {
        content = (
            <QueryErrorState
                error={queryStates.iterations.error}
                title={t('plan.master.planningDataUnavailable')}
                fallback={t('plan.master.planningDataUnavailableBody')}
                headingLevel={2}
                isRetrying={queryStates.iterations.isFetching}
                onRetry={() => { void refetch(); }}
            />
        );
    } else if (setupFirst) {
        content = (
            <NextStepEmptyState
                title={t('emptyStates.plan.title')}
                description={t('emptyStates.plan.body')}
                fallback={{ label: t('firstRun.steps.iteration.title'), to: scopeLink(firstRunPlanHref('iteration')) }}
            />
        );
    } else if (noIteration) {
        // No iteration, so no readiness to read: the Iteration step offers New iteration and
        // carries no state.
        content = (
            <ol className="plan-sections" aria-label={t('plan.page.checkpoints')}>
                <li className="plan-section is-open" data-testid="plan-section-iteration">
                    <div className="plan-section-head">
                        <span className="plan-section-number" aria-hidden="true">1</span>
                        <h2 id="plan-section-iteration-title" className="plan-section-title">
                            {t('plan.steps.iteration.title')}
                        </h2>
                    </div>
                    <div className="plan-section-body" role="region" aria-labelledby="plan-section-iteration-title">
                        <PlanIterationCheckpoint iteration={null} done={false} />
                    </div>
                </li>
            </ol>
        );
    } else if (!sections && queryStates.checkpoints.isLoading) {
        content = <QueryLoadingState message={t('plan.master.planningDataLoading')} />;
    } else if (!sections) {
        content = (
            <QueryErrorState
                error={queryStates.checkpoints.error}
                title={t('plan.page.checkpointsUnavailable')}
                fallback={t('plan.page.checkpointsUnavailableBody')}
                headingLevel={2}
                isRetrying={queryStates.checkpoints.isFetching}
                onRetry={() => { void queryStates.checkpoints.refetch(); }}
            />
        );
    } else {
        content = (
            <ol className="plan-sections" aria-label={t('plan.page.checkpoints')}>
                {sections.map(section => (
                    <CheckpointSection
                        key={section.id}
                        section={section}
                        open={openId === section.id}
                        onToggle={() => toggle(section.id)}
                        result={checkpointResult(section, planningSummary, readiness, t, i18n.language)}
                    >
                        <CheckpointBody section={section} readiness={readiness} />
                    </CheckpointSection>
                ))}
            </ol>
        );
    }

    return (
        <PageLayout variant="wide" className="plan-page">
            {header}
            <SetupReturnBar />
            {noIteration && !setupFirst && !iterationIsNext && (
                <NextStepEmptyState
                    title={t('emptyStates.plan.title')}
                    description={t('emptyStates.plan.body')}
                    fallback={{ label: t('firstRun.steps.iteration.title'), to: scopeLink(firstRunPlanHref('iteration')) }}
                />
            )}
            <div aria-busy={isFetching || undefined}>{content}</div>
        </PageLayout>
    );
};

/** Plan is the six checkpoints; iterations are managed in drawers that open over them. */
const PlanPage = () => (
    <>
        <PlanCheckpoints />
        <PlanIterationDrawers />
    </>
);

export default PlanPage;

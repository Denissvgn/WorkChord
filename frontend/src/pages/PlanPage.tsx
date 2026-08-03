import { useState } from 'react';
import { Link } from 'react-router-dom';
import {
    ArrowRight,
    CalendarRange,
    Check,
    ChevronDown,
    GanttChartSquare,
    Inbox,
    Layers,
    ListTodo,
    LockKeyhole,
    RefreshCw,
    Sparkles,
    TriangleAlert,
    Users,
} from 'lucide-react';
import type { LucideIcon } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { localizeStatus, STEP_DEFS } from '../features/planningMasters/masters';
import { usePlanningReadiness } from '../features/planningMasters/usePlanningReadiness';
import { PageHeader, PageLayout } from '../components/ui';
import { QueryErrorState, QueryLoadingState } from '../components/feedback/QueryState';
import { PlanningWorkflowGuide } from '../components/planning/PlanningWorkflowGuide';
import { formatDate } from '../utils/formatDate';

type LocalizedStepStatus = {
    state: string;
    summary?: string;
    missing?: string[];
};

type PlanningJob = {
    id: string;
    title: string;
    description: string;
    icon: LucideIcon;
    meta: string;
    to: string;
};

type RefreshStatus = 'idle' | 'success' | 'error';

const stepClassName = (state: string, isNext: boolean) => {
    if (state === 'done') return 'done';
    if (state === 'warn') return 'warn';
    if (state === 'blocked') return 'blocked';
    return isNext ? 'current' : '';
};

const refetchResultFailed = (value: unknown) => (
    typeof value === 'object'
    && value !== null
    && 'isError' in value
    && Boolean((value as { isError?: boolean }).isError)
);

function PlanningReadinessLauncher({
    ready,
    status,
    nextId,
}: {
    ready: { done: number; total: number; pct: number };
    status: Record<string, LocalizedStepStatus>;
    nextId: string;
}) {
    const { t } = useTranslation();
    const nextStep = STEP_DEFS.find(step => step.id === nextId);
    const action = ready.done === 0
        ? t('plan.hub.start')
        : ready.done === ready.total
            ? t('plan.hub.review')
            : t('plan.hub.resume');
    const recommendation = ready.done === 0
        ? t('plan.hub.recommendedStart')
        : ready.done === ready.total
            ? t('plan.hub.recommendedWrap')
            : t('plan.hub.recommendedResume');
    const readinessSummary = ready.pct === 0
        ? t('plan.hub.nothingSetUp')
        : ready.pct === 100
            ? t('plan.hub.planReadyShare')
            : t('plan.hub.stepsComplete', { done: ready.done, total: ready.total });

    const localizedState = (stepId: string) => {
        const stepStatus = status[stepId];
        if (stepStatus.state === 'done') return stepStatus.summary || t('plan.hub.done');
        if (stepStatus.state === 'warn') {
            return stepStatus.missing?.[0] || t('plan.hub.needsAttention');
        }
        if (stepStatus.state === 'blocked') return t('plan.hub.locked');
        if (stepId === nextId) return t('plan.hub.nextStep');
        return t('plan.hub.notStarted');
    };

    return (
        <section className="mcard primary plan-hub-primary" aria-labelledby="plan-hub-primary-title">
            <div className="plan-hub-primary-header">
                <div className="plan-hub-primary-copy">
                    <div className="mc-icon">
                        <CalendarRange aria-hidden="true" size={17} />
                    </div>
                    <div>
                        <div className="plan-hub-primary-title-row">
                            <h2 id="plan-hub-primary-title" className="mc-title">
                                {t('plan.hub.planIterationTitle')}
                            </h2>
                            <span className="pill current sm">{recommendation}</span>
                        </div>
                        <p className="mc-desc">{t('plan.hub.planIterationDescription')}</p>
                    </div>
                </div>
                <Link className="btn primary lg plan-hub-primary-action" to="/plan/master">
                    {action}
                    <ArrowRight aria-hidden="true" size={14} />
                </Link>
            </div>

            <div className="plan-hub-readiness">
                <div className="plan-hub-readiness-copy">
                    <strong>{readinessSummary}</strong>
                    <span>
                        {ready.pct < 100 && nextStep ? (
                            <>
                                {t('plan.hub.next')}: {t(`plan.steps.${nextStep.id}.title`)}
                                {status[nextId]?.missing?.[0] && <> · {status[nextId].missing?.[0]}</>}
                            </>
                        ) : t('plan.hub.noActiveRisks')}
                    </span>
                </div>
                <div
                    className="plan-hub-progress"
                    role="progressbar"
                    aria-label={t('plan.hub.readinessProgress', { percent: ready.pct })}
                    aria-valuemin={0}
                    aria-valuemax={100}
                    aria-valuenow={ready.pct}
                    aria-valuetext={readinessSummary}
                >
                    <span style={{ transform: `scaleX(${ready.pct / 100})` }} />
                </div>
            </div>

            <details className="plan-hub-checkpoints">
                <summary>
                    <span>
                        {t('plan.hub.checkpointProgress', {
                            done: ready.done,
                            total: ready.total,
                        })}
                    </span>
                    <ChevronDown aria-hidden="true" size={15} />
                </summary>
                <ol
                    className="plan-hub-checkpoint-grid"
                    aria-label={t('plan.hub.checkpointList')}
                >
                    {STEP_DEFS.map((step, index) => {
                        const stepStatus = status[step.id];
                        const isNext = step.id === nextId;
                        return (
                            <li
                                key={step.id}
                                className={`mini-step ${stepClassName(stepStatus.state, isNext)}`}
                                aria-current={isNext ? 'step' : undefined}
                            >
                                <span className="ms-dot" aria-hidden="true">
                                    {stepStatus.state === 'done' ? (
                                        <Check size={11} strokeWidth={3} />
                                    ) : stepStatus.state === 'blocked' ? (
                                        <LockKeyhole size={10} />
                                    ) : index + 1}
                                </span>
                                <span className="plan-hub-checkpoint-copy">
                                    <strong>{t(`plan.steps.${step.id}.title`)}</strong>
                                    <span>{localizedState(step.id)}</span>
                                </span>
                            </li>
                        );
                    })}
                </ol>
            </details>
        </section>
    );
}

function PlanningJobLink({ job }: { job: PlanningJob }) {
    const { t } = useTranslation();
    const Icon = job.icon;

    return (
        <Link
            className="plan-hub-job"
            to={job.to}
            aria-labelledby={`plan-hub-job-${job.id}-title`}
            aria-describedby={`plan-hub-job-${job.id}-description plan-hub-job-${job.id}-meta`}
        >
            <span className="mc-icon" aria-hidden="true">
                <Icon size={16} />
            </span>
            <span className="plan-hub-job-copy">
                <strong id={`plan-hub-job-${job.id}-title`}>{job.title}</strong>
                <span id={`plan-hub-job-${job.id}-description`}>{job.description}</span>
                <small id={`plan-hub-job-${job.id}-meta`}>{job.meta}</small>
            </span>
            <span className="plan-hub-job-action" aria-hidden="true">
                {t('plan.hub.open')}
                <ArrowRight size={12} />
            </span>
        </Link>
    );
}

const PlanPage = () => {
    const { t } = useTranslation();
    const [refreshStatus, setRefreshStatus] = useState<RefreshStatus>('idle');
    const {
        currentIteration,
        readinessData,
        status: rawStatus,
        ready,
        nextId,
        isFetching,
        queryStates,
        refetch,
    } = usePlanningReadiness({ includeInbox: true });
    const status = localizeStatus(rawStatus, readinessData, t);

    const enabledCoreQueries = [
        queryStates.team,
        queryStates.tasks,
        queryStates.gantt,
    ].filter(query => query.enabled);
    const isCoreLoading = queryStates.iterations.isLoading
        || enabledCoreQueries.some(query => query.isLoading);
    const coreError = queryStates.iterations.isBlockingError
        ? queryStates.iterations.error
        : enabledCoreQueries.find(query => query.isBlockingError)?.error;

    const refreshPlanning = async () => {
        if (isFetching) return;
        setRefreshStatus('idle');
        try {
            const results = await refetch();
            const failed = results.some(result => (
                result.status === 'rejected'
                || (result.status === 'fulfilled' && refetchResultFailed(result.value))
            ));
            setRefreshStatus(failed ? 'error' : 'success');
        } catch {
            setRefreshStatus('error');
        }
    };

    const intakeMeta = queryStates.inbox.isLoading
        ? t('plan.hub.intakeStatusLoading')
        : queryStates.inbox.isError
            ? t('plan.hub.intakeStatusUnavailable')
            : t('plan.hub.inQueue', { count: readinessData.inboxCount || 0 });

    const planningJobs: PlanningJob[] = [
        ...(readinessData.inboxCount > 0 || queryStates.inbox.isError ? [{
            id: 'intake',
            title: t('plan.masters.processIntake.title'),
            description: t('plan.masters.processIntake.description'),
            icon: Inbox,
            meta: intakeMeta,
            to: '/triage',
        }] : []),
        ...(readinessData.riskCount > 0 ? [{
            id: 'replan',
            title: t('plan.masters.replanAtRisk.title'),
            description: t('plan.masters.replanAtRisk.description'),
            icon: TriangleAlert,
            meta: t('plan.hub.activeSignals', { count: readinessData.riskCount }),
            to: '/gantt',
        }] : []),
    ];

    if (isCoreLoading) {
        return (
            <PageLayout variant="wide">
                <QueryLoadingState message={t('plan.master.planningDataLoading')} />
            </PageLayout>
        );
    }

    if (coreError) {
        return (
            <PageLayout variant="wide">
                <QueryErrorState
                    title={t('plan.master.planningDataUnavailable')}
                    message={t('plan.master.planningDataUnavailableBody')}
                    onRetry={refreshPlanning}
                />
            </PageLayout>
        );
    }

    return (
        <PageLayout variant="wide">
            <PageHeader
                title={t('plan.title')}
                subtitle={t('plan.hub.subtitle')}
                actions={(
                    <>
                        <Link
                            className="iter-pick"
                            to="/plan/master"
                            aria-label={t('plan.hub.openPeriodSetup', {
                                period: currentIteration?.name || t('plan.hub.pickPeriod'),
                            })}
                        >
                            <CalendarRange aria-hidden="true" size={13} />
                            <span className="plan-hub-period-name">
                                {currentIteration?.name || t('plan.hub.pickPeriod')}
                            </span>
                            {currentIteration && (
                                <span className="iter-dates">
                                    · {formatDate(readinessData.currentIterationStart)}
                                    –{formatDate(readinessData.currentIterationEnd)}
                                </span>
                            )}
                            <ArrowRight aria-hidden="true" size={11} />
                        </Link>
                        <PlanningWorkflowGuide surface="plan" />
                        <button
                            className="btn"
                            type="button"
                            onClick={() => { void refreshPlanning(); }}
                            disabled={isFetching}
                            aria-busy={isFetching}
                        >
                            <RefreshCw
                                aria-hidden="true"
                                className={isFetching ? 'animate-spin' : undefined}
                                size={12}
                            />
                            {isFetching ? t('actions.refreshing') : t('plan.hub.refresh')}
                        </button>
                        {refreshStatus !== 'idle' && (
                            <span
                                className={`plan-hub-refresh-status ${refreshStatus}`}
                                role={refreshStatus === 'error' ? 'alert' : 'status'}
                            >
                                {refreshStatus === 'error'
                                    ? t('plan.hub.refreshFailed')
                                    : t('plan.hub.refreshSucceeded')}
                            </span>
                        )}
                    </>
                )}
            />

            <PlanningReadinessLauncher
                ready={ready}
                status={status}
                nextId={nextId}
            />

            {planningJobs.length > 0 && (
                <section className="plan-hub-jobs" aria-labelledby="plan-hub-jobs-title">
                    <div className="plan-hub-section-heading">
                        <h2 id="plan-hub-jobs-title">{t('plan.hub.attentionJobs')}</h2>
                        <p>{t('plan.hub.attentionJobsDescription')}</p>
                    </div>
                    <div className="plan-hub-job-list">
                        {planningJobs.map(job => <PlanningJobLink key={job.id} job={job} />)}
                    </div>
                </section>
            )}

            <details className="plan-hub-direct-tools">
                <summary>
                    <span>
                        <strong>{t('plan.hub.directTools')}</strong>
                        <small>{t('plan.hub.directToolsDescription')}</small>
                    </span>
                    <ChevronDown aria-hidden="true" size={15} />
                </summary>
                <nav className="plan-hub-direct-tool-groups" aria-label={t('plan.hub.directTools')}>
                    <section className="plan-hub-direct-tool-group">
                        <h3>{t('plan.hub.directToolGroups.shape')}</h3>
                        <div className="plan-hub-direct-tool-list">
                            <Link to="/projects" className="btn sm ghost">
                                <Layers aria-hidden="true" size={12} />
                                {t('plan.masters.planProject.title')}
                            </Link>
                            <Link to="/triage" className="btn sm ghost">
                                <Inbox aria-hidden="true" size={12} />
                                {t('nav.triage')}
                            </Link>
                            <Link to="/tasks" className="btn sm ghost">
                                <ListTodo aria-hidden="true" size={12} />
                                {t('nav.tasks')}
                            </Link>
                        </div>
                    </section>
                    <section className="plan-hub-direct-tool-group">
                        <h3>{t('plan.hub.directToolGroups.schedule')}</h3>
                        <div className="plan-hub-direct-tool-list">
                            <Link to="/iterations" className="btn sm ghost">
                                <CalendarRange aria-hidden="true" size={12} />
                                {t('nav.iterations')}
                            </Link>
                            <Link to="/team" className="btn sm ghost">
                                <Users aria-hidden="true" size={12} />
                                {t('nav.team')}
                            </Link>
                            <Link to="/gantt" className="btn sm ghost">
                                <GanttChartSquare aria-hidden="true" size={12} />
                                {t('nav.gantt')}
                            </Link>
                        </div>
                    </section>
                    <section className="plan-hub-direct-tool-group">
                        <h3>{t('plan.hub.directToolGroups.automation')}</h3>
                        <div className="plan-hub-direct-tool-list">
                            <Link to="/agent-pipeline" className="btn sm ghost">
                                <Sparkles aria-hidden="true" size={12} />
                                {t('plan.masters.agentReady.title')}
                            </Link>
                        </div>
                    </section>
                </nav>
            </details>
        </PageLayout>
    );
};

export default PlanPage;

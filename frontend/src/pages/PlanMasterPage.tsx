import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import type { ReactNode } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import {
    ArrowRight,
    CalendarRange,
    Check,
    Copy,
    ExternalLink,
    GanttChartSquare,
    ListChecks,
    RefreshCw,
    Share2,
    ShieldAlert,
    Users,
} from 'lucide-react';
import { Link, useSearchParams } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import {
    localizeStatus,
    readiness as calculateReadiness,
    STEP_DEFS,
    nextStep,
} from '../features/planningMasters/masters';
import type { PlanReadiness, StepStatus } from '../features/planningMasters/masters';
import {
    usePlanningReadiness,
} from '../features/planningMasters/usePlanningReadiness';
import type {
    PlanningQueryFeedback,
} from '../features/planningMasters/usePlanningReadiness';
import { planShareService } from '../services/planShareService';
import type { PlanShare } from '../services/planShareService';
import { copyText } from '../utils/copyText';
import { formatDate, formatDateTime } from '../utils/formatDate';
import { Breadcrumbs } from '../components/layout/Breadcrumbs';
import { QueryErrorState, QueryLoadingState } from '../components/feedback/QueryState';
import { useConfirmDialog } from '../components/common/useConfirmDialog';
import { useToast } from '../components/feedback/toast';
import {
    isPlanningStepId,
    withPlanMasterReturn,
} from '../features/planningMasters/planningReturn';
import type { PlanningStepId } from '../features/planningMasters/planningReturn';

type StepDataState = {
    loading: boolean;
    fetching: boolean;
    error: unknown;
    retry: () => Promise<unknown> | unknown;
    label: string;
};

type EvidenceItem = {
    label: string;
    value: string;
    exception?: boolean;
};

const STEP_ICONS: Record<string, ReactNode> = {
    iteration: <CalendarRange aria-hidden="true" />,
    team: <Users aria-hidden="true" />,
    work: <ListChecks aria-hidden="true" />,
    blockers: <ShieldAlert aria-hidden="true" />,
    schedule: <GanttChartSquare aria-hidden="true" />,
    review: <Share2 aria-hidden="true" />,
};

const stepQueryStates = (
    stepId: string,
    queryStates: ReturnType<typeof usePlanningReadiness>['queryStates'],
) => {
    if (stepId === 'team') return [queryStates.team];
    if (stepId === 'work' || stepId === 'blockers') return [queryStates.tasks];
    if (stepId === 'schedule' || stepId === 'review') {
        return [queryStates.team, queryStates.tasks, queryStates.gantt];
    }
    return [];
};

const StepStatePill = ({ state }: { state: StepStatus['state'] }) => {
    const { t } = useTranslation();
    const labels: Record<StepStatus['state'], string> = {
        done: t('plan.master.done'),
        warn: t('plan.master.needsAttention'),
        blocked: t('plan.master.blocked'),
        todo: t('plan.master.notStarted'),
    };
    return (
        <span className={`pill ${state === 'todo' ? 'opt' : state}`}>
            <span className="pdot" />
            {labels[state]}
        </span>
    );
};

const getStepEvidence = (
    stepId: string,
    readiness: PlanReadiness,
    t: ReturnType<typeof useTranslation>['t'],
    language: string,
): EvidenceItem[] => {
    if (stepId === 'iteration') {
        return [
            {
                label: t('plan.master.selectedPeriod'),
                value: readiness.currentIterationName || t('plan.master.notAvailable'),
                exception: !readiness.hasCurrentIteration,
            },
            {
                label: t('plan.master.periodDates'),
                value: readiness.hasCurrentIteration
                    ? `${formatDate(readiness.currentIterationStart, language)} – ${formatDate(readiness.currentIterationEnd, language)}`
                    : t('plan.master.notAvailable'),
                exception: !readiness.hasCurrentIteration,
            },
            {
                label: t('plan.master.workingDays'),
                value: readiness.hasCurrentIteration
                    ? t('plan.master.daysCount', { count: readiness.currentIterationDays })
                    : t('plan.master.notAvailable'),
            },
        ];
    }
    if (stepId === 'team') {
        return [
            {
                label: t('plan.master.people'),
                value: String(readiness.teamMemberCount),
                exception: readiness.teamMemberCount === 0,
            },
            {
                label: t('plan.master.totalCapacity'),
                value: t('units.hoursCompact', { count: readiness.teamCapacity }),
                exception: readiness.teamCapacity <= 0,
            },
            {
                label: t('plan.master.missingAllocation'),
                value: String(readiness.teamMembersNoCap),
                exception: readiness.teamMembersNoCap > 0,
            },
        ];
    }
    if (stepId === 'work') {
        return [
            {
                label: t('plan.master.tasksInPeriod'),
                value: String(readiness.taskCount),
                exception: readiness.taskCount === 0,
            },
            {
                label: t('plan.master.unassigned'),
                value: String(readiness.tasksWithoutAssignee),
                exception: readiness.tasksWithoutAssignee > 0,
            },
            {
                label: t('plan.master.missingEffort'),
                value: String(readiness.tasksWithoutEffort),
                exception: readiness.tasksWithoutEffort > 0,
            },
        ];
    }
    if (stepId === 'blockers') {
        return [
            {
                label: t('plan.master.unassigned'),
                value: String(readiness.tasksWithoutAssignee),
                exception: readiness.tasksWithoutAssignee > 0,
            },
            {
                label: t('plan.master.missingEffort'),
                value: String(readiness.tasksWithoutEffort),
                exception: readiness.tasksWithoutEffort > 0,
            },
            {
                label: t('plan.master.tasksInPeriod'),
                value: String(readiness.taskCount),
            },
        ];
    }
    if (stepId === 'schedule') {
        return [
            {
                label: t('plan.master.savedSchedule'),
                value: readiness.hasGanttSchedule
                    ? t('plan.master.available')
                    : t('plan.master.notAvailable'),
                exception: !readiness.hasGanttSchedule,
            },
            {
                label: t('plan.master.planningExceptions'),
                value: String(readiness.riskCount),
                exception: readiness.riskCount > 0,
            },
            {
                label: t('plan.master.tasksInPeriod'),
                value: String(readiness.taskCount),
            },
        ];
    }
    return [
        {
            label: t('plan.master.savedSchedule'),
            value: readiness.hasGanttSchedule
                ? t('plan.master.available')
                : t('plan.master.notAvailable'),
            exception: !readiness.hasGanttSchedule,
        },
        {
            label: t('plan.master.planningExceptions'),
            value: String(readiness.riskCount),
            exception: readiness.riskCount > 0,
        },
        {
            label: t('plan.master.tasksInPeriod'),
            value: String(readiness.taskCount),
        },
    ];
};

const ShareCheckpoint = ({
    share,
    loading,
    error,
    pending,
    onRetry,
    onCreate,
    onCopy,
    onRefresh,
    onRevoke,
}: {
    share: PlanShare | null;
    loading: boolean;
    error: unknown;
    pending: boolean;
    onRetry: () => void;
    onCreate: () => void;
    onCopy: () => void;
    onRefresh: () => void;
    onRevoke: () => void;
}) => {
    const { t, i18n } = useTranslation();
    if (loading) {
        return <QueryLoadingState message={t('plan.master.loadingShareLink')} />;
    }
    if (error) {
        return (
            <QueryErrorState
                error={error}
                title={t('plan.master.shareLinkUnavailable')}
                fallback={t('plan.master.shareLinkUnavailableBody')}
                onRetry={pending ? undefined : onRetry}
            />
        );
    }
    if (!share) {
        return (
            <section className="plan-checkpoint-share" aria-labelledby="plan-share-heading">
                <div>
                    <h3 id="plan-share-heading">{t('plan.master.readyToShareTitle')}</h3>
                    <p>{t('plan.master.readyToShareBody')}</p>
                </div>
                <button type="button" className="btn" disabled={pending} onClick={onCreate}>
                    <Share2 aria-hidden="true" size={14} />
                    {pending
                        ? t('plan.master.creatingShareLink')
                        : t('plan.master.createShareLink')}
                </button>
            </section>
        );
    }

    const shareUrl = `${window.location.origin}/plan/share/${share.public_id}`;
    return (
        <section className="plan-checkpoint-share active" aria-labelledby="plan-share-heading">
            <div className="plan-checkpoint-share-copy">
                <h3 id="plan-share-heading">{t('plan.master.planSharedTitle')}</h3>
                <p>
                    {t('plan.master.planSharedBody', {
                        date: formatDateTime(share.created_at, i18n.language),
                    })}
                </p>
                <label className="plan-share-link-field">
                    {t('plan.master.shareLinkLabel')}
                    <input value={shareUrl} readOnly />
                </label>
            </div>
            <div className="plan-checkpoint-share-actions">
                <button type="button" className="btn" disabled={pending} onClick={onCopy}>
                    <Copy aria-hidden="true" size={14} />
                    {t('plan.master.copyShareLink')}
                </button>
                <a className="btn ghost" href={shareUrl} target="_blank" rel="noreferrer">
                    <ExternalLink aria-hidden="true" size={14} />
                    {t('plan.master.openSharedPlan')}
                </a>
                <button type="button" className="btn ghost" disabled={pending} onClick={onRefresh}>
                    <RefreshCw aria-hidden="true" size={14} />
                    {t('plan.master.refreshShareSnapshot')}
                </button>
                <button type="button" className="btn danger" disabled={pending} onClick={onRevoke}>
                    {t('plan.master.revokeShareLink')}
                </button>
            </div>
        </section>
    );
};

const StepCheckpoint = ({
    stepId,
    status,
    readiness,
    dataState,
    share,
    shareLoading,
    shareError,
    sharePending,
    onRetryShare,
    onCreateShare,
    onCopyShare,
    onRefreshShare,
    onRevokeShare,
}: {
    stepId: string;
    status: Record<string, StepStatus>;
    readiness: PlanReadiness;
    dataState?: StepDataState;
    share: PlanShare | null;
    shareLoading: boolean;
    shareError: unknown;
    sharePending: boolean;
    onRetryShare: () => void;
    onCreateShare: () => void;
    onCopyShare: () => void;
    onRefreshShare: () => void;
    onRevokeShare: () => void;
}) => {
    const { t, i18n } = useTranslation();
    const definition = STEP_DEFS.find(step => step.id === stepId) ?? STEP_DEFS[0]!;
    const stepStatus = status[definition.id];
    const firstIncompleteId = nextStep(status);
    const actionStep = stepStatus.state === 'blocked'
        ? STEP_DEFS.find(step => step.id === firstIncompleteId) ?? definition
        : definition;
    const actionHref = withPlanMasterReturn(
        actionStep.route,
        definition.id as PlanningStepId,
    );
    const evidence = getStepEvidence(definition.id, readiness, t, i18n.language);
    const exceptionEvidence = evidence.filter(item => item.exception);
    const visibleEvidence = exceptionEvidence.length > 0
        ? [
            ...exceptionEvidence,
            ...evidence.filter(item => !item.exception).slice(0, 1),
        ]
        : evidence.slice(0, 2);
    const headingRef = useRef<HTMLHeadingElement>(null);
    const previousStepRef = useRef(stepId);

    useEffect(() => {
        if (previousStepRef.current !== stepId) {
            headingRef.current?.focus();
            previousStepRef.current = stepId;
        }
    }, [stepId]);

    const unavailable = Boolean(dataState?.error);
    const loading = Boolean(dataState?.loading && !dataState.error);
    return (
        <article className="plan-checkpoint">
            <header className="plan-checkpoint-header">
                <div className="plan-checkpoint-title">
                    <span className="plan-checkpoint-icon">{STEP_ICONS[definition.id]}</span>
                    <div>
                        <div className="plan-checkpoint-heading-row">
                            <h2
                                id="plan-master-active-step-heading"
                                ref={headingRef}
                                tabIndex={-1}
                            >
                                {t(`plan.steps.${definition.id}.title`)}
                            </h2>
                            <StepStatePill state={stepStatus.state} />
                        </div>
                        <p>{t(`plan.steps.${definition.id}.description`)}</p>
                    </div>
                </div>
            </header>

            {dataState?.fetching && !loading && !unavailable && (
                <div className="banner accent" role="status" aria-live="polite">
                    <RefreshCw aria-hidden="true" size={14} />
                    <span>{t('plan.master.refreshingPlanningData')}</span>
                </div>
            )}

            {loading ? (
                <QueryLoadingState
                    message={t('plan.master.sectionLoading', { section: dataState?.label })}
                />
            ) : unavailable ? (
                <QueryErrorState
                    error={dataState?.error}
                    title={t('plan.master.sectionUnavailableTitle', {
                        section: dataState?.label,
                    })}
                    fallback={t('plan.master.sectionUnavailableBody', {
                        section: dataState?.label,
                    })}
                    onRetry={dataState?.fetching
                        ? undefined
                        : () => { void dataState?.retry(); }}
                />
            ) : (
                <>
                    <section
                        className="plan-checkpoint-evidence"
                        aria-labelledby="plan-checkpoint-evidence-heading"
                    >
                        <h3 id="plan-checkpoint-evidence-heading">
                            {t('plan.master.readinessEvidence')}
                        </h3>
                        <dl>
                            {visibleEvidence.map(item => (
                                <div key={item.label} className={item.exception ? 'exception' : ''}>
                                    <dt>{item.label}</dt>
                                    <dd>{item.value}</dd>
                                </div>
                            ))}
                        </dl>
                    </section>

                    <section
                        className="plan-checkpoint-action"
                        data-blocked={stepStatus.state === 'blocked'}
                    >
                        <p>
                            {stepStatus.state === 'blocked'
                                ? t('plan.master.resolveFirst', {
                                    step: t(`plan.steps.${actionStep.id}.title`),
                                })
                                : t('plan.master.authoritativeWorkspaceBody')}
                        </p>
                        <Link className="btn primary" to={actionHref}>
                            {t(`plan.steps.${actionStep.id}.expert`)}
                            <ArrowRight aria-hidden="true" size={14} />
                        </Link>
                    </section>

                    {definition.id === 'review' && stepStatus.state !== 'blocked' && (
                        <ShareCheckpoint
                            share={share}
                            loading={shareLoading}
                            error={shareError}
                            pending={sharePending}
                            onRetry={onRetryShare}
                            onCreate={onCreateShare}
                            onCopy={onCopyShare}
                            onRefresh={onRefreshShare}
                            onRevoke={onRevokeShare}
                        />
                    )}
                </>
            )}
        </article>
    );
};

const PlanMasterPage = () => {
    const { t } = useTranslation();
    const [searchParams, setSearchParams] = useSearchParams();
    const queryClient = useQueryClient();
    const toast = useToast();
    const { requestConfirmation, confirmationDialog } = useConfirmDialog();
    const {
        currentIteration,
        readinessData,
        status: rawStatus,
        queryStates,
        isFetching,
        refetch,
    } = usePlanningReadiness();
    const [retryPending, setRetryPending] = useState(false);

    const shareQuery = useQuery({
        queryKey: ['plan-share', currentIteration?.id],
        queryFn: () => planShareService.getCurrent(currentIteration!.id),
        enabled: Boolean(currentIteration),
        retry: false,
    });
    const createShareMutation = useMutation({
        mutationFn: (iterationId: number) => planShareService.create(iterationId),
        onSuccess: share => {
            queryClient.setQueryData(['plan-share', share.iteration_id], share);
            toast.success(t('plan.master.shareLinkCreated'), {
                dedupeKey: `plan-share-created-${share.id}`,
            });
        },
    });
    const revokeShareMutation = useMutation({
        mutationFn: ({ shareId }: { shareId: number; iterationId: number }) => (
            planShareService.revoke(shareId)
        ),
        onSuccess: (_response, variables) => {
            queryClient.setQueryData(['plan-share', variables.iterationId], null);
            toast.success(t('plan.master.shareLinkRevoked'), {
                dedupeKey: 'plan-share-revoked',
            });
        },
    });

    const status = useMemo(() => {
        const localized: Record<string, StepStatus> = {
            ...localizeStatus(rawStatus, readinessData, t),
        };
        const markUnavailable = (
            query: PlanningQueryFeedback,
            affectedStepIds: string[],
            label: string,
        ) => {
            if (!query.enabled || (query.hasData && !query.isBlockingError)) return;
            const missing = query.isBlockingError
                ? t('plan.master.sectionUnavailableTitle', { section: label })
                : t('plan.master.sectionLoading', { section: label });
            affectedStepIds.forEach(stepId => {
                localized[stepId] = { state: 'blocked', missing: [missing] };
            });
        };
        markUnavailable(
            queryStates.team,
            ['team', 'schedule', 'review'],
            t('plan.steps.team.title'),
        );
        markUnavailable(
            queryStates.tasks,
            ['work', 'blockers', 'schedule', 'review'],
            t('plan.steps.work.title'),
        );
        markUnavailable(
            queryStates.gantt,
            ['schedule', 'review'],
            t('plan.steps.schedule.title'),
        );
        return localized;
    }, [queryStates.gantt, queryStates.tasks, queryStates.team, rawStatus, readinessData, t]);

    const ready = calculateReadiness(status);
    const requestedStep = searchParams.get('step');
    const stepId = isPlanningStepId(requestedStep) ? requestedStep : nextStep(status);
    const activeDefinition = STEP_DEFS.find(step => step.id === stepId) ?? STEP_DEFS[0]!;
    const hasRefetchError = Object.values(queryStates).some(query => query.isRefetchError);
    const currentShare = shareQuery.data ?? null;
    const sharePending = createShareMutation.isPending || revokeShareMutation.isPending;
    const shareError = shareQuery.error
        ?? createShareMutation.error
        ?? revokeShareMutation.error;

    const setActiveStep = useCallback((nextStepId: string) => {
        const nextParams = new URLSearchParams(searchParams);
        nextParams.set('step', nextStepId);
        setSearchParams(nextParams, { replace: true });
    }, [searchParams, setSearchParams]);

    const retryQueries = useCallback(async (queries?: PlanningQueryFeedback[]) => {
        if (retryPending) return;
        setRetryPending(true);
        try {
            if (queries) {
                await Promise.allSettled(
                    queries.filter(query => query.enabled).map(query => query.refetch()),
                );
            } else {
                await refetch();
            }
        } finally {
            setRetryPending(false);
        }
    }, [refetch, retryPending]);

    const relevantQueries = stepQueryStates(stepId, queryStates);
    const blockingStepQuery = relevantQueries.find(query => (
        query.enabled && query.isBlockingError
    ));
    const stepDataState: StepDataState | undefined = relevantQueries.length > 0
        ? {
            loading: relevantQueries.some(query => (
                query.enabled && query.isLoading && !query.hasData
            )),
            fetching: relevantQueries.some(query => query.enabled && query.isFetching),
            error: blockingStepQuery?.error ?? null,
            retry: () => retryQueries(relevantQueries),
            label: t(`plan.steps.${activeDefinition.id}.title`),
        }
        : undefined;

    const createShare = useCallback(() => {
        if (!currentIteration || sharePending) return;
        createShareMutation.mutate(currentIteration.id);
    }, [createShareMutation, currentIteration, sharePending]);

    const refreshShare = useCallback(() => {
        if (!currentIteration || sharePending) return;
        createShareMutation.mutate(currentIteration.id);
    }, [createShareMutation, currentIteration, sharePending]);

    const copyShare = useCallback(async () => {
        if (!currentShare) return;
        const shareUrl = `${window.location.origin}/plan/share/${currentShare.public_id}`;
        if (await copyText(shareUrl)) {
            toast.success(t('plan.master.shareLinkCopied'), {
                dedupeKey: `plan-share-copy-${currentShare.id}`,
            });
            return;
        }
        toast.error(t('plan.master.shareLinkCopyFailed'), {
            dedupeKey: `plan-share-copy-failed-${currentShare.id}`,
        });
    }, [currentShare, t, toast]);

    const requestShareRevoke = useCallback(() => {
        if (!currentShare || sharePending) return;
        requestConfirmation({
            title: t('plan.master.revokeShareTitle'),
            description: t('plan.master.revokeShareBody'),
            confirmLabel: t('plan.master.revokeShareLink'),
            cancelLabel: t('actions.cancel'),
            closeLabel: t('actions.close'),
            tone: 'danger',
            onConfirm: () => revokeShareMutation.mutateAsync({
                shareId: currentShare.id,
                iterationId: currentShare.iteration_id,
            }),
        });
    }, [
        currentShare,
        requestConfirmation,
        revokeShareMutation,
        sharePending,
        t,
    ]);

    if (queryStates.iterations.isLoading && !queryStates.iterations.hasData) {
        return (
            <div className="wc plan-master-full-state">
                <QueryLoadingState message={t('plan.master.planningDataLoading')} />
            </div>
        );
    }

    if (queryStates.iterations.isBlockingError) {
        return (
            <div className="wc plan-master-full-state">
                <QueryErrorState
                    error={queryStates.iterations.error}
                    title={t('plan.master.planningDataUnavailable')}
                    fallback={t('plan.master.planningDataUnavailableBody')}
                    onRetry={retryPending ? undefined : () => { void retryQueries(); }}
                />
                {confirmationDialog}
            </div>
        );
    }

    return (
        <div className="wc plan-master-page" aria-busy={isFetching || undefined}>
            <header className="plan-master-header">
                <div className="plan-master-breadcrumbs">
                    <Breadcrumbs items={[
                        { label: t('plan.title'), path: '/plan' },
                        { label: t('plan.hub.planIterationTitle') },
                    ]} />
                </div>
                <div className="plan-master-title-row">
                    <div>
                        <h1 className="wc-page-title">{t('plan.hub.planIterationTitle')}</h1>
                        <p className="wc-page-sub">{t('plan.master.checkpointPageDescription')}</p>
                    </div>
                    <p className="plan-master-period">
                        {currentIteration
                            ? currentIteration.name
                            : t('plan.master.noPeriodYet')}
                    </p>
                </div>
                <div className="plan-master-mobile-context">
                    <div className="plan-master-mobile-context-row">
                        <span>
                            {currentIteration
                                ? currentIteration.name
                                : t('plan.master.noPeriodYet')}
                        </span>
                        <span className="tnum">
                            {t('plan.master.stepsComplete', {
                                done: ready.done,
                                total: ready.total,
                            })}
                        </span>
                    </div>
                    <label className="plan-master-mobile-step-select">
                        <span>{t('plan.master.selectStep')}</span>
                        <select
                            className="input"
                            value={stepId}
                            onChange={event => setActiveStep(event.target.value)}
                        >
                            {STEP_DEFS.map((definition, index) => (
                                <option key={definition.id} value={definition.id}>
                                    {index + 1}. {t(`plan.steps.${definition.id}.title`)}
                                </option>
                            ))}
                        </select>
                    </label>
                </div>
            </header>

            {hasRefetchError && (
                <div className="banner warn plan-master-data-banner" role="status">
                    <ShieldAlert aria-hidden="true" size={14} />
                    <span>{t('plan.master.stalePlanningData')}</span>
                    <button
                        type="button"
                        className="btn sm"
                        disabled={retryPending}
                        onClick={() => { void retryQueries(); }}
                    >
                        <RefreshCw aria-hidden="true" size={12} />
                        {retryPending
                            ? t('plan.master.retryingPlanningData')
                            : t('plan.master.retryPlanningData')}
                    </button>
                </div>
            )}

            <div className="wc-master plan-master-shell">
                <aside className="wc-master-rail" aria-label={t('plan.master.steps')}>
                    <div className="plan-master-rail-summary">
                        <div>
                            <strong>{t('plan.master.stepsComplete', {
                                done: ready.done,
                                total: ready.total,
                            })}</strong>
                            <span className="tnum">{ready.pct}%</span>
                        </div>
                        <div
                            className="plan-readiness-progress"
                            role="progressbar"
                            aria-label={t('plan.master.progress')}
                            aria-valuemin={0}
                            aria-valuemax={100}
                            aria-valuenow={ready.pct}
                        >
                            <span style={{ width: `${ready.pct}%` }} />
                        </div>
                    </div>
                    <nav className="step-rail plan-master-step-rail" aria-label={t('plan.master.steps')}>
                        {STEP_DEFS.map((definition, index) => {
                            const stepStatus = status[definition.id];
                            const isCurrent = definition.id === stepId;
                            return (
                                <button
                                    type="button"
                                    key={definition.id}
                                    className={`step-item${stepStatus.state === 'done' ? ' done' : ''}${isCurrent ? ' current' : ''}`}
                                    aria-current={isCurrent ? 'step' : undefined}
                                    onClick={() => setActiveStep(definition.id)}
                                >
                                    <span className="step-num">
                                        {stepStatus.state === 'done'
                                            ? <Check aria-hidden="true" size={11} strokeWidth={3} />
                                            : index + 1}
                                    </span>
                                    <span className="step-title">
                                        {t(`plan.steps.${definition.id}.title`)}
                                    </span>
                                    <span className="sr-only">
                                        {stepStatus.state === 'done'
                                            ? t('plan.master.done')
                                            : t('plan.master.incomplete')}
                                    </span>
                                </button>
                            );
                        })}
                    </nav>
                </aside>

                <section className="wc-master-main" aria-labelledby="plan-master-active-step-heading">
                    <StepCheckpoint
                        stepId={stepId}
                        status={status}
                        readiness={readinessData}
                        dataState={stepDataState}
                        share={currentShare}
                        shareLoading={shareQuery.isLoading}
                        shareError={shareError}
                        sharePending={sharePending}
                        onRetryShare={() => {
                            createShareMutation.reset();
                            revokeShareMutation.reset();
                            void shareQuery.refetch();
                        }}
                        onCreateShare={createShare}
                        onCopyShare={() => { void copyShare(); }}
                        onRefreshShare={refreshShare}
                        onRevokeShare={requestShareRevoke}
                    />
                </section>
            </div>
            {confirmationDialog}
        </div>
    );
};

export default PlanMasterPage;

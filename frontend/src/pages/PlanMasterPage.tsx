import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import type { ReactNode, RefObject } from 'react';
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
    derivePlanningRecovery,
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
import { MasterProgress } from '../components/ui/MasterProgress';
import {
    isPlanningStepId,
    withPlanMasterReturn,
} from '../features/planningMasters/planningReturn';
import type { PlanningStepId } from '../features/planningMasters/planningReturn';
import {
    PLANNING_ITERATION_PARAM,
    planningIssueTasksHref,
} from '../features/planningMasters/planningTaskIssues';
import type {
    PlanningTaskIssue,
} from '../features/planningMasters/planningTaskIssues';
import { captureFocusOrigin, focusOwnedTarget } from '../utils/focusLifecycle';

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
    href?: string;
    actionLabel?: string;
};

type RecoveryFocusTarget = 'iterations' | 'stale' | 'step';
type ShareFocusTarget = 'ready' | 'retry' | 'shared';

interface RecoveryFocusIntent {
    origin: HTMLElement | null;
    stepId?: string;
    target: RecoveryFocusTarget;
    token: number;
}

interface ShareFocusIntent {
    origin: HTMLElement | null;
    target: ShareFocusTarget;
    token: number;
}

const STEP_ICONS: Record<string, ReactNode> = {
    iteration: <CalendarRange aria-hidden="true" />,
    team: <Users aria-hidden="true" />,
    work: <ListChecks aria-hidden="true" />,
    blockers: <ShieldAlert aria-hidden="true" />,
    schedule: <GanttChartSquare aria-hidden="true" />,
    review: <Share2 aria-hidden="true" />,
};

const STEP_STATE_LABEL_KEYS: Record<StepStatus['state'], string> = {
    done: 'plan.master.done',
    warn: 'plan.master.needsAttention',
    blocked: 'plan.master.blocked',
    todo: 'plan.master.notStarted',
};

type StepPresentationState = StepStatus['state'] | 'loading' | 'unavailable';

const STEP_PRESENTATION_LABEL_KEYS: Record<StepPresentationState, string> = {
    ...STEP_STATE_LABEL_KEYS,
    loading: 'plan.master.loadingStatus',
    unavailable: 'plan.master.unavailableStatus',
};

const stepPresentationTone = (state: StepPresentationState) => {
    if (state === 'loading') return 'todo';
    if (state === 'unavailable') return 'blocked';
    return state;
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

const presentationStateForStep = (
    stepId: string,
    state: StepStatus['state'],
    queryStates: ReturnType<typeof usePlanningReadiness>['queryStates'],
): StepPresentationState => {
    const relevantQueries = stepQueryStates(stepId, queryStates);
    if (relevantQueries.some(query => query.enabled && query.isBlockingError)) {
        return 'unavailable';
    }
    if (relevantQueries.some(query => (
        query.enabled && query.isLoading && !query.hasData
    ))) {
        return 'loading';
    }
    return state;
};

const StepStatePill = ({ state }: { state: StepPresentationState }) => {
    const { t } = useTranslation();
    const tone = stepPresentationTone(state);
    return (
        <span className={`pill ${tone === 'todo' ? 'opt' : tone}`}>
            <span className="pdot" />
            {t(STEP_PRESENTATION_LABEL_KEYS[state])}
        </span>
    );
};

const PlanMasterFullState = ({
    children,
    headingRef,
}: {
    children: ReactNode;
    headingRef: RefObject<HTMLHeadingElement | null>;
}) => {
    const { t } = useTranslation();

    return (
        <div className="wc plan-master-full-state">
            <header className="plan-master-full-state-header">
                <h1
                    ref={headingRef}
                    className="wc-page-title wc-master-focus-heading"
                    tabIndex={-1}
                >
                    {t('plan.hub.planIterationTitle')}
                </h1>
                <p className="wc-page-sub">{t('plan.master.checkpointPageDescription')}</p>
            </header>
            {children}
        </div>
    );
};

const getStepEvidence = (
    stepId: string,
    readiness: PlanReadiness,
    t: ReturnType<typeof useTranslation>['t'],
    language: string,
    iterationId: number,
): EvidenceItem[] => {
    const planningIssueEvidence = ({
        issue,
        label,
        count,
        actionKey,
    }: {
        issue: PlanningTaskIssue;
        label: string;
        count: number;
        actionKey: string;
    }): EvidenceItem => ({
        label,
        value: String(count),
        exception: count > 0,
        ...(count > 0 ? {
            href: planningIssueTasksHref({
                issue,
                iterationId,
                returnStepId: stepId as PlanningStepId,
            }),
            actionLabel: t(actionKey, { count }),
        } : {}),
    });

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
        ];
    }
    if (stepId === 'blockers') {
        return [
            planningIssueEvidence({
                issue: 'unassigned',
                label: t('plan.master.unassigned'),
                count: readiness.tasksWithoutAssignee,
                actionKey: 'plan.master.openUnassignedTasks',
            }),
            planningIssueEvidence({
                issue: 'missing-effort',
                label: t('plan.master.missingEffort'),
                count: readiness.tasksWithoutEffort,
                actionKey: 'plan.master.openMissingEffortTasks',
            }),
            {
                label: t('plan.master.tasksInPeriod'),
                value: String(readiness.taskCount),
            },
        ];
    }
    const downstreamTaskExceptions = [
        planningIssueEvidence({
            issue: 'unassigned',
            label: t('plan.master.unassigned'),
            count: readiness.tasksWithoutAssignee,
            actionKey: 'plan.master.openUnassignedTasks',
        }),
        planningIssueEvidence({
            issue: 'missing-effort',
            label: t('plan.master.missingEffort'),
            count: readiness.tasksWithoutEffort,
            actionKey: 'plan.master.openMissingEffortTasks',
        }),
    ].filter(item => item.exception);
    if (stepId === 'schedule') {
        return [
            ...downstreamTaskExceptions,
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
        ...downstreamTaskExceptions,
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
    retrying,
    readyHeadingRef,
    retryButtonRef,
    sharedHeadingRef,
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
    retrying: boolean;
    readyHeadingRef: RefObject<HTMLHeadingElement | null>;
    retryButtonRef: RefObject<HTMLButtonElement | null>;
    sharedHeadingRef: RefObject<HTMLHeadingElement | null>;
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
                headingLevel={3}
                isRetrying={retrying}
                onRetry={onRetry}
                retryButtonRef={retryButtonRef}
            />
        );
    }
    if (!share) {
        return (
            <section className="plan-checkpoint-share" aria-labelledby="plan-share-heading">
                <div>
                    <h3
                        id="plan-share-heading"
                        ref={readyHeadingRef}
                        className="wc-master-focus-heading"
                        tabIndex={-1}
                    >
                        {t('plan.master.readyToShareTitle')}
                    </h3>
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
                <h3
                    id="plan-share-heading"
                    ref={sharedHeadingRef}
                    className="wc-master-focus-heading"
                    tabIndex={-1}
                >
                    {t('plan.master.planSharedTitle')}
                </h3>
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
    headingRef,
    status,
    readiness,
    iterationId,
    dataState,
    share,
    shareLoading,
    shareError,
    sharePending,
    shareRetrying,
    shareReadyHeadingRef,
    shareRetryButtonRef,
    shareSharedHeadingRef,
    onRetryShare,
    onCreateShare,
    onCopyShare,
    onRefreshShare,
    onRevokeShare,
}: {
    stepId: string;
    headingRef: RefObject<HTMLHeadingElement | null>;
    status: Record<string, StepStatus>;
    readiness: PlanReadiness;
    iterationId: number;
    dataState?: StepDataState;
    share: PlanShare | null;
    shareLoading: boolean;
    shareError: unknown;
    sharePending: boolean;
    shareRetrying: boolean;
    shareReadyHeadingRef: RefObject<HTMLHeadingElement | null>;
    shareRetryButtonRef: RefObject<HTMLButtonElement | null>;
    shareSharedHeadingRef: RefObject<HTMLHeadingElement | null>;
    onRetryShare: () => void;
    onCreateShare: () => void;
    onCopyShare: () => void;
    onRefreshShare: () => void;
    onRevokeShare: () => void;
}) => {
    const { t, i18n } = useTranslation();
    const definition = STEP_DEFS.find(step => step.id === stepId) ?? STEP_DEFS[0]!;
    const stepStatus = status[definition.id];
    const recovery = derivePlanningRecovery(
        definition.id as PlanningStepId,
        readiness,
    );
    const actionStep = STEP_DEFS.find(step => step.id === recovery.ownerStep)
        ?? definition;
    const actionHref = recovery.planningIssue
        ? planningIssueTasksHref({
            issue: recovery.planningIssue,
            iterationId,
            returnStepId: definition.id as PlanningStepId,
        })
        : withPlanMasterReturn(
            recovery.route,
            definition.id as PlanningStepId,
            {
                ...recovery.query,
                ...(recovery.route === '/tasks' && iterationId > 0
                    ? { [PLANNING_ITERATION_PARAM]: String(iterationId) }
                    : {}),
            },
        );
    const evidence = getStepEvidence(
        definition.id,
        readiness,
        t,
        i18n.language,
        iterationId,
    );
    const exceptionEvidence = evidence.filter(item => item.exception);
    const visibleEvidence = exceptionEvidence.length > 0
        ? [
            ...exceptionEvidence,
            ...evidence.filter(item => !item.exception).slice(0, 1),
        ]
        : evidence.slice(0, 2);
    const unavailable = Boolean(dataState?.error);
    const loading = Boolean(dataState?.loading && !dataState.error);
    const presentationState: StepPresentationState = unavailable
        ? 'unavailable'
        : loading
            ? 'loading'
            : stepStatus.state;
    const assignAction = t('plan.master.assignTasks', {
        count: readiness.tasksWithoutAssignee,
    });
    const estimateAction = t('plan.master.estimateTasks', {
        count: readiness.tasksWithoutEffort,
    });
    const taskRecoverySummary = (
        readiness.tasksWithoutAssignee > 0
        && readiness.tasksWithoutEffort > 0
    )
        ? t('plan.master.taskRecoveryBoth', {
            assign: assignAction,
            estimate: estimateAction,
        })
        : readiness.tasksWithoutAssignee > 0
            ? t('plan.master.taskRecoveryUnassigned', { action: assignAction })
            : readiness.tasksWithoutEffort > 0
                ? t('plan.master.taskRecoveryEffort', { action: estimateAction })
                : null;
    const actionLabel = recovery.kind === 'repair-assignee'
        ? assignAction
        : recovery.kind === 'repair-effort'
            ? estimateAction
            : t(`plan.steps.${actionStep.id}.expert`);
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
                                className="wc-master-focus-heading"
                                tabIndex={-1}
                            >
                                {t(`plan.steps.${definition.id}.title`)}
                            </h2>
                            <StepStatePill state={presentationState} />
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
                    headingLevel={3}
                    isRetrying={dataState?.fetching}
                    onRetry={() => { void dataState?.retry(); }}
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
                                    <dd>
                                        {item.href ? (
                                            <Link
                                                className="plan-evidence-link"
                                                to={item.href}
                                                aria-label={item.actionLabel}
                                            >
                                                <span>{item.value}</span>
                                                <ArrowRight aria-hidden="true" size={13} />
                                            </Link>
                                        ) : item.value}
                                    </dd>
                                </div>
                            ))}
                        </dl>
                    </section>

                    <section
                        className="plan-checkpoint-action"
                        data-blocked={stepStatus.state === 'blocked'}
                        aria-labelledby="plan-checkpoint-next-action-heading"
                    >
                        <div>
                            <h3 id="plan-checkpoint-next-action-heading">
                                {t('plan.master.nextAction')}
                            </h3>
                            <p>
                                {recovery.planningIssue && taskRecoverySummary
                                    ? taskRecoverySummary
                                    : stepStatus.state === 'blocked'
                                    ? t('plan.master.resolveFirst', {
                                        step: t(`plan.steps.${actionStep.id}.title`),
                                    })
                                    : t('plan.master.authoritativeWorkspaceBody')}
                            </p>
                        </div>
                        <Link className="btn primary" to={actionHref}>
                            {actionLabel}
                            <ArrowRight aria-hidden="true" size={14} />
                        </Link>
                    </section>

                    {definition.id === 'review' && stepStatus.state !== 'blocked' && (
                        <ShareCheckpoint
                            share={share}
                            loading={shareLoading}
                            error={shareError}
                            pending={sharePending}
                            retrying={shareRetrying}
                            readyHeadingRef={shareReadyHeadingRef}
                            retryButtonRef={shareRetryButtonRef}
                            sharedHeadingRef={shareSharedHeadingRef}
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
    const {
        requestConfirmation,
        confirmationDialog,
        confirmationOpen,
    } = useConfirmDialog();
    const {
        currentIteration,
        readinessData,
        status: rawStatus,
        queryStates,
        isFetching,
        refetch,
    } = usePlanningReadiness();
    const [retryPending, setRetryPending] = useState(false);
    const [recoveryFocusVersion, setRecoveryFocusVersion] = useState(0);
    const [shareFocusVersion, setShareFocusVersion] = useState(0);
    const railRef = useRef<HTMLElement>(null);
    const mobileStepSelectRef = useRef<HTMLSelectElement>(null);
    const activeStepButtonRef = useRef<HTMLButtonElement>(null);
    const activeStepHeadingRef = useRef<HTMLHeadingElement>(null);
    const pageTitleRef = useRef<HTMLHeadingElement>(null);
    const pendingStepFocus = useRef<{
        origin: HTMLElement | null;
        stepId: string;
    } | null>(null);
    const recoveryFocusSequence = useRef(0);
    const pendingRecoveryFocus = useRef<RecoveryFocusIntent | null>(null);
    const recoveryInFlight = useRef(false);
    const shareFocusSequence = useRef(0);
    const pendingShareFocus = useRef<ShareFocusIntent | null>(null);
    const shareCommandInFlight = useRef(false);
    const shareRetryInFlight = useRef(false);
    const shareReadyHeadingRef = useRef<HTMLHeadingElement>(null);
    const shareRetryButtonRef = useRef<HTMLButtonElement>(null);
    const shareSharedHeadingRef = useRef<HTMLHeadingElement>(null);

    useEffect(() => {
        if (typeof window.matchMedia !== 'function') return undefined;
        const mobileLayout = window.matchMedia('(max-width: 768px)');
        const preserveStepFocus = (event: MediaQueryListEvent) => {
            const activeElement = document.activeElement;
            if (event.matches && railRef.current?.contains(activeElement)) {
                mobileStepSelectRef.current?.focus();
            } else if (
                !event.matches
                && activeElement === mobileStepSelectRef.current
            ) {
                activeStepButtonRef.current?.focus();
            }
        };
        mobileLayout.addEventListener('change', preserveStepFocus);
        return () => mobileLayout.removeEventListener('change', preserveStepFocus);
    }, []);

    const shareQuery = useQuery({
        queryKey: ['plan-share', currentIteration?.id],
        queryFn: () => planShareService.getCurrent(currentIteration!.id),
        enabled: Boolean(currentIteration),
        retry: false,
    });

    const beginShareFocus = useCallback((
        target: ShareFocusTarget,
        origin = captureFocusOrigin(),
    ) => {
        const token = shareFocusSequence.current + 1;
        shareFocusSequence.current = token;
        pendingShareFocus.current = { origin, target, token };
        return token;
    }, []);

    const settleShareFocus = useCallback((token: number, target: ShareFocusTarget) => {
        if (pendingShareFocus.current?.token !== token) return;
        pendingShareFocus.current = {
            ...pendingShareFocus.current,
            target,
        };
        setShareFocusVersion(current => current + 1);
    }, []);

    const cancelShareFocus = useCallback((token: number) => {
        if (pendingShareFocus.current?.token === token) {
            pendingShareFocus.current = null;
        }
    }, []);

    const createShareMutation = useMutation({
        mutationFn: ({
            iterationId,
        }: {
            command: 'create' | 'refresh';
            focusToken: number;
            iterationId: number;
        }) => planShareService.create(iterationId),
        onSuccess: (share, variables) => {
            queryClient.setQueryData(['plan-share', share.iteration_id], share);
            toast.success(t(
                variables.command === 'refresh'
                    ? 'plan.master.shareLinkRefreshed'
                    : 'plan.master.shareLinkCreated',
            ), {
                dedupeKey: `plan-share-${variables.command}-${share.id}`,
            });
            if (variables.command === 'create') {
                settleShareFocus(variables.focusToken, 'shared');
            } else {
                cancelShareFocus(variables.focusToken);
            }
        },
        onError: (_error, variables) => {
            settleShareFocus(variables.focusToken, 'retry');
        },
        onSettled: () => {
            shareCommandInFlight.current = false;
        },
    });
    const revokeShareMutation = useMutation({
        mutationFn: ({
            shareId,
        }: {
            focusToken: number;
            iterationId: number;
            shareId: number;
        }) => (
            planShareService.revoke(shareId)
        ),
        onSuccess: (_response, variables) => {
            queryClient.setQueryData(['plan-share', variables.iterationId], null);
            toast.success(t('plan.master.shareLinkRevoked'), {
                dedupeKey: 'plan-share-revoked',
            });
            settleShareFocus(variables.focusToken, 'ready');
        },
        onError: (_error, variables) => {
            settleShareFocus(variables.focusToken, 'retry');
        },
        onSettled: () => {
            shareCommandInFlight.current = false;
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
    const shareRetrying = shareQuery.isFetching && !shareQuery.isLoading;
    const shareError = shareQuery.error
        ?? createShareMutation.error
        ?? revokeShareMutation.error;

    useEffect(() => {
        const intent = pendingStepFocus.current;
        if (!intent || intent.stepId !== stepId) return;

        focusOwnedTarget(intent.origin, activeStepHeadingRef.current);
        pendingStepFocus.current = null;
    }, [stepId]);

    useEffect(() => {
        const intent = pendingShareFocus.current;
        if (!intent || confirmationOpen) return;

        const target = intent.target === 'ready'
            ? shareReadyHeadingRef.current
            : intent.target === 'shared'
                ? shareSharedHeadingRef.current
                : shareRetryButtonRef.current;
        focusOwnedTarget(
            intent.origin,
            target ?? activeStepHeadingRef.current ?? pageTitleRef.current,
        );
        pendingShareFocus.current = null;
    }, [confirmationOpen, currentShare, shareError, shareFocusVersion]);

    const setActiveStep = useCallback((
        nextStepId: string,
        origin = captureFocusOrigin(),
    ) => {
        if (nextStepId === stepId) return;
        pendingStepFocus.current = { origin, stepId: nextStepId };
        const nextParams = new URLSearchParams(searchParams);
        nextParams.set('step', nextStepId);
        setSearchParams(nextParams, { replace: true });
    }, [searchParams, setSearchParams, stepId]);

    const retryQueries = useCallback(async (
        queries: PlanningQueryFeedback[] | undefined,
        target: RecoveryFocusTarget,
    ) => {
        if (retryPending || recoveryInFlight.current) return;
        const token = recoveryFocusSequence.current + 1;
        recoveryFocusSequence.current = token;
        pendingRecoveryFocus.current = {
            origin: captureFocusOrigin(),
            stepId: target === 'iterations' ? undefined : stepId,
            target,
            token,
        };
        recoveryInFlight.current = true;
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
            recoveryInFlight.current = false;
            setRetryPending(false);
            setRecoveryFocusVersion(current => current + 1);
        }
    }, [refetch, retryPending, stepId]);

    const relevantQueries = stepQueryStates(stepId, queryStates);
    const blockingStepQuery = relevantQueries.find(query => (
        query.enabled && query.isBlockingError
    ));
    const stepDataState: StepDataState | undefined = relevantQueries.length > 0
        ? {
            loading: relevantQueries.some(query => (
                query.enabled && query.isLoading && !query.hasData
            )),
            fetching: retryPending || relevantQueries.some(query => (
                query.enabled && query.isFetching
            )),
            error: blockingStepQuery?.error ?? null,
            retry: () => retryQueries(relevantQueries, 'step'),
            label: t(`plan.steps.${activeDefinition.id}.title`),
        }
        : undefined;

    useEffect(() => {
        const intent = pendingRecoveryFocus.current;
        if (!intent || retryPending) return;

        const recovered = intent.target === 'iterations'
            ? !queryStates.iterations.isBlockingError
            : intent.target === 'stale'
                ? !hasRefetchError
                : !blockingStepQuery;
        const target = recovered
            ? intent.target === 'iterations'
                ? pageTitleRef.current
                : activeStepHeadingRef.current
            : intent.origin;

        focusOwnedTarget(intent.origin, target);
        pendingRecoveryFocus.current = null;
    }, [
        blockingStepQuery,
        hasRefetchError,
        queryStates.iterations.isBlockingError,
        recoveryFocusVersion,
        retryPending,
        stepId,
    ]);

    const createShare = useCallback(() => {
        if (!currentIteration || sharePending || shareCommandInFlight.current) return;
        shareCommandInFlight.current = true;
        const focusToken = beginShareFocus('shared');
        createShareMutation.mutate({
            command: 'create',
            focusToken,
            iterationId: currentIteration.id,
        });
    }, [beginShareFocus, createShareMutation, currentIteration, sharePending]);

    const refreshShare = useCallback(() => {
        if (!currentIteration || sharePending || shareCommandInFlight.current) return;
        shareCommandInFlight.current = true;
        const focusToken = beginShareFocus('shared');
        createShareMutation.mutate({
            command: 'refresh',
            focusToken,
            iterationId: currentIteration.id,
        });
    }, [beginShareFocus, createShareMutation, currentIteration, sharePending]);

    const retryShare = useCallback(async () => {
        if (shareRetrying || shareRetryInFlight.current) return;
        shareRetryInFlight.current = true;
        const focusToken = beginShareFocus(currentShare ? 'shared' : 'ready');
        try {
            const result = await shareQuery.refetch();
            if (result.isError) {
                settleShareFocus(focusToken, 'retry');
                return;
            }
            createShareMutation.reset();
            revokeShareMutation.reset();
            settleShareFocus(focusToken, result.data ? 'shared' : 'ready');
        } catch {
            settleShareFocus(focusToken, 'retry');
        } finally {
            shareRetryInFlight.current = false;
        }
    }, [
        beginShareFocus,
        createShareMutation,
        currentShare,
        revokeShareMutation,
        settleShareFocus,
        shareQuery,
        shareRetrying,
    ]);

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
        if (!currentShare || sharePending || shareCommandInFlight.current) return;
        requestConfirmation({
            title: t('plan.master.revokeShareTitle'),
            description: t('plan.master.revokeShareBody'),
            confirmLabel: t('plan.master.revokeShareLink'),
            cancelLabel: t('actions.cancel'),
            closeLabel: t('actions.close'),
            tone: 'danger',
            onConfirm: () => {
                if (shareCommandInFlight.current) return Promise.resolve();
                shareCommandInFlight.current = true;
                const focusToken = beginShareFocus('ready');
                return revokeShareMutation.mutateAsync({
                    focusToken,
                    shareId: currentShare.id,
                    iterationId: currentShare.iteration_id,
                });
            },
        });
    }, [
        beginShareFocus,
        currentShare,
        requestConfirmation,
        revokeShareMutation,
        sharePending,
        t,
    ]);

    if (queryStates.iterations.isLoading && !queryStates.iterations.hasData) {
        return (
            <PlanMasterFullState headingRef={pageTitleRef}>
                <QueryLoadingState message={t('plan.master.planningDataLoading')} />
            </PlanMasterFullState>
        );
    }

    if (queryStates.iterations.isBlockingError) {
        return (
            <PlanMasterFullState headingRef={pageTitleRef}>
                <QueryErrorState
                    error={queryStates.iterations.error}
                    title={t('plan.master.planningDataUnavailable')}
                    fallback={t('plan.master.planningDataUnavailableBody')}
                    headingLevel={2}
                    isRetrying={retryPending}
                    onRetry={() => { void retryQueries(undefined, 'iterations'); }}
                />
                {confirmationDialog}
            </PlanMasterFullState>
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
                        <h1
                            ref={pageTitleRef}
                            className="wc-page-title wc-master-focus-heading"
                            tabIndex={-1}
                        >
                            {t('plan.hub.planIterationTitle')}
                        </h1>
                        <p className="wc-page-sub">{t('plan.master.checkpointPageDescription')}</p>
                    </div>
                    <p className="plan-master-period">
                        {currentIteration
                            ? currentIteration.name
                            : t('plan.master.noPeriodYet')}
                    </p>
                </div>
                <section
                    className="plan-master-mobile-context"
                    aria-labelledby="plan-master-mobile-readiness-heading"
                >
                    <h2
                        id="plan-master-mobile-readiness-heading"
                        className="plan-master-mobile-context-title"
                    >
                        {t('plan.master.planReadiness')}
                    </h2>
                    <div className="plan-master-mobile-context-row">
                        <span>
                            {currentIteration
                                ? currentIteration.name
                                : t('plan.master.noPeriodYet')}
                        </span>
                        <span className="tnum" aria-hidden="true">
                            {t('plan.master.checkpointsComplete', {
                                done: ready.done,
                                total: ready.total,
                            })}
                        </span>
                    </div>
                    <MasterProgress
                        className="plan-master-mobile-progress"
                        completed={ready.done}
                        label={t('plan.master.summaryProgress')}
                        total={ready.total}
                        valueText={t('plan.master.checkpointsComplete', {
                            done: ready.done,
                            total: ready.total,
                        })}
                    />
                    <label className="plan-master-mobile-step-select">
                        <span>{t('plan.master.selectCheckpoint')}</span>
                        <select
                            ref={mobileStepSelectRef}
                            className="input"
                            value={stepId}
                            onChange={event => setActiveStep(
                                event.target.value,
                                event.currentTarget,
                            )}
                        >
                            {STEP_DEFS.map((definition, index) => {
                                const stepStatus = status[definition.id];
                                const presentationState = presentationStateForStep(
                                    definition.id,
                                    stepStatus.state,
                                    queryStates,
                                );
                                return (
                                    <option key={definition.id} value={definition.id}>
                                        {t('plan.master.checkpointOption', {
                                            checkpoint: t(`plan.steps.${definition.id}.title`),
                                            index: index + 1,
                                            state: t(
                                                STEP_PRESENTATION_LABEL_KEYS[presentationState],
                                            ),
                                        })}
                                    </option>
                                );
                            })}
                        </select>
                    </label>
                </section>
            </header>

            {hasRefetchError && (
                <div className="banner warn plan-master-data-banner" role="status">
                    <ShieldAlert aria-hidden="true" size={14} />
                    <span>{t('plan.master.stalePlanningData')}</span>
                    <button
                        type="button"
                        className="btn sm"
                        disabled={retryPending}
                        onClick={() => { void retryQueries(undefined, 'stale'); }}
                    >
                        <RefreshCw aria-hidden="true" size={12} />
                        {retryPending
                            ? t('plan.master.retryingPlanningData')
                            : t('plan.master.retryPlanningData')}
                    </button>
                </div>
            )}

            <div className="wc-master plan-master-shell">
                <aside
                    ref={railRef}
                    className="wc-master-rail"
                    aria-labelledby="plan-master-readiness-heading"
                >
                    <header className="wc-master-rail-head">
                        <h2
                            id="plan-master-readiness-heading"
                            className="wc-master-rail-title"
                        >
                            {t('plan.master.planReadiness')}
                        </h2>
                        <p className="wc-master-rail-progress-text" aria-hidden="true">
                            {t('plan.master.checkpointsComplete', {
                                done: ready.done,
                                total: ready.total,
                            })}
                        </p>
                        <MasterProgress
                            completed={ready.done}
                            label={t('plan.master.railProgress')}
                            total={ready.total}
                            valueText={t('plan.master.checkpointsComplete', {
                                done: ready.done,
                                total: ready.total,
                            })}
                        />
                    </header>
                    <nav aria-label={t('plan.master.checkpoints')}>
                        <ol className="step-rail plan-master-step-rail">
                            {STEP_DEFS.map((definition, index) => {
                                const stepStatus = status[definition.id];
                                const presentationState = presentationStateForStep(
                                    definition.id,
                                    stepStatus.state,
                                    queryStates,
                                );
                                const tone = stepPresentationTone(presentationState);
                                const isCurrent = definition.id === stepId;
                                return (
                                    <li key={definition.id}>
                                        <button
                                            ref={isCurrent ? activeStepButtonRef : undefined}
                                            type="button"
                                            className={`step-item ${tone}${isCurrent ? ' current' : ''}`}
                                            aria-current={isCurrent ? 'step' : undefined}
                                            onClick={event => setActiveStep(
                                                definition.id,
                                                event.currentTarget,
                                            )}
                                        >
                                            <span className="step-num">
                                                {tone === 'done'
                                                    ? <Check aria-hidden="true" size={11} strokeWidth={3} />
                                                    : index + 1}
                                            </span>
                                            <span className="step-title">
                                                {t(`plan.steps.${definition.id}.title`)}
                                            </span>
                                            <span className="sr-only">
                                                {t(
                                                    STEP_PRESENTATION_LABEL_KEYS[
                                                        presentationState
                                                    ],
                                                )}
                                            </span>
                                        </button>
                                    </li>
                                );
                            })}
                        </ol>
                    </nav>
                </aside>

                <section className="wc-master-main" aria-labelledby="plan-master-active-step-heading">
                    <StepCheckpoint
                        stepId={stepId}
                        headingRef={activeStepHeadingRef}
                        status={status}
                        readiness={readinessData}
                        iterationId={currentIteration?.id ?? 0}
                        dataState={stepDataState}
                        share={currentShare}
                        shareLoading={shareQuery.isLoading}
                        shareError={shareError}
                        sharePending={sharePending}
                        shareRetrying={shareRetrying}
                        shareReadyHeadingRef={shareReadyHeadingRef}
                        shareRetryButtonRef={shareRetryButtonRef}
                        shareSharedHeadingRef={shareSharedHeadingRef}
                        onRetryShare={() => {
                            void retryShare();
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

import { useEffect, useMemo, useRef, useState } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import axios from 'axios';
import {
    Check,
    ChevronDown,
    CircleAlert,
    FileJson,
    KeyRound,
    LoaderCircle,
    RefreshCw,
    ShieldCheck,
} from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { Breadcrumbs } from '../components/layout/Breadcrumbs';
import { AdminAccessGate } from '../components/settings/AdminAccessGate';
import { MasterProgress } from '../components/ui/MasterProgress';
import {
    AGENT_TEAM_STEP_DEFINITIONS,
    stateTone,
} from '../features/agentTeamSetup/masters';
import type { AgentTeamStepId } from '../features/agentTeamSetup/masters';
import { parseAgentTeamMasterEditor } from '../features/agentTeamSetup/manifest';
import {
    deriveAgentTeamStatusScopes,
    type RuntimeReadinessState,
    type SessionAuthorityState,
    type TopologyConfigurationState,
} from '../features/agentTeamSetup/statusScopes';
import { useAgentTeamReadiness } from '../features/agentTeamSetup/useAgentTeamReadiness';
import { agentService } from '../services/agentService';
import type {
    AgentTeamApplyResponse,
    AgentTeamMaster,
    AgentTeamPlan,
    AgentTeamPlanAction,
    AgentTeamValidation,
} from '../types/agent';
import { captureFocusOrigin, focusOwnedTarget } from '../utils/focusLifecycle';
import { formatDateTime } from '../utils/formatDate';

const errorMessage = (error: unknown): string => {
    if (axios.isAxiosError(error)) {
        const detail = error.response?.data?.detail;
        if (typeof detail === 'string') return detail;
        if (detail && typeof detail === 'object') {
            const code = 'code' in detail ? String(detail.code) : '';
            const message = 'message' in detail ? String(detail.message) : '';
            return [code, message].filter(Boolean).join(': ');
        }
    }
    return error instanceof Error ? error.message : String(error);
};

const actionCanApply = (action: AgentTeamPlanAction): boolean => ![
    'blocked',
    'no_change',
    'unmanaged',
].includes(action.operation);

type StatusTone = 'done' | 'warn' | 'blocked' | 'opt' | 'accent';
type AgentTeamStepScope = 'authority' | 'topology' | 'runtime';

const topologyTone: Record<TopologyConfigurationState, StatusTone> = {
    unavailable: 'opt',
    notConfigured: 'warn',
    reconciliationNeeded: 'warn',
    configured: 'done',
    disabled: 'opt',
};

const authorityTone: Record<SessionAuthorityState, StatusTone> = {
    checking: 'opt',
    unverified: 'warn',
    readOnly: 'opt',
    changesAllowed: 'done',
};

const runtimeTone: Record<RuntimeReadinessState, StatusTone> = {
    unknown: 'opt',
    blocked: 'blocked',
    onboarding: 'warn',
    ready: 'done',
    disabled: 'opt',
};

const stepScope = (stepId: string): AgentTeamStepScope => {
    if (stepId === 'authority') return 'authority';
    if (stepId === 'review') return 'runtime';
    return 'topology';
};

const AGENT_TEAM_STEP_SCOPES: AgentTeamStepScope[] = [
    'authority',
    'topology',
    'runtime',
];

const AGENT_TEAM_OPERATION_KEYS: Record<string, string> = {
    create_member: 'agentTeamSetup.operations.createMember',
    adopt_member: 'agentTeamSetup.operations.adoptMember',
    update_member: 'agentTeamSetup.operations.updateMember',
    no_change: 'agentTeamSetup.operations.noChange',
    disable_member: 'agentTeamSetup.operations.disableMember',
    replace_member: 'agentTeamSetup.operations.replaceMember',
    blocked: 'agentTeamSetup.operations.blocked',
    unmanaged: 'agentTeamSetup.operations.unmanaged',
};

const AGENT_TEAM_RECONCILIATION_KEYS: Record<
    AgentTeamPlanAction['reconciliation_class'],
    string
> = {
    create: 'agentTeamSetup.reconciliationClasses.create',
    safe_update: 'agentTeamSetup.reconciliationClasses.safeUpdate',
    no_change: 'agentTeamSetup.reconciliationClasses.noChange',
    blocked_conflict: 'agentTeamSetup.reconciliationClasses.blockedConflict',
    requires_replacement: 'agentTeamSetup.reconciliationClasses.requiresReplacement',
    propose_disable: 'agentTeamSetup.reconciliationClasses.proposeDisable',
    unmanaged: 'agentTeamSetup.reconciliationClasses.unmanaged',
};

const AGENT_TEAM_APPLY_STATUS_KEYS: Record<
    AgentTeamApplyResponse['status'],
    string
> = {
    completed: 'agentTeamSetup.applyStatuses.completed',
    partial: 'agentTeamSetup.applyStatuses.partial',
    blocked: 'agentTeamSetup.applyStatuses.blocked',
};

const AGENT_TEAM_APPLY_STATUS_TONES: Record<
    AgentTeamApplyResponse['status'],
    StatusTone
> = {
    completed: 'done',
    partial: 'warn',
    blocked: 'blocked',
};

type AgentTeamActionReceiptStatus = AgentTeamApplyResponse['receipts'][number]['status'];
type WorkflowFocusTarget = 'plan' | 'receipt';

interface WorkflowFocusIntent {
    origin: HTMLElement | null;
    target: WorkflowFocusTarget;
    token: number;
}

const AGENT_TEAM_ACTION_STATUS_KEYS: Record<
    AgentTeamActionReceiptStatus,
    string
> = {
    pending: 'agentTeamSetup.actionStatuses.pending',
    applied: 'agentTeamSetup.actionStatuses.applied',
    no_change: 'agentTeamSetup.actionStatuses.noChange',
    blocked: 'agentTeamSetup.actionStatuses.blocked',
};

const AGENT_TEAM_ACTION_STATUS_TONES: Record<
    AgentTeamActionReceiptStatus,
    StatusTone
> = {
    pending: 'warn',
    applied: 'done',
    no_change: 'opt',
    blocked: 'blocked',
};

const AgentTeamStepList = ({
    currentStepId,
    idPrefix,
    steps,
}: {
    currentStepId: AgentTeamStepId | null;
    idPrefix: string;
    steps: ReturnType<typeof useAgentTeamReadiness>['steps'];
}) => {
    const { t } = useTranslation();

    return (
        <ol className="agent-team-step-groups">
            {AGENT_TEAM_STEP_SCOPES.map(scope => {
                const definitions = AGENT_TEAM_STEP_DEFINITIONS.filter(
                    definition => stepScope(definition.id) === scope,
                );
                const labelId = `${idPrefix}-${scope}-label`;
                return (
                    <li key={scope} className="agent-team-step-group">
                        <h3 id={labelId} className="agent-team-step-scope">
                            {t(`agentTeamSetup.statusScopes.${scope}.title`)}
                        </h3>
                        <ol
                            className="step-rail agent-team-setup-steps"
                            aria-labelledby={labelId}
                        >
                            {definitions.map(definition => {
                                const index = AGENT_TEAM_STEP_DEFINITIONS.findIndex(
                                    candidate => candidate.id === definition.id,
                                );
                                const step = steps[definition.id];
                                const tone = stateTone(step?.state);
                                return (
                                    <li
                                        key={definition.id}
                                        className={`step-item ${tone}`}
                                        aria-current={
                                            currentStepId === definition.id
                                                ? 'step'
                                                : undefined
                                        }
                                    >
                                        <span className="step-num">
                                            {tone === 'done'
                                                ? <Check size={11} aria-hidden="true" />
                                                : index + 1}
                                        </span>
                                        <span>
                                            <span className="step-title">
                                                {t(definition.titleKey)}
                                            </span>
                                            <span className="step-sub">
                                                {step && step.state !== 'done'
                                                    ? t(`agentTeamSetup.steps.${definition.id}.action`)
                                                    : t(definition.descriptionKey)}
                                            </span>
                                        </span>
                                        <span className={`pill sm ${tone}`}>
                                            {t(`agentTeamSetup.stepStates.${tone}`)}
                                        </span>
                                    </li>
                                );
                            })}
                        </ol>
                    </li>
                );
            })}
        </ol>
    );
};

const newCommandId = (prefix: string): string => (
    typeof crypto !== 'undefined' && 'randomUUID' in crypto
        ? `${prefix}-${crypto.randomUUID()}`
        : `${prefix}-${Date.now().toString(36)}`
);

const AgentTeamSetupMasterPage = () => {
    const { i18n, t } = useTranslation();
    const queryClient = useQueryClient();
    const readiness = useAgentTeamReadiness();
    const fileInput = useRef<HTMLInputElement>(null);
    const planHeadingRef = useRef<HTMLHeadingElement>(null);
    const receiptHeadingRef = useRef<HTMLHeadingElement>(null);
    const workflowRegionRef = useRef<HTMLElement>(null);
    const workflowFocusSequence = useRef(0);
    const pendingWorkflowFocus = useRef<WorkflowFocusIntent | null>(null);
    const pendingStatusRecoveryFocus = useRef<HTMLElement | null>(null);
    const commandInFlight = useRef(false);
    const [editor, setEditor] = useState('{\n  "schema_version": "agent-team-master-v1"\n}\n');
    const [validation, setValidation] = useState<AgentTeamValidation | null>(null);
    const [plan, setPlan] = useState<AgentTeamPlan | null>(null);
    const [lastReceipt, setLastReceipt] = useState<AgentTeamApplyResponse | null>(null);
    const [localError, setLocalError] = useState<string | null>(null);
    const [rationale, setRationale] = useState(
        t('agentTeamSetup.defaultRationale'),
    );
    const rationalePristine = useRef(true);
    const [confirmations, setConfirmations] = useState<Record<string, boolean>>({});
    const [preservedStatusError, setPreservedStatusError] = useState<string | null>(null);
    const [statusRecoveryFocusVersion, setStatusRecoveryFocusVersion] = useState(0);
    const [workflowFocusVersion, setWorkflowFocusVersion] = useState(0);
    const [runtimeDetailsOpen, setRuntimeDetailsOpen] = useState(() => (
        typeof window === 'undefined' || typeof window.matchMedia !== 'function'
            ? true
            : !window.matchMedia('(max-width: 1100px)').matches
    ));
    const idempotencyKeys = useRef<Record<string, string>>({});

    useEffect(() => {
        const intent = pendingWorkflowFocus.current;
        if (!intent) return;

        const target = (
            intent.target === 'plan' && plan
                ? planHeadingRef.current
                : intent.target === 'receipt' && lastReceipt
                    ? receiptHeadingRef.current
                    : null
        ) ?? workflowRegionRef.current;
        focusOwnedTarget(intent.origin, target);
        pendingWorkflowFocus.current = null;
    }, [lastReceipt, plan, workflowFocusVersion]);

    useEffect(() => {
        if (rationalePristine.current) {
            setRationale(t('agentTeamSetup.defaultRationale'));
        }
    }, [i18n.language, t]);

    const beginWorkflowFocus = (
        target: WorkflowFocusTarget,
        origin: HTMLElement | null,
    ) => {
        const token = workflowFocusSequence.current + 1;
        workflowFocusSequence.current = token;
        pendingWorkflowFocus.current = { origin, target, token };
        return token;
    };

    const cancelWorkflowFocus = (token: number) => {
        if (pendingWorkflowFocus.current?.token === token) {
            pendingWorkflowFocus.current = null;
        }
    };

    const settleWorkflowFocus = (token: number) => {
        if (pendingWorkflowFocus.current?.token === token) {
            setWorkflowFocusVersion(current => current + 1);
        }
    };

    // feedback-policy: mutation pending,inline
    const validateMutation = useMutation({
        mutationFn: (manifest: AgentTeamMaster) => (
            agentService.validateAgentTeamMaster(manifest)
        ),
        onSuccess: result => {
            setValidation(result);
            setPlan(null);
            setLastReceipt(null);
            setLocalError(null);
        },
        onError: error => setLocalError(errorMessage(error)),
        onSettled: () => {
            commandInFlight.current = false;
        },
    });

    // feedback-policy: mutation pending,inline
    const planMutation = useMutation({
        mutationFn: ({
            manifest,
        }: {
            focusToken: number;
            manifest: AgentTeamMaster;
        }) => (
            agentService.planAgentTeamMaster(
                manifest,
                readiness.status?.topology_revision ?? 0,
            )
        ),
        onSuccess: (result, variables) => {
            if (pendingWorkflowFocus.current?.token !== variables.focusToken) return;
            setPlan(result);
            setConfirmations({});
            setLastReceipt(null);
            setLocalError(null);
            settleWorkflowFocus(variables.focusToken);
        },
        onError: (error, variables) => {
            cancelWorkflowFocus(variables.focusToken);
            setLocalError(errorMessage(error));
        },
        onSettled: () => {
            commandInFlight.current = false;
        },
    });

    // feedback-policy: mutation pending,inline
    const applyMutation = useMutation({
        mutationFn: ({
            manifest,
            currentPlan,
            action,
        }: {
            manifest: AgentTeamMaster;
            currentPlan: AgentTeamPlan;
            action: AgentTeamPlanAction;
            focusToken: number;
        }) => {
            const idempotencyKey = (
                idempotencyKeys.current[action.action_id]
                ?? newCommandId(`team-${action.action_id}`)
            );
            idempotencyKeys.current[action.action_id] = idempotencyKey;
            return agentService.applyAgentTeamAction(
                manifest,
                currentPlan,
                action.action_id,
                Boolean(confirmations[action.action_id]),
                {
                    idempotencyKey,
                    rationale,
                    correlationId: newCommandId('agent-team-ui'),
                },
            );
        },
        onSuccess: async (result, variables) => {
            delete idempotencyKeys.current[variables.action.action_id];
            if (pendingWorkflowFocus.current?.token !== variables.focusToken) return;
            setLastReceipt(result);
            setPlan(null);
            setValidation(null);
            setLocalError(null);
            settleWorkflowFocus(variables.focusToken);
            await queryClient.invalidateQueries({ queryKey: ['agent-team-setup'] });
        },
        onError: (error, variables) => {
            cancelWorkflowFocus(variables.focusToken);
            setLocalError(errorMessage(error));
        },
        onSettled: () => {
            commandInFlight.current = false;
        },
    });

    const busy = validateMutation.isPending
        || planMutation.isPending
        || applyMutation.isPending;
    const canMutate = readiness.status?.can_mutate === true;
    const statusError = readiness.isError
        ? errorMessage(readiness.error)
        : preservedStatusError;
    const statusScopes = deriveAgentTeamStatusScopes({
        status: readiness.status,
        isLoading: readiness.isPending,
    });
    const lastConfirmed = readiness.dataUpdatedAt > 0
        ? formatDateTime(new Date(readiness.dataUpdatedAt), i18n.language)
        : null;

    useEffect(() => {
        const origin = pendingStatusRecoveryFocus.current;
        if (!origin || readiness.isFetching) return;

        focusOwnedTarget(
            origin,
            statusError ? origin : workflowRegionRef.current,
        );
        pendingStatusRecoveryFocus.current = null;
    }, [readiness.isFetching, statusError, statusRecoveryFocusVersion]);

    const retryStatus = async (origin: HTMLElement) => {
        if (readiness.isFetching) return;
        pendingStatusRecoveryFocus.current = origin;
        setPreservedStatusError(statusError);
        try {
            await readiness.refetch();
        } finally {
            setPreservedStatusError(null);
            setStatusRecoveryFocusVersion(current => current + 1);
        }
    };

    const currentManifest = (): AgentTeamMaster | null => {
        try {
            const manifest = parseAgentTeamMasterEditor(editor);
            setLocalError(null);
            return manifest;
        } catch (error) {
            setLocalError(errorMessage(error));
            return null;
        }
    };
    const handleValidate = () => {
        if (busy || commandInFlight.current) return;
        const manifest = currentManifest();
        if (manifest) {
            commandInFlight.current = true;
            validateMutation.mutate(manifest);
        }
    };
    const handlePlan = (origin: HTMLElement | null) => {
        if (busy || commandInFlight.current) return;
        const manifest = currentManifest();
        if (manifest) {
            commandInFlight.current = true;
            const focusToken = beginWorkflowFocus(
                'plan',
                origin ?? captureFocusOrigin(),
            );
            planMutation.mutate({ manifest, focusToken });
        }
    };
    const handleApply = (
        action: AgentTeamPlanAction,
        origin: HTMLElement | null,
    ) => {
        if (busy || commandInFlight.current) return;
        const manifest = currentManifest();
        if (!manifest || !plan) return;
        commandInFlight.current = true;
        const focusToken = beginWorkflowFocus(
            'receipt',
            origin ?? captureFocusOrigin(),
        );
        applyMutation.mutate({
            manifest,
            currentPlan: plan,
            action,
            focusToken,
        });
    };
    const loadFile = async (file: File | undefined) => {
        if (!file) return;
        try {
            const nextEditor = await file.text();
            parseAgentTeamMasterEditor(nextEditor);
            setEditor(`${JSON.stringify(JSON.parse(nextEditor), null, 2)}\n`);
            setValidation(null);
            setPlan(null);
            setLastReceipt(null);
            setLocalError(null);
            pendingWorkflowFocus.current = null;
        } catch (error) {
            setLocalError(errorMessage(error));
        } finally {
            if (fileInput.current) fileInput.current.value = '';
        }
    };

    const memberCounts = useMemo(() => ({
        ready: readiness.status?.members.filter(member => member.runtime_ready).length ?? 0,
        total: readiness.status?.members.length ?? 0,
    }), [readiness.status]);
    const confirmedProgress = readiness.progress;
    const setupComplete = Boolean(
        readiness.status
        && confirmedProgress
        && confirmedProgress.done === confirmedProgress.total,
    );
    const currentSetupDefinition = readiness.status
        ? AGENT_TEAM_STEP_DEFINITIONS.find(
            definition => readiness.steps[definition.id]?.state !== 'done',
        ) ?? null
        : null;
    const currentSetupStep = currentSetupDefinition
        ? readiness.steps[currentSetupDefinition.id]
        : null;
    const currentSetupTone = setupComplete ? 'done' : stateTone(currentSetupStep?.state);
    const currentSetupStepId = currentSetupDefinition?.id ?? null;
    const mobileBlockerCodes = currentSetupStep?.blocker_codes.length
        ? currentSetupStep.blocker_codes
        : readiness.status?.blocker_codes ?? [];
    const runtimeAction = t(`agentTeamSetup.statusScopes.runtime.actions.${
        statusScopes.topology === 'notConfigured'
            ? 'topologyRequired'
            : statusScopes.runtime
    }`);
    const progressText = confirmedProgress
        ? t('agentTeamSetup.checksComplete', {
            done: confirmedProgress.done,
            total: confirmedProgress.total,
        })
        : null;
    const operationLabel = (operation: string) => {
        const key = AGENT_TEAM_OPERATION_KEYS[operation];
        return key ? t(key) : operation;
    };

    return (
        <div className="wc agent-team-setup-page">
            <div className="wc-page-wide wc-page-stack">
                <Breadcrumbs items={[
                    { label: t('nav.settings'), path: '/settings' },
                    { label: t('agentTeamSetup.title') },
                ]} />

                <header className="wc-page-head">
                    <div className="wc-page-copy">
                        <div className="row" style={{ gap: 10 }}>
                            <ShieldCheck size={22} aria-hidden="true" />
                            <h1 className="wc-page-title">{t('agentTeamSetup.title')}</h1>
                        </div>
                        <p className="wc-page-sub">{t('agentTeamSetup.description')}</p>
                    </div>
                    <div className="wc-page-actions">
                        <button
                            type="button"
                            className="btn sm"
                            onClick={() => readiness.refetch()}
                            disabled={readiness.isFetching}
                        >
                            <RefreshCw size={13} aria-hidden="true" />
                            {readiness.isFetching
                                ? t('actions.refreshing')
                                : t('actions.refresh')}
                        </button>
                    </div>
                </header>

                <section
                    className="agent-team-status-summary"
                    aria-labelledby="agent-team-status-heading"
                    aria-busy={readiness.isFetching}
                >
                    <h2 id="agent-team-status-heading" className="sr-only">
                        {t('agentTeamSetup.statusScopes.label')}
                    </h2>
                    <dl className="agent-team-status-scopes">
                        <div className="agent-team-status-scope">
                            <dt>{t('agentTeamSetup.statusScopes.topology.title')}</dt>
                            <dd className="agent-team-status-state">
                                <span className={`pill ${topologyTone[statusScopes.topology]}`}>
                                    {t(`agentTeamSetup.statusScopes.topology.states.${statusScopes.topology}`)}
                                </span>
                            </dd>
                            <dd className="agent-team-status-evidence">
                                {readiness.status?.topology_key
                                    ? t('agentTeamSetup.statusScopes.topology.recordEvidence', {
                                        key: readiness.status.topology_key,
                                        revision: readiness.status.topology_revision ?? '—',
                                    })
                                    : t('agentTeamSetup.statusScopes.topology.noRecordEvidence')}
                            </dd>
                        </div>
                        <div className="agent-team-status-scope">
                            <dt>{t('agentTeamSetup.statusScopes.authority.title')}</dt>
                            <dd className="agent-team-status-state">
                                <span className={`pill ${authorityTone[statusScopes.authority]}`}>
                                    {t(`agentTeamSetup.statusScopes.authority.states.${statusScopes.authority}`)}
                                </span>
                            </dd>
                            <dd className="agent-team-status-evidence">
                                {t(`agentTeamSetup.statusScopes.authority.evidence.${statusScopes.authority}`)}
                            </dd>
                        </div>
                        <div className="agent-team-status-scope">
                            <dt>{t('agentTeamSetup.statusScopes.runtime.title')}</dt>
                            <dd className="agent-team-status-state">
                                <span className={`pill ${runtimeTone[statusScopes.runtime]}`}>
                                    {t(`agentTeamSetup.statusScopes.runtime.states.${statusScopes.runtime}`)}
                                </span>
                            </dd>
                            <dd className="agent-team-status-evidence">
                                {readiness.status
                                    ? t('agentTeamSetup.statusScopes.runtime.memberEvidence', {
                                        ready: memberCounts.ready,
                                        total: memberCounts.total,
                                    })
                                    : t('agentTeamSetup.statusScopes.runtime.noEvidence')}
                            </dd>
                        </div>
                    </dl>
                    <p className="agent-team-status-freshness" role="status">
                        {readiness.isFetching && !lastConfirmed
                            ? t('agentTeamSetup.statusScopes.checking')
                            : readiness.isFetching && lastConfirmed
                                ? t('agentTeamSetup.statusScopes.refreshingLastConfirmed', {
                                    date: lastConfirmed,
                                })
                            : lastConfirmed
                                ? t('agentTeamSetup.statusScopes.lastConfirmed', {
                                    date: lastConfirmed,
                                })
                                : t('agentTeamSetup.statusScopes.notConfirmed')}
                    </p>
                </section>

                {localError && (
                    <div className="card card-pad" role="alert" style={{ borderColor: 'var(--blocked-line)' }}>
                        <div className="row" style={{ alignItems: 'flex-start' }}>
                            <CircleAlert size={17} aria-hidden="true" style={{ color: 'var(--blocked)' }} />
                            <div>
                                <h2 className="wc-state-heading">
                                    {t('agentTeamSetup.errorTitle')}
                                </h2>
                                <div className="muted mono" style={{ marginTop: 4 }}>
                                    {localError}
                                </div>
                            </div>
                        </div>
                    </div>
                )}

                {statusError && (
                    <div className="card card-pad" role="alert" style={{ borderColor: 'var(--blocked-line)' }}>
                        <div className="between" style={{ alignItems: 'flex-start' }}>
                            <div className="row" style={{ alignItems: 'flex-start' }}>
                                <CircleAlert size={17} aria-hidden="true" style={{ color: 'var(--blocked)' }} />
                                <div>
                                    <h2 className="wc-state-heading">
                                        {t('agentTeamSetup.statusUnavailableTitle')}
                                    </h2>
                                    <div className="muted mono" style={{ marginTop: 4 }}>
                                        {statusError}
                                    </div>
                                </div>
                            </div>
                            <button
                                type="button"
                                className="btn sm"
                                disabled={readiness.isFetching}
                                onClick={event => {
                                    void retryStatus(event.currentTarget);
                                }}
                            >
                                <RefreshCw size={13} aria-hidden="true" />
                                {t('queryFeedback.retry')}
                            </button>
                        </div>
                    </div>
                )}

                {readiness.status && confirmedProgress && progressText && (
                    <section
                        className="agent-team-mobile-context card"
                        aria-labelledby="agent-team-mobile-readiness-title"
                    >
                        <h2 id="agent-team-mobile-readiness-title">
                            {t('agentTeamSetup.readinessTitle')}
                        </h2>
                        <div className="agent-team-mobile-context-head">
                            <div>
                                <h3>
                                    {setupComplete
                                        ? t('agentTeamSetup.setupComplete')
                                        : t('agentTeamSetup.currentCheckNamed', {
                                            check: t(currentSetupDefinition!.titleKey),
                                        })}
                                </h3>
                            </div>
                            <span className={`pill ${currentSetupTone}`}>
                                {t(`agentTeamSetup.stepStates.${currentSetupTone}`)}
                            </span>
                        </div>
                        <p className="agent-team-mobile-context-action">
                            {setupComplete
                                ? t('agentTeamSetup.allChecksCompleteBody')
                                : t(`agentTeamSetup.steps.${currentSetupDefinition!.id}.action`)}
                        </p>
                        {mobileBlockerCodes.length > 0 && (
                            <ul
                                className="agent-team-mobile-blockers"
                                aria-label={t('agentTeamSetup.blockersLabel')}
                            >
                                {mobileBlockerCodes.map(code => (
                                    <li key={code} className="pill warn mono">{code}</li>
                                ))}
                            </ul>
                        )}
                        <p className="agent-team-mobile-context-progress" aria-hidden="true">
                            {progressText}
                        </p>
                        <MasterProgress
                            completed={confirmedProgress.done}
                            label={t('agentTeamSetup.summaryProgress')}
                            total={confirmedProgress.total}
                            valueText={progressText}
                        />
                        <details className="agent-team-mobile-steps">
                            <summary aria-label={t('agentTeamSetup.allChecks')}>
                                <span>{t('agentTeamSetup.allChecks')}</span>
                                <span className="tnum" aria-hidden="true">{progressText}</span>
                            </summary>
                            <AgentTeamStepList
                                currentStepId={currentSetupStepId}
                                idPrefix="agent-team-mobile"
                                steps={readiness.steps}
                            />
                        </details>
                    </section>
                )}

                <div className="wc-master agent-team-master-layout">
                    <aside
                        className="wc-master-rail"
                        aria-labelledby="agent-team-readiness-heading"
                    >
                        <header className="wc-master-rail-head agent-team-rail-head">
                            <h2
                                id="agent-team-readiness-heading"
                                className="wc-master-rail-title"
                            >
                                {t('agentTeamSetup.readinessTitle')}
                            </h2>
                            {readiness.status && confirmedProgress && progressText ? (
                                <>
                                    <p className="wc-master-rail-progress-text" aria-hidden="true">
                                        {progressText}
                                    </p>
                                    <MasterProgress
                                        completed={confirmedProgress.done}
                                        label={t('agentTeamSetup.railProgress')}
                                        total={confirmedProgress.total}
                                        valueText={progressText}
                                    />
                                </>
                            ) : (
                                <p className="wc-master-rail-progress-text" role="status">
                                    {statusError
                                        ? t('agentTeamSetup.statusUnavailableTitle')
                                        : t('agentTeamSetup.statusScopes.checking')}
                                </p>
                            )}
                        </header>
                        {readiness.status && confirmedProgress && (
                            <AgentTeamStepList
                                currentStepId={currentSetupStepId}
                                idPrefix="agent-team-desktop"
                                steps={readiness.steps}
                            />
                        )}
                    </aside>

                    <section
                        ref={workflowRegionRef}
                        className="wc-master-main wc-master-focus-region"
                        aria-labelledby="agent-team-workflow-heading"
                        tabIndex={-1}
                    >
                        <h2 id="agent-team-workflow-heading" className="sr-only">
                            {t('agentTeamSetup.workflowTitle')}
                        </h2>
                        {readiness.isPending && !readiness.status ? (
                            <div className="card card-pad" role="status">
                                <div className="row">
                                    <LoaderCircle size={16} className="animate-spin" aria-hidden="true" />
                                    {t('agentTeamSetup.statusScopes.checking')}
                                </div>
                            </div>
                        ) : (
                        <AdminAccessGate accessGranted={canMutate} headingLevel={3}>
                            <div className="col" style={{ gap: 16 }}>
                            <section className="card card-pad">
                                <div className="between agent-team-master-panel-head">
                                    <div>
                                        <h3 className="wc-master-section-title">
                                            {t('agentTeamSetup.masterTitle')}
                                        </h3>
                                        <p className="muted" style={{ margin: '4px 0 0' }}>
                                            {t('agentTeamSetup.masterHelp')}
                                        </p>
                                    </div>
                                    <div className="row">
                                        <input
                                            ref={fileInput}
                                            type="file"
                                            accept="application/json,.json"
                                            hidden
                                            onChange={event => loadFile(event.target.files?.[0])}
                                        />
                                        <button
                                            type="button"
                                            className="btn"
                                            onClick={() => fileInput.current?.click()}
                                            disabled={!canMutate || busy}
                                        >
                                            <FileJson size={13} aria-hidden="true" />
                                            {t('agentTeamSetup.import')}
                                        </button>
                                    </div>
                                </div>
                                <div className="field" style={{ marginTop: 14 }}>
                                    <label className="field-lbl" htmlFor="agent-team-master-editor">
                                        {t('agentTeamSetup.secretFreeJson')}
                                    </label>
                                    <textarea
                                        id="agent-team-master-editor"
                                        className="input mono agent-team-master-editor"
                                        rows={18}
                                        spellCheck={false}
                                        value={editor}
                                        disabled={!canMutate || busy}
                                        onChange={event => {
                                            setEditor(event.target.value);
                                            setValidation(null);
                                            setPlan(null);
                                            setLastReceipt(null);
                                            setLocalError(null);
                                            pendingWorkflowFocus.current = null;
                                        }}
                                    />
                                    <div className="field-hint">
                                        <KeyRound size={12} aria-hidden="true" />{' '}
                                        {t('agentTeamSetup.noSecrets')}
                                    </div>
                                </div>
                                <div className="between agent-team-master-footer" style={{ marginTop: 12 }}>
                                    <div
                                        className="mono muted agent-team-technical-line"
                                        aria-live="polite"
                                    >
                                        {validation?.manifest_digest
                                            ? `${t('agentTeamSetup.digest')}: ${validation.manifest_digest}`
                                            : t('agentTeamSetup.notValidated')}
                                    </div>
                                    <div className="row agent-team-master-actions">
                                        <button
                                            type="button"
                                            className="btn"
                                            disabled={!canMutate || busy}
                                            onClick={handleValidate}
                                        >
                                            {validateMutation.isPending
                                                ? t('agentTeamSetup.validating')
                                                : t('agentTeamSetup.validate')}
                                        </button>
                                        <button
                                            type="button"
                                            className="btn primary"
                                            disabled={!canMutate || busy || validation?.valid !== true}
                                            onClick={event => handlePlan(event.currentTarget)}
                                        >
                                            {planMutation.isPending && (
                                                <LoaderCircle
                                                    size={13}
                                                    className="animate-spin"
                                                    aria-hidden="true"
                                                />
                                            )}
                                            {planMutation.isPending
                                                ? t('agentTeamSetup.planning')
                                                : t('agentTeamSetup.dryRun')}
                                        </button>
                                    </div>
                                </div>
                                {validation && validation.blocker_codes.length > 0 && (
                                    <div className="row wrap" style={{ marginTop: 10 }}>
                                        {validation.blocker_codes.map(code => (
                                            <span key={code} className="pill warn mono">{code}</span>
                                        ))}
                                    </div>
                                )}
                            </section>

                            {plan && (
                                <section className="card">
                                    <div className="card-head between">
                                        <div>
                                            <h3
                                                ref={planHeadingRef}
                                                className="wc-master-section-title wc-master-focus-heading"
                                                tabIndex={-1}
                                            >
                                                {t('agentTeamSetup.planTitle')}
                                            </h3>
                                            <div className="muted mono agent-team-technical-line">
                                                {t('agentTeamSetup.topologyRevision', {
                                                    revision: plan.expected_topology_revision,
                                                })} · {plan.plan_digest}
                                            </div>
                                        </div>
                                        <span className="pill">{plan.actions.length}</span>
                                    </div>
                                    <div className="card-pad col">
                                        {plan.actions.length > 0 ? (
                                            <div className="field">
                                                <label className="field-lbl" htmlFor="agent-team-rationale">
                                                    {t('agentTeamSetup.rationale')}
                                                </label>
                                                <input
                                                    id="agent-team-rationale"
                                                    className="input"
                                                    value={rationale}
                                                    disabled={busy}
                                                    onChange={event => {
                                                        rationalePristine.current = false;
                                                        setRationale(event.target.value);
                                                    }}
                                                />
                                            </div>
                                        ) : (
                                            <p className="muted agent-team-no-actions" role="status">
                                                {t('agentTeamSetup.noActions')}
                                            </p>
                                        )}
                                        {plan.actions.map((action, index) => {
                                            const actionHeadingId = `agent-team-plan-action-${index}`;
                                            const actionLabel = operationLabel(action.operation);
                                            const actionHeading = t(
                                                'agentTeamSetup.actionHeadingFor',
                                                {
                                                    action: actionLabel,
                                                    actionId: action.action_id,
                                                    actor: action.actor_key,
                                                },
                                            );
                                            const actionApplying = (
                                                applyMutation.isPending
                                                && applyMutation.variables?.action.action_id
                                                    === action.action_id
                                            );
                                            return (
                                            <section
                                                key={action.action_id}
                                                className="agent-team-plan-action"
                                                aria-labelledby={actionHeadingId}
                                            >
                                                <div className="between agent-team-plan-action-layout">
                                                    <div>
                                                        <h4
                                                            id={actionHeadingId}
                                                            className="agent-team-plan-action-title"
                                                        >
                                                            {actionHeading}
                                                        </h4>
                                                        <div className="row wrap">
                                                            <strong className="mono agent-team-action-id">
                                                                {action.action_id}
                                                            </strong>
                                                            <span className="pill agent-team-technical-pill">
                                                                {t(AGENT_TEAM_RECONCILIATION_KEYS[
                                                                    action.reconciliation_class
                                                                ])}
                                                            </span>
                                                            {action.authority_change && (
                                                                <span className="pill warn">
                                                                    {t('agentTeamSetup.authorityChange')}
                                                                </span>
                                                            )}
                                                        </div>
                                                        <div
                                                            className="muted mono agent-team-technical-line"
                                                            style={{ marginTop: 5 }}
                                                        >
                                                            {action.actor_key}
                                                        </div>
                                                        {action.blocker_code && (
                                                            <div className="mono" style={{ color: 'var(--blocked)', marginTop: 5 }}>
                                                                {action.blocker_code}
                                                            </div>
                                                        )}
                                                    </div>
                                                    <div className="col agent-team-plan-action-controls">
                                                        {action.requires_explicit_confirmation && (
                                                            <label className="row agent-team-action-confirmation">
                                                                <input
                                                                    type="checkbox"
                                                                    checked={Boolean(confirmations[action.action_id])}
                                                                    disabled={busy}
                                                                    onChange={event => setConfirmations(current => ({
                                                                        ...current,
                                                                        [action.action_id]: event.target.checked,
                                                                    }))}
                                                                />
                                                                {t('agentTeamSetup.confirmActionFor', {
                                                                    action: actionLabel,
                                                                    actionId: action.action_id,
                                                                    actor: action.actor_key,
                                                                })}
                                                            </label>
                                                        )}
                                                        <button
                                                            type="button"
                                                            className="btn primary"
                                                            aria-busy={actionApplying || undefined}
                                                            aria-label={t('agentTeamSetup.applyActionFor', {
                                                                action: actionLabel,
                                                                actionId: action.action_id,
                                                                actor: action.actor_key,
                                                            })}
                                                            disabled={
                                                                applyMutation.isPending
                                                                || !actionCanApply(action)
                                                                || (
                                                                    action.requires_explicit_confirmation
                                                                    && !confirmations[action.action_id]
                                                                )
                                                            }
                                                            onClick={event => handleApply(
                                                                action,
                                                                event.currentTarget,
                                                            )}
                                                        >
                                                            {actionApplying && (
                                                                <LoaderCircle
                                                                    size={13}
                                                                    className="animate-spin"
                                                                    aria-hidden="true"
                                                                />
                                                            )}
                                                            {actionApplying
                                                                ? t('agentTeamSetup.applying')
                                                                : t('agentTeamSetup.applyAction')}
                                                        </button>
                                                    </div>
                                                </div>
                                            </section>
                                            );
                                        })}
                                    </div>
                                </section>
                            )}

                            {lastReceipt && (
                                <section className="card card-pad">
                                    <h3
                                        ref={receiptHeadingRef}
                                        className="wc-master-section-title wc-master-focus-heading"
                                        tabIndex={-1}
                                    >
                                        {t('agentTeamSetup.receiptTitle')}
                                    </h3>
                                    <div className="muted agent-team-technical-line" style={{ marginTop: 6 }}>
                                        <span className="mono">{lastReceipt.apply_id}</span>
                                        {' · '}
                                        <span className={`pill sm ${AGENT_TEAM_APPLY_STATUS_TONES[lastReceipt.status]}`}>
                                            {t(AGENT_TEAM_APPLY_STATUS_KEYS[lastReceipt.status])}
                                        </span>
                                        {' · '}
                                        <span className="mono">
                                            {t('agentTeamSetup.topologyRevision', {
                                                revision: lastReceipt.resulting_topology_revision,
                                            })}
                                        </span>
                                    </div>
                                    <ul className="agent-team-receipts">
                                        {lastReceipt.receipts.map(receipt => (
                                            <li
                                                key={receipt.action_id}
                                                className={`pill agent-team-technical-pill ${
                                                    AGENT_TEAM_ACTION_STATUS_TONES[receipt.status]
                                                }`}
                                            >
                                                <span className="mono">{receipt.action_id}</span>
                                                <span aria-hidden="true">:</span>
                                                {t(AGENT_TEAM_ACTION_STATUS_KEYS[receipt.status])}
                                            </li>
                                        ))}
                                    </ul>
                                </section>
                            )}
                            </div>
                        </AdminAccessGate>
                        )}
                    </section>

                    <aside
                        className="wc-master-aux agent-team-runtime-aux"
                        aria-labelledby="agent-team-runtime-heading"
                    >
                        <h2
                            id="agent-team-runtime-heading"
                            className="wc-master-aux-scope-title"
                        >
                            {t('agentTeamSetup.runtimeDetails')}
                        </h2>
                        <details
                            className="agent-team-runtime-details"
                            open={runtimeDetailsOpen}
                            onToggle={event => setRuntimeDetailsOpen(event.currentTarget.open)}
                        >
                            <summary className="agent-team-runtime-summary">
                                <span className="agent-team-runtime-summary-copy">
                                    <strong>{t('agentTeamSetup.runtimeDetails')}</strong>
                                    <span>{runtimeAction}</span>
                                </span>
                                <span className="agent-team-runtime-summary-state">
                                    <span className={`pill ${runtimeTone[statusScopes.runtime]}`}>
                                        {t(`agentTeamSetup.statusScopes.runtime.states.${statusScopes.runtime}`)}
                                    </span>
                                    <span className="agent-team-runtime-summary-count">
                                        {t('agentTeamSetup.membersReadyCount', {
                                            ready: memberCounts.ready,
                                            total: memberCounts.total,
                                        })}
                                    </span>
                                    <ChevronDown
                                        className="agent-team-runtime-summary-chevron"
                                        size={16}
                                        aria-hidden="true"
                                    />
                                </span>
                            </summary>
                            <div className="agent-team-runtime-details-body">
                        <section className="card card-pad">
                            <h3 className="wc-master-aux-title">
                                {t('agentTeamSetup.statusScopes.topology.title')}
                            </h3>
                            <div className="between" style={{ marginTop: 10 }}>
                                <span className="muted">{t('agentTeamSetup.currentState')}</span>
                                <span className={`pill ${topologyTone[statusScopes.topology]}`}>
                                    {t(`agentTeamSetup.statusScopes.topology.states.${statusScopes.topology}`)}
                                </span>
                            </div>
                            <div className="divider" />
                            <div className="mono muted">
                                {readiness.status?.topology_key ?? t('agentTeamSetup.noTopology')}
                            </div>
                            <div className="mono muted">
                                {t('agentTeamSetup.topologyRevision', {
                                    revision: readiness.status?.topology_revision ?? '—',
                                })}
                            </div>
                            <p className="muted">
                                {readiness.status?.pending_action_ids.length
                                    ? t('agentTeamSetup.pendingReconciliationActions', {
                                        count: readiness.status.pending_action_ids.length,
                                    })
                                    : t('agentTeamSetup.topologyRecordHelp')}
                            </p>
                        </section>
                        <section className="card card-pad">
                            <div className="between">
                                <h3 className="wc-master-aux-title">
                                    {t('agentTeamSetup.statusScopes.runtime.title')}
                                </h3>
                                <span className={`pill ${runtimeTone[statusScopes.runtime]}`}>
                                    {t(`agentTeamSetup.statusScopes.runtime.states.${statusScopes.runtime}`)}
                                </span>
                            </div>
                            <div className="between" style={{ marginTop: 10 }}>
                                <span className="muted">{t('agentTeamSetup.membersReady')}</span>
                                <strong>{memberCounts.ready}/{memberCounts.total}</strong>
                            </div>
                            <p className="muted">
                                {runtimeAction}
                            </p>
                        </section>
                        {readiness.status?.members.map(member => (
                            <section key={member.actor_key} className="card card-pad">
                                <div className="between">
                                    <h3 className="agent-team-member-title">{member.display_name}</h3>
                                    <span className="pill opt">
                                        {t(`agentTeamSetup.roles.${member.role}`)}
                                    </span>
                                </div>
                                <div className="muted mono" style={{ marginTop: 5 }}>{member.actor_key}</div>
                                <dl className="agent-team-member-facts">
                                    <div>
                                        <dt>{t('agentTeamSetup.memberConfiguration')}</dt>
                                        <dd>
                                            <span className={`pill ${member.configured ? 'done' : 'warn'}`}>
                                                {t(member.configured
                                                    ? 'agentTeamSetup.configured'
                                                    : 'agentTeamSetup.notConfigured')}
                                            </span>
                                        </dd>
                                    </div>
                                    <div>
                                        <dt>{t('agentTeamSetup.statusScopes.runtime.title')}</dt>
                                        <dd>
                                            <span className={`pill ${member.runtime_ready ? 'done' : 'blocked'}`}>
                                                {t(member.runtime_ready
                                                    ? 'agentTeamSetup.statusScopes.runtime.states.ready'
                                                    : 'agentTeamSetup.statusScopes.runtime.states.blocked')}
                                            </span>
                                        </dd>
                                    </div>
                                    <div>
                                        <dt>{t('agentTeamSetup.memberLifecycle')}</dt>
                                        <dd>{t(`agentTeamSetup.lifecycleStates.${member.lifecycle_state}`)}</dd>
                                    </div>
                                    <div>
                                        <dt>{t('agentTeamSetup.connectionEvidence')}</dt>
                                        <dd>{t(`agentTeamSetup.connectionStates.${member.connection_state}`)}</dd>
                                    </div>
                                    <div>
                                        <dt>{t('agentTeamSetup.lastObserved')}</dt>
                                        <dd>{member.last_seen_at
                                            ? formatDateTime(member.last_seen_at, i18n.language)
                                            : t('agentTeamSetup.neverObserved')}</dd>
                                    </div>
                                    <div>
                                        <dt>{t('agentTeamSetup.dispatchAvailability')}</dt>
                                        <dd>{t('agentTeamSetup.availabilityNotEvaluated')}</dd>
                                    </div>
                                </dl>
                                <div className="muted" style={{ marginTop: 6 }}>
                                    {t('agentTeamSetup.queueEvidence', {
                                        queued: member.queued_assignments ?? '—',
                                        accepted: member.accepted_assignments ?? '—',
                                        running: member.running_runs ?? '—',
                                    })}
                                </div>
                                <div className="muted" style={{ marginTop: 6 }}>
                                    {member.skill_package.name}@{member.skill_package.version}
                                </div>
                                {member.handoff && (
                                    <details className="agent-team-runtime-handoff">
                                        <summary>
                                            {t('agentTeamSetup.handoffFor', {
                                                actor: member.actor_key,
                                                name: member.display_name,
                                            })}
                                        </summary>
                                        <dl className="agent-team-handoff-facts">
                                            <div>
                                                <dt>{t('agentTeamSetup.credentialReference')}</dt>
                                                <dd className="mono">{member.handoff.credential_ref}</dd>
                                            </div>
                                            <div>
                                                <dt>{t('agentTeamSetup.serverUrl')}</dt>
                                                <dd className="mono">{member.handoff.server_url}</dd>
                                            </div>
                                        </dl>
                                    </details>
                                )}
                            </section>
                        ))}
                            </div>
                        </details>
                    </aside>
                </div>
            </div>
        </div>
    );
};

export default AgentTeamSetupMasterPage;

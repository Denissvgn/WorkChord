import { useMemo, useRef, useState } from 'react';
import { useMutation, useQueryClient } from '@tanstack/react-query';
import axios from 'axios';
import {
    Check,
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
import {
    AGENT_TEAM_STEP_DEFINITIONS,
    stateTone,
} from '../features/agentTeamSetup/masters';
import { parseAgentTeamMasterEditor } from '../features/agentTeamSetup/manifest';
import { useAgentTeamReadiness } from '../features/agentTeamSetup/useAgentTeamReadiness';
import { useAdminAccess } from '../hooks/useAdminAccess';
import { agentService } from '../services/agentService';
import type {
    AgentTeamApplyResponse,
    AgentTeamMaster,
    AgentTeamPlan,
    AgentTeamPlanAction,
    AgentTeamValidation,
} from '../types/agent';

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

const newCommandId = (prefix: string): string => (
    typeof crypto !== 'undefined' && 'randomUUID' in crypto
        ? `${prefix}-${crypto.randomUUID()}`
        : `${prefix}-${Date.now().toString(36)}`
);

const AgentTeamSetupMasterPage = () => {
    const { t } = useTranslation();
    const queryClient = useQueryClient();
    const { hasAdminKey } = useAdminAccess();
    const readiness = useAgentTeamReadiness();
    const fileInput = useRef<HTMLInputElement>(null);
    const [editor, setEditor] = useState('{\n  "schema_version": "agent-team-master-v1"\n}\n');
    const [validation, setValidation] = useState<AgentTeamValidation | null>(null);
    const [plan, setPlan] = useState<AgentTeamPlan | null>(null);
    const [lastReceipt, setLastReceipt] = useState<AgentTeamApplyResponse | null>(null);
    const [localError, setLocalError] = useState<string | null>(null);
    const [rationale, setRationale] = useState(
        t('agentTeamSetup.defaultRationale'),
    );
    const [confirmations, setConfirmations] = useState<Record<string, boolean>>({});
    const idempotencyKeys = useRef<Record<string, string>>({});

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
    });

    // feedback-policy: mutation pending,inline
    const planMutation = useMutation({
        mutationFn: (manifest: AgentTeamMaster) => (
            agentService.planAgentTeamMaster(
                manifest,
                readiness.status?.topology_revision ?? 0,
            )
        ),
        onSuccess: result => {
            setPlan(result);
            setConfirmations({});
            setLastReceipt(null);
            setLocalError(null);
        },
        onError: error => setLocalError(errorMessage(error)),
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
            setLastReceipt(result);
            setPlan(null);
            setValidation(null);
            setLocalError(null);
            await queryClient.invalidateQueries({ queryKey: ['agent-team-setup'] });
        },
        onError: error => setLocalError(errorMessage(error)),
    });

    const busy = validateMutation.isPending
        || planMutation.isPending
        || applyMutation.isPending;
    const statusError = readiness.isError ? errorMessage(readiness.error) : null;
    const progressLabel = `${readiness.progress.done}/${readiness.progress.total}`;
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
        const manifest = currentManifest();
        if (manifest) validateMutation.mutate(manifest);
    };
    const handlePlan = () => {
        const manifest = currentManifest();
        if (manifest) planMutation.mutate(manifest);
    };
    const handleApply = (action: AgentTeamPlanAction) => {
        const manifest = currentManifest();
        if (!manifest || !plan) return;
        applyMutation.mutate({ manifest, currentPlan: plan, action });
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

    return (
        <div className="wc">
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
                    <div className="row">
                        <span className={`pill ${readiness.status?.runtime_ready ? 'done' : 'warn'}`}>
                            {readiness.status?.topology_state ?? t('common.loading')}
                        </span>
                        <span className="pill">{progressLabel}</span>
                        <button
                            type="button"
                            className="btn sm"
                            onClick={() => readiness.refetch()}
                            disabled={readiness.isFetching}
                        >
                            <RefreshCw size={13} aria-hidden="true" />
                            {t('actions.refresh')}
                        </button>
                    </div>
                </header>

                {(localError || statusError) && (
                    <div className="card card-pad" role="alert" style={{ borderColor: 'var(--blocked-line)' }}>
                        <div className="row" style={{ alignItems: 'flex-start' }}>
                            <CircleAlert size={17} aria-hidden="true" style={{ color: 'var(--blocked)' }} />
                            <div>
                                <strong>{t('agentTeamSetup.errorTitle')}</strong>
                                <div className="muted mono" style={{ marginTop: 4 }}>
                                    {localError ?? statusError}
                                </div>
                            </div>
                        </div>
                    </div>
                )}

                <div className="wc-master" style={{ minHeight: 680 }}>
                    <aside className="wc-master-rail">
                        <div className="wc-master-rail-head between">
                            <strong>{t('agentTeamSetup.stepsLabel')}</strong>
                            <span className="pill sm">{readiness.progress.percent}%</span>
                        </div>
                        <div className="step-rail">
                            {AGENT_TEAM_STEP_DEFINITIONS.map((definition, index) => {
                                const step = readiness.steps[definition.id];
                                const tone = stateTone(step?.state);
                                return (
                                    <div
                                        key={definition.id}
                                        className={`step-item ${tone}`}
                                    >
                                        <div className="step-num">
                                            {tone === 'done' ? <Check size={11} /> : index + 1}
                                        </div>
                                        <div>
                                            <div className="step-title">{t(definition.titleKey)}</div>
                                            <div className="step-sub">
                                                {step?.next_action
                                                    ?? step?.blocker_codes[0]
                                                    ?? t(definition.descriptionKey)}
                                            </div>
                                        </div>
                                        <span className={`pill sm ${tone}`}>{tone}</span>
                                    </div>
                                );
                            })}
                        </div>
                    </aside>

                    <main className="wc-master-main">
                        <AdminAccessGate>
                            <div className="col" style={{ gap: 16 }}>
                            <section className="card card-pad">
                                <div className="between">
                                    <div>
                                        <h2 style={{ margin: 0, fontSize: 16 }}>
                                            {t('agentTeamSetup.masterTitle')}
                                        </h2>
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
                                            disabled={!hasAdminKey || busy}
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
                                        className="input mono"
                                        rows={18}
                                        spellCheck={false}
                                        value={editor}
                                        disabled={!hasAdminKey}
                                        onChange={event => {
                                            setEditor(event.target.value);
                                            setValidation(null);
                                            setPlan(null);
                                            setLastReceipt(null);
                                        }}
                                    />
                                    <div className="field-hint">
                                        <KeyRound size={12} aria-hidden="true" />{' '}
                                        {t('agentTeamSetup.noSecrets')}
                                    </div>
                                </div>
                                <div className="between" style={{ marginTop: 12 }}>
                                    <div className="mono muted">
                                        {validation?.manifest_digest
                                            ? `${t('agentTeamSetup.digest')}: ${validation.manifest_digest}`
                                            : t('agentTeamSetup.notValidated')}
                                    </div>
                                    <div className="row">
                                        <button
                                            type="button"
                                            className="btn"
                                            disabled={!hasAdminKey || busy}
                                            onClick={handleValidate}
                                        >
                                            {t('agentTeamSetup.validate')}
                                        </button>
                                        <button
                                            type="button"
                                            className="btn primary"
                                            disabled={!hasAdminKey || busy || validation?.valid !== true}
                                            onClick={handlePlan}
                                        >
                                            {planMutation.isPending && <LoaderCircle size={13} className="animate-spin" />}
                                            {t('agentTeamSetup.dryRun')}
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
                                            <h2 style={{ margin: 0, fontSize: 16 }}>
                                                {t('agentTeamSetup.planTitle')}
                                            </h2>
                                            <div className="muted mono">
                                                rev {plan.expected_topology_revision} · {plan.plan_digest}
                                            </div>
                                        </div>
                                        <span className="pill">{plan.actions.length}</span>
                                    </div>
                                    <div className="card-pad col">
                                        <div className="field">
                                            <label className="field-lbl" htmlFor="agent-team-rationale">
                                                {t('agentTeamSetup.rationale')}
                                            </label>
                                            <input
                                                id="agent-team-rationale"
                                                className="input"
                                                value={rationale}
                                                onChange={event => setRationale(event.target.value)}
                                            />
                                        </div>
                                        {plan.actions.map(action => (
                                            <div key={action.action_id} className="card card-pad">
                                                <div className="between" style={{ alignItems: 'flex-start' }}>
                                                    <div>
                                                        <div className="row wrap">
                                                            <strong className="mono">{action.action_id}</strong>
                                                            <span className="pill">{action.reconciliation_class}</span>
                                                            {action.authority_change && (
                                                                <span className="pill warn">
                                                                    {t('agentTeamSetup.authorityChange')}
                                                                </span>
                                                            )}
                                                        </div>
                                                        <div className="muted" style={{ marginTop: 5 }}>
                                                            {action.operation} · {action.actor_key}
                                                        </div>
                                                        {action.blocker_code && (
                                                            <div className="mono" style={{ color: 'var(--blocked)', marginTop: 5 }}>
                                                                {action.blocker_code}
                                                            </div>
                                                        )}
                                                    </div>
                                                    <div className="col" style={{ alignItems: 'flex-end' }}>
                                                        {action.requires_explicit_confirmation && (
                                                            <label className="row">
                                                                <input
                                                                    type="checkbox"
                                                                    checked={Boolean(confirmations[action.action_id])}
                                                                    onChange={event => setConfirmations(current => ({
                                                                        ...current,
                                                                        [action.action_id]: event.target.checked,
                                                                    }))}
                                                                />
                                                                {t('agentTeamSetup.confirmAction')}
                                                            </label>
                                                        )}
                                                        <button
                                                            type="button"
                                                            className="btn primary"
                                                            disabled={
                                                                applyMutation.isPending
                                                                || !actionCanApply(action)
                                                                || (
                                                                    action.requires_explicit_confirmation
                                                                    && !confirmations[action.action_id]
                                                                )
                                                            }
                                                            onClick={() => handleApply(action)}
                                                        >
                                                            {t('agentTeamSetup.applyAction')}
                                                        </button>
                                                    </div>
                                                </div>
                                            </div>
                                        ))}
                                    </div>
                                </section>
                            )}

                            {lastReceipt && (
                                <section className="card card-pad" aria-live="polite">
                                    <h2 style={{ margin: 0, fontSize: 16 }}>
                                        {t('agentTeamSetup.receiptTitle')}
                                    </h2>
                                    <div className="mono muted" style={{ marginTop: 6 }}>
                                        {lastReceipt.apply_id} · {lastReceipt.status} · rev {lastReceipt.resulting_topology_revision}
                                    </div>
                                    <div className="row wrap" style={{ marginTop: 10 }}>
                                        {lastReceipt.receipts.map(receipt => (
                                            <span key={receipt.action_id} className={`pill ${receipt.status === 'blocked' ? 'warn' : 'done'}`}>
                                                {receipt.action_id}: {receipt.status}
                                            </span>
                                        ))}
                                    </div>
                                </section>
                            )}
                            </div>
                        </AdminAccessGate>
                    </main>

                    <aside className="wc-master-aux">
                        <section className="card card-pad">
                            <h2 style={{ margin: 0, fontSize: 15 }}>
                                {t('agentTeamSetup.readinessTitle')}
                            </h2>
                            <div className="between" style={{ marginTop: 10 }}>
                                <span className="muted">{t('agentTeamSetup.membersReady')}</span>
                                <strong>{memberCounts.ready}/{memberCounts.total}</strong>
                            </div>
                            <div className="divider" />
                            <div className="mono muted">
                                {readiness.status?.topology_key ?? t('agentTeamSetup.noTopology')}
                            </div>
                            <div className="mono muted">
                                {readiness.status?.topology_revision
                                    ? `revision ${readiness.status.topology_revision}`
                                    : 'revision —'}
                            </div>
                            <p className="muted">{readiness.status?.next_action}</p>
                        </section>
                        {readiness.status?.members.map(member => (
                            <section key={member.actor_key} className="card card-pad">
                                <div className="between">
                                    <strong>{member.display_name}</strong>
                                    <span className={`pill ${member.runtime_ready ? 'done' : 'warn'}`}>
                                        {member.lifecycle_state}
                                    </span>
                                </div>
                                <div className="muted mono" style={{ marginTop: 5 }}>
                                    {member.actor_key} · {member.role}
                                </div>
                                <div className="muted" style={{ marginTop: 6 }}>
                                    {member.connection_state} · {member.availability}
                                </div>
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
                                    <details style={{ marginTop: 10 }}>
                                        <summary>{t('agentTeamSetup.handoff')}</summary>
                                        <div className="mono muted" style={{ marginTop: 8, overflowWrap: 'anywhere' }}>
                                            {member.handoff.credential_ref}
                                            <br />
                                            {member.handoff.server_url}
                                        </div>
                                    </details>
                                )}
                            </section>
                        ))}
                    </aside>
                </div>
            </div>
        </div>
    );
};

export default AgentTeamSetupMasterPage;

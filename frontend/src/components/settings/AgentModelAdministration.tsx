import { useMemo, useState } from 'react';
import type { FormEvent } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import {
    AlertTriangle,
    Bot,
    Database,
    Link2,
    Pencil,
    Plus,
    RefreshCw,
    ShieldCheck,
    X,
} from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { useAgentAccess } from '../../hooks/useAgentAccess';
import { agentService } from '../../services/agentService';
import type {
    AgentModelBinding,
    AgentModelBindingCreate,
    AgentModelCatalogCreate,
    AgentModelCatalogEntry,
} from '../../types/agent';
import { normalizeApiError } from '../../utils/apiError';
import {
    createAgentCommandMetadata,
    formatRoutingCode,
    parseRoutingTags,
} from '../../utils/modelRouting';
import { protectedQueryRetry } from '../../utils/protectedQueries';
import { formatDateTime } from '../../utils/formatDate';
import { Button } from '../common/Button';
import { Checkbox } from '../common/Checkbox';
import { Input } from '../common/Input';
import { QueryEmptyState, QueryErrorState, QueryLoadingState } from '../feedback/QueryState';
import { useToast } from '../feedback/toast';
import { useConfirmDialog } from '../common/useConfirmDialog';

interface CatalogForm {
    id: number | null;
    revision: number | null;
    key: string;
    provider: string;
    configuredModelAlias: string;
    reasoningTier: 1 | 2 | 3;
    contextTier: 'small' | 'medium' | 'large';
    modalityTags: string;
    costTier: 'low' | 'medium' | 'high';
    latencyTier: 'fast' | 'balanced' | 'slow';
    lastVerifiedAt: string;
}

interface BindingForm {
    id: number | null;
    revision: number | null;
    actorId: number | null;
    modelCatalogId: number | null;
    isDefault: boolean;
    toolTags: string;
    dataPolicyTags: string;
}

const EMPTY_CATALOG_FORM: CatalogForm = {
    id: null,
    revision: null,
    key: '',
    provider: '',
    configuredModelAlias: '',
    reasoningTier: 2,
    contextTier: 'medium',
    modalityTags: 'text',
    costTier: 'medium',
    latencyTier: 'balanced',
    lastVerifiedAt: '',
};

const EMPTY_BINDING_FORM: BindingForm = {
    id: null,
    revision: null,
    actorId: null,
    modelCatalogId: null,
    isDefault: false,
    toolTags: '',
    dataPolicyTags: '',
};

const toLocalDateTime = (value?: string | null) => {
    if (!value) return '';
    const date = new Date(value);
    if (Number.isNaN(date.getTime())) return '';
    const offset = date.getTimezoneOffset() * 60_000;
    return new Date(date.getTime() - offset).toISOString().slice(0, 16);
};

const toIsoDateTime = (value: string) => (
    value ? new Date(value).toISOString() : null
);

export const AgentModelAdministration = () => {
    const { t } = useTranslation();
    const { hasAgentKey } = useAgentAccess();
    const queryClient = useQueryClient();
    const toast = useToast();
    const { requestConfirmation, confirmationDialog } = useConfirmDialog();
    const [catalogForm, setCatalogForm] = useState<CatalogForm>(EMPTY_CATALOG_FORM);
    const [bindingForm, setBindingForm] = useState<BindingForm>(EMPTY_BINDING_FORM);
    const [auditRationale, setAuditRationale] = useState('');
    const [reconcileLiveAssignments, setReconcileLiveAssignments] = useState(false);
    const [conflictMessage, setConflictMessage] = useState<string | null>(null);

    // feedback-policy: query loading,error,retry,empty
    const capabilitiesQuery = useQuery({
        queryKey: ['agent-capabilities'],
        queryFn: agentService.getCapabilities,
        enabled: hasAgentKey,
        retry: protectedQueryRetry,
    });
    const capabilitiesCurrent = capabilitiesQuery.isSuccess
        && !capabilitiesQuery.isError;
    const scopes = capabilitiesCurrent
        ? capabilitiesQuery.data?.scopes ?? []
        : [];
    const canRead = scopes.includes('admin') || scopes.includes('planning:read');
    const canAdminister = scopes.includes('admin');
    const routingStatus = capabilitiesQuery.data?.model_aware_routing;
    const routingBlockerCodes = Array.from(new Set([
        ...(routingStatus?.blocker_codes ?? []),
        ...(routingStatus?.topology_readiness.blocker_codes ?? []),
    ]));

    // feedback-policy: query loading,error,retry,empty
    const rosterQuery = useQuery({
        queryKey: ['agent-actor-roster', true],
        queryFn: () => agentService.getActorRoster(true),
        enabled: hasAgentKey && canRead,
        retry: protectedQueryRetry,
    });

    // feedback-policy: query loading,error,retry,empty
    const catalogQuery = useQuery({
        queryKey: ['agent-model-catalog', true],
        queryFn: () => agentService.getModelCatalog(true),
        enabled: hasAgentKey && canRead,
        retry: protectedQueryRetry,
    });

    // feedback-policy: query loading,error,retry,empty
    const bindingsQuery = useQuery({
        queryKey: ['agent-model-bindings', true],
        queryFn: () => agentService.getModelBindings({ includeDisabled: true }),
        enabled: hasAgentKey && canRead,
        retry: protectedQueryRetry,
    });

    const refreshEvidence = (clearConflict = true) => {
        if (clearConflict) setConflictMessage(null);
        void queryClient.invalidateQueries({ queryKey: ['agent-capabilities'] });
        void queryClient.invalidateQueries({ queryKey: ['agent-actor-roster'] });
        void queryClient.invalidateQueries({ queryKey: ['agent-model-catalog'] });
        void queryClient.invalidateQueries({ queryKey: ['agent-model-bindings'] });
        void queryClient.invalidateQueries({ queryKey: ['routing-preview'] });
    };

    const mutationError = (
        error: unknown,
        fallback: string,
        recoverConflict?: () => void,
    ) => {
        const normalized = normalizeApiError(error, fallback);
        if (normalized.status === 409) {
            recoverConflict?.();
            setConflictMessage(normalized.message);
            refreshEvidence(false);
            return;
        }
        toast.error(normalized.message);
    };

    const mutationSuccess = (message: string) => {
        refreshEvidence();
        setCatalogForm(EMPTY_CATALOG_FORM);
        setBindingForm(EMPTY_BINDING_FORM);
        setReconcileLiveAssignments(false);
        toast.success(message);
    };

    // feedback-policy: mutation pending,toast
    const createCatalogMutation = useMutation({
        mutationFn: (data: AgentModelCatalogCreate) => (
            agentService.createModelCatalogEntry(
                data,
                createAgentCommandMetadata(auditRationale),
            )
        ),
        onSuccess: () => mutationSuccess(t('modelAdministration.catalogCreateSuccess')),
        onError: error => mutationError(error, t('modelAdministration.catalogMutationFailed')),
    });

    // feedback-policy: mutation pending,toast
    const updateCatalogMutation = useMutation({
        mutationFn: ({ id, data }: {
            id: number;
            data: Parameters<typeof agentService.updateModelCatalogEntry>[1];
        }) => agentService.updateModelCatalogEntry(
            id,
            data,
            createAgentCommandMetadata(auditRationale),
        ),
        onSuccess: () => mutationSuccess(t('modelAdministration.catalogUpdateSuccess')),
        onError: error => mutationError(
            error,
            t('modelAdministration.catalogMutationFailed'),
            () => setCatalogForm(EMPTY_CATALOG_FORM),
        ),
    });

    // feedback-policy: mutation pending,toast
    const disableCatalogMutation = useMutation({
        mutationFn: (entry: AgentModelCatalogEntry) => (
            agentService.disableModelCatalogEntry(
                entry.id,
                {
                    expected_revision: entry.revision,
                    reconcile_live_assignments: reconcileLiveAssignments,
                },
                createAgentCommandMetadata(auditRationale),
            )
        ),
        onSuccess: () => mutationSuccess(t('modelAdministration.catalogDisableSuccess')),
        onError: error => mutationError(error, t('modelAdministration.catalogMutationFailed')),
    });

    // feedback-policy: mutation pending,toast
    const enableCatalogMutation = useMutation({
        mutationFn: (entry: AgentModelCatalogEntry) => (
            agentService.updateModelCatalogEntry(
                entry.id,
                {
                    expected_revision: entry.revision,
                    enabled: true,
                    reconcile_live_assignments: reconcileLiveAssignments,
                },
                createAgentCommandMetadata(auditRationale),
            )
        ),
        onSuccess: () => mutationSuccess(t('modelAdministration.catalogEnableSuccess')),
        onError: error => mutationError(error, t('modelAdministration.catalogMutationFailed')),
    });

    // feedback-policy: mutation pending,toast
    const createBindingMutation = useMutation({
        mutationFn: (data: AgentModelBindingCreate) => (
            agentService.createModelBinding(
                data,
                createAgentCommandMetadata(auditRationale),
            )
        ),
        onSuccess: () => mutationSuccess(t('modelAdministration.bindingCreateSuccess')),
        onError: error => mutationError(error, t('modelAdministration.bindingMutationFailed')),
    });

    // feedback-policy: mutation pending,toast
    const updateBindingMutation = useMutation({
        mutationFn: ({ id, data }: {
            id: number;
            data: Parameters<typeof agentService.updateModelBinding>[1];
        }) => agentService.updateModelBinding(
            id,
            data,
            createAgentCommandMetadata(auditRationale),
        ),
        onSuccess: () => mutationSuccess(t('modelAdministration.bindingUpdateSuccess')),
        onError: error => mutationError(
            error,
            t('modelAdministration.bindingMutationFailed'),
            () => setBindingForm(EMPTY_BINDING_FORM),
        ),
    });

    // feedback-policy: mutation pending,toast
    const disableBindingMutation = useMutation({
        mutationFn: (binding: AgentModelBinding) => (
            agentService.disableModelBinding(
                binding.id,
                {
                    expected_revision: binding.revision,
                    reconcile_live_assignments: reconcileLiveAssignments,
                },
                createAgentCommandMetadata(auditRationale),
            )
        ),
        onSuccess: () => mutationSuccess(t('modelAdministration.bindingDisableSuccess')),
        onError: error => mutationError(error, t('modelAdministration.bindingMutationFailed')),
    });

    // feedback-policy: mutation pending,toast
    const enableBindingMutation = useMutation({
        mutationFn: (binding: AgentModelBinding) => (
            agentService.updateModelBinding(
                binding.id,
                {
                    expected_revision: binding.revision,
                    enabled: true,
                    reconcile_live_assignments: reconcileLiveAssignments,
                },
                createAgentCommandMetadata(auditRationale),
            )
        ),
        onSuccess: () => mutationSuccess(t('modelAdministration.bindingEnableSuccess')),
        onError: error => mutationError(error, t('modelAdministration.bindingMutationFailed')),
    });

    const actors = useMemo(() => rosterQuery.data ?? [], [rosterQuery.data]);
    const catalog = useMemo(() => catalogQuery.data ?? [], [catalogQuery.data]);
    const bindings = useMemo(() => bindingsQuery.data ?? [], [bindingsQuery.data]);
    const actorById = useMemo(
        () => new Map(actors.map(actor => [actor.id, actor])),
        [actors],
    );
    const catalogById = useMemo(
        () => new Map(catalog.map(entry => [entry.id, entry])),
        [catalog],
    );
    const isMutating = [
        createCatalogMutation,
        updateCatalogMutation,
        disableCatalogMutation,
        enableCatalogMutation,
        createBindingMutation,
        updateBindingMutation,
        disableBindingMutation,
        enableBindingMutation,
    ].some(mutation => mutation.isPending);
    const rationaleReady = auditRationale.trim().length > 0;

    const submitCatalog = (event: FormEvent) => {
        event.preventDefault();
        if (!canAdminister || !rationaleReady) return;
        const createData: AgentModelCatalogCreate = {
            key: catalogForm.key.trim().toLowerCase(),
            provider: catalogForm.provider.trim(),
            configured_model_alias: catalogForm.configuredModelAlias.trim(),
            reasoning_tier: catalogForm.reasoningTier,
            context_tier: catalogForm.contextTier,
            modality_tags: parseRoutingTags(catalogForm.modalityTags),
            cost_tier: catalogForm.costTier,
            latency_tier: catalogForm.latencyTier,
            enabled: true,
            revision: 1,
            last_verified_at: toIsoDateTime(catalogForm.lastVerifiedAt),
        };
        if (catalogForm.id && catalogForm.revision) {
            updateCatalogMutation.mutate({
                id: catalogForm.id,
                data: {
                    expected_revision: catalogForm.revision,
                    provider: createData.provider,
                    configured_model_alias: createData.configured_model_alias,
                    reasoning_tier: createData.reasoning_tier,
                    context_tier: createData.context_tier,
                    modality_tags: createData.modality_tags,
                    cost_tier: createData.cost_tier,
                    latency_tier: createData.latency_tier,
                    last_verified_at: createData.last_verified_at,
                    reconcile_live_assignments: reconcileLiveAssignments,
                },
            });
            return;
        }
        createCatalogMutation.mutate(createData);
    };

    const submitBinding = (event: FormEvent) => {
        event.preventDefault();
        if (
            !canAdminister
            || !rationaleReady
            || !bindingForm.actorId
            || !bindingForm.modelCatalogId
        ) return;
        const createData: AgentModelBindingCreate = {
            actor_id: bindingForm.actorId,
            model_catalog_id: bindingForm.modelCatalogId,
            is_default: bindingForm.isDefault,
            enabled: true,
            tool_tags: parseRoutingTags(bindingForm.toolTags),
            data_policy_tags: parseRoutingTags(bindingForm.dataPolicyTags),
            revision: 1,
        };
        if (bindingForm.id && bindingForm.revision) {
            updateBindingMutation.mutate({
                id: bindingForm.id,
                data: {
                    expected_revision: bindingForm.revision,
                    is_default: bindingForm.isDefault,
                    tool_tags: createData.tool_tags,
                    data_policy_tags: createData.data_policy_tags,
                    reconcile_live_assignments: reconcileLiveAssignments,
                },
            });
            return;
        }
        createBindingMutation.mutate(createData);
    };

    const editCatalog = (entry: AgentModelCatalogEntry) => {
        setCatalogForm({
            id: entry.id,
            revision: entry.revision,
            key: entry.key,
            provider: entry.provider,
            configuredModelAlias: entry.configured_model_alias,
            reasoningTier: entry.reasoning_tier,
            contextTier: entry.context_tier,
            modalityTags: entry.modality_tags.join(', '),
            costTier: entry.cost_tier,
            latencyTier: entry.latency_tier,
            lastVerifiedAt: toLocalDateTime(entry.last_verified_at),
        });
    };

    const editBinding = (binding: AgentModelBinding) => {
        setBindingForm({
            id: binding.id,
            revision: binding.revision,
            actorId: binding.actor_id,
            modelCatalogId: binding.model_catalog_id,
            isDefault: binding.is_default,
            toolTags: binding.tool_tags.join(', '),
            dataPolicyTags: binding.data_policy_tags.join(', '),
        });
    };

    if (!hasAgentKey) {
        return (
            <QueryEmptyState
                title={t('modelAdministration.accessRequiredTitle')}
                description={t('modelAdministration.accessRequiredDescription')}
            />
        );
    }

    if (capabilitiesQuery.isPending) {
        return <QueryLoadingState message={t('modelAdministration.checkingAccess')} />;
    }

    if (capabilitiesQuery.isError) {
        return (
            <QueryErrorState
                error={capabilitiesQuery.error}
                fallback={t('modelAdministration.accessFailed')}
                onRetry={() => { void capabilitiesQuery.refetch(); }}
            />
        );
    }

    if (!canRead) {
        return (
            <QueryErrorState
                message={t('modelAdministration.readScopeRequired')}
                title={t('modelAdministration.accessDenied')}
            />
        );
    }

    const evidenceLoading = rosterQuery.isPending || catalogQuery.isPending || bindingsQuery.isPending;
    if (evidenceLoading) {
        return <QueryLoadingState message={t('modelAdministration.loading')} />;
    }

    const evidenceError = rosterQuery.error || catalogQuery.error || bindingsQuery.error;
    if (evidenceError) {
        return (
            <QueryErrorState
                error={evidenceError}
                fallback={t('modelAdministration.loadFailed')}
                onRetry={refreshEvidence}
            />
        );
    }

    return (
        <div className="space-y-5">
            <section className="card space-y-3" aria-labelledby="model-admin-overview-heading">
                <div className="flex flex-wrap items-start justify-between gap-3">
                    <div>
                        <h2 id="model-admin-overview-heading" className="flex items-center gap-2 text-lg font-semibold text-content-primary">
                            <ShieldCheck aria-hidden="true" className="h-5 w-5 text-action" />
                            {t('modelAdministration.title')}
                        </h2>
                        <p className="mt-1 text-sm text-content-secondary">{t('modelAdministration.description')}</p>
                    </div>
                    <div className={`rounded-full border px-3 py-1 text-xs font-medium ${
                        canAdminister
                            ? 'border-feedback-success-border bg-feedback-success-muted text-feedback-success-foreground'
                            : 'border-feedback-info-border bg-feedback-info-muted text-feedback-info-foreground'
                    }`}>
                        {canAdminister
                            ? t('modelAdministration.adminMode')
                            : t('modelAdministration.readOnlyMode')}
                    </div>
                </div>
                <div className="grid grid-cols-1 gap-3 sm:grid-cols-3">
                    <div className="kpi"><div className="kpi-lbl">{t('modelAdministration.actors')}</div><div className="kpi-val tnum">{actors.length}</div></div>
                    <div className="kpi"><div className="kpi-lbl">{t('modelAdministration.catalogEntries')}</div><div className="kpi-val tnum">{catalog.length}</div></div>
                    <div className="kpi"><div className="kpi-lbl">{t('modelAdministration.bindings')}</div><div className="kpi-val tnum">{bindings.length}</div></div>
                </div>
                <div className="grid grid-cols-1 gap-3 sm:grid-cols-3">
                    <div className="kpi">
                        <div className="kpi-lbl">{t('modelAdministration.configuredRoutingMode')}</div>
                        <div className="kpi-val text-base">
                            {t(`taskRouting.rolloutModes.${routingStatus?.configured_mode ?? 'off'}`)}
                        </div>
                    </div>
                    <div className="kpi">
                        <div className="kpi-lbl">{t('modelAdministration.effectiveRoutingMode')}</div>
                        <div className="kpi-val text-base">
                            {t(`taskRouting.rolloutModes.${routingStatus?.effective_mode ?? 'off'}`)}
                        </div>
                    </div>
                    <div className="kpi">
                        <div className="kpi-lbl">{t('modelAdministration.topologyReadiness')}</div>
                        <div className="kpi-val text-base">
                            {t(`taskRouting.topologyStatuses.${routingStatus?.topology_readiness.status ?? 'unavailable'}`)}
                        </div>
                    </div>
                </div>
                {routingBlockerCodes.length > 0 && (
                    <div className="rounded-md border border-feedback-warning-border bg-feedback-warning-muted p-3">
                        <p className="text-xs font-semibold uppercase tracking-wide text-feedback-warning-foreground">
                            {t('modelAdministration.routingBlockers')}
                        </p>
                        <ul className="mt-1 list-disc space-y-1 pl-5 text-xs text-feedback-warning-foreground">
                            {routingBlockerCodes.map(code => (
                                <li key={code}>{formatRoutingCode(code)}</li>
                            ))}
                        </ul>
                    </div>
                )}
                <Button type="button" size="sm" variant="secondary" onClick={() => refreshEvidence()}>
                    <RefreshCw aria-hidden="true" className="mr-2 h-4 w-4" />
                    {t('actions.refresh')}
                </Button>
            </section>

            {conflictMessage && (
                <div className="rounded-md border border-feedback-warning-border bg-feedback-warning-muted p-3 text-sm text-feedback-warning-foreground" role="alert">
                    <div className="flex items-start gap-2">
                        <AlertTriangle aria-hidden="true" className="mt-0.5 h-4 w-4 shrink-0" />
                        <div className="flex-1">
                            <p className="font-semibold">{t('modelAdministration.conflictTitle')}</p>
                            <p>{conflictMessage}</p>
                        </div>
                        <Button type="button" size="sm" variant="ghost" onClick={() => setConflictMessage(null)} aria-label={t('actions.close')}>
                            <X aria-hidden="true" className="h-4 w-4" />
                        </Button>
                    </div>
                </div>
            )}

            {canAdminister && (
                <section className="card space-y-3" aria-labelledby="model-admin-audit-heading">
                    <h3 id="model-admin-audit-heading" className="font-semibold text-content-primary">{t('modelAdministration.auditControls')}</h3>
                    <Input
                        label={t('modelAdministration.auditRationale')}
                        value={auditRationale}
                        onChange={event => setAuditRationale(event.target.value)}
                        placeholder={t('modelAdministration.auditRationalePlaceholder')}
                        required
                    />
                    <Checkbox
                        checked={reconcileLiveAssignments}
                        onChange={setReconcileLiveAssignments}
                        label={t('modelAdministration.reconcileLiveAssignments')}
                    />
                    <p className="text-xs text-content-secondary">{t('modelAdministration.reconcileWarning')}</p>
                </section>
            )}

            <section className="card space-y-4" aria-labelledby="actor-roster-heading">
                <div>
                    <h3 id="actor-roster-heading" className="flex items-center gap-2 font-semibold text-content-primary">
                        <Bot aria-hidden="true" className="h-4 w-4 text-action" />
                        {t('modelAdministration.actorRoster')}
                    </h3>
                    <p className="text-sm text-content-secondary">{t('modelAdministration.actorRosterDescription')}</p>
                </div>
                {actors.length === 0 ? (
                    <QueryEmptyState title={t('modelAdministration.noActors')} />
                ) : (
                    <div className="grid grid-cols-1 gap-3 xl:grid-cols-2">
                        {actors.map(actor => {
                            const hasSelectableBindingEvidence = actor.enabled
                                && Boolean(actor.profile)
                                && actor.eligible_model_bindings.length > 0;
                            return (
                                <article key={actor.id} className="rounded-lg border border-border bg-surface-muted p-4">
                                    <div className="flex items-start justify-between gap-3">
                                        <div>
                                            <h4 className="font-medium text-content-primary">{actor.display_name}</h4>
                                            <p className="text-xs text-content-secondary">{actor.name} · {actor.role}</p>
                                        </div>
                                        <span className={`rounded-full border px-2 py-0.5 text-xs ${
                                            hasSelectableBindingEvidence
                                                ? 'border-feedback-success-border bg-feedback-success-muted text-feedback-success-foreground'
                                                : 'border-feedback-warning-border bg-feedback-warning-muted text-feedback-warning-foreground'
                                        }`}>
                                            {hasSelectableBindingEvidence
                                                ? t('modelAdministration.selectableBindingEvidence')
                                                : t('modelAdministration.noSelectableBindingEvidence')}
                                        </span>
                                    </div>
                                    <dl className="mt-3 grid grid-cols-2 gap-2 text-xs">
                                        <div><dt className="text-content-tertiary">{t('modelAdministration.profile')}</dt><dd className="text-content-primary">{actor.profile?.display_name ?? t('common.none')}</dd></div>
                                        <div><dt className="text-content-tertiary">{t('modelAdministration.profileKind')}</dt><dd className="text-content-primary">{actor.profile?.profile_kind ?? t('common.none')}</dd></div>
                                        <div><dt className="text-content-tertiary">{t('modelAdministration.assignmentModes')}</dt><dd className="text-content-primary">{actor.profile?.assignment_modes.join(', ') || t('common.none')}</dd></div>
                                        <div><dt className="text-content-tertiary">{t('modelAdministration.queueRevision')}</dt><dd className="text-content-primary tnum">{actor.queue_revision}</dd></div>
                                        <div><dt className="text-content-tertiary">{t('modelAdministration.queue')}</dt><dd className="text-content-primary tnum">{actor.queued_assignments} / {actor.accepted_assignments}</dd></div>
                                        <div><dt className="text-content-tertiary">{t('modelAdministration.runningRuns')}</dt><dd className="text-content-primary tnum">{actor.running_runs}</dd></div>
                                    </dl>
                                    <div className="mt-3 flex flex-wrap gap-1">
                                        {actor.eligible_model_bindings.map(binding => (
                                            <span key={binding.id} className="rounded-full border border-feedback-success-border bg-feedback-success-muted px-2 py-0.5 text-xs text-feedback-success-foreground">
                                                {binding.model_catalog?.configured_model_alias ?? binding.model_catalog_key}
                                                {' · '}r{binding.revision}
                                            </span>
                                        ))}
                                        {actor.eligible_model_bindings.length === 0 && (
                                            <span className="text-xs text-feedback-warning-foreground">{t('modelAdministration.noSelectableBindings')}</span>
                                        )}
                                    </div>
                                </article>
                            );
                        })}
                    </div>
                )}
            </section>

            <section className="grid grid-cols-1 gap-5 2xl:grid-cols-[minmax(0,1fr)_420px]" aria-labelledby="catalog-heading">
                <div className="card space-y-4">
                    <div>
                        <h3 id="catalog-heading" className="flex items-center gap-2 font-semibold text-content-primary">
                            <Database aria-hidden="true" className="h-4 w-4 text-action" />
                            {t('modelAdministration.modelCatalog')}
                        </h3>
                        <p className="text-sm text-content-secondary">{t('modelAdministration.modelCatalogDescription')}</p>
                    </div>
                    {catalog.length === 0 ? (
                        <QueryEmptyState title={t('modelAdministration.noCatalogEntries')} />
                    ) : (
                        <div className="space-y-3">
                            {catalog.map(entry => (
                                <article key={entry.id} className="rounded-lg border border-border bg-surface-muted p-4">
                                    <div className="flex items-start justify-between gap-3">
                                        <div>
                                            <h4 className="font-medium text-content-primary">{entry.configured_model_alias}</h4>
                                            <p className="text-xs text-content-secondary">{entry.key} · {entry.provider}</p>
                                        </div>
                                        <span className={`rounded-full border px-2 py-0.5 text-xs ${
                                            entry.enabled
                                                ? 'border-feedback-success-border bg-feedback-success-muted text-feedback-success-foreground'
                                                : 'border-border bg-surface-subtle text-content-secondary'
                                        }`}>
                                            {entry.enabled ? t('common.enabled') : t('common.disabled')}
                                        </span>
                                    </div>
                                    <dl className="mt-3 grid grid-cols-2 gap-2 text-xs sm:grid-cols-4">
                                        <div><dt className="text-content-tertiary">{t('modelAdministration.reasoningTier')}</dt><dd className="text-content-primary tnum">{entry.reasoning_tier}</dd></div>
                                        <div><dt className="text-content-tertiary">{t('modelAdministration.contextTier')}</dt><dd className="text-content-primary">{entry.context_tier}</dd></div>
                                        <div><dt className="text-content-tertiary">{t('modelAdministration.costTier')}</dt><dd className="text-content-primary">{entry.cost_tier}</dd></div>
                                        <div><dt className="text-content-tertiary">{t('modelAdministration.latencyTier')}</dt><dd className="text-content-primary">{entry.latency_tier}</dd></div>
                                        <div><dt className="text-content-tertiary">{t('modelAdministration.revision')}</dt><dd className="text-content-primary tnum">{entry.revision}</dd></div>
                                        <div className="sm:col-span-3"><dt className="text-content-tertiary">{t('modelAdministration.lastVerified')}</dt><dd className="text-content-primary">{entry.last_verified_at ? formatDateTime(entry.last_verified_at) : t('modelAdministration.neverVerified')}</dd></div>
                                    </dl>
                                    <div className="mt-3 flex flex-wrap gap-2">
                                        <span className="text-xs text-content-secondary">{t('modelAdministration.modalities')}: {entry.modality_tags.join(', ')}</span>
                                    </div>
                                    {canAdminister && (
                                        <div className="mt-3 flex gap-2">
                                            <Button
                                                type="button"
                                                size="sm"
                                                variant="secondary"
                                                onClick={() => editCatalog(entry)}
                                                disabled={isMutating}
                                                aria-label={t('modelAdministration.editCatalogAction', { alias: entry.configured_model_alias })}
                                            >
                                                <Pencil aria-hidden="true" className="mr-2 h-3.5 w-3.5" />
                                                {t('actions.edit')}
                                            </Button>
                                            {entry.enabled && (
                                                <Button
                                                    type="button"
                                                    size="sm"
                                                    variant="outline"
                                                    disabled={!rationaleReady || isMutating}
                                                    aria-label={t('modelAdministration.disableCatalogAction', { alias: entry.configured_model_alias })}
                                                    onClick={() => requestConfirmation({
                                                        title: t('modelAdministration.disableCatalogTitle'),
                                                        description: t('modelAdministration.disableCatalogDescription', { alias: entry.configured_model_alias }),
                                                        confirmLabel: t('common.disable'),
                                                        cancelLabel: t('actions.cancel'),
                                                        closeLabel: t('actions.close'),
                                                        onConfirm: () => disableCatalogMutation.mutateAsync(entry),
                                                    })}
                                                >
                                                    {t('common.disable')}
                                                </Button>
                                            )}
                                            {!entry.enabled && (
                                                <Button
                                                    type="button"
                                                    size="sm"
                                                    variant="outline"
                                                    disabled={!rationaleReady || isMutating}
                                                    aria-label={t('modelAdministration.enableCatalogAction', { alias: entry.configured_model_alias })}
                                                    onClick={() => enableCatalogMutation.mutate(entry)}
                                                >
                                                    {t('common.enable')}
                                                </Button>
                                            )}
                                        </div>
                                    )}
                                </article>
                            ))}
                        </div>
                    )}
                </div>

                {canAdminister && (
                    <form className="card space-y-3" onSubmit={submitCatalog}>
                        <h3 className="font-semibold text-content-primary">
                            {catalogForm.id
                                ? t('modelAdministration.editCatalogEntry')
                                : t('modelAdministration.createCatalogEntry')}
                        </h3>
                        <Input label={t('modelAdministration.catalogKey')} value={catalogForm.key} onChange={event => setCatalogForm({ ...catalogForm, key: event.target.value })} disabled={Boolean(catalogForm.id)} required />
                        <Input label={t('modelAdministration.provider')} value={catalogForm.provider} onChange={event => setCatalogForm({ ...catalogForm, provider: event.target.value })} required />
                        <Input label={t('modelAdministration.configuredAlias')} value={catalogForm.configuredModelAlias} onChange={event => setCatalogForm({ ...catalogForm, configuredModelAlias: event.target.value })} required />
                        <div className="grid grid-cols-2 gap-3">
                            <label className="field">
                                <span className="field-lbl">{t('modelAdministration.reasoningTier')}</span>
                                <select className="input" value={catalogForm.reasoningTier} onChange={event => setCatalogForm({ ...catalogForm, reasoningTier: Number(event.target.value) as 1 | 2 | 3 })}>
                                    <option value={1}>1</option><option value={2}>2</option><option value={3}>3</option>
                                </select>
                            </label>
                            <label className="field">
                                <span className="field-lbl">{t('modelAdministration.contextTier')}</span>
                                <select className="input" value={catalogForm.contextTier} onChange={event => setCatalogForm({ ...catalogForm, contextTier: event.target.value as CatalogForm['contextTier'] })}>
                                    <option value="small">{t('modelAdministration.small')}</option>
                                    <option value="medium">{t('modelAdministration.medium')}</option>
                                    <option value="large">{t('modelAdministration.large')}</option>
                                </select>
                            </label>
                            <label className="field">
                                <span className="field-lbl">{t('modelAdministration.costTier')}</span>
                                <select className="input" value={catalogForm.costTier} onChange={event => setCatalogForm({ ...catalogForm, costTier: event.target.value as CatalogForm['costTier'] })}>
                                    <option value="low">{t('modelAdministration.low')}</option>
                                    <option value="medium">{t('modelAdministration.medium')}</option>
                                    <option value="high">{t('modelAdministration.high')}</option>
                                </select>
                            </label>
                            <label className="field">
                                <span className="field-lbl">{t('modelAdministration.latencyTier')}</span>
                                <select className="input" value={catalogForm.latencyTier} onChange={event => setCatalogForm({ ...catalogForm, latencyTier: event.target.value as CatalogForm['latencyTier'] })}>
                                    <option value="fast">{t('modelAdministration.fast')}</option>
                                    <option value="balanced">{t('modelAdministration.balanced')}</option>
                                    <option value="slow">{t('modelAdministration.slow')}</option>
                                </select>
                            </label>
                        </div>
                        <Input label={t('modelAdministration.modalities')} value={catalogForm.modalityTags} onChange={event => setCatalogForm({ ...catalogForm, modalityTags: event.target.value })} required />
                        <Input label={t('modelAdministration.lastVerified')} type="datetime-local" value={catalogForm.lastVerifiedAt} onChange={event => setCatalogForm({ ...catalogForm, lastVerifiedAt: event.target.value })} />
                        <div className="flex gap-2">
                            {catalogForm.id && (
                                <Button type="button" variant="ghost" onClick={() => setCatalogForm(EMPTY_CATALOG_FORM)}>
                                    {t('actions.cancel')}
                                </Button>
                            )}
                            <Button type="submit" isLoading={createCatalogMutation.isPending || updateCatalogMutation.isPending} disabled={!rationaleReady || isMutating}>
                                <Plus aria-hidden="true" className="mr-2 h-4 w-4" />
                                {catalogForm.id ? t('actions.save') : t('actions.create')}
                            </Button>
                        </div>
                    </form>
                )}
            </section>

            <section className="grid grid-cols-1 gap-5 2xl:grid-cols-[minmax(0,1fr)_420px]" aria-labelledby="bindings-heading">
                <div className="card space-y-4">
                    <div>
                        <h3 id="bindings-heading" className="flex items-center gap-2 font-semibold text-content-primary">
                            <Link2 aria-hidden="true" className="h-4 w-4 text-action" />
                            {t('modelAdministration.modelBindings')}
                        </h3>
                        <p className="text-sm text-content-secondary">{t('modelAdministration.modelBindingsDescription')}</p>
                    </div>
                    {bindings.length === 0 ? (
                        <QueryEmptyState title={t('modelAdministration.noBindings')} />
                    ) : (
                        <div className="space-y-3">
                            {bindings.map(binding => {
                                const actor = actorById.get(binding.actor_id);
                                const entry = binding.model_catalog ?? catalogById.get(binding.model_catalog_id);
                                const isSelectable = Boolean(actor?.enabled)
                                    && binding.enabled
                                    && Boolean(entry?.enabled)
                                    && binding.selectable;
                                return (
                                    <article key={binding.id} className="rounded-lg border border-border bg-surface-muted p-4">
                                        <div className="flex items-start justify-between gap-3">
                                            <div>
                                                <h4 className="font-medium text-content-primary">
                                                    {actor?.display_name ?? t('modelAdministration.actorNumber', { id: binding.actor_id })}
                                                </h4>
                                                <p className="text-xs text-content-secondary">
                                                    {entry?.configured_model_alias ?? binding.model_catalog_key ?? t('common.unknown')}
                                                    {' · '}r{binding.revision}
                                                </p>
                                            </div>
                                            <span className={`rounded-full border px-2 py-0.5 text-xs ${
                                                isSelectable
                                                    ? 'border-feedback-success-border bg-feedback-success-muted text-feedback-success-foreground'
                                                    : 'border-feedback-warning-border bg-feedback-warning-muted text-feedback-warning-foreground'
                                            }`}>
                                                {isSelectable
                                                    ? t('modelAdministration.selectable')
                                                    : binding.enabled
                                                        ? t('modelAdministration.staleOrUnselectable')
                                                        : t('common.disabled')}
                                            </span>
                                        </div>
                                        <dl className="mt-3 grid grid-cols-2 gap-2 text-xs sm:grid-cols-4">
                                            <div><dt className="text-content-tertiary">{t('modelAdministration.profile')}</dt><dd className="text-content-primary">{actor?.profile?.display_name ?? t('common.none')}</dd></div>
                                            <div><dt className="text-content-tertiary">{t('modelAdministration.default')}</dt><dd className="text-content-primary">{binding.is_default ? t('common.yes') : t('common.no')}</dd></div>
                                            <div><dt className="text-content-tertiary">{t('modelAdministration.liveAssignments')}</dt><dd className="text-content-primary tnum">{binding.live_assignment_count}</dd></div>
                                            <div><dt className="text-content-tertiary">{t('modelAdministration.runReferences')}</dt><dd className="text-content-primary tnum">{binding.run_reference_count}</dd></div>
                                        </dl>
                                        <p className="mt-2 text-xs text-content-secondary">{t('modelAdministration.tools')}: {binding.tool_tags.join(', ') || t('common.none')}</p>
                                        <p className="mt-1 text-xs text-content-secondary">{t('modelAdministration.dataPolicy')}: {binding.data_policy_tags.join(', ') || t('common.none')}</p>
                                        {canAdminister && (
                                            <div className="mt-3 flex gap-2">
                                                <Button
                                                    type="button"
                                                    size="sm"
                                                    variant="secondary"
                                                    onClick={() => editBinding(binding)}
                                                    disabled={isMutating}
                                                    aria-label={t('modelAdministration.editBindingAction', {
                                                        actor: actor?.display_name ?? binding.actor_id,
                                                        model: entry?.configured_model_alias ?? binding.model_catalog_key ?? binding.model_catalog_id,
                                                    })}
                                                >
                                                    <Pencil aria-hidden="true" className="mr-2 h-3.5 w-3.5" />
                                                    {t('actions.edit')}
                                                </Button>
                                                {binding.enabled && (
                                                    <Button
                                                        type="button"
                                                        size="sm"
                                                        variant="outline"
                                                        disabled={!rationaleReady || isMutating}
                                                        aria-label={t('modelAdministration.disableBindingAction', {
                                                            actor: actor?.display_name ?? binding.actor_id,
                                                            model: entry?.configured_model_alias ?? binding.model_catalog_key ?? binding.model_catalog_id,
                                                        })}
                                                        onClick={() => requestConfirmation({
                                                            title: t('modelAdministration.disableBindingTitle'),
                                                            description: t('modelAdministration.disableBindingDescription', { actor: actor?.display_name ?? binding.actor_id }),
                                                            confirmLabel: t('common.disable'),
                                                            cancelLabel: t('actions.cancel'),
                                                            closeLabel: t('actions.close'),
                                                            onConfirm: () => disableBindingMutation.mutateAsync(binding),
                                                        })}
                                                    >
                                                        {t('common.disable')}
                                                    </Button>
                                                )}
                                                {!binding.enabled && (
                                                    <Button
                                                        type="button"
                                                        size="sm"
                                                        variant="outline"
                                                        disabled={!rationaleReady || isMutating}
                                                        aria-label={t('modelAdministration.enableBindingAction', {
                                                            actor: actor?.display_name ?? binding.actor_id,
                                                            model: entry?.configured_model_alias ?? binding.model_catalog_key ?? binding.model_catalog_id,
                                                        })}
                                                        onClick={() => enableBindingMutation.mutate(binding)}
                                                    >
                                                        {t('common.enable')}
                                                    </Button>
                                                )}
                                            </div>
                                        )}
                                    </article>
                                );
                            })}
                        </div>
                    )}
                </div>

                {canAdminister && (
                    <form className="card space-y-3" onSubmit={submitBinding}>
                        <h3 className="font-semibold text-content-primary">
                            {bindingForm.id
                                ? t('modelAdministration.editBinding')
                                : t('modelAdministration.createBinding')}
                        </h3>
                        <label className="field">
                            <span className="field-lbl">{t('modelAdministration.actor')}</span>
                            <select className="input" value={bindingForm.actorId ?? ''} onChange={event => setBindingForm({ ...bindingForm, actorId: Number(event.target.value) || null })} disabled={Boolean(bindingForm.id)} required>
                                <option value="">{t('modelAdministration.selectActor')}</option>
                                {actors.map(actor => <option key={actor.id} value={actor.id}>{actor.display_name} ({actor.role})</option>)}
                            </select>
                        </label>
                        <label className="field">
                            <span className="field-lbl">{t('modelAdministration.catalogEntry')}</span>
                            <select className="input" value={bindingForm.modelCatalogId ?? ''} onChange={event => setBindingForm({ ...bindingForm, modelCatalogId: Number(event.target.value) || null })} disabled={Boolean(bindingForm.id)} required>
                                <option value="">{t('modelAdministration.selectCatalogEntry')}</option>
                                {catalog.filter(entry => entry.enabled).map(entry => <option key={entry.id} value={entry.id}>{entry.configured_model_alias} ({entry.key})</option>)}
                            </select>
                        </label>
                        <Input label={t('modelAdministration.tools')} value={bindingForm.toolTags} onChange={event => setBindingForm({ ...bindingForm, toolTags: event.target.value })} placeholder="code-edit, shell" />
                        <Input label={t('modelAdministration.dataPolicy')} value={bindingForm.dataPolicyTags} onChange={event => setBindingForm({ ...bindingForm, dataPolicyTags: event.target.value })} placeholder="private-code" />
                        <Checkbox checked={bindingForm.isDefault} onChange={isDefault => setBindingForm({ ...bindingForm, isDefault })} label={t('modelAdministration.defaultBinding')} />
                        <div className="flex gap-2">
                            {bindingForm.id && (
                                <Button type="button" variant="ghost" onClick={() => setBindingForm(EMPTY_BINDING_FORM)}>
                                    {t('actions.cancel')}
                                </Button>
                            )}
                            <Button type="submit" isLoading={createBindingMutation.isPending || updateBindingMutation.isPending} disabled={!rationaleReady || isMutating}>
                                <Plus aria-hidden="true" className="mr-2 h-4 w-4" />
                                {bindingForm.id ? t('actions.save') : t('actions.create')}
                            </Button>
                        </div>
                    </form>
                )}
            </section>
            {confirmationDialog}
        </div>
    );
};

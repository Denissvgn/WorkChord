import { useCallback, useEffect, useMemo, useRef, useState, type ReactNode } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import {
    AlertTriangle,
    Database,
    Link2,
    Plus,
    X,
} from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { ButtonLink } from '../common/ButtonLink';
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
    parseRoutingTags,
} from '../../utils/modelRouting';
import { protectedQueryRetry } from '../../utils/protectedQueries';
import { Button } from '../common/Button';
import { Checkbox } from '../common/Checkbox';
import { Input, RequiredIndicator } from '../common/Input';
import { QueryErrorState, QueryLoadingState } from '../feedback/QueryState';
import { InlineEmptyState } from '../ui';
import type { OverflowMenuItem } from '../ui/OverflowMenu';
import { useToast } from '../feedback/toast';
import { useConfirmDialog } from '../common/useConfirmDialog';
import { ModelCatalog } from './ModelCatalog';
import { ModelBindings } from './ModelBindings';
import { Modal } from '../common/Modal';
import { SlideOverDrawer } from '../ui/SlideOverDrawer';

import { Select } from '../../components/common/Select';
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

interface ConflictResolution {
    scope: 'catalog' | 'binding';
    currentRevision: number;
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

const toIsoDateTime = (value: string) => {
    if (!value) return null;
    const date = new Date(value);
    return Number.isNaN(date.getTime()) ? null : date.toISOString();
};

const conflictRevisionFromError = (error: unknown): number | null => {
    const detail = (
        error as {
            response?: {
                data?: {
                    detail?: {
                        current_revision?: unknown;
                    };
                };
            };
        }
    )?.response?.data?.detail;
    return typeof detail?.current_revision === 'number'
        && Number.isFinite(detail.current_revision)
        ? detail.current_revision
        : null;
};

export interface ModelHeaderActions {
    primaryAction: ReactNode;
    overflowItems: OverflowMenuItem[];
}

export const AgentModelAdministration = ({ onHeaderActionsChange }: {
    onHeaderActionsChange?: (actions: ModelHeaderActions | null) => void;
}) => {
    const { t } = useTranslation();
    const { hasAgentKey } = useAgentAccess();
    const queryClient = useQueryClient();
    const toast = useToast();
    const { requestConfirmation, confirmationDialog } = useConfirmDialog();
    const [catalogForm, setCatalogForm] = useState<CatalogForm>(EMPTY_CATALOG_FORM);
    const [bindingForm, setBindingForm] = useState<BindingForm>(EMPTY_BINDING_FORM);
    // Catalog entries and bindings are created and edited in the shared drawer.
    const [catalogDrawerOpen, setCatalogDrawerOpen] = useState(false);
    const [bindingDrawerOpen, setBindingDrawerOpen] = useState(false);
    const [auditRationale, setAuditRationale] = useState('');
    const reasonRef = useRef('');
    const reconcileRef = useRef(false);
    const [pendingAction, setPendingAction] = useState<(() => void) | null>(null);
    const askReason = (action: () => void) => { setAuditRationale(''); setReconcileLiveAssignments(false); reconcileRef.current = false; setPendingAction(() => action); };
    const [reconcileLiveAssignments, setReconcileLiveAssignments] = useState(false);
    const [conflictMessage, setConflictMessage] = useState<string | null>(null);
    const [conflictResolution, setConflictResolution] = useState<ConflictResolution | null>(null);

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
        if (clearConflict) {
            setConflictMessage(null);
            setConflictResolution(null);
        }
        void queryClient.invalidateQueries({ queryKey: ['agent-capabilities'] });
        void queryClient.invalidateQueries({ queryKey: ['agent-actor-roster'] });
        void queryClient.invalidateQueries({ queryKey: ['agent-model-catalog'] });
        void queryClient.invalidateQueries({ queryKey: ['agent-model-bindings'] });
        void queryClient.invalidateQueries({ queryKey: ['routing-preview'] });
    };

    const mutationError = (
        error: unknown,
        fallback: string,
        conflictScope?: ConflictResolution['scope'],
    ) => {
        const normalized = normalizeApiError(error, fallback);
        if (normalized.status === 409) {
            setConflictMessage(normalized.message);
            const currentRevision = conflictRevisionFromError(error);
            setConflictResolution(
                conflictScope && currentRevision != null
                    ? { scope: conflictScope, currentRevision }
                    : null,
            );
            refreshEvidence(false);
            return;
        }
        toast.error(normalized.message);
    };

    const mutationSuccess = (
        message: string,
        completedForm: 'catalog' | 'binding' | null = null,
    ) => {
        refreshEvidence();
        if (completedForm === 'catalog') {
            setCatalogForm(EMPTY_CATALOG_FORM);
            setCatalogDrawerOpen(false);
        }
        if (completedForm === 'binding') {
            setBindingForm(EMPTY_BINDING_FORM);
            setBindingDrawerOpen(false);
        }
        setReconcileLiveAssignments(false);
        toast.success(message);
    };

    // feedback-policy: mutation pending,toast
    const createCatalogMutation = useMutation({
        mutationFn: (data: AgentModelCatalogCreate) => (
            agentService.createModelCatalogEntry(
                data,
                createAgentCommandMetadata(reasonRef.current),
            )
        ),
        onSuccess: () => mutationSuccess(t('modelAdministration.catalogCreateSuccess'), 'catalog'),
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
            createAgentCommandMetadata(reasonRef.current),
        ),
        onSuccess: () => mutationSuccess(t('modelAdministration.catalogUpdateSuccess'), 'catalog'),
        onError: error => mutationError(
            error,
            t('modelAdministration.catalogMutationFailed'),
            'catalog',
        ),
    });

    // feedback-policy: mutation pending,toast
    const disableCatalogMutation = useMutation({
        mutationFn: (entry: AgentModelCatalogEntry) => (
            agentService.disableModelCatalogEntry(
                entry.id,
                {
                    expected_revision: entry.revision,
                    reconcile_live_assignments: reconcileRef.current,
                },
                createAgentCommandMetadata(reasonRef.current),
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
                    reconcile_live_assignments: reconcileRef.current,
                },
                createAgentCommandMetadata(reasonRef.current),
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
                createAgentCommandMetadata(reasonRef.current),
            )
        ),
        onSuccess: () => mutationSuccess(t('modelAdministration.bindingCreateSuccess'), 'binding'),
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
            createAgentCommandMetadata(reasonRef.current),
        ),
        onSuccess: () => mutationSuccess(t('modelAdministration.bindingUpdateSuccess'), 'binding'),
        onError: error => mutationError(
            error,
            t('modelAdministration.bindingMutationFailed'),
            'binding',
        ),
    });

    // feedback-policy: mutation pending,toast
    const disableBindingMutation = useMutation({
        mutationFn: (binding: AgentModelBinding) => (
            agentService.disableModelBinding(
                binding.id,
                {
                    expected_revision: binding.revision,
                    reconcile_live_assignments: reconcileRef.current,
                },
                createAgentCommandMetadata(reasonRef.current),
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
                    reconcile_live_assignments: reconcileRef.current,
                },
                createAgentCommandMetadata(reasonRef.current),
            )
        ),
        onSuccess: () => mutationSuccess(t('modelAdministration.bindingEnableSuccess')),
        onError: error => mutationError(error, t('modelAdministration.bindingMutationFailed')),
    });

    const actors = useMemo(() => rosterQuery.data ?? [], [rosterQuery.data]);
    const catalog = useMemo(() => catalogQuery.data ?? [], [catalogQuery.data]);
    const bindings = useMemo(() => bindingsQuery.data ?? [], [bindingsQuery.data]);
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

    const submitCatalog = () => {
        if (!canAdminister) return;
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
                    reconcile_live_assignments: reconcileRef.current,
                },
            });
            return;
        }
        createCatalogMutation.mutate(createData);
    };

    const submitBinding = () => {
        if (
            !canAdminister
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
                    reconcile_live_assignments: reconcileRef.current,
                },
            });
            return;
        }
        createBindingMutation.mutate(createData);
    };

    const editCatalog = (entry: AgentModelCatalogEntry) => {
        setConflictMessage(null);
        setConflictResolution(null);
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
        setCatalogDrawerOpen(true);
    };

    const createCatalog = useCallback(() => {
        setCatalogForm(EMPTY_CATALOG_FORM);
        setCatalogDrawerOpen(true);
    }, []);

    const closeCatalogDrawer = () => {
        if (isMutating) return;
        setCatalogForm(EMPTY_CATALOG_FORM);
        setCatalogDrawerOpen(false);
    };

    const editBinding = (binding: AgentModelBinding) => {
        setConflictMessage(null);
        setConflictResolution(null);
        setBindingForm({
            id: binding.id,
            revision: binding.revision,
            actorId: binding.actor_id,
            modelCatalogId: binding.model_catalog_id,
            isDefault: binding.is_default,
            toolTags: binding.tool_tags.join(', '),
            dataPolicyTags: binding.data_policy_tags.join(', '),
        });
        setBindingDrawerOpen(true);
    };

    const createBinding = useCallback(() => {
        setBindingForm(EMPTY_BINDING_FORM);
        setBindingDrawerOpen(true);
    }, []);

    const closeBindingDrawer = () => {
        if (isMutating) return;
        setBindingForm(EMPTY_BINDING_FORM);
        setBindingDrawerOpen(false);
    };

    const prepareConflictOverwrite = () => {
        if (!conflictResolution) return;
        requestConfirmation({
            title: t('modelAdministration.conflictOverwriteTitle'),
            description: t('modelAdministration.conflictOverwriteDescription', {
                revision: conflictResolution.currentRevision,
            }),
            confirmLabel: t('modelAdministration.conflictUseLatestRevision'),
            cancelLabel: t('actions.cancel'),
            closeLabel: t('actions.close'),
            tone: 'warning',
            onConfirm: () => {
                if (conflictResolution.scope === 'catalog') {
                    setCatalogForm(current => ({
                        ...current,
                        revision: conflictResolution.currentRevision,
                    }));
                } else {
                    setBindingForm(current => ({
                        ...current,
                        revision: conflictResolution.currentRevision,
                    }));
                }
                setConflictMessage(null);
                setConflictResolution(null);
            },
        });
    };

    const evidenceLoading = rosterQuery.isPending || catalogQuery.isPending || bindingsQuery.isPending;
    const evidenceError = rosterQuery.error || catalogQuery.error || bindingsQuery.error;
    const evidenceRetrying = (rosterQuery.isError && rosterQuery.isFetching)
        || (catalogQuery.isError && catalogQuery.isFetching)
        || (bindingsQuery.isError && bindingsQuery.isFetching);
    const { isPending: accessLoading, isError: accessFailed, isFetching: accessFetching, refetch: retryAccess } = capabilitiesQuery;
    const { isError: rosterFailed, refetch: retryRoster } = rosterQuery;
    const { isError: catalogFailed, refetch: retryCatalog } = catalogQuery;
    const { isError: bindingsFailed, refetch: retryBindings } = bindingsQuery;
    const retryFailedEvidence = useCallback(() => {
        if (rosterFailed) void retryRoster();
        if (catalogFailed) void retryCatalog();
        if (bindingsFailed) void retryBindings();
    }, [rosterFailed, retryRoster, catalogFailed, retryCatalog, bindingsFailed, retryBindings]);

    const headerActions = useMemo<ModelHeaderActions>(() => {
        const unlockAction = <ButtonLink variant="primary" to="/settings?tab=access">{t('emptyStates.team.unlock')}</ButtonLink>;
        const loadingAction = <Button type="button" disabled>{t('modelAdministration.addModel')}</Button>;
        if (!hasAgentKey) return { primaryAction: unlockAction, overflowItems: [] };
        if (accessLoading) return { primaryAction: loadingAction, overflowItems: [] };
        if (accessFailed) {
            return {
                primaryAction: (
                    <Button type="button" disabled={accessFetching} onClick={() => { void retryAccess(); }}>
                        {t('queryFeedback.retry')}
                    </Button>
                ),
                overflowItems: [],
            };
        }
        if (!canRead) return { primaryAction: unlockAction, overflowItems: [] };
        if (evidenceError) {
            return {
                primaryAction: (
                    <Button type="button" disabled={evidenceRetrying} onClick={retryFailedEvidence}>
                        {t('queryFeedback.retry')}
                    </Button>
                ),
                overflowItems: [],
            };
        }
        if (evidenceLoading) return { primaryAction: loadingAction, overflowItems: [] };
        return {
            primaryAction: canAdminister ? (
                <Button type="button" onClick={catalog.length === 0 ? createCatalog : createBinding} disabled={isMutating}>
                    <Plus className="h-4 w-4" aria-hidden="true" />
                    {t(catalog.length === 0 ? 'modelAdministration.addModel' : 'modelAdministration.addBinding')}
                </Button>
            ) : unlockAction,
            overflowItems: canAdminister ? [
                { label: t('modelAdministration.newModel'), onSelect: createCatalog, disabled: isMutating },
                { label: t('modelAdministration.newBinding'), onSelect: createBinding, disabled: isMutating },
            ] : [],
        };
    }, [hasAgentKey, accessLoading, accessFailed, accessFetching, retryAccess,
        canRead, canAdminister, evidenceError, evidenceLoading, evidenceRetrying, retryFailedEvidence,
        catalog.length, createBinding, createCatalog, isMutating, t]);

    useEffect(() => {
        onHeaderActionsChange?.(headerActions);
    }, [headerActions, onHeaderActionsChange]);

    useEffect(() => () => onHeaderActionsChange?.(null), [onHeaderActionsChange]);

    if (!hasAgentKey) {
        return (
            <InlineEmptyState
                title={t('emptyStates.team.modelsTitle')}
                description={t('emptyStates.team.modelsBody')}
                actions={<ButtonLink variant={onHeaderActionsChange ? 'secondary' : 'primary'} to="/settings?tab=access">{t('emptyStates.team.unlock')}</ButtonLink>}
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

    if (evidenceError) {
        return (
            <QueryErrorState
                error={evidenceError}
                fallback={t('modelAdministration.loadFailed')}
            />
        );
    }

    if (evidenceLoading) {
        return <QueryLoadingState message={t('modelAdministration.loading')} />;
    }

    // The audit reason and the reconcile choice apply to every change, so the drawers show them too.
    const auditFields = (
        <>
            <Input
                label={t('modelAdministration.auditRationale')}
                value={auditRationale}
                onChange={event => setAuditRationale(event.target.value)}
                placeholder={t('modelAdministration.auditRationalePlaceholder')}
                disabled={isMutating}
                required
            />
            <Checkbox
                checked={reconcileLiveAssignments}
                onChange={value => { reconcileRef.current = value; setReconcileLiveAssignments(value); }}
                label={t('modelAdministration.reconcileLiveAssignments')}
                disabled={isMutating}
            />
            <p className="text-xs text-content-secondary">{t('modelAdministration.reconcileWarning')}</p>
        </>
    );

    const conflictNotice = conflictMessage ? (
        <div className="rounded-md border border-feedback-warning-border bg-feedback-warning-muted p-3 text-sm text-feedback-warning-foreground" role="alert">
            <div className="flex items-start gap-2">
                <AlertTriangle aria-hidden="true" className="mt-0.5 h-4 w-4 shrink-0" />
                <div className="flex-1">
                    <p className="font-semibold">{t('modelAdministration.conflictTitle')}</p>
                    <p className="break-words">{conflictMessage}</p>
                    <p className="mt-1 break-words text-xs">
                        {t(
                            conflictResolution
                                ? 'modelAdministration.conflictRecovery'
                                : 'modelAdministration.conflictRefresh',
                        )}
                    </p>
                    {conflictResolution && (
                        <Button
                            type="button"
                            size="sm"
                            variant="outline"
                            className="mt-2"
                            onClick={prepareConflictOverwrite}
                        >
                            {t('modelAdministration.conflictUseLatestRevision')}
                        </Button>
                    )}
                </div>
                <Button
                    type="button"
                    size="sm"
                    variant="ghost"
                    onClick={() => {
                        setConflictMessage(null);
                        setConflictResolution(null);
                    }}
                    aria-label={t('actions.close')}
                >
                    <X aria-hidden="true" className="h-4 w-4" />
                </Button>
            </div>
        </div>
    ) : null;

    return (
        <div className="space-y-5">
            {!catalogDrawerOpen && !bindingDrawerOpen && conflictNotice}

            <section aria-label={catalog.length === 0 ? t('modelAdministration.modelCatalog') : undefined} aria-labelledby={catalog.length > 0 ? "catalog-heading" : undefined}>
                <div className="card space-y-4">
                    {catalog.length > 0 && <div className="flex flex-wrap items-start justify-between gap-3">
                        <div className="min-w-0">
                            <h3 id="catalog-heading" className="flex items-center gap-2 font-semibold text-content-primary">
                                <Database aria-hidden="true" className="h-4 w-4 text-action" />
                                {t('modelAdministration.modelCatalog')}
                            </h3>
                            <p className="text-sm text-content-secondary">{t('modelAdministration.modelCatalogDescription')}</p>
                        </div>
                    </div>}
                    {catalog.length === 0 ? (
                        <InlineEmptyState
                            description={t('emptyStates.team.catalogBody')}
                            actions={canAdminister ? (
                                <Button type="button" variant="secondary" onClick={createCatalog} disabled={isMutating}>{t('modelAdministration.addModel')}</Button>
                            ) : <ButtonLink variant={onHeaderActionsChange ? "secondary" : "primary"} to="/settings?tab=access">{t('emptyStates.team.unlock')}</ButtonLink>}
                        />
                    ) : (
                        <ModelCatalog entries={catalog} canAdminister={canAdminister} busy={isMutating} onEdit={editCatalog} onToggle={entry => askReason(() => entry.enabled ? disableCatalogMutation.mutate(entry) : enableCatalogMutation.mutate(entry))} />
                    )}
                </div>

                {canAdminister && (
                    <SlideOverDrawer
                        open={catalogDrawerOpen}
                        title={catalogForm.id ? t('modelAdministration.editCatalogEntry') : t('modelAdministration.createCatalogEntry')}
                        ariaLabel={catalogForm.id ? t('modelAdministration.editCatalogEntry') : t('modelAdministration.createCatalogEntry')}
                        onClose={closeCatalogDrawer}
                        closeDisabled={isMutating}
                    >
                        <form className="space-y-3 p-5" onSubmit={event => { event.preventDefault(); askReason(submitCatalog); }} aria-busy={isMutating}>
                            {conflictNotice}
                            <fieldset className="min-w-0 space-y-3" disabled={isMutating}>
                                <Input label={t('modelAdministration.catalogKey')} value={catalogForm.key} onChange={event => setCatalogForm({ ...catalogForm, key: event.target.value })} disabled={Boolean(catalogForm.id)} required />
                                <Input label={t('modelAdministration.provider')} value={catalogForm.provider} onChange={event => setCatalogForm({ ...catalogForm, provider: event.target.value })} required />
                                <Input label={t('modelAdministration.configuredAlias')} value={catalogForm.configuredModelAlias} onChange={event => setCatalogForm({ ...catalogForm, configuredModelAlias: event.target.value })} required />
                                <div className="grid grid-cols-1 gap-3 sm:grid-cols-2">
                                    <label className="field">
                                        <span className="field-lbl">{t('modelAdministration.reasoningTier')}</span>
                                        <Select className="input" value={catalogForm.reasoningTier} onChange={event => setCatalogForm({ ...catalogForm, reasoningTier: Number(event.target.value) as 1 | 2 | 3 })}>
                                            <option value={1}>1</option><option value={2}>2</option><option value={3}>3</option>
                                        </Select>
                                    </label>
                                    <label className="field">
                                        <span className="field-lbl">{t('modelAdministration.contextTier')}</span>
                                        <Select className="input" value={catalogForm.contextTier} onChange={event => setCatalogForm({ ...catalogForm, contextTier: event.target.value as CatalogForm['contextTier'] })}>
                                            <option value="small">{t('modelAdministration.small')}</option>
                                            <option value="medium">{t('modelAdministration.medium')}</option>
                                            <option value="large">{t('modelAdministration.large')}</option>
                                        </Select>
                                    </label>
                                    <label className="field">
                                        <span className="field-lbl">{t('modelAdministration.costTier')}</span>
                                        <Select className="input" value={catalogForm.costTier} onChange={event => setCatalogForm({ ...catalogForm, costTier: event.target.value as CatalogForm['costTier'] })}>
                                            <option value="low">{t('modelAdministration.low')}</option>
                                            <option value="medium">{t('modelAdministration.medium')}</option>
                                            <option value="high">{t('modelAdministration.high')}</option>
                                        </Select>
                                    </label>
                                    <label className="field">
                                        <span className="field-lbl">{t('modelAdministration.latencyTier')}</span>
                                        <Select className="input" value={catalogForm.latencyTier} onChange={event => setCatalogForm({ ...catalogForm, latencyTier: event.target.value as CatalogForm['latencyTier'] })}>
                                            <option value="fast">{t('modelAdministration.fast')}</option>
                                            <option value="balanced">{t('modelAdministration.balanced')}</option>
                                            <option value="slow">{t('modelAdministration.slow')}</option>
                                        </Select>
                                    </label>
                                </div>
                                <Input label={t('modelAdministration.modalities')} value={catalogForm.modalityTags} onChange={event => setCatalogForm({ ...catalogForm, modalityTags: event.target.value })} required />
                                <Input label={t('modelAdministration.lastVerified')} type="datetime-local" value={catalogForm.lastVerifiedAt} onChange={event => setCatalogForm({ ...catalogForm, lastVerifiedAt: event.target.value })} />
                                <div className="flex flex-wrap justify-end gap-2">
                                    <Button type="button" variant="ghost" onClick={closeCatalogDrawer}>
                                        {t('actions.cancel')}
                                    </Button>
                                    <Button type="submit" isLoading={createCatalogMutation.isPending || updateCatalogMutation.isPending} disabled={isMutating}>
                                        <Plus aria-hidden="true" className="mr-2 h-4 w-4" />
                                        {catalogForm.id ? t('actions.save') : t('actions.create')}
                                    </Button>
                                </div>
                            </fieldset>
                        </form>
                    </SlideOverDrawer>
                )}
            </section>

            {(catalog.length > 0 || bindingDrawerOpen) && <section aria-label={bindings.length === 0 ? t('modelAdministration.modelBindings') : undefined} aria-labelledby={bindings.length > 0 ? "bindings-heading" : undefined}>
                <div className="card space-y-4">
                    {bindings.length > 0 && <div className="flex flex-wrap items-start justify-between gap-3">
                        <div className="min-w-0">
                            <h3 id="bindings-heading" className="flex items-center gap-2 font-semibold text-content-primary">
                                <Link2 aria-hidden="true" className="h-4 w-4 text-action" />
                                {t('modelAdministration.modelBindings')}
                            </h3>
                            <p className="text-sm text-content-secondary">{t('modelAdministration.modelBindingsDescription')}</p>
                        </div>
                    </div>}
                    {bindings.length === 0 ? (
                        <InlineEmptyState
                            description={t('emptyStates.team.bindingsBody')}
                            actions={canAdminister ? (
                                <Button type="button" variant="secondary" onClick={createBinding} disabled={isMutating}>{t('modelAdministration.addBinding')}</Button>
                            ) : <ButtonLink variant={onHeaderActionsChange ? "secondary" : "primary"} to="/settings?tab=access">{t('emptyStates.team.unlock')}</ButtonLink>}
                        />
                    ) : (
                        <ModelBindings bindings={bindings} actorNames={new Map(actors.map(actor => [actor.id, actor.display_name]))} catalog={catalogById} canAdminister={canAdminister} busy={isMutating} onEdit={editBinding} onToggle={binding => askReason(() => binding.enabled ? disableBindingMutation.mutate(binding) : enableBindingMutation.mutate(binding))} />
                    )}
                </div>

                {canAdminister && (
                    <SlideOverDrawer
                        open={bindingDrawerOpen}
                        title={bindingForm.id ? t('modelAdministration.editBinding') : t('modelAdministration.createBinding')}
                        ariaLabel={bindingForm.id ? t('modelAdministration.editBinding') : t('modelAdministration.createBinding')}
                        onClose={closeBindingDrawer}
                        closeDisabled={isMutating}
                    >
                        <form className="space-y-3 p-5" onSubmit={event => { event.preventDefault(); askReason(submitBinding); }} aria-busy={isMutating}>
                            {conflictNotice}
                            <fieldset className="min-w-0 space-y-3" disabled={isMutating}>
                                <label className="field">
                                    <span className="field-lbl">
                                        {t('modelAdministration.actor')}
                                        <RequiredIndicator />
                                    </span>
                                    <Select className="input" value={bindingForm.actorId ?? ''} onChange={event => setBindingForm({ ...bindingForm, actorId: Number(event.target.value) || null })} disabled={Boolean(bindingForm.id)} required>
                                        <option value="">{t('modelAdministration.selectActor')}</option>
                                        {actors.map(actor => <option key={actor.id} value={actor.id}>{actor.display_name} ({actor.role})</option>)}
                                    </Select>
                                </label>
                                <label className="field">
                                    <span className="field-lbl">
                                        {t('modelAdministration.catalogEntry')}
                                        <RequiredIndicator />
                                    </span>
                                    <Select className="input" value={bindingForm.modelCatalogId ?? ''} onChange={event => setBindingForm({ ...bindingForm, modelCatalogId: Number(event.target.value) || null })} disabled={Boolean(bindingForm.id)} required>
                                        <option value="">{t('modelAdministration.selectCatalogEntry')}</option>
                                        {catalog.filter(entry => entry.enabled).map(entry => <option key={entry.id} value={entry.id}>{entry.configured_model_alias} ({entry.key})</option>)}
                                    </Select>
                                </label>
                                <Input label={t('modelAdministration.tools')} value={bindingForm.toolTags} onChange={event => setBindingForm({ ...bindingForm, toolTags: event.target.value })} placeholder="code-edit, shell" />
                                <Input label={t('modelAdministration.dataPolicy')} value={bindingForm.dataPolicyTags} onChange={event => setBindingForm({ ...bindingForm, dataPolicyTags: event.target.value })} placeholder="private-code" />
                                <Checkbox checked={bindingForm.isDefault} onChange={isDefault => setBindingForm({ ...bindingForm, isDefault })} label={t('modelAdministration.defaultBinding')} />
                                <div className="flex flex-wrap justify-end gap-2">
                                    <Button type="button" variant="ghost" onClick={closeBindingDrawer}>
                                        {t('actions.cancel')}
                                    </Button>
                                    <Button type="submit" isLoading={createBindingMutation.isPending || updateBindingMutation.isPending} disabled={isMutating}>
                                        <Plus aria-hidden="true" className="mr-2 h-4 w-4" />
                                        {bindingForm.id ? t('actions.save') : t('actions.create')}
                                    </Button>
                                </div>
                            </fieldset>
                        </form>
                    </SlideOverDrawer>
                )}
            </section>}
            {confirmationDialog}
            <Modal open={pendingAction !== null} title={t('modelAdministration.auditControls')} onClose={() => setPendingAction(null)} closeLabel={t('actions.close')}>
                <form className="space-y-3" onSubmit={event => { event.preventDefault(); if (!rationaleReady || !pendingAction) return; reasonRef.current = auditRationale.trim(); const action = pendingAction; setPendingAction(null); action(); }}>
                    {auditFields}
                    <div className="flex justify-end gap-2">
                        <Button type="button" variant="ghost" onClick={() => setPendingAction(null)}>{t('actions.cancel')}</Button>
                        <Button type="submit" disabled={!rationaleReady || isMutating}>{t('actions.save')}</Button>
                    </div>
                </form>
            </Modal>
        </div>
    );
};

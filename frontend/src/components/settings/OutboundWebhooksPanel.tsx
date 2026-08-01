import { useId, useMemo, useState } from 'react';
import type { FormEvent } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import {
    Edit2,
    Loader2,
    Plus,
    RefreshCw,
    Save,
    Send,
    Trash2,
    Webhook,
    X,
} from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { Button } from '../common/Button';
import { useConfirmDialog } from '../common/useConfirmDialog';
import { Checkbox } from '../common/Checkbox';
import { Input } from '../common/Input';
import { outboundWebhookService } from '../../services/outboundWebhookService';
import { getAdminAccessErrorMessage } from '../../utils/adminAccess';
import { useAdminAccess } from '../../hooks/useAdminAccess';
import { protectedQueryRetry } from '../../utils/protectedQueries';
import { formatDateTime } from '../../utils/formatDate';
import { QueryErrorState } from '../feedback/QueryState';
import { useToast } from '../feedback/toast';
import type {
    OutboundWebhookDelivery,
    OutboundWebhookDeliveryStatus,
    OutboundWebhookTarget,
    OutboundWebhookTargetCreate,
    OutboundWebhookTargetUpdate,
} from '../../types/outboundWebhook';

interface TargetFormState {
    name: string;
    description: string;
    url: string;
    enabled: boolean;
    subscribedEvents: string[];
    secret: string;
    clearSecret: boolean;
    headersJson: string;
}

interface TargetFormErrors {
    name?: string;
    url?: string;
    subscribedEvents?: string;
    headersJson?: string;
}

interface EventOption {
    value: string;
    labelKey: string;
}

const eventGroups: Array<{ labelKey: string; options: EventOption[] }> = [
    {
        labelKey: 'settingsWebhooks.groups.all',
        options: [
            { value: '*', labelKey: 'settingsWebhooks.events.domainAll' },
        ],
    },
    {
        labelKey: 'settingsWebhooks.groups.tasksAgents',
        options: [
            { value: 'task.*', labelKey: 'settingsWebhooks.events.taskAll' },
            { value: 'task.created', labelKey: 'settingsWebhooks.events.taskCreated' },
            { value: 'task.updated', labelKey: 'settingsWebhooks.events.taskUpdated' },
            { value: 'task.status_changed', labelKey: 'settingsWebhooks.events.taskStatusChanged' },
            { value: 'task.claimed', labelKey: 'settingsWebhooks.events.taskClaimed' },
            { value: 'agent.*', labelKey: 'settingsWebhooks.events.agentAll' },
        ],
    },
    {
        labelKey: 'settingsWebhooks.groups.portfolio',
        options: [
            { value: 'project.*', labelKey: 'settingsWebhooks.events.projectAll' },
            { value: 'project.health_updated', labelKey: 'settingsWebhooks.events.projectHealthUpdated' },
            { value: 'release.*', labelKey: 'settingsWebhooks.events.releaseAll' },
            { value: 'release.shipped', labelKey: 'settingsWebhooks.events.releaseShipped' },
        ],
    },
    {
        labelKey: 'settingsWebhooks.groups.intake',
        options: [
            { value: 'triage.*', labelKey: 'settingsWebhooks.events.triageAll' },
            { value: 'triage.converted', labelKey: 'settingsWebhooks.events.triageConverted' },
            { value: 'request_source.*', labelKey: 'settingsWebhooks.events.requestSourceAll' },
            { value: 'request_source.linked', labelKey: 'settingsWebhooks.events.requestSourceLinked' },
        ],
    },
    {
        labelKey: 'settingsWebhooks.groups.externalTraceability',
        options: [
            { value: 'external_link.*', labelKey: 'settingsWebhooks.events.externalLinkAll' },
            { value: 'github.*', labelKey: 'settingsWebhooks.events.githubAll' },
            { value: 'github.pr_merged', labelKey: 'settingsWebhooks.events.githubPrMerged' },
            { value: 'webhook.test', labelKey: 'settingsWebhooks.events.testDelivery' },
        ],
    },
];

const emptyForm: TargetFormState = {
    name: '',
    description: '',
    url: '',
    enabled: true,
    subscribedEvents: ['task.*', 'project.*', 'triage.*'],
    secret: '',
    clearSecret: false,
    headersJson: '{}',
};

const statusClasses: Record<OutboundWebhookDeliveryStatus, string> = {
    pending: 'bg-feedback-warning-muted text-feedback-warning-foreground border-feedback-warning-border',
    delivered: 'bg-feedback-success-muted text-feedback-success-foreground border-feedback-success-border',
    failed: 'bg-feedback-danger-muted text-feedback-danger-foreground border-feedback-danger-border',
};

const parseHeaders = (
    headersJson: string,
    messages: { objectError: string; valueError: string },
): Record<string, string> => {
    const trimmed = headersJson.trim();
    if (!trimmed) {
        return {};
    }
    const parsed = JSON.parse(trimmed) as unknown;
    if (!parsed || Array.isArray(parsed) || typeof parsed !== 'object') {
        throw new Error(messages.objectError);
    }
    return Object.fromEntries(
        Object.entries(parsed as Record<string, unknown>).map(([key, value]) => {
            if (typeof value !== 'string') {
                throw new Error(messages.valueError);
            }
            return [key, value];
        })
    );
};

const targetToForm = (target: OutboundWebhookTarget): TargetFormState => ({
    name: target.name,
    description: target.description || '',
    url: target.url,
    enabled: target.enabled,
    subscribedEvents: target.subscribed_events_json,
    secret: '',
    clearSecret: false,
    headersJson: JSON.stringify(target.headers_json || {}, null, 2),
});

const formsMatch = (left: TargetFormState, right: TargetFormState) => (
    JSON.stringify(left) === JSON.stringify(right)
);

export const OutboundWebhooksPanel = () => {
    const { t } = useTranslation();
    const queryClient = useQueryClient();
    const { hasAdminKey } = useAdminAccess();
    const toast = useToast();
    const { requestConfirmation, confirmationDialog } = useConfirmDialog();
    const headersInputId = useId();
    const [form, setForm] = useState<TargetFormState>(emptyForm);
    const [baselineForm, setBaselineForm] = useState<TargetFormState>(emptyForm);
    const [formErrors, setFormErrors] = useState<TargetFormErrors>({});
    const [editingTargetId, setEditingTargetId] = useState<number | null>(null);
    const [deliveryStatus, setDeliveryStatus] = useState<OutboundWebhookDeliveryStatus | ''>('');
    const [deliveryTargetId, setDeliveryTargetId] = useState<number | ''>('');

    const { data: targets = [], isLoading: targetsLoading, error: targetsError, refetch: refetchTargets } = useQuery({
        queryKey: ['outbound-webhook-targets'],
        queryFn: outboundWebhookService.getTargets,
        enabled: hasAdminKey,
        retry: protectedQueryRetry,
    });

    const { data: deliveries = [], isLoading: deliveriesLoading, error: deliveriesError, refetch: refetchDeliveries } = useQuery({
        queryKey: ['outbound-webhook-deliveries', deliveryTargetId, deliveryStatus],
        queryFn: () => outboundWebhookService.getDeliveries({
            target_id: deliveryTargetId === '' ? null : deliveryTargetId,
            status: deliveryStatus || null,
            limit: 50,
        }),
        enabled: hasAdminKey,
        retry: protectedQueryRetry,
    });

    const knownEventLabels = useMemo(() => {
        const labels = new Map<string, string>();
        eventGroups.forEach(group => group.options.forEach(option => labels.set(option.value, t(option.labelKey))));
        return labels;
    }, [t]);

    const hasUnsavedChanges = !formsMatch(form, baselineForm);

    const statusBadge = (status: OutboundWebhookDeliveryStatus) => (
        <span className={`inline-flex rounded border px-2 py-0.5 text-xs font-medium ${statusClasses[status]}`}>
            {t(`settingsWebhooks.statuses.${status}`)}
        </span>
    );

    const invalidateWebhookQueries = () => {
        queryClient.invalidateQueries({ queryKey: ['outbound-webhook-targets'] });
        queryClient.invalidateQueries({ queryKey: ['outbound-webhook-deliveries'] });
    };

    const resetFormNow = () => {
        setEditingTargetId(null);
        setForm(emptyForm);
        setBaselineForm(emptyForm);
        setFormErrors({});
    };

    // feedback-policy: mutation pending,toast - the form is frozen and retains its draft on failure.
    const createMutation = useMutation({
        mutationFn: outboundWebhookService.createTarget,
        onSuccess: () => {
            invalidateWebhookQueries();
            resetFormNow();
            toast.success(t('settingsWebhooks.createSuccess'));
        },
        onError: (err: unknown) => {
            toast.error(getAdminAccessErrorMessage(err, {
                missingOrInvalid: t('settings.adminAccessMissingOrInvalid'),
                backendNotConfigured: t('settings.adminAccessBackendNotConfigured'),
                fallback: t('settingsWebhooks.createFailed'),
            }));
        },
    });

    // feedback-policy: mutation pending,toast - the form is frozen and retains its draft on failure.
    const updateMutation = useMutation({
        mutationFn: ({ targetId, data }: { targetId: number; data: OutboundWebhookTargetUpdate }) => (
            outboundWebhookService.updateTarget(targetId, data)
        ),
        onSuccess: () => {
            invalidateWebhookQueries();
            resetFormNow();
            toast.success(t('settingsWebhooks.saveSuccess'));
        },
        onError: (err: unknown) => {
            toast.error(getAdminAccessErrorMessage(err, {
                missingOrInvalid: t('settings.adminAccessMissingOrInvalid'),
                backendNotConfigured: t('settings.adminAccessBackendNotConfigured'),
                fallback: t('settingsWebhooks.saveFailed'),
            }));
        },
    });

    // feedback-policy: mutation pending,toast - row controls are locked and the active target is identified inline.
    const toggleMutation = useMutation({
        mutationFn: ({ targetId, enabled }: { targetId: number; enabled: boolean }) => (
            outboundWebhookService.updateTarget(targetId, { enabled })
        ),
        onSuccess: (_result, { targetId, enabled }) => {
            invalidateWebhookQueries();
            if (editingTargetId === targetId) {
                setForm(current => ({ ...current, enabled }));
                setBaselineForm(current => ({ ...current, enabled }));
            }
        },
        onError: (err: unknown) => {
            toast.error(getAdminAccessErrorMessage(err, {
                missingOrInvalid: t('settings.adminAccessMissingOrInvalid'),
                backendNotConfigured: t('settings.adminAccessBackendNotConfigured'),
                fallback: t('settingsWebhooks.updateFailed'),
            }));
        },
    });

    // feedback-policy: mutation pending,toast - row controls are locked and the active target is identified inline.
    const deleteMutation = useMutation({
        mutationFn: outboundWebhookService.deleteTarget,
        onSuccess: (_response, targetId) => {
            invalidateWebhookQueries();
            if (editingTargetId === targetId) {
                resetFormNow();
            }
            toast.success(t('settingsWebhooks.deleteSuccess'));
        },
        onError: (err: unknown) => {
            toast.error(getAdminAccessErrorMessage(err, {
                missingOrInvalid: t('settings.adminAccessMissingOrInvalid'),
                backendNotConfigured: t('settings.adminAccessBackendNotConfigured'),
                fallback: t('settingsWebhooks.deleteFailed'),
            }));
        },
    });

    // feedback-policy: mutation pending,toast - row controls are locked and the active target is identified inline.
    const testMutation = useMutation({
        mutationFn: outboundWebhookService.testTarget,
        onSuccess: (response) => {
            invalidateWebhookQueries();
            const message = response.delivery.status === 'delivered'
                ? t('settingsWebhooks.testSent')
                : t('settingsWebhooks.testFailed');
            if (response.delivery.status === 'delivered') toast.success(message);
            else toast.error(message);
        },
        onError: (err: unknown) => {
            toast.error(getAdminAccessErrorMessage(err, {
                missingOrInvalid: t('settings.adminAccessMissingOrInvalid'),
                backendNotConfigured: t('settings.adminAccessBackendNotConfigured'),
                fallback: t('settingsWebhooks.testRequestFailed'),
            }));
        },
    });

    // feedback-policy: mutation pending,toast - retry controls lock and the active delivery is identified inline.
    const retryMutation = useMutation({
        mutationFn: outboundWebhookService.retryDelivery,
        onSuccess: (response) => {
            queryClient.invalidateQueries({ queryKey: ['outbound-webhook-deliveries'] });
            const message = response.delivery.status === 'delivered'
                ? t('settingsWebhooks.retrySucceeded')
                : t('settingsWebhooks.retryFailed');
            if (response.delivery.status === 'delivered') toast.success(message);
            else toast.error(message);
        },
        onError: (err: unknown) => {
            toast.error(getAdminAccessErrorMessage(err, {
                missingOrInvalid: t('settings.adminAccessMissingOrInvalid'),
                backendNotConfigured: t('settings.adminAccessBackendNotConfigured'),
                fallback: t('settingsWebhooks.retryRequestFailed'),
            }));
        },
    });

    const updateField = <K extends keyof TargetFormState>(field: K, value: TargetFormState[K]) => {
        setForm(prev => ({ ...prev, [field]: value }));
        if (field === 'name' || field === 'url' || field === 'headersJson') {
            setFormErrors(prev => ({ ...prev, [field]: undefined }));
        }
    };

    const updateSecret = (value: string) => {
        setForm(prev => ({ ...prev, secret: value, clearSecret: false }));
    };

    const updateClearSecret = (checked: boolean) => {
        setForm(prev => ({
            ...prev,
            clearSecret: checked,
            secret: checked ? '' : prev.secret,
        }));
    };

    const toggleEvent = (eventValue: string, checked: boolean) => {
        setForm(prev => ({
            ...prev,
            subscribedEvents: checked
                ? Array.from(new Set([...prev.subscribedEvents, eventValue]))
                : prev.subscribedEvents.filter(value => value !== eventValue),
        }));
        setFormErrors(prev => ({ ...prev, subscribedEvents: undefined }));
    };

    const validateForm = (): TargetFormErrors => {
        const errors: TargetFormErrors = {};
        const name = form.name.trim();
        const url = form.url.trim();

        if (!name) {
            errors.name = t('settingsWebhooks.nameRequired');
        }

        if (!url) {
            errors.url = t('settingsWebhooks.urlRequired');
        } else {
            try {
                const endpoint = new URL(url);
                if (endpoint.protocol !== 'http:' && endpoint.protocol !== 'https:') {
                    errors.url = t('settingsWebhooks.urlInvalid');
                }
            } catch {
                errors.url = t('settingsWebhooks.urlInvalid');
            }
        }

        if (form.subscribedEvents.length === 0) {
            errors.subscribedEvents = t('settingsWebhooks.eventRequired');
        }

        try {
            parseHeaders(form.headersJson, {
                objectError: t('settingsWebhooks.headersObjectError'),
                valueError: t('settingsWebhooks.headerValuesError'),
            });
        } catch (error) {
            errors.headersJson = error instanceof Error
                ? error.message
                : t('settingsWebhooks.formInvalid');
        }

        return errors;
    };

    const payloadFromForm = (): OutboundWebhookTargetCreate | OutboundWebhookTargetUpdate => {
        const name = form.name.trim();
        const url = form.url.trim();
        const basePayload: OutboundWebhookTargetCreate = {
            name,
            description: form.description.trim() || null,
            url,
            enabled: form.enabled,
            subscribed_events_json: form.subscribedEvents,
            headers_json: parseHeaders(form.headersJson, {
                objectError: t('settingsWebhooks.headersObjectError'),
                valueError: t('settingsWebhooks.headerValuesError'),
            }),
        };

        if (editingTargetId !== null) {
            if (form.clearSecret) {
                return { ...basePayload, secret: null };
            }
            if (form.secret.trim()) {
                return { ...basePayload, secret: form.secret.trim() };
            }
            return basePayload;
        }

        return { ...basePayload, secret: form.secret.trim() || null };
    };

    const handleSubmit = (event: FormEvent<HTMLFormElement>) => {
        event.preventDefault();
        if (isSaving) return;

        const errors = validateForm();
        setFormErrors(errors);
        if (Object.keys(errors).length > 0) {
            toast.error(t('settingsWebhooks.formInvalid'));
            return;
        }

        const payload = payloadFromForm();

        if (editingTargetId !== null) {
            updateMutation.mutate({ targetId: editingTargetId, data: payload });
        } else {
            createMutation.mutate(payload as OutboundWebhookTargetCreate);
        }
    };

    const editTargetNow = (target: OutboundWebhookTarget) => {
        const nextForm = targetToForm(target);
        setEditingTargetId(target.id);
        setForm(nextForm);
        setBaselineForm(nextForm);
        setFormErrors({});
    };

    const requestDraftTransition = (onDiscard: () => void) => {
        if (isSaving || targetActionPending) return;
        if (!hasUnsavedChanges) {
            onDiscard();
            return;
        }
        requestConfirmation({
            title: t('settingsWebhooks.discardDraftTitle'),
            description: t('settingsWebhooks.discardDraftDescription'),
            confirmLabel: t('actions.discard'),
            cancelLabel: t('actions.cancel'),
            closeLabel: t('actions.close'),
            tone: 'warning',
            onConfirm: onDiscard,
        });
    };

    const handleEdit = (target: OutboundWebhookTarget) => {
        if (editingTargetId === target.id) return;
        requestDraftTransition(() => editTargetNow(target));
    };

    const handleDelete = (target: OutboundWebhookTarget) => {
        requestConfirmation({
            title: t('actions.delete'),
            description: t('settingsWebhooks.deleteConfirm', { name: target.name }),
            confirmLabel: t('actions.delete'),
            cancelLabel: t('actions.cancel'),
            closeLabel: t('actions.close'),
            onConfirm: () => deleteMutation.mutateAsync(target.id),
        });
    };

    const isSaving = createMutation.isPending || updateMutation.isPending;
    const targetActionPending = toggleMutation.isPending
        || deleteMutation.isPending
        || testMutation.isPending;
    const formLocked = isSaving || targetActionPending;

    if (targetsLoading) {
        return (
            <div className="flex items-center justify-center py-12">
                <Loader2 className="h-8 w-8 animate-spin text-action" />
                <span className="ml-3 text-content-secondary">{t('settingsWebhooks.loadingTargets')}</span>
            </div>
        );
    }

    if (targetsError) {
        const message = getAdminAccessErrorMessage(targetsError, {
            missingOrInvalid: t('settings.adminAccessMissingOrInvalid'),
            backendNotConfigured: t('settings.adminAccessBackendNotConfigured'),
            fallback: t('settings.webhookTargetsLoadFailed'),
        });
        return <QueryErrorState message={message} onRetry={() => void refetchTargets()} />;
    }

    return (
        <div className="max-w-7xl space-y-5">
            <form onSubmit={handleSubmit} className="card space-y-5" aria-busy={formLocked} noValidate>
                <fieldset disabled={formLocked} className="contents">
                <div className="flex flex-col items-stretch justify-between gap-4 sm:flex-row sm:items-start">
                    <div className="flex min-w-0 items-center gap-3">
                        <div className="rounded-full bg-action p-2 text-content-emphasis">
                            <Webhook className="h-5 w-5" aria-hidden="true" />
                        </div>
                        <div className="min-w-0">
                            <h2 className="break-words text-lg font-semibold text-content-primary">{t('settingsWebhooks.title')}</h2>
                            <p className="break-words text-sm text-content-secondary">
                                {t('settingsWebhooks.description')}
                            </p>
                        </div>
                    </div>
                    <Button
                        type="button"
                        variant="outline"
                        size="sm"
                        onClick={() => requestDraftTransition(resetFormNow)}
                        className="sm:shrink-0"
                    >
                        <Plus className="mr-1 h-4 w-4" aria-hidden="true" />
                        {t('settingsWebhooks.newTarget')}
                    </Button>
                </div>

                <div className="grid grid-cols-1 gap-4 lg:grid-cols-12">
                    <div className="lg:col-span-3">
                        <Input
                            label={t('settingsWebhooks.name')}
                            value={form.name}
                            onChange={event => updateField('name', event.target.value)}
                            placeholder={t('settingsWebhooks.namePlaceholder')}
                            error={formErrors.name}
                            required
                        />
                    </div>
                    <div className="lg:col-span-5">
                        <Input
                            label={t('settingsWebhooks.url')}
                            value={form.url}
                            onChange={event => updateField('url', event.target.value)}
                            placeholder={t('settingsWebhooks.urlPlaceholder')}
                            error={formErrors.url}
                            type="url"
                            inputMode="url"
                            autoCapitalize="none"
                            autoCorrect="off"
                            spellCheck={false}
                            required
                        />
                    </div>
                    <div className="lg:col-span-2">
                        <Input
                            label={t('settingsWebhooks.secret')}
                            type="password"
                            value={form.secret}
                            onChange={event => updateSecret(event.target.value)}
                            placeholder={editingTargetId !== null ? t('settingsWebhooks.leaveUnchanged') : t('settingsWebhooks.optional')}
                            disabled={form.clearSecret}
                            autoComplete="new-password"
                        />
                    </div>
                    <div className="flex items-end lg:col-span-2">
                        <Checkbox
                            label={t('settingsWebhooks.enabled')}
                            checked={form.enabled}
                            onChange={checked => updateField('enabled', checked)}
                            className="pb-2"
                        />
                    </div>
                    <div className="lg:col-span-6">
                        <Input
                            label={t('settingsWebhooks.descriptionField')}
                            value={form.description}
                            onChange={event => updateField('description', event.target.value)}
                            placeholder={t('settingsWebhooks.descriptionPlaceholder')}
                        />
                    </div>
                    <div className="lg:col-span-6">
                        <label htmlFor={headersInputId} className="mb-1 block text-sm font-medium text-content-primary">{t('settingsWebhooks.headersJson')}</label>
                        <textarea
                            id={headersInputId}
                            value={form.headersJson}
                            onChange={event => updateField('headersJson', event.target.value)}
                            rows={3}
                            aria-invalid={Boolean(formErrors.headersJson)}
                            aria-describedby={formErrors.headersJson ? `${headersInputId}-error` : undefined}
                            className="w-full rounded-md border border-border-strong px-3 py-2 font-mono text-sm shadow-sm focus:border-action focus:outline-none focus:ring-1 focus:ring-focus aria-[invalid=true]:border-feedback-danger"
                            placeholder='{"X-Route": "workchord"}'
                            spellCheck={false}
                        />
                        {formErrors.headersJson && (
                            <p id={`${headersInputId}-error`} className="field-error" role="alert">
                                {formErrors.headersJson}
                            </p>
                        )}
                    </div>
                    {editingTargetId !== null && (
                        <div className="lg:col-span-12">
                            <Checkbox
                                label={t('settingsWebhooks.clearStoredSecret')}
                                checked={form.clearSecret}
                                onChange={updateClearSecret}
                            />
                        </div>
                    )}
                </div>

                <fieldset className="space-y-3">
                    <div>
                        <legend className="text-sm font-semibold text-content-primary">{t('settingsWebhooks.subscribedEvents')}</legend>
                        <p className="text-xs text-content-secondary">{t('settingsWebhooks.subscribedEventsHelp')}</p>
                    </div>
                    <div className="grid grid-cols-1 gap-3 md:grid-cols-2 xl:grid-cols-5">
                        {eventGroups.map(group => (
                            <div key={group.labelKey} className="rounded-md border border-border p-3">
                                <div className="mb-2 text-xs font-semibold uppercase text-content-secondary">{t(group.labelKey)}</div>
                                <div className="space-y-2">
                                    {group.options.map(option => (
                                        <Checkbox
                                            key={option.value}
                                            label={t(option.labelKey)}
                                            checked={form.subscribedEvents.includes(option.value)}
                                            onChange={checked => toggleEvent(option.value, checked)}
                                            aria-describedby={formErrors.subscribedEvents ? 'webhook-events-error' : undefined}
                                        />
                                    ))}
                                </div>
                            </div>
                        ))}
                    </div>
                    {formErrors.subscribedEvents && (
                        <p id="webhook-events-error" className="field-error" role="alert">
                            {formErrors.subscribedEvents}
                        </p>
                    )}
                </fieldset>

                <div className="flex flex-col-reverse gap-2 sm:flex-row sm:justify-end">
                    {editingTargetId !== null && (
                        <Button
                            type="button"
                            variant="ghost"
                            size="sm"
                            onClick={() => requestDraftTransition(resetFormNow)}
                        >
                            <X className="mr-1 h-4 w-4" aria-hidden="true" />
                            {t('settingsWebhooks.cancel')}
                        </Button>
                    )}
                    <Button type="submit" size="sm" isLoading={isSaving}>
                        <Save className="mr-1 h-4 w-4" aria-hidden="true" />
                        {editingTargetId !== null ? t('settingsWebhooks.saveTarget') : t('settingsWebhooks.createTarget')}
                    </Button>
                </div>
                </fieldset>
            </form>

            <div className="overflow-hidden rounded-lg border border-border bg-surface-card">
                <div className="flex items-center justify-between border-b border-border px-4 py-3">
                    <h3 className="font-semibold text-content-primary">{t('settingsWebhooks.targets')}</h3>
                    <span className="text-sm text-content-secondary">{t('settingsWebhooks.configuredCount', { count: targets.length })}</span>
                </div>
                <div className="overflow-x-auto">
                    <table className="min-w-full divide-y divide-border text-sm">
                        <thead className="bg-surface-muted text-left text-xs font-semibold uppercase text-content-secondary">
                            <tr>
                                <th className="px-3 py-2">{t('settingsWebhooks.enabled')}</th>
                                <th className="px-3 py-2">{t('settingsWebhooks.target')}</th>
                                <th className="px-3 py-2">{t('settingsWebhooks.subscriptions')}</th>
                                <th className="px-3 py-2">{t('settingsWebhooks.security')}</th>
                                <th className="px-3 py-2">{t('settingsWebhooks.updated')}</th>
                                <th className="px-3 py-2 text-right">{t('settingsWebhooks.actions')}</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-border-subtle">
                            {targets.map(target => (
                                <tr key={target.id} className="align-top">
                                    <td className="px-3 py-3">
                                        <div className="flex items-center gap-2">
                                            <Checkbox
                                                checked={target.enabled}
                                                onChange={checked => toggleMutation.mutate({ targetId: target.id, enabled: checked })}
                                                disabled={targetActionPending || isSaving}
                                                aria-label={`${target.name}: ${t('settingsWebhooks.enabled')}`}
                                            />
                                            {toggleMutation.isPending && toggleMutation.variables?.targetId === target.id && (
                                                <span className="inline-flex text-content-secondary">
                                                    <Loader2 className="h-4 w-4 animate-spin" aria-hidden="true" />
                                                    <span className="sr-only">{t('common.saving')}</span>
                                                </span>
                                            )}
                                        </div>
                                    </td>
                                    <td className="px-3 py-3">
                                        <div className="max-w-lg break-words font-medium text-content-primary">{target.name}</div>
                                        <div className="mt-1 max-w-lg break-all text-xs text-content-secondary">{target.url}</div>
                                        {target.description && (
                                            <div className="mt-1 max-w-lg break-words text-xs text-content-secondary [overflow-wrap:anywhere]">{target.description}</div>
                                        )}
                                    </td>
                                    <td className="px-3 py-3">
                                        <div className="flex max-w-md flex-wrap gap-1">
                                            {target.subscribed_events_json.map(eventName => (
                                                <span key={eventName} className="max-w-full break-all rounded bg-surface-subtle px-2 py-0.5 text-xs text-content-primary">
                                                    {knownEventLabels.get(eventName) || eventName}
                                                </span>
                                            ))}
                                        </div>
                                    </td>
                                    <td className="px-3 py-3">
                                        <div className="space-y-1 text-xs text-content-secondary">
                                            <div>{target.has_secret ? t('settingsWebhooks.signed') : t('settingsWebhooks.unsigned')}</div>
                                            <div>{t('settingsWebhooks.customHeaders', { count: Object.keys(target.headers_json || {}).length })}</div>
                                        </div>
                                    </td>
                                    <td className="px-3 py-3 text-content-secondary">{formatDateTime(target.updated_at)}</td>
                                    <td className="px-3 py-3">
                                        <div className="flex justify-end gap-2">
                                            <Button
                                                type="button"
                                                variant="outline"
                                                size="sm"
                                                onClick={() => testMutation.mutate(target.id)}
                                                isLoading={testMutation.isPending && testMutation.variables === target.id}
                                                disabled={targetActionPending || isSaving}
                                                aria-label={`${t('settingsWebhooks.test')}: ${target.name}`}
                                            >
                                                <Send className="h-3.5 w-3.5" aria-hidden="true" />
                                            </Button>
                                            <Button
                                                type="button"
                                                variant="outline"
                                                size="sm"
                                                onClick={() => handleEdit(target)}
                                                disabled={targetActionPending || isSaving}
                                                aria-label={`${t('actions.edit')}: ${target.name}`}
                                            >
                                                <Edit2 className="h-3.5 w-3.5" aria-hidden="true" />
                                            </Button>
                                            <Button
                                                type="button"
                                                variant="danger"
                                                size="sm"
                                                onClick={() => handleDelete(target)}
                                                isLoading={deleteMutation.isPending && deleteMutation.variables === target.id}
                                                disabled={targetActionPending || isSaving}
                                                aria-label={`${t('actions.delete')}: ${target.name}`}
                                            >
                                                <Trash2 className="h-3.5 w-3.5" aria-hidden="true" />
                                            </Button>
                                        </div>
                                    </td>
                                </tr>
                            ))}
                            {targets.length === 0 && (
                                <tr>
                                    <td className="px-3 py-8 text-center text-content-secondary" colSpan={6}>
                                        {t('settingsWebhooks.noTargets')}
                                    </td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                </div>
            </div>

            <div className="overflow-hidden rounded-lg border border-border bg-surface-card">
                <div className="flex flex-col gap-3 border-b border-border px-4 py-3 md:flex-row md:items-center md:justify-between">
                    <div>
                        <h3 className="font-semibold text-content-primary">{t('settingsWebhooks.recentDeliveries')}</h3>
                        <p className="text-sm text-content-secondary">{t('settingsWebhooks.deliveriesHelp')}</p>
                    </div>
                    <div className="flex flex-wrap gap-2">
                        <select
                            value={deliveryTargetId}
                            onChange={event => setDeliveryTargetId(event.target.value ? Number(event.target.value) : '')}
                            aria-label={t('settingsWebhooks.target')}
                            disabled={deliveriesLoading}
                            className="min-w-0 flex-1 rounded-md border border-border-strong px-3 py-2 text-sm shadow-sm focus:border-action focus:outline-none focus:ring-1 focus:ring-focus sm:flex-none"
                        >
                            <option value="">{t('settingsWebhooks.allTargets')}</option>
                            {targets.map(target => (
                                <option key={target.id} value={target.id}>{target.name}</option>
                            ))}
                        </select>
                        <select
                            value={deliveryStatus}
                            onChange={event => setDeliveryStatus(event.target.value as OutboundWebhookDeliveryStatus | '')}
                            aria-label={t('settingsWebhooks.status')}
                            disabled={deliveriesLoading}
                            className="min-w-0 flex-1 rounded-md border border-border-strong px-3 py-2 text-sm shadow-sm focus:border-action focus:outline-none focus:ring-1 focus:ring-focus sm:flex-none"
                        >
                            <option value="">{t('settingsWebhooks.allStatuses')}</option>
                            <option value="delivered">{t('settingsWebhooks.statuses.delivered')}</option>
                            <option value="failed">{t('settingsWebhooks.statuses.failed')}</option>
                            <option value="pending">{t('settingsWebhooks.statuses.pending')}</option>
                        </select>
                    </div>
                </div>
                {deliveriesError ? (
                    <div className="p-4">
                        <QueryErrorState error={deliveriesError} onRetry={() => void refetchDeliveries()} />
                    </div>
                ) : (
                <div className="overflow-x-auto">
                    <table className="min-w-full divide-y divide-border text-sm">
                        <thead className="bg-surface-muted text-left text-xs font-semibold uppercase text-content-secondary">
                            <tr>
                                <th className="px-3 py-2">{t('settingsWebhooks.status')}</th>
                                <th className="px-3 py-2">{t('settingsWebhooks.event')}</th>
                                <th className="px-3 py-2">{t('settingsWebhooks.target')}</th>
                                <th className="px-3 py-2">{t('settingsWebhooks.attempts')}</th>
                                <th className="px-3 py-2">{t('settingsWebhooks.lastAttempt')}</th>
                                <th className="px-3 py-2">{t('settingsWebhooks.error')}</th>
                                <th className="px-3 py-2 text-right">{t('settingsWebhooks.actions')}</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-border-subtle">
                            {deliveriesLoading ? (
                                <tr>
                                    <td className="px-3 py-8 text-center text-content-secondary" colSpan={7}>
                                        {t('settingsWebhooks.loadingDeliveries')}
                                    </td>
                                </tr>
                            ) : deliveries.map((delivery: OutboundWebhookDelivery) => (
                                <tr key={delivery.id} className="align-top">
                                    <td className="px-3 py-3">{statusBadge(delivery.status)}</td>
                                    <td className="px-3 py-3">
                                        <div className="max-w-xs break-all font-medium text-content-primary">{delivery.event.event_type}</div>
                                        <div className="max-w-xs break-all text-xs text-content-secondary">
                                            {delivery.event.entity_type}
                                            {delivery.event.entity_id ? ` #${delivery.event.entity_id}` : ''}
                                        </div>
                                    </td>
                                    <td className="px-3 py-3">
                                        <div className="max-w-xs break-words font-medium text-content-primary">{delivery.target_name || t('settingsWebhooks.deletedTarget')}</div>
                                        <div className="max-w-xs break-all text-xs text-content-secondary">{delivery.target_url || t('settingsWebhooks.noUrlSnapshot')}</div>
                                    </td>
                                    <td className="px-3 py-3 text-content-primary">{delivery.attempt_count}</td>
                                    <td className="px-3 py-3 text-content-secondary">{formatDateTime(delivery.last_attempt_at)}</td>
                                    <td className="px-3 py-3">
                                        <div className="max-w-md break-words text-xs text-content-secondary [overflow-wrap:anywhere]">
                                            {delivery.last_http_status && (
                                                <span className="mr-2 rounded bg-surface-subtle px-1.5 py-0.5">
                                                    HTTP {delivery.last_http_status}
                                                </span>
                                            )}
                                            {delivery.last_error || delivery.last_response_body || '-'}
                                        </div>
                                    </td>
                                    <td className="px-3 py-3">
                                        <div className="flex justify-end">
                                            {delivery.status === 'delivered' ? (
                                                <span className="max-w-48 break-words text-right text-xs text-content-secondary">
                                                    {t('settingsWebhooks.retryAlreadyDelivered')}
                                                </span>
                                            ) : !delivery.target_id ? (
                                                <span className="max-w-48 break-words text-right text-xs text-content-secondary">
                                                    {t('settingsWebhooks.retryTargetUnavailable')}
                                                </span>
                                            ) : (
                                                <Button
                                                    type="button"
                                                    variant="outline"
                                                    size="sm"
                                                    onClick={() => retryMutation.mutate(delivery.id)}
                                                    disabled={retryMutation.isPending}
                                                    isLoading={retryMutation.isPending && retryMutation.variables === delivery.id}
                                                    aria-label={`${t('settingsWebhooks.retry')}: ${delivery.event.event_type}`}
                                                >
                                                    <RefreshCw className="h-3.5 w-3.5" aria-hidden="true" />
                                                </Button>
                                            )}
                                        </div>
                                    </td>
                                </tr>
                            ))}
                            {!deliveriesLoading && deliveries.length === 0 && (
                                <tr>
                                    <td className="px-3 py-8 text-center text-content-secondary" colSpan={7}>
                                        {t('settingsWebhooks.noDeliveries')}
                                    </td>
                                </tr>
                            )}
                        </tbody>
                    </table>
                </div>
                )}
            </div>
            {confirmationDialog}
        </div>
    );
};

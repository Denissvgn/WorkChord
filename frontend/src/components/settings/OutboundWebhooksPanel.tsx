import { useMemo, useState } from 'react';
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

export const OutboundWebhooksPanel = () => {
    const { t } = useTranslation();
    const queryClient = useQueryClient();
    const { hasAdminKey } = useAdminAccess();
    const toast = useToast();
    const { requestConfirmation, confirmationDialog } = useConfirmDialog();
    const [form, setForm] = useState<TargetFormState>(emptyForm);
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

    const statusBadge = (status: OutboundWebhookDeliveryStatus) => (
        <span className={`inline-flex rounded border px-2 py-0.5 text-xs font-medium ${statusClasses[status]}`}>
            {t(`settingsWebhooks.statuses.${status}`)}
        </span>
    );

    const invalidateWebhookQueries = () => {
        queryClient.invalidateQueries({ queryKey: ['outbound-webhook-targets'] });
        queryClient.invalidateQueries({ queryKey: ['outbound-webhook-deliveries'] });
    };

    const resetForm = () => {
        setEditingTargetId(null);
        setForm(emptyForm);
    };

    const createMutation = useMutation({
        mutationFn: outboundWebhookService.createTarget,
        onSuccess: () => {
            invalidateWebhookQueries();
            resetForm();
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

    const updateMutation = useMutation({
        mutationFn: ({ targetId, data }: { targetId: number; data: OutboundWebhookTargetUpdate }) => (
            outboundWebhookService.updateTarget(targetId, data)
        ),
        onSuccess: () => {
            invalidateWebhookQueries();
            resetForm();
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

    const toggleMutation = useMutation({
        mutationFn: ({ targetId, enabled }: { targetId: number; enabled: boolean }) => (
            outboundWebhookService.updateTarget(targetId, { enabled })
        ),
        onSuccess: invalidateWebhookQueries,
        onError: (err: unknown) => {
            toast.error(getAdminAccessErrorMessage(err, {
                missingOrInvalid: t('settings.adminAccessMissingOrInvalid'),
                backendNotConfigured: t('settings.adminAccessBackendNotConfigured'),
                fallback: t('settingsWebhooks.updateFailed'),
            }));
        },
    });

    const deleteMutation = useMutation({
        mutationFn: outboundWebhookService.deleteTarget,
        onSuccess: () => {
            invalidateWebhookQueries();
            resetForm();
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
    };

    const toggleEvent = (eventValue: string, checked: boolean) => {
        setForm(prev => ({
            ...prev,
            subscribedEvents: checked
                ? Array.from(new Set([...prev.subscribedEvents, eventValue]))
                : prev.subscribedEvents.filter(value => value !== eventValue),
        }));
    };

    const payloadFromForm = (): OutboundWebhookTargetCreate | OutboundWebhookTargetUpdate => {
        const name = form.name.trim();
        const url = form.url.trim();
        if (!name) {
            throw new Error(t('settingsWebhooks.nameRequired'));
        }
        if (!url) {
            throw new Error(t('settingsWebhooks.urlRequired'));
        }
        if (form.subscribedEvents.length === 0) {
            throw new Error(t('settingsWebhooks.eventRequired'));
        }

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

        if (editingTargetId) {
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
        let payload: OutboundWebhookTargetCreate | OutboundWebhookTargetUpdate;
        try {
            payload = payloadFromForm();
        } catch (err) {
            toast.error(err instanceof Error ? err.message : t('settingsWebhooks.formInvalid'));
            return;
        }

        if (editingTargetId) {
            updateMutation.mutate({ targetId: editingTargetId, data: payload });
        } else {
            createMutation.mutate(payload as OutboundWebhookTargetCreate);
        }
    };

    const handleEdit = (target: OutboundWebhookTarget) => {
        setEditingTargetId(target.id);
        setForm(targetToForm(target));
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
            {Boolean(deliveriesError) && <QueryErrorState error={deliveriesError} onRetry={() => void refetchDeliveries()} />}
            <form onSubmit={handleSubmit} className="card space-y-5">
                <div className="flex items-start justify-between gap-4">
                    <div className="flex items-center gap-3">
                        <div className="rounded-full bg-action p-2 text-content-emphasis">
                            <Webhook className="h-5 w-5" />
                        </div>
                        <div>
                            <h2 className="text-lg font-semibold text-content-primary">{t('settingsWebhooks.title')}</h2>
                            <p className="text-sm text-content-secondary">
                                {t('settingsWebhooks.description')}
                            </p>
                        </div>
                    </div>
                    <Button type="button" variant="outline" size="sm" onClick={resetForm}>
                        <Plus className="mr-1 h-4 w-4" />
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
                        />
                    </div>
                    <div className="lg:col-span-5">
                        <Input
                            label={t('settingsWebhooks.url')}
                            value={form.url}
                            onChange={event => updateField('url', event.target.value)}
                            placeholder={t('settingsWebhooks.urlPlaceholder')}
                        />
                    </div>
                    <div className="lg:col-span-2">
                        <Input
                            label={t('settingsWebhooks.secret')}
                            type="password"
                            value={form.secret}
                            onChange={event => updateField('secret', event.target.value)}
                            placeholder={editingTargetId ? t('settingsWebhooks.leaveUnchanged') : t('settingsWebhooks.optional')}
                            disabled={form.clearSecret}
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
                        <label className="mb-1 block text-sm font-medium text-content-primary">{t('settingsWebhooks.headersJson')}</label>
                        <textarea
                            value={form.headersJson}
                            onChange={event => updateField('headersJson', event.target.value)}
                            rows={3}
                            className="w-full rounded-md border border-border-strong px-3 py-2 font-mono text-sm shadow-sm focus:border-action focus:outline-none focus:ring-1 focus:ring-focus"
                            placeholder='{"X-Route": "workchord"}'
                        />
                    </div>
                    {editingTargetId && (
                        <div className="lg:col-span-12">
                            <Checkbox
                                label={t('settingsWebhooks.clearStoredSecret')}
                                checked={form.clearSecret}
                                onChange={checked => updateField('clearSecret', checked)}
                            />
                        </div>
                    )}
                </div>

                <div className="space-y-3">
                    <div>
                        <h3 className="text-sm font-semibold text-content-primary">{t('settingsWebhooks.subscribedEvents')}</h3>
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
                                        />
                                    ))}
                                </div>
                            </div>
                        ))}
                    </div>
                </div>

                <div className="flex justify-end gap-2">
                    {editingTargetId && (
                        <Button type="button" variant="ghost" size="sm" onClick={resetForm}>
                            <X className="mr-1 h-4 w-4" />
                            {t('settingsWebhooks.cancel')}
                        </Button>
                    )}
                    <Button type="submit" size="sm" isLoading={isSaving}>
                        <Save className="mr-1 h-4 w-4" />
                        {editingTargetId ? t('settingsWebhooks.saveTarget') : t('settingsWebhooks.createTarget')}
                    </Button>
                </div>
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
                                        <Checkbox
                                            checked={target.enabled}
                                            onChange={checked => toggleMutation.mutate({ targetId: target.id, enabled: checked })}
                                            disabled={toggleMutation.isPending}
                                        />
                                    </td>
                                    <td className="px-3 py-3">
                                        <div className="font-medium text-content-primary">{target.name}</div>
                                        <div className="mt-1 max-w-lg truncate text-xs text-content-secondary">{target.url}</div>
                                        {target.description && (
                                            <div className="mt-1 max-w-lg text-xs text-content-secondary">{target.description}</div>
                                        )}
                                    </td>
                                    <td className="px-3 py-3">
                                        <div className="flex max-w-md flex-wrap gap-1">
                                            {target.subscribed_events_json.map(eventName => (
                                                <span key={eventName} className="rounded bg-surface-subtle px-2 py-0.5 text-xs text-content-primary">
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
                                                isLoading={testMutation.isPending}
                                                aria-label={t('settingsWebhooks.test')}
                                            >
                                                <Send className="h-3.5 w-3.5" />
                                            </Button>
                                            <Button type="button" variant="outline" size="sm" onClick={() => handleEdit(target)} aria-label={t('actions.edit')}>
                                                <Edit2 className="h-3.5 w-3.5" />
                                            </Button>
                                            <Button
                                                type="button"
                                                variant="danger"
                                                size="sm"
                                                onClick={() => handleDelete(target)}
                                                isLoading={deleteMutation.isPending}
                                                aria-label={t('actions.delete')}
                                            >
                                                <Trash2 className="h-3.5 w-3.5" />
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
                            className="rounded-md border border-border-strong px-3 py-2 text-sm shadow-sm focus:border-action focus:outline-none focus:ring-1 focus:ring-focus"
                        >
                            <option value="">{t('settingsWebhooks.allTargets')}</option>
                            {targets.map(target => (
                                <option key={target.id} value={target.id}>{target.name}</option>
                            ))}
                        </select>
                        <select
                            value={deliveryStatus}
                            onChange={event => setDeliveryStatus(event.target.value as OutboundWebhookDeliveryStatus | '')}
                            className="rounded-md border border-border-strong px-3 py-2 text-sm shadow-sm focus:border-action focus:outline-none focus:ring-1 focus:ring-focus"
                        >
                            <option value="">{t('settingsWebhooks.allStatuses')}</option>
                            <option value="delivered">{t('settingsWebhooks.statuses.delivered')}</option>
                            <option value="failed">{t('settingsWebhooks.statuses.failed')}</option>
                            <option value="pending">{t('settingsWebhooks.statuses.pending')}</option>
                        </select>
                    </div>
                </div>
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
                                        <div className="font-medium text-content-primary">{delivery.event.event_type}</div>
                                        <div className="text-xs text-content-secondary">
                                            {delivery.event.entity_type}
                                            {delivery.event.entity_id ? ` #${delivery.event.entity_id}` : ''}
                                        </div>
                                    </td>
                                    <td className="px-3 py-3">
                                        <div className="font-medium text-content-primary">{delivery.target_name || t('settingsWebhooks.deletedTarget')}</div>
                                        <div className="max-w-xs truncate text-xs text-content-secondary">{delivery.target_url || t('settingsWebhooks.noUrlSnapshot')}</div>
                                    </td>
                                    <td className="px-3 py-3 text-content-primary">{delivery.attempt_count}</td>
                                    <td className="px-3 py-3 text-content-secondary">{formatDateTime(delivery.last_attempt_at)}</td>
                                    <td className="px-3 py-3">
                                        <div className="max-w-md text-xs text-content-secondary">
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
                                            <Button
                                                type="button"
                                                variant="outline"
                                                size="sm"
                                                onClick={() => retryMutation.mutate(delivery.id)}
                                                disabled={delivery.status === 'delivered' || !delivery.target_id}
                                                isLoading={retryMutation.isPending}
                                                aria-label={t('settingsWebhooks.retry')}
                                            >
                                                <RefreshCw className="h-3.5 w-3.5" />
                                            </Button>
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
            </div>
            {confirmationDialog}
        </div>
    );
};

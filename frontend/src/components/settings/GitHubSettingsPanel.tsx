import { useId, useMemo, useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { Edit2, Github, Loader2, Plus, Save, Trash2, X } from 'lucide-react';
import { Button } from '../common/Button';
import { Checkbox } from '../common/Checkbox';
import { Input } from '../common/Input';
import { useConfirmDialog } from '../common/useConfirmDialog';
import { QueryErrorState } from '../feedback/QueryState';
import { useToast } from '../feedback/toast';
import { githubService } from '../../services/githubService';
import { getApiErrorMessage } from '../../utils/apiError';
import type {
    GitHubAutomationEventType,
    GitHubAutomationTargetStatus,
    GitHubStatusAutomationRule,
    GitHubStatusAutomationRuleCreate,
} from '../../types/github';
import type { TaskStatus } from '../../types/task';
import { githubRuleDisplay } from '../../i18n/seedDisplay';

const eventOptions: Array<{ value: GitHubAutomationEventType; labelKey: string }> = [
    { value: 'github_pr_opened', labelKey: 'settingsGithubAutomation.events.github_pr_opened' },
    { value: 'github_pr_reopened', labelKey: 'settingsGithubAutomation.events.github_pr_reopened' },
    { value: 'github_pr_ready_for_review', labelKey: 'settingsGithubAutomation.events.github_pr_ready_for_review' },
    { value: 'github_pr_synchronize', labelKey: 'settingsGithubAutomation.events.github_pr_synchronize' },
    { value: 'github_pr_closed', labelKey: 'settingsGithubAutomation.events.github_pr_closed' },
    { value: 'github_pr_merged', labelKey: 'settingsGithubAutomation.events.github_pr_merged' },
];

const statusOptions: TaskStatus[] = ['planned', 'active', 'resolved', 'closed'];
const targetStatusOptions: GitHubAutomationTargetStatus[] = ['active', 'resolved', 'closed'];

const emptyForm = (reasonTemplate: string): GitHubStatusAutomationRuleCreate => ({
    name: '',
    description: '',
    enabled: false,
    github_event_type: 'github_pr_opened',
    from_status: 'planned',
    target_status: 'active',
    reason_template: reasonTemplate,
    sort_order: 100,
});

type FormErrors = Partial<Record<'name' | 'sort_order', string>>;

const formsMatch = (
    left: GitHubStatusAutomationRuleCreate,
    right: GitHubStatusAutomationRuleCreate,
) => JSON.stringify(left) === JSON.stringify(right);

export const GitHubSettingsPanel = () => {
    const { t } = useTranslation();
    const queryClient = useQueryClient();
    const toast = useToast();
    const initialForm = useMemo(
        () => emptyForm(t('settingsGithubAutomation.reasonTemplatePlaceholder')),
        [t],
    );
    const [form, setForm] = useState<GitHubStatusAutomationRuleCreate>(initialForm);
    const [baselineForm, setBaselineForm] = useState<GitHubStatusAutomationRuleCreate>(initialForm);
    const [formErrors, setFormErrors] = useState<FormErrors>({});
    const [editingRuleId, setEditingRuleId] = useState<number | null>(null);
    const { requestConfirmation, confirmationDialog } = useConfirmDialog();
    const eventSelectId = useId();
    const fromStatusSelectId = useId();
    const targetStatusSelectId = useId();
    const saveStatusId = useId();

    const eventLabel = (eventType: GitHubAutomationEventType) => {
        const option = eventOptions.find(candidate => candidate.value === eventType);
        return option ? t(option.labelKey) : eventType;
    };

    const statusLabel = (status: string | null | undefined) => (
        status ? t(`statuses.${status}`, { defaultValue: status }) : t('settingsGithubAutomation.any')
    );

    // feedback-policy: query loading,error,retry,empty - page states keep rule management explicit.
    const { data: rules = [], isLoading, error, refetch } = useQuery({
        queryKey: ['github-status-automation-rules'],
        queryFn: githubService.getStatusAutomationRules,
    });

    const hasUnsavedChanges = !formsMatch(form, baselineForm);

    const resetFormNow = () => {
        const nextForm = emptyForm(t('settingsGithubAutomation.reasonTemplatePlaceholder'));
        setEditingRuleId(null);
        setForm(nextForm);
        setBaselineForm(nextForm);
        setFormErrors({});
    };

    // feedback-policy: mutation pending,toast - freeze the draft snapshot and preserve it on failure.
    const createMutation = useMutation({
        mutationFn: githubService.createStatusAutomationRule,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['github-status-automation-rules'] });
            resetFormNow();
            toast.success(t('settingsGithubAutomation.createSuccess'));
        },
        onError: (err: unknown) => {
            toast.error(getApiErrorMessage(err, t('settingsGithubAutomation.createFailed')));
        },
    });

    // feedback-policy: mutation pending,toast - freeze the draft snapshot and preserve it on failure.
    const updateMutation = useMutation({
        mutationFn: ({ ruleId, data }: { ruleId: number; data: GitHubStatusAutomationRuleCreate }) => (
            githubService.updateStatusAutomationRule(ruleId, data)
        ),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['github-status-automation-rules'] });
            resetFormNow();
            toast.success(t('settingsGithubAutomation.saveSuccess'));
        },
        onError: (err: unknown) => {
            toast.error(getApiErrorMessage(err, t('settingsGithubAutomation.saveFailed')));
        },
    });

    // feedback-policy: mutation pending,toast - only the affected row reports progress; failures remain actionable.
    const toggleMutation = useMutation({
        mutationFn: ({ ruleId, enabled }: { ruleId: number; enabled: boolean }) => (
            githubService.updateStatusAutomationRule(ruleId, { enabled })
        ),
        onSuccess: (_result, { ruleId, enabled }) => {
            queryClient.invalidateQueries({ queryKey: ['github-status-automation-rules'] });
            if (editingRuleId === ruleId) {
                setForm(current => ({ ...current, enabled }));
                setBaselineForm(current => ({ ...current, enabled }));
            }
        },
        onError: (err: unknown) => {
            toast.error(getApiErrorMessage(err, t('settingsGithubAutomation.updateFailed')));
        },
    });

    // feedback-policy: mutation pending,toast - confirm first, mark only the affected row, and keep unrelated drafts.
    const deleteMutation = useMutation({
        mutationFn: githubService.deleteStatusAutomationRule,
        onSuccess: (_result, deletedRuleId) => {
            queryClient.invalidateQueries({ queryKey: ['github-status-automation-rules'] });
            if (editingRuleId === deletedRuleId) {
                resetFormNow();
            }
            toast.success(t('settingsGithubAutomation.deleteSuccess'));
        },
        onError: (err: unknown) => {
            toast.error(getApiErrorMessage(err, t('settingsGithubAutomation.deleteFailed')));
        },
    });

    const updateField = <K extends keyof GitHubStatusAutomationRuleCreate>(
        field: K,
        value: GitHubStatusAutomationRuleCreate[K],
    ) => {
        if (createMutation.isPending || updateMutation.isPending || rowMutationPending) return;
        setForm(prev => ({ ...prev, [field]: value }));
        if (field === 'name' || field === 'sort_order') {
            setFormErrors(prev => ({ ...prev, [field]: undefined }));
        }
    };

    const payloadFromForm = (): GitHubStatusAutomationRuleCreate => ({
        ...form,
        name: form.name.trim(),
        description: form.description?.trim() || null,
        from_status: form.from_status || null,
        reason_template: form.reason_template?.trim() || null,
        sort_order: Number(form.sort_order) || 0,
    });

    const handleSubmit = () => {
        if (createMutation.isPending || updateMutation.isPending || rowMutationPending) return;

        const payload = payloadFromForm();
        const nextErrors: FormErrors = {};
        if (!payload.name) {
            nextErrors.name = t('settingsGithubAutomation.nameRequired');
        } else if (payload.name.length > 255) {
            nextErrors.name = t('settingsGithubAutomation.nameTooLong');
        }
        if (!Number.isSafeInteger(payload.sort_order)) {
            nextErrors.sort_order = t('settingsGithubAutomation.orderMustBeInteger');
        }
        if (Object.keys(nextErrors).length > 0) {
            setFormErrors(nextErrors);
            toast.error(t('settingsGithubAutomation.validationTitle'));
            return;
        }

        setFormErrors({});
        if (editingRuleId !== null) {
            updateMutation.mutate({ ruleId: editingRuleId, data: payload });
        } else {
            createMutation.mutate(payload);
        }
    };

    const editRuleNow = (rule: GitHubStatusAutomationRule) => {
        const nextForm: GitHubStatusAutomationRuleCreate = {
            name: rule.name,
            description: rule.description || '',
            enabled: rule.enabled,
            github_event_type: rule.github_event_type,
            from_status: rule.from_status || null,
            target_status: rule.target_status,
            reason_template: rule.reason_template || '',
            sort_order: rule.sort_order,
        };
        setEditingRuleId(rule.id);
        setForm(nextForm);
        setBaselineForm(nextForm);
        setFormErrors({});
    };

    const requestDraftTransition = (onDiscard: () => void) => {
        if (createMutation.isPending || updateMutation.isPending || rowMutationPending) return;
        if (!hasUnsavedChanges) {
            onDiscard();
            return;
        }
        requestConfirmation({
            title: t('settingsGithubAutomation.discardDraftTitle'),
            description: t('settingsGithubAutomation.discardDraftDescription'),
            confirmLabel: t('actions.discard'),
            cancelLabel: t('actions.cancel'),
            closeLabel: t('actions.close'),
            tone: 'warning',
            onConfirm: onDiscard,
        });
    };

    const handleEdit = (rule: GitHubStatusAutomationRule) => {
        if (editingRuleId === rule.id) return;
        requestDraftTransition(() => editRuleNow(rule));
    };

    const handleDelete = (rule: GitHubStatusAutomationRule) => {
        requestConfirmation({
            title: t('actions.delete'),
            description: t(
                editingRuleId === rule.id && hasUnsavedChanges
                    ? 'settingsGithubAutomation.deleteEditingConfirm'
                    : 'settingsGithubAutomation.deleteConfirm',
            ),
            confirmLabel: t('actions.delete'),
            cancelLabel: t('actions.cancel'),
            closeLabel: t('actions.close'),
            onConfirm: () => deleteMutation.mutateAsync(rule.id),
        });
    };

    if (isLoading) {
        return (
            <div className="flex items-center justify-center py-12">
                <Loader2 className="w-8 h-8 animate-spin text-action" />
                <span className="ml-3 text-content-secondary">{t('settingsGithubAutomation.loading')}</span>
            </div>
        );
    }

    if (error) {
        return <QueryErrorState error={error} fallback={t('settingsGithubAutomation.loadFailed')} onRetry={() => void refetch()} />;
    }

    const isSaving = createMutation.isPending || updateMutation.isPending;
    const rowMutationPending = toggleMutation.isPending || deleteMutation.isPending;
    const formLocked = isSaving || rowMutationPending;

    return (
        <div className="max-w-6xl space-y-5">
            <div className="card space-y-4">
                <div className="flex flex-col items-stretch gap-4 sm:flex-row sm:items-start sm:justify-between">
                    <div className="flex min-w-0 items-center gap-3">
                        <div className="shrink-0 rounded-full bg-content-primary p-2 text-content-emphasis">
                            <Github aria-hidden="true" className="h-5 w-5" />
                        </div>
                        <div className="min-w-0">
                            <h2 className="break-words text-lg font-semibold text-content-primary">{t('settingsGithubAutomation.title')}</h2>
                            <p className="break-words text-sm text-content-secondary">
                                {t('settingsGithubAutomation.description')}
                            </p>
                        </div>
                    </div>
                    <Button
                        variant="outline"
                        size="sm"
                        className="w-full shrink-0 sm:w-auto"
                        onClick={() => requestDraftTransition(resetFormNow)}
                        disabled={formLocked}
                        aria-describedby={formLocked ? saveStatusId : undefined}
                        title={formLocked ? t('settingsGithubAutomation.rowUpdateInProgress') : undefined}
                    >
                        <Plus aria-hidden="true" className="mr-1 h-4 w-4" />
                        {t('settingsGithubAutomation.newRule')}
                    </Button>
                </div>

                <fieldset
                    className="contents"
                    disabled={formLocked}
                    aria-busy={formLocked}
                    aria-describedby={formLocked ? saveStatusId : undefined}
                >
                    <div className="grid grid-cols-1 gap-3 lg:grid-cols-12">
                        <div className="lg:col-span-3">
                            <Input
                                label={t('settingsGithubAutomation.name')}
                                value={form.name}
                                onChange={event => updateField('name', event.target.value)}
                                placeholder={t('settingsGithubAutomation.namePlaceholder')}
                                maxLength={255}
                                required
                                error={formErrors.name}
                            />
                        </div>
                        <div className="lg:col-span-2">
                            <label htmlFor={eventSelectId} className="mb-1 block text-sm font-medium text-content-primary">{t('settingsGithubAutomation.event')}</label>
                            <select
                                id={eventSelectId}
                                value={form.github_event_type}
                                onChange={event => updateField('github_event_type', event.target.value as GitHubAutomationEventType)}
                                className="w-full rounded-md border border-border-strong px-3 py-2 text-sm shadow-sm focus:border-action focus:outline-none focus:ring-1 focus:ring-focus"
                            >
                                {eventOptions.map(option => (
                                    <option key={option.value} value={option.value}>{t(option.labelKey)}</option>
                                ))}
                            </select>
                        </div>
                        <div className="lg:col-span-2">
                            <label htmlFor={fromStatusSelectId} className="mb-1 block text-sm font-medium text-content-primary">{t('settingsGithubAutomation.fromStatus')}</label>
                            <select
                                id={fromStatusSelectId}
                                value={form.from_status || ''}
                                onChange={event => updateField('from_status', (event.target.value || null) as TaskStatus | null)}
                                className="w-full rounded-md border border-border-strong px-3 py-2 text-sm shadow-sm focus:border-action focus:outline-none focus:ring-1 focus:ring-focus"
                            >
                                <option value="">{t('settingsGithubAutomation.any')}</option>
                                {statusOptions.map(status => (
                                    <option key={status} value={status}>{statusLabel(status)}</option>
                                ))}
                            </select>
                        </div>
                        <div className="lg:col-span-2">
                            <label htmlFor={targetStatusSelectId} className="mb-1 block text-sm font-medium text-content-primary">{t('settingsGithubAutomation.targetStatus')}</label>
                            <select
                                id={targetStatusSelectId}
                                value={form.target_status}
                                onChange={event => updateField('target_status', event.target.value as GitHubAutomationTargetStatus)}
                                className="w-full rounded-md border border-border-strong px-3 py-2 text-sm shadow-sm focus:border-action focus:outline-none focus:ring-1 focus:ring-focus"
                            >
                                {targetStatusOptions.map(status => (
                                    <option key={status} value={status}>{statusLabel(status)}</option>
                                ))}
                            </select>
                        </div>
                        <div className="lg:col-span-1">
                            <Input
                                label={t('settingsGithubAutomation.order')}
                                type="number"
                                step={1}
                                value={form.sort_order}
                                onChange={event => updateField('sort_order', Number(event.target.value))}
                                error={formErrors.sort_order}
                            />
                        </div>
                        <div className="flex items-end lg:col-span-2">
                            <Checkbox
                                label={t('settingsGithubAutomation.enabled')}
                                checked={form.enabled}
                                onChange={checked => updateField('enabled', checked)}
                                className="pb-2"
                            />
                        </div>
                        <div className="min-w-0 lg:col-span-6">
                            <Input
                                label={t('settingsGithubAutomation.descriptionField')}
                                value={form.description || ''}
                                onChange={event => updateField('description', event.target.value)}
                                placeholder={t('settingsGithubAutomation.descriptionPlaceholder')}
                            />
                        </div>
                        <div className="min-w-0 lg:col-span-6">
                            <Input
                                label={t('settingsGithubAutomation.reasonTemplate')}
                                value={form.reason_template || ''}
                                onChange={event => updateField('reason_template', event.target.value)}
                                placeholder={t('settingsGithubAutomation.reasonTemplatePlaceholder')}
                            />
                        </div>
                    </div>

                    <div className="flex flex-col-reverse items-stretch justify-end gap-2 sm:flex-row sm:items-center">
                        {editingRuleId !== null && (
                            <Button
                                variant="ghost"
                                size="sm"
                                className="w-full sm:w-auto"
                                onClick={() => requestDraftTransition(resetFormNow)}
                            >
                                <X aria-hidden="true" className="mr-1 h-4 w-4" />
                                {t('settingsGithubAutomation.cancel')}
                            </Button>
                        )}
                        <Button className="w-full sm:w-auto" size="sm" onClick={handleSubmit} isLoading={isSaving}>
                            <Save aria-hidden="true" className="mr-1 h-4 w-4" />
                            {editingRuleId !== null ? t('settingsGithubAutomation.saveRule') : t('settingsGithubAutomation.createRule')}
                        </Button>
                    </div>
                </fieldset>

                <p id={saveStatusId} className="min-h-4 text-right text-xs text-content-secondary" aria-live="polite">
                    {isSaving
                        ? t('common.saving')
                        : rowMutationPending
                            ? t('settingsGithubAutomation.rowUpdateInProgress')
                            : ''}
                </p>
            </div>

            <div className="overflow-hidden rounded-lg border border-border bg-surface-card">
                <div className="overflow-x-auto">
                    <table className="min-w-[720px] divide-y divide-border text-sm">
                        <thead className="bg-surface-muted text-left text-xs font-semibold uppercase text-content-secondary">
                            <tr>
                                <th className="px-3 py-2">{t('settingsGithubAutomation.enabled')}</th>
                                <th className="px-3 py-2">{t('settingsGithubAutomation.rule')}</th>
                                <th className="px-3 py-2">{t('settingsGithubAutomation.event')}</th>
                                <th className="px-3 py-2">{t('settingsGithubAutomation.transition')}</th>
                                <th className="px-3 py-2">{t('settingsGithubAutomation.order')}</th>
                                <th className="px-3 py-2 text-right">{t('settingsGithubAutomation.actions')}</th>
                            </tr>
                        </thead>
                        <tbody className="divide-y divide-border-subtle">
                            {rules.map(rule => {
                                const display = githubRuleDisplay(rule);
                                const isToggling = toggleMutation.isPending
                                    && toggleMutation.variables?.ruleId === rule.id;
                                const isDeleting = deleteMutation.isPending
                                    && deleteMutation.variables === rule.id;
                                const isRowBusy = isToggling || isDeleting;
                                const rowDisabledReason = isSaving
                                    ? t('common.saving')
                                    : rowMutationPending
                                        ? t('settingsGithubAutomation.rowUpdateInProgress')
                                        : undefined;

                                return (
                                    <tr key={rule.id} className="align-top" aria-busy={isRowBusy}>
                                        <td className="px-3 py-3">
                                            <div className="flex items-center gap-2">
                                                <Checkbox
                                                    checked={rule.enabled}
                                                    onChange={checked => toggleMutation.mutate({ ruleId: rule.id, enabled: checked })}
                                                    disabled={isSaving || rowMutationPending}
                                                    aria-label={t(
                                                        rule.enabled
                                                            ? 'settingsGithubAutomation.disableRule'
                                                            : 'settingsGithubAutomation.enableRule',
                                                        { name: display.name },
                                                    )}
                                                    title={rowDisabledReason}
                                                />
                                                {isToggling && (
                                                    <span className="inline-flex items-center" role="status">
                                                        <Loader2 aria-hidden="true" className="h-4 w-4 animate-spin text-action" />
                                                        <span className="sr-only">{t('settingsGithubAutomation.updatingRule', { name: display.name })}</span>
                                                    </span>
                                                )}
                                            </div>
                                        </td>
                                        <td className="min-w-0 px-3 py-3">
                                            <div className="max-w-xs break-words font-medium text-content-primary">{display.name}</div>
                                            {display.description && (
                                                <div className="mt-1 max-w-xs break-words text-xs text-content-secondary">{display.description}</div>
                                            )}
                                        </td>
                                        <td className="px-3 py-3 text-content-primary">{eventLabel(rule.github_event_type)}</td>
                                        <td className="px-3 py-3">
                                            <span className="inline-block max-w-xs break-words rounded bg-surface-subtle px-2 py-1 text-xs text-content-primary">
                                                {statusLabel(rule.from_status)} {t('settingsGithubAutomation.transitionTo')} {statusLabel(rule.target_status)}
                                            </span>
                                        </td>
                                        <td className="px-3 py-3 text-content-secondary">{rule.sort_order}</td>
                                        <td className="px-3 py-3">
                                            <div className="flex justify-end gap-2">
                                                <Button
                                                    variant="outline"
                                                    size="sm"
                                                    onClick={() => handleEdit(rule)}
                                                    disabled={isSaving || rowMutationPending}
                                                    aria-label={t('settingsGithubAutomation.editRule', { name: display.name })}
                                                    title={rowDisabledReason}
                                                >
                                                    <Edit2 aria-hidden="true" className="h-3.5 w-3.5" />
                                                </Button>
                                                <Button
                                                    variant="danger"
                                                    size="sm"
                                                    onClick={() => handleDelete(rule)}
                                                    isLoading={isDeleting}
                                                    disabled={isSaving || rowMutationPending}
                                                    aria-busy={isDeleting}
                                                    aria-label={t('settingsGithubAutomation.deleteRule', { name: display.name })}
                                                    title={rowDisabledReason}
                                                >
                                                    <Trash2 aria-hidden="true" className="h-3.5 w-3.5" />
                                                </Button>
                                            </div>
                                        </td>
                                    </tr>
                                );
                            })}
                            {rules.length === 0 && (
                                <tr>
                                    <td className="px-3 py-8 text-center text-content-secondary" colSpan={6}>
                                        {t('settingsGithubAutomation.empty')}
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

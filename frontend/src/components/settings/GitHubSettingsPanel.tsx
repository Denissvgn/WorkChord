import { useState } from 'react';
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

export const GitHubSettingsPanel = () => {
    const { t } = useTranslation();
    const queryClient = useQueryClient();
    const toast = useToast();
    const [form, setForm] = useState<GitHubStatusAutomationRuleCreate>(() => (
        emptyForm(t('settingsGithubAutomation.reasonTemplatePlaceholder'))
    ));
    const [editingRuleId, setEditingRuleId] = useState<number | null>(null);
    const { requestConfirmation, confirmationDialog } = useConfirmDialog();

    const eventLabel = (eventType: GitHubAutomationEventType) => {
        const option = eventOptions.find(candidate => candidate.value === eventType);
        return option ? t(option.labelKey) : eventType;
    };

    const statusLabel = (status: string | null | undefined) => (
        status ? t(`statuses.${status}`, { defaultValue: status }) : t('settingsGithubAutomation.any')
    );

    const { data: rules = [], isLoading, error, refetch } = useQuery({
        queryKey: ['github-status-automation-rules'],
        queryFn: githubService.getStatusAutomationRules,
    });

    const resetForm = () => {
        setEditingRuleId(null);
        setForm(emptyForm(t('settingsGithubAutomation.reasonTemplatePlaceholder')));
    };

    const createMutation = useMutation({
        mutationFn: githubService.createStatusAutomationRule,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['github-status-automation-rules'] });
            resetForm();
            toast.success(t('settingsGithubAutomation.createSuccess'));
        },
        onError: (err: unknown) => {
            toast.error(getApiErrorMessage(err, t('settingsGithubAutomation.createFailed')));
        },
    });

    const updateMutation = useMutation({
        mutationFn: ({ ruleId, data }: { ruleId: number; data: GitHubStatusAutomationRuleCreate }) => (
            githubService.updateStatusAutomationRule(ruleId, data)
        ),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['github-status-automation-rules'] });
            resetForm();
            toast.success(t('settingsGithubAutomation.saveSuccess'));
        },
        onError: (err: unknown) => {
            toast.error(getApiErrorMessage(err, t('settingsGithubAutomation.saveFailed')));
        },
    });

    const toggleMutation = useMutation({
        mutationFn: ({ ruleId, enabled }: { ruleId: number; enabled: boolean }) => (
            githubService.updateStatusAutomationRule(ruleId, { enabled })
        ),
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['github-status-automation-rules'] });
        },
        onError: (err: unknown) => {
            toast.error(getApiErrorMessage(err, t('settingsGithubAutomation.updateFailed')));
        },
    });

    const deleteMutation = useMutation({
        mutationFn: githubService.deleteStatusAutomationRule,
        onSuccess: () => {
            queryClient.invalidateQueries({ queryKey: ['github-status-automation-rules'] });
            resetForm();
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
        setForm(prev => ({ ...prev, [field]: value }));
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
        const payload = payloadFromForm();
        if (!payload.name) {
            toast.error(t('settingsGithubAutomation.nameRequired'));
            return;
        }

        if (editingRuleId) {
            updateMutation.mutate({ ruleId: editingRuleId, data: payload });
        } else {
            createMutation.mutate(payload);
        }
    };

    const handleEdit = (rule: GitHubStatusAutomationRule) => {
        setEditingRuleId(rule.id);
        setForm({
            name: rule.name,
            description: rule.description || '',
            enabled: rule.enabled,
            github_event_type: rule.github_event_type,
            from_status: rule.from_status || null,
            target_status: rule.target_status,
            reason_template: rule.reason_template || '',
            sort_order: rule.sort_order,
        });
    };

    const handleDelete = (rule: GitHubStatusAutomationRule) => {
        requestConfirmation({
            title: t('actions.delete'),
            description: t('settingsGithubAutomation.deleteConfirm'),
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

    return (
        <div className="max-w-6xl space-y-5">
            <div className="card space-y-4">
                <div className="flex items-start justify-between gap-4">
                    <div className="flex items-center gap-3">
                        <div className="rounded-full bg-content-primary p-2 text-content-emphasis">
                            <Github className="h-5 w-5" />
                        </div>
                        <div>
                            <h2 className="text-lg font-semibold text-content-primary">{t('settingsGithubAutomation.title')}</h2>
                            <p className="text-sm text-content-secondary">
                                {t('settingsGithubAutomation.description')}
                            </p>
                        </div>
                    </div>
                    <Button variant="outline" size="sm" onClick={resetForm}>
                        <Plus className="mr-1 h-4 w-4" />
                        {t('settingsGithubAutomation.newRule')}
                    </Button>
                </div>

                <div className="grid grid-cols-1 gap-3 lg:grid-cols-12">
                    <div className="lg:col-span-3">
                        <Input
                            label={t('settingsGithubAutomation.name')}
                            value={form.name}
                            onChange={event => updateField('name', event.target.value)}
                            placeholder={t('settingsGithubAutomation.namePlaceholder')}
                        />
                    </div>
                    <div className="lg:col-span-2">
                        <label className="mb-1 block text-sm font-medium text-content-primary">{t('settingsGithubAutomation.event')}</label>
                        <select
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
                        <label className="mb-1 block text-sm font-medium text-content-primary">{t('settingsGithubAutomation.fromStatus')}</label>
                        <select
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
                        <label className="mb-1 block text-sm font-medium text-content-primary">{t('settingsGithubAutomation.targetStatus')}</label>
                        <select
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
                            value={form.sort_order}
                            onChange={event => updateField('sort_order', Number(event.target.value))}
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
                    <div className="lg:col-span-6">
                        <Input
                            label={t('settingsGithubAutomation.descriptionField')}
                            value={form.description || ''}
                            onChange={event => updateField('description', event.target.value)}
                            placeholder={t('settingsGithubAutomation.descriptionPlaceholder')}
                        />
                    </div>
                    <div className="lg:col-span-6">
                        <Input
                            label={t('settingsGithubAutomation.reasonTemplate')}
                            value={form.reason_template || ''}
                            onChange={event => updateField('reason_template', event.target.value)}
                            placeholder={t('settingsGithubAutomation.reasonTemplatePlaceholder')}
                        />
                    </div>
                </div>

                <div className="flex items-center justify-end gap-2">
                    {editingRuleId && (
                        <Button variant="ghost" size="sm" onClick={resetForm}>
                            <X className="mr-1 h-4 w-4" />
                            {t('settingsGithubAutomation.cancel')}
                        </Button>
                    )}
                    <Button size="sm" onClick={handleSubmit} isLoading={isSaving}>
                        <Save className="mr-1 h-4 w-4" />
                        {editingRuleId ? t('settingsGithubAutomation.saveRule') : t('settingsGithubAutomation.createRule')}
                    </Button>
                </div>
            </div>

            <div className="overflow-hidden rounded-lg border border-border bg-surface-card">
                <div className="overflow-x-auto">
                    <table className="min-w-full divide-y divide-border text-sm">
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
                            {rules.map(rule => (
                                <tr key={rule.id} className="align-top">
                                    <td className="px-3 py-3">
                                        <Checkbox
                                            checked={rule.enabled}
                                            onChange={checked => toggleMutation.mutate({ ruleId: rule.id, enabled: checked })}
                                            disabled={toggleMutation.isPending}
                                        />
                                    </td>
                                    <td className="px-3 py-3">
                                        <div className="font-medium text-content-primary">{githubRuleDisplay(rule).name}</div>
                                        {githubRuleDisplay(rule).description && (
                                            <div className="mt-1 max-w-md text-xs text-content-secondary">{githubRuleDisplay(rule).description}</div>
                                        )}
                                    </td>
                                    <td className="px-3 py-3 text-content-primary">{eventLabel(rule.github_event_type)}</td>
                                    <td className="px-3 py-3">
                                        <span className="rounded bg-surface-subtle px-2 py-1 text-xs text-content-primary">
                                            {statusLabel(rule.from_status)} {t('settingsGithubAutomation.transitionTo')} {statusLabel(rule.target_status)}
                                        </span>
                                    </td>
                                    <td className="px-3 py-3 text-content-secondary">{rule.sort_order}</td>
                                    <td className="px-3 py-3">
                                        <div className="flex justify-end gap-2">
                                            <Button variant="outline" size="sm" onClick={() => handleEdit(rule)}>
                                                <span className="sr-only">{t('actions.edit')}</span>
                                                <Edit2 className="h-3.5 w-3.5" />
                                            </Button>
                                            <Button
                                                variant="danger"
                                                size="sm"
                                                onClick={() => handleDelete(rule)}
                                                isLoading={deleteMutation.isPending}
                                                aria-label={t('actions.delete')}
                                            >
                                                <Trash2 className="h-3.5 w-3.5" />
                                            </Button>
                                        </div>
                                    </td>
                                </tr>
                            ))}
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

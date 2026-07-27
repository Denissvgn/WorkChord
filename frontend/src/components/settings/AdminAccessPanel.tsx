import { useState } from 'react';
import { useQueryClient } from '@tanstack/react-query';
import { CheckCircle, KeyRound, ShieldCheck, Trash2 } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { Button } from '../common/Button';
import { Input } from '../common/Input';
import { clearAdminApiKey, setAdminApiKey } from '../../utils/adminAccess';
import { useAdminAccess } from '../../hooks/useAdminAccess';

const protectedQueryKeys = [
    ['system-settings'],
    ['scheduling-rules'],
    ['email-settings'],
    ['outbound-webhook-targets'],
    ['outbound-webhook-deliveries'],
    ['agent-capabilities'],
    ['agent-actor-roster'],
    ['agent-model-catalog'],
    ['agent-model-bindings'],
    ['agent-profile-skill-catalog'],
    ['routing-assessment'],
    ['routing-preview'],
    ['agent-assignments'],
    ['agent-pipeline'],
    ['task-timeline'],
    ['agent-run-detail'],
] as const;

export const AdminAccessPanel = () => {
    const { t } = useTranslation();
    const queryClient = useQueryClient();
    const { hasAdminKey } = useAdminAccess();
    const [draftKey, setDraftKey] = useState('');
    const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);

    const refreshProtectedQueries = () => {
        protectedQueryKeys.forEach(queryKey => {
            void queryClient.invalidateQueries({ queryKey: [...queryKey] });
        });
    };

    const removeProtectedQueries = () => {
        protectedQueryKeys.forEach(queryKey => {
            queryClient.removeQueries({ queryKey: [...queryKey] });
        });
    };

    const saveKey = () => {
        const nextKey = draftKey.trim();
        if (!nextKey) {
            setMessage({ type: 'error', text: t('settings.adminAccessEnterKey') });
            return;
        }

        setAdminApiKey(nextKey);
        removeProtectedQueries();
        setDraftKey('');
        setMessage({ type: 'success', text: t('settings.adminAccessSaved') });
        refreshProtectedQueries();
    };

    const clearKey = () => {
        clearAdminApiKey();
        removeProtectedQueries();
        setDraftKey('');
        setMessage({ type: 'success', text: t('settings.adminAccessCleared') });
    };

    return (
        <section className="card max-w-3xl space-y-4">
            <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
                <div>
                    <h2 className="flex items-center gap-2 text-lg font-semibold text-content-primary">
                        <ShieldCheck className="h-5 w-5 text-action" />
                        {t('settings.adminAccessTitle')}
                    </h2>
                    <p className="mt-1 text-sm text-content-secondary">{t('settings.adminAccessDescription')}</p>
                </div>
                <div
                    className={`inline-flex w-fit items-center gap-2 rounded-full border px-3 py-1 text-xs font-medium ${
                        hasAdminKey
                            ? 'border-feedback-success-border bg-feedback-success-muted text-feedback-success-foreground'
                            : 'border-feedback-warning-border bg-feedback-warning-muted text-feedback-warning-foreground'
                    }`}
                >
                    <CheckCircle className="h-3.5 w-3.5" />
                    {hasAdminKey ? t('settings.adminAccessConfigured') : t('settings.adminAccessNotConfigured')}
                </div>
            </div>

            {message && (
                <div
                    className={`flex items-center gap-2 rounded-md border px-3 py-2 text-sm ${
                        message.type === 'success'
                            ? 'border-feedback-success-border bg-feedback-success-muted text-feedback-success-foreground'
                            : 'border-feedback-danger-border bg-feedback-danger-muted text-feedback-danger-foreground'
                    }`}
                >
                    {message.text}
                </div>
            )}

            <div className="flex flex-col gap-3 sm:flex-row">
                <Input
                    label={t('settings.adminAccessField')}
                    type="password"
                    autoComplete="off"
                    spellCheck={false}
                    value={draftKey}
                    onChange={(event) => setDraftKey(event.target.value)}
                    placeholder={t('settings.adminAccessPlaceholder')}
                />
                <div className="flex shrink-0 items-end gap-2">
                    <Button type="button" onClick={saveKey} className="inline-flex items-center gap-2">
                        <KeyRound className="h-4 w-4" />
                        {t('settings.adminAccessSave')}
                    </Button>
                    <Button
                        type="button"
                        variant="outline"
                        onClick={clearKey}
                        disabled={!hasAdminKey && !draftKey}
                        className="inline-flex items-center gap-2"
                    >
                        <Trash2 className="h-4 w-4" />
                        {t('settings.adminAccessClear')}
                    </Button>
                </div>
            </div>
        </section>
    );
};

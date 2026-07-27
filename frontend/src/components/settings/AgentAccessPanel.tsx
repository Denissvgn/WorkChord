import { useState } from 'react';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { AlertTriangle, CheckCircle2, KeyRound, ShieldCheck, Trash2 } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { useAgentAccess } from '../../hooks/useAgentAccess';
import { agentService } from '../../services/agentService';
import {
    clearAgentApiKey,
    setAgentApiKey,
} from '../../utils/agentAccess';
import { getApiErrorMessage } from '../../utils/apiError';
import { protectedQueryRetry } from '../../utils/protectedQueries';
import { Button } from '../common/Button';
import { Input } from '../common/Input';

const AGENT_QUERY_KEYS = [
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

export const AgentAccessPanel = () => {
    const { t } = useTranslation();
    const queryClient = useQueryClient();
    const { hasAgentKey } = useAgentAccess();
    const [draftKey, setDraftKey] = useState('');
    const [message, setMessage] = useState<string | null>(null);

    // feedback-policy: query loading,error,retry,empty
    const capabilitiesQuery = useQuery({
        queryKey: ['agent-capabilities'],
        queryFn: agentService.getCapabilities,
        enabled: hasAgentKey,
        retry: protectedQueryRetry,
    });

    const removeProtectedQueries = () => {
        AGENT_QUERY_KEYS.forEach(queryKey => {
            queryClient.removeQueries({ queryKey: [...queryKey] });
        });
    };

    const refreshProtectedQueries = () => {
        AGENT_QUERY_KEYS.forEach(queryKey => {
            void queryClient.invalidateQueries({ queryKey: [...queryKey] });
        });
    };

    const saveKey = () => {
        const nextKey = draftKey.trim();
        if (!nextKey) {
            setMessage(t('agentAccess.enterKey'));
            return;
        }
        setAgentApiKey(nextKey);
        removeProtectedQueries();
        refreshProtectedQueries();
        setDraftKey('');
        setMessage(null);
    };

    const clearKey = () => {
        clearAgentApiKey();
        removeProtectedQueries();
        setDraftKey('');
        setMessage(null);
    };

    const accessConfirmed = hasAgentKey
        && capabilitiesQuery.isSuccess
        && !capabilitiesQuery.isError
        && Boolean(capabilitiesQuery.data);
    const actor = accessConfirmed ? capabilitiesQuery.data?.actor : undefined;
    const isAdmin = accessConfirmed
        && (capabilitiesQuery.data?.scopes.includes('admin') ?? false);
    const accessState = !hasAgentKey
        ? t('agentAccess.notConfigured')
        : capabilitiesQuery.isPending
            ? t('agentAccess.checking')
            : capabilitiesQuery.isError
                ? t('agentAccess.invalid')
                : isAdmin
                    ? t('agentAccess.adminAccess')
                    : t('agentAccess.readerAccess');

    return (
        <section className="card max-w-4xl space-y-4" aria-labelledby="agent-access-heading">
            <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
                <div>
                    <h2 id="agent-access-heading" className="flex items-center gap-2 text-lg font-semibold text-content-primary">
                        <ShieldCheck aria-hidden="true" className="h-5 w-5 text-action" />
                        {t('agentAccess.title')}
                    </h2>
                    <p className="mt-1 text-sm text-content-secondary">{t('agentAccess.description')}</p>
                </div>
                <div
                    className={`inline-flex w-fit items-center gap-2 rounded-full border px-3 py-1 text-xs font-medium ${
                        accessConfirmed
                            ? 'border-feedback-success-border bg-feedback-success-muted text-feedback-success-foreground'
                            : capabilitiesQuery.isError
                                ? 'border-feedback-danger-border bg-feedback-danger-muted text-feedback-danger-foreground'
                                : 'border-feedback-warning-border bg-feedback-warning-muted text-feedback-warning-foreground'
                    }`}
                    role="status"
                >
                    {accessConfirmed ? (
                        <CheckCircle2 aria-hidden="true" className="h-3.5 w-3.5" />
                    ) : capabilitiesQuery.isError ? (
                        <AlertTriangle aria-hidden="true" className="h-3.5 w-3.5" />
                    ) : (
                        <KeyRound aria-hidden="true" className="h-3.5 w-3.5" />
                    )}
                    {accessState}
                </div>
            </div>

            {actor && (
                <div className="rounded-md border border-border bg-surface-muted px-3 py-2 text-sm text-content-secondary">
                    <span className="font-medium text-content-primary">{actor.display_name}</span>
                    {' · '}
                    {t('agentAccess.actorSummary', { role: actor.role, name: actor.name })}
                </div>
            )}

            {(message || capabilitiesQuery.isError) && (
                <div className="rounded-md border border-feedback-danger-border bg-feedback-danger-muted px-3 py-2 text-sm text-feedback-danger-foreground" role="alert">
                    {message ?? getApiErrorMessage(capabilitiesQuery.error, t('agentAccess.invalidDescription'))}
                </div>
            )}

            <div className="flex flex-col gap-3 sm:flex-row">
                <Input
                    label={t('agentAccess.field')}
                    type="password"
                    autoComplete="off"
                    spellCheck={false}
                    value={draftKey}
                    onChange={event => setDraftKey(event.target.value)}
                    placeholder={t('agentAccess.placeholder')}
                />
                <div className="flex shrink-0 items-end gap-2">
                    <Button type="button" onClick={saveKey} className="inline-flex items-center gap-2">
                        <KeyRound aria-hidden="true" className="h-4 w-4" />
                        {t('agentAccess.save')}
                    </Button>
                    <Button
                        type="button"
                        variant="outline"
                        onClick={clearKey}
                        disabled={!hasAgentKey && !draftKey}
                        className="inline-flex items-center gap-2"
                    >
                        <Trash2 aria-hidden="true" className="h-4 w-4" />
                        {t('agentAccess.clear')}
                    </Button>
                </div>
            </div>
            <p className="text-xs text-content-tertiary">{t('agentAccess.sessionOnly')}</p>
        </section>
    );
};

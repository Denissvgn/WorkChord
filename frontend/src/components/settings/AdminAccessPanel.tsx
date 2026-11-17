import { useState } from 'react';
import { useQueryClient } from '@tanstack/react-query';
import { KeyRound, ShieldCheck, Trash2 } from 'lucide-react';
import { useTranslation } from 'react-i18next';
import { Button } from '../common/Button';
import { Input } from '../common/Input';
import { clearAdminApiKey, setAdminApiKey } from '../../utils/adminAccess';
import { useAdminAccess } from '../../hooks/useAdminAccess';
import { verifyAdminApiKey } from '../../services/adminAccessService';
import { useIdentity } from '../../features/identity/identityContext';
import { OperatorIdentityNotice } from '../../features/identity/OperatorIdentityNotice';
import { getApiErrorStatus } from '../../utils/apiError';
import { protectedQueryKeys } from './protectedQueryKeys';

export const AdminAccessPanel = ({
    headingLevel = 2,
    saveVariant = 'primary',
}: {
    headingLevel?: 2 | 3;
    /** Secondary when the page around the panel already leads with a primary action. */
    saveVariant?: 'primary' | 'secondary';
}) => {
    const { t } = useTranslation();
    const queryClient = useQueryClient();
    const { hasAdminKey, actingAsOperator } = useAdminAccess();
    const identity = useIdentity()?.identity;
    const signedInPerson = identity?.principal?.kind === 'human';
    const [draftKey, setDraftKey] = useState('');
    const [message, setMessage] = useState<{ type: 'success' | 'error'; text: string } | null>(null);
    const [verifying, setVerifying] = useState(false);
    const Heading = headingLevel === 2 ? 'h2' : 'h3';

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

    const saveKey = async () => {
        const nextKey = draftKey.trim();
        if (!nextKey) {
            setMessage({ type: 'error', text: t('settings.adminAccessEnterKey') });
            return;
        }

        setVerifying(true);
        setMessage(null);
        try {
            // One protected read tells whether the server accepts this key.
            await verifyAdminApiKey(nextKey);
            setAdminApiKey(nextKey);
            removeProtectedQueries();
            setDraftKey('');
            setMessage({ type: 'success', text: t('settings.adminAccessAccepted') });
            refreshProtectedQueries();
        } catch (cause) {
            const status = getApiErrorStatus(cause);
            if (status === 401 || status === 403 || status === 503) {
                setMessage({
                    type: 'error',
                    text: t(status === 503 ? 'settings.adminAccessBackendNotConfigured' : 'settings.adminAccessRejected'),
                });
            } else {
                setMessage({ type: 'error', text: t('identity.keyNotChecked') });
            }
        } finally {
            setVerifying(false);
        }
    };

    const clearKey = () => {
        clearAdminApiKey();
        removeProtectedQueries();
        setDraftKey('');
        setMessage({ type: 'success', text: t('settings.adminAccessCleared') });
    };

    if (signedInPerson) return <section className="card max-w-3xl space-y-4">
        <Heading className="font-semibold text-content-primary">{t('identity.editing', {
            state: t(hasAdminKey ? 'identity.editingUnlocked' : 'identity.editingLocked'),
        })}</Heading>
        <p className="text-sm text-content-secondary">{t('identity.editingFollowsRole')}</p>
        {identity.workspace_role && <p className="text-sm">{t('identity.workspaceRole', { role: identity.workspace_role })}</p>}
    </section>;

    return (
        <section className="card max-w-3xl space-y-4">
            <div className="flex flex-col gap-3 sm:flex-row sm:items-start sm:justify-between">
                <div>
                    <Heading
                        className={`flex items-center gap-2 font-semibold text-content-primary ${
                            headingLevel === 3 ? 'text-base' : 'text-lg'
                        }`}
                    >
                        <ShieldCheck className="h-5 w-5 text-action" />
                        {t('settings.adminAccessTitle')}
                    </Heading>
                    <p className="mt-1 text-sm text-content-secondary">{t('settings.adminAccessDescription')}</p>
                </div>
                <div
                    className={`inline-flex w-fit items-center gap-2 rounded-full border px-3 py-1 text-xs font-medium ${
                        hasAdminKey
                            ? 'border-feedback-info-border bg-feedback-info-muted text-feedback-info-foreground'
                            : 'border-feedback-warning-border bg-feedback-warning-muted text-feedback-warning-foreground'
                    }`}
                    role="status"
                >
                    <KeyRound aria-hidden="true" className="h-3.5 w-3.5" />
                    {hasAdminKey ? t('settings.adminAccessConfigured') : t('settings.adminAccessNotConfigured')}
                </div>
            </div>

            {actingAsOperator && <OperatorIdentityNotice />}
            {message && (
                <div
                    className={`flex items-center gap-2 rounded-md border px-3 py-2 text-sm ${
                        message.type === 'success'
                            ? 'border-feedback-success-border bg-feedback-success-muted text-feedback-success-foreground'
                            : 'border-feedback-danger-border bg-feedback-danger-muted text-feedback-danger-foreground'
                    }`}
                    role={message.type === 'error' ? 'alert' : 'status'}
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
                    disabled={verifying}
                    onChange={(event) => setDraftKey(event.target.value)}
                    placeholder={t('settings.adminAccessPlaceholder')}
                />
                <div className="flex shrink-0 items-end gap-2">
                    <Button type="button" variant={saveVariant} onClick={() => void saveKey()} isLoading={verifying} className="inline-flex items-center gap-2">
                        <KeyRound className="h-4 w-4" />
                        {t('settings.adminAccessSave')}
                    </Button>
                    {/* Nothing stored and nothing typed: there is nothing to clear, so no button. */}
                    {(hasAdminKey || draftKey) && <Button
                        type="button"
                        variant="outline"
                        disabled={verifying}
                        onClick={clearKey}
                        className="inline-flex items-center gap-2"
                    >
                        <Trash2 className="h-4 w-4" />
                        {t('settings.adminAccessClear')}
                    </Button>}
                </div>
            </div>
        </section>
    );
};

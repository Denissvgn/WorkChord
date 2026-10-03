import { useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import api from '../services/api';
import { useIdentity } from '../features/identity/identityContext';
import { getApiErrorMessage } from '../utils/apiError';
import { Button } from '../components/common/Button';

export default function NativeConnectionPage() {
    const [params] = useSearchParams();
    const request = params.get('request') ?? '';
    const principal = useIdentity()?.identity?.principal?.id;
    return <NativeConnection key={`${request}:${principal ?? 'anonymous'}`} request={request} />;
}

function NativeConnection({ request }: { request: string }) {
    const { t } = useTranslation();
    const valid = /^[A-Za-z0-9_-]{43}$/.test(request);
    const identity = useIdentity()?.identity;
    const [confirmed, setConfirmed] = useState(false);
    const [approved, setApproved] = useState(false);
    const [saving, setSaving] = useState(false);
    const [error, setError] = useState<string | null>(null);
    // feedback-policy: query loading,error,retry,empty
    const connection = useQuery({ queryKey: ['nativeConnection', request], enabled: valid && identity?.principal?.kind === 'human',
        retry: false, queryFn: async ({ signal }) => (await api.get<{ verification_code: string; expires_at: string; approved: boolean }>(
            `/auth/native-connections/${request}`, { signal })).data });
    const approve = async () => {
        if (!connection.data || !confirmed || saving) return;
        setSaving(true); setError(null);
        try {
            await api.post(`/auth/native-connections/${request}/approve`, { verification_code: connection.data.verification_code });
            setApproved(true);
        } catch (cause) { setError(getApiErrorMessage(cause, t('teamwork.connectFailed'))); }
        finally { setSaving(false); }
    };
    return <section className="mx-auto max-w-xl space-y-5 p-6" aria-labelledby="native-connection-title">
        <h1 id="native-connection-title" className="text-2xl font-semibold">{t('teamwork.connectDevice')}</h1>
        <p>{t('teamwork.connectHelp')}</p>
        {!valid ? <p role="alert">{t('teamwork.connectInvalid')}</p>
            : identity?.principal?.kind !== 'human' ? <p role="alert">{t('teamwork.connectHumanRequired')}</p>
                : connection.isPending ? <p role="status">{t('common.loading')}</p>
                    : connection.isError ? <div role="alert" className="space-y-3"><p>{getApiErrorMessage(connection.error, t('teamwork.connectFailed'))}</p>
                        <Button variant="secondary" onClick={() => void connection.refetch()}>{t('teamwork.retry')}</Button></div>
                        : !connection.data ? <p role="status">{t('teamwork.connectInvalid')}</p>
                            : approved || connection.data.approved ? <p role="status">{t('teamwork.connectApproved')}</p> : <>
                                <p>{t('teamwork.connectAccount', { name: identity.principal.display_name })}</p>
                                <p className="font-mono text-3xl tracking-wide">{connection.data.verification_code}</p>
                                <label className="flex min-h-11 items-center gap-3">
                                    <input type="checkbox" className="h-5 w-5" checked={confirmed} onChange={event => setConfirmed(event.target.checked)} />
                                    {t('teamwork.connectConfirm')}
                                </label>
                                {error && <p role="alert">{error}</p>}
                                <Button onClick={() => void approve()} disabled={!confirmed || saving}>{saving ? t('common.saving') : t('teamwork.connectApprove')}</Button>
                            </>}
    </section>;
}

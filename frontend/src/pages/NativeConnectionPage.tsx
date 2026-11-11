import { useEffect, useState } from 'react';
import { useSearchParams } from 'react-router-dom';
import { useQuery } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import api from '../services/api';
import { useIdentity } from '../features/identity/identityContext';
import { getApiErrorMessage } from '../utils/apiError';
import { Button } from '../components/common/Button';
import { DisabledReason } from '../components/common/DisabledReason';

export default function NativeConnectionPage() {
    const [params] = useSearchParams();
    const request = params.get('request') ?? '';
    const principal = useIdentity()?.identity?.principal?.id;
    return <NativeConnection key={`${request}:${principal ?? 'anonymous'}`} request={request} />;
}

/** "4:32" until the request expires; null once it has. */
const remaining = (expiresAt: string, now: number) => {
    const seconds = Math.floor((new Date(expiresAt).getTime() - now) / 1000);
    if (!Number.isFinite(seconds) || seconds <= 0) return null;
    return `${Math.floor(seconds / 60)}:${String(seconds % 60).padStart(2, '0')}`;
};

function NativeConnection({ request }: { request: string }) {
    const { t } = useTranslation();
    const valid = /^[A-Za-z0-9_-]{43}$/.test(request);
    const identity = useIdentity()?.identity;
    const [confirmed, setConfirmed] = useState(false);
    const [outcome, setOutcome] = useState<'approved' | 'denied' | null>(null);
    const [saving, setSaving] = useState<'approve' | 'deny' | null>(null);
    const [error, setError] = useState<string | null>(null);
    const [now, setNow] = useState(() => Date.now());
    // feedback-policy: query loading,error,retry,empty
    const connection = useQuery({ queryKey: ['nativeConnection', request], enabled: valid && identity?.principal?.kind === 'human',
        retry: false, queryFn: async ({ signal }) => (await api.get<{ verification_code: string; expires_at: string; approved: boolean }>(
            `/auth/native-connections/${request}`, { signal })).data });
    const pending = Boolean(connection.data && !connection.data.approved && outcome === null);
    useEffect(() => {
        if (!pending) return undefined;
        const timer = window.setInterval(() => setNow(Date.now()), 1000);
        return () => window.clearInterval(timer);
    }, [pending]);
    const decide = async (decision: 'approve' | 'deny') => {
        if (!connection.data || saving || (decision === 'approve' && !confirmed)) return;
        setSaving(decision); setError(null);
        try {
            await api.post(`/auth/native-connections/${request}/${decision}`,
                decision === 'approve' ? { verification_code: connection.data.verification_code } : undefined);
            setOutcome(decision === 'approve' ? 'approved' : 'denied');
        } catch (cause) { setError(getApiErrorMessage(cause, t('teamwork.connectFailed'))); }
        finally { setSaving(null); }
    };
    const timeLeft = connection.data ? remaining(connection.data.expires_at, now) : null;
    return <section className="mx-auto max-w-xl space-y-5 p-6" aria-labelledby="native-connection-title">
        <h1 id="native-connection-title" className="text-2xl font-semibold">{t('teamwork.connectDevice')}</h1>
        <p>{t('teamwork.connectHelp')}</p>
        {!valid ? <p role="alert" className="banner warn">{t('teamwork.connectInvalid')}</p>
            : identity?.principal?.kind !== 'human' ? <p role="alert" className="banner warn">{t('teamwork.connectHumanRequired')}</p>
                : connection.isPending ? <p role="status">{t('common.loading')}</p>
                    : connection.isError ? <div role="alert" className="banner warn space-y-3"><p>{getApiErrorMessage(connection.error, t('teamwork.connectFailed'))}</p>
                        <Button variant="secondary" onClick={() => void connection.refetch()}>{t('teamwork.retry')}</Button></div>
                        : !connection.data ? <p role="status" className="banner warn">{t('teamwork.connectInvalid')}</p>
                            : outcome === 'denied' ? <p role="status" className="banner">{t('teamwork.connectDenied')}</p>
                                : outcome === 'approved' || connection.data.approved ? <p role="status" className="banner done">{t('teamwork.connectApproved')}</p>
                                    : timeLeft === null ? <p role="alert" className="banner warn">{t('teamwork.connectExpired')}</p> : <>
                                        <p>{t('teamwork.connectAccount', { name: identity.principal.display_name })}</p>
                                        <p className="text-sm text-content-secondary">{t('teamwork.connectScope')}</p>
                                        <p className="font-mono text-3xl tracking-wide">{connection.data.verification_code}</p>
                                        <p className="text-sm text-content-secondary" aria-live="off">{t('teamwork.connectExpiresIn', { time: timeLeft })}</p>
                                        <label className="flex min-h-11 items-center gap-3">
                                            <input type="checkbox" className="h-5 w-5" checked={confirmed} onChange={event => setConfirmed(event.target.checked)} />
                                            {t('teamwork.connectConfirm')}
                                        </label>
                                        {error && <p role="alert" className="banner warn">{error}</p>}
                                        <div className="flex flex-wrap gap-2">
                                            <Button onClick={() => void decide('approve')} disabled={!confirmed || saving !== null} isLoading={saving === 'approve'}>{t('teamwork.connectApprove')}</Button>
                                            <Button variant="secondary" onClick={() => void decide('deny')} disabled={saving !== null} isLoading={saving === 'deny'}>{t('teamwork.connectDeny')}</Button>
                                        </div>
                                        {!confirmed && <DisabledReason reason={t('teamwork.connectConfirmFirst')} />}
                                    </>}
    </section>;
}

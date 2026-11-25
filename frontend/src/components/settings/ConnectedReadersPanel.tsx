import { useState } from 'react';
import { useMutation, useQuery, useQueryClient } from '@tanstack/react-query';
import { useTranslation } from 'react-i18next';
import { identityService, type AccountSession } from '../../features/identity/identityService';
import { useIdentity } from '../../features/identity/identityContext';
import { formatDateTime } from '../../utils/formatDate';
import { getApiErrorMessage } from '../../utils/apiError';
import { Button } from '../common/Button';

const connected = (row: AccountSession, now: number) => row.access === 'observe' && !row.revoked_at
    && (!row.expires_at || new Date(row.expires_at).getTime() > now);

/** Read-only readers paired with this account, or with a trusted-local workspace; each can be revoked. */
export const ConnectedReadersPanel = () => {
    const { t, i18n } = useTranslation();
    const identity = useIdentity()?.identity;
    const signedIn = identity?.principal?.kind === 'human';
    const localBrowser = identity?.mode === 'trusted_local' && !identity.principal;
    const enabled = (signedIn || localBrowser) && identity?.access !== 'observe';
    const queryClient = useQueryClient();
    const [notice, setNotice] = useState<string | null>(null);
    // feedback-policy: query loading,error,retry,empty
    const sessions = useQuery({ queryKey: ['accountSessions'], enabled,
        queryFn: ({ signal }) => identityService.sessions(signal),
        select: rows => rows.filter(row => connected(row, Date.now())) });
    // feedback-policy: mutation pending,inline
    const revoke = useMutation({
        mutationFn: (row: AccountSession) => identityService.revokeSession(row.public_id),
        onMutate: () => setNotice(null),
        onSuccess: (_result, row) => {
            setNotice(t('teamwork.readersRevoked', { label: row.client_label || t('teamwork.readersUnnamed') }));
            void queryClient.invalidateQueries({ queryKey: ['accountSessions'] });
        },
    });
    if (!enabled) return null;
    const readers = sessions.data ?? [];
    return (
        <section className="card card-pad space-y-3" aria-labelledby="connected-readers-title">
            <h3 id="connected-readers-title" className="text-base font-semibold">{t('teamwork.readersTitle')}</h3>
            <p className="text-sm text-content-secondary">{t('teamwork.readersHelp')}</p>
            {sessions.isPending ? <p role="status">{t('common.loading')}</p>
                : sessions.isError ? (
                    <div role="alert" className="banner warn space-y-3">
                        <p>{t('teamwork.readersLoadFailed')}</p>
                        <Button variant="secondary" onClick={() => void sessions.refetch()}>{t('teamwork.retry')}</Button>
                    </div>
                )
                    : readers.length === 0 ? <p className="text-sm">{t('teamwork.readersEmpty')}</p>
                        : (
                            <ul className="space-y-2">
                                {readers.map(row => {
                                    const name = row.client_label || t('teamwork.readersUnnamed');
                                    return (
                                        <li key={row.public_id} className="flex flex-wrap items-center justify-between gap-3">
                                            <div className="min-w-0">
                                                <p className="font-medium wrap-break-word">{name}</p>
                                                <p className="text-sm text-content-secondary">
                                                    {t('teamwork.readersConnected', { date: formatDateTime(row.created_at, i18n.language) })}
                                                    {row.expires_at && <> · {t('teamwork.readersExpires', { date: formatDateTime(row.expires_at, i18n.language) })}</>}
                                                </p>
                                            </div>
                                            <Button variant="secondary" aria-label={t('teamwork.readersRevokeLabel', { label: name })}
                                                onClick={() => revoke.mutate(row)} disabled={revoke.isPending}
                                                isLoading={revoke.isPending && revoke.variables?.public_id === row.public_id}>
                                                {t('teamwork.readersRevoke')}
                                            </Button>
                                        </li>
                                    );
                                })}
                            </ul>
                        )}
            {revoke.isError && <p role="alert" className="banner warn">{getApiErrorMessage(revoke.error, t('teamwork.readersRevokeFailed'))}</p>}
            {notice && <p role="status" className="banner done">{notice}</p>}
        </section>
    );
};

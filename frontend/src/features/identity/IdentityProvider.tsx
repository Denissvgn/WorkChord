import { useCallback, useEffect, useMemo, useRef, useState } from 'react';
import type { ReactNode } from 'react';
import { QueryClient, QueryClientProvider, useQuery, useQueryClient } from '@tanstack/react-query';
import { useLocation } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { LogIn, LogOut, ShieldCheck, User } from 'lucide-react';
import { Button } from '../../components/common/Button';
import { getApiErrorMessage } from '../../utils/apiError';
import { clearAdminApiKey } from '../../utils/adminAccess';
import { clearAgentApiKey } from '../../utils/agentAccess';
import { ADMIN_API_KEY_CHANGED_EVENT } from '../../utils/adminAccess';
import { AGENT_API_KEY_CHANGED_EVENT } from '../../utils/agentAccess';
import { installWorkFreshness } from '../workQueryFreshness';
import { setSessionIntegrity, IDENTITY_EXPIRED_EVENT } from '../../services/api';
import { identityService } from './identityService';
import { teamService } from '../../services/teamService';
import api from '../../services/api';
import type { WorkspaceIdentity } from './identityService';

import { IdentityContext, useIdentity } from './identityContext';

const clearDrafts = (scope?: string) => {
    for (const key of Object.keys(sessionStorage)) {
        if (key.startsWith(`workchord-draft:${scope ? `${scope}:` : ''}`)) sessionStorage.removeItem(key);
    }
};

export const IdentityProvider = ({ children }: { children: ReactNode }) => {
    const { t } = useTranslation();
    const location = useLocation();
    const queryClient = useQueryClient();
    const [expired, setExpired] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [credentialEpoch, setCredentialEpoch] = useState(0);
    const [verified, setVerified] = useState<{ resolved?: WorkspaceIdentity; lastAuthenticated: WorkspaceIdentity | null }>({ lastAuthenticated: null });
    const previous = useRef(sessionStorage.getItem('workchord-principal-scope'));
    const fetchIdentity = useCallback(async ({ signal }: { signal: AbortSignal }) => {
        const result = await identityService.get(signal);
        if (signal.aborted) throw new DOMException('Request cancelled', 'AbortError');
        setVerified(previousValue => ({ resolved: result, lastAuthenticated: result.authenticated ? result
            : result.authentication_error === 'session_expired' ? previousValue.lastAuthenticated : null }));
        setExpired(result.authentication_error === 'session_expired');
        return result;
    }, []);
    // feedback-policy: query loading,error,retry,empty
    const identityQuery = useQuery({ queryKey: ['workspaceIdentity'], queryFn: fetchIdentity,
        retry: false, staleTime: 15000, refetchInterval: 30000, refetchOnWindowFocus: true });
    const { refetch: refreshIdentity } = identityQuery;
    const lastAuthenticated = verified.lastAuthenticated;
    const expiredSession = verified.resolved?.authentication_error === 'session_expired';
    const identity = useMemo(() => expiredSession && lastAuthenticated
        ? { ...lastAuthenticated, authenticated: false, csrf_token: null, authentication_error: 'session_expired' }
        : verified.resolved, [expiredSession, lastAuthenticated, verified.resolved]);
    const scope = identity?.principal ? String(identity.principal.id) : identity?.mode === 'trusted_local' ? 'local' : null;
    const accessKey = JSON.stringify([scope, identity?.workspace_role, identity?.projects, identity?.profile?.id, credentialEpoch]);
    const workClient = useMemo(() => new QueryClient({ defaultOptions: { queries: { retry: 1, staleTime: 15000, refetchOnWindowFocus: true, meta: { workspaceAccess: accessKey } } } }), [accessKey]);
    useEffect(() => {
        const current = verified.resolved;
        if (current && !current.authenticated && current.mode === 'managed' && current.authentication_error !== 'session_expired') {
            if (previous.current) clearDrafts(previous.current);
        }
    }, [verified.resolved]);
    useEffect(() => {
        const stop = installWorkFreshness(workClient);
        return () => { stop(); workClient.clear(); };
    }, [workClient]);
    useEffect(() => {
        const changed = () => setCredentialEpoch(value => value + 1);
        window.addEventListener(ADMIN_API_KEY_CHANGED_EVENT, changed);
        window.addEventListener(AGENT_API_KEY_CHANGED_EVENT, changed);
        return () => {
            window.removeEventListener(ADMIN_API_KEY_CHANGED_EVENT, changed);
            window.removeEventListener(AGENT_API_KEY_CHANGED_EVENT, changed);
        };
    }, []);
    useEffect(() => {
        if (!identity) return;
        setSessionIntegrity(identity.csrf_token, identity.principal?.kind === 'human');
        if (scope && previous.current && scope !== previous.current) {
            queryClient.removeQueries({ predicate: query => query.queryKey[0] !== 'workspaceIdentity' });
            clearDrafts(previous.current);
            clearAdminApiKey();
            clearAgentApiKey();
        }
        if (scope) {
            previous.current = scope;
            sessionStorage.setItem('workchord-principal-scope', scope);
        }
    }, [identity, queryClient, scope]);
    useEffect(() => {
        const handleExpiry = () => {
            setExpired(true);
            setSessionIntegrity(null, identity?.principal?.kind === 'human');
            queryClient.removeQueries({ predicate: query => query.queryKey[0] !== 'workspaceIdentity' && query.getObserversCount() === 0 });
            void refreshIdentity();
        };
        window.addEventListener(IDENTITY_EXPIRED_EVENT, handleExpiry);
        return () => window.removeEventListener(IDENTITY_EXPIRED_EVENT, handleExpiry);
    }, [queryClient, refreshIdentity, identity?.principal?.kind]);
    const performSignOut = async () => {
        try {
            await identityService.logout();
            setSessionIntegrity(null, false);
            clearDrafts();
            clearAdminApiKey();
            clearAgentApiKey();
            sessionStorage.removeItem('workchord-principal-scope');
            previous.current = null;
            queryClient.clear();
            workClient.clear();
            window.location.assign('/');
        } catch (cause) { setError(getApiErrorMessage(cause, t('identity.logoutFailed'))); }
    };
    const signOut = async () => {
        const event = new CustomEvent('workchord-before-signout', { cancelable: true, detail: () => { void performSignOut(); } });
        if (window.dispatchEvent(event)) await performSignOut();
    };
    const login = `/api/auth/login?return_to=${encodeURIComponent(location.pathname + location.search)}`;
    const publicRoute = location.pathname === '/welcome' || location.pathname.startsWith('/plan/share/');
    const mayEnter = identity?.mode === 'trusted_local' || identity?.authenticated || expiredSession && lastAuthenticated !== null;
    if (!publicRoute && !mayEnter) {
        return <main className="wc min-h-screen bg-surface-canvas px-6 py-16 text-content-primary">
            <section className="mx-auto max-w-lg space-y-5">
                <h1 className="text-2xl font-semibold">{t('identity.signInTitle')}</h1>
                {identityQuery.isPending ? <p role="status">{t('common.loading')}</p> : <>
                    <p className="text-content-secondary">{t(identity?.configured ? 'identity.signInBody' : 'identity.setupRequired')}</p>
                    {identityQuery.isError && <p role="alert">{getApiErrorMessage(identityQuery.error, t('identity.unavailable'))}</p>}
                    {identity?.configured && <a className="inline-flex min-h-11 items-center gap-2 rounded-md bg-action px-4 py-2 font-medium text-content-inverse" href={login}>
                        <LogIn aria-hidden="true" className="h-4 w-4" />{t('identity.signIn')}
                    </a>}
                    <Button variant="secondary" onClick={() => { void identityQuery.refetch(); }}>{t('taskEditor.retry')}</Button>
                </>}
            </section>
        </main>;
    }
    return <IdentityContext.Provider value={{ identity, refresh: () => { void identityQuery.refetch(); }, signOut }}>
        {(expired || expiredSession) && <div role="alert" className="wc border-b border-feedback-warning-border bg-feedback-warning-muted px-4 py-3 text-feedback-warning-foreground">
            {t('identity.expired')} <a className="font-semibold underline" href={login}>{t('identity.signIn')}</a>
        </div>}
        {error && <p role="alert" className="wc p-3 text-feedback-danger">{error}</p>}
        {identity?.authenticated && !identity.workspace_role && Object.keys(identity.projects).length === 0 &&
            <p role="status" className="wc border-b border-border bg-surface-muted px-4 py-3 text-sm text-content-secondary">{t('identity.membershipMissing')}</p>}
        <QueryClientProvider client={workClient}><div key={accessKey}>{children}</div></QueryClientProvider>
    </IdentityContext.Provider>;
};

export const IdentityBadge = () => {
    const context = useIdentity();
    const { t } = useTranslation();
    const [error, setError] = useState<string | null>(null);
    const [profileId, setProfileId] = useState('');
    const operator = context?.identity?.workspace_role === 'owner' || context?.identity?.workspace_role === 'operator';
    // feedback-policy: query loading,error,retry,empty
    const profilesQuery = useQuery({ queryKey: ['teamMemberProfiles'], queryFn: teamService.getProfiles, enabled: Boolean(operator) });
    if (!context?.identity) return null;
    const { identity } = context;
    return <div className="flex items-center gap-2">
        <details className="relative">
            <summary className="session-badge cursor-pointer list-none" aria-label={t('identity.accountMenu')}>
                <User className="h-4 w-4" aria-hidden="true" />
                <strong>{identity.principal?.display_name ?? t('identity.localMode')}</strong>
            </summary>
            <div className="absolute right-0 z-50 mt-2 w-80 max-w-[90vw] space-y-3 rounded-xl border border-border bg-surface-card p-4 text-sm text-content-primary shadow-lg">
                <p className="flex items-center gap-2"><ShieldCheck className="h-4 w-4" aria-hidden="true" />{t(identity.mode === 'trusted_local' ? 'identity.localMode' : 'identity.managedMode')}</p>
                {identity.principal && <p>{t('identity.accountId', { id: identity.principal.id })}</p>}
                <p>{identity.profile ? t('identity.linkedProfile', { name: identity.profile.display_name }) : t('identity.profileUnlinked')}</p>
                {operator && identity.principal?.kind === 'human' && <div className="space-y-2">
                    <label className="block text-sm">{t('identity.chooseProfile')}
                        <select className="mt-1 min-h-11 w-full rounded-md border border-border bg-surface-card px-2" value={profileId}
                            onChange={event => setProfileId(event.target.value)} disabled={profilesQuery.isLoading}>
                            <option value="">{t('identity.chooseProfile')}</option>
                            {(profilesQuery.data ?? []).map(profile => <option key={profile.id} value={profile.id}>{profile.display_name} (#{profile.id})</option>)}
                        </select>
                    </label>
                    {profilesQuery.isError && <button type="button" className="underline" onClick={() => { void profilesQuery.refetch(); }}>{t('taskEditor.retry')}</button>}
                    <Button size="sm" variant="secondary" disabled={!profileId} onClick={async () => {
                        try {
                            await api.put(`/auth/principals/${identity.principal!.id}/profile`, { profile_id: Number(profileId), reason: 'Owner explicitly linked the verified account to this work profile' });
                            context.refresh(); setError(null);
                        } catch (cause) { setError(getApiErrorMessage(cause, t('identity.linkFailed'))); }
                    }}>{t('identity.linkProfile')}</Button>
                </div>}
                {identity.authenticated && !identity.workspace_role && Object.keys(identity.projects).length === 0 && <p role="status">{t('identity.membershipMissing')}</p>}
                {identity.workspace_role && <p>{t('identity.workspaceRole', { role: identity.workspace_role })}</p>}
                {identity.principal?.kind === 'human' && <>
                    <Button size="sm" variant="secondary" onClick={async () => {
                        try { await identityService.transferGuest(); context.refresh(); setError(null); }
                        catch (cause) { setError(getApiErrorMessage(cause, t('identity.transferFailed'))); }
                    }}>{t('identity.transferGuest')}</Button>
                    <p className="text-xs text-content-secondary">{t('identity.transferNote')}</p>
                    <Button size="sm" variant="secondary" onClick={() => { void context.signOut(); }}><LogOut className="mr-2 h-4 w-4" aria-hidden="true" />{t('identity.signOut')}</Button>
                </>}
                {error && <p role="alert" className="text-feedback-danger">{error}</p>}
            </div>
        </details>
    </div>;
};

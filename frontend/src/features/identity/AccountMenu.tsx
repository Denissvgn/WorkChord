import { useCallback, useEffect, useId, useRef, useState } from 'react';
import type { FormEvent } from 'react';
import { useQuery, useQueryClient } from '@tanstack/react-query';
import { Link } from 'react-router-dom';
import { useTranslation } from 'react-i18next';
import { LogOut, User } from 'lucide-react';
import { Button } from '../../components/common/Button';
import { Input } from '../../components/common/Input';
import { protectedQueryKeys } from '../../components/settings/protectedQueryKeys';
import { teamService } from '../../services/teamService';
import { getApiErrorMessage, getApiErrorStatus } from '../../utils/apiError';
import { ADMIN_API_KEY_CHANGED_EVENT, clearAdminApiKey, hasAdminApiKey, setAdminApiKey } from '../../utils/adminAccess';
import { useAdminAccess } from '../../hooks/useAdminAccess';
import api from '../../services/api';
import { useIdentity } from './identityContext';
import { identityService } from './identityService';
import { LocalProfilePicker } from './LocalProfilePicker';

/**
 * The top-bar account menu: who the work is done as, how the sign-in is established,
 * whether editing is unlocked, and links to My preferences and Access. It is a popover
 * under its button that closes on Escape and on an outside click.
 */
export const IdentityBadge = () => {
    const context = useIdentity();
    const { t } = useTranslation();
    const queryClient = useQueryClient();
    const { hasAdminKey } = useAdminAccess();
    const panelId = useId();
    const [open, setOpen] = useState(false);
    const [error, setError] = useState<string | null>(null);
    const [profileId, setProfileId] = useState('');
    const [keyStored, setKeyStored] = useState(hasAdminApiKey);
    const [unlockOpen, setUnlockOpen] = useState(false);
    const [draftKey, setDraftKey] = useState('');
    const [keyMessage, setKeyMessage] = useState<string | null>(null);
    const [verifying, setVerifying] = useState(false);
    const wrapper = useRef<HTMLDivElement>(null);
    const trigger = useRef<HTMLButtonElement>(null);
    const operator = context?.identity?.workspace_role === 'owner' || context?.identity?.workspace_role === 'operator';
    // feedback-policy: query loading,error,retry,empty
    const profilesQuery = useQuery({ queryKey: ['teamMemberProfiles'], queryFn: teamService.getProfiles, enabled: Boolean(operator) });

    const close = useCallback((restoreFocus: boolean) => {
        setOpen(false);
        if (restoreFocus) trigger.current?.focus();
    }, []);

    useEffect(() => {
        if (!open) return;
        const onPointerDown = (event: PointerEvent) => {
            const root = wrapper.current;
            if (root?.contains(event.target as Node)) return;
            const focusWasInside = Boolean(root?.contains(document.activeElement));
            close(false);
            if (focusWasInside) {
                // The pointer's default action moves focus after this handler, so the return waits for it.
                // It applies only when nothing else took focus, so a field the user clicked keeps it.
                window.setTimeout(() => {
                    const active = document.activeElement;
                    if (!active || active === document.body) trigger.current?.focus();
                }, 0);
            }
        };
        const onKeyDown = (event: KeyboardEvent) => {
            if (event.key !== 'Escape') return;
            event.preventDefault();
            close(true);
        };
        document.addEventListener('pointerdown', onPointerDown);
        document.addEventListener('keydown', onKeyDown);
        return () => {
            document.removeEventListener('pointerdown', onPointerDown);
            document.removeEventListener('keydown', onKeyDown);
        };
    }, [open, close]);

    useEffect(() => {
        const sync = () => setKeyStored(hasAdminApiKey());
        window.addEventListener(ADMIN_API_KEY_CHANGED_EVENT, sync);
        return () => window.removeEventListener(ADMIN_API_KEY_CHANGED_EVENT, sync);
    }, []);

    if (!context?.identity) return null;
    const { identity } = context;
    const local = identity.mode === 'trusted_local' && !identity.principal;
    const name = identity.principal?.display_name
        ?? (local && identity.profile ? t('identity.workingAs', { name: identity.profile.display_name }) : t('identity.localMode'));
    const signedIn = identity.mode === 'managed' && identity.authenticated;

    const refreshProtectedQueries = () => {
        protectedQueryKeys.forEach(queryKey => { void queryClient.invalidateQueries({ queryKey: [...queryKey] }); });
    };
    const removeProtectedQueries = () => {
        protectedQueryKeys.forEach(queryKey => { queryClient.removeQueries({ queryKey: [...queryKey] }); });
    };

    const unlock = async (event: FormEvent) => {
        event.preventDefault();
        const key = draftKey.trim();
        if (!key) {
            setKeyMessage(t('settings.adminAccessEnterKey'));
            return;
        }
        setVerifying(true);
        setKeyMessage(null);
        try {
            // One protected read tells whether the server accepts the key. The key is sent with this request
            // only and stored after the server accepts it: storing it remounts the app under IdentityProvider,
            // which would drop this menu and any message it shows.
            await api.get('/scheduling-rules', { headers: { 'X-Admin-API-Key': key } });
            setAdminApiKey(key);
            removeProtectedQueries();
            setDraftKey('');
            setUnlockOpen(false);
            refreshProtectedQueries();
        } catch (cause) {
            const status = getApiErrorStatus(cause);
            setKeyMessage(status === 401 || status === 403 || status === 503
                ? t(status === 503 ? 'settings.adminAccessBackendNotConfigured' : 'settings.adminAccessRejected')
                : t('identity.keyNotChecked'));
        } finally {
            setVerifying(false);
        }
    };

    const lock = () => {
        clearAdminApiKey();
        removeProtectedQueries();
        setUnlockOpen(false);
        setKeyMessage(null);
    };

    const performSignOut = () => { void context.signOut(); };

    return <div ref={wrapper} className="relative flex items-center gap-2">
        <button
            ref={trigger}
            type="button"
            className="session-badge cursor-pointer"
            aria-label={t('identity.accountMenu')}
            aria-expanded={open}
            aria-haspopup="dialog"
            aria-controls={open ? panelId : undefined}
            onClick={() => (open ? close(true) : setOpen(true))}
        >
            <User className="h-4 w-4" aria-hidden="true" />
            <strong>{name}</strong>
        </button>
        {open && <div
            id={panelId}
            role="dialog"
            aria-label={t('identity.accountMenu')}
            className="absolute right-0 top-full z-50 mt-2 max-h-[80vh] w-80 max-w-[90vw] space-y-4 overflow-y-auto rounded-xl border border-border bg-surface-card p-4 text-sm text-content-primary shadow-lg"
        >
            <section className="space-y-2" aria-labelledby={`${panelId}-working`}>
                <h3 id={`${panelId}-working`} className="font-semibold">{t('identity.workingAsHeading')}</h3>
                {local ? <>
                    <p className="font-medium">{identity.profile ? t('identity.workingAs', { name: identity.profile.display_name }) : t('identity.notWorkingAs')}</p>
                    <LocalProfilePicker current={identity.profile} onChosen={context.refresh} />
                </> : <>
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
                </>}
            </section>

            <section className="space-y-2" aria-labelledby={`${panelId}-sign-in`}>
                <h3 id={`${panelId}-sign-in`} className="font-semibold">{t('identity.signInHeading')}</h3>
                <p>{identity.mode === 'trusted_local' ? t('identity.localNotVerifiedSignIn') : signedIn ? t('identity.signedInVerified') : t('identity.notSignedIn')}</p>
                {identity.principal && <p className="text-xs text-content-secondary">{t('identity.accountId', { id: identity.principal.id })}</p>}
                {identity.authenticated && !identity.workspace_role && Object.keys(identity.projects).length === 0 && <p role="status">{t('identity.membershipMissing')}</p>}
                {identity.workspace_role && <p>{t('identity.workspaceRole', { role: identity.workspace_role })}</p>}
                {signedIn && identity.principal?.kind === 'human' && <>
                    <Button size="sm" variant="secondary" onClick={async () => {
                        try { await identityService.transferGuest(); context.refresh(); setError(null); }
                        catch (cause) { setError(getApiErrorMessage(cause, t('identity.transferFailed'))); }
                    }}>{t('identity.transferGuest')}</Button>
                    <p className="text-xs text-content-secondary">{t('identity.transferNote')}</p>
                    <Button size="sm" variant="secondary" onClick={performSignOut}><LogOut className="mr-2 h-4 w-4" aria-hidden="true" />{t('identity.signOut')}</Button>
                </>}
            </section>

            <section className="space-y-2" aria-labelledby={`${panelId}-editing`}>
                <div className="flex flex-wrap items-center justify-between gap-2">
                    <h3 id={`${panelId}-editing`} className="font-semibold">
                        {t('identity.editing', { state: hasAdminKey ? t('identity.editingUnlocked') : t('identity.editingLocked') })}
                    </h3>
                    {hasAdminKey
                        ? keyStored && <Button size="sm" variant="secondary" onClick={lock}>{t('identity.lock')}</Button>
                        : !unlockOpen && <Button size="sm" variant="secondary" aria-expanded={unlockOpen} aria-controls={`${panelId}-unlock`}
                            onClick={() => setUnlockOpen(true)}>{t('identity.unlock')}</Button>}
                </div>
                <p className="text-xs text-content-secondary">{hasAdminKey && !keyStored ? t('identity.editingByRole') : t('identity.editingNote')}</p>
                {!hasAdminKey && unlockOpen && <form id={`${panelId}-unlock`} className="space-y-2" onSubmit={unlock}>
                    <p className="text-xs text-content-secondary">{t('identity.unlockHelp')}</p>
                    <Input
                        label={t('settings.adminAccessField')}
                        type="password"
                        autoComplete="off"
                        spellCheck={false}
                        value={draftKey}
                        onChange={event => setDraftKey(event.target.value)}
                    />
                    <Button type="submit" size="sm" isLoading={verifying} disabled={verifying}>{t('identity.unlock')}</Button>
                </form>}
                {keyMessage && <p role="alert" className="text-feedback-danger-foreground">{keyMessage}</p>}
            </section>

            <nav aria-label={t('identity.accountLinks')} className="flex flex-col gap-1 border-t border-border pt-3">
                <Link className="underline" to="/settings?tab=theme" onClick={() => close(false)}>{t('settingsPage.groups.myPreferences')}</Link>
                <Link className="underline" to="/settings?tab=access" onClick={() => close(false)}>{t('settingsPage.sections.access')}</Link>
            </nav>

            {error && <p role="alert" className="text-feedback-danger">{error}</p>}
        </div>}
    </div>;
};

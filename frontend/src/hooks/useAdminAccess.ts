import { useEffect, useState } from 'react';
import { ADMIN_API_KEY_CHANGED_EVENT, hasAdminApiKey } from '../utils/adminAccess';
import { useIdentity } from '../features/identity/identityContext';

export const useAdminAccess = () => {
    const identity = useIdentity();
    const [hasAdminKey, setHasAdminKey] = useState(hasAdminApiKey());

    useEffect(() => {
        const refreshAdminKeyState = () => setHasAdminKey(hasAdminApiKey());
        window.addEventListener(ADMIN_API_KEY_CHANGED_EVENT, refreshAdminKeyState);
        window.addEventListener('storage', refreshAdminKeyState);
        return () => {
            window.removeEventListener(ADMIN_API_KEY_CHANGED_EVENT, refreshAdminKeyState);
            window.removeEventListener('storage', refreshAdminKeyState);
        };
    }, []);

    const role = identity?.identity?.workspace_role;
    const hasAdminAccess = hasAdminKey || role === 'owner' || role === 'operator';
    return { hasAdminKey: hasAdminAccess, hasAdminAccess };
};

/**
 * Whether this person may read settings and views of work without the admin key:
 * a trusted-local session or a workspace member. The server applies the same rule
 * and withholds sensitive values; every change still needs the key.
 */
export const useKeylessReader = () => {
    const identity = useIdentity()?.identity;
    if (!identity) return { settings: false, workViews: false };
    const local = identity.mode === 'trusted_local' && !identity.principal;
    // `!= null`: an absent role is not membership, matching the server's `is not None`.
    const member = identity.principal?.kind === 'human' && identity.workspace_role != null;
    const projectMember = identity.principal?.kind === 'human' && Object.keys(identity.projects ?? {}).length > 0;
    return { settings: local || member, workViews: local || member || projectMember };
};

/** Settings panels load for key holders and for keyless readers, who see them read-only. */
export const useCanReadSettings = () => {
    const { hasAdminKey } = useAdminAccess();
    const reader = useKeylessReader();
    return hasAdminKey || reader.settings;
};

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

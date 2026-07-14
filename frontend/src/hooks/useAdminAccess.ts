import { useEffect, useState } from 'react';
import { ADMIN_API_KEY_CHANGED_EVENT, hasAdminApiKey } from '../utils/adminAccess';

export const useAdminAccess = () => {
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

    return { hasAdminKey };
};

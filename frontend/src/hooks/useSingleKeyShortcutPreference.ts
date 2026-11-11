import { useCallback, useEffect, useState } from 'react';
import {
    readSingleKeyShortcutsEnabled,
    SINGLE_KEY_SHORTCUTS_CHANGED_EVENT,
    SINGLE_KEY_SHORTCUTS_STORAGE_KEY,
    writeSingleKeyShortcutsEnabled,
} from '../utils/singleKeyShortcutPreference';

export const useSingleKeyShortcutPreference = () => {
    const [enabled, setEnabledState] = useState(readSingleKeyShortcutsEnabled);

    useEffect(() => {
        const handleSameTabChange = (event: Event) => {
            const preferenceEvent = event as CustomEvent<unknown>;
            if (typeof preferenceEvent.detail === 'boolean') {
                setEnabledState(preferenceEvent.detail);
            }
        };
        const handleStorageChange = (event: StorageEvent) => {
            if (event.storageArea && event.storageArea !== window.localStorage) return;
            if (event.key === null) {
                setEnabledState(true);
                return;
            }
            if (event.key !== SINGLE_KEY_SHORTCUTS_STORAGE_KEY) return;
            setEnabledState(event.newValue !== 'false');
        };

        window.addEventListener(
            SINGLE_KEY_SHORTCUTS_CHANGED_EVENT,
            handleSameTabChange,
        );
        window.addEventListener('storage', handleStorageChange);
        return () => {
            window.removeEventListener(
                SINGLE_KEY_SHORTCUTS_CHANGED_EVENT,
                handleSameTabChange,
            );
            window.removeEventListener('storage', handleStorageChange);
        };
    }, []);

    const setEnabled = useCallback((nextEnabled: boolean) => {
        setEnabledState(nextEnabled);
        writeSingleKeyShortcutsEnabled(nextEnabled);
    }, []);

    return { enabled, setEnabled };
};

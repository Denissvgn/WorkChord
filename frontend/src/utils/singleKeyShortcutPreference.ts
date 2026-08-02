export const SINGLE_KEY_SHORTCUTS_STORAGE_KEY = (
    'workchord.command-menu.single-key-shortcuts'
);

export const SINGLE_KEY_SHORTCUTS_CHANGED_EVENT = (
    'workchord:single-key-shortcuts-changed'
);

export const readSingleKeyShortcutsEnabled = () => {
    if (typeof window === 'undefined') return false;
    try {
        return window.localStorage.getItem(SINGLE_KEY_SHORTCUTS_STORAGE_KEY) === 'true';
    } catch {
        return false;
    }
};

export const writeSingleKeyShortcutsEnabled = (enabled: boolean) => {
    if (typeof window === 'undefined') return;
    try {
        window.localStorage.setItem(
            SINGLE_KEY_SHORTCUTS_STORAGE_KEY,
            String(enabled),
        );
    } catch {
        // The current tab still receives the in-memory preference below.
    }
    window.dispatchEvent(new CustomEvent<boolean>(
        SINGLE_KEY_SHORTCUTS_CHANGED_EVENT,
        { detail: enabled },
    ));
};

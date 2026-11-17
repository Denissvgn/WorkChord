import { create } from 'zustand';

/**
 * Where this tab remembers that a step was opened from the Get started panel. It lasts for the
 * tab only and nothing reaches the server.
 */
export const SETUP_RETURN_KEY = 'workchord-setup-return';

const tabStorage = (): Storage | undefined => {
    try {
        return typeof window === 'undefined' ? undefined : window.sessionStorage;
    } catch {
        return undefined;
    }
};

const readActive = (): boolean => {
    try {
        return tabStorage()?.getItem(SETUP_RETURN_KEY) === '1';
    } catch {
        return false;
    }
};

const writeActive = (active: boolean) => {
    try {
        const storage = tabStorage();
        if (active) storage?.setItem(SETUP_RETURN_KEY, '1');
        else storage?.removeItem(SETUP_RETURN_KEY);
    } catch {
        // Storage can be blocked; the way back then lasts until the page reloads.
    }
};

interface SetupReturn {
    /**
     * A step opened from the panel is in progress. It stays on through every page the step
     * leads to (a saved iteration putting itself in scope, Tasks and back) until Overview is
     * shown again.
     */
    active: boolean;
    start: () => void;
    finish: () => void;
}

export const useSetupReturn = create<SetupReturn>((set, get) => ({
    active: readActive(),
    start: () => {
        if (get().active) return;
        writeActive(true);
        set({ active: true });
    },
    finish: () => {
        if (!get().active) return;
        writeActive(false);
        set({ active: false });
    },
}));

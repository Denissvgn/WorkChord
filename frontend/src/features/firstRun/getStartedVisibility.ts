import { create } from 'zustand';

/** Where this browser remembers that the Get started panel was dismissed. Nothing reaches the server. */
export const GET_STARTED_DISMISSED_KEY = 'workchord-get-started-dismissed';

const browserStorage = (): Storage | undefined => {
    try {
        return typeof window === 'undefined' ? undefined : window.localStorage;
    } catch {
        return undefined;
    }
};

export const readGetStartedDismissed = (): boolean => {
    try {
        return browserStorage()?.getItem(GET_STARTED_DISMISSED_KEY) === '1';
    } catch {
        return false;
    }
};

const writeDismissed = (dismissed: boolean) => {
    try {
        const storage = browserStorage();
        if (dismissed) storage?.setItem(GET_STARTED_DISMISSED_KEY, '1');
        else storage?.removeItem(GET_STARTED_DISMISSED_KEY);
    } catch {
        // Storage can be blocked; the choice then lasts until the page reloads.
    }
};

interface GetStartedVisibility {
    /** Dismissed in this browser. */
    dismissed: boolean;
    /** Reopened from Help: shown even when every step is done, until it is closed again. */
    requested: boolean;
    dismiss: () => void;
    reopen: () => void;
}

export const useGetStartedVisibility = create<GetStartedVisibility>(set => ({
    dismissed: readGetStartedDismissed(),
    requested: false,
    dismiss: () => {
        writeDismissed(true);
        set({ dismissed: true, requested: false });
    },
    reopen: () => {
        writeDismissed(false);
        set({ dismissed: false, requested: true });
    },
}));

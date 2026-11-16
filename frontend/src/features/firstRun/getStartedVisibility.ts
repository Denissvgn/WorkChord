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

/**
 * Reopened from Help. `pending` until the steps are known; `incomplete` lasts until setup is
 * complete, when the panel hides itself as usual; `complete` (setup was already complete)
 * lasts until the panel is closed again.
 */
export type GetStartedRequest = false | 'pending' | 'incomplete' | 'complete';

interface GetStartedVisibility {
    /** Dismissed in this browser. */
    dismissed: boolean;
    requested: GetStartedRequest;
    dismiss: () => void;
    reopen: () => void;
    /** Records how far setup was when it was reopened, and ends a reopening once setup completes. */
    settleRequest: (complete: boolean) => void;
}

export const useGetStartedVisibility = create<GetStartedVisibility>((set, get) => ({
    dismissed: readGetStartedDismissed(),
    requested: false,
    dismiss: () => {
        writeDismissed(true);
        set({ dismissed: true, requested: false });
    },
    reopen: () => {
        writeDismissed(false);
        set({ dismissed: false, requested: 'pending' });
    },
    settleRequest: complete => {
        const { requested } = get();
        if (requested === 'pending') set({ requested: complete ? 'complete' : 'incomplete' });
        else if (requested === 'incomplete' && complete) set({ requested: false });
    },
}));

import { createContext, useContext } from 'react';

/**
 * Set by a page that shows one Unlock editing control for all of its protected
 * sections. Gates inside it then show their content read-only, or a short
 * locked note, without an unlock control of their own.
 */
export interface SharedUnlock {
    /** Id of the element that says why the controls are disabled. */
    noteId: string;
}

export const SharedUnlockContext = createContext<SharedUnlock | null>(null);

export const useSharedUnlock = () => useContext(SharedUnlockContext);

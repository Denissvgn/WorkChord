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

/**
 * Set by a gate around content that disables its own editing controls while
 * the admin key is missing. Such content keeps its view controls (tabs, type
 * lists, filters, expanders) usable, so readers can still look through it.
 */
export interface SettingsReadOnly {
    /** Id of the element that says why the editing controls are disabled. */
    noteId: string;
}

export const SettingsReadOnlyContext = createContext<SettingsReadOnly | null>(null);

/** Null when the content may be edited. */
export const useSettingsReadOnly = () => useContext(SettingsReadOnlyContext);

import { createContext } from 'react';

/**
 * The top bar's own row under its controls. The account menu panel opens here, so it takes its place in the page flow
 * and pushes the workspace down instead of covering the page header actions. Null outside the top bar.
 */
export const AccountMenuRowContext = createContext<HTMLElement | null>(null);

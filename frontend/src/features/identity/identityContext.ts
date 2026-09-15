import { createContext, useContext } from 'react';
import type { WorkspaceIdentity } from './identityService';

type IdentityContextValue = { identity: WorkspaceIdentity | undefined; refresh: () => void; signOut: () => Promise<void> };
export const IdentityContext = createContext<IdentityContextValue | null>(null);
export const useIdentity = () => useContext(IdentityContext);

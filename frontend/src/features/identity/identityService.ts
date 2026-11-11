import api from '../../services/api';

/** A linked profile is verified; a trusted-local session's own choice is not. */
export interface WorkProfile { id: number; display_name: string; verified?: boolean }

export interface WorkspaceIdentity {
    mode: 'managed' | 'trusted_local';
    authenticated: boolean;
    configured: boolean;
    principal: { id: number; kind: 'human' | 'agent' | 'system'; display_name: string } | null;
    profile: WorkProfile | null;
    workspace_role: 'owner' | 'operator' | 'member' | null;
    projects: Record<string, string>;
    csrf_token: string | null;
    authentication_error?: string | null;
}

export const identityService = {
    get: async (signal?: AbortSignal) => (await api.get<WorkspaceIdentity>('/auth/me', { signal })).data,
    logout: async () => { await api.post('/auth/logout'); },
    transferGuest: async () => (await api.post('/auth/transfer-guest', {})).data,
    chooseLocalProfile: async (profileId: number | null) =>
        (await api.put<{ profile: WorkProfile | null }>('/auth/local-profile', { profile_id: profileId })).data,
};

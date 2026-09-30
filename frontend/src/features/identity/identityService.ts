import api from '../../services/api';

export interface WorkspaceIdentity {
    mode: 'managed' | 'trusted_local';
    authenticated: boolean;
    configured: boolean;
    principal: { id: number; kind: 'human' | 'agent' | 'system'; display_name: string } | null;
    profile: { id: number; display_name: string } | null;
    workspace_role: 'owner' | 'operator' | 'member' | null;
    projects: Record<string, string>;
    csrf_token: string | null;
    authentication_error?: string | null;
}

export const identityService = {
    get: async (signal?: AbortSignal) => (await api.get<WorkspaceIdentity>('/auth/me', { signal })).data,
    logout: async () => { await api.post('/auth/logout'); },
    transferGuest: async () => (await api.post('/auth/transfer-guest', {})).data,
};

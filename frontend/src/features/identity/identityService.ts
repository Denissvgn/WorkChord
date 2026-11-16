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
    /** "observe" for a paired read-only reader; null with no session. */
    access?: 'full' | 'observe' | null;
    observer?: { client_label: string | null; expires_at: string; renewable_until: string } | null;
    /** Server features a client may use, such as `person-run-reads-v1`. */
    features?: string[];
}

/** One session of this account, or on a trusted-local server, one paired reader. */
export interface AccountSession {
    public_id: string;
    created_at: string;
    expires_at: string | null;
    revoked_at: string | null;
    user_agent: string | null;
    current: boolean;
    access: 'full' | 'observe';
    client_label: string | null;
}

export const identityService = {
    get: async (signal?: AbortSignal) => (await api.get<WorkspaceIdentity>('/auth/me', { signal })).data,
    logout: async () => { await api.post('/auth/logout'); },
    transferGuest: async () => (await api.post('/auth/transfer-guest', {})).data,
    chooseLocalProfile: async (profileId: number | null) =>
        (await api.put<{ profile: WorkProfile | null }>('/auth/local-profile', { profile_id: profileId })).data,
    sessions: async (signal?: AbortSignal) => (await api.get<AccountSession[]>('/auth/sessions', { signal })).data,
    revokeSession: async (publicId: string) => { await api.delete(`/auth/sessions/${encodeURIComponent(publicId)}`); },
};

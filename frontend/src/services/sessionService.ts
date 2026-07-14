import api from './api';

export interface UserSession {
    id: number;
    public_id: string;
    display_name: string;
    created_at: string;
    last_seen_at: string;
}

export const sessionService = {
    getWhoAmI: async (): Promise<UserSession> => {
        const response = await api.get<UserSession>('/session/whoami');
        return response.data;
    },
    rotate: async (): Promise<UserSession> => {
        const response = await api.post<UserSession>('/session/rotate');
        return response.data;
    },
    revoke: async (): Promise<void> => {
        await api.delete('/session');
    },
};

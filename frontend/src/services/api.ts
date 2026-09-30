import axios, { AxiosHeaders } from 'axios';
import { getAdminApiKey } from '../utils/adminAccess';
import { getAgentApiKey } from '../utils/agentAccess';

export const IDENTITY_EXPIRED_EVENT = 'workchord-identity-expired';
let csrfToken: string | null = null;
let humanSession = false;
export const setSessionIntegrity = (token: string | null, human: boolean) => {
    csrfToken = token;
    humanSession = human;
};

const api = axios.create({
    baseURL: '/api',
    withCredentials: true,
    headers: {
        'Content-Type': 'application/json',
    },
});

api.interceptors.request.use((config) => {
    const adminApiKey = getAdminApiKey();
    const agentApiKey = getAgentApiKey();
    const sendsAgentCredential = config.url?.startsWith('/agent') ?? false;
    const identityRead = config.url === '/auth/me';
    if (
        (csrfToken || adminApiKey || (agentApiKey && sendsAgentCredential))
        && (!config.headers || typeof config.headers.set !== 'function')
    ) {
        config.headers = new AxiosHeaders(config.headers);
    }
    if (adminApiKey && !identityRead && !humanSession && !(agentApiKey && sendsAgentCredential)) {
        config.headers.set('X-Admin-API-Key', adminApiKey);
    }
    if (agentApiKey && sendsAgentCredential && !humanSession) {
        config.headers.set('X-Agent-API-Key', agentApiKey);
    }
    if (csrfToken && !['get', 'head', 'options'].includes((config.method ?? 'get').toLowerCase())) {
        config.headers.set('X-CSRF-Token', csrfToken);
    }
    return config;
});

api.interceptors.response.use(response => response, error => {
    if (error.response?.status === 401 && error.config?.url !== '/auth/me' && typeof window !== 'undefined') {
        window.dispatchEvent(new Event(IDENTITY_EXPIRED_EVENT));
    }
    return Promise.reject(error);
});

export default api;

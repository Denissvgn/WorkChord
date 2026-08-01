import axios, { AxiosHeaders } from 'axios';
import { getAdminApiKey } from '../utils/adminAccess';
import { getAgentApiKey } from '../utils/agentAccess';

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
    if (
        (adminApiKey || (agentApiKey && sendsAgentCredential))
        && (!config.headers || typeof config.headers.set !== 'function')
    ) {
        config.headers = new AxiosHeaders(config.headers);
    }
    if (adminApiKey) {
        config.headers.set('X-Admin-API-Key', adminApiKey);
    }
    if (agentApiKey && sendsAgentCredential) {
        config.headers.set('X-Agent-API-Key', agentApiKey);
    }
    return config;
});

export default api;

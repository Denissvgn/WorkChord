import axios, { AxiosHeaders } from 'axios';
import { getAdminApiKey } from '../utils/adminAccess';

const api = axios.create({
    baseURL: '/api',
    withCredentials: true,
    headers: {
        'Content-Type': 'application/json',
    },
});

api.interceptors.request.use((config) => {
    const adminApiKey = getAdminApiKey();
    if (adminApiKey) {
        if (config.headers && typeof config.headers.set === 'function') {
            config.headers.set('X-Admin-API-Key', adminApiKey);
        } else {
            config.headers = new AxiosHeaders(config.headers);
            config.headers.set('X-Admin-API-Key', adminApiKey);
        }
    }
    return config;
});

export default api;

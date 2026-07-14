import { getApiErrorMessage, getApiErrorStatus } from './apiError';

export const ADMIN_API_KEY_STORAGE_KEY = 'workchord_admin_api_key';
export const ADMIN_API_KEY_CHANGED_EVENT = 'workchord-admin-api-key-changed';

export interface AdminAccessErrorMessages {
    missingOrInvalid: string;
    backendNotConfigured: string;
    fallback: string;
}

const browserSessionStorage = () => {
    if (typeof window === 'undefined') return null;
    return window.sessionStorage;
};

const notifyAdminApiKeyChanged = () => {
    if (typeof window !== 'undefined') {
        window.dispatchEvent(new Event(ADMIN_API_KEY_CHANGED_EVENT));
    }
};

export const getAdminApiKey = () => {
    try {
        return browserSessionStorage()?.getItem(ADMIN_API_KEY_STORAGE_KEY) ?? '';
    } catch {
        return '';
    }
};

export const hasAdminApiKey = () => getAdminApiKey().trim().length > 0;

export const setAdminApiKey = (apiKey: string) => {
    browserSessionStorage()?.setItem(ADMIN_API_KEY_STORAGE_KEY, apiKey);
    notifyAdminApiKeyChanged();
};

export const clearAdminApiKey = () => {
    browserSessionStorage()?.removeItem(ADMIN_API_KEY_STORAGE_KEY);
    notifyAdminApiKeyChanged();
};

export const getAdminAccessErrorMessage = (
    error: unknown,
    messages: AdminAccessErrorMessages,
) => {
    const status = getApiErrorStatus(error);
    if (status === 401) return messages.missingOrInvalid;
    if (status === 503) return messages.backendNotConfigured;
    return getApiErrorMessage(error, messages.fallback);
};

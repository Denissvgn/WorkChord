export const AGENT_API_KEY_STORAGE_KEY = 'workchord_agent_api_key';
export const AGENT_API_KEY_CHANGED_EVENT = 'workchord-agent-api-key-changed';

const browserSessionStorage = () => {
    if (typeof window === 'undefined') return null;
    return window.sessionStorage;
};

const notifyAgentApiKeyChanged = () => {
    if (typeof window !== 'undefined') {
        window.dispatchEvent(new Event(AGENT_API_KEY_CHANGED_EVENT));
    }
};

export const getAgentApiKey = () => {
    try {
        return browserSessionStorage()?.getItem(AGENT_API_KEY_STORAGE_KEY) ?? '';
    } catch {
        return '';
    }
};

// Key presence only controls whether authenticated reads should be attempted.
// The backend capability response and operation-specific 403s remain authoritative.
export const hasAgentApiKey = () => getAgentApiKey().trim().length > 0;

export const setAgentApiKey = (apiKey: string) => {
    browserSessionStorage()?.setItem(AGENT_API_KEY_STORAGE_KEY, apiKey);
    notifyAgentApiKeyChanged();
};

export const clearAgentApiKey = () => {
    browserSessionStorage()?.removeItem(AGENT_API_KEY_STORAGE_KEY);
    notifyAgentApiKeyChanged();
};

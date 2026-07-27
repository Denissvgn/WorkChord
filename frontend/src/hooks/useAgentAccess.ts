import { useEffect, useState } from 'react';
import {
    AGENT_API_KEY_CHANGED_EVENT,
    hasAgentApiKey,
} from '../utils/agentAccess';

export const useAgentAccess = () => {
    const [hasAgentKey, setHasAgentKey] = useState(hasAgentApiKey());

    useEffect(() => {
        const refreshAgentKeyState = () => setHasAgentKey(hasAgentApiKey());
        window.addEventListener(AGENT_API_KEY_CHANGED_EVENT, refreshAgentKeyState);
        window.addEventListener('storage', refreshAgentKeyState);
        return () => {
            window.removeEventListener(AGENT_API_KEY_CHANGED_EVENT, refreshAgentKeyState);
            window.removeEventListener('storage', refreshAgentKeyState);
        };
    }, []);

    return { hasAgentKey };
};

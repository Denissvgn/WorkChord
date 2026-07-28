import type { AgentTeamMaster } from '../../types/agent';

const SECRET_FIELDS = new Set([
    'api_key',
    'api_token',
    'authorization',
    'client_secret',
    'credential',
    'credentials',
    'database_url',
    'environment',
    'environment_value',
    'password',
    'private_endpoint_token',
    'private_key',
    'prompt',
    'raw_log',
    'secret',
    'secret_key',
    'token',
]);

const SECRET_VALUE_PATTERNS = [
    /-----BEGIN [A-Z0-9 ]*PRIVATE KEY-----/,
    /\bbearer\s+[a-z0-9._~+/=-]{12,}/i,
    /\bpmag_[A-Za-z0-9_-]{20,}/,
    /\bAKIA[0-9A-Z]{16}\b/,
    /[a-z][a-z0-9+.-]*:\/\/[^/@\s:]+:[^/@\s]+@/i,
];

export const assertAgentTeamMasterSecretFree = (
    value: unknown,
    path = '$',
): void => {
    if (Array.isArray(value)) {
        value.forEach((item, index) => (
            assertAgentTeamMasterSecretFree(item, `${path}[${index}]`)
        ));
        return;
    }
    if (value !== null && typeof value === 'object') {
        for (const [key, nested] of Object.entries(value)) {
            if (SECRET_FIELDS.has(key.trim().toLowerCase())) {
                throw new Error(`Secret-bearing field is not allowed at ${path}.${key}`);
            }
            assertAgentTeamMasterSecretFree(nested, `${path}.${key}`);
        }
        return;
    }
    if (
        typeof value === 'string'
        && SECRET_VALUE_PATTERNS.some(pattern => pattern.test(value))
    ) {
        throw new Error(`Credential-shaped value is not allowed at ${path}`);
    }
};

export const parseAgentTeamMasterEditor = (text: string): AgentTeamMaster => {
    const value: unknown = JSON.parse(text);
    if (value === null || Array.isArray(value) || typeof value !== 'object') {
        throw new Error('The master must be one JSON object.');
    }
    assertAgentTeamMasterSecretFree(value);
    return value as AgentTeamMaster;
};

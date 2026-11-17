import api from './api';

/** Check a candidate key without changing the credential stored in this tab. */
export const verifyAdminApiKey = async (key: string) => {
    await api.get('/scheduling-rules', { headers: { 'X-Admin-API-Key': key }, skipIdentityExpiry: true });
};

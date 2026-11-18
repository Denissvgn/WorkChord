import { act, screen, waitFor } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { AxiosError } from 'axios';
import type { AxiosResponse, InternalAxiosRequestConfig } from 'axios';
import i18n from '../../i18n/i18n';
import { createTestQueryClient, renderWithProviders } from '../../test/renderWithProviders';
import { AdminAccessPanel } from './AdminAccessPanel';
import { protectedQueryKeys } from './protectedQueryKeys';
import api, { IDENTITY_EXPIRED_EVENT, setSessionIntegrity } from '../../services/api';
import { ADMIN_API_KEY_CHANGED_EVENT, getAdminApiKey, setAdminApiKey } from '../../utils/adminAccess';
import { IdentityProvider } from '../../features/identity/IdentityProvider';
import { IdentityContext } from '../../features/identity/identityContext';
import type { WorkspaceIdentity } from '../../features/identity/identityService';

const local: WorkspaceIdentity = { mode: 'trusted_local', authenticated: false, configured: true,
    principal: null, profile: { id: 3, display_name: 'Ada' }, workspace_role: null, projects: {}, csrf_token: null };
const originalAdapter = api.defaults.adapter;
const server = vi.fn();
const respond = (config: InternalAxiosRequestConfig, status = 200, data: unknown = {}) => {
    const response: AxiosResponse = { data, status, statusText: String(status), headers: {}, config };
    if (status >= 400) throw new AxiosError('Rejected', 'ERR_BAD_REQUEST', config, null, response);
    return response;
};
const typeKey = async (user: ReturnType<typeof renderWithProviders>['user'], key: string) => {
    await user.type(screen.getByLabelText(i18n.t('settings.adminAccessField')), key);
    await user.click(screen.getByRole('button', { name: i18n.t('settings.adminAccessSave') }));
};

describe('AdminAccessPanel through the API interceptor', () => {
    beforeEach(() => {
        sessionStorage.clear();
        setSessionIntegrity(null, false);
        server.mockReset();
        server.mockImplementation(async (config: InternalAxiosRequestConfig) => respond(config, 200, config.url === '/auth/me' ? local : {}));
        api.defaults.adapter = server;
    });
    afterEach(() => { api.defaults.adapter = originalAdapter; setSessionIntegrity(null, false); });

    it('rejects a wrong key without storing it or remounting the form, and names the cause', async () => {
        server.mockImplementation(async (config: InternalAxiosRequestConfig) => respond(config, config.url === '/auth/me' ? 200 : 401, local));
        const changed = vi.fn();
        const expired = vi.fn();
        window.addEventListener(ADMIN_API_KEY_CHANGED_EVENT, changed);
        window.addEventListener(IDENTITY_EXPIRED_EVENT, expired);
        try {
            const { user } = renderWithProviders(<IdentityProvider><AdminAccessPanel /></IdentityProvider>);
            await screen.findByLabelText('Admin key');
            await typeKey(user, 'wrong-key');
            expect(await screen.findByRole('alert')).toHaveTextContent('The server rejected this key. Nothing was saved.');
            expect(screen.getByLabelText('Admin key')).toHaveValue('wrong-key');
            expect(getAdminApiKey()).toBe('');
            expect(changed).not.toHaveBeenCalled();
            expect(expired).not.toHaveBeenCalled();
            expect(server.mock.calls.find(([config]) => config.url === '/scheduling-rules')?.[0].headers.get('X-Admin-API-Key')).toBe('wrong-key');
        } finally {
            window.removeEventListener(ADMIN_API_KEY_CHANGED_EVENT, changed);
            window.removeEventListener(IDENTITY_EXPIRED_EVENT, expired);
        }
    });

    it('stores a correct key only after verification and sends it on subsequent requests', async () => {
        let accept!: () => void;
        server.mockImplementation(async (config: InternalAxiosRequestConfig) => config.url === '/scheduling-rules'
            ? new Promise(resolve => { accept = () => resolve(respond(config)); }) : respond(config, 200, local));
        const { user } = renderWithProviders(<IdentityProvider><AdminAccessPanel /></IdentityProvider>);
        await screen.findByLabelText('Admin key');
        await typeKey(user, 'correct-key');
        expect(getAdminApiKey()).toBe('');
        expect(server.mock.calls.at(-1)?.[0].headers.get('X-Admin-API-Key')).toBe('correct-key');
        await act(async () => accept());
        await waitFor(() => expect(getAdminApiKey()).toBe('correct-key'));
        await api.get('/projects');
        expect(server.mock.calls.at(-1)?.[0].headers.get('X-Admin-API-Key')).toBe('correct-key');
        expect(await screen.findByText(i18n.t('identity.adminKeyReplacesPerson'))).toBeInTheDocument();
    });

    it('checks a replacement instead of the stored key and preserves the old key on rejection', async () => {
        setAdminApiKey('existing-key');
        server.mockImplementation(async (config: InternalAxiosRequestConfig) => respond(config, 401));
        const { user } = renderWithProviders(<AdminAccessPanel />);
        await typeKey(user, 'wrong-replacement');
        expect(await screen.findByRole('alert')).toHaveTextContent(i18n.t('settings.adminAccessRejected'));
        expect(server.mock.calls[0][0].headers.get('X-Admin-API-Key')).toBe('wrong-replacement');
        expect(getAdminApiKey()).toBe('existing-key');
    });

    it.each([503, 500, 0])('does not save a key when verification is unavailable (%s)', async status => {
        server.mockImplementation(async (config: InternalAxiosRequestConfig) => {
            if (!status) throw new AxiosError('Network Error', 'ERR_NETWORK', config);
            return respond(config, status);
        });
        const { user } = renderWithProviders(<AdminAccessPanel />);
        await typeKey(user, 'unchecked-key');
        expect(await screen.findByRole('alert')).toHaveTextContent(i18n.t(status === 503 ? 'settings.adminAccessBackendNotConfigured' : 'identity.keyNotChecked'));
        expect(getAdminApiKey()).toBe('');
        expect(screen.getByLabelText('Admin key')).toHaveValue('unchecked-key');
    });

    it('purges protected caches on a verified replacement and on Lock', async () => {
        const queryClient = createTestQueryClient();
        const remove = vi.spyOn(queryClient, 'removeQueries');
        const invalidate = vi.spyOn(queryClient, 'invalidateQueries');
        const { user } = renderWithProviders(<AdminAccessPanel />, { queryClient });
        await typeKey(user, 'replacement-key');
        expect(await screen.findByText(i18n.t('settings.adminAccessAccepted'))).toBeInTheDocument();
        protectedQueryKeys.forEach(queryKey => {
            expect(remove).toHaveBeenCalledWith({ queryKey: [...queryKey] });
            expect(invalidate).toHaveBeenCalledWith({ queryKey: [...queryKey] });
        });
        remove.mockClear();
        await user.click(screen.getByRole('button', { name: i18n.t('settings.adminAccessClear') }));
        expect(getAdminApiKey()).toBe('');
        protectedQueryKeys.forEach(queryKey => expect(remove).toHaveBeenCalledWith({ queryKey: [...queryKey] }));
    });

    it.each(['owner', 'operator', 'member', null] as const)('shows role-based editing without an admin key field for signed-in %s', async role => {
        setAdminApiKey('leftover-key');
        setSessionIntegrity('csrf', true);
        const identity: WorkspaceIdentity = { ...local, mode: 'managed', authenticated: true,
            principal: { id: 7, kind: 'human', display_name: 'Ada' }, workspace_role: role };
        renderWithProviders(<IdentityContext.Provider value={{ identity, refresh: vi.fn(), signOut: vi.fn() }}><AdminAccessPanel /></IdentityContext.Provider>);
        expect(screen.getByText('Editing follows the workspace role of this account.')).toBeInTheDocument();
        expect(screen.getByRole('heading')).toHaveTextContent(role === 'owner' || role === 'operator' ? 'Editing: unlocked' : 'Editing: locked');
        expect(screen.queryByLabelText('Admin key')).not.toBeInTheDocument();
        expect(screen.queryByRole('button')).not.toBeInTheDocument();
        await api.get('/projects', { headers: { 'X-Admin-API-Key': 'explicit-key' } });
        expect(server.mock.calls.at(-1)?.[0].headers.has('X-Admin-API-Key')).toBe(false);
    });
});

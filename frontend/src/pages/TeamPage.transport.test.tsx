import { screen, waitFor, within } from '@testing-library/react';
import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { AxiosError } from 'axios';
import type { AxiosAdapter, AxiosResponse, InternalAxiosRequestConfig } from 'axios';
import type { TeamMemberProfile } from '../types/team';
import api, { IDENTITY_EXPIRED_EVENT } from '../services/api';
import { clearAdminApiKey, setAdminApiKey } from '../utils/adminAccess';
import { clearAgentApiKey, setAgentApiKey } from '../utils/agentAccess';
import { IdentityProvider } from '../features/identity/IdentityProvider';
import { renderWithProviders } from '../test/renderWithProviders';
import TeamPage from './TeamPage';

// The identity and profile reads are answered directly; the roster read goes through the real API client.
const services = vi.hoisted(() => ({
    identity: { get: vi.fn(), logout: vi.fn(), transferGuest: vi.fn(), chooseLocalProfile: vi.fn() },
    team: { getProfiles: vi.fn() },
}));
vi.mock('../features/identity/identityService', () => ({ identityService: services.identity }));
vi.mock('../services/teamService', () => ({ teamService: services.team }));

const originalAdapter = api.defaults.adapter;
const EXPIRED_TEXT = 'Your session expired. Sign in again to continue.';

/** Answers every request at the transport level with one status, so the real interceptors of the API client run. */
const answerFromServer = (status: number) => {
    const adapter = vi.fn<AxiosAdapter>(async (config: InternalAxiosRequestConfig): Promise<AxiosResponse> => {
        const response: AxiosResponse = { data: [], status, statusText: String(status), headers: {}, config };
        if (status >= 400) throw new AxiosError(`Request failed with status ${status}`, 'ERR_BAD_REQUEST', config, null, response);
        return response;
    });
    api.defaults.adapter = adapter;
    return adapter;
};

const managedSession = {
    mode: 'managed',
    authenticated: true,
    configured: true,
    principal: { id: 1, display_name: 'Ada' },
    profile: { id: 1, display_name: 'Ada' },
    workspace_role: 'member',
    projects: {},
    csrf_token: 'token',
};

const agentProfile: TeamMemberProfile = {
    id: 2, seed_key: null, display_name: 'Builder', email: null, headline: null, summary: null, notes: null,
    automation_enabled: true, profile_kind: 'agent', assignment_modes: ['execution'], skills: [], created_at: '', updated_at: '',
};

const renderTeam = () => renderWithProviders(<IdentityProvider><TeamPage /></IdentityProvider>, { initialEntries: ['/team'] });

describe('Team page roster read through the API client', () => {
    const sessionEnded = vi.fn();

    beforeEach(() => {
        vi.clearAllMocks();
        sessionStorage.clear();
        clearAdminApiKey();
        clearAgentApiKey();
        services.identity.get.mockResolvedValue(managedSession);
        services.team.getProfiles.mockResolvedValue([agentProfile]);
        window.addEventListener(IDENTITY_EXPIRED_EVENT, sessionEnded);
    });

    afterEach(() => {
        window.removeEventListener(IDENTITY_EXPIRED_EVENT, sessionEnded);
        api.defaults.adapter = originalAdapter;
        clearAdminApiKey();
        clearAgentApiKey();
    });

    it.each([
        ['a revoked agent key', () => setAgentApiKey('revoked-agent-key')],
        ['a rejected admin key', () => setAdminApiKey('rejected-admin-key')],
    ])('shows Unknown and no session-expired alert when the roster read is refused with %s', async (_name, storeKey) => {
        storeKey();
        const adapter = answerFromServer(401);
        renderTeam();

        const row = await screen.findByRole('button', { name: 'Open Builder' });
        await waitFor(() => expect(adapter).toHaveBeenCalledWith(expect.objectContaining({ url: '/agent/actors' })));
        const cells = within(row.closest('tr') as HTMLElement);
        await waitFor(() => expect(cells.getAllByText('Unknown')).toHaveLength(2));

        expect(sessionEnded).not.toHaveBeenCalled();
        expect(screen.queryByText(EXPIRED_TEXT)).not.toBeInTheDocument();
        expect(screen.queryByRole('alert')).not.toBeInTheDocument();
    });

    it('still reports an expired session for a required read', async () => {
        answerFromServer(401);
        renderTeam();
        await screen.findByRole('button', { name: 'Open Builder' });
        // The server has ended the session: a required read is refused and the identity read says so.
        services.identity.get.mockResolvedValue({ ...managedSession, authenticated: false, csrf_token: null, authentication_error: 'session_expired' });

        await expect(api.get('/tasks')).rejects.toBeInstanceOf(AxiosError);

        expect(sessionEnded).toHaveBeenCalledTimes(1);
        expect(await screen.findByText(EXPIRED_TEXT)).toBeVisible();
    });
});

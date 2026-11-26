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
import { modelAwareRoutingRoster } from '../test/fixtures/modelAwareRouting';
import type { AgentModelBinding, AgentModelCatalogEntry } from '../types/agent';

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

    it('loads Models and creates a binding through the real request set with only the saved admin key', async () => {
        services.identity.get.mockResolvedValue({
            ...managedSession, mode: 'trusted_local', principal: null, workspace_role: null,
        });
        setAdminApiKey('operator-key');
        const catalog: AgentModelCatalogEntry = {
            id: 21, key: 'reasoner', provider: 'configured-provider', configured_model_alias: 'Reasoner',
            reasoning_tier: 3, context_tier: 'large', modality_tags: ['text'], cost_tier: 'medium',
            latency_tier: 'balanced', local_first: false, enabled: true, revision: 1, last_verified_at: null,
            created_at: '', updated_at: '',
        };
        const binding: AgentModelBinding = {
            id: 31, actor_id: 11, model_catalog_id: 21, is_default: false, enabled: true,
            tool_tags: [], data_policy_tags: [], revision: 1, model_catalog_key: 'reasoner',
            selectable: true, model_catalog: catalog, live_assignment_count: 0,
            historical_assignment_count: 0, run_reference_count: 0, created_at: '', updated_at: '',
        };
        const requests: InternalAxiosRequestConfig[] = [];
        api.defaults.adapter = async config => {
            requests.push(config);
            expect(config.headers.get('X-Admin-API-Key')).toBe('operator-key');
            expect(config.headers.has('X-Agent-API-Key')).toBe(false);
            let data: unknown;
            if (config.method === 'get' && config.url === '/agent/actors') {
                expect(config.params).toEqual({ include_disabled: true });
                data = modelAwareRoutingRoster;
            } else if (config.method === 'get' && config.url === '/agent/model-catalog') {
                expect(config.params).toEqual({ include_disabled: true });
                data = [catalog];
            } else if (config.method === 'get' && config.url === '/agent/model-bindings') {
                expect(config.params).toEqual({ actor_id: undefined, include_disabled: true });
                data = [binding];
            } else if (config.method === 'post' && config.url === '/agent/model-bindings') {
                expect(JSON.parse(config.data)).toEqual({
                    actor_id: 11, model_catalog_id: 21, is_default: false, enabled: true,
                    tool_tags: [], data_policy_tags: [], revision: 1,
                });
                expect(config.headers.get('X-Agent-Rationale')).toBe('Connect the worker model');
                expect(config.headers.get('Idempotency-Key')).toBeTruthy();
                expect(config.headers.get('X-Correlation-ID')).toBeTruthy();
                data = { result: binding };
            } else {
                throw new Error(`Unexpected request: ${config.method} ${config.url}`);
            }
            return { data, status: config.method === 'post' ? 201 : 200, statusText: 'OK', headers: {}, config };
        };
        const { user } = renderWithProviders(<IdentityProvider><TeamPage /></IdentityProvider>, {
            initialEntries: ['/team?tab=models'],
        });
        expect(await screen.findByRole('heading', { name: 'Model catalog' })).toBeVisible();
        expect(screen.getAllByRole('table')).toHaveLength(2);
        expect(screen.getByText('Ada Lovelace')).toBeVisible();
        expect(screen.getAllByText('Reasoner').length).toBeGreaterThan(0);
        await user.click(within(screen.getByTestId('page-header')).getByRole('button', { name: 'Add a binding' }));
        const drawer = screen.getByRole('dialog', { name: 'Create model binding' });
        await user.selectOptions(within(drawer).getByRole('combobox', { name: 'Actor' }), '11');
        await user.selectOptions(within(drawer).getByRole('combobox', { name: 'Catalog entry' }), '21');
        await user.click(within(drawer).getByRole('button', { name: 'Create' }));
        const dialog = screen.getByRole('dialog', { name: 'Audited change controls' });
        await user.type(within(dialog).getByLabelText('Change rationale'), 'Connect the worker model');
        await user.click(within(dialog).getByRole('button', { name: 'Save' }));
        await waitFor(() => expect(screen.queryByRole('dialog', { name: 'Create model binding' })).not.toBeInTheDocument());
        expect(requests.filter(request => request.method === 'post')).toHaveLength(1);
        expect(new Set(requests.map(request => `${request.method} ${request.url}`))).toEqual(new Set([
            'get /agent/actors', 'get /agent/model-catalog', 'get /agent/model-bindings', 'post /agent/model-bindings',
        ]));
        expect(sessionEnded).not.toHaveBeenCalled();
        expect(screen.queryByText('Unable to load data')).not.toBeInTheDocument();
    });
});

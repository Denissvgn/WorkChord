import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { screen, waitFor, within } from '@testing-library/react';
import { AxiosError } from 'axios';
import type { AxiosAdapter, AxiosResponse, InternalAxiosRequestConfig } from 'axios';
import { renderWithProviders } from '../../test/renderWithProviders';
import { IdentityProvider } from './IdentityProvider';
import { IdentityBadge } from './AccountMenu';
import { AppTopNav } from '../../components/layout/AppTopNav';
import api, { IDENTITY_EXPIRED_EVENT } from '../../services/api';
import { clearAdminApiKey, hasAdminApiKey } from '../../utils/adminAccess';

const originalAdapter = api.defaults.adapter;

/**
 * Answers requests at the transport level, so the real request and response interceptors of the API client run.
 * Each reply is an HTTP status; a status of 400 or above is raised the way axios raises it.
 */
const answerFromServer = (...statuses: number[]) => {
    const adapter = vi.fn<AxiosAdapter>(async (config: InternalAxiosRequestConfig): Promise<AxiosResponse> => {
        const status = statuses.shift() ?? 200;
        const response: AxiosResponse = { data: {}, status, statusText: String(status), headers: {}, config };
        if (status >= 400) throw new AxiosError(`Request failed with status ${status}`, 'ERR_BAD_REQUEST', config, null, response);
        return response;
    });
    api.defaults.adapter = adapter;
    return adapter;
};

const service = vi.hoisted(() => ({ get: vi.fn(), logout: vi.fn(), transferGuest: vi.fn(), chooseLocalProfile: vi.fn() }));
vi.mock('./identityService', () => ({ identityService: service }));

const team = vi.hoisted(() => ({ getProfiles: vi.fn() }));
vi.mock('../../services/teamService', () => ({ teamService: team }));

// The top bar that holds the menu renders its scope and navigation summary; these keep it offline in the layout test.
const topBarMocks = vi.hoisted(() => ({
    summary: vi.fn(),
    iterations: vi.fn(),
    projects: vi.fn(),
    triage: vi.fn(),
}));
vi.mock('../planningMasters/usePlanningNavigationSummary', () => ({
    usePlanningNavigationSummary: topBarMocks.summary,
}));
vi.mock('../../services/iterationService', () => ({ iterationService: { getAll: topBarMocks.iterations } }));
vi.mock('../../services/projectService', () => ({ projectService: { getAll: topBarMocks.projects } }));
vi.mock('../../services/triageService', () => ({ triageService: { getAll: topBarMocks.triage } }));
vi.mock('../../navigation/routeModules', async importOriginal => ({
    ...await importOriginal<typeof import('../../navigation/routeModules')>(),
    warmRouteModule: vi.fn(),
}));

const localWorkspace = {
    mode: 'trusted_local',
    authenticated: false,
    configured: true,
    principal: null,
    profile: { id: 3, display_name: 'Ada' },
    workspace_role: null,
    projects: {},
    csrf_token: null,
};

const renderLocalMenu = () => renderWithProviders(<IdentityProvider>
    <IdentityBadge />
</IdentityProvider>);

const openMenu = async (user: ReturnType<typeof renderLocalMenu>['user']) => {
    await user.click(await screen.findByRole('button', { name: 'Account and access' }));
    return screen.getByRole('dialog', { name: 'Account and access' });
};

describe('account menu', () => {
    beforeEach(() => {
        vi.resetAllMocks();
        sessionStorage.clear();
        clearAdminApiKey();
        service.get.mockResolvedValue(localWorkspace);
        team.getProfiles.mockResolvedValue([
            { id: 3, display_name: 'Ada', profile_kind: 'human' },
            { id: 4, display_name: 'Grace', profile_kind: 'human' },
        ]);
    });

    afterEach(() => {
        api.defaults.adapter = originalAdapter;
        vi.restoreAllMocks();
    });

    it('shows the working profile, the sign-in state and the editing state from one menu', async () => {
        const { user } = renderLocalMenu();
        const menu = await openMenu(user);

        expect(within(menu).getByText('Working as: Ada')).toBeInTheDocument();
        expect(within(menu).getByRole('button', { name: 'Work as this person' })).toBeInTheDocument();
        expect(within(menu).getByRole('button', { name: 'Add me' })).toBeInTheDocument();
        expect(within(menu).getByText('Local workspace, not a verified sign-in')).toBeInTheDocument();
        expect(within(menu).getByText('Editing: locked')).toBeInTheDocument();
        expect(within(menu).getByRole('button', { name: 'Unlock' })).toBeInTheDocument();
        expect(within(menu).getByRole('link', { name: 'My preferences' })).toHaveAttribute('href', '/settings?tab=theme');
        expect(within(menu).getByRole('link', { name: 'Access' })).toHaveAttribute('href', '/settings?tab=access');
        expect(within(menu).queryByRole('button', { name: 'Sign out' })).not.toBeInTheDocument();
    });

    it('changes the working profile from the menu', async () => {
        service.chooseLocalProfile.mockResolvedValue({ profile: { id: 4, display_name: 'Grace' } });
        service.get.mockResolvedValueOnce(localWorkspace).mockResolvedValue({ ...localWorkspace, profile: { id: 4, display_name: 'Grace' } });
        const { user } = renderLocalMenu();
        const menu = await openMenu(user);

        await user.selectOptions(within(menu).getByLabelText('Person profile'), '4');
        await user.click(within(menu).getByRole('button', { name: 'Work as this person' }));

        expect(service.chooseLocalProfile).toHaveBeenCalledWith(4);
        // A profile change remounts the app under IdentityProvider, so the menu opens again to show the new profile.
        await waitFor(() => expect(screen.queryByRole('dialog', { name: 'Account and access' })).not.toBeInTheDocument());
        const reopened = await openMenu(user);
        expect(within(reopened).getByText('Working as: Grace')).toBeInTheDocument();
    });

    it('unlocks editing from the menu, keeps a rejected key out of storage, and locks again', async () => {
        const server = answerFromServer(401, 200);
        const sessionEnded = vi.fn();
        window.addEventListener(IDENTITY_EXPIRED_EVENT, sessionEnded);
        const { user } = renderLocalMenu();
        let menu = await openMenu(user);

        await user.click(within(menu).getByRole('button', { name: 'Unlock' }));
        await user.type(within(menu).getByLabelText('Admin key'), 'wrong-key');
        await user.click(within(menu).getByRole('button', { name: 'Unlock' }));

        // The rejection shows in place: the menu stays open and nothing is stored.
        expect(await within(menu).findByText('The server rejected this key. Nothing was saved.')).toBeInTheDocument();
        expect(hasAdminApiKey()).toBe(false);
        // A rejected key is not an expired session: the real interceptor does not report one, so no banner follows.
        expect(sessionEnded).not.toHaveBeenCalled();
        expect(screen.queryByText('Your session expired. Sign in again to continue.')).not.toBeInTheDocument();
        window.removeEventListener(IDENTITY_EXPIRED_EVENT, sessionEnded);
        const [checked] = server.mock.calls[0];
        expect(checked.url).toBe('/scheduling-rules');
        expect(checked.headers.get('X-Admin-API-Key')).toBe('wrong-key');

        await user.clear(within(menu).getByLabelText('Admin key'));
        await user.type(within(menu).getByLabelText('Admin key'), 'right-key');
        await user.click(within(menu).getByRole('button', { name: 'Unlock' }));
        await waitFor(() => expect(hasAdminApiKey()).toBe(true));
        expect(server.mock.calls[1][0].headers.get('X-Admin-API-Key')).toBe('right-key');

        // The accepted key remounts the app, so the menu opens again to show the unlocked state.
        await waitFor(() => expect(screen.queryByRole('dialog', { name: 'Account and access' })).not.toBeInTheDocument());
        menu = await openMenu(user);
        expect(within(menu).getByText('Editing: unlocked')).toBeInTheDocument();

        await user.click(within(menu).getByRole('button', { name: 'Lock' }));
        expect(hasAdminApiKey()).toBe(false);
        menu = await openMenu(user);
        expect(within(menu).getByText('Editing: locked')).toBeInTheDocument();
    });

    it('leaves editing to the workspace role for a signed-in person, with no key to unlock or lock', async () => {
        service.get.mockResolvedValue({
            mode: 'managed', authenticated: true, configured: true,
            principal: { id: 7, kind: 'human', display_name: 'Ada' }, profile: null,
            workspace_role: null, projects: { 1: 'viewer' }, csrf_token: 'csrf',
        });
        const { user } = renderLocalMenu();
        const menu = await openMenu(user);

        expect(within(menu).getByText('Sign-in')).toBeInTheDocument();
        expect(within(menu).getByText('Signed in with your team account.')).toBeInTheDocument();
        expect(within(menu).getByText('Editing: locked')).toBeInTheDocument();
        expect(within(menu).getByText('Editing follows the workspace role of this account.')).toBeInTheDocument();
        expect(within(menu).getByRole('link', { name: 'Manage roles in Team' })).toHaveAttribute('href', '/team');
        expect(within(menu).queryByRole('button', { name: 'Unlock' })).not.toBeInTheDocument();
        expect(within(menu).getByRole('button', { name: 'Sign out' })).toBeInTheDocument();
    });

    it('shows editing as unlocked by an owner role, with no Lock that could not end it', async () => {
        service.get.mockResolvedValue({
            mode: 'managed', authenticated: true, configured: true,
            principal: { id: 7, kind: 'human', display_name: 'Ada' }, profile: null,
            workspace_role: 'owner', projects: {}, csrf_token: 'csrf',
        });
        const { user } = renderLocalMenu();
        const menu = await openMenu(user);

        expect(within(menu).getByText('Editing: unlocked')).toBeInTheDocument();
        expect(within(menu).getByText('Your workspace role lets you edit without the admin key.')).toBeInTheDocument();
        expect(within(menu).queryByRole('button', { name: 'Lock' })).not.toBeInTheDocument();
    });

    it('closes on Escape and on an outside click, and returns focus to its button', async () => {
        const { user } = renderLocalMenu();
        const trigger = await screen.findByRole('button', { name: 'Account and access' });

        await user.click(trigger);
        expect(screen.getByRole('dialog', { name: 'Account and access' })).toBeInTheDocument();
        await user.keyboard('{Escape}');
        expect(screen.queryByRole('dialog', { name: 'Account and access' })).not.toBeInTheDocument();
        expect(trigger).toHaveFocus();

        await user.click(trigger);
        await user.click(document.body);
        expect(screen.queryByRole('dialog', { name: 'Account and access' })).not.toBeInTheDocument();

        await user.click(trigger);
        screen.getByRole('link', { name: 'Access' }).focus();
        await user.click(document.body);
        expect(screen.queryByRole('dialog', { name: 'Account and access' })).not.toBeInTheDocument();
        expect(trigger).toHaveFocus();
    });

    it('returns focus to its button after an outside click on another focusable control', async () => {
        const { user } = renderWithProviders(<IdentityProvider>
            <IdentityBadge />
            <button type="button">Elsewhere on the page</button>
        </IdentityProvider>);
        const trigger = await screen.findByRole('button', { name: 'Account and access' });

        await user.click(trigger);
        await user.click(screen.getByRole('button', { name: 'Elsewhere on the page' }));

        expect(screen.queryByRole('dialog', { name: 'Account and access' })).not.toBeInTheDocument();
        expect(trigger).toHaveFocus();
    });

    it('keeps a right-aligned page header action visible and clickable while the menu is open', async () => {
        topBarMocks.summary.mockReturnValue({ iterations: [], ready: { done: 0, total: 0, pct: 0 } });
        topBarMocks.iterations.mockResolvedValue([]);
        topBarMocks.projects.mockResolvedValue([]);
        topBarMocks.triage.mockResolvedValue([]);
        const onExport = vi.fn();
        const { user } = renderWithProviders(<IdentityProvider>
            <AppTopNav />
            <main>
                <header className="flex items-center justify-between">
                    <h1>Projects</h1>
                    <button type="button" onClick={onExport}>Export projects</button>
                </header>
            </main>
        </IdentityProvider>, { initialEntries: ['/projects'] });

        await user.click(await screen.findByRole('button', { name: 'Account and access' }));
        const menu = screen.getByRole('dialog', { name: 'Account and access' });
        const action = screen.getByRole('button', { name: 'Export projects' });

        // The panel opens in the top bar's own row, which is in the page flow: it is not an overlay on the workspace.
        expect(menu.closest('[data-testid="app-navbar"] .topnav-account-row')).not.toBeNull();
        expect(menu.closest('main')).toBeNull();
        expect(action).toBeVisible();
        expect(action).toBeEnabled();

        await user.click(action);
        expect(onExport).toHaveBeenCalledTimes(1);
        expect(screen.queryByRole('dialog', { name: 'Account and access' })).not.toBeInTheDocument();
    });
});

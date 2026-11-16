import { beforeEach, describe, expect, it, vi } from 'vitest';
import { screen, waitFor, within } from '@testing-library/react';
import { renderWithProviders } from '../../test/renderWithProviders';
import { IdentityProvider } from './IdentityProvider';
import { IdentityBadge } from './AccountMenu';
import { clearAdminApiKey, hasAdminApiKey } from '../../utils/adminAccess';

const service = vi.hoisted(() => ({ get: vi.fn(), logout: vi.fn(), transferGuest: vi.fn(), chooseLocalProfile: vi.fn() }));
vi.mock('./identityService', () => ({ identityService: service }));

const scheduling = vi.hoisted(() => ({ getRules: vi.fn() }));
vi.mock('../../services/schedulingRulesService', () => ({ schedulingRulesService: scheduling }));

const team = vi.hoisted(() => ({ getProfiles: vi.fn() }));
vi.mock('../../services/teamService', () => ({ teamService: team }));

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

describe('account menu', () => {
    beforeEach(() => {
        vi.resetAllMocks();
        sessionStorage.clear();
        clearAdminApiKey();
        service.get.mockResolvedValue(localWorkspace);
        team.getProfiles.mockResolvedValue([{ id: 3, display_name: 'Ada', profile_kind: 'human' }]);
        scheduling.getRules.mockResolvedValue({});
    });

    it('shows the working profile, the sign-in state and the editing state, and changes each from the menu', async () => {
        const { user } = renderLocalMenu();
        await user.click(await screen.findByRole('button', { name: 'Account and access' }));
        const menu = screen.getByRole('dialog', { name: 'Account and access' });

        expect(within(menu).getByText('Working as: Ada')).toBeInTheDocument();
        expect(within(menu).getByText('Local workspace, not a verified sign-in')).toBeInTheDocument();
        expect(within(menu).getByText('Editing: locked')).toBeInTheDocument();
        expect(within(menu).getByRole('button', { name: 'Add me' })).toBeInTheDocument();
        expect(within(menu).queryByRole('button', { name: 'Sign out' })).not.toBeInTheDocument();
        expect(within(menu).getByRole('link', { name: 'My preferences' })).toHaveAttribute('href', '/settings?tab=theme');
        expect(within(menu).getByRole('link', { name: 'Access' })).toHaveAttribute('href', '/settings?tab=access');

        await user.click(within(menu).getByRole('button', { name: 'Unlock' }));
        await user.type(within(menu).getByLabelText('Admin key'), 'operator-key');
        await user.click(within(menu).getByRole('button', { name: 'Unlock' }));
        await waitFor(() => expect(hasAdminApiKey()).toBe(true));
        expect(scheduling.getRules).toHaveBeenCalledOnce();
        // A key change remounts the app under IdentityProvider, so the menu opens again to show the new state.
        await waitFor(() => expect(screen.queryByRole('dialog', { name: 'Account and access' })).not.toBeInTheDocument());
        await user.click(await screen.findByRole('button', { name: 'Account and access' }));
        expect(screen.getByText('Editing: unlocked')).toBeInTheDocument();

        await user.click(screen.getByRole('button', { name: 'Lock' }));
        expect(hasAdminApiKey()).toBe(false);
        await user.click(await screen.findByRole('button', { name: 'Account and access' }));
        expect(screen.getByText('Editing: locked')).toBeInTheDocument();
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
});

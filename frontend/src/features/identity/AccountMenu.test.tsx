import { afterEach, beforeEach, describe, expect, it, vi } from 'vitest';
import { screen, waitFor, within } from '@testing-library/react';
import { renderWithProviders } from '../../test/renderWithProviders';
import { IdentityProvider } from './IdentityProvider';
import { IdentityBadge } from './AccountMenu';
import api from '../../services/api';
import { clearAdminApiKey, hasAdminApiKey } from '../../utils/adminAccess';

const service = vi.hoisted(() => ({ get: vi.fn(), logout: vi.fn(), transferGuest: vi.fn(), chooseLocalProfile: vi.fn() }));
vi.mock('./identityService', () => ({ identityService: service }));

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
        const check = vi.spyOn(api, 'get')
            .mockRejectedValueOnce(Object.assign(new Error('Unauthorized'), { response: { status: 401 } }))
            .mockResolvedValueOnce({ data: {} });
        const { user } = renderLocalMenu();
        let menu = await openMenu(user);

        await user.click(within(menu).getByRole('button', { name: 'Unlock' }));
        await user.type(within(menu).getByLabelText('Admin key'), 'wrong-key');
        await user.click(within(menu).getByRole('button', { name: 'Unlock' }));

        // The rejection shows in place: the menu stays open and nothing is stored.
        expect(await within(menu).findByText('The server rejected this key. Nothing was saved.')).toBeInTheDocument();
        expect(hasAdminApiKey()).toBe(false);
        expect(check).toHaveBeenLastCalledWith('/scheduling-rules', { headers: { 'X-Admin-API-Key': 'wrong-key' } });

        await user.type(within(menu).getByLabelText('Admin key'), 'right-key');
        await user.click(within(menu).getByRole('button', { name: 'Unlock' }));
        await waitFor(() => expect(hasAdminApiKey()).toBe(true));

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
});

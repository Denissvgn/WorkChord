import { beforeEach, describe, expect, it, vi } from 'vitest';
import { screen, waitFor } from '@testing-library/react';
import { renderWithProviders } from '../../test/renderWithProviders';
import { IdentityProvider, IdentityBadge } from './IdentityProvider';

const service = vi.hoisted(() => ({ get: vi.fn(), logout: vi.fn() }));
vi.mock('./identityService', () => ({ identityService: service }));

describe('signed-out navigation', () => {
    beforeEach(() => {
        vi.resetAllMocks();
        sessionStorage.clear();
        service.get.mockResolvedValue({ mode: 'managed', authenticated: true, configured: true,
            principal: { id: 7, kind: 'human', display_name: 'Ada' }, profile: null,
            workspace_role: null, projects: { 1: 'manager' }, csrf_token: 'csrf' });
        service.logout.mockResolvedValue({});
    });

    it.each([
        ['/mobile/connect?request=' + 'r'.repeat(43), '/mobile/connect?request=' + 'r'.repeat(43)],
        ['/tasks?project_id=1', '/'],
        ['/mobile/connect?request=invalid', '/'],
    ])('clears private drafts before leaving %s', async (route, destination) => {
        sessionStorage.setItem('workchord-draft:7:private', 'private input');
        const navigate = vi.fn(() => expect(sessionStorage.getItem('workchord-draft:7:private')).toBeNull());
        const { user } = renderWithProviders(<IdentityProvider navigateAfterSignOut={navigate}>
            <IdentityBadge />
        </IdentityProvider>, { initialEntries: [route] });
        await screen.findByText('Ada');
        await user.click(screen.getByLabelText('Account and access'));
        await user.click(screen.getByRole('button', { name: 'Sign out' }));
        await waitFor(() => expect(navigate).toHaveBeenCalledWith(destination));
        expect(service.logout).toHaveBeenCalledOnce();
    });
});

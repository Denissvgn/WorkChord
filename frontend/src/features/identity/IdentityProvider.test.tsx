import { beforeEach, describe, expect, it, vi } from 'vitest';
import { screen, waitFor } from '@testing-library/react';
import { renderWithProviders } from '../../test/renderWithProviders';
import { IdentityProvider, IdentityBadge } from './IdentityProvider';
import { useQueryClient } from '@tanstack/react-query';
import type { QueryClient } from '@tanstack/react-query';
import { act } from '@testing-library/react';
import { planningNavigationSummaryKey } from '../planningMasters/usePlanningNavigationSummary';
import { useEffect } from 'react';

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

    it('invalidates planning navigation on the identity-scoped workspace client', async () => {
        let workspaceClient: QueryClient | undefined;
        const CaptureClient = () => {
            const client = useQueryClient();
            useEffect(() => { workspaceClient = client; }, [client]);
            return <IdentityBadge />;
        };
        const { queryClient: outerClient } = renderWithProviders(<IdentityProvider>
            <CaptureClient />
        </IdentityProvider>);
        await screen.findByText('Ada');
        expect(workspaceClient).toBeDefined();
        expect(workspaceClient).not.toBe(outerClient);
        const client = workspaceClient!;
        client.setQueryData(planningNavigationSummaryKey(7), { task_count: 3 });
        client.setQueryData(['tasks', 7], []);
        await act(async () => { await client.invalidateQueries({ queryKey: ['tasks', 7] }); });
        expect(client.getQueryState(planningNavigationSummaryKey(7))?.isInvalidated).toBe(true);
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

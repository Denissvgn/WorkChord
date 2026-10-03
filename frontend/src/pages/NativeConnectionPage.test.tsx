import { beforeEach, describe, expect, it, vi } from 'vitest';
import { screen, waitFor } from '@testing-library/react';
import { renderWithProviders } from '../test/renderWithProviders';
import { IdentityContext } from '../features/identity/identityContext';
import NativeConnectionPage from './NativeConnectionPage';

const service = vi.hoisted(() => ({ get: vi.fn(), post: vi.fn() }));
vi.mock('../services/api', () => ({ default: service }));

const request = 'r'.repeat(43);
const content = (principal = 1) => <IdentityContext.Provider value={{ identity: {
    mode: 'managed', authenticated: true, configured: true, principal: { id: principal, kind: 'human', display_name: principal === 1 ? 'Sam' : 'Ada' },
    profile: null, workspace_role: null, projects: {}, csrf_token: 'csrf',
}, refresh: vi.fn(), signOut: async () => undefined }}><NativeConnectionPage /></IdentityContext.Provider>;
const renderPage = () => renderWithProviders(content(),
{ initialEntries: [`/mobile/connect?request=${request}`] });

describe('native connection consent', () => {
    beforeEach(() => {
        vi.resetAllMocks();
        service.get.mockResolvedValue({ data: { verification_code: 'ABCD-EFGH', expires_at: '2026-10-03T12:00:00Z', approved: false } });
        service.post.mockResolvedValue({ data: { approved: true } });
    });

    it('requires explicit code confirmation and shows the account before approval', async () => {
        const { user } = renderPage();
        await screen.findByText('ABCD-EFGH');
        expect(screen.getByText('Your device will sign in as Sam.')).toBeInTheDocument();
        const button = screen.getByRole('button', { name: 'Approve connection' });
        expect(button).toBeDisabled();
        await user.click(screen.getByRole('checkbox'));
        await user.click(button);
        await screen.findByText('Connection approved. Return to your device and check the connection.');
        expect(service.post).toHaveBeenCalledWith(`/auth/native-connections/${request}/approve`, { verification_code: 'ABCD-EFGH' });
    });

    it('keeps failed approval recoverable without claiming success', async () => {
        service.post.mockRejectedValue(new Error('Connection expired'));
        const { user } = renderPage();
        await screen.findByText('ABCD-EFGH');
        await user.click(screen.getByRole('checkbox'));
        await user.click(screen.getByRole('button', { name: 'Approve connection' }));
        await waitFor(() => expect(screen.getByRole('alert')).toBeInTheDocument());
        expect(screen.getByRole('button', { name: 'Approve connection' })).toBeEnabled();
        expect(screen.queryByText('Connection approved. Return to your device and check the connection.')).not.toBeInTheDocument();
    });

    it('requires confirmation again after the signed-in account changes', async () => {
        const { user, rerender } = renderPage();
        await screen.findByText('ABCD-EFGH');
        await user.click(screen.getByRole('checkbox'));
        expect(screen.getByRole('button', { name: 'Approve connection' })).toBeEnabled();
        rerender(content(2));
        await screen.findByText('Your device will sign in as Ada.');
        expect(screen.getByRole('checkbox')).not.toBeChecked();
        expect(screen.getByRole('button', { name: 'Approve connection' })).toBeDisabled();
    });
});

import { beforeEach, describe, expect, it, vi } from 'vitest';
import { screen } from '@testing-library/react';
import { renderWithProviders } from '../../test/renderWithProviders';
import { IdentityContext } from '../../features/identity/identityContext';
import type { WorkspaceIdentity } from '../../features/identity/identityService';
import { ConnectedReadersPanel } from './ConnectedReadersPanel';

const service = vi.hoisted(() => ({ get: vi.fn(), delete: vi.fn() }));
vi.mock('../../services/api', () => ({ default: service }));

const person: WorkspaceIdentity = {
    mode: 'managed', authenticated: true, configured: true, principal: { id: 1, kind: 'human', display_name: 'Sam' },
    profile: null, workspace_role: null, projects: {}, csrf_token: 'csrf', access: 'full', observer: null,
};
const render = (identity: WorkspaceIdentity = person) => renderWithProviders(
    <IdentityContext.Provider value={{ identity, refresh: vi.fn(), signOut: async () => undefined }}><ConnectedReadersPanel /></IdentityContext.Provider>);
const later = new Date(Date.now() + 3_600_000).toISOString();
const row = (id: string, overrides: Record<string, unknown> = {}) => ({
    public_id: id, created_at: '2026-11-15T10:00:00Z', expires_at: later, revoked_at: null, user_agent: null,
    current: false, access: 'observe', client_label: `Reader ${id}`, ...overrides,
});

describe('connected readers', () => {
    beforeEach(() => {
        vi.resetAllMocks();
        service.get.mockResolvedValue({ data: [
            row('a'), row('b', { access: 'full', client_label: null }), row('c', { revoked_at: '2026-11-15T11:00:00Z' }),
            row('d', { expires_at: '2026-01-01T00:00:00Z' }), row('e', { client_label: null }),
        ] });
        service.delete.mockResolvedValue({ data: { revoked: true } });
    });

    it('lists only live read-only readers and revokes one', async () => {
        const { user } = render();
        await screen.findByText('Reader a');
        expect(screen.getByText('Unnamed reader')).toBeInTheDocument();
        expect(screen.queryByText('Reader c')).not.toBeInTheDocument();
        expect(screen.queryByText('Reader d')).not.toBeInTheDocument();
        expect(screen.getAllByRole('button', { name: /^Revoke / })).toHaveLength(2);
        await user.click(screen.getByRole('button', { name: 'Revoke Reader a' }));
        await screen.findByText('Reader a was revoked.');
        expect(service.delete).toHaveBeenCalledWith('/auth/sessions/a');
    });

    it('says when no reader is connected', async () => {
        service.get.mockResolvedValue({ data: [row('b', { access: 'full' })] });
        render();
        await screen.findByText('No readers are connected.');
    });

    it('stays hidden for a reader and for a signed-out managed browser', () => {
        render({ ...person, access: 'observe' });
        expect(screen.queryByText('Connected readers')).not.toBeInTheDocument();
        render({ ...person, authenticated: false, principal: null, access: null });
        expect(screen.queryByText('Connected readers')).not.toBeInTheDocument();
        expect(service.get).not.toHaveBeenCalled();
    });
});

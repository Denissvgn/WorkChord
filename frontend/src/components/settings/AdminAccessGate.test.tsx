import { describe, expect, it, vi } from 'vitest';
import { screen } from '@testing-library/react';
import { renderWithProviders } from '../../test/renderWithProviders';
import { IdentityContext } from '../../features/identity/identityContext';
import type { WorkspaceIdentity } from '../../features/identity/identityService';
import { AdminAccessGate } from './AdminAccessGate';

vi.mock('./AdminAccessPanel', () => ({ AdminAccessPanel: () => <p>Admin key form</p> }));

const identity = (overrides: Partial<WorkspaceIdentity>): WorkspaceIdentity => ({
    mode: 'trusted_local', authenticated: false, configured: false, principal: null, profile: null,
    workspace_role: null, projects: {}, csrf_token: null, ...overrides,
});
const renderGate = (value: WorkspaceIdentity, readable = true) => renderWithProviders(
    <IdentityContext.Provider value={{ identity: value, refresh: vi.fn(), signOut: async () => undefined }}>
        <AdminAccessGate showPanel={false} readable={readable}><label>Rule <input defaultValue="Weekdays" /></label></AdminAccessGate>
    </IdentityContext.Provider>);

describe('admin access gate', () => {
    it('shows a readable panel read-only and takes the key in place', async () => {
        const { user } = renderGate(identity({}));
        expect(screen.getByRole('textbox', { name: 'Rule' })).toBeDisabled();
        expect(screen.getByText('Read-only')).toBeInTheDocument();
        expect(screen.queryByText('Admin key form')).toBeNull();
        await user.click(screen.getByRole('button', { name: 'Unlock editing' }));
        expect(screen.getByText('Admin key form')).toBeInTheDocument();
    });

    it('keeps the gate for people who cannot read without the key', () => {
        renderGate(identity({ mode: 'managed', authenticated: true, principal: { id: 3, kind: 'human', display_name: 'Guest' } }));
        expect(screen.queryByRole('textbox', { name: 'Rule' })).toBeNull();
        expect(screen.getByRole('heading', { name: 'Admin key required' })).toBeInTheDocument();
    });

    it('keeps the gate for panels that are not marked readable', () => {
        renderGate(identity({}), false);
        expect(screen.queryByRole('textbox', { name: 'Rule' })).toBeNull();
    });
});

import { expect, it, vi } from 'vitest';
import { screen, waitFor } from '@testing-library/react';
import { renderWithProviders } from '../../test/renderWithProviders';
import { IdentityContext } from '../../features/identity/identityContext';
import { TimeEntriesReport } from './TimeEntriesReport';
const capability = vi.hoisted(() => vi.fn());
vi.mock('../../services/timeEntryService', () => ({ timeEntryService: { capabilities: capability } }));
it('shows localized capability failure and retries without rendering private data', async () => {
    capability.mockRejectedValueOnce(new Error('Capability read failed')).mockResolvedValueOnce({ schema_version: 1, enabled: false });
    const { user } = renderWithProviders(<IdentityContext.Provider value={{ identity: {
        mode: 'managed', authenticated: true, configured: true, principal: { id: 1, kind: 'human', display_name: 'Sam' },
        profile: null, workspace_role: 'member', projects: { '2': 'manager' }, csrf_token: null,
    }, refresh: vi.fn(), signOut: async () => undefined }}><TimeEntriesReport projectId={2} /></IdentityContext.Provider>);
    expect(await screen.findByRole('alert')).toHaveTextContent('Could not load the time report.');
    await user.click(screen.getByRole('button', { name: /retry/i }));
    await waitFor(() => expect(capability).toHaveBeenCalledTimes(2));
    await waitFor(() => expect(screen.queryByRole('alert')).not.toBeInTheDocument());
    expect(screen.queryByRole('table')).not.toBeInTheDocument();
});

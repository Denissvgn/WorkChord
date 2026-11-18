import { afterEach, describe, expect, it, vi } from 'vitest';
import { act, screen, waitFor } from '@testing-library/react';
import { Link, useLocation } from 'react-router-dom';
import { renderWithProviders } from '../../test/renderWithProviders';
import { FirstRunLanding } from '../firstRun/FirstRunLanding';
import { clearAdminApiKey, setAdminApiKey } from '../../utils/adminAccess';
import { IdentityProvider } from './IdentityProvider';

vi.mock('./identityService', () => ({ identityService: { get: vi.fn(async () => ({ mode: 'trusted_local', authenticated: false,
    configured: false, principal: null, profile: null, workspace_role: null, projects: {}, csrf_token: null })) } }));
vi.mock('../../services/projectService', () => ({ projectService: { getAll: vi.fn(async () => []) } }));

const Where = () => <><p data-testid="where">{useLocation().pathname}</p><Link to="/team/connect">Open Connect</Link></>;

describe('admin key in a workspace with no project', () => {
    afterEach(() => sessionStorage.clear());

    it('keeps the browser on Team Connect after the key is saved or cleared', async () => {
        const { user } = renderWithProviders(<IdentityProvider><FirstRunLanding /><Where /></IdentityProvider>, { initialEntries: ['/'] });
        // Open Team Connect from inside the app, as the operator does before saving the key.
        await user.click(await screen.findByRole('link', { name: 'Open Connect' }));
        expect(screen.getByTestId('where')).toHaveTextContent('/team/connect');
        // Saving the key rebuilds the app; the guard must not send the browser to Overview.
        act(() => setAdminApiKey('key'));
        await act(async () => { await new Promise(resolve => setTimeout(resolve, 100)); });
        expect(screen.getByTestId('where')).toHaveTextContent('/team/connect');
        act(() => clearAdminApiKey());
        await act(async () => { await new Promise(resolve => setTimeout(resolve, 100)); });
        await waitFor(() => expect(screen.getByTestId('where')).toHaveTextContent('/team/connect'));
    });
});

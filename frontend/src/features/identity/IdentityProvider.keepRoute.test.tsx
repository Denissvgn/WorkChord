import { afterEach, beforeEach, describe, expect, it } from 'vitest';
import { act, screen, waitFor } from '@testing-library/react';
import { Link, Route, Routes, useLocation } from 'react-router-dom';
import { AxiosError } from 'axios';
import type { AxiosResponse, InternalAxiosRequestConfig } from 'axios';
import api, { setSessionIntegrity } from '../../services/api';
import { renderWithProviders } from '../../test/renderWithProviders';
import TeamPage from '../../pages/TeamPage';
import { FirstRunLanding } from '../firstRun/FirstRunLanding';
import { clearAdminApiKey, getAdminApiKey } from '../../utils/adminAccess';
import { IdentityProvider } from './IdentityProvider';

const local = { mode: 'trusted_local', authenticated: false, configured: true, principal: null,
    profile: null, workspace_role: null, projects: {}, csrf_token: null };
const originalAdapter = api.defaults.adapter;
const respond = (config: InternalAxiosRequestConfig, status = 200, data: unknown = {}) => {
    const response: AxiosResponse = { data, status, statusText: String(status), headers: {}, config };
    if (status >= 400) throw new AxiosError('Rejected', 'ERR_BAD_REQUEST', config, null, response);
    return response;
};

const Where = () => {
    const location = useLocation();
    return <><p data-testid="where">{location.pathname + location.search}</p><Link to="/team?tab=connect">Open Connect</Link></>;
};

// A workspace with no project: the first-run guard would send a fresh visit to Overview.
describe('admin key in a workspace with no project', () => {
    beforeEach(() => {
        sessionStorage.clear();
        setSessionIntegrity(null, false);
        api.defaults.adapter = async (config: InternalAxiosRequestConfig) => {
            if (config.url === '/auth/me') return respond(config, 200, local);
            if (config.url === '/projects/page') return respond(config, 200, { items: [], has_more: false, next_after_id: null, upper_id: 0 });
            if (config.url === '/scheduling-rules') return respond(config, 200, {});
            return respond(config, 500);
        };
    });
    afterEach(() => { api.defaults.adapter = originalAdapter; setSessionIntegrity(null, false); clearAdminApiKey(); });

    it('stays on Team Connect, query string included, after the key is saved and after it is cleared', async () => {
        const { user } = renderWithProviders(<IdentityProvider>
            <FirstRunLanding />
            <Where />
            <Routes><Route path="/team" element={<TeamPage />} /><Route path="/" element={<p>Overview</p>} /></Routes>
        </IdentityProvider>, { initialEntries: ['/'] });
        // Reached from inside the app, as the operator does; a first visit would be sent to Overview.
        await user.click(await screen.findByRole('link', { name: 'Open Connect' }));
        expect(screen.getByTestId('where')).toHaveTextContent('/team?tab=connect');
        await user.click(await screen.findByRole('button', { name: 'Unlock editing' }));
        await user.type(await screen.findByLabelText('Admin key'), 'correct-key');
        await user.click(screen.getByRole('button', { name: 'Save key' }));
        await waitFor(() => expect(getAdminApiKey()).toBe('correct-key'));
        await act(async () => { await new Promise(resolve => setTimeout(resolve, 150)); });
        expect(screen.getByTestId('where')).toHaveTextContent('/team?tab=connect');
        expect(screen.queryByText('Overview')).not.toBeInTheDocument();
        act(() => clearAdminApiKey());
        await act(async () => { await new Promise(resolve => setTimeout(resolve, 150)); });
        expect(screen.getByTestId('where')).toHaveTextContent('/team?tab=connect');
    });
});

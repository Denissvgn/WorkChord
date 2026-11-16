import type { ReactNode } from 'react';
import { render, screen } from '@testing-library/react';
import { MemoryRouter, useLocation } from 'react-router-dom';
import { describe, expect, it, vi } from 'vitest';
import App from './App';

// The app's own route table, redirect wrapper and switches run unchanged; only the
// shell and the destination pages are replaced, so the test reads where routing lands.
vi.mock('./components/layout/AppShell', () => ({ AppShell: ({ children }: { children: ReactNode }) => <>{children}</> }));
vi.mock('./pages/TeamPage', () => ({
    default: function TeamLocation() {
        const location = useLocation();
        return <p data-testid="team-location">{location.pathname + location.search + location.hash}</p>;
    },
}));
vi.mock('./pages/AgentTeamSetupMasterPage', () => ({ default: () => <p>Old agent team setup page</p> }));

const renderAt = (entry: string) => render(<MemoryRouter initialEntries={[entry]}><App /></MemoryRouter>);

describe('agent team setup legacy route', () => {
    it('opens Team on the Connect tab', async () => {
        renderAt('/agent-team/setup');
        expect(await screen.findByTestId('team-location')).toHaveTextContent(/^\/team\?tab=connect$/);
        expect(screen.queryByText('Old agent team setup page')).not.toBeInTheDocument();
    });

    it('keeps query parameters and the hash', async () => {
        renderAt('/agent-team/setup?return=%2Fplan&project=3#advanced');
        expect(await screen.findByTestId('team-location')).toHaveTextContent(/^\/team\?return=%2Fplan&project=3&tab=connect#advanced$/);
        expect(screen.queryByText('Old agent team setup page')).not.toBeInTheDocument();
    });
});

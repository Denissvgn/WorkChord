import { screen } from '@testing-library/react';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import i18n from '../i18n/i18n';
import { renderWithProviders } from '../test/renderWithProviders';
import type { AgentTeamStatus } from '../types/agent';
import AgentTeamSetupMasterPage from './AgentTeamSetupMasterPage';

const agentServiceMock = vi.hoisted(() => ({
    getAgentTeamStatus: vi.fn(),
    validateAgentTeamMaster: vi.fn(),
    planAgentTeamMaster: vi.fn(),
    applyAgentTeamAction: vi.fn(),
}));
const useAdminAccessMock = vi.hoisted(() => vi.fn());

vi.mock('../services/agentService', () => ({
    agentService: agentServiceMock,
}));
vi.mock('../hooks/useAdminAccess', () => ({
    useAdminAccess: useAdminAccessMock,
}));

const statusFixture: AgentTeamStatus = {
    schema_version: 'agent-team-status-v1',
    topology_key: 'delivery-team',
    topology_revision: 4,
    manifest_digest: 'a'.repeat(64),
    topology_state: 'blocked',
    runtime_ready: false,
    availability: 'availability_unknown',
    blocker_codes: ['minimum_workers_not_runtime_ready'],
    steps: [{
        id: 'authority',
        state: 'done',
        blocker_codes: [],
        next_action: null,
    }, {
        id: 'workers',
        state: 'blocked',
        blocker_codes: ['minimum_workers_not_runtime_ready'],
        next_action: 'Acknowledge the worker runtime',
    }],
    members: [],
    pending_action_ids: [],
    can_mutate: false,
    next_action: 'Acknowledge the worker runtime',
};

describe('AgentTeamSetupMasterPage authority and readiness', () => {
    beforeEach(() => {
        agentServiceMock.getAgentTeamStatus.mockReset();
        agentServiceMock.getAgentTeamStatus.mockResolvedValue(statusFixture);
        useAdminAccessMock.mockReset();
    });

    it('shows server readiness but no mutation actions to a PM', async () => {
        useAdminAccessMock.mockReturnValue({ hasAdminKey: false });

        renderWithProviders(<AgentTeamSetupMasterPage />);

        expect(await screen.findByText('delivery-team')).toBeVisible();
        expect(
            screen.getAllByText('Acknowledge the worker runtime').length,
        ).toBeGreaterThan(0);
        expect(screen.queryByRole('button', {
            name: i18n.t('agentTeamSetup.import'),
        })).not.toBeInTheDocument();
        expect(screen.queryByRole('button', {
            name: i18n.t('agentTeamSetup.validate'),
        })).not.toBeInTheDocument();
        expect(screen.getByText(
            i18n.t('settings.adminAccessProtectedTitle'),
        )).toBeVisible();
    });

    it('shows the labeled secret-free editor and exact planning actions to an operator', async () => {
        useAdminAccessMock.mockReturnValue({ hasAdminKey: true });
        agentServiceMock.getAgentTeamStatus.mockResolvedValue({
            ...statusFixture,
            can_mutate: true,
        });

        renderWithProviders(<AgentTeamSetupMasterPage />);

        expect(await screen.findByRole('textbox', {
            name: i18n.t('agentTeamSetup.secretFreeJson'),
        })).toBeEnabled();
        expect(screen.getByRole('button', {
            name: i18n.t('agentTeamSetup.import'),
        })).toBeEnabled();
        expect(screen.getByRole('button', {
            name: i18n.t('agentTeamSetup.validate'),
        })).toBeEnabled();
        expect(screen.queryByText(/api_key/i)).not.toBeInTheDocument();
    });
});

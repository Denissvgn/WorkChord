import { fireEvent, screen } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
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

    it('requires the current server action and explicit confirmation before apply', async () => {
        const user = userEvent.setup();
        useAdminAccessMock.mockReturnValue({ hasAdminKey: true });
        agentServiceMock.getAgentTeamStatus.mockResolvedValue({
            ...statusFixture,
            can_mutate: true,
        });
        agentServiceMock.validateAgentTeamMaster.mockResolvedValue({
            schema_version: 'agent-team-validation-v1',
            valid: true,
            manifest_digest: 'b'.repeat(64),
            normalized_manifest: {
                schema_version: 'agent-team-master-v1',
                topology_key: 'delivery-team',
            },
            blocker_codes: [],
        });
        agentServiceMock.planAgentTeamMaster.mockResolvedValue({
            schema_version: 'agent-team-reconciliation-plan-v1',
            topology_key: 'delivery-team',
            expected_topology_revision: 4,
            manifest_digest: 'b'.repeat(64),
            plan_digest: 'c'.repeat(64),
            blocker_codes: [],
            actions: [{
                action_id: 'safe-update-worker',
                action_digest: 'd'.repeat(64),
                reconciliation_class: 'safe_update',
                operation: 'update_member',
                actor_key: 'backend-worker',
                target_actor_id: 9,
                expected_object_revision: 2,
                expected_actor_revision: 4,
                before: null,
                after: null,
                preconditions: {},
                blocker_code: null,
                requires_explicit_confirmation: true,
                authority_change: true,
            }],
        });
        agentServiceMock.applyAgentTeamAction.mockResolvedValue({
            schema_version: 'agent-team-apply-receipt-v1',
            apply_id: 'e'.repeat(32),
            topology_key: 'delivery-team',
            manifest_digest: 'b'.repeat(64),
            plan_digest: 'c'.repeat(64),
            expected_topology_revision: 4,
            resulting_topology_revision: 5,
            status: 'completed',
            replayed: false,
            receipts: [],
            pending_action_ids: [],
            blocker_codes: [],
        });

        renderWithProviders(<AgentTeamSetupMasterPage />);

        const editor = await screen.findByRole('textbox', {
            name: i18n.t('agentTeamSetup.secretFreeJson'),
        });
        fireEvent.change(editor, {
            target: {
                value: JSON.stringify({
                    schema_version: 'agent-team-master-v1',
                    topology_key: 'delivery-team',
                }),
            },
        });
        await user.click(screen.getByRole('button', {
            name: i18n.t('agentTeamSetup.validate'),
        }));
        await user.click(await screen.findByRole('button', {
            name: i18n.t('agentTeamSetup.dryRun'),
        }));

        const apply = await screen.findByRole('button', {
            name: i18n.t('agentTeamSetup.applyAction'),
        });
        expect(apply).toBeDisabled();
        await user.click(screen.getByRole('checkbox', {
            name: i18n.t('agentTeamSetup.confirmAction'),
        }));
        expect(apply).toBeEnabled();
        await user.click(apply);

        expect(agentServiceMock.applyAgentTeamAction).toHaveBeenCalledWith(
            expect.objectContaining({ topology_key: 'delivery-team' }),
            expect.objectContaining({ plan_digest: 'c'.repeat(64) }),
            'safe-update-worker',
            true,
            expect.objectContaining({
                rationale: i18n.t('agentTeamSetup.defaultRationale'),
            }),
        );
        expect(await screen.findByText(
            new RegExp(`${'e'.repeat(32)}.*completed.*5`),
        )).toBeVisible();
    });

    it('renders stale and blocked server failures as an accessible alert', async () => {
        useAdminAccessMock.mockReturnValue({ hasAdminKey: true });
        agentServiceMock.getAgentTeamStatus.mockRejectedValue(
            new Error('agent_team_topology_revision_conflict'),
        );

        renderWithProviders(<AgentTeamSetupMasterPage />);

        const alert = await screen.findByRole('alert');
        expect(alert).toHaveTextContent(
            'agent_team_topology_revision_conflict',
        );
        expect(alert).toHaveTextContent(
            i18n.t('agentTeamSetup.errorTitle'),
        );
    });
});

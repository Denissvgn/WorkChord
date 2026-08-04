import { act, fireEvent, screen, waitFor, within } from '@testing-library/react';
import userEvent from '@testing-library/user-event';
import { beforeEach, describe, expect, it, vi } from 'vitest';
import i18n from '../i18n/i18n';
import { renderWithProviders } from '../test/renderWithProviders';
import {
    accessibleNameViolations,
    summaryNameViolations,
} from '../test/accessibilityInvariants';
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

const runtimeMemberFixture = (
    actorKey: string,
    actorId: number,
): AgentTeamStatus['members'][number] => ({
    actor_key: actorKey,
    actor_id: actorId,
    actor_name: actorKey,
    display_name: 'Shared Worker Name',
    role: 'worker',
    desired: true,
    configured: true,
    lifecycle_state: 'connected',
    enabled: true,
    profile_key: 'backend',
    profile_revision: 'profile-rev-4',
    binding_revisions: { balanced: 3 },
    skill_package: {
        name: 'workchord-worker',
        version: '1.2.0',
        sha256: 'b'.repeat(64),
    },
    package_acknowledged: true,
    credential_delivery_state: 'delivered',
    connection_state: 'stale',
    last_seen_at: '2026-08-04T09:30:00Z',
    queued_assignments: 2,
    accepted_assignments: 1,
    running_runs: 0,
    runtime_ready: false,
    availability: 'availability_unknown',
    blocker_codes: ['runtime_observation_stale'],
    handoff: {
        schema_version: 'agent-team-runtime-handoff-v1',
        topology_key: 'delivery-team',
        topology_revision: 4,
        actor_key: actorKey,
        actor_id: actorId,
        role: 'worker',
        server_url: `https://agents.example.test/${actorKey}`,
        required_server_features: ['assignments'],
        skill_package: {
            name: 'workchord-worker',
            version: '1.2.0',
            sha256: 'b'.repeat(64),
        },
        profile_key: 'backend',
        profile_revision: 'profile-rev-4',
        model_binding_revisions: { balanced: 3 },
        supported_assignment_modes: ['execute'],
        startup_instructions: ['Start the worker'],
        credential_ref: `vault://workchord/${actorKey}`,
    },
});

describe('AgentTeamSetupMasterPage authority and readiness', () => {
    beforeEach(() => {
        agentServiceMock.getAgentTeamStatus.mockReset();
        agentServiceMock.getAgentTeamStatus.mockResolvedValue(statusFixture);
        useAdminAccessMock.mockReset();
    });

    it('does not invent setup completion before status is confirmed', () => {
        useAdminAccessMock.mockReturnValue({ hasAdminKey: false });
        agentServiceMock.getAgentTeamStatus.mockReturnValue(new Promise(() => {}));

        renderWithProviders(<AgentTeamSetupMasterPage />);

        const readinessRail = screen.getByRole('complementary', {
            name: i18n.t('agentTeamSetup.readinessTitle'),
        });
        expect(within(readinessRail).getByRole('heading', {
            level: 2,
            name: i18n.t('agentTeamSetup.readinessTitle'),
        })).toBeVisible();
        expect(within(readinessRail).queryByRole('progressbar')).not.toBeInTheDocument();
        expect(readinessRail.querySelectorAll('.step-item')).toHaveLength(0);
        expect(readinessRail).toHaveTextContent(
            i18n.t('agentTeamSetup.statusScopes.checking'),
        );
    });

    it('separates configured topology, read-only authority, and blocked runtime for a PM', async () => {
        useAdminAccessMock.mockReturnValue({ hasAdminKey: false });

        renderWithProviders(<AgentTeamSetupMasterPage />);

        expect(await screen.findByText('delivery-team')).toBeVisible();
        const scopes = screen.getByLabelText(
            i18n.t('agentTeamSetup.statusScopes.label'),
        );
        expect(scopes).toHaveTextContent(
            i18n.t('agentTeamSetup.statusScopes.topology.title'),
        );
        expect(scopes).toHaveTextContent(
            i18n.t('agentTeamSetup.statusScopes.topology.states.configured'),
        );
        expect(scopes).toHaveTextContent(
            i18n.t('agentTeamSetup.statusScopes.authority.title'),
        );
        expect(scopes).toHaveTextContent(
            i18n.t('agentTeamSetup.statusScopes.authority.states.readOnly'),
        );
        expect(scopes).toHaveTextContent(
            i18n.t('agentTeamSetup.statusScopes.runtime.title'),
        );
        expect(scopes).toHaveTextContent(
            i18n.t('agentTeamSetup.statusScopes.runtime.states.blocked'),
        );
        expect(screen.queryByRole('button', {
            name: i18n.t('agentTeamSetup.import'),
        })).not.toBeInTheDocument();
        expect(screen.queryByRole('button', {
            name: i18n.t('agentTeamSetup.validate'),
        })).not.toBeInTheDocument();
        expect(screen.getByText(
            i18n.t('settings.adminAccessProtectedTitle'),
        )).toBeVisible();
        expect(screen.getByRole('heading', {
            level: 3,
            name: i18n.t('settings.adminAccessProtectedTitle'),
        })).toBeVisible();
        expect(screen.getByRole('heading', {
            level: 3,
            name: i18n.t('settings.adminAccessTitle'),
        })).toBeVisible();
    });

    it('keeps last-confirmed evidence visible while status refreshes', async () => {
        const user = userEvent.setup();
        let resolveRefresh: ((value: AgentTeamStatus) => void) | undefined;
        useAdminAccessMock.mockReturnValue({ hasAdminKey: false });

        renderWithProviders(<AgentTeamSetupMasterPage />);

        expect(await screen.findByText('delivery-team')).toBeVisible();
        agentServiceMock.getAgentTeamStatus.mockReturnValueOnce(new Promise(resolve => {
            resolveRefresh = resolve;
        }));
        await user.click(screen.getByRole('button', {
            name: i18n.t('actions.refresh'),
        }));

        expect(await screen.findByText(/^Refreshing · last confirmed/)).toBeVisible();
        expect(screen.getByRole('button', {
            name: i18n.t('actions.refreshing'),
        })).toBeDisabled();

        resolveRefresh?.(statusFixture);
        expect(await screen.findByRole('button', {
            name: i18n.t('actions.refresh'),
        })).toBeEnabled();
    });

    it('keeps the current blocker and runtime recovery reachable outside desktop rails', async () => {
        useAdminAccessMock.mockReturnValue({ hasAdminKey: false });

        renderWithProviders(<AgentTeamSetupMasterPage />);

        const mobileContext = await screen.findByRole('region', {
            name: i18n.t('agentTeamSetup.readinessTitle'),
        });
        expect(mobileContext).toHaveTextContent(
            i18n.t('agentTeamSetup.steps.master.title'),
        );
        expect(mobileContext).toHaveTextContent(
            i18n.t('agentTeamSetup.steps.master.action'),
        );
        expect(mobileContext).toHaveTextContent('minimum_workers_not_runtime_ready');
        expect(within(mobileContext).getByRole('progressbar', {
            name: i18n.t('agentTeamSetup.summaryProgress'),
        })).toHaveAttribute(
            'aria-valuetext',
            i18n.t('agentTeamSetup.checksComplete', { done: 1, total: 7 }),
        );
        expect(within(mobileContext).getByRole('progressbar'))
            .toHaveAttribute('aria-valuenow', '1');
        expect(within(mobileContext).getByRole('progressbar'))
            .toHaveAttribute('aria-valuemax', '7');
        expect(mobileContext.querySelectorAll(
            '.agent-team-mobile-steps .step-item',
        )).toHaveLength(7);
        const setupRail = screen.getByRole('complementary', {
            name: i18n.t('agentTeamSetup.readinessTitle'),
        });
        expect(within(setupRail).getByRole('progressbar', {
            name: i18n.t('agentTeamSetup.railProgress'),
        })).toHaveAttribute('aria-valuenow', '1');
        expect(within(setupRail).getByText(
            i18n.t('agentTeamSetup.steps.master.title'),
        ).closest('li')).toHaveAttribute('aria-current', 'step');

        const runtimeSummary = screen.getByRole('complementary', {
            name: i18n.t('agentTeamSetup.runtimeDetails'),
        }).querySelector('summary');
        expect(runtimeSummary).not.toBeNull();
        expect(runtimeSummary).toHaveTextContent(
            i18n.t('agentTeamSetup.statusScopes.runtime.states.blocked'),
        );
        expect(runtimeSummary).toHaveTextContent(
            i18n.t('agentTeamSetup.statusScopes.runtime.actions.blocked'),
        );
    });

    it('announces complete setup without leaving a false current check', async () => {
        useAdminAccessMock.mockReturnValue({ hasAdminKey: false });
        agentServiceMock.getAgentTeamStatus.mockResolvedValue({
            ...statusFixture,
            topology_state: 'active',
            runtime_ready: true,
            blocker_codes: [],
            steps: [
                'authority',
                'master',
                'controller',
                'workers',
                'bindings',
                'verifier',
                'review',
            ].map(id => ({
                id,
                state: 'done',
                blocker_codes: [],
                next_action: null,
            })),
        });

        renderWithProviders(<AgentTeamSetupMasterPage />);

        const completeContext = await screen.findByRole('region', {
            name: i18n.t('agentTeamSetup.readinessTitle'),
        });
        expect(within(completeContext).getByRole('heading', {
            level: 3,
            name: i18n.t('agentTeamSetup.setupComplete'),
        })).toBeVisible();
        expect(completeContext).toHaveTextContent(
            i18n.t('agentTeamSetup.allChecksCompleteBody'),
        );
        expect(within(completeContext).getByRole('progressbar'))
            .toHaveAttribute('aria-valuenow', '7');
        expect(within(completeContext).getByRole('progressbar'))
            .toHaveAttribute('aria-valuemax', '7');
        expect(completeContext).not.toHaveTextContent(
            i18n.t('agentTeamSetup.currentCheckNamed', {
                check: i18n.t('agentTeamSetup.steps.review.title'),
            }),
        );
        expect(document.querySelector(
            '.agent-team-step-groups [aria-current="step"]',
        )).not.toBeInTheDocument();
    });

    it('shows the labeled secret-free editor and exact planning actions to an operator', async () => {
        useAdminAccessMock.mockReturnValue({ hasAdminKey: true });
        agentServiceMock.getAgentTeamStatus.mockResolvedValue({
            ...statusFixture,
            can_mutate: true,
        });

        renderWithProviders(<AgentTeamSetupMasterPage />);

        const editor = await screen.findByRole('textbox', {
            name: i18n.t('agentTeamSetup.secretFreeJson'),
        });
        expect(editor).toBeEnabled();
        expect(editor).toHaveClass('agent-team-master-editor');
        expect(editor).toHaveAttribute('rows', '18');
        expect(screen.getByRole('button', {
            name: i18n.t('agentTeamSetup.import'),
        })).toBeEnabled();
        expect(screen.getByRole('button', {
            name: i18n.t('agentTeamSetup.validate'),
        })).toBeEnabled();
        expect(screen.queryByRole('main')).not.toBeInTheDocument();
        expect(screen.getByRole('region', {
            name: i18n.t('agentTeamSetup.workflowTitle'),
        })).toBeVisible();
        expect(screen.queryByText(/api_key/i)).not.toBeInTheDocument();
    });

    it('keeps shell landmarks page-owned and every exposed role uniquely named', async () => {
        useAdminAccessMock.mockReturnValue({ hasAdminKey: true });
        agentServiceMock.getAgentTeamStatus.mockResolvedValue({
            ...statusFixture,
            can_mutate: true,
        });

        const { container } = renderWithProviders(<AgentTeamSetupMasterPage />);

        expect(await screen.findByRole('textbox', {
            name: i18n.t('agentTeamSetup.secretFreeJson'),
        })).toBeVisible();
        expect(screen.queryByRole('main')).not.toBeInTheDocument();
        expect(screen.getAllByRole('complementary')).toHaveLength(2);
        const readinessRail = screen.getByRole('complementary', {
            name: i18n.t('agentTeamSetup.readinessTitle'),
        });
        expect(readinessRail).toBeVisible();
        expect(screen.getByRole('complementary', {
            name: i18n.t('agentTeamSetup.runtimeDetails'),
        })).toBeVisible();
        expect(screen.getByRole('region', {
            name: i18n.t('agentTeamSetup.statusScopes.label'),
        })).toBeVisible();
        const compactReadiness = screen.getByRole('region', {
            name: i18n.t('agentTeamSetup.readinessTitle'),
        });
        expect(compactReadiness).toBeVisible();
        expect(screen.getByRole('region', {
            name: i18n.t('agentTeamSetup.workflowTitle'),
        })).toBeVisible();
        expect(within(readinessRail).getByRole('heading', {
            level: 2,
            name: i18n.t('agentTeamSetup.readinessTitle'),
        })).toBeVisible();
        expect(within(compactReadiness).getByRole('heading', {
            level: 2,
            name: i18n.t('agentTeamSetup.readinessTitle'),
        })).toBeVisible();
        expect(screen.getByRole('heading', {
            level: 2,
            name: i18n.t('agentTeamSetup.workflowTitle'),
        })).toBeVisible();
        expect(screen.getByRole('heading', {
            level: 2,
            name: i18n.t('agentTeamSetup.runtimeDetails'),
        })).toBeVisible();
        expect(screen.getByRole('heading', {
            level: 3,
            name: i18n.t('agentTeamSetup.masterTitle'),
        })).toBeVisible();
        expect(accessibleNameViolations(container)).toEqual([]);
        expect(summaryNameViolations(container)).toEqual([]);
    });

    it('freezes the validated snapshot while validation is pending', async () => {
        const user = userEvent.setup();
        let resolveValidation: ((value: unknown) => void) | undefined;
        useAdminAccessMock.mockReturnValue({ hasAdminKey: true });
        agentServiceMock.getAgentTeamStatus.mockResolvedValue({
            ...statusFixture,
            can_mutate: true,
        });
        agentServiceMock.validateAgentTeamMaster.mockReturnValue(new Promise(resolve => {
            resolveValidation = resolve;
        }));

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

        expect(editor).toBeDisabled();
        expect(screen.getByRole('button', {
            name: i18n.t('agentTeamSetup.validating'),
        })).toBeDisabled();

        resolveValidation?.({
            schema_version: 'agent-team-validation-v1',
            valid: true,
            manifest_digest: 'b'.repeat(64),
            normalized_manifest: {
                schema_version: 'agent-team-master-v1',
                topology_key: 'delivery-team',
            },
            blocker_codes: [],
        });

        expect(await screen.findByRole('button', {
            name: i18n.t('agentTeamSetup.validate'),
        })).toBeEnabled();
        expect(editor).toBeEnabled();
    });

    it('clears a corrected local editor error immediately', async () => {
        const user = userEvent.setup();
        useAdminAccessMock.mockReturnValue({ hasAdminKey: true });
        agentServiceMock.getAgentTeamStatus.mockResolvedValue({
            ...statusFixture,
            can_mutate: true,
        });

        renderWithProviders(<AgentTeamSetupMasterPage />);

        const editor = await screen.findByRole('textbox', {
            name: i18n.t('agentTeamSetup.secretFreeJson'),
        });
        fireEvent.change(editor, { target: { value: '{' } });
        await user.click(screen.getByRole('button', {
            name: i18n.t('agentTeamSetup.validate'),
        }));
        expect(screen.getByRole('alert')).toHaveTextContent(
            i18n.t('agentTeamSetup.errorTitle'),
        );

        fireEvent.change(editor, {
            target: {
                value: JSON.stringify({
                    schema_version: 'agent-team-master-v1',
                    topology_key: 'delivery-team',
                }),
            },
        });
        expect(screen.queryByRole('alert')).not.toBeInTheDocument();
    });

    it('keeps member configuration, lifecycle, observation, and runtime facts separate', async () => {
        useAdminAccessMock.mockReturnValue({ hasAdminKey: false });
        agentServiceMock.getAgentTeamStatus.mockResolvedValue({
            ...statusFixture,
            members: [{
                actor_key: 'backend-worker',
                actor_id: 9,
                actor_name: 'backend-worker',
                display_name: 'Backend Worker',
                role: 'worker',
                desired: true,
                configured: true,
                lifecycle_state: 'connected',
                enabled: true,
                profile_key: 'backend',
                profile_revision: 'profile-rev-4',
                binding_revisions: { balanced: 3 },
                skill_package: {
                    name: 'workchord-worker',
                    version: '1.2.0',
                    sha256: 'b'.repeat(64),
                },
                package_acknowledged: true,
                credential_delivery_state: 'delivered',
                connection_state: 'stale',
                last_seen_at: '2026-08-04T09:30:00Z',
                queued_assignments: 2,
                accepted_assignments: 1,
                running_runs: 0,
                runtime_ready: false,
                availability: 'availability_unknown',
                blocker_codes: ['runtime_observation_stale'],
                handoff: {
                    schema_version: 'agent-team-runtime-handoff-v1',
                    topology_key: 'delivery-team',
                    topology_revision: 4,
                    actor_key: 'backend-worker',
                    actor_id: 9,
                    role: 'worker',
                    server_url: 'https://agents.example.test/backend-worker',
                    required_server_features: ['assignments'],
                    skill_package: {
                        name: 'workchord-worker',
                        version: '1.2.0',
                        sha256: 'b'.repeat(64),
                    },
                    profile_key: 'backend',
                    profile_revision: 'profile-rev-4',
                    model_binding_revisions: { balanced: 3 },
                    supported_assignment_modes: ['execute'],
                    startup_instructions: ['Start the worker'],
                    credential_ref: 'vault://workchord/backend-worker',
                },
            }],
        });

        renderWithProviders(<AgentTeamSetupMasterPage />);

        const member = (await screen.findByText('Backend Worker')).closest('section');
        expect(member).not.toBeNull();
        const memberView = within(member as HTMLElement);
        expect(memberView.getByText(
            i18n.t('agentTeamSetup.memberConfiguration'),
        )).toBeVisible();
        expect(memberView.getByText(
            i18n.t('agentTeamSetup.configured'),
        )).toBeVisible();
        expect(memberView.getByText(
            i18n.t('agentTeamSetup.statusScopes.runtime.states.blocked'),
        )).toBeVisible();
        expect(memberView.getByText(
            i18n.t('agentTeamSetup.connectionStates.stale'),
        )).toBeVisible();
        expect(memberView.getByText(
            i18n.t('agentTeamSetup.availabilityNotEvaluated'),
        )).toBeVisible();
        expect(memberView.getByText(
            i18n.t('agentTeamSetup.handoffFor', {
                actor: 'backend-worker',
                name: 'Backend Worker',
            }),
        ).closest('summary')).not.toBeNull();
        expect(member).not.toHaveTextContent('availability_unknown');
        expect(member).not.toHaveTextContent('runtime_ready');
    });

    it('keeps runtime disclosures unique when display names collide', async () => {
        useAdminAccessMock.mockReturnValue({ hasAdminKey: false });
        agentServiceMock.getAgentTeamStatus.mockResolvedValue({
            ...statusFixture,
            members: [
                runtimeMemberFixture('backend-worker-a', 9),
                runtimeMemberFixture('backend-worker-b', 10),
            ],
        });

        const { container } = renderWithProviders(<AgentTeamSetupMasterPage />);

        expect(await screen.findAllByText('Shared Worker Name')).toHaveLength(2);
        expect(screen.getByText(i18n.t('agentTeamSetup.handoffFor', {
            actor: 'backend-worker-a',
            name: 'Shared Worker Name',
        }))).toBeVisible();
        expect(screen.getByText(i18n.t('agentTeamSetup.handoffFor', {
            actor: 'backend-worker-b',
            name: 'Shared Worker Name',
        }))).toBeVisible();
        expect(summaryNameViolations(container)).toEqual([]);
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
            }, {
                action_id: 'safe-update-worker-2',
                action_digest: 'e'.repeat(64),
                reconciliation_class: 'safe_update',
                operation: 'update_member',
                actor_key: 'frontend-worker',
                target_actor_id: 10,
                expected_object_revision: 2,
                expected_actor_revision: 4,
                before: null,
                after: null,
                preconditions: {},
                blocker_code: null,
                requires_explicit_confirmation: false,
                authority_change: false,
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
            receipts: ['pending', 'applied', 'no_change', 'blocked'].map(
                (status, index) => ({
                    action_id: `receipt-${index}`,
                    action_digest: 'f'.repeat(64),
                    reconciliation_class: status === 'no_change'
                        ? 'no_change'
                        : 'safe_update',
                    operation: 'update_member',
                    actor_key: `worker-${index}`,
                    status,
                    target_actor_id: index + 1,
                    before_revision: 4,
                    after_revision: status === 'applied' ? 5 : null,
                    blocker_code: status === 'blocked' ? 'runtime_blocked' : null,
                    next_action: null,
                }),
            ),
            pending_action_ids: [],
            blocker_codes: [],
        });

        const { container } = renderWithProviders(<AgentTeamSetupMasterPage />);

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

        const actionName = i18n.t('agentTeamSetup.operations.updateMember');
        const apply = await screen.findByRole('button', {
            name: i18n.t('agentTeamSetup.applyActionFor', {
                action: actionName,
                actionId: 'safe-update-worker',
                actor: 'backend-worker',
            }),
        });
        const planHeading = screen.getByRole('heading', {
            level: 3,
            name: i18n.t('agentTeamSetup.planTitle'),
        });
        expect(planHeading).toHaveFocus();
        expect(planHeading).toHaveAttribute('tabindex', '-1');
        expect(planHeading).toHaveClass(
            'wc-master-section-title',
            'wc-master-focus-heading',
        );
        expect(screen.getByRole('region', {
            name: i18n.t('agentTeamSetup.actionHeadingFor', {
                action: actionName,
                actionId: 'safe-update-worker',
                actor: 'backend-worker',
            }),
        })).toBeVisible();
        expect(screen.getByRole('heading', {
            level: 4,
            name: i18n.t('agentTeamSetup.actionHeadingFor', {
                action: actionName,
                actionId: 'safe-update-worker',
                actor: 'backend-worker',
            }),
        })).toBeVisible();
        expect(screen.getByRole('region', {
            name: i18n.t('agentTeamSetup.actionHeadingFor', {
                action: actionName,
                actionId: 'safe-update-worker-2',
                actor: 'frontend-worker',
            }),
        })).toBeVisible();
        expect(accessibleNameViolations(container)).toEqual([]);
        await user.click(screen.getByRole('button', {
            name: i18n.t('agentTeamSetup.dryRun'),
        }));
        await waitFor(() => {
            expect(planHeading).toHaveFocus();
        });
        expect(agentServiceMock.planAgentTeamMaster).toHaveBeenCalledTimes(2);
        expect(screen.getAllByText(
            i18n.t('agentTeamSetup.reconciliationClasses.safeUpdate'),
        )).toHaveLength(2);
        expect(screen.queryByText('safe_update')).not.toBeInTheDocument();
        expect(apply).toBeDisabled();
        await user.click(screen.getByRole('checkbox', {
            name: i18n.t('agentTeamSetup.confirmActionFor', {
                action: actionName,
                actionId: 'safe-update-worker',
                actor: 'backend-worker',
            }),
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
        const receiptHeading = await screen.findByRole('heading', {
            level: 3,
            name: i18n.t('agentTeamSetup.receiptTitle'),
        });
        expect(receiptHeading).toHaveFocus();
        expect(receiptHeading).toHaveAttribute('tabindex', '-1');
        expect(receiptHeading).toHaveClass(
            'wc-master-section-title',
            'wc-master-focus-heading',
        );
        const receipt = receiptHeading.closest('section');
        expect(receipt).toHaveTextContent('e'.repeat(32));
        expect(receipt).toHaveTextContent(
            i18n.t('agentTeamSetup.applyStatuses.completed'),
        );
        expect(receipt).toHaveTextContent(
            i18n.t('agentTeamSetup.topologyRevision', { revision: 5 }),
        );
        expect(receipt).not.toHaveTextContent('completed');
        for (const status of ['pending', 'applied', 'noChange', 'blocked']) {
            expect(receipt).toHaveTextContent(
                i18n.t(`agentTeamSetup.actionStatuses.${status}`),
            );
        }
        expect(receipt?.querySelector('.pill.warn')).toHaveTextContent(
            i18n.t('agentTeamSetup.actionStatuses.pending'),
        );
        expect(receipt?.querySelector('.pill.opt')).toHaveTextContent(
            i18n.t('agentTeamSetup.actionStatuses.noChange'),
        );
        expect(receipt?.querySelector('.pill.blocked')).toHaveTextContent(
            i18n.t('agentTeamSetup.actionStatuses.blocked'),
        );
    });

    it('renders a late plan without stealing focus from a newer operator action', async () => {
        const user = userEvent.setup();
        let resolvePlan: ((value: unknown) => void) | undefined;
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
        agentServiceMock.planAgentTeamMaster.mockReturnValue(new Promise(resolve => {
            resolvePlan = resolve;
        }));

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

        const refresh = screen.getByRole('button', {
            name: i18n.t('actions.refresh'),
        });
        refresh.focus();
        await act(async () => {
            resolvePlan?.({
                schema_version: 'agent-team-reconciliation-plan-v1',
                topology_key: 'delivery-team',
                expected_topology_revision: 4,
                manifest_digest: 'b'.repeat(64),
                plan_digest: 'c'.repeat(64),
                blocker_codes: [],
                actions: [],
            });
        });

        expect(await screen.findByRole('heading', {
            level: 3,
            name: i18n.t('agentTeamSetup.planTitle'),
        })).toBeVisible();
        expect(refresh).toHaveFocus();
    });

    it('keeps focus on the initiating control when plan creation fails', async () => {
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
        agentServiceMock.planAgentTeamMaster.mockRejectedValue(
            new Error('Plan could not be created'),
        );

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
        const dryRun = await screen.findByRole('button', {
            name: i18n.t('agentTeamSetup.dryRun'),
        });
        await user.click(dryRun);

        expect(await screen.findByRole('alert')).toHaveTextContent(
            'Plan could not be created',
        );
        expect(screen.getByRole('button', {
            name: i18n.t('agentTeamSetup.dryRun'),
        })).toBe(dryRun);
        expect(dryRun).toHaveFocus();
    });

    it('keeps status retry mounted and focuses the recovered workflow', async () => {
        const user = userEvent.setup();
        let resolveStatus: ((value: AgentTeamStatus) => void) | undefined;
        useAdminAccessMock.mockReturnValue({ hasAdminKey: false });
        agentServiceMock.getAgentTeamStatus
            .mockRejectedValueOnce(new Error('status unavailable'))
            .mockReturnValueOnce(new Promise(resolve => {
                resolveStatus = resolve;
            }));

        renderWithProviders(<AgentTeamSetupMasterPage />);

        const retry = await screen.findByRole('button', {
            name: i18n.t('queryFeedback.retry'),
        });
        await user.click(retry);

        expect(screen.getByRole('button', {
            name: i18n.t('queryFeedback.retry'),
        })).toBe(retry);
        expect(retry).toBeDisabled();
        expect(retry).toHaveFocus();

        await act(async () => {
            resolveStatus?.(statusFixture);
        });

        await waitFor(() => {
            expect(screen.getByRole('region', {
                name: i18n.t('agentTeamSetup.workflowTitle'),
            })).toHaveFocus();
        });
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
            i18n.t('agentTeamSetup.statusUnavailableTitle'),
        );
        const readinessRail = screen.getByRole('complementary', {
            name: i18n.t('agentTeamSetup.readinessTitle'),
        });
        expect(within(readinessRail).queryByRole('progressbar')).not.toBeInTheDocument();
        expect(readinessRail.querySelectorAll('.step-item')).toHaveLength(0);
    });
});

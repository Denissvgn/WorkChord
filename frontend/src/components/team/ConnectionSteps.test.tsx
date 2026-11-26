import { screen } from '@testing-library/react';
import { describe, expect, it } from 'vitest';
import { renderWithProviders } from '../../test/renderWithProviders';
import type {
    AgentTeamMaster, AgentTeamMemberSpec, AgentTeamMemberStatus, AgentTeamRuntimeIdentityStatus,
} from '../../types/agent';
import { ConnectionSteps } from './ConnectionSteps';

const worker: AgentTeamMemberSpec = {
    actor_key: 'backend-worker', actor_name: 'workchord-backend-worker', display_name: 'Backend worker', role: 'worker',
    scope_preset: 'worker-v1', profile_key: 'worker-profile',
    skill_package: { name: 'workchord-worker', version: '1.8.0', sha256: 'a'.repeat(64) },
    assignment_modes: ['execution'], model_binding_keys: ['catalog-model'], default_model_binding_key: 'catalog-model',
    runtime_ref: 'runtime://codex/backend-worker', credential_ref: 'private-sink/backend-worker',
};
const manifest = {
    schema_version: 'agent-team-master-v1', topology_key: 'team', server_url: 'https://workchord.example', credential_sink_ref: 'private-sink',
    required_server_features: ['agent-team-master-v1'], controller: worker, workers: [worker], verifiers: [],
    readiness_policy: { minimum_execution_workers: 1, require_independent_verifier_when_assessed: true, maximum_runtime_staleness_seconds: 300 },
} as unknown as AgentTeamMaster;
const identity = (overrides: Partial<AgentTeamRuntimeIdentityStatus> = {}): AgentTeamRuntimeIdentityStatus => ({
    state: 'unknown', expected_instance_id: 'rti-expected', acknowledged_instance_id: null, previous_instance_id: null,
    changed_at: null, refused_instance_id: null, refused_at: null, ...overrides,
});
const status = (runtimeIdentity?: AgentTeamRuntimeIdentityStatus): AgentTeamMemberStatus => ({
    actor_key: worker.actor_key, actor_id: 9, actor_name: worker.actor_name, display_name: worker.display_name, role: 'worker',
    desired: true, configured: true, lifecycle_state: 'connected', enabled: true, profile_key: worker.profile_key, profile_revision: null,
    binding_revisions: {}, skill_package: worker.skill_package, package_acknowledged: true, acknowledgement_state: 'current',
    runtime_identity: runtimeIdentity,
    credential_delivery_state: 'delivered', connection_state: 'observed', last_seen_at: null, queued_assignments: 0,
    accepted_assignments: 0, running_runs: 0, runtime_ready: true, availability: 'availability_unknown', blocker_codes: [], handoff: null,
});
const render = (memberStatus: AgentTeamMemberStatus | undefined) => renderWithProviders(
    <ConnectionSteps manifest={manifest} member={worker} memberStatus={memberStatus} connected onCheck={() => {}} />,
);
const facts = () => screen.getByText('Runtime instance').closest('div') as HTMLElement;

describe('the runtime instance shown with the connection steps', () => {
    it('names the acknowledging runtime instance', () => {
        render(status(identity({ state: 'current', acknowledged_instance_id: 'rti-first' })));
        expect(facts()).toHaveAttribute('data-runtime-identity', 'current');
        expect(facts()).toHaveTextContent('Acknowledged by this runtime instance');
        expect(facts()).toHaveTextContent('rti-first');
    });

    it('says that the identity is unknown for an acknowledgement made before it existed', () => {
        render(status(undefined));
        expect(facts()).toHaveAttribute('data-runtime-identity', 'unknown');
        expect(facts()).toHaveTextContent('Identity unknown (not sent by the runtime)');
    });

    it('shows a second runtime taking the same seat as a change of identity', () => {
        render(status(identity({
            state: 'changed', acknowledged_instance_id: 'rti-second', previous_instance_id: 'rti-first', changed_at: '2026-11-26T10:00:00Z',
        })));
        expect(facts()).toHaveAttribute('data-runtime-identity', 'changed');
        expect(facts()).toHaveTextContent('Identity changed');
        expect(facts()).toHaveTextContent('rti-second');
        expect(facts()).toHaveTextContent(/Changed from rti-first at /);
    });

    it('shows a refused identity with the identity that was turned away', () => {
        render(status(identity({ state: 'refused', refused_instance_id: 'rti-other', refused_at: '2026-11-26T10:00:00Z' })));
        expect(facts()).toHaveAttribute('data-runtime-identity', 'refused');
        expect(facts()).toHaveTextContent(/Refused rti-other at /);
    });

    it('shows nothing for an agent that does not exist yet', () => {
        render(undefined);
        expect(screen.queryByText('Runtime instance')).not.toBeInTheDocument();
    });
});

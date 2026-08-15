import type { AgentTeamStatus } from '../../types/agent';

export type TopologyConfigurationState =
    | 'unavailable'
    | 'notConfigured'
    | 'reconciliationNeeded'
    | 'configured'
    | 'disabled';

export type SessionAuthorityState =
    | 'checking'
    | 'unverified'
    | 'readOnly'
    | 'changesAllowed';

export type RuntimeReadinessState =
    | 'unknown'
    | 'blocked'
    | 'onboarding'
    | 'ready'
    | 'disabled';

export interface AgentTeamStatusScopes {
    topology: TopologyConfigurationState;
    authority: SessionAuthorityState;
    runtime: RuntimeReadinessState;
}

export const deriveAgentTeamStatusScopes = ({
    status,
    isLoading,
}: {
    status: AgentTeamStatus | undefined;
    isLoading: boolean;
}): AgentTeamStatusScopes => {
    if (!status) {
        return {
            topology: 'unavailable',
            authority: isLoading ? 'checking' : 'unverified',
            runtime: 'unknown',
        };
    }

    const topology: TopologyConfigurationState = !status.topology_key
        ? 'notConfigured'
        : status.topology_state === 'disabled'
            ? 'disabled'
            : status.pending_action_ids.length > 0
                ? 'reconciliationNeeded'
                : 'configured';

    const runtime: RuntimeReadinessState = status.topology_state === 'disabled'
        ? 'disabled'
        : status.runtime_ready
            ? 'ready'
            : status.topology_state === 'onboarding'
                ? 'onboarding'
                : 'blocked';

    return {
        topology,
        authority: status.can_mutate ? 'changesAllowed' : 'readOnly',
        runtime,
    };
};

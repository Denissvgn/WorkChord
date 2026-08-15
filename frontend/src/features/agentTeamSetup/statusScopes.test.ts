import { describe, expect, it } from 'vitest';
import type { AgentTeamStatus } from '../../types/agent';
import { deriveAgentTeamStatusScopes } from './statusScopes';

const statusFixture = (
    overrides: Partial<AgentTeamStatus> = {},
): AgentTeamStatus => ({
    schema_version: 'agent-team-status-v1',
    topology_key: 'delivery-team',
    topology_revision: 4,
    manifest_digest: 'a'.repeat(64),
    topology_state: 'blocked',
    runtime_ready: false,
    availability: 'availability_unknown',
    blocker_codes: ['minimum_workers_not_runtime_ready'],
    steps: [],
    members: [],
    pending_action_ids: [],
    can_mutate: false,
    next_action: 'Acknowledge the worker runtime',
    ...overrides,
});

describe('agent-team status scopes', () => {
    it('keeps a configured topology independent from blocked runtime readiness', () => {
        expect(deriveAgentTeamStatusScopes({
            status: statusFixture(),
            isLoading: false,
        })).toEqual({
            topology: 'configured',
            authority: 'readOnly',
            runtime: 'blocked',
        });
    });

    it('derives session authority only from the confirmed status response', () => {
        expect(deriveAgentTeamStatusScopes({
            status: undefined,
            isLoading: true,
        }).authority).toBe('checking');
        expect(deriveAgentTeamStatusScopes({
            status: undefined,
            isLoading: false,
        }).authority).toBe('unverified');
        expect(deriveAgentTeamStatusScopes({
            status: statusFixture({ can_mutate: true }),
            isLoading: false,
        }).authority).toBe('changesAllowed');
    });

    it('reports pending reconciliation without changing the runtime fact', () => {
        expect(deriveAgentTeamStatusScopes({
            status: statusFixture({
                runtime_ready: true,
                topology_state: 'runtime_ready',
                pending_action_ids: ['replace-worker'],
            }),
            isLoading: false,
        })).toMatchObject({
            topology: 'reconciliationNeeded',
            runtime: 'ready',
        });
    });

    it('lets a disabled topology override contradictory runtime-ready evidence', () => {
        expect(deriveAgentTeamStatusScopes({
            status: statusFixture({
                topology_state: 'disabled',
                runtime_ready: true,
            }),
            isLoading: false,
        })).toMatchObject({
            topology: 'disabled',
            runtime: 'disabled',
        });
    });
});
